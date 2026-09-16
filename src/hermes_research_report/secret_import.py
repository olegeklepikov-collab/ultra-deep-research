"""User-authorized, value-free secret import planning and readback assessment."""

from __future__ import annotations

import re
from datetime import datetime
from typing import Any

from .canonical import with_receipt_hash
from .errors import (
    fail,
    require_bool,
    require_exact_keys,
    require_int,
    require_list,
    require_mapping,
    require_string,
)

SECRET_IMPORT_ASSESS_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "authorization",
        "source_binding",
        "target_binding",
        "mode",
        "items",
        "non_secret_assets",
    ],
    "properties": {
        "schema_version": {"const": 1},
        "authorization": {"type": "object"},
        "source_binding": {"type": "object"},
        "target_binding": {"type": "object"},
        "mode": {"enum": ["dry_run", "apply_readback", "rollback_readback"]},
        "items": {"type": "array", "items": {"type": "object"}},
        "non_secret_assets": {"type": "object"},
    },
}

_PROHIBITED_SECRET_IDS = {
    "SUDO_PASSWORD",
    "TELEGRAM_BOT_TOKEN",
    "TELEGRAM_ALLOWED_USERS",
    "TELEGRAM_HOME_CHANNEL",
    "TELEGRAM_HOME_CHANNEL_THREAD_ID",
}
_SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{0,127}$")
_SECRET_ID = re.compile(r"^[A-Z][A-Z0-9_]{0,127}$")
_STORE_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/:-]{0,255}$")
_PURPOSES = {
    "provider_or_model_access",
    "workspace_api_access",
    "telemetry_access",
}
_ROTATION_STATUSES = {"reuse_until_rotation", "rotation_required", "rotated"}


def _version(data: dict[str, object]) -> None:
    if data["schema_version"] != 1:
        fail(
            "unsupported_schema",
            "request.schema_version",
            "Поддерживается schema_version=1.",
        )


def _strings(value: object, path: str) -> list[str]:
    result = [
        require_string(item, f"{path}[{index}]")
        for index, item in enumerate(require_list(value, path))
    ]
    if len(result) != len(set(result)):
        fail("duplicate_item", path, "Повтор элемента запрещён.")
    return result


def _matched(value: object, path: str, pattern: re.Pattern[str]) -> str:
    text = require_string(value, path)
    if not pattern.fullmatch(text):
        fail("unsafe_identifier", path, "Идентификатор содержит запрещённые символы.")
    return text


def _timestamp(value: object, path: str) -> datetime:
    text = require_string(value, path)
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        fail("invalid_timestamp", path, "Нужна временная отметка ISO 8601.")
    if parsed.tzinfo is None:
        fail("timezone_required", path, "Временная зона обязательна.")
    return parsed


