# redcell

> 🇺🇸 [English version](README.en.md)

**전략을 *주어진 환경* 아래 시뮬레이션해서 우리 팀과 경쟁사가 어떻게 반응하는지 보는 도구.** 한 번의 시뮬레이션이 multi-turn으로 진행되며, 양측이 환경에 *합리적으로* 반응하는 trajectory를 출력합니다.

전략기획팀이 사전 점검을 돌리거나, 컨설턴트가 보고서 초안을 잡기 전에 *환경 가정 하 양측 반응*을 미리 보기 위한 용도.

**예시 시나리오 + 결과물** (4개 산업, 각 디렉토리에 `config.yaml` + 생성된 brief)

| 시나리오 | 우리 측 | 환경 | 산물 |
|---|---|---|---|
| [aurie](examples/aurie/) | AURIE (K-beauty mid-cap) | Shiseido 30% 가격 인하 | [brief](examples/aurie/brief.md) · [trace](examples/aurie/brief_trace.md) |
| [hbm](examples/hbm/) | SK Hynix | NVIDIA Blackwell + supplier 다변화 | [brief](examples/hbm/brief.md) · [trace](examples/hbm/brief_trace.md) |
| [streaming](examples/streaming/) | Coupang Play | Netflix Korea 가격 인상 | [brief](examples/streaming/brief.md) · [trace](examples/streaming/brief_trace.md) |
| [fintech](examples/fintech/) | Toss | 금감원 수수료 인하 권고 | [brief](examples/fintech/brief.md) · [trace](examples/fintech/brief_trace.md) |

## 동작 방식

전략 + 환경을 입력하면:

1. **환경 주입** — 환경을 *우리 측 deliberation 컨텍스트*와 *각 경쟁사의 strategy*에 모두 주입합니다. 경쟁사도 환경을 알고 그에 맞춰 행동합니다.
2. **Multi-turn 시뮬레이션** — 매 턴 모든 측 C-suite(CEO/CFO/CTO/CMO/COO)가 *독립적으로* 의사결정을 내리고, adjudicator 패널이 시장 포지션을 매기고 현금을 정산합니다.
3. **브리프 출력** — 요약 표 + 턴별 전개 (양측 행동 / 포지션 / 현금) + 우리 측 현금 동인 분해.

## ChatGPT에게 물어보는 것 과의 차이

LLM에 한 번 물어보면 그럴듯한 서사 하나를 받습니다. 하지만 redcell 은 보다 더 고도화된 시뮬레이터입니다:

- **양측 반응 동시 모델링** — 우리만 행동하는 게 아니라, 경쟁사도 같은 환경에 따라 *자기 입장에서* 매 턴 행동합니다
- **궤적** — 여러 턴에 걸친 현금·포지션 전개. 첫 턴 행동의 결과가 다음 턴 의사결정에 누적
- **현금 정산 투명성** — 매 턴 현금 변화의 동인 (action 비용 / event Δ / position revenue) 분해

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

`base_url`에서 provider를 자동으로 알아내고, 어댑터가 provider별로 안 통하는 옵션을 알아서 잘라 보냅니다. 그래서 provider를 바꿔도 코드는 손대지 않습니다.

| Provider | 감지 조건 | 상태 |
|---|---|---|
| **sglang 로컬** (Qwen) | `localhost` / `10.*` / `192.168.*` + 모델명에 `qwen` | ✅ 개발 환경 권장. `guided_json`이 토큰 단위로 스키마를 강제 |
| **DashScope** (알리바바 Qwen) | URL에 `dashscope` / `aliyuncs.com` | ✅ E2E 스모크 검증 완료. 스키마는 권고 수준이지만 프롬프트로 보완. 드물게 reasoning이 폭주하면 어댑터가 thinking을 끄고 자동 재시도 |
| **OpenAI** (api.openai.com) | base_url 없거나 `openai.com` 포함 | ⚠ 실 테스트 미진행. `json_schema strict`는 진짜로 동작. `enable_thinking` 인자는 무시되며, reasoning은 o1/o3/gpt-5 같은 모델명으로 활성화 |
| **OpenAI-compatible** (Groq, Together, vLLM-direct 등) | 그 외 모든 endpoint | ⚠ 보수적 패스스루. Qwen 전용 옵션은 모두 비활성. 스키마 강제가 약한 서버에서는 프롬프트의 명시적 필드 나열에 의존 |

지금 endpoint가 어떤 provider로 잡히는지는 `redcell doctor`로 확인할 수 있습니다.

## 비용 감각

한 번의 `redcell run` = 1 trajectory × `max_turns` 턴. 매 턴 모든 측 C-suite 토론 + adjudicator 패널이 돌아가서 토큰 사용량이 턴 수에 거의 선형으로 비례합니다.

| 모델 | `max_turns=5` 기준 |
|---|---|
| **qwen3.5-flash** (DashScope) | $1-2 |
| **qwen3.5-plus** (DashScope) | $6-10 |
| sglang 로컬 | $0 |

초기 셋업 (rulebook + event_deck + competitor_strategies LLM 생성) 은 scenario hash 단위로 캐시되어, 같은 scenario.yaml 을 다시 돌리면 그 부분만큼 비용이 줄어듭니다. CLAUDE.md 의 override hook 으로 LLM 생성 자체를 끄면 더 줄어듭니다.

## Run config 예시

```yaml
strategy: |
  <우리가 수행하는 전략 — 시뮬 전체에 걸쳐 정적>
environment: |
  <시뮬 시작 시점의 시장/위협 조건. 모든 측 deliberation 컨텍스트에 주입됨>
max_turns: 5
scenario_path: scenarios/kbeauty_aurie.yaml
```

산업·우리 회사·경쟁사 정보는 `scenario_path`가 가리키는 시나리오 YAML 안의 `sides`에서 읽어옵니다.

## 구성

- LLM 호출 계층 (`redcell/llm.py`) — sglang / DashScope / OpenAI / 그 외 OpenAI 호환 endpoint를 자동으로 구분해 다룹니다.
- 시뮬레이션 엔진 (`redcell/sim/`) — 멀티 에이전트 C-suite 토론, adjudicator 패널, 이벤트 덱, 룰북 생성기.
- 사전 워크숍 파이프라인 (`redcell/adversary.py`, `analysis.py`, `pipeline.py`, `render.py`) — 적대 시나리오 생성, 궤적 분석, 브리프 렌더링.

## 라이선스

[MIT](LICENSE) © 2026 Hanjin Kim
