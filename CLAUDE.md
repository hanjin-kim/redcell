# redcell — guide for Claude Code agents

> 사용자가 Claude Code로 redcell 을 커스터마이즈할 때 이 파일을 먼저 읽으세요.
> 특히 "**도메인 경험표(experience table) 를 가진 사용자**" — 산업별 액션 효과 범위, 이벤트 풀, 경쟁사 행동 패턴을 이미 알고 있는 사용자가 그것을 LLM 생성이 아닌 *자기 데이터*로 주입하는 경로가 이 문서의 1순위입니다.

## 한 줄 요약

redcell 은 `(전략, 환경) → multi-turn 시뮬레이션 → 양측 반응 trajectory` 도구. 입력은 `redcell_config.yaml` + `scenario.yaml`, 출력은 `brief.md` + `brief_trace.md`.

## Override hooks — 경험표를 가진 사용자의 1순위 경로

`scenario.yaml` 의 *top-level* 에 아래 키를 채우면 해당 단계 LLM 생성을 *건너뜁니다*. 일부만 채우는 부분 override 도 가능 — 채운 것은 사용자 데이터, 비운 것은 LLM 생성.

### 권장 워크플로 — 처음부터 손으로 쓰지 말 것

`rulebook` / `event_deck` (12-18 이벤트) / `competitor_strategies` 를 백지에서 손으로 쓰는 건 비효율. 표준 흐름:

1. **첫 실행** — scenario.yaml 의 override 키들을 비워두고 `redcell run` 실행. LLM 이 산업별로 모두 자동 생성.
2. **결과 확인** — `<cache_dir>/generated_overrides.yaml` 에 현재 사용 중인 rulebook + event_deck + competitor_strategies 가 한 파일에 사람이 읽을 수 있는 YAML 로 dump 됨. 헤더에 각 블록이 *user-supplied* 인지 *auto-generated* 인지 표시.
3. **검토 / 편집** — 그 파일을 열어 LLM 이 산업 특성을 잘못 잡은 부분 (확률, side_effects 비대칭, 누락 이벤트) 수정.
4. **paste-back** — 편집한 블록 (예: `event_deck:` 전체) 을 scenario.yaml 의 top-level 로 복사. 다음 실행부터 override 활성화 → 그 부분 LLM 호출 0회.

> LLM 생성이 *실패* 하면 silent fallback 없이 즉시 `RuntimeError` 로 종료합니다. 에러 메시지가 "scenario.yaml 에 그 블록을 직접 채우라" 고 안내합니다 — 분석이 fallback 으로 조용히 망가지는 일은 없습니다.

### 1) `rulebook` — 액션 효과 범위 (가장 유용)

산업별로 `Price Cut` 이 share 를 몇 pp 흔드는지, cash 를 얼마나 쓰는지의 *범위*. 사내에 이 데이터가 있다면 LLM 짐작보다 훨씬 정확.

```yaml
# scenario.yaml
industry: semiconductor_memory
sides: [...]
rulebook:
  industry: semiconductor_memory
  revenue_coefficient: 0.08   # position revenue 가 cash 에 기여하는 계수
  rules:
    - action_type: Price Cut
      description: Aggressive pricing
      share_delta_range: [2, 6]       # 결과 share Δ 의 허용 범위 (pp)
      cash_cost_range: [-0.06, -0.02] # 정규화 cash [0,1] 기준 비용
      delay_turns: 0                  # 효과 발현 지연
      available_to: [all]             # 또는 [side_a, side_b] 처럼 특정 측 전용
    - action_type: Capacity Expansion
      description: Fab build-out
      share_delta_range: [4, 12]
      cash_cost_range: [-0.10, -0.05]
      delay_turns: 2
      available_to: [side_a, side_b]
  market_characteristics:
    switching_cost: high
    winner_take_all_tendency: medium
    regulation_impact: low
    innovation_cycle: short
```

스키마는 `redcell/sim/rulebook.py::_generate_rulebook` 의 fallback 구조 그대로. 한 액션이라도 빠뜨리면 deliberation 이 그 액션을 *선택지에서 빼고* 답합니다 — 망가지지 않고 좁아질 뿐.

### 2) `event_deck` — 산업별 외생 이벤트 풀

C-suite 가 통제 못 하는 시장 충격 카드 12-18 장. 산업별로 어떤 충격이 어느 정도 확률로 어느 측을 어떻게 때리는지 — 이게 *진짜 경험표* 의 형태.

```yaml
event_deck:
  - id: evt_01
    name: Export Control Tightening
    label_ko: 수출규제 강화
    description: 미국이 AI 반도체 수출통제를 추가 강화
    category: geopolitical
    effects:
      mode: per_side
      side_effects:
        side_a: {cash_delta: -0.03}
        side_b: {cash_delta: -0.05}
    probability: 0.15        # 매 턴 발현 확률
    eligible_turns: [2, 3, 4, 5]
    max_occurrences: 1
    mutex_group: trade_policy
  - id: evt_02
    name: Industry-Wide Demand Surge
    label_ko: 산업 수요 급증
    description: AI 인프라 투자 확대
    category: market
    effects:
      mode: uniform
      uniform_cash_delta: 0.03
    probability: 0.12
    eligible_turns: [3, 4, 5]
    max_occurrences: 1
    mutex_group: demand_cycle
```

