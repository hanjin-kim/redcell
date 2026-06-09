# redcell

**Adversarial strategy scenario generator.** Turn a strategy and a single worry into N distinct stress-test scenarios — each with a cash/position trajectory and workshop diligence questions.

redcell is a **pre-workshop thinking aid**: a hypothesis generator for strategy teams running pre-mortems. It is *not* a statistical estimator, *not* a parameter-calibrated forecast, and *not* a client-facing deck. It surfaces *missed scenarios* and turns abstract risks into concrete data-gathering questions.

## What it does

Give it your strategy and one risk you're worried about. redcell:

1. **Expands** the worry into N distinct adversary scenarios across axes — competitor action, customer reaction, channel leverage, regulatory shock, macro pressure, internal execution. (The one you named is Scenario 1; the rest are ones you may not have considered.)
2. **Simulates** each scenario as an independent linear run — your C-suite vs AI-driven competitors over N turns, with an adjudication panel awarding competitive positions and booking cash.
3. **Analyzes** each trajectory honestly — axis-aligned, grounded in the actual simulation trace (it will tell you when the axis *didn't* materialize rather than forcing a narrative).
4. **Renders** a scenario-card brief: primary stressor, trajectory, per-turn cash drivers, observation triggers, and 3 specific diligence questions per scenario.

## Why not just ask ChatGPT?

A single LLM prompt gives you a plausible narrative. redcell gives you:
- **breadth** — multiple adversary axes, including ones you didn't name
- **trajectory** — multi-turn cash/position propagation, not a one-shot guess
- **honest grounding** — analysis flags when a scenario's outcome is driven by something *other* than the named axis
- **workshop-ready output** — diligence questions with measurable thresholds, not prose

## What it is NOT

- ❌ Statistical estimator — no "robust", no confidence intervals, no p-values. Each scenario is one *conditional plausible future*.
- ❌ Matched counterfactual — it does not isolate one event's causal effect.
- ❌ Calibrated forecast — cash/revenue mappings are day-0 rulebook assumptions. Use *relative comparison* and *direction*, not absolute numbers.
- ❌ A conclusion — the output is *questions to ask*, not answers to cite.

## Quickstart

```bash
# 1. Install (editable)
pip install -e .

# 2. Set LLM credentials. Any of these env-var sets works:
#    OpenAI direct:
export OPENAI_API_KEY=sk-...
#    DashScope Qwen (Alibaba):
export SF_QWEN_API_KEY=sk-...
export SF_QWEN_MODEL=qwen-plus
export SF_QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
#    Local sglang serving Qwen:
export SF_QWEN_API_KEY=local-sglang
export SF_QWEN_MODEL=Qwen/Qwen3.5-35B-A3B
export SF_QWEN_BASE_URL=http://localhost:8000/v1

# 3. Scaffold a starter config
redcell init

# 4. Edit redcell_config.yaml + scenario.yaml

# 5. Pre-flight check (verifies creds + connectivity)
redcell doctor

# 6. Generate the brief
redcell run redcell_config.yaml -o brief.md
```

## CLI

| Command | What it does |
|---|---|
| `redcell init [-o config.yaml]` | Scaffold a starter config + scenario stub |
| `redcell doctor` | Pre-flight: LLM creds, provider detection, ping, optional deps |
| `redcell run <config.yaml> -o brief.md` | Generate the adversarial scenario brief |

## Supported LLM providers

redcell auto-detects the provider from `base_url`. The adapter strips provider-incompatible kwargs so you can swap providers without touching code.

| Provider | Detected by | Status |
|---|---|---|
| **sglang local** (Qwen) | `localhost` / `10.*` / `192.168.*` + `qwen` in model name | ✅ Recommended for dev. Full `guided_json` strict schema. |
| **DashScope** (Alibaba Qwen) | `dashscope` / `aliyuncs.com` in URL | ✅ Tested. Schema is advisory (relies on prompt). Empty-content edge case observed but not reproducible. |
| **OpenAI** (api.openai.com) | no base_url, or `openai.com` | ⚠ Untested in CI. Real `json_schema` strict supported. `enable_thinking` kwarg dropped (use o1/o3/gpt-5 model names for reasoning). |
| **OpenAI-compatible** (Groq, Together, vLLM-direct, …) | anything else | ⚠ Conservative passthrough. Qwen-specific extras disabled. May parse-fail on weak-schema servers — prompts are explicit but some providers need defensive retry. |

Run `redcell doctor` to confirm the detected provider for your endpoint.

## Run config

```yaml
industry: kbeauty_premium_skincare
our_company: AURIE
competitors: [Shiseido, Amore Pacific]
strategy: |
  <your strategy in prose>
worried_risk: |
  <the one risk you're worried about>
n_scenarios: 5
max_turns: 5
scenario_path: scenarios/kbeauty_aurie.yaml
```

## Status

`0.2` — fully self-contained.

- LLM transport layer (`redcell/llm.py`) — provider-portable, auto-detects sglang / DashScope / OpenAI / generic OpenAI-compatible.
- Simulation engine (`redcell/sim/`) — multi-agent C-suite deliberation, adjudication panel, event deck, rulebook generator. Vendored from the original strategyforge implementation; no runtime dependency on strategyforge.
- Pre-workshop flow (`redcell/adversary.py`, `analysis.py`, `pipeline.py`, `render.py`) — native.

`pip install -e .` and you have a standalone tool.

## License

[MIT](LICENSE) © 2026 Hanjin Kim
