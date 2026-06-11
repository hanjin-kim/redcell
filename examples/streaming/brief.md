# Red Team Brief

이 전략을 주어진 환경에서 수행할 때, 우리 측과 경쟁사가 어떻게 반응하고 어떤 risk가 emerging 되는지 트레이싱한 결과입니다.

**산업:** `streaming_korea_ott`

**우리 회사:** Coupang Play  ·  **경쟁사:** Netflix Korea, Tving

**검증 대상 전략:**
> Sports + 멤버십 끼워팔기 fortress 강화:
- 로켓와우 멤버십 (4,990원/월) 가격 동결 — 사실상 무료 OTT 사용자 850만 → 1000만
- MLB 중계권 재계약 (2026-2030) + EPL 한국 독점 협상 마무리
- 오리지널 콘텐츠 투자 연 1500억 → 2500억 확대 (한국 한정)
- 광고 inventory 활성화 — 850만 사용자 베이스 광고주 영업 가속
- e-commerce LTV 향상과 OTT 사용자 데이터 통합 — 추천 광고 ARPU 증가
24개월 KPI: MAU 850 → 1100만, 광고 매출 +200%, 멤버십 churn -30%.

**주어진 환경:**
> Netflix가 2026 Q1부터 한국 베이직(광고 포함) 5,500 → 7,900원, 스탠더드 13,500 →
17,000원 가격 인상 발표 + 한국 오리지널 콘텐츠 투자 연 7000억 → 1조원 확대.
오징어게임 시즌 3 (2026 H2 출시) global hit 예상으로 Netflix Korea 가입자 stickness
급격히 강화 시그널. Tving은 KBO 야구 시즌 (3-10월) 사용자 spike + Naver Plus 통합
마케팅 확대.

## 1. 시뮬레이션 결과 요약

각 측의 시작 → 종료 변동:

| 측 | 초기 cash | T-final cash | Δ cash | T-final position |
|---|---|---|---|---|
| **Coupang Play** | 65.0% | 47.9% | -17.1pp | `dominant` |
| Netflix Korea | 80.0% | 66.0% | -14.0pp | `dominant` |
| Tving | 50.0% | 0.0% | -50.0pp | `weak` |

## 2. 턴별 전개

### Turn 1  ([C-suite 토론 상세 →](brief_trace.md#turn-1))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Live Sports Exclusive`@0.85 | `strong` ↑ | 60.0% |
| Netflix Korea | `Ad-Tier Optimization`@0.70 | `dominant` ↗ | 80.3% |
| Tving | `KBO Season Spike`@0.85 | `contested` ↘ | 44.0% |

**Adjudicator narrative:** Coupang Play 는 Rocket WOW 멤버십과의 결합을 통해 기존 이커머스 사용자 기반을 OTT 구독으로 전환시키며 시장 점유율을 빠르게 높이고 있습니다. 반면 Netflix Korea 는 글로벌 자본력을 바탕으로 고품질 콘텐츠를 지속적으로 투자하며 가격 민감 계층을 제외한 충성도 높은 사용자층을 유지하고 있습니다. Tving 은 KBO 시즌을 활용한 단기 트래픽 증가에 성공했으나, 낮은 현금 보유량과 계절성 의존도가 누적되어 장기적인 성장 동력이 약화되는 양상을 보이고 있습니다.

**경쟁 상호작용 분석:** Coupang Play 의 이커머스 결합 모델이 시장 진입 장벽을 높이는 반면, Netflix Korea 는 자본 우위로 이를 견제하며 시장을 주도하고 있습니다. Tving 은 특정 시즌의 트래픽 급증으로 일시적 점유율을 얻었으나, 지속적인 현금 소모와 계절성 의존도가 경쟁력을 약화시키는 요인으로 작용하고 있습니다.