규칙:
- `mode: uniform` → `uniform_cash_delta` (스칼라). `side_effects` 넣지 말 것.
- `mode: per_side` → `side_effects: {side_id: {cash_delta: N}}`. `uniform_cash_delta` 넣지 말 것.
- `cash_delta` 는 [0,1] 정규화 자원. 일반 이벤트 ±0.01~0.05, 극단 black swan 도 ±0.08 이하.
- 상호 배타 이벤트는 같은 `mutex_group` 으로 묶어 동시 발현 차단.
- 스키마 정의: `redcell/sim/rulebook.py::_generate_event_deck` 의 프롬프트 + `_fallback_event_deck`.

### 3) `competitor_strategies` — 경쟁사 초기 자세

각 경쟁사가 시뮬 시작 시 *어떤 전략을 들고 들어오는지*. LLM 이 환경 + 구조적 우위로부터 추론하지만, 사용자가 이미 알면 직접 박는 게 정확.

```yaml
competitor_strategies:
  side_b: |
    Samsung HBM4 12-Hi 양산 일정 가속화 + NVIDIA Blackwell 디자인 인-에 재진입.
    중국 향 수출규제 강화에 대응해 미국 텍사스 어드밴스드 패키징 캐파 확대.
  side_c: |
    Micron — HBM3E 12-Hi 양산 본격화, NVIDIA 보조 supplier 포지션 강화.
    HBM4 단계에서는 design-in 전쟁 회피 + 수익성 우선.
```

비워두면 LLM 이 환경 + sides[].structural_advantages 로부터 생성. 일부만 채워도 됨 — 비운 경쟁사는 LLM 이 채움 (`load_or_generate_run_inputs` 의 cache 분기와 동등).

### 4) (보조) `_interview.rulebook_hints` — partial override

전체 rulebook 대신 *시장 특성만* 힌트로 주고 싶을 때 (LLM 이 rules 는 만들되 사용자가 알려준 anchor 를 존중):

```yaml
_interview:
  rulebook_hints:
    price_war_share_swing: 8pp        # 가격전 시 share 진폭
    innovation_cycle_months: 12
    regulation_impact: high
    switching_cost: high
    winner_take_all: low
```

이건 LLM 을 끄지 않습니다 — 가이드만 줍니다.

## 검증 루프

override 가 진짜 먹히는지 확인:

```bash
redcell run config.yaml -o brief.md
# 로그에서 다음 줄 확인:
#   [  0.0%] Rulebook: using user override (scenario.rulebook)
# 안 보이면 override 가 안 잡힌 것. scenario.yaml top-level 인지 확인.
```

캐시는 `.redcell_cache_*/` 에 저장됩니다 — override 를 바꾸면 scenario hash 가 변해서 자동으로 새 캐시. 캐시를 강제로 비우려면 디렉토리 삭제.

## Module map — 어디를 만질지

| 파일 | 무엇이 들어있나 | 자주 손대는가 |
|---|---|---|
| `redcell/sim/simulation_setup.py` | 캐시 / LLM 생성 / **user override** 분기 | override hook 확장 시 |
| `redcell/sim/rulebook.py` | rulebook + event_deck LLM 생성 + fallback | 스키마 reference |
| `redcell/sim/strategic_setup.py` | competitor_strategies LLM 생성 | 경쟁사 추론 로직 |
| `redcell/sim/deliberation_v2.py` | C-suite 3-phase 토론, reassess | 토론 프롬프트 수정 |
| `redcell/sim/event_tree.py` | per-turn 진행 + per-side reassess 호출부 | 턴 흐름 수정 |
| `redcell/sim/adjudicator.py` | 3-expert panel + synthesis | adjudication 기준 |
| `redcell/llm.py` | provider 어댑터 (sglang/DashScope/OpenAI) | provider 추가 시 |
| `redcell/engine.py` | `run_linear_scenario` — 시나리오 환경 주입 | 안 만짐 |
| `redcell/pipeline.py` | run + render 오케스트레이션 | 출력 흐름 수정 |
| `redcell/render.py` | brief / trace 마크다운 렌더링 | 출력 포맷 변경 |

## 안 만져도 되는 것

- `redcell/sim/state.py` — `TreeNode` / position tier / share 정규화. 내부 자료구조.
- `redcell/sim/cash.py` — cash identity (`starting + action_cost + events_delta + position_revenue = ending`). 이 식이 깨지면 brief 의 cash_attribution 이 거짓말함.
- `redcell/sim/sim_utils.py` — `scenario_hash`, `paths_hash`, 캐시 I/O.

## Custom 추가 시 원칙

- **LLM 생성을 끄는 override 는 항상 *top-level scenario 키*** — `_interview` 같은 nested 가 아니라. 위 4 가지가 그 자리에 있는 이유.
- **schema 는 LLM 생성기의 fallback 함수가 reference** — `_generate_*` 의 success 경로가 LLM 출력 검증에 의존하므로 정확한 shape 은 fallback 쪽이 더 안전.
- **silent fallback 금지** — LLM 생성이 실패하면 *raise*, fallback 으로 도망가지 마세요. (이 코드베이스는 과거 silent fallback 때문에 디버깅 지옥을 겪었습니다 — `feedback_no_workaround` 메모리 참조.)
- **probe-first** — override 스키마 바꾸기 전에 `scripts/probe_*.py` 패턴으로 LLM 실제 응답을 관측. 코드부터 쓰지 마세요.

## Quick sanity check

```python
# Python REPL 에서:
import yaml
s = yaml.safe_load(open("scenarios/your_scenario.yaml"))
print("rulebook override:", bool(s.get("rulebook")))
print("event_deck override:", bool(s.get("event_deck")))
print("competitor_strategies override:", bool(s.get("competitor_strategies")))
```

세 줄 모두 `True` 면 LLM 은 환경 주입 + C-suite 토론 + adjudication 만 담당, 나머지는 사용자 데이터.
