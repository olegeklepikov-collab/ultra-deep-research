# Research workflows and artifacts

[Home](../../README.md) · [Русский](../ru/workflows.md) · [Tool catalog](../reference/tools.md)

Current development adds [model-class selection](model-classes.md); the release examples below remain scoped to r152.

## Contract tools versus execution scripts

Call registered `research_*` tools when you need a typed decision over supplied data: validate a plan, assess a budget, check a claim/fragment relationship, evaluate a review record, or build a structured report. The individual schema determines the required fields and output contract. A decision over supplied measurements does not prove those measurements were independently obtained.

Use the skill scripts when the task requires an actual bounded sequence of model calls, source acquisition and retained artifacts. The scripts are in `skills/research/scripts/` under the installed Research plugin. Scripts ending in `reconcile_*` work with a prior attempt and its retained records; they are not permission to repeat an unknown external effect.

## Entry points

| Entry point | Purpose |
|---|---|
| `plan_beta_from_question.py` | One bounded, tool-free model call to construct a Search/Deep/Ultra/Academic plan |
| `run_beta_search.py` | Short web-only workflow with source selection, candidate/semantic checks and a partial or evidence-limited result |
| `run_beta_deep_question.py` | Deeper question-driven workflow over multiple source families |
| `run_beta_research.py --mode ultra --domain-first` | Domain decomposition, competing explanations, coverage, synthesis/challenge and control searches within limits |
| `run_beta_research.py --mode academic` | Sealed academic protocol, discovery/screening, optional document/dataset examination and an academic dossier |
| `appraise_beta_papers.py` | Examine supplied PDF or abstract records in sequential parts; preserve source-linked statements and reading gaps |
| `reanalyze_academic_dataset.py` | Reanalyse mapped spreadsheet data with source-cell provenance and explicit missingness |
| `acquire_orthogonal_metadata.py` | Additional metadata routes including Europe PMC/PMC, ORCID/ROR and Common Crawl index references |
| `import_portable_bundle.py` | Controlled import of a portable bundle through its explicit validation route |

Provider metadata, abstract access, full-text access and independent scientific support are separate capabilities. A Common Crawl index locator is not a downloaded archival page. A substituted provider is not automatically equivalent to an unavailable database.

## Minimal public Search

Run the scripts with the same Python environment that supplies the `hermes` executable. The output root must already exist, be absolute and not be a symlink; each run creates new private subdirectories.

```sh
UDR_PYTHON=/absolute/path/to/hermes/venv/bin/python
UDR_HERMES=/absolute/path/to/hermes/venv/bin/hermes
UDR_SCRIPTS="$HERMES_HOME/plugins/ultra-deep-research/skills/research/scripts"
mkdir -p "$HERMES_HOME/research-runs"
"$UDR_PYTHON" "$UDR_SCRIPTS/run_beta_search.py"   --question 'State exactly what FAIR principle F1 requires.'   --hermes "$UDR_HERMES"   --output-root "$HERMES_HOME/research-runs" --public-query-ack
```

`--public-query-ack` acknowledges that the query and relevant input material may be sent through the configured external research/model routes. It does not turn private material into public material or grant rights to redistribute a source.

For Ultra or Academic, use the same environment and output-root rules:

```sh
"$UDR_PYTHON" "$UDR_SCRIPTS/run_beta_research.py"   --mode ultra --domain-first --question 'Your bounded public question'   --hermes "$UDR_HERMES" --output-root "$HERMES_HOME/research-runs" --public-query-ack

"$UDR_PYTHON" "$UDR_SCRIPTS/run_beta_research.py"   --mode academic --question 'Your bounded public review question'   --academic-documents /absolute/path/documents.json   --hermes "$UDR_HERMES" --output-root "$HERMES_HOME/research-runs" --public-query-ack
```

Inspect each script's `--help` before adding controls such as `--planning-dir`, `--decomposition`, `--coverage-frame`, `--adaptive-coverage-batches`, `--academic-datasets`, or control-query budgets. Supplying `--academic-documents` supports appraisal; it does not itself freeze every source-discovery step.

## Initial plan limits in this release

| Mode | Search calls | Maximum sources | Model calls | Wall seconds | Estimated USD cap |
|---|---:|---:|---:|---:|---:|
| Search | 2 | 3 | 2 | 120 | 0.02 |
| Deep | 8 | 16 | 4 | 600 | 0.20 |
| Ultra | 16 | 32 | 8 | 1200 | 0.50 |
| Academic | 12 | 40 | 64 | 3600 | 0.30 |

These are the initial plan constants, not promised completion times or current model-price quotations. Bootstrap planning has a separate one-call, 60-second, 0.01 USD estimated budget. Additional stages are subject to their declared stage and remaining global limits. The actual receipts are authoritative for what ran. OAuth `included` accounting must remain visible alongside token counts and measured time.

## What to inspect

| Artifact | Meaning |
|---|---|
| `plan.json`, `planning-run.json` | Planned scope and the observation that produced the plan |
| `attempt.json` | Intent, bounds and retry policy before a potentially external operation |
| `effective-runtime.json`, `effective-model-entry.json` | Hash-bound effective runtime and model configuration |
| `capture.json`, source text/PDF files | Actual acquisition outcomes and retained source bytes |
| `source-selection.json` | Chosen source and eligible, missing or unreviewed leaves; the original ledger is retained |
| `model-usage.json`, `cost-accounting.json` | Measured usage and the interpretation of the cost estimate |
| `model-candidate.json`, verification/review records | Candidate statements and the scope of their checks |
| `result.json`, `result.md` where produced | Structured result and readable presentation |
| `failure.json` and reconciliation records | Failure or uncertain outcome; whether a fresh external attempt is permissible |

For papers, provide a document manifest with `document_id`, `title`, `url`, `path` and `read_scope` (`full_text` or the supported abstract form). Use the [tagged skill](https://github.com/olegeklepikov-collab/ultra-deep-research/tree/v0.41.0a1-r152-v21/skills/research) for the full per-script contract. PDF reading can be partial because of time, size, extraction or image limits; absence of an extracted visual element is not proof that the original page contains no meaningful figure, table or equation.

## When to stop or reconcile

A budget boundary preserves a partial result. A missing mandatory primary read prevents a stronger reading claim. A source-selection receipt does not make unreviewed leaves covered. Configuration changes require a new run. For an uncertain external result, inspect the retained attempt and the appropriate reconciliation entrypoint before any retry; never rerun solely because the local process returned an error.
