# Release, verification and operations

[Home](../../README.md) · [Русский](../ru/release-and-operations.md) · [Published release](https://github.com/olegeklepikov-collab/ultra-deep-research/releases/tag/v0.41.0a1-r153-v22)

## Exact publication identity

Tag: `v0.41.0a1-r153-v22` (**prerelease**). The public Research source is the target of this immutable tag; resolve its full commit with `git rev-parse v0.41.0a1-r153-v22^{commit}` after fetching the tag. The Foundation source commit recorded in its signed manifest is `8dd99cca1755d2f7a6e8513b9e7a72bb23f52752`. Foundation source files are distributed in `foundation.zip`; no separate public Foundation repository is claimed here.

| Artifact | Filename | SHA-256 |
|---|---|---|
| Combined ZIP | `hermes-local-release-r153-v22.zip` | See the release `SHA256SUMS` asset |
| Research r153 | `research.zip` | `6fc52b5fd64a82f257277976be6ca30a9a96993e8d6e32abaef1d3166eede6ff` |
| Foundation v22 | `foundation.zip` | `a1f34369cedec311d79228365ffd94bf6b08a228a2ef50fd5d3a5ddfb31a8d50` |

The outer ZIP contains `research.zip`, `foundation.zip`, `foundation.zip.minisig`, `release-signing.pub`, `manifest.json`, `README.md`, and a version-matched `documentation/` directory. **The Minisign signature covers Foundation.** The verified Foundation `bridge-lock.json` pins the Research ZIP hash. Verify the outer ZIP against the separate release `SHA256SUMS` asset. The manifest describes bundle members and the packaged documentation snapshot, not the mutable documentation tree on `main`.

Only public release material is distributed. Working databases, private keys, OAuth tokens, gateway credentials, private logs and the operator's home directories are excluded. Updating this documentation does not change the signed archives or release tag.

## What was verified

| Layer | Recorded evidence and limits |
|---|---|
| Packaging | Exact runtime members, checksums, license declaration, clean Foundation source binding and compatible Research pin |
| Changed behavior | Model-class routing checks in r153; bounded-route, Search-planning, short-identifier and source-selection checks inherited from r152 |
| Installation | Public plugin entrypoints, exact installed bytes and plugin doctor; applicable update/rollback evidence retained |
| Telegram/gateway | Controlled live ingress/egress, single-writer rejection, heartbeat progress and restart on an isolated local setup |
| Recovery | Twelve state classes captured, restored and read back; individual recovery thresholds checked; a single overrun blocks the result |
| Release trust | Minisign verification and native `foundation_release_verify`; `foundation_bridge_health` returned `integration_ready` |
| Prior r152 Search smoke | Normal `insufficient_evidence` completion with zero released claims; inherited evidence, not an r153 scientific benchmark |

Earlier inventories contain 44 bounded E2E executions and 862 indexed normative positions. Their counts do not mean 44 unrestricted live runs or 862 independent scientific acceptances. Each observation retains its version and scope. The prepared twenty-case FAIR corpus was not completed and is not a release-wide accuracy score.

## Changes in r153 / v22

- Research r153 adds operator-configured model classes with a bound concrete provider/model/reasoning route and recorded configuration fingerprint. A class label does not qualify its model or research results.
- Foundation v22 pins the exact r153 archive. The combined ZIP adds a version-matched `documentation/` snapshot; the outer ZIP hash is published separately in `SHA256SUMS`.
- The bounded-route, Search-planning, short-identifier and source-selection fixes from r152 remain part of the new package. They are inherited behavior, not new r153 scientific results.

## Runtime status vocabulary

These terms explain the boundaries; consult each tool's schema for its exact enumeration.

| State or flag | Operational interpretation |
|---|---|
| `configured` / `available` | Configuration or an entrypoint exists; successful qualification is not implied |
| `verified` | A named check passed for a specific input and scope |
| `partial` / `review_required` | Retained work has unresolved obligations or still requires review |
| `insufficient_evidence` | The available material does not justify the requested conclusion |
| `unknown_outcome` | An external effect may exist; reconcile before retrying |
| `integration_ready` | The software integration checks are satisfied in the observed environment |
| `qualified` | Only the specifically qualified profile/scope may inherit this decision |
| `production_activation_allowed=false` | Signature or integration success has not authorized production activation |

## Recovery and operating policy

The validation stand used a 24-hour recovery-point objective and a one-hour recovery-time objective for each of twelve classes: profiles/gateway state; Beads; Dolt databases; Dolt privileges/branch controls; runtime SQLite; AgentMemory; Graphiti/FalkorDB; Zvec source/rebuild records; artifacts; Git repositories; dependency locks; configuration manifests.

Its operator-managed job was configured every 12 hours, retained three automatic checkpoints, rejected concurrent execution, and treated state older than 24 hours as stale. Manual checkpoints were preserved. Restore was repeated after changed builds; changed configuration also invalidated the recorded runtime binding. A first actual scheduled-service execution and stale/concurrency checks were observed; a full longitudinal uptime guarantee was not established.

**That local scheduling job is part of the validation stand, not an automatically installed feature of the combined release bundle.** Foundation exposes inventory, objective and restore-assessment contracts. A deployment must provide its own backup execution, scheduling, retention and monitoring, following the component's `RECOVERY.md`. Do not treat `enabled` as evidence of a fresh successful backup.

Keep operator secrets outside Git. Provision credentials deliberately for a new instance. Reusing a Telegram bot while another gateway is polling it creates a competing consumer; use a single owner and an explicit handover. Do not silently import prior memories, jobs or acceptance states during installation.

## Troubleshooting by evidence

| Symptom | First check |
|---|---|
| `hermes_python_entrypoint_required` | Script Python and the Python `venv/bin/hermes` entrypoint must belong to the same environment |
| `model_route_not_allowed` | Confirm the supported provider/model pair in the selected home's configuration |
| Runtime/configuration changed | Preserve existing output; start a new bounded run after intentional reconfiguration |
| `unsafe_public_text` | Inspect the reported field: length/control-character rules may be responsible, not necessarily a secret leak |
| `unknown_outcome` / reconciliation required | Retain the attempt; inspect the operation/readback before a new external effect |
| Telegram `send_path_degraded` just after connect | Await confirmed polling progress; successful connection alone is not send readiness |
| Invalid release signature | Verify the exact archive, signature and trusted key; an older release signature cannot authenticate new bytes |
| Insufficient evidence or unqualified profile | Inspect missing source/reading/review obligations; do not change thresholds after seeing the answer |

## Readiness is not automatic activation

The software publication is complete. Deployment, operator activation and research-profile qualification are separate decisions. This follows the project's E2E-38, TC-214 and NFR-E32 distinction: limited integration does not inherit research qualification. The release provides the executable contracts and explicitly bounded workflows; it does not certify every research domain or every provider configuration.
