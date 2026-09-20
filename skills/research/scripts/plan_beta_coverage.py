"""Propose and seal a provisional atomic coverage frame before source calls."""

from __future__ import annotations

import argparse
import hashlib
import json
import secrets
import sys
from datetime import UTC, datetime
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "src"))

try:
    from .file_io import load_json, write_exclusive_json
    from .model_call import ModelCallError, run_tool_free_model
except ImportError:
    from file_io import load_json, write_exclusive_json
    from model_call import ModelCallError, run_tool_free_model

from hermes_research_report.beta_coverage_planner import (
    build_coverage_prompt,
    parse_coverage_proposal,
)
from hermes_research_report.beta_modes import validate_public_question
from hermes_research_report.canonical import with_receipt_hash
from hermes_research_report.errors import ContractError


def persist_coverage_result(
    *,
    output: Path,
    run_id: str,
    profile: str,
    question: str,
    raw: str,
    usage: dict,
    trace: dict,
    decomposition: object | None = None,
    reconciled: bool = False,
) -> tuple[dict, dict]:
    frame, proposal = parse_coverage_proposal(
        raw,
        question=question,
        profile=profile,
        run_id=run_id,
        decomposition=decomposition,
    )
    receipt = with_receipt_hash(
        {
            "schema_version": 1,
            "contract": "BetaCoveragePlanningRun",
            "run_id": run_id,
            "profile": profile,
            "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
            "frame_receipt_hash": frame["receipt_hash"],
            "proposal_receipt_hash": proposal["receipt_hash"],
            "decomposition_receipt_hash": frame.get("decomposition_receipt_hash"),
            "reported_model_cost_usd": usage["estimated_cost_usd"],
            "model_session_id": usage["session_id"],
            "model_trace_message_count": len(trace["messages"]),
            "reconciled_without_new_model_call": reconciled,
            "additional_model_calls": 0,
            "independent_review_status": "not_performed",
            "source_calls": 0,
            "release_authorized": False,
        }
    )
    write_exclusive_json(output / "frame.json", frame)
    write_exclusive_json(output / "proposal.json", proposal)
    write_exclusive_json(output / "planning-run.json", receipt)
    return frame, receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument(
        "--profile", choices=("search", "deep", "ultra", "academic"), required=True
    )
    parser.add_argument("--hermes", type=Path, required=True)
    parser.add_argument("--decomposition", type=Path)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--public-query-ack", action="store_true")
    args = parser.parse_args(argv)
    if not args.public_query_ack:
        print(
            json.dumps({"status": "error", "code": "public_query_ack_required"}),
            file=sys.stderr,
        )
        return 2
    output: Path | None = None
    run_id: str | None = None
    model_completed = False
    try:
        question = validate_public_question(args.question)
        decomposition = None
        if args.decomposition is not None:
            decomposition, _ = load_json(args.decomposition)
        if (
            not args.output_root.is_absolute()
            or args.output_root.is_symlink()
            or not args.output_root.is_dir()
        ):
            raise ValueError("coverage_output_root_invalid")
        run_id = (
            f"BETA-COV-{datetime.now(UTC):%Y%m%d-%H%M%S}-{secrets.token_hex(4).upper()}"
        )
        output = args.output_root / f"{run_id}-coverage-planning"
        assert output is not None
        budget: dict[str, object] = {
            "schema_version": 1,
            "run_id": run_id,
            "wall_seconds": 60,
            "max_estimated_cost_usd": 0.01,
            "model_calls": 1,
        }
        raw, usage, trace = run_tool_free_model(
            bootstrap_budget=budget,
            prompt=build_coverage_prompt(
                question=question, profile=args.profile, decomposition=decomposition
            ),
            hermes=args.hermes,
            output=output,
            attempt_binding={
                "purpose": "provisional_coverage_frame",
                "profile": args.profile,
                "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
                **(
                    {"decomposition_receipt_hash": decomposition["receipt_hash"]}
                    if type(decomposition) is dict
                    else {}
                ),
            },
        )
        model_completed = True
        frame, _receipt = persist_coverage_result(
            output=output,
            run_id=run_id,
            profile=args.profile,
            question=question,
            raw=raw,
            usage=usage,
            trace=trace,
            decomposition=decomposition,
        )
        print(
            json.dumps(
                {
                    "status": "provisional_frame",
                    "run_id": run_id,
                    "output": str(output),
                    "facet_count": len(frame["facets"]),
                    "atom_count": len(frame["atoms"]),
                    "model_cost_usd": usage["estimated_cost_usd"],
                    "source_calls": 0,
                    "release_authorized": False,
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, ModelCallError, OSError, ValueError, KeyError) as error:
        code = (
            error.code
            if isinstance(error, (ContractError, ModelCallError))
            else str(error)
            if isinstance(error, ValueError)
            else "coverage_planning_failed"
        )
        if model_completed and output is not None:
            try:
                write_exclusive_json(
                    output / "failure.json",
                    {
                        "schema_version": 1,
                        "status": "failed_after_model_response",
                        "reason_code": code,
                        "reconciliation_required": True,
                        "retry_allowed": False,
                    },
                )
            except (OSError, ValueError):
                pass
        print(
            json.dumps({"status": "error", "code": code, "run_id": run_id}),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
