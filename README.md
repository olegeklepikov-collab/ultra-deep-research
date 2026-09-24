# Ultra Deep Research

[Русский](README.ru.md) · [Release](https://github.com/olegeklepikov-collab/ultra-deep-research/releases/tag/v0.41.0a1-r152-v21) · [Installation](docs/en/installation.md) · [Tool reference](docs/reference/tools.md)

**Evidence-traceable research workflows for Hermes.** Ultra Deep Research turns a question into a bounded plan, retrieves and examines source material, records the basis of candidate claims, and produces a report with explicit gaps and qualification status.

The project combines deterministic contract checks with model-assisted research. It separates source acquisition, exact fragment verification, interpretation, independent review, acceptance, release, and delivery. A successful tool call or matching quotation is not treated as proof that a scientific conclusion is true.

**Current development:** [model classes](docs/en/model-classes.md) decouple a research request from a particular vendor/model. Operators update the mapping in Hermes configuration; the concrete executed route remains recorded. The signed release below is unchanged.

## Current publication

| Item | Published state |
|---|---|
| Release | [r152 / v21](https://github.com/olegeklepikov-collab/ultra-deep-research/releases/tag/v0.41.0a1-r152-v21), **prerelease** |
| Research component | `ultra-deep-research` `0.41.0a1`, revision r152; **147 registered tools** |
| Foundation component | `hermes-foundation-bridge` `0.12.0`, revision v21; **64 tools and 5 hooks** |
| Distribution | [Combined release archive](https://github.com/olegeklepikov-collab/ultra-deep-research/releases/download/v0.41.0a1-r152-v21/hermes-local-release-r152-v21.zip), with component archives, Foundation signature, public key, and checksum manifest |
| Software verification | Exact package checks, affected tests, local installation, applicable rollback checks, native signature verification, and twelve-class restore |
| Integration status | `integration_ready` on the validated local stand |
| Research qualification | Independent per profile and scope; no general Deep/Ultra/Academic qualification is claimed |
| Production activation | Not performed by publication |

This documentation describes that release. Use the [tagged runtime source](https://github.com/olegeklepikov-collab/ultra-deep-research/tree/v0.41.0a1-r152-v21) or its exact commit for installation; documentation on `main` can evolve independently of an immutable release.

## What the system does

| Area | Functional behavior |
|---|---|
| Research framing | Question and scope contracts, domain decomposition, concepts, competing explanations, and versioned changes |
| Bounded execution | Explicit model, time, token, source, and cost-estimate limits; retained attempts and configuration fingerprints |
| Search and discovery | Search, Deep, Ultra, and Academic entrypoints; source-family routing, coverage ledgers, and explicit missing coverage |
| Source examination | Captured response bytes, exact source references, bounded full-text reading, document chunks, PDF structure and selected page images |
| Claims and evidence | Exact quotations and locators, candidate-claim evaluation, semantic checks, independence assessment, and contradiction handling |
| Quantitative work | Numerical reproduction contracts and source-linked spreadsheet reanalysis; incompatible data are not silently pooled |
| Review and reporting | Screening/adjudication records, synthesis and challenge checks, structured results, Markdown reports, and unresolved obligations |
| Recovery and provenance | Immutable attempt records, unknown-outcome reconciliation, artifact hashes, and restart/restore evidence |

See [workflows](docs/en/workflows.md) for executable entrypoints and [all 147 research tools](docs/reference/tools.md) for the contract surface. A registered tool, a configured provider, and a qualified capability are different states.

## Architecture at a glance

```mermaid
flowchart LR
    U[Question and scope] --> H[Hermes runtime]
    H --> R[Research contracts and workflows]
    R --> S[Source acquisition and reading]
    S --> E[Fragments, claims and review]
    E --> O[Report with evidence and gaps]
    H --> F[Foundation Bridge]
    F --> D[Tasks, state, artifacts, retrieval and traces]
    D --> R
```

Hermes owns the model loop, sessions, plugin loading, and gateway. Research owns research contracts and bounded workflows. Foundation connects public tools and hooks to isolated state and storage services. It does not introduce a second agent loop. [Architecture and trust boundaries →](docs/en/architecture.md)

## Start here

1. Read [installation and verification](docs/en/installation.md). Use a new Hermes home for the full Foundation deployment.
2. Install the exact published Research commit, then run the plugin doctor before enabling it.
3. Configure a supported model route and the source route required by the chosen workflow.
4. Start with a public, non-sensitive question and a fresh output directory. Inspect the resulting status and source coverage before using a conclusion.

```sh
hermes plugins install olegeklepikov-collab/ultra-deep-research   --ref 9077d24d5e7b6dda5db7902bac2a927503791db6 --no-enable
hermes plugins doctor ultra-deep-research --ci
hermes plugins enable ultra-deep-research --no-allow-tool-override
```

These commands install the Research plugin into the selected Hermes instance. They do not provision the Foundation databases, containers, or credentials; those steps are covered separately.

## Read the result, not just the exit code

`partial`, `review_required`, and `insufficient_evidence` preserve useful work while withholding unsupported conclusions. `unknown_outcome` means an external operation may already have occurred and must be reconciled before retrying. `integration_ready` describes software integration, not the scientific reliability of every answer.

The final release smoke run completed normally with `insufficient_evidence` and no released claims. This demonstrates the bounded completion path; it is not a successful scientific benchmark. The prepared twenty-case FAIR set is narrow and was not completed or used to claim universal qualification.

## Documentation

- [Installation, OAuth, update and rollback](docs/en/installation.md)
- [Architecture, storage ownership and evidence boundaries](docs/en/architecture.md)
- [Research workflows, budgets and artifacts](docs/en/workflows.md)
- [Publication, verification, operations and limitations](docs/en/release-and-operations.md)
- [Bilingual Research tool reference](docs/reference/tools.md)
- [Bilingual Foundation tools and hooks](docs/reference/foundation.md)
- [Model classes in current development](docs/en/model-classes.md)
- [Contributing](CONTRIBUTING.md)

## License

Project code is licensed under [Apache-2.0](LICENSE). Hermes, storage engines, model providers, and external data sources retain their own licenses and service terms.
