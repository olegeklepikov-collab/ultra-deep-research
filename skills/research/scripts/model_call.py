"""One bounded Hermes call with durable attempt and tool-free trace."""

from __future__ import annotations

import hashlib
import importlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any

try:
    from .file_io import (
        fsync_directory,
        load_json,
        new_private_directory,
        write_exclusive_bytes,
        write_exclusive_json,
    )
except ImportError:
    from file_io import (
        fsync_directory,
        load_json,
        new_private_directory,
        write_exclusive_bytes,
        write_exclusive_json,
    )

from hermes_research_report.beta_model import validate_tool_free_observation
from hermes_research_report.beta_modes import verify_beta_mode_plan
from hermes_research_report.canonical import sha256_json
from hermes_research_report.errors import ContractError

PROVIDER = "openrouter"
MODEL = "openai/gpt-5.4-nano"
MAX_WALL_SECONDS = 120
_SESSION_ID = re.compile(r"^[0-9]{8}_[0-9]{6}_[0-9a-f]+$")
_RESERVED = {
    "schema_version",
    "status",
    "run_id",
    "plan_receipt_hash",
    "bootstrap_budget_hash",
    "prompt_sha256",
    "provider",
    "model",
    "max_total_tokens",
    "max_estimated_cost_usd",
    "model_calls_limit",
    "retry_allowed",
}


class ModelCallError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def _code(error: BaseException) -> str:
    if isinstance(error, ContractError):
        return error.code
    if isinstance(error, subprocess.TimeoutExpired):
        return "model_outcome_unknown_reconcile_first"
    if (
        isinstance(error, ValueError)
        and str(error).replace("_", "").isalnum()
        and len(str(error)) < 80
    ):
        return str(error)
    return "model_input_or_storage_failed"