### Turn 2  ([C-suite 토론 상세 →](brief_trace.md#turn-2))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Rocket Wow Integration`@0.85 | `dominant` ↑ | 58.0% |
| Netflix Korea | `Ad-Tier Optimization`@0.80 | `dominant` ↗ | 78.3% |
| Tving | `Cultural IP Dominance`@0.80 | `contested` ↘ | 37.7% |

**Adjudicator narrative:** Coupang Play 는 T1 에서 시작한 라이브 스포츠 독점 전략을 로켓와우 멤버십과 결합하며 시장 진입 장벽을 사실상 완성했습니다. Netflix Korea 는 T1 의 광고 tiers 최적화 성과를 바탕으로 현금 보유량을 활용해 점유율 방어와 성장을 동시에 추구하고 있습니다. 반면 Tving 은 T1 의 KBO 시즌 상승세를 일시적 반등으로만 활용했을 뿐, 와브 통합 비용과 자금 부족으로 인해 격차가 벌어지고 있습니다. 결과적으로 커머스 기반의 락인 효과와 글로벌 자본력의 차이가 시장 구조를 재편하며 Tving 은 생존을 위한 추가 자금이 절실한 상황입니다.

**경쟁 상호작용 분석:** 로켓와우의 락인 효과로 인해 Tving은 순수 콘텐츠 경쟁사로서 마케팅 여력이 극도로 축소된 반면, Netflix 는 글로벌 인프라를 활용해 가격 변동성을 흡수하며 방어에 집중하고 있습니다. 이로 인해 시장 양극화가 심화되어 Tving 의 자본 효율성 저하가 규제 리스크와 맞물려 약세 국면으로 진입했습니다.

### Turn 3  ([C-suite 토론 상세 →](brief_trace.md#turn-3))

**Events fired:** 제작비 인플레이션 급등, 구독 피로도 및 이탈 대량 발생

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Rocket Wow Integration`@0.80 | `dominant` ↑ | 56.9% |
| Netflix Korea | `Original Library Expansion`@0.85 | `dominant` ↗ | 68.3% |
| Tving | `Wavve Integration Cost Cut`@0.80 | `weak` ↓ | 25.8% |

**Adjudicator narrative:** Coupang Play 는 T1 의 라이브 스포츠 독점과 T2 의 Rocket Wow 통합을 통해 물류 및 데이터 인프라를 구독 유지의 핵심 자산으로 전환하며, 규제 리스크에도 불구하고 시장 지배력을 공고히 했습니다. Netflix Korea 는 T1 과 T2 의 Ad-Tier 최적화로 안정적인 현금 흐름을 확보한 뒤, 글로벌 인프라를 활용해 제작비 인플레이션을 관리하며 콘텐츠 경쟁력을 확장했습니다. 반면 Tving 은 T1 의 KBO 시즌과 T2 의 문화 IP 우위를 바탕으로 유입을 늘렸으나, Wavve 통합 후에도 현금 소진과 낮은 자본 효율성으로 인해 외부 자본 의존도가 높아지며 시장 주도권을 잃었습니다.

**경쟁 상호작용 분석:** Coupang Play 의 생태계 연동 전략과 Netflix 의 글로벌 인프라 활용이 시장 양극화를 심화시키며, Tving 은 자본 효율성 부족으로 인해 양측의 압력 사이에서 고립되었습니다. 특히 Coupang Play 의 Rocket Wow 통합이 규제 감시 대상이 되면서 시장 진입 장벽이 높아진 반면, Tving 은 내부 구조 조정 실패로 인해 이러한 장벽을 넘지 못했습니다.

### Turn 4  ([C-suite 토론 상세 →](brief_trace.md#turn-4))

**Events fired:** OTT 콘텐츠 과세안 도입 논의, 글로벌 OTT 플랫폼 통합 가속화

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Rocket Wow Integration`@0.80 | `dominant` ↗ | 50.9% |
| Netflix Korea | `Original Library Expansion`@0.80 | `dominant` ↗ | 62.6% |
| Tving | `Premium Content Acquisition`@0.80 | `weak` ↓ | 7.8% |

