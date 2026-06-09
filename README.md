# redcell

> 🇺🇸 [English version](README.en.md)

**워크숍 전에 전략을 미리 깨뜨려 보는 도구.** 신경 쓰이는 위협 하나를 여러 각도의 시나리오로 펼치고, 각각의 현금·점유율 궤적과 워크숍에서 던질 만한 구체적인 질문을 만들어 줍니다.

전략기획팀이 사전 점검을 돌리거나, 컨설턴트가 보고서 초안을 잡기 전에 빈 곳을 짚어 보는 용도. 평소 안 보이던 시나리오를 끌어내고, 막연한 우려를 *어떤 데이터를 확인해야 하는지*로 바꿔 줍니다.

## 동작 방식

전략과 걱정되는 위협 한 가지를 입력하면:

1. **시나리오 확장** — 입력한 위협을 6개 축(경쟁사 행동, 고객 반응, 채널 압박, 규제 충격, 거시 환경, 내부 실행)으로 펼쳐 서로 다른 N개의 적대적 시나리오를 만듭니다. 입력한 위협은 첫 번째 시나리오로 보존되고, 나머지는 미처 떠올리지 못했을 수 있는 다른 종류의 위협으로 채워집니다.
2. **시뮬레이션** — 각 시나리오를 여러 턴에 걸쳐 돌립니다. 우리 측 C-suite(CEO/CFO/CTO/CMO/COO)와 경쟁사가 매 턴 의사결정을 내리고, adjudicator 패널이 시장 포지션을 매기고 현금을 정산합니다.
3. **분석** — 각 궤적을 시나리오의 축 관점에서 다시 읽습니다. 그 축이 시뮬레이션에서 실제로 발현되지 않았다면 억지로 끼워 맞추지 않고 그 사실을 그대로 적습니다. 매 턴 현금 변동의 주요 동인도 숫자까지 노출합니다.
4. **브리프 출력** — 시나리오별 카드 형식 마크다운. 핵심 스트레스 요인, 궤적, 현금 동인, 관찰 신호, 그리고 워크숍에서 바로 쓸 수 있는 구체적인 진단 질문 3개씩.

## ChatGPT에 한 번 물어보는 것과의 차이

LLM에 한 번 물어보면 그럴듯한 서사 하나를 받습니다. redcell이 더 주는 것:

- **폭** — 사용자가 명시한 위협 외에 다른 축의 시나리오도 함께 surface
- **궤적** — 여러 턴에 걸친 현금·포지션 전개, 한 번에 추측한 결과가 아님
- **솔직한 결론** — 결과가 명시한 축이 아닌 다른 요인 때문이었다면 분석이 그대로 적음
- **워크숍에서 바로 쓸 수 있는 질문** — 측정 가능한 임계값이 들어간 진단 질문, 산문 narrative가 아님

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

## 비용 감각 (2 시나리오 × 2 턴 기준)

| 모델 | 추정 비용 |
|---|---|
| **qwen3.5-flash** (DashScope) | $0.35-0.60 |
| **qwen3.5-plus** (DashScope) | $2-3 |
| 권장 기본값 5 × 5 | flash 약 $2-4, plus 약 $12-20 |
| sglang 로컬 | $0 |

## Run config 예시

```yaml
strategy: |
  <여기에 전략을 산문으로>
worried_risk: |
  <걱정되는 risk 한 줄>
n_scenarios: 5
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
