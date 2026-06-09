# redcell

> 🇺🇸 [English version](README.en.md)

**전략을 워크숍 *전* stress-test 하는 도구.** 한 가지 걱정거리를 *여러 axis의 N개 adversary scenarios*로 펼쳐서, 각각의 cash/position trajectory와 *측정 가능한 워크숍 질문*을 출력합니다.

전략기획팀의 *pre-mortem*, 컨설턴트의 *deck prep 전 빈틈 점검*에 사용. *missed scenarios* 발굴 + *추상 risk를 구체적 데이터 요청으로 전환*.

## 무엇을 하나

전략과 *걱정되는 risk 한 가지*를 입력하면 redcell은:

1. **확장** — 입력 risk를 6개 axis (competitor action / customer reaction / channel leverage / regulatory shock / macro pressure / internal execution)에 걸쳐 N개 distinct adversary scenarios로 풀어냄. 사용자 worry는 Scenario 1로 보존, 나머지는 *생각 못 했을 수도 있는 위협*.
2. **시뮬레이션** — 각 시나리오를 multi-turn linear run으로 실행. 우리 C-suite (CEO/CFO/CTO/CMO/COO) vs AI 경쟁사 deliberation, adjudication panel이 *position tier* 부여하고 cash 정산.
3. **분석** — 각 trajectory를 axis 기준 재해석. Axis가 trace에 *명확히 materialize 안 했으면* 솔직히 명시 — narrative 강요 안 함. Per-turn cash drivers 산술까지 노출.
4. **렌더링** — Scenario card 형식 brief: primary stressor / trajectory / cash drivers / observation triggers / 3개 구체 diligence questions.

## ChatGPT 한 번 물어보는 것과 차이

단일 LLM prompt는 *그럴듯한 narrative 하나*를 줍니다. redcell의 차별점:
- **breadth** — 사용자가 명시 안 한 axis까지 포함한 여러 adversary 후보
- **trajectory** — multi-turn cash/position propagation, *한 방 짐작* 아님
- **honest grounding** — 분석이 *axis 외 다른 요인*이 결과를 끌었으면 그대로 표기
- **workshop-ready output** — *측정 가능 threshold* 있는 diligence questions, 산문 아님

## Quickstart

```bash
# 1. 설치 (editable)
pip install -e .

# 2. LLM credentials 설정 — 아래 셋 중 하나
#    OpenAI 직접:
export OPENAI_API_KEY=sk-...
#    DashScope Qwen (Alibaba Cloud):
export SF_QWEN_API_KEY=sk-...
export SF_QWEN_MODEL=qwen-plus
export SF_QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
#    로컬 sglang serving Qwen:
export SF_QWEN_API_KEY=local-sglang
export SF_QWEN_MODEL=Qwen/Qwen3.5-35B-A3B
export SF_QWEN_BASE_URL=http://localhost:8000/v1

# 3. 시작 config scaffold
redcell init

# 4. redcell_config.yaml + scenario.yaml 편집

# 5. Pre-flight check (creds + 연결성 점검)
redcell doctor

# 6. Brief 생성
redcell run redcell_config.yaml -o brief.md
```

## CLI

| Command | 설명 |
|---|---|
| `redcell init [-o config.yaml]` | 시작 config + scenario stub scaffold |
| `redcell doctor` | LLM 자격증명 / provider 자동 감지 / ping / optional dep 점검 |
| `redcell run <config.yaml> -o brief.md` | Adversary scenario brief 생성 |

## 지원 LLM provider

redcell은 `base_url`에서 provider를 *자동 감지*. 어댑터가 provider별 비호환 kwargs를 자동 제거하므로 *코드 수정 없이* provider 전환 가능.

| Provider | 자동 감지 조건 | 상태 |
|---|---|---|
| **sglang local** (Qwen) | `localhost` / `10.*` / `192.168.*` + 모델명에 `qwen` | ✅ Dev 권장. `guided_json` 완전 strict |
| **DashScope** (Alibaba Qwen) | URL에 `dashscope` / `aliyuncs.com` | ✅ E2E smoke 검증. Schema는 *advisory* (prompt가 보호). 드물게 reasoning runaway → adapter가 자동 retry |
| **OpenAI** (api.openai.com) | base_url 없거나 `openai.com` 포함 | ⚠ CI 미검증. `json_schema strict` 실제 동작. `enable_thinking` kwarg는 무시 (reasoning은 o1/o3/gpt-5 모델명으로 활성화) |
| **OpenAI-compatible** (Groq, Together, vLLM-direct, …) | 그 외 모든 endpoint | ⚠ Conservative passthrough. Qwen 전용 extras 비활성. Schema 약한 server는 *prompt explicit listing*에 의존 |

`redcell doctor`로 현재 endpoint의 감지된 provider 확인 가능.

## 비용 (참고용 — 2 scenario × 2 turn 기준)

| 모델 | 추정 비용 |
|---|---|
| **qwen3.5-flash** (DashScope) | $0.35-0.60 |
| **qwen3.5-plus** (DashScope) | $2-3 |
| 5 scenario × 5 turn (권장 default) | flash $2-4, plus $12-20 |
| 로컬 sglang | $0 (시간 비용만) |

MBB 워크숍 reference ($50-200k)와 비교 시 *coffee 값*. 단 절대 무료 아님.

## Run config 예시

```yaml
industry: kbeauty_premium_skincare
our_company: AURIE
competitors: [Shiseido, Amore Pacific]
strategy: |
  <여기에 전략을 산문으로>
worried_risk: |
  <걱정되는 risk 한 줄>
n_scenarios: 5
max_turns: 5
scenario_path: scenarios/kbeauty_aurie.yaml
```

## 상태

`0.2` — fully self-contained.

- LLM transport (`redcell/llm.py`) — provider-portable, sglang/DashScope/OpenAI/generic 자동 감지
- Simulation engine (`redcell/sim/`) — multi-agent C-suite deliberation, adjudication panel, event deck, rulebook 생성기. 원래 strategyforge에서 vendored, *runtime 의존 0*
- Pre-workshop flow (`redcell/adversary.py`, `analysis.py`, `pipeline.py`, `render.py`) — native

`pip install -e .` 한 줄이면 standalone 도구.

## 라이선스

[MIT](LICENSE) © 2026 Hanjin Kim
