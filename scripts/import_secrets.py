"""Import an explicit dotenv allowlist without evaluating or printing values."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import tempfile
from pathlib import Path

_LINE = re.compile(r"^[ \t]*(?:export[ \t]+)?([A-Za-z_][A-Za-z0-9_]*)[ \t]*=(.*)$")
_PROHIBITED = {
    "SUDO_PASSWORD",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_ALLOWED_USERS",
    "TELEGRAM_HOME_CHANNEL",
    "TELEGRAM_HOME_CHANNEL_THREAD_ID",
}


class ImportErrorSafe(ValueError):
    pass


def _regular_private(path: Path) -> None:
    if path.is_symlink():
        raise ImportErrorSafe("source_symlink_forbidden")
    try:
        info = path.stat()
    except OSError as error:
        raise ImportErrorSafe("source_unavailable") from error
    if not stat.S_ISREG(info.st_mode):
        raise ImportErrorSafe("source_not_regular")
    if stat.S_IMODE(info.st_mode) & 0o077:
        raise ImportErrorSafe("source_permissions_too_broad")


def _parse(path: Path) -> dict[str, str]:
    _regular_private(path)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ImportErrorSafe("source_read_failed") from error
    values: dict[str, str] = {}
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = _LINE.match(line)
        if not match:
            raise ImportErrorSafe("unsupported_dotenv_line")
        name, value = match.groups()
        if name in values:
            raise ImportErrorSafe("duplicate_secret_name")
        values[name] = value
    return values


def _selection(source: Path, allowlist: list[str]) -> dict[str, str]:
    if len(allowlist) != len(set(allowlist)):
        raise ImportErrorSafe("duplicate_allowlist_name")
    forbidden = sorted(set(allowlist) & _PROHIBITED)
    if forbidden:
        raise ImportErrorSafe("prohibited_secret_name")
    values = _parse(source)
    missing = sorted(set(allowlist) - set(values))
    if missing:
        raise ImportErrorSafe("allowlisted_secret_missing")
    return {name: values[name] for name in sorted(allowlist)}


def _serialized(selected: dict[str, str]) -> bytes:
    return (
        "\n".join(f"{name}={value}" for name, value in selected.items()) + "\n"
    ).encode("utf-8")


def _apply(target: Path, payload: bytes, selected: dict[str, str]) -> str:
    if target.is_symlink():
        raise ImportErrorSafe("target_symlink_forbidden")
    if target.exists():
        _regular_private(target)
        try:
            existing = target.read_bytes()
        except OSError as error:
            raise ImportErrorSafe("target_read_failed") from error
        if existing != payload:
            raise ImportErrorSafe("target_exists_with_different_content")
        return "already_applied"
    parent = target.parent
    if not parent.is_dir() or parent.is_symlink():
        raise ImportErrorSafe("target_parent_invalid")
    descriptor, temporary_name = tempfile.mkstemp(prefix=".secret-import-", dir=parent)
    temporary = Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        written = 0
        while written < len(payload):
            written += os.write(descriptor, payload[written:])
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = -1
        if target.exists() or target.is_symlink():
            raise ImportErrorSafe("target_appeared_during_import")
        os.replace(temporary, target)
        directory_fd = os.open(parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        readback = _parse(target)
        if readback != selected or stat.S_IMODE(target.stat().st_mode) != 0o600:
            raise ImportErrorSafe("target_readback_failed")
    finally:
        if descriptor >= 0:
            os.close(descriptor)
        if temporary.exists():
            temporary.unlink()
    return "applied"


def _rollback(target: Path, rollback_path: Path, selected: dict[str, str]) -> str:
    _regular_private(target)
    if _parse(target) != selected:
        raise ImportErrorSafe("rollback_target_content_mismatch")
    if rollback_path.exists() or rollback_path.is_symlink():
        raise ImportErrorSafe("rollback_target_exists")
    if rollback_path.parent != target.parent:
        raise ImportErrorSafe("rollback_must_share_parent")
    os.replace(target, rollback_path)
    directory_fd = os.open(target.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    return "rolled_back"


def run(
    source: Path,
    target: Path,
    allowlist: list[str],
    mode: str,
    rollback_path: Path | None = None,
) -> dict[str, object]:
    selected = _selection(source, allowlist)
    status = "dry_run_ready"
    if mode == "apply":
        status = _apply(target, _serialized(selected), selected)
    elif mode == "rollback":
        if rollback_path is None:
            raise ImportErrorSafe("rollback_path_missing")
        status = _rollback(target, rollback_path, selected)
    elif mode != "dry_run":
        raise ImportErrorSafe("invalid_mode")
    return {
        "status": status,
        "selected_secret_ids": sorted(selected),
        "selected_count": len(selected),
        "secret_values_emitted": False,
        "secret_hashes_emitted": False,
        "permission_mode": "0600",
        "operational_assets_copied": 0,
        "identity_copied": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--allow", action="append", default=[])
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dry-run", action="store_true")
    group.add_argument("--apply", action="store_true")
    group.add_argument("--rollback-to", type=Path)
    args = parser.parse_args(argv)
    mode = "apply" if args.apply else "rollback" if args.rollback_to else "dry_run"
    try:
        result = run(
            args.source,
            args.target,
            args.allow,
            mode,
            rollback_path=args.rollback_to,
        )
    except ImportErrorSafe as error:
        print(json.dumps({"status": "error", "code": str(error)}, sort_keys=True))
        return 2
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
