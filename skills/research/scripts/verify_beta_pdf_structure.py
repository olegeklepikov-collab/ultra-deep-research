"""Retain page-level PDF text and table grids for formal follow-up appraisal."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

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
except ImportError:
    from file_io import (
        load_json,
        new_private_directory,
        read_private_bytes,
        write_exclusive_bytes,
        write_exclusive_json,
    )

from hermes_research_report.beta_modes import verify_beta_mode_plan
from hermes_research_report.canonical import verify_receipt_hash, with_receipt_hash
from hermes_research_report.errors import ContractError

_CODE = re.compile(r"^[a-z][a-z0-9_]{2,79}$")


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--fulltext", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args(argv)
    output: Path | None = None
    try:
        plan_value, _ = load_json(args.plan)
        plan = verify_beta_mode_plan(plan_value)
        fulltext_value, _ = load_json(args.fulltext)
        if (
            plan["mode"] != "academic"
            or type(fulltext_value) is not dict
            or not verify_receipt_hash(fulltext_value)
            or fulltext_value.get("contract") != "BetaArxivFullTextRead"
            or fulltext_value.get("plan_receipt_hash") != plan["receipt_hash"]
            or fulltext_value.get("release_authorized") is not False
        ):
            raise ValueError("pdf_structure_source_invalid")
        fulltext = fulltext_value
        if (
            args.plan != args.output_root / f"{plan['run_id']}-planning/plan.json"
            or args.fulltext.is_symlink()
            or args.fulltext.parent.is_symlink()
            or args.output_root.is_symlink()
        ):
            raise ValueError("pdf_structure_paths_invalid")
        pdf = read_private_bytes(args.fulltext.parent / "paper.pdf", maximum=50_000_000)
        if _sha(pdf) != fulltext["pdf_sha256"] or len(pdf) != fulltext["pdf_bytes"]:
            raise ValueError("pdf_structure_bytes_invalid")
        try:
            import pdfplumber
        except ImportError:
            raise ValueError("pdf_structure_dependency_missing") from None
        output = args.output_root / f"{plan['run_id']}-academic-pdf-structure"
        new_private_directory(output)
        write_exclusive_json(
            output / "attempt.json",
            {
                "schema_version": 1,
                "status": "started_unknown_until_reconciled",
                "run_id": plan["run_id"],
                "plan_receipt_hash": plan["receipt_hash"],
                "fulltext_receipt_hash": fulltext["receipt_hash"],
                "retry_allowed": False,
            },
        )
        pages = []
        table_total = 0
        image_total = 0
        with pdfplumber.open(args.fulltext.parent / "paper.pdf") as document:
            if len(document.pages) != fulltext["page_count"]:
                raise ValueError("pdf_structure_page_count_mismatch")
            for page_index, page in enumerate(document.pages, 1):
                text_status = "parsed"
                try:
                    page_text = page.extract_text() or ""
                except (OSError, ValueError, TypeError):
                    page_text = ""
                    text_status = "failed"
                text_raw = page_text.encode("utf-8")
                text_name = f"page-{page_index:04d}.txt"
                write_exclusive_bytes(output / text_name, text_raw)
                table_status = "parsed"
                tables = []
                try:
                    for table_index, table in enumerate(page.find_tables(), 1):
                        grid = table.extract()
                        tables.append(
                            {
                                "table_index": table_index,
                                "bbox": [
                                    round(float(value), 3) for value in table.bbox
                                ],
                                "row_count": len(grid),
                                "column_count": max(
                                    (len(row) for row in grid), default=0
                                ),
                                "grid": grid,
                            }
                        )
                except (OSError, ValueError, TypeError):
                    table_status = "failed"
                    tables = []
                table_name = f"page-{page_index:04d}.tables.json"
                table_raw = (
                    json.dumps(tables, ensure_ascii=False, sort_keys=True) + "\n"
                ).encode("utf-8")
                write_exclusive_bytes(output / table_name, table_raw)
                images = [
                    {
                        "x0": round(float(item.get("x0") or 0), 3),
                        "top": round(float(item.get("top") or 0), 3),
                        "x1": round(float(item.get("x1") or 0), 3),
                        "bottom": round(float(item.get("bottom") or 0), 3),
                    }
                    for item in page.images
                ]
                image_name = f"page-{page_index:04d}.images.json"
                image_raw = (
                    json.dumps(images, ensure_ascii=False, sort_keys=True) + "\n"
                ).encode("utf-8")
                write_exclusive_bytes(output / image_name, image_raw)
                table_total += len(tables)
                image_total += len(images)
                pages.append(
                    {
                        "page": page_index,
                        "width": round(float(page.width), 3),
                        "height": round(float(page.height), 3),
                        "text_status": text_status,
                        "text_chars": len(page_text),
                        "text_file": text_name,
                        "text_sha256": _sha(text_raw),
                        "table_status": table_status,
                        "table_count": len(tables),
                        "table_file": table_name,
                        "table_sha256": _sha(table_raw),
                        "image_count": len(images),
                        "image_file": image_name,
                        "image_sha256": _sha(image_raw),
                    }
                )
        result = with_receipt_hash(
            {
                "schema_version": 1,
                "contract": "BetaAcademicPdfStructure",
                "status": "page_structure_candidate",
                "run_id": plan["run_id"],
                "mode": "academic",
                "plan_receipt_hash": plan["receipt_hash"],
                "fulltext_receipt_hash": fulltext["receipt_hash"],
                "pdf_sha256": fulltext["pdf_sha256"],
                "page_count": len(pages),
                "pages_with_text": sum(row["text_chars"] >= 20 for row in pages),
                "pages_empty_or_unreadable": [
                    row["page"] for row in pages if row["text_chars"] < 20
                ],
                "table_grid_count": table_total,
                "image_object_count": image_total,
                "pages": pages,
                "page_text_extraction_complete": all(
                    row["text_status"] == "parsed" for row in pages
                ),
                "table_extraction_complete": all(
                    row["table_status"] == "parsed" for row in pages
                ),
                "table_values_verified": False,
                "figure_semantics_verified": False,
                "formula_semantics_verified": False,
                "numeric_computation_replayed": False,
                "mode_qualified": False,
                "release_authorized": False,
            }
        )
        write_exclusive_json(output / "structure.json", result)
        print(
            json.dumps(
                {
                    "status": result["status"],
                    "run_id": plan["run_id"],
                    "page_count": result["page_count"],
                    "table_grid_count": table_total,
                    "image_object_count": image_total,
                    "release_authorized": False,
                },
                sort_keys=True,
            )
        )
        return 0
    except (ContractError, OSError, ValueError, TypeError) as error:
        code = error.code if isinstance(error, ContractError) else str(error)
        if not _CODE.fullmatch(code):
            code = "pdf_structure_failed"
        if output is not None and output.is_dir():
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
        print(json.dumps({"status": "error", "code": code}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
