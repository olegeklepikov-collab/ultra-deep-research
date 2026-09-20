"""One-command, fail-closed local Ultra/Academic source dossier.

This is a usable source-discovery path, not a qualified synthesis engine.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PLUGIN_ROOT / "src"))

try:
    from .file_io import (
        load_json,
        new_private_directory,
        read_private_bytes,
        write_exclusive_bytes,
        write_exclusive_json,
    )
    from .run_beta_search import SearchRunError, _child, _receipt
except ImportError:
    from file_io import (
        load_json,
        new_private_directory,
        read_private_bytes,
        write_exclusive_bytes,
        write_exclusive_json,
    )
    from run_beta_search import SearchRunError, _child, _receipt

from hermes_research_report.beta_modes import verify_beta_mode_plan
from hermes_research_report.canonical import verify_receipt_hash, with_receipt_hash
from hermes_research_report.errors import ContractError

SCRIPTS = Path(__file__).resolve().parent
_CODE = re.compile(r"^[a-z][a-z0-9_]{2,79}$")


def _verify_structure_files(directory: Path, structure: dict[str, Any]) -> None:
    pages = structure.get("pages")
    if type(pages) is not list or len(pages) != structure.get("page_count"):
        raise ValueError("profile_structure_files_invalid")
    for page in pages:
        if type(page) is not dict:
            raise ValueError("profile_structure_files_invalid")
        for name_key, hash_key in (
            ("text_file", "text_sha256"),
            ("table_file", "table_sha256"),
            ("image_file", "image_sha256"),
        ):
            name = page.get(name_key)
            if type(name) is not str or "/" in name or "\\" in name:
                raise ValueError("profile_structure_files_invalid")
            payload = read_private_bytes(directory / name, maximum=5_000_000)
            if hashlib.sha256(payload).hexdigest() != page.get(hash_key):
                raise ValueError("profile_structure_files_invalid")


def assemble_source_dossier(
    *,
    plan: dict[str, Any],
    planning: dict[str, Any],
    execution: dict[str, Any] | None,
    portfolio: dict[str, Any] | None,
    protocol: dict[str, Any] | None,
    screening: dict[str, Any] | None = None,
    screening_attempted: bool = False,
    challenge: dict[str, Any] | None = None,
    challenge_attempted: bool = False,
    sensitivity: dict[str, Any] | None = None,
    sensitivity_attempted: bool = False,
    fulltext: dict[str, Any] | None = None,
    fulltext_attempted: bool = False,
    structure: dict[str, Any] | None = None,
    structure_attempted: bool = False,
    analysis: dict[str, Any] | None = None,
    analysis_attempted: bool = False,
    study_graph: dict[str, Any] | None = None,
    study_graph_attempted: bool = False,
) -> tuple[dict[str, Any], bytes]:
    verified = verify_beta_mode_plan(plan)
    mode = verified["mode"]
    if mode not in {"ultra", "academic"}:
        raise ValueError("profile_mode_invalid")
    if (
        not verify_receipt_hash(planning)
        or planning.get("contract") != "BetaAutonomousPlanningRun"
        or planning.get("plan_receipt_hash") != verified["receipt_hash"]
        or planning.get("run_id") != verified["run_id"]
        or planning.get("mode") != mode
        or planning.get("release_authorized") is not False
    ):
        raise ValueError("profile_planning_not_bound")
    if mode == "academic":
        if (
            type(protocol) is not dict
            or not verify_receipt_hash(protocol)
            or protocol.get("contract") != "BetaAutonomousAcademicProtocol"
            or protocol.get("run_id") != verified["run_id"]
            or protocol.get("receipt_hash")
            != verified["academic_protocol"]["protocol_ref"]
            or planning.get("academic_protocol_receipt_hash")
            != protocol["receipt_hash"]
        ):
            raise ValueError("profile_protocol_not_bound")
    elif protocol is not None:
        raise ValueError("profile_protocol_not_applicable")
    if execution is not None and (
        not verify_receipt_hash(execution)
        or execution.get("contract") != "BetaAutomaticSourceExecution"
        or execution.get("run_id") != verified["run_id"]
        or execution.get("plan_receipt_hash") != verified["receipt_hash"]
        or execution.get("mode") != mode
        or execution.get("release_authorized") is not False
    ):
        raise ValueError("profile_execution_not_bound")
    if portfolio is not None and (
        execution is None
        or not verify_receipt_hash(portfolio)
        or portfolio.get("contract") != "BetaSourcePortfolio"
        or portfolio.get("run_id") != verified["run_id"]
        or portfolio.get("plan_receipt_hash") != verified["receipt_hash"]
        or portfolio.get("mode") != mode
        or portfolio.get("release_authorized") is not False
        or execution.get("portfolio_receipt_hash") != portfolio["receipt_hash"]
    ):
        raise ValueError("profile_portfolio_not_bound")
    if screening is not None and (
        mode != "academic"
        or protocol is None
        or execution is None
        or portfolio is None
        or not verify_receipt_hash(screening)
        or screening.get("contract") != "BetaAcademicPreliminaryScreen"
        or screening.get("run_id") != verified["run_id"]
        or screening.get("plan_receipt_hash") != verified["receipt_hash"]
        or screening.get("protocol_receipt_hash") != protocol["receipt_hash"]
        or screening.get("execution_receipt_hash") != execution["receipt_hash"]
        or screening.get("portfolio_receipt_hash") != portfolio["receipt_hash"]
        or screening.get("included_study_count") != 0
        or screening.get("release_authorized") is not False
    ):
        raise ValueError("profile_screening_not_bound")
    if screening is not None and (
        type(screening.get("decisions")) is not list
        or len(screening["decisions"]) != screening.get("identified_record_count")
        or any(
            type(row) is not dict
            or type(row.get("record_id")) is not str
            or row.get("verdict") not in {"include_candidate", "exclude", "uncertain"}
            or type(row.get("reason")) is not str
            or any(ord(char) < 32 for char in row["reason"])
            for row in screening["decisions"]
        )
    ):
        raise ValueError("profile_screening_invalid")
    if challenge is not None and (
        mode != "ultra"
        or execution is None
        or portfolio is None
        or not verify_receipt_hash(challenge)
        or challenge.get("contract") != "BetaUltraRivalChallenge"
        or challenge.get("run_id") != verified["run_id"]
        or challenge.get("plan_receipt_hash") != verified["receipt_hash"]
        or challenge.get("execution_receipt_hash") != execution["receipt_hash"]
        or challenge.get("portfolio_receipt_hash") != portfolio["receipt_hash"]
        or challenge.get("accepted_claim_count") != 0
        or challenge.get("release_authorized") is not False
    ):
        raise ValueError("profile_challenge_not_bound")
    if sensitivity is not None and (
        mode != "ultra"
        or challenge is None
        or not verify_receipt_hash(sensitivity)
        or sensitivity.get("contract") != "BetaUltraSensitivity"
        or sensitivity.get("run_id") != verified["run_id"]
        or sensitivity.get("plan_receipt_hash") != verified["receipt_hash"]
        or sensitivity.get("challenge_receipt_hash") != challenge["receipt_hash"]
        or sensitivity.get("robustness_verified") is not False
        or sensitivity.get("release_authorized") is not False
    ):
        raise ValueError("profile_sensitivity_not_bound")
    if fulltext is not None and (
        mode != "academic"
        or screening is None
        or not verify_receipt_hash(fulltext)
        or fulltext.get("contract") != "BetaArxivFullTextRead"
        or fulltext.get("run_id") != verified["run_id"]
        or fulltext.get("plan_receipt_hash") != verified["receipt_hash"]
        or fulltext.get("screening_receipt_hash") != screening["receipt_hash"]
        or fulltext.get("status") != "parsed_text_candidate"
        or fulltext.get("release_authorized") is not False
        or not any(
            row.get("record_id") == fulltext.get("record_id")
            and row.get("verdict") == "include_candidate"
            for row in screening.get("decisions", [])
            if type(row) is dict
        )
    ):
        raise ValueError("profile_fulltext_not_bound")
    if analysis is not None and (
        mode != "academic"
        or fulltext is None
        or not verify_receipt_hash(analysis)
        or analysis.get("contract") != "BetaAcademicFullTextAnalysis"
        or analysis.get("run_id") != verified["run_id"]
        or analysis.get("plan_receipt_hash") != verified["receipt_hash"]
        or analysis.get("fulltext_receipt_hash") != fulltext["receipt_hash"]
        or type(analysis.get("cards")) is not list
        or analysis.get("reported_statement_count") != len(analysis["cards"])
        or analysis.get("accepted_claim_count") != 0
        or analysis.get("release_authorized") is not False
    ):
        raise ValueError("profile_analysis_not_bound")
    if structure is not None and (
        mode != "academic"
        or fulltext is None
        or not verify_receipt_hash(structure)
        or structure.get("contract") != "BetaAcademicPdfStructure"
        or structure.get("run_id") != verified["run_id"]
        or structure.get("plan_receipt_hash") != verified["receipt_hash"]
        or structure.get("fulltext_receipt_hash") != fulltext["receipt_hash"]
        or structure.get("page_count") != fulltext["page_count"]
        or structure.get("table_values_verified") is not False
        or structure.get("release_authorized") is not False
    ):
        raise ValueError("profile_structure_not_bound")
    if study_graph is not None and (
        mode != "academic"
        or screening is None
        or not verify_receipt_hash(study_graph)
        or study_graph.get("contract") != "BetaAcademicStudyGraph"
        or study_graph.get("run_id") != verified["run_id"]
        or study_graph.get("plan_receipt_hash") != verified["receipt_hash"]
        or study_graph.get("screening_receipt_hash") != screening["receipt_hash"]
        or study_graph.get("fulltext_receipt_hash")
        != (fulltext["receipt_hash"] if fulltext else None)
        or study_graph.get("quantitative_pooling_allowed") is not False
        or study_graph.get("release_authorized") is not False
    ):
        raise ValueError("profile_study_graph_not_bound")
    source_rows = portfolio["leaves"] if portfolio is not None else []
    if type(source_rows) is not list or any(
        type(row) is not dict for row in source_rows
    ):
        raise ValueError("profile_source_rows_invalid")
    observed = {row["leaf_id"]: row for row in source_rows}
    if len(observed) != len(source_rows) or not set(observed).issubset(
        {leaf["leaf_id"] for leaf in verified["leaves"]}
    ):
        raise ValueError("profile_source_rows_duplicate")
    lines = [
        "# Предварительное досье источников",
        "",
        f"Режим: {mode}. Принятых исследовательских выводов: 0. Квалификация режима: нет.",
        f"Вопрос: {verified['question']}",
        "",
        "## Исполненные поисковые листья",
        "",
    ]
    for leaf in verified["leaves"]:
        row = observed.get(leaf["leaf_id"])
        if row is None:
            lines.append(
                f"- {leaf['leaf_id']} ({leaf['source_family']}): нет проверенной квитанции."
            )
        else:
            lines.append(
                f"- {leaf['leaf_id']} ({leaf['source_family']}): {row['status']}; "
                f"кандидатов {row['candidate_count']}; область чтения {row['read_scope']}"
                + (
                    f"; причина {row['reason']}"
                    if row["status"] != "candidate" and row.get("reason")
                    else ""
                )
                + "."
            )
    lines.extend(["", "## Невыполненные проверки", ""])
    if mode == "ultra":
        lines.append("Конкурирующие гипотезы и предварительная проверка по аннотациям:")
        judgments = (
            {row["rival_index"]: row for row in challenge["judgments"]}
            if challenge is not None
            else {}
        )
        for index, rival in enumerate(verified["rival_hypotheses"]):
            row = judgments.get(index)
            if row is None:
                lines.append(f"- {rival}: не проверена.")
            else:
                verdict = {
                    "supported": "предварительно поддержана",
                    "contradicted": "предварительно оспорена",
                    "unclear": "неясно",
                }[row["verdict"]]
                lines.append(
                    f"- {rival}: {verdict} ({row['reason']}); "
                    f"опора: {row['source_ref'] or 'нет'}; "
                    f"точный фрагмент: «{row['quote']}»."
                )
        if sensitivity is not None:
            lines.append(
                f"Проверка удаления цитируемого источника: {sensitivity['single_citation_dependent_count']} "
                "предварительных вердиктов требуют повторного анализа; устойчивость не установлена."
            )
        elif sensitivity_attempted:
            lines.append(
                "Проверка устойчивости не завершена; исходные гипотезы и цитаты сохранены."
            )
        lines.append(
            "Вердикты по аннотациям предварительны; не выполнены независимое сопоставление полных работ и анализ устойчивости."
        )
    else:
        lines.append(
            f"Протокол запечатан до получения источников: {protocol['receipt_hash']}."
        )
        if screening is None:
            lines.append("Предварительный отбор названий и аннотаций не завершён.")
        else:
            lines.append(
                "Предварительный отбор названий и аннотаций: "
                f"{screening['identified_record_count']} записей; "
                f"{screening['include_candidate_count']} кандидатов к полному тексту, "
                f"{screening['exclude_count']} исключены, "
                f"{screening['uncertain_count']} неясны."
            )
            titles = {row["record_id"]: row["title"] for row in screening["records"]}
            screen_labels = {
                "include_candidate": "кандидат к полному тексту",
                "exclude": "исключена по аннотации",
                "uncertain": "неясно",
            }
            lines.extend(
                f"- {titles.get(row['record_id'], 'Название недоступно')} "
                f"({row['record_id']}): {screen_labels[row['verdict']]}; "
                f"{row['reason']}"
                for row in screening["decisions"]
            )
        if fulltext is not None:
            lines.append(
                f"Полный PDF кандидата {fulltext['record_id']} сохранён и текст извлечён: "
                f"{fulltext['page_count']} страниц, {fulltext['text_chars']} знаков. "
                "Полнота формул, таблиц, рисунков и отсканированных страниц ещё не удостоверена."
            )
        elif fulltext_attempted:
            lines.append(
                "Попытка получить полный PDF не завершилась проверенным текстом; предварительный отбор по аннотации сохранён."
            )
        if structure is not None:
            lines.append(
                f"Постраничная структура: текст обнаружен на {structure['pages_with_text']}/{structure['page_count']} страницах; "
                f"выделено {structure['table_grid_count']} табличных сеток. "
                "Ячейки сохранены с координатами, но значения и расчёты не перепроверены."
            )
        elif structure_attempted:
            lines.append(
                "Постраничный разбор таблиц и изображений не завершён; текстовый анализ остаётся доступным с этой оговоркой."
            )
        if analysis is not None:
            if "chunks_total" in analysis:
                lines.append(
                    "Охват текстового слоя: "
                    f"{analysis['text_chars_processed']}/{analysis['text_chars_total']} знаков, "
                    f"{analysis['chunks_analyzed']}/{analysis['chunks_total']} частей. "
                    "Необработанный остаток не считается прочитанным."
                )
            kind_labels = {
                "method": "метод",
                "empirical_observation": "эмпирическое наблюдение",
                "statistical_result": "сообщённый статистический результат",
                "hypothesis": "гипотеза",
                "opinion": "мнение авторов",
                "theory": "теоретическое положение",
                "limitation": "ограничение",
            }
            lines.append(
                "Положения из извлечённого текста PDF; это сообщения авторов, не независимые выводы системы:"
            )
            for card in analysis["cards"]:
                grade = (
                    "точный фрагмент найден, но расположение и визуальные элементы не проверены"
                    if card["quote"] is not None
                    else "цитата модели не совпала с текстом; интерпретация не привязана точно"
                )
                if (
                    card["quote"] is not None
                    and card["claim_type"] == "statistical_result"
                ):
                    grade = "точный фрагмент найден; числа, таблицы и метод расчёта не перепроверены"
                lines.append(
                    f"- {kind_labels[card['claim_type']]}: {card['statement']} "
                    f"Опора: {grade}. "
                    f"Цитата: «{card['quote'] or 'нет проверенной цитаты'}». "
                    f"Ограничение: {card['uncertainty']}"
                )
        elif analysis_attempted:
            lines.append(
                "Содержательный разбор извлечённого текста не завершён; сам текст и его ограничения сохранены."
            )
        if study_graph is not None:
            lines.append(
                f"Карта публикаций: {study_graph['identified_record_count']} записей, "
                f"{len(study_graph['identity_groups'])} консервативных групп идентичности, "
                f"{study_graph['fulltext_read_count']} прочитанный PDF, "
                "формально включённых исследований: 0. Численное объединение результатов запрещено."
            )
        elif study_graph_attempted:
            lines.append(
                "Связи версий и исследований не завершены; объединение результатов не допускается."
            )
        remaining = ["оценка риска ошибки", "межисследовательский научный синтез"]
        if fulltext is None:
            remaining.insert(0, "отбор и разбор полного текста")
        if study_graph is None:
            remaining.insert(0, "карта исследований")
        lines.append("Не выполнены: " + ", ".join(remaining) + ".")
    lines.append(
        "Метаданные и аннотации не являются полным текстом или доказательством независимости исследований."
    )
    status = (
        "partial_source_dossier"
        if execution is not None
        and execution.get("status") == "partial_analysis_required"
        and portfolio is not None
        and source_rows
        else "source_execution_blocked"
    )
    cost = planning.get("reported_model_cost_usd")
    source_cost = (
        execution.get("reported_total_cost_usd") if execution is not None else None
    )
    screening_cost = (
        screening.get("reported_incremental_cost_usd") if screening is not None else 0
    )
    challenge_cost = (
        challenge.get("reported_incremental_cost_usd") if challenge is not None else 0
    )
    analysis_cost = (
        analysis.get("reported_incremental_cost_usd") if analysis is not None else 0
    )
    if (
        type(cost) not in (int, float)
        or cost < 0
        or type(screening_cost) not in (int, float)
        or screening_cost < 0
        or type(challenge_cost) not in (int, float)
        or challenge_cost < 0
        or type(analysis_cost) not in (int, float)
        or analysis_cost < 0
        or (
            source_cost is not None
            and (type(source_cost) not in (int, float) or source_cost < 0)
        )
    ):
        raise ValueError("profile_cost_invalid")
    cost_complete = (
        source_cost is not None
        and (not screening_attempted or screening is not None)
        and (not challenge_attempted or challenge is not None)
        and (not analysis_attempted or analysis is not None)
    )
    total_cost = (
        round(
            float(cost)
            + float(source_cost)
            + float(screening_cost)
            + float(challenge_cost)
            + float(analysis_cost),
            8,
        )
        if cost_complete
        else None
    )
    workflow_gaps = []
    if (
        execution is None
        or portfolio is None
        or execution.get("status") != "partial_analysis_required"
    ):
        workflow_gaps.append("source_execution")
    elif len(source_rows) != len(verified["leaves"]):
        workflow_gaps.append("source_leaf_coverage")
    if mode == "ultra":
        if challenge is None:
            workflow_gaps.append("rival_challenge")
        if sensitivity is None:
            workflow_gaps.append("source_sensitivity")
    else:
        if screening is None:
            workflow_gaps.append("preliminary_screening")
        elif screening["include_candidate_count"] > 0:
            if fulltext is None:
                workflow_gaps.append("candidate_fulltext")
            if structure is None:
                workflow_gaps.append("page_structure")
            if analysis is None:
                workflow_gaps.append("fulltext_analysis")
            elif (
                type(analysis.get("text_chars_total")) is not int
                or analysis.get("text_chars_processed")
                != analysis.get("text_chars_total")
                or analysis.get("text_chars_total") != fulltext["text_chars"]
            ):
                workflow_gaps.append("fulltext_coverage")
        if study_graph is None:
            workflow_gaps.append("study_graph")
    if not cost_complete:
        workflow_gaps.append("cost_observation")
    elif (
        total_cost is not None
        and total_cost > verified["limits"]["max_estimated_cost_usd"]
    ):
        workflow_gaps.append("cost_limit")
    lines.extend(
        [
            "",
            "## Исполнение маршрута и надёжность результата",
            "",
            "Запланированный маршрут выполнен; научная надёжность каждого положения указана отдельно."
            if not workflow_gaps
            else "Маршрут завершён частично; недостающие обязательные шаги: "
            + ", ".join(workflow_gaps)
            + ".",
            "Завершённость маршрута не означает подтверждения тезисов или допуска к публичному выпуску.",
        ]
    )
    markdown = ("\n".join(lines) + "\n").encode("utf-8")
    receipt = with_receipt_hash(
        {
            "schema_version": 1,
            "contract": "BetaAutonomousProfileDossier",
            "run_id": verified["run_id"],
            "mode": mode,
            "status": status,
            "plan_receipt_hash": verified["receipt_hash"],
            "planning_run_receipt_hash": planning["receipt_hash"],
            "execution_receipt_hash": execution["receipt_hash"] if execution else None,
            "portfolio_receipt_hash": portfolio["receipt_hash"] if portfolio else None,
            "academic_protocol_receipt_hash": protocol["receipt_hash"]
            if protocol
            else None,
            "screening_receipt_hash": screening["receipt_hash"] if screening else None,
            "challenge_receipt_hash": challenge["receipt_hash"] if challenge else None,
            "sensitivity_receipt_hash": sensitivity["receipt_hash"]
            if sensitivity
            else None,
            "sensitivity_attempted": sensitivity_attempted,
            "fulltext_receipt_hash": fulltext["receipt_hash"] if fulltext else None,
            "fulltext_attempted": fulltext_attempted,
            "structure_receipt_hash": structure["receipt_hash"] if structure else None,
            "structure_attempted": structure_attempted,
            "analysis_receipt_hash": analysis["receipt_hash"] if analysis else None,
            "analysis_attempted": analysis_attempted,
            "study_graph_receipt_hash": study_graph["receipt_hash"]
            if study_graph
            else None,
            "study_graph_attempted": study_graph_attempted,
            "observed_leaf_count": len(source_rows),
            "candidate_leaf_count": sum(
                row["status"] == "candidate" for row in source_rows
            ),
            "workflow_execution_complete": not workflow_gaps,
            "workflow_gaps": workflow_gaps,
            "accepted_claim_count": 0,
            "markdown_sha256": hashlib.sha256(markdown).hexdigest(),
            "reported_total_cost_usd": total_cost,
            "cost_observation_complete": cost_complete,
            "final_acceptance_external": True,
            "internal_human_gate_required": False,
            "mode_qualified": False,
            "release_authorized": False,
            "external_delivery_authorized": False,
        }
    )
    return receipt, markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("ultra", "academic"), required=True)
    parser.add_argument("--question", required=True)
    parser.add_argument("--hermes", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--planning-dir", type=Path)
    parser.add_argument("--public-query-ack", action="store_true")
    args = parser.parse_args(argv)
    if not args.public_query_ack:
        print(
            json.dumps({"status": "error", "code": "public_query_ack_required"}),
            file=sys.stderr,
        )
        return 2
    plan: dict[str, Any] | None = None
    planning: dict[str, Any] | None = None
    execution: dict[str, Any] | None = None
    portfolio: dict[str, Any] | None = None
    protocol: dict[str, Any] | None = None
    screening: dict[str, Any] | None = None
    screening_attempted = False
    challenge: dict[str, Any] | None = None
    challenge_attempted = False
    sensitivity: dict[str, Any] | None = None
    sensitivity_attempted = False
    fulltext: dict[str, Any] | None = None
    fulltext_attempted = False
    structure: dict[str, Any] | None = None
    structure_attempted = False
    analysis: dict[str, Any] | None = None
    analysis_attempted = False
    study_graph: dict[str, Any] | None = None
    study_graph_attempted = False
    output: Path | None = None
    try:
        if (
            not args.output_root.is_absolute()
            or args.output_root.is_symlink()
            or not args.output_root.is_dir()
        ):
            raise ValueError("output_root_invalid")
        if args.planning_dir is None:
            plan_code, created = _child(
                [
                    sys.executable,
                    str(SCRIPTS / "plan_beta_from_question.py"),
                    "--mode",
                    args.mode,
                    "--question",
                    args.question,
                    "--hermes",
                    str(args.hermes),
                    "--output-root",
                    str(args.output_root),
                    "--public-query-ack",
                ],
                timeout=75,
            )
            if (
                plan_code != 0
                or created.get("status") != "ready_to_execute"
                or type(created.get("run_id")) is not str
            ):
                raise ValueError("profile_planning_blocked")
            run_id = created["run_id"]
            plan_dir = args.output_root / f"{run_id}-planning"
            if created.get("output") != str(plan_dir):
                raise ValueError("profile_planning_path_invalid")
        else:
            plan_dir = args.planning_dir
            if (
                not plan_dir.is_absolute()
                or plan_dir.is_symlink()
                or not plan_dir.is_dir()
                or plan_dir.parent != args.output_root
                or not plan_dir.name.endswith("-planning")
            ):
                raise ValueError("profile_planning_path_invalid")
            run_id = plan_dir.name.removesuffix("-planning")
            if not re.fullmatch(r"^[A-Z][A-Z0-9-]{2,63}$", run_id):
                raise ValueError("profile_planning_path_invalid")
        plan = verify_beta_mode_plan(
            _receipt(plan_dir / "plan.json", "BetaModeExecutionPlan", run_id)
        )
        planning = _receipt(
            plan_dir / "planning-run.json", "BetaAutonomousPlanningRun", run_id
        )
        if (
            plan["mode"] != args.mode
            or plan["question"] != args.question.strip()
            or plan["status"] != "ready_to_execute"
        ):
            raise ValueError("profile_plan_not_executable")
        if args.mode == "academic":
            protocol_value, _ = load_json(plan_dir / "academic-protocol.json")
            if type(protocol_value) is not dict:
                raise ValueError("profile_protocol_invalid")
            protocol = protocol_value
        output = args.output_root / f"{run_id}-{args.mode}-overall"
        new_private_directory(output)
        write_exclusive_json(
            output / "attempt.json",
            {
                "schema_version": 1,
                "status": "started_unknown_until_reconciled",
                "run_id": run_id,
                "mode": args.mode,
                "plan_receipt_hash": plan["receipt_hash"],
                "retry_allowed": False,
            },
        )
        deadline = time.monotonic() + float(plan["limits"]["wall_seconds"])
        try:
            _child(
                [
                    sys.executable,
                    str(SCRIPTS / "execute_beta_sources.py"),
                    "--plan",
                    str(plan_dir / "plan.json"),
                    "--output-root",
                    str(args.output_root),
                    "--public-query-ack",
                ],
                timeout=deadline - time.monotonic(),
            )
        except SearchRunError:
            pass
        execution_file = args.output_root / f"{run_id}-execution/execution.json"
        portfolio_file = args.output_root / f"{run_id}-execution/portfolio.json"
        if execution_file.is_file():
            execution = _receipt(execution_file, "BetaAutomaticSourceExecution", run_id)
        if execution is not None and portfolio_file.is_file():
            portfolio = _receipt(portfolio_file, "BetaSourcePortfolio", run_id)
        if (
            args.mode == "academic"
            and execution is not None
            and execution.get("status") == "partial_analysis_required"
            and portfolio is not None
        ):
            screening_attempted = True
            try:
                screen_code, _ = _child(
                    [
                        sys.executable,
                        str(SCRIPTS / "screen_beta_academic.py"),
                        "--plan",
                        str(plan_dir / "plan.json"),
                        "--protocol",
                        str(plan_dir / "academic-protocol.json"),
                        "--execution",
                        str(execution_file),
                        "--portfolio",
                        str(portfolio_file),
                        "--hermes",
                        str(args.hermes),
                        "--output-root",
                        str(args.output_root),
                    ],
                    timeout=deadline - time.monotonic(),
                )
                if screen_code == 0:
                    screening = _receipt(
                        args.output_root / f"{run_id}-academic-screen/screening.json",
                        "BetaAcademicPreliminaryScreen",
                        run_id,
                    )
            except SearchRunError:
                pass
        if (
            args.mode == "ultra"
            and execution is not None
            and execution.get("status") == "partial_analysis_required"
            and portfolio is not None
        ):
            challenge_attempted = True
            try:
                challenge_code, _ = _child(
                    [
                        sys.executable,
                        str(SCRIPTS / "challenge_beta_ultra.py"),
                        "--plan",
                        str(plan_dir / "plan.json"),
                        "--execution",
                        str(execution_file),
                        "--portfolio",
                        str(portfolio_file),
                        "--hermes",
                        str(args.hermes),
                        "--output-root",
                        str(args.output_root),
                    ],
                    timeout=deadline - time.monotonic(),
                )
                if challenge_code == 0:
                    challenge = _receipt(
                        args.output_root / f"{run_id}-ultra-challenge/challenge.json",
                        "BetaUltraRivalChallenge",
                        run_id,
                    )
            except SearchRunError:
                pass
        if (
            args.mode == "ultra"
            and challenge is not None
            and execution is not None
            and portfolio is not None
        ):
            sensitivity_attempted = True
            try:
                sensitivity_code, _ = _child(
                    [
                        sys.executable,
                        str(SCRIPTS / "assess_beta_ultra_sensitivity.py"),
                        "--plan",
                        str(plan_dir / "plan.json"),
                        "--execution",
                        str(execution_file),
                        "--portfolio",
                        str(portfolio_file),
                        "--challenge",
                        str(
                            args.output_root
                            / f"{run_id}-ultra-challenge/challenge.json"
                        ),
                        "--output-root",
                        str(args.output_root),
                    ],
                    timeout=deadline - time.monotonic(),
                )
                if sensitivity_code == 0:
                    sensitivity = _receipt(
                        args.output_root / f"{run_id}.ultra-sensitivity.json",
                        "BetaUltraSensitivity",
                        run_id,
                    )
            except SearchRunError:
                pass
        if args.mode == "academic" and screening is not None:
            selected = [
                row
                for row in screening["decisions"]
                if row["verdict"] == "include_candidate"
            ]
            records = {row["record_id"]: row for row in screening["records"]}
            arxiv_selected = [
                row
                for row in selected
                if records[row["record_id"]]["provider"] == "arxiv"
            ]
            if arxiv_selected:
                fulltext_attempted = True
                chosen = arxiv_selected[0]["record_id"]
                leaf_id = records[chosen]["leaf_id"]
                try:
                    fulltext_code, _ = _child(
                        [
                            sys.executable,
                            str(SCRIPTS / "acquire_arxiv_fulltext.py"),
                            "--plan",
                            str(plan_dir / "plan.json"),
                            "--arxiv-capture",
                            str(
                                args.output_root
                                / f"{run_id}-{leaf_id}-arxiv/capture.json"
                            ),
                            "--screening",
                            str(
                                args.output_root
                                / f"{run_id}-academic-screen/screening.json"
                            ),
                            "--record-id",
                            chosen,
                            "--output-root",
                            str(args.output_root),
                        ],
                        timeout=deadline - time.monotonic(),
                    )
                    if fulltext_code == 0:
                        stem = chosen.rsplit("/", 1)[-1]
                        fulltext_file = (
                            args.output_root
                            / f"{run_id}-{leaf_id}-{stem}-fulltext/capture.json"
                        )
                        fulltext = _receipt(
                            fulltext_file,
                            "BetaArxivFullTextRead",
                            run_id,
                        )
                        pdf = read_private_bytes(
                            fulltext_file.parent / "paper.pdf", maximum=50_000_000
                        )
                        parsed = read_private_bytes(
                            fulltext_file.parent / "paper.md", maximum=25_000_000
                        )
                        if (
                            hashlib.sha256(pdf).hexdigest() != fulltext["pdf_sha256"]
                            or hashlib.sha256(parsed).hexdigest()
                            != fulltext["text_sha256"]
                            or len(pdf) != fulltext["pdf_bytes"]
                        ):
                            raise ValueError("profile_fulltext_bytes_not_bound")
                except SearchRunError:
                    pass
        if args.mode == "academic" and fulltext is not None:
            structure_attempted = True
            try:
                structure_code, _ = _child(
                    [
                        sys.executable,
                        str(SCRIPTS / "verify_beta_pdf_structure.py"),
                        "--plan",
                        str(plan_dir / "plan.json"),
                        "--fulltext",
                        str(fulltext_file),
                        "--output-root",
                        str(args.output_root),
                    ],
                    timeout=deadline - time.monotonic(),
                )
                if structure_code == 0:
                    structure_dir = (
                        args.output_root / f"{run_id}-academic-pdf-structure"
                    )
                    structure = _receipt(
                        structure_dir / "structure.json",
                        "BetaAcademicPdfStructure",
                        run_id,
                    )
                    _verify_structure_files(structure_dir, structure)
            except (SearchRunError, OSError, ValueError):
                structure = None
        if args.mode == "academic" and fulltext is not None:
            analysis_attempted = True
            try:
                analysis_code, _ = _child(
                    [
                        sys.executable,
                        str(SCRIPTS / "analyze_beta_fulltext.py"),
                        "--plan",
                        str(plan_dir / "plan.json"),
                        "--fulltext",
                        str(fulltext_file),
                        "--hermes",
                        str(args.hermes),
                        "--output-root",
                        str(args.output_root),
                    ],
                    timeout=deadline - time.monotonic(),
                )
                if analysis_code == 0:
                    analysis = _receipt(
                        args.output_root
                        / f"{run_id}-academic-fulltext-analysis/analysis.json",
                        "BetaAcademicFullTextAnalysis",
                        run_id,
                    )
            except SearchRunError:
                pass
        if args.mode == "academic" and screening is not None:
            study_graph_attempted = True
            graph_command = [
                sys.executable,
                str(SCRIPTS / "assess_beta_academic_study_graph.py"),
                "--plan",
                str(plan_dir / "plan.json"),
                "--execution",
                str(execution_file),
                "--portfolio",
                str(portfolio_file),
                "--screening",
                str(args.output_root / f"{run_id}-academic-screen/screening.json"),
                "--output-root",
                str(args.output_root),
            ]
            if fulltext is not None:
                graph_command.extend(("--fulltext", str(fulltext_file)))
            if structure is not None:
                graph_command.extend(
                    ("--structure", str(structure_dir / "structure.json"))
                )
            if analysis is not None:
                graph_command.extend(
                    (
                        "--analysis",
                        str(
                            args.output_root
                            / f"{run_id}-academic-fulltext-analysis/analysis.json"
                        ),
                    )
                )
            try:
                graph_code, _ = _child(
                    graph_command, timeout=deadline - time.monotonic()
                )
                if graph_code == 0:
                    study_graph = _receipt(
                        args.output_root / f"{run_id}.academic-study-graph.json",
                        "BetaAcademicStudyGraph",
                        run_id,
                    )
            except SearchRunError:
                pass
        result, markdown = assemble_source_dossier(
            plan=plan,
            planning=planning,
            execution=execution,
            portfolio=portfolio,
            protocol=protocol,
            screening=screening,
            screening_attempted=screening_attempted,
            challenge=challenge,
            challenge_attempted=challenge_attempted,
            sensitivity=sensitivity,
            sensitivity_attempted=sensitivity_attempted,
            fulltext=fulltext,
            fulltext_attempted=fulltext_attempted,
            structure=structure,
            structure_attempted=structure_attempted,
            analysis=analysis,
            analysis_attempted=analysis_attempted,
            study_graph=study_graph,
            study_graph_attempted=study_graph_attempted,
        )
        write_exclusive_bytes(output / "result.md", markdown)
        write_exclusive_json(output / "outcome.json", result)
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "mode": args.mode,
                    "run_id": run_id,
                    "result": str(output / "result.md"),
                    "workflow_execution_complete": result[
                        "workflow_execution_complete"
                    ],
                    "workflow_gaps": result["workflow_gaps"],
                    "accepted_claim_count": 0,
                    "release_authorized": False,
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, SearchRunError, OSError, ValueError) as error:
        code = error.code if isinstance(error, ContractError) else str(error)
        if not _CODE.fullmatch(code):
            code = "profile_run_failed"
        print(
            json.dumps(
                {
                    "status": "error",
                    "code": code,
                    "run_id": plan["run_id"] if plan else None,
                }
            ),
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
