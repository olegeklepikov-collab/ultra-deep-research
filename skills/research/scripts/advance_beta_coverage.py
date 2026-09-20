"""Run one bounded domain-grounded adaptive web batch for an open atom."""

from __future__ import annotations

import argparse
import hashlib
import json
import stat
import subprocess
import sys
from pathlib import Path
from typing import Any, cast

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "src"))

try:
    from .file_io import (
        load_json,
        new_private_directory,
        read_private_bytes,
        write_exclusive_json,
    )
    from .model_call import MODEL, PROVIDER, ModelCallError, run_tool_free_model
except ImportError:
    from file_io import (
        load_json,
        new_private_directory,
        read_private_bytes,
        write_exclusive_json,
    )
    from model_call import MODEL, PROVIDER, ModelCallError, run_tool_free_model

from hermes_research_report.beta_domain_source import (
    build_domain_web_prompt,
    observe_domain_web_batch,
    parse_domain_web_query,
)
from hermes_research_report.beta_model import validate_tool_free_observation
from hermes_research_report.beta_modes import verify_beta_mode_plan
from hermes_research_report.canonical import verify_receipt_hash, with_receipt_hash
from hermes_research_report.errors import ContractError

SCRIPTS = Path(__file__).resolve().parent


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frame", type=Path, required=True)
    parser.add_argument("--decomposition", type=Path, required=True)
    parser.add_argument("--atom-id", required=True)
    parser.add_argument("--batch", type=int, required=True)
    parser.add_argument("--parent-run-id")
    parser.add_argument("--hermes", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--public-query-ack", action="store_true")
    parser.add_argument("--resume-saved", action="store_true")
    args = parser.parse_args(argv)
    if not args.public_query_ack:
        print(
            json.dumps({"status": "error", "code": "public_query_ack_required"}),
            file=sys.stderr,
        )
        return 2
    output: Path | None = None
    model_completed = False
    try:
        frame, _ = load_json(args.frame)
        decomposition, _ = load_json(args.decomposition)
        if (
            type(frame) is not dict
            or type(decomposition) is not dict
            or not all(verify_receipt_hash(row) for row in (frame, decomposition))
            or not args.output_root.is_absolute()
            or args.output_root.is_symlink()
            or not args.output_root.is_dir()
            or args.frame
            != args.output_root / f"{frame['run_id']}-coverage-planning/frame.json"
            or args.decomposition
            != args.output_root
            / f"{decomposition['run_id']}-domain-planning/decomposition.json"
            or not 1 <= args.batch <= 99
        ):
            raise ValueError("adaptive_coverage_paths_invalid")
        parent_plan = None
        if args.parent_run_id is not None:
            plan_value, _ = load_json(
                args.output_root / f"{args.parent_run_id}-planning/plan.json"
            )
            parent_plan = verify_beta_mode_plan(plan_value)
            if (
                parent_plan["run_id"] != args.parent_run_id
                or parent_plan["mode"] != "ultra"
                or parent_plan["question"] != frame["question"]
            ):
                raise ValueError("adaptive_parent_plan_invalid")
        prefix = args.parent_run_id or frame["run_id"]
        suffix = "C" if args.parent_run_id else "D"
        previous = None
        if args.batch > 1:
            previous, _ = load_json(
                args.output_root
                / f"{prefix}-{suffix}{args.batch - 1:02d}-domain-web-observed/observations.json"
            )
        prompt = build_domain_web_prompt(
            frame, decomposition, None, atom_id=args.atom_id
        )
        batch_run_id = f"{prefix}-{suffix}{args.batch:02d}"
        output = args.output_root / f"{batch_run_id}-domain-web-plan"
        assert output is not None
        if args.resume_saved:
            if (
                not output.is_dir()
                or output.is_symlink()
                or stat.S_IMODE(output.stat().st_mode) & 0o077
                or (output / "plan.json").exists()
            ):
                raise ValueError("adaptive_recovery_target_invalid")
            attempt, _ = load_json(output / "attempt.json")
            failure, _ = load_json(output / "failure.json")
            usage, _ = load_json(output / "model-usage.json")
            trace, _ = load_json(output / "model-trace.json")
            raw = (
                read_private_bytes(output / "model.raw.json", maximum=1_048_576)
                .decode("utf-8")
                .rstrip("\n")
            )
            if any(type(row) is not dict for row in (attempt, failure, usage, trace)):
                raise ValueError("adaptive_recovery_record_invalid")
            attempt = cast(dict[str, Any], attempt)
            failure = cast(dict[str, Any], failure)
            usage = cast(dict[str, Any], usage)
            trace = cast(dict[str, Any], trace)
            if (
                attempt.get("purpose") != "adaptive_domain_coverage_query"
                or attempt.get("frame_receipt_hash") != frame["receipt_hash"]
                or attempt.get("decomposition_receipt_hash")
                != decomposition["receipt_hash"]
                or attempt.get("atom_id") != args.atom_id
                or attempt.get("batch_number") != args.batch
                or attempt.get("parent_plan_receipt_hash")
                != (parent_plan["receipt_hash"] if parent_plan else None)
                or attempt.get("prompt_sha256")
                != hashlib.sha256(prompt.encode()).hexdigest()
                or attempt.get("provider") != PROVIDER
                or attempt.get("model") != MODEL
                or attempt.get("retry_allowed") is not False
                or failure.get("reconciliation_required") is not True
                or failure.get("retry_allowed") is not False
                or type(trace.get("messages")) is not list
                or len(trace["messages"]) != 2
                or trace["messages"][0].get("content") != prompt
                or trace["messages"][1].get("content", "").strip() != raw
            ):
                raise ValueError("adaptive_recovery_lineage_invalid")
            validate_tool_free_observation(
                max_estimated_cost_usd=0.01,
                usage=usage,
                trace=trace,
                provider=PROVIDER,
                model=MODEL,
                max_total_tokens=attempt["max_total_tokens"],
            )
        else:
            raw, usage, trace = run_tool_free_model(
                bootstrap_budget={
                    "schema_version": 1,
                    "run_id": batch_run_id,
                    "wall_seconds": 60,
                    "max_estimated_cost_usd": 0.01,
                    "model_calls": 1,
                },
                prompt=prompt,
                hermes=args.hermes,
                output=output,
                attempt_binding={
                    "purpose": "adaptive_domain_coverage_query",
                    "frame_receipt_hash": frame["receipt_hash"],
                    "decomposition_receipt_hash": decomposition["receipt_hash"],
                    "atom_id": args.atom_id,
                    "batch_number": args.batch,
                    "parent_plan_receipt_hash": parent_plan["receipt_hash"]
                    if parent_plan
                    else None,
                },
            )
        model_completed = True
        plan, batch = parse_domain_web_query(
            raw,
            frame=frame,
            decomposition=decomposition,
            review=None,
            atom_id=args.atom_id,
            batch_number=args.batch,
            batch_run_id=batch_run_id,
        )
        run = with_receipt_hash(
            {
                "schema_version": 1,
                "contract": "BetaDomainWebPlanningRun",
                "run_id": batch_run_id,
                "batch_receipt_hash": batch["receipt_hash"],
                "plan_receipt_hash": plan["receipt_hash"],
                "model_session_id": usage["session_id"],
                "reported_model_cost_usd": usage["estimated_cost_usd"],
                "model_trace_message_count": len(trace["messages"]),
                "reconciled_without_new_model_call": args.resume_saved,
                "additional_model_calls": 0 if args.resume_saved else 1,
                "source_calls": 0,
                "release_authorized": False,
            }
        )
        write_exclusive_json(output / "plan.json", plan)
        write_exclusive_json(output / "batch.json", batch)
        write_exclusive_json(output / "run.json", run)
        child = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "execute_beta_sources.py"),
                "--plan",
                str(output / "plan.json"),
                "--output-root",
                str(args.output_root),
                "--public-query-ack",
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=plan["limits"]["wall_seconds"] + 10,
        )
        if child.returncode not in (0, 3):
            raise ValueError("adaptive_source_execution_incomplete")
        execution, _ = load_json(
            args.output_root / f"{batch_run_id}-execution/execution.json"
        )
        portfolio, _ = load_json(
            args.output_root / f"{batch_run_id}-execution/portfolio.json"
        )
        capture, _ = load_json(args.output_root / f"{batch_run_id}/capture.json")
        if any(type(row) is not dict for row in (execution, portfolio, capture)):
            raise ValueError("adaptive_source_receipts_invalid")
        execution = cast(dict[str, Any], execution)
        portfolio = cast(dict[str, Any], portfolio)
        capture = cast(dict[str, Any], capture)
        observations, progress, observed = observe_domain_web_batch(
            frame=frame,
            review=None,
            plan=plan,
            batch=batch,
            execution=execution,
            portfolio=portfolio,
            capture=capture,
            previous_observations=previous,
        )
        observed_dir = args.output_root / f"{batch_run_id}-domain-web-observed"
        new_private_directory(observed_dir)
        write_exclusive_json(observed_dir / "observations.json", observations)
        write_exclusive_json(observed_dir / "coverage.json", progress)
        write_exclusive_json(observed_dir / "batch-observation.json", observed)
        receipt = with_receipt_hash(
            {
                "schema_version": 1,
                "contract": "BetaAdaptiveCoverageBatchRun",
                "run_id": batch_run_id,
                "atom_id": args.atom_id,
                "frame_receipt_hash": frame["receipt_hash"],
                "parent_run_id": args.parent_run_id,
                "parent_plan_receipt_hash": parent_plan["receipt_hash"]
                if parent_plan
                else None,
                "batch_plan_receipt_hash": batch["receipt_hash"],
                "execution_receipt_hash": execution["receipt_hash"],
                "observation_receipt_hash": observed["receipt_hash"],
                "reported_model_cost_usd": usage["estimated_cost_usd"],
                "reconciled_without_new_model_call": args.resume_saved,
                "additional_model_calls": 0 if args.resume_saved else 1,
                "reported_source_cost_usd": execution.get("reported_total_cost_usd"),
                "verified_source_count": 0,
                "saturation_verified": False,
                "release_authorized": False,
            }
        )
        write_exclusive_json(observed_dir / "run.json", receipt)
        print(
            json.dumps(
                {
                    "status": "adaptive_coverage_partial",
                    "run_id": batch_run_id,
                    "atom_id": args.atom_id,
                    "candidate_count": observed["candidate_count"],
                    "verified_source_count": 0,
                    "reported_model_cost_usd": usage["estimated_cost_usd"],
                    "additional_model_calls": 0 if args.resume_saved else 1,
                    "reported_source_cost_usd": execution.get(
                        "reported_total_cost_usd"
                    ),
                    "saturation_verified": False,
                    "release_authorized": False,
                },
                sort_keys=True,
            )
        )
        return 0
    except (
        ContractError,
        ModelCallError,
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.TimeoutExpired,
    ) as error:
        code = (
            error.code
            if isinstance(error, (ContractError, ModelCallError))
            else str(error)
        )
        if (
            model_completed
            and output is not None
            and not (output / "plan.json").exists()
        ):
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
        print(json.dumps({"status": "error", "code": code}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