**Adjudicator narrative:** T1부터 T3까지 지속된 제작비 인플레이션과 구독 피로도는 모든 플랫폼에 부정적 영향을 미쳤으나, Coupang Play는 T2와 T3의 로켓와우 통합을 통해 콘텐츠 단점을 상쇄하며 시장 선점 우위를 더욱 견고하게 다졌습니다. 반면 Netflix Korea는 T3의 오리지널 라이브러리 확장으로 글로벌 아카이브와 프리미엄 광고 인프라를 결합하여 가격 민감도를 관리하며 지배적 지위를 유지했습니다. Tving은 T1의 KBO 시즌과 T2의 문화적 IP 공세에도 불구하고 T3의 비용 절감 노력이 늦게 시작되어 현금 고갈 속도가 빨라졌고, 이로 인해 구조적 생존 위험이 극대화되었습니다.

**경쟁 상호작용 분석:** Coupang Play와 Netflix Korea는 각각 로켓와우 통합과 글로벌 자본력을 바탕으로 규제 환경 변화에도 불구하고 시장 지배력을 강화하는 반면, Tving은 고비용 콘텐츠 확보 전략이 현금 고갈을 가속화하며 경쟁사들과의 격차가 벌어지고 있습니다. 특히 제작비 인플레이션과 구독 이탈이라는 공통된 외부 충격 앞에서 자본력과 생태계 결합도가 높은 두 강자는 방어선을 유지하는 반면, 자본이 약한 Tving은 구조적 악순환에 빠지게 되었습니다.

### Turn 5  ([C-suite 토론 상세 →](brief_trace.md#turn-5))

**Events fired:** 한국 드라마 글로벌 바이럴 현상, 주요 IP 저작권 분쟁 발생

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Rocket Wow Integration`@0.90 | `dominant` ↑ | 47.9% |
| Netflix Korea | `Ad-Tier Optimization`@0.80 | `dominant` ↗ | 66.0% |
| Tving | `Wavve Integration Cost Cut`@0.80 | `weak` ↓ | 0.0% |

**Adjudicator narrative:** 쿠팡플레이는 T2부터 T4까지 지속된 로켓와우 통합과 MLB 독점 전략이 T5에 이르러 생태계 잠금 효과를 극대화하며 시장 지배력을 강화했습니다. 넷플릭스는 T2와 T3의 광고 tiers 최적화와 콘텐츠 확장으로 안정적인 현금 흐름을 유지하며 우위를 지키고 있으나, 쿠팡플레이의 성장세에 밀려 격차가 좁혀지고 있습니다. 티빙은 T3와 T4의 비용 절감 및 콘텐츠 확보 시도가 현금 소진 속도를 늦추지 못해 구조적 위기가 심화되어 생존 자체가 위협받는 상황입니다.

**경쟁 상호작용 분석:** 쿠팡플레이의 생태계 통합과 넷플릭스의 수익성 개선 전략이 양강 체제를 형성하며 시장을 양분하고 있습니다. 반면 티빙의 현금 고갈은 콘텐츠 투자 위축으로 이어져 경쟁사들과의 격차가 더욱 벌어지고 있습니다.

## 3. 우리 측 현금 동인

매 턴 cash identity: `starting + action_cost + events_delta + position_revenue = ending`

| Turn | Start | Action | Events | Position rev | End |
|------|-------|--------|--------|--------------|-----|
| T1 | 65.0% | -12.0pp | +0.0pp | +7.0pp | 60.0% |
| T2 | 60.0% | -12.0pp | +0.0pp | +10.0pp | 58.0% |
| T3 | 58.0% | -6.1pp | -5.0pp | +10.0pp | 56.9% |
| T4 | 56.9% | -12.0pp | -4.0pp | +10.0pp | 50.9% |
| T5 | 50.9% | -12.0pp | -1.0pp | +10.0pp | 47.9% |
