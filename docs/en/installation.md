# Installation and configuration

[Home](../../README.md) · [Русский](../ru/installation.md)

> These steps reproduce the signed r153/v22 release, including [model classes](model-classes.md).

## Choose the deployment surface

The Research plugin provides local contract tools and bounded research scripts. A complete managed deployment additionally needs Foundation and its state services. Installing a plugin does not provision those services or authenticate a model.

The source packages require Python 3.11 or later. The release stand used Python 3.13 on macOS with Docker. Foundation pins Hermes 0.21.3 at commit `2034126e0d1f397b4612782156097243dbbdc819` plus its packaged Telegram callback patch. Do not substitute an arbitrary Hermes build when reproducing this release.

Prerequisites by feature:

| Feature | Prerequisites |
|---|---|
| Research contract tools | Compatible Hermes and plugin loader; dependencies declared in `plugin.yaml` |
| Model-assisted workflows | Authorized supported model route; Python and `venv/bin/hermes` from the same environment |
| Bounded web acquisition | The Keenable-only route shown below; working outbound HTTPS |
| PDF examination | `pdfplumber==0.11.9`; relevant workflows also need `psutil`, `anydoc`, `pdfinfo` and `pdftoppm`/Poppler |
| Foundation state services | Git, Beads, Dolt, Docker, age and Minisign as required by the component guides and pinned manifests |

The Hermes plugin installer displays Python dependencies but does not automatically install them. Install the declared packages into the actual Hermes environment. Resource-limited parsing is not a substitute for isolating untrusted documents.

## Download and verify

Use an empty directory. The published bundle is immutable; checksums refer to that bundle, not this evolving documentation.

```sh
mkdir udr-r153-v22
cd udr-r153-v22
gh release download v0.41.0a1-r153-v22 --repo olegeklepikov-collab/ultra-deep-research
shasum -a 256 -c SHA256SUMS
unzip -n hermes-local-release-r153-v22.zip
minisign -Vm foundation.zip -p release-signing.pub
```

`manifest.json` lists the component checksums. The trusted public-key fingerprint is SHA-256 `2295aaab3cb418c4f81a867a701a8187e8cdd0f73105a1f318c1faf981dfdb1a`. Verify `research.zip` against `research_report.bundle_sha256` in `bridge-lock.json` inside the verified Foundation archive. This establishes the component pairing; the outer ZIP has a published checksum and contains the Foundation signature.

## Install Research into a new instance

Choose and initialize a new Hermes home using the supported Hermes setup flow; do not point these variables at a working instance accidentally. Configure your Git author name and email first. Then create a local Git source from the verified `research.zip` manifest and install that exact local commit:

```sh
export HERMES_HOME="$HOME/.hermes-udr"
export HERMES_FOUNDATION_ROOT="$HERMES_HOME/foundation"
unzip -n research.zip -d research-source
python3 - <<'PYCODE'
import json
import subprocess
from pathlib import Path
root = Path("research-source").resolve()
manifest = json.loads((root / "bundle-manifest.json").read_text())
files = [row["path"] for row in manifest["files"]] + ["bundle-manifest.json"]
subprocess.run(["git", "-C", str(root), "init", "-b", "release"], check=True)
subprocess.run(["git", "-C", str(root), "add", "--", *files], check=True)
subprocess.run(["git", "-C", str(root), "commit", "-m", "Exact Research r153 package"], check=True)
PYCODE
UDR_SOURCE_REF="$(git -C research-source rev-parse HEAD)"
hermes plugins install "file://$PWD/research-source" --ref "$UDR_SOURCE_REF" --no-enable
hermes plugins doctor ultra-deep-research --ci
hermes plugins enable ultra-deep-research --no-allow-tool-override
```

The release tag is `v0.41.0a1-r153-v22`. The local commit above is generated from the archive bytes and differs from the public source commit. Its manifest-listed files, not the mutable repository tree or README, define the installed package.

## Authenticate and select the model

For a separate Codex OAuth session in the selected Hermes home:

```sh
hermes auth add openai-codex --type oauth --label "UDR workstation"
```

