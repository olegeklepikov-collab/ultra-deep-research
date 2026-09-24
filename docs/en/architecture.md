# Architecture and evidence model

[Home](../../README.md) · [Русский](../ru/architecture.md)

## Three responsibilities

**Hermes runtime.** Owns sessions, model invocation, public plugin tools/hooks, gateway lifecycle, and user-facing transport. The validated Foundation dependency is Hermes `0.21.3` at commit `2034126e0d1f397b4612782156097243dbbdc819`, plus the callback-authorization patch pinned in the Foundation archive. A version number alone does not identify this composite dependency.

**Research component.** The `plugin.py` entrypoint registers 147 research tools. Most evaluate typed local requests and emit decisions or receipts; selected diagnostic/provider paths perform external operations. The `research` skill and `skills/research/scripts/` implement bounded, model-assisted workflows. These are two distinct interfaces: validating a contract does not execute the entire research process.

**Foundation Bridge.** Registers 64 tools and five hooks, connecting research work to persistent state and external storage services. It supplies authority checks, leases, idempotency, artifact handling, profile handoff, trace collection, and release/recovery checks. The Research component can expose its local contract surface without a complete storage deployment; managed integration requires the corresponding Foundation services.

## State ownership

| System | Responsibility | Interpretation boundary |
|---|---|---|
| Beads | Task identity, assignment, lifecycle and dependencies through the public CLI | Closing a task does not accept a result |
| Dolt SQL | Versioned objects, revisions, commits and restricted writer authority | A commit does not certify scientific truth |
| Runtime SQLite | Execution coordination, leases, external-operation records and outbox state | Cross-store work uses recovery protocols, not one distributed ACID transaction |
| Artifact store | Original bytes, content hashes, metadata, atomic publication and quarantine | Hash equality verifies identity, not relevance or rights |
| AgentMemory | Scoped contextual memory | Retrieved memory is a candidate contribution, not primary evidence |
| Graphiti / FalkorDB | Scoped graph facts and retrieval | A graph edge does not independently prove its claim |
| Zvec | Rebuildable retrieval from an accepted source ledger | This release's validated profile is FTS/BM25, `embedding_model=none`, `dimension=0` |
| Observability SQLite | Traces, bounded hook queue and reconciliation | Content is minimized; a trace receipt is not a scientific review |

The Dolt databases are `kw_core`, `kw_context`, `kw_quant`, and `kw_registry`. The live SQL service is the authority for SQL-managed objects; Beads remains behind its own CLI boundary. Per-instance `BEADS_DIR` prevents accidental selection of a parent workspace.

## From source to report

1. **Declare scope and limits.** Record the question, concepts, source families, protocol where applicable, and budgets.
2. **Capture.** Retain the exact request/response context and source bytes with hashes and observed retrieval outcomes.
3. **Select and read.** Preserve the acquisition ledger. Selection does not erase screened, missing, or unreviewed leaves.
4. **Form candidates.** Link a proposed claim to its source, quotation, and locator. Exact quotation matching and semantic support are separate checks.
5. **Review and qualify.** Assess independence, contradictions, limitations, scope and review obligations. Multiple URLs may share the same underlying work or error channel.
6. **Publish a result artifact.** Produce structured data and a readable report with the surviving qualifications and gaps. Research acceptance and external delivery remain separate decisions.

A *receipt* is a structured, hash-bound record of inputs, observations and a decision. It supports provenance and tamper detection. It does not establish the truth of assertions supplied to it; some records explicitly retain unverified declarations.

## Execution boundaries

Model calls use a bounded route selected at process startup and checked again before invocation. Attempt, worker and usage records must agree on provider, model and reasoning setting. Runtime fingerprints cover relevant configuration files and effective provider inputs; changed configuration stops subsequent work while preserving existing output. This is boundary checking, not a filesystem lock or an attestation of a remote provider's internal configuration.

External writes record their intent before execution. Lost responses can produce `unknown_outcome` and `safe_to_retry=false`; a retry must not silently create another effect. Artifact publication uses temporary writes, atomic rename and readback. Recovery distinguishes a completed historical operation from a freshly verified one.

## Isolation and activation

New deployments use new roots, profiles, stores, service identities and operator-provided credentials. Importing a previous runtime's directories, memories or acceptance states is not an implicit installation step. The parser's time/memory limits are resource controls, not a security sandbox.

Foundation gates G0–G8 cover structure, infrastructure, memory/graph, evidence fragments, Telegram, profiles, multi-agent work, operations and integration. Research also has its own qualification records. Their similarly named vectors are not interchangeable. `foundation_ready` must not promote a research profile, and a signed archive must not itself activate production.

See [operations](release-and-operations.md) and the [release source](https://github.com/olegeklepikov-collab/ultra-deep-research/tree/v0.41.0a1-r152-v21).
