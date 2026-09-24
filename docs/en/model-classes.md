# Model classes

[Home](../../README.md) · [Русский](../ru/model-classes.md) · [Installation](installation.md)

> Version boundary: model classes are included in the r153/v22 release. The earlier r152/v21 tag remains immutable and retains its two bounded concrete routes.

## Stable requests, replaceable implementations

A research invocation selects a **model class**, not a hard-coded vendor/model pair. The operator maps that class to a concrete provider, model and reasoning setting in the selected Hermes home's `config.yaml`. Updating the model stack then changes configuration rather than research code or question templates.

Class names are operator-owned routing labels. `economy`, `balanced` and `advanced` are examples, not certified quality levels, fixed provider lists or an automatic ranking service. You can define a class such as `vision` when your selected Hermes-supported model and workflow actually meet that requirement. Naming a class does not prove the model has the capability.

## Configuration contract

Replace every `your-*`/`another-*` placeholder with identifiers supported by your configured Hermes. Provider authentication and custom endpoint configuration remain Hermes responsibilities.

```yaml
research:
  default_model_class: balanced
  model_classes:
    economy:
      provider: your-provider-id
      model: your-current-small-model-id
      reasoning: low
    balanced:
      provider: your-provider-id
      model: your-current-general-model-id
      reasoning: medium
    advanced:
      provider: another-provider-id
      model: your-current-reasoning-model-id
      reasoning: high
```

- Class identifiers match `[a-z][a-z0-9_-]{0,31}`.
- Each class declares exactly `provider`, `model` and `reasoning`. Use an explicit canonical Hermes provider ID; `auto` and endpoint URLs in the model field are not accepted. Configure endpoints through Hermes.
- Reasoning syntax follows Hermes: `none`, `minimal`, `low`, `medium`, `high`, `xhigh`, `max`, `ultra`. The selected provider/model must support the chosen setting.
- `research.default_model_class` chooses the class when the invocation does not override it.
- `HERMES_RESEARCH_MODEL_CLASS` selects a class for one process and its inherited child workflow stages.
- An unknown class, incomplete entry or missing selection fails before a model call. There is no silent fallback to another class or vendor.

```sh
HERMES_RESEARCH_MODEL_CLASS=balanced   "$UDR_PYTHON" "$UDR_SCRIPTS/run_beta_search.py"   --question 'Your bounded public question'   --hermes "$UDR_HERMES"   --output-root "$HERMES_HOME/research-runs" --public-query-ack
```

The environment variables for the executable and script directory are introduced in [workflows](workflows.md). Select another class before starting a new invocation. Switching the class or its mapping halfway through an existing invocation is configuration drift and is rejected.

## Compatibility without a class table

If `research.model_classes` is absent, the restricted caller uses the **actual loaded Hermes** `model.provider` and `model.default`. It does not supply an embedded Nano/OpenRouter fallback. In this mode, reasoning uses explicit `agent.reasoning_effort`, or `none` if omitted. The class-selection environment variable is not accepted without a class table.

This direct configuration path supports existing operator-managed Hermes setups while removing model-name lists from the Research plugin. It is not a promise that every conceivable provider API works: transport, credentials, endpoint support, multimodal support and usage reporting must work in Hermes.

## Reproducibility and accounting

An invocation freezes the requested class, routing origin, routing-table fingerprint and resolved provider/model/reasoning. It checks the effective configuration again before calling the model. Worker arguments, the saved attempt and returned usage must agree. Class selection is part of the runtime environment snapshot.

The receipt preserves the **concrete model identifier reported by Hermes** even though the request was class-based. Provider-side aliases can change independently; use versioned identifiers where available when strict reproducibility is required. This record does not attest to a remote model’s internal weights. Two runs called `balanced` can therefore be distinguished after an operator changes the mapping. Historical receipts retain their original route; they are not relabelled as executions of the new model.

Time, token, call-count and cost-estimate checks remain in force. Subscription-included estimates are labelled as such; missing or unreliable accounting must not be presented as a verified cash price. Model classes do not introduce automatic failover, spend authorization, background model discovery, or a new provider SDK.

## Recorded routing fields

| Field | Meaning |
|---|---|
| `requested_model_class` | Selected class; `null` for the direct Hermes-default path |
| `model_class_selection_source` | `environment`, `configured_default`, or `not_applicable` |
| `model_route_source` | `research_model_class` or `hermes_model_default` |
| `model_class_mapping_hash` | Fingerprint of the class table and default; `null` without a table |
| `provider`, `model`, `reasoning` | Resolved concrete route checked against the actual invocation |

## Updating the stack

1. Choose a model available through your authorized Hermes provider configuration.
2. Change the relevant class mapping and compatible reasoning setting.
3. Complete or reconcile old attempts under their recorded conditions; start fresh invocations with the new mapping.
4. Verify the affected capability and retain the new concrete route in its receipt. Preserve separate scientific qualification and release decisions.

The published r153/v22 [installation recipe](installation.md) includes model classes. The signed release bundle and its `documentation/` snapshot provide the version-matched instructions; the older r152/v21 archive remains unchanged.