Complete the device-login instructions, then add the following model/source configuration to that instance's `config.yaml`. Authentication alone does not choose the model route.

```yaml
model:
  provider: openai-codex
  default: gpt-5.6-sol
research:
  default_model_class: balanced
  model_classes:
    balanced:
      provider: openai-codex
      model: gpt-5.6-sol
      reasoning: low

web:
  search_backend: keenable
  extract_backend: keenable
  keyless_rescue: false
  provider_tier:
    keenable: free
    exa: paid
    parallel: paid
    firecrawl: paid
```

The three `paid` tier entries exclude those vendors from the keyless fallback ring; the bounded workflow selects only Keenable and disables rescue. This does not provision credentials or authorize paid calls to those providers.

The `balanced` label is an operator-selected route, not a quality grade. You may map a class to another Hermes-supported, authorized provider/model/reasoning combination; the concrete route is recorded and checked during the run. Without a class table, the worker uses the loaded Hermes `model.provider` and `model.default`. Disable `fallback_model` and `fallback_providers` for bounded calls. Do not change configuration during a run: the runtime fingerprint is checked before subsequent operations.

OAuth credentials stay in the selected home's private auth store. Never add them to the repository. An `included` cost record with zero per-call estimate is subscription accounting, not a statement that the entire workflow has no economic cost.

## Add Foundation when required

After verifying the archive, the following creates a local Git source from exactly its manifest-listed files. Configure your own Git author identity first. The new local installation commit is distinct from the original Foundation source commit recorded in the signed manifest.

```sh
unzip foundation.zip -d foundation-source
python3 - <<'PYCODE'
import json
import subprocess
from pathlib import Path
root = Path("foundation-source").resolve()
manifest = json.loads((root / "bundle-manifest.json").read_text())
files = [row["path"] for row in manifest["files"]] + ["bundle-manifest.json"]
subprocess.run(["git", "-C", str(root), "init", "-b", "release"], check=True)
subprocess.run(["git", "-C", str(root), "add", "--", *files], check=True)
subprocess.run(["git", "-C", str(root), "commit", "-m", "Exact Foundation v22 package"], check=True)
PYCODE
UDR_FOUNDATION_REF="$(git -C foundation-source rev-parse HEAD)"
hermes plugins install "file://$PWD/foundation-source" \
  --ref "$UDR_FOUNDATION_REF" --no-enable
hermes plugins doctor hermes-foundation-bridge --ci
hermes plugins enable hermes-foundation-bridge --no-allow-tool-override
```

Complete the packaged `README.md`, `RELEASE.md`, `DOLT_SQL.md` and `RECOVERY.md` instructions before enabling managed operations:

1. Create a new checkout of the Hermes commit in `bridge-lock.json`; apply the packaged callback patch there after checking its source hash and `git apply --check`. Verify the patched Telegram file hash.
2. Create new Foundation roots, profiles, service identities, Docker networks/volumes and local credentials. Provision the pinned SQL, memory, graph and retrieval components.
3. Preview `foundation_bridge_migrate` with `apply=false`; apply migrations only to the intended new root, then initialize the relevant profile/index/graph/memory/Beads components.
4. Stage the Foundation ZIP, signature and public key in `HERMES_FOUNDATION_ROOT/releases/hermes-foundation-bridge-0.12.0/` using the filenames in the packaged release guide. Invoke `foundation_release_verify` with version `0.12.0` and commit `8dd99cca1755d2f7a6e8513b9e7a72bb23f52752`.
5. Inspect `foundation_bridge_health`, complete the applicable instance gates, and record the separate operator activation decision. Enabling the plugin registers its tools; it does not activate production.

These are explicit deployment steps; the combined ZIP is not a one-click installer or a backup of the author's working environment.

## Update and rollback

Record the currently installed exact commit and retain its verified archive before updating. Disable the affected plugin, install the new exact ref with `--force --no-enable`, run its doctor and relevant characteristic checks, and enable it only after a successful decision. Rollback uses the retained old ref through the same public installer.

Keep a compatible Research/Foundation pair. A successful code rollback does not restore changed databases or justify discarding new records; data recovery follows the recovery contract separately. Never reuse a signature for a changed archive.