def assess_secret_import(request: object) -> dict[str, Any]:
    data = require_mapping(request, "request")
    require_exact_keys(
        data,
        {
            "schema_version",
            "authorization",
            "source_binding",
            "target_binding",
            "mode",
            "items",
            "non_secret_assets",
        },
        "request",
    )
    _version(data)
    authorization = require_mapping(data["authorization"], "request.authorization")
    require_exact_keys(
        authorization,
        {
            "authorization_id",
            "user_authorized",
            "issued_at",
            "expires_at",
            "source_instance_id",
            "target_instance_id",
            "allowed_secret_ids",
        },
        "request.authorization",
    )
    user_authorized = require_bool(
        authorization["user_authorized"], "request.authorization.user_authorized"
    )
    allowed_path = "request.authorization.allowed_secret_ids"
    allowed_items = _strings(authorization["allowed_secret_ids"], allowed_path)
    allowed = {
        _matched(secret_id, f"{allowed_path}[{index}]", _SECRET_ID)
        for index, secret_id in enumerate(allowed_items)
    }
    prohibited_authorized = sorted(allowed & _PROHIBITED_SECRET_IDS)
    if prohibited_authorized:
        fail(
            "prohibited_secret_authorization",
            "request.authorization.allowed_secret_ids",
            f"Запрещён перенос идентичности или привилегии: {prohibited_authorized[0]}.",
        )
    source = require_mapping(data["source_binding"], "request.source_binding")
    target = require_mapping(data["target_binding"], "request.target_binding")
    binding_fields = {"instance_id", "profile_id", "credential_store_ref"}
    require_exact_keys(source, binding_fields, "request.source_binding")
    require_exact_keys(target, binding_fields, "request.target_binding")
    source_instance = _matched(
        source["instance_id"], "request.source_binding.instance_id", _SAFE_ID
    )
    target_instance = _matched(
        target["instance_id"], "request.target_binding.instance_id", _SAFE_ID
    )
    source_profile = _matched(
        source["profile_id"], "request.source_binding.profile_id", _SAFE_ID
    )
    target_profile = _matched(
        target["profile_id"], "request.target_binding.profile_id", _SAFE_ID
    )
    source_store = _matched(
        source["credential_store_ref"],
        "request.source_binding.credential_store_ref",
        _STORE_REF,
    )
    target_store = _matched(
        target["credential_store_ref"],
        "request.target_binding.credential_store_ref",
        _STORE_REF,
    )
    if source_instance == target_instance:
        fail(
            "same_instance_binding",
            "request.target_binding.instance_id",
            "Источник и цель должны быть разными экземплярами.",
        )
    authorization_matches = source_instance == require_string(
        authorization["source_instance_id"],
        "request.authorization.source_instance_id",
    ) and target_instance == require_string(
        authorization["target_instance_id"],
        "request.authorization.target_instance_id",
    )
    mode = require_string(data["mode"], "request.mode")
    if mode not in {"dry_run", "apply_readback", "rollback_readback"}:
        fail("invalid_import_mode", "request.mode", "Неизвестен режим.")
    items = []
    secret_ids = set()
    blockers = []
    for index, raw in enumerate(require_list(data["items"], "request.items")):
        path = f"request.items[{index}]"
        item = require_mapping(raw, path)
        fields = {
            "secret_id",
            "purpose",
            "source_ref",
            "target_ref",
            "selected",
            "available",
            "scope_allowed",
            "target_instance_id",
            "target_profile_id",
            "permission_mode",
            "readback_verified",
            "rotation_status",
            "rollback_prepared",
            "rollback_verified",
        }
        require_exact_keys(item, fields, path)
        secret_id = _matched(item["secret_id"], f"{path}.secret_id", _SECRET_ID)
        if secret_id in secret_ids:
            fail("duplicate_secret", path, "Повтор секрета запрещён.")
        secret_ids.add(secret_id)
        if secret_id in _PROHIBITED_SECRET_IDS:
            blockers.append(f"prohibited_secret:{secret_id}")
        selected = require_bool(item["selected"], f"{path}.selected")
        available = require_bool(item["available"], f"{path}.available")
        scope_allowed = require_bool(item["scope_allowed"], f"{path}.scope_allowed")
        item_target_instance = require_string(
            item["target_instance_id"], f"{path}.target_instance_id"
        )
        item_target_profile = require_string(
            item["target_profile_id"], f"{path}.target_profile_id"
        )
        permission_mode = require_int(
            item["permission_mode"], f"{path}.permission_mode"
        )
        readback = require_bool(item["readback_verified"], f"{path}.readback_verified")
        rollback_prepared = require_bool(
            item["rollback_prepared"], f"{path}.rollback_prepared"
        )
        rollback_verified = require_bool(
            item["rollback_verified"], f"{path}.rollback_verified"
        )
        purpose = require_string(item["purpose"], f"{path}.purpose")
        if purpose not in _PURPOSES:
            fail(
                "invalid_secret_purpose", f"{path}.purpose", "Неизвестна цель секрета."
            )
        rotation_status = require_string(
            item["rotation_status"], f"{path}.rotation_status"
        )
        if rotation_status not in _ROTATION_STATUSES:
            fail(
                "invalid_rotation_status",
                f"{path}.rotation_status",
                "Неизвестен статус ротации.",
            )
        expected_source_ref = f"{source_store}#{secret_id}"
        expected_target_ref = f"{target_store}#{secret_id}"
        source_ref_matches = (
            require_string(item["source_ref"], f"{path}.source_ref")
            == expected_source_ref
        )
        target_ref_matches = (
            require_string(item["target_ref"], f"{path}.target_ref")
            == expected_target_ref
        )
        if selected:
            if secret_id not in allowed:
                blockers.append(f"secret_not_allowlisted:{secret_id}")
            if not available:
                blockers.append(f"secret_unavailable:{secret_id}")
            if not scope_allowed:
                blockers.append(f"secret_scope_denied:{secret_id}")
            if (
                item_target_instance != target_instance
                or item_target_profile != target_profile
            ):
                blockers.append(f"secret_binding_mismatch:{secret_id}")
            if permission_mode != 0o600:
                blockers.append(f"secret_permissions_invalid:{secret_id}")
            if not rollback_prepared:
                blockers.append(f"secret_rollback_unprepared:{secret_id}")
            if not source_ref_matches or not target_ref_matches:
                blockers.append(f"secret_reference_mismatch:{secret_id}")
            if mode == "apply_readback" and not readback:
                blockers.append(f"secret_readback_missing:{secret_id}")
            if mode == "rollback_readback" and not rollback_verified:
                blockers.append(f"secret_rollback_unverified:{secret_id}")
        items.append(
            {
                "secret_id": secret_id,
                "purpose": purpose,
                "source_ref": expected_source_ref,
                "target_ref": expected_target_ref,
                "selected": selected,
                "available": available,
                "scope_allowed": scope_allowed,
                "target_instance_id": item_target_instance,
                "target_profile_id": item_target_profile,
                "permission_mode": permission_mode,
                "readback_verified": readback,
                "rotation_status": rotation_status,
                "rollback_prepared": rollback_prepared,
                "rollback_verified": rollback_verified,
            }
        )
    non_secret = require_mapping(data["non_secret_assets"], "request.non_secret_assets")
    require_exact_keys(
        non_secret,
        {
            "sessions_copied",
            "memory_objects_copied",
            "work_items_copied",
            "operational_artifacts_copied",
            "identity_copied",
        },
        "request.non_secret_assets",
    )
    counts = {
        field: require_int(non_secret[field], f"request.non_secret_assets.{field}")
        for field in (
            "sessions_copied",
            "memory_objects_copied",
            "work_items_copied",
            "operational_artifacts_copied",
        )
    }
    identity_copied = require_bool(
        non_secret["identity_copied"], "request.non_secret_assets.identity_copied"
    )
    if any(counts.values()) or identity_copied:
        blockers.append("non_secret_or_identity_inheritance_detected")
    if not user_authorized:
        blockers.append("user_authorization_missing")
    if not authorization_matches:
        blockers.append("authorization_binding_mismatch")
    issued_at = _timestamp(
        authorization["issued_at"], "request.authorization.issued_at"
    )
    expires_at = _timestamp(
        authorization["expires_at"], "request.authorization.expires_at"
    )
    if expires_at <= issued_at:
        blockers.append("authorization_window_invalid")
    selected_count = sum(item["selected"] for item in items)
    if selected_count == 0:
        blockers.append("secret_selection_empty")
    ready = not blockers
    status = (
        "dry_run_ready"
        if ready and mode == "dry_run"
        else "import_verified"
        if ready and mode == "apply_readback"
        else "rollback_verified"
        if ready
        else "blocked"
    )
    return with_receipt_hash(
        {
            "contract": "SecretImportDecisionReceipt",
            "status": status,
            "authorization": {
                "authorization_id": _matched(
                    authorization["authorization_id"],
                    "request.authorization.authorization_id",
                    _SAFE_ID,
                ),
                "user_authorized": user_authorized,
                "issued_at": issued_at.isoformat(),
                "expires_at": expires_at.isoformat(),
                "source_instance_id": source_instance,
                "target_instance_id": target_instance,
                "allowed_secret_ids": sorted(allowed),
            },
            "source_binding": {
                "instance_id": source_instance,
                "profile_id": source_profile,
                "credential_store_ref": source_store,
            },
            "target_binding": {
                "instance_id": target_instance,
                "profile_id": target_profile,
                "credential_store_ref": target_store,
            },
            "mode": mode,
            "items": items,
            "selected_count": selected_count,
            "imported_count": selected_count if status == "import_verified" else 0,
            "rolled_back_count": selected_count if status == "rollback_verified" else 0,
            "non_secret_assets": {**counts, "identity_copied": identity_copied},
            "blockers": sorted(set(blockers)),
            "secret_values_accepted": False,
            "secret_hashes_recorded": False,
            "operational_state_inherited": False,
        }
    )