def run_tool_free_model(
    *,
    prompt: str,
    hermes: Path,
    output: Path,
    attempt_binding: dict[str, object],
    plan: object | None = None,
    bootstrap_budget: dict[str, object] | None = None,
) -> tuple[str, dict[str, Any], dict[str, Any]]:
    if (plan is None) == (bootstrap_budget is None) or set(attempt_binding) & _RESERVED:
        raise ModelCallError("model_attempt_binding_invalid")
    verified = verify_beta_mode_plan(plan) if plan is not None else None
    if verified is not None:
        if verified["schema_version"] != 2:
            raise ModelCallError("model_attempt_binding_invalid")
        run_id = verified["run_id"]
        limit = float(verified["limits"]["max_estimated_cost_usd"])
        wall_seconds = verified["limits"]["wall_seconds"]
        model_calls = verified["limits"]["model_calls"]
        binding = {"plan_receipt_hash": verified["receipt_hash"]}
    else:
        budget = bootstrap_budget
        if (
            type(budget) is not dict
            or set(budget)
            != {
                "schema_version",
                "run_id",
                "wall_seconds",
                "max_estimated_cost_usd",
                "model_calls",
            }
            or budget["schema_version"] != 1
            or type(budget["run_id"]) is not str
            or not re.fullmatch(r"^[A-Z][A-Z0-9-]{2,63}$", budget["run_id"])
            or type(budget["wall_seconds"]) is not int
            or not 1 <= budget["wall_seconds"] <= 60
            or type(budget["max_estimated_cost_usd"]) not in (int, float)
            or not 0 < budget["max_estimated_cost_usd"] <= 0.01
            or type(budget["model_calls"]) is not int
            or budget["model_calls"] != 1
        ):
            raise ModelCallError("planning_budget_invalid")
        run_id = budget["run_id"]
        limit = float(budget["max_estimated_cost_usd"])
        wall_seconds = budget["wall_seconds"]
        model_calls = 1
        binding = {"bootstrap_budget_hash": sha256_json(budget)}
    if (
        not hermes.is_absolute()
        or not hermes.is_file()
        or hermes.is_symlink()
        or not os.access(hermes, os.X_OK)
    ):
        raise ModelCallError("hermes_executable_invalid")
    token_limit = (
        30_000
        if verified is not None
        and verified["mode"] == "academic"
        and attempt_binding.get("source_scope") == "parsed_pdf_text_layout_unverified"
        and type(attempt_binding.get("fulltext_receipt_hash")) is str
        else 10_000
    )
    home = Path(os.environ.get("HERMES_HOME", ""))
    if not home.is_absolute() or not home.is_dir() or home.is_symlink():
        raise ModelCallError("hermes_home_invalid")
    try:
        from hermes_cli.config import load_config

        if load_config().get("fallback_model"):
            raise ValueError("model_fallback_route_not_bounded")
        model_tools = importlib.import_module("model_tools")
        if model_tools.get_tool_definitions(
            enabled_toolsets=["context_engine"], quiet_mode=True
        ):
            raise ValueError("model_tool_surface_not_empty")
    except (ImportError, ValueError) as error:
        raise ModelCallError(_code(error)) from None
    created = False
    try:
        new_private_directory(output)
        created = True
        attempt = {
            "schema_version": 1,
            "status": "started_unknown_until_reconciled",
            "run_id": run_id,
            **binding,
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "provider": PROVIDER,
            "model": MODEL,
            "max_total_tokens": token_limit,
            "max_estimated_cost_usd": limit,
            "model_calls_limit": model_calls,
            "retry_allowed": False,
            **attempt_binding,
        }
        write_exclusive_json(output / "attempt.json", attempt)
        usage_file = output / "model-usage.json"
        completed = subprocess.run(
            [
                str(hermes),
                "-z",
                prompt,
                "--provider",
                PROVIDER,
                "-m",
                MODEL,
                "--reasoning",
                "none",
                "-t",
                "context_engine",
                "--safe-mode",
                "--usage-file",
                str(usage_file),
            ],
            cwd=home,
            capture_output=True,
            text=True,
            check=False,
            timeout=min(wall_seconds, MAX_WALL_SECONDS),
            env={**os.environ, "HERMES_HOME": str(home)},
        )
        if usage_file.is_file():
            usage_file.chmod(0o600)
        if completed.returncode != 0 or not usage_file.is_file():
            raise ValueError("model_call_failed_reconcile_first")
        usage_value, _ = load_json(usage_file)
        if type(usage_value) is not dict:
            raise ValueError("model_usage_invalid")
        usage = usage_value
        session_id = usage.get("session_id")
        if type(session_id) is not str or not _SESSION_ID.fullmatch(session_id):
            raise ValueError("model_session_id_invalid")
        raw = completed.stdout.strip()
        if not raw or len(raw) > 5000:
            raise ValueError("model_response_invalid")
        write_exclusive_bytes(output / "model.raw.json", (raw + "\n").encode())
        exported = subprocess.run(
            [
                str(hermes),
                "sessions",
                "export",
                "--format",
                "jsonl",
                "--session-id",
                session_id,
                "-",
                "--dry-run",
            ],
            cwd=home,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
            env={**os.environ, "HERMES_HOME": str(home)},
        )
        if exported.returncode != 0 or len(exported.stdout) > 250_000:
            raise ValueError("model_trace_unavailable")
        trace = json.loads(exported.stdout)
        if type(trace) is not dict:
            raise ValueError("model_trace_invalid")
        write_exclusive_json(output / "model-trace.json", trace)
        validate_tool_free_observation(
            plan=verified,
            max_estimated_cost_usd=limit if verified is None else None,
            usage=usage,
            trace=trace,
            provider=PROVIDER,
            model=MODEL,
            max_total_tokens=token_limit,
        )
        fsync_directory(output)
        return raw, usage, trace
    except (
        ContractError,
        ImportError,
        OSError,
        ValueError,
        subprocess.TimeoutExpired,
    ) as error:
        code = _code(error)
        if created:
            try:
                write_exclusive_json(
                    output / "failure.json",
                    {
                        "schema_version": 1,
                        "status": "failed_or_unknown",
                        "reason_code": code,
                        "reconciliation_required": True,
                        "retry_allowed": False,
                    },
                )
            except (OSError, ValueError):
                pass
        raise ModelCallError(code) from None
