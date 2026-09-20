"""One bounded model proposal becomes a deterministic autonomous beta plan."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from typing import Any

from .beta_modes import (
    ARXIV_VERSIONED_ID,
    build_beta_mode_plan,
    validate_public_protocol_rule,
    validate_public_question,
)
from .canonical import sha256_json, with_receipt_hash
from .errors import (
    fail,
    require_exact_keys,
    require_list,
    require_mapping,
    require_string,
)

_LIMITS = {
    "search": (2, 3, 2, 120, 0.02),
    "deep": (8, 16, 4, 600, 0.20),
    "ultra": (16, 32, 8, 1200, 0.50),
    "academic": (12, 40, 64, 3600, 0.30),
}
_FAMILIES = ("web", "scholarly_index", "preprint_archive")


def build_planning_prompt(*, question: str, mode: str) -> str:
    question = validate_public_question(question)
    if mode not in _LIMITS:
        fail("invalid_mode", "mode", "Неизвестный режим.")
    minimum = {"search": 1, "deep": 2, "ultra": 3, "academic": 2}[mode]
    return (
        "Постройте ограниченный план исследования, но НЕ ищите источники и НЕ отвечайте "
        "на вопрос. Верните ровно один JSON с полями leaves, rival_hypotheses, "
        "protocol. leaves — массив объектов с ровно leaf_id, query, source_family, "
        "concept_groups. concept_groups — массив из 1–8 массивов строковых синонимов "
        '(например, [["происхождение", "источник"], ["метаданные"]]); '
        "не используйте объекты внутри групп. Каждая группа должна "
        "быть представлена в будущем источнике; разделяйте предметные понятия, чтобы "
        "один общий термин не давал ложную релевантность. Формулируйте термины на языке "
        "ожидаемого источника и запроса: для английского поиска в каждой группе нужен "
        "хотя бы один английский термин. Не создавайте отдельную группу из слов "
        "«определение», «документация» или «модель данных», если они не являются "
        "предметом ответа; для простого Search достаточно двух предметных групп. "
        "Допустимые source_family: "
        f"{', '.join(_FAMILIES)}. leaf_id пишите как LEAF-001, LEAF-002 и далее. "
        f"Нужно не менее {minimum} листьев и стольких же "
        "разных семейств для режима, кроме Search, где достаточно одного web. "
        "Для preprint_archive query должен начинаться с all:, ti:, abs:, au: или cat: "
        "без пробела после двоеточия; если в вопросе указан ID arXiv с версией vN, "
        "используйте id_list:IDvN. Для web и "
        "scholarly_index пишите обычные поисковые слова без префиксов arXiv. "
        "Для Ultra дайте две конкурирующие "
        "rival_hypotheses, для остальных — пустой массив. Для Academic protocol — "
        "объект с ровно search_rule, screening_rule, synthesis_rule, reporting_rule; "
        "для остальных protocol=null. Не добавляйте секреты, URL, полномочия, "
        "запросы к людям или действия вне анализа.\n\n"
        f"РЕЖИМ: {mode}\nВОПРОС: {question}"
    )


def parse_planning_proposal(
    raw: str,
    *,
    question: str,
    mode: str,
    run_id: str,
    observed_at: datetime | None = None,
) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any]]:
    question = validate_public_question(question)
    if mode not in _LIMITS or type(raw) is not str or not 0 < len(raw) <= 12_000:
        fail("planning_response_invalid", "raw", "Ответ планировщика вне границ.")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                fail("planning_duplicate_key", "raw", "Повтор поля JSON запрещён.")
            result[key] = value
        return result

    try:
        value = json.loads(
            raw,
            object_pairs_hook=pairs,
            parse_constant=lambda _item: fail(
                "planning_nonfinite", "raw", "Нечисловая константа."
            ),
        )
    except json.JSONDecodeError:
        fail("planning_response_invalid", "raw", "Нужен один объект JSON.")
    proposal = require_mapping(value, "proposal")
    require_exact_keys(proposal, {"leaves", "rival_hypotheses", "protocol"}, "proposal")
    raw_leaves = require_list(proposal["leaves"], "proposal.leaves")
    raw_rivals = require_list(proposal["rival_hypotheses"], "proposal.rival_hypotheses")
    rivals: list[str] = []
    normalized_rival_objects = 0
    for index, raw_rival in enumerate(raw_rivals):
        if type(raw_rival) is dict:
            wrapped = require_mapping(raw_rival, f"proposal.rival_hypotheses[{index}]")
            require_exact_keys(
                wrapped,
                {"name", "hypothesis"},
                f"proposal.rival_hypotheses[{index}]",
            )
            require_string(wrapped["name"], f"proposal.rival_hypotheses[{index}].name")
            raw_rival = wrapped["hypothesis"]
            normalized_rival_objects += 1
        rivals.append(require_string(raw_rival, f"proposal.rival_hypotheses[{index}]"))
    leaves = []
    normalized_groups = 0
    normalized_duplicate_terms = 0
    route_normalizations: list[str] = []
    versioned_ids = set(ARXIV_VERSIONED_ID.findall(question))
    original_queries: dict[str, str] = {}
    for index, raw_leaf in enumerate(raw_leaves):
        leaf = require_mapping(raw_leaf, f"proposal.leaves[{index}]")
        if "concept_groups" not in leaf:
            fail(
                "concept_groups_required",
                f"proposal.leaves[{index}]",
                "Нужны группы понятий.",
            )
        require_exact_keys(
            leaf,
            {"leaf_id", "query", "source_family", "concept_groups"},
            f"proposal.leaves[{index}]",
        )
        groups = require_list(
            leaf["concept_groups"], f"proposal.leaves[{index}].concept_groups"
        )
        clean_groups = []
        seen_terms: set[str] = set()
        for group_index, group in enumerate(groups):
            if type(group) is dict:
                wrapped = require_mapping(
                    group, f"proposal.leaves[{index}].concept_groups[{group_index}]"
                )
                require_exact_keys(wrapped, {"synonyms"}, "proposal.concept_group")
                terms = wrapped["synonyms"]
                normalized_groups += 1
            else:
                terms = group
            raw_terms = require_list(
                terms, f"proposal.leaves[{index}].concept_groups[{group_index}]"
            )
            deduplicated = []
            for term in raw_terms:
                if type(term) is str:
                    key = term.strip().casefold()
                    if key in seen_terms:
                        normalized_duplicate_terms += 1
                        continue
                    seen_terms.add(key)
                deduplicated.append(term)
            if deduplicated:
                clean_groups.append(deduplicated)
        family = require_string(
            leaf["source_family"], f"proposal.leaves[{index}].source_family"
        )
        leaf_id = require_string(leaf["leaf_id"], f"proposal.leaves[{index}].leaf_id")
        query = require_string(leaf["query"], f"proposal.leaves[{index}].query").strip()
        original_queries[leaf_id] = query
        if (
            family == "preprint_archive"
            and query.startswith("id_list:")
            and len(versioned_ids) != 1
        ):
            fail(
                "unrequested_versioned_id",
                f"proposal.leaves[{index}].query",
                "Точный ID должен присутствовать в вопросе.",
            )
        if family == "preprint_archive" and len(versioned_ids) == 1:
            exact_query = "id_list:" + next(iter(versioned_ids))
            if query != exact_query:
                route_normalizations.append(
                    f"{leaf['leaf_id']}:arxiv_versioned_id_from_question"
                )
            query = exact_query
            leaves.append({**leaf, "query": query, "concept_groups": clean_groups})
            continue
        if family == "preprint_archive" and re.match(r"(?i)^arxiv:\s*", query):
            query = re.sub(r"(?i)^arxiv:\s*", "", query, count=1)
            route_normalizations.append(f"{leaf['leaf_id']}:arxiv_label_removed")
        arxiv_prefix = re.match(r"^(all|ti|abs|au|cat):\s*", query)
        if family == "preprint_archive" and arxiv_prefix is not None:
            tail = query[arxiv_prefix.end() :]
            if not tail:
                fail(
                    "preprint_query_not_structured",
                    f"proposal.leaves[{index}].query",
                    "Пустой запрос arXiv.",
                )
            normalized = arxiv_prefix.group(1) + ":" + tail
            if normalized != query:
                route_normalizations.append(
                    f"{leaf['leaf_id']}:arxiv_colon_space_removed"
                )
            query = normalized
        elif family == "preprint_archive" and not re.match(r"^[A-Za-z]+:", query):
            plain_query = re.sub(r":(?=\s)", " ", query)
            plain_query = re.sub(r"\s+", " ", plain_query).strip()
            if plain_query != query:
                route_normalizations.append(
                    f"{leaf['leaf_id']}:arxiv_title_colon_removed"
                )
            query = "all:" + plain_query
            route_normalizations.append(f"{leaf['leaf_id']}:arxiv_all_prefix_added")
        elif family in {"web", "scholarly_index"} and arxiv_prefix is not None:
            query = query[arxiv_prefix.end() :].strip()
            if not query:
                fail(
                    "search_query_empty_after_prefix",
                    f"proposal.leaves[{index}].query",
                    "Пустой поисковый запрос.",
                )
            route_normalizations.append(f"{leaf['leaf_id']}:arxiv_prefix_removed")
        leaves.append({**leaf, "query": query, "concept_groups": clean_groups})
    if (
        mode == "academic"
        and len(versioned_ids) == 1
        and len(leaves) >= 2
        and {leaf["source_family"] for leaf in leaves} == {"preprint_archive"}
    ):
        secondary = leaves[-1]
        original = original_queries[secondary["leaf_id"]]
        plain = re.sub(r"(?i)^(?:all|ti|abs|au|cat):\s*", "", original)
        plain = re.sub(r"(?i)\b(?:all|ti|abs|au|cat):\s*", " ", plain)
        plain = re.sub(
            r"(?i)\barxiv\s*:\s*" + re.escape(next(iter(versioned_ids))),
            " ",
            plain,
        )
        plain = " ".join(re.sub(r"[;:]+", " ", plain).split())
        if len(plain) < 5:
            named_title = re.search(
                r"(?i)\bin the ([^?]{5,200}?)\s+preprint\b", question
            )
            if named_title is not None:
                plain = " ".join(named_title.group(1).split())
                route_normalizations.append(
                    f"{secondary['leaf_id']}:academic_index_query_from_question_title"
                )
        if len(plain) >= 5:
            secondary["source_family"] = "scholarly_index"
            secondary["query"] = plain
            route_normalizations.append(
                f"{secondary['leaf_id']}:academic_distinct_index_route"
            )
    now = observed_at or datetime.now(UTC)
    if now.tzinfo is None:
        fail(
            "planning_timestamp_invalid", "observed_at", "Нужно время с часовым поясом."
        )
    protocol: dict[str, Any] | None = None
    academic_ref = None
    if mode == "academic":
        rules = require_mapping(proposal["protocol"], "proposal.protocol")
        require_exact_keys(
            rules,
            {"search_rule", "screening_rule", "synthesis_rule", "reporting_rule"},
            "proposal.protocol",
        )
        clean_rules = {
            key: validate_public_protocol_rule(rules[key]) for key in sorted(rules)
        }
        protocol = with_receipt_hash(
            {
                "schema_version": 1,
                "contract": "BetaAutonomousAcademicProtocol",
                "run_id": run_id,
                "sealed_at": now.astimezone(UTC).isoformat(),
                "acceptance_basis": "automatic_policy_before_source_results",
                "rules": clean_rules,
            }
        )
        academic_ref = {
            "protocol_ref": protocol["receipt_hash"],
            "accepted_before_results": True,
            "search_strategy_ref": sha256_json(clean_rules["search_rule"]),
            "screening_rule_ref": sha256_json(clean_rules["screening_rule"]),
        }
    discarded_nonacademic_protocol = (
        mode != "academic" and proposal["protocol"] is not None
    )
    search_calls, max_sources, model_calls, wall_seconds, max_cost = _LIMITS[mode]
    request = {
        "schema_version": 2,
        "run_id": run_id,
        "mode": mode,
        "question": question,
        "leaves": leaves,
        "rival_hypotheses": rivals,
        "academic_protocol": academic_ref,
        "limits": {
            "search_calls": search_calls,
            "max_sources": max_sources,
            "model_calls": model_calls,
            "wall_seconds": wall_seconds,
            "max_estimated_cost_usd": max_cost,
        },
        "oversight": {
            "internal_human_gate": False,
            "external_delivery_allowed": False,
        },
    }
    plan = build_beta_mode_plan(request)
    if plan["status"] != "ready_to_execute":
        fail("planning_route_blocked", "proposal.leaves", "Нет исполнимого маршрута.")
    record = with_receipt_hash(
        {
            "schema_version": 1,
            "contract": "BetaAutonomousPlanProposal",
            "run_id": run_id,
            "mode": mode,
            "question_sha256": hashlib.sha256(question.encode()).hexdigest(),
            "model_response_sha256": hashlib.sha256(raw.encode()).hexdigest(),
            "plan_receipt_hash": plan["receipt_hash"],
            "academic_protocol_receipt_hash": protocol["receipt_hash"]
            if protocol
            else None,
            "normalized_synonym_wrappers": normalized_groups,
            "normalized_duplicate_concept_terms": normalized_duplicate_terms,
            "normalized_rival_objects": normalized_rival_objects,
            "route_query_normalizations": route_normalizations,
            "discarded_nonacademic_protocol": discarded_nonacademic_protocol,
            "source_calls_before_seal": 0,
            "internal_human_gate_required": False,
            "release_authorized": False,
        }
    )
    return plan, protocol, record
