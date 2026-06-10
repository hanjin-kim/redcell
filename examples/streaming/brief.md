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
| **Coupang Play** | 65.0% | 64.4% | -0.6pp | `dominant` |
| Netflix Korea | 80.0% | 89.2% | +9.2pp | `dominant` |
| Tving | 50.0% | 28.2% | -21.8pp | `weak` |

## 2. 턴별 전개

### Turn 1  ([C-suite 토론 상세 →](brief_trace.md#turn-1))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Ecosystem Bundle Push`@0.80 | `strong` ↗ | 67.7% |
| Netflix Korea | `Global Hit Investment`@0.80 | `dominant` ↑ | 78.0% |
| Tving | `Live Sports Integration`@0.85 | `contested` ↘ | 42.3% |

**Adjudicator narrative:** 쿠팡플레이는 로켓 WOW 멤버십 연동을 통해 기존 OTT 시장의 전환 비용 구조를 재편하며 저비용으로 사용자 기반을 빠르게 확장했습니다.与此同时, 넷플릭스는 풍부한 현금 여유와 글로벌 히트 콘텐츠를 무기로 가격 인상에도 불구하고 시장 지배력을 공고히 하며 전체 시장을 견인하는 지위를 유지했습니다. 반면 티빙은 KBO 리그 등 지역 특화 전략을 펼쳤으나, Wavve 합병으로 인한 자금 부담과 낮은 현금 보유량이 누적되어 경쟁 지속성에 심각한 불안요인이 발생했습니다. 이로 인해 쿠팡플레이와 넷플릭스의 양강 구도가 더욱 강화되는 반면, 티빙은 생존을 위협받는 contested 상태로 밀려나고 있습니다.

**경쟁 상호작용 분석:** 쿠팡플레이의 이커머스 연계 모델은 기존 OTT 규제 프레임워크를 우회하며 시장 진입 장벽을 낮추는 반면, 넷플릭스의 강력한 자본력은 이러한 새로운 경쟁 구도에서도 시장 지배력을 유지하는 방어막 역할을 합니다. 티빙은 생방송 콘텐츠로 차별화를 꾀했으나, 합병 비용과 현금 부족이라는 구조적 약점으로 인해 쿠팡플레이의 확장 속도와 넷플릭스의 가격 경쟁력 앞에서 고전하고 있습니다.

### Turn 2  ([C-suite 토론 상세 →](brief_trace.md#turn-2))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Global Hit Investment`@0.90 | `dominant` ↑ | 65.7% |
| Netflix Korea | `Premium Original Production`@0.75 | `dominant` ↑ | 76.0% |
| Tving | `CJ ENM Content Leverage`@0.85 | `weak` ↓ | 40.6% |

**Adjudicator narrative:** T1에서 Coupang Play가 구축한 Rocket WOW 기반의 사용자 층은 이번 턴에 콘텐츠 투자 효과를 극대화하며 시장 지배력을 확립하는 계기가 되었습니다. 반면 Netflix Korea는 T1부터 유지해 온 높은 현금 흐름을 바탕으로 광고 계층 최적화를 병행하며 선두 위치를 더욱 공고히 했습니다. Tving은 T1의 Live Sports Integration 전략이 계절성 자산 의존도를 높이는 부작용을 낳아, 양대 강자의 동시 공격에 구조적 취약점이 노출되었습니다. 이로 인해 T1 이후 누적된 자본 효율성 격차가 이번 턴에 결정적인 승패를 가르는 요인으로 작용했습니다.

**경쟁 상호작용 분석:** Coupang Play의 이커머스 결합 판매 전략과 Netflix Korea의 광고 인센티브 강화가 동시에 작용하며 시장 양극화를 가속화했습니다. Tving은 이러한 양대 강자의 공격적 자원 투입과 규제 리스크 관리 격차로 인해 상대적으로 고립된 위치로 밀려났습니다.

### Turn 3  ([C-suite 토론 상세 →](brief_trace.md#turn-3))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Ecosystem Bundle Push`@0.80 | `dominant` ↗ | 71.4% |
| Netflix Korea | `Premium Original Production`@0.80 | `dominant` → | 74.0% |
| Tving | `Global Hit Investment`@0.80 | `contested` ↗ | 32.6% |

**Adjudicator narrative:** Coupang Play 는 T1 의 생태계 번들 전략과 T2 의 글로벌 히트 투자를 바탕으로 Rocket WOW 와의 결합을 심화시켜 전환율과 락인을 가속화했습니다. Netflix Korea 는 T2 의 프리미엄 오리지널 생산과 광고 tiers 전환을 통해 가격 인상 충격을 흡수하며 현금 흐름을 안정화시켰으나, 국내 라이브 스포츠 부재는 Tving 이 점유하는 틈새시장을 방치했습니다. Tving 은 T1 의 라이브 스포츠 통합과 T2 의 CJ ENM 콘텐츠 활용으로 국소적 충성도를 회복하며 격차를 좁혔지만, 낮은 현금 보유량이 자본 적정성 우려를 해소하지 못해 구조적 취약성이 고착화되었습니다.

**경쟁 상호작용 분석:** Coupang Play 의 이커머스 생태계 결합 전략은 사용자의 이탈을 원천 차단하며 Netflix 의 콘텐츠 우위를 상쇄하는 효과를 낳았습니다. 반면 Tving 은 라이브 스포츠와 자사 콘텐츠로 틈새시장을 공략했으나, 낮은 현금 비율이 글로벌 투자와 자본 효율성 측면에서 경쟁력을 제한했습니다.

### Turn 4  ([C-suite 토론 상세 →](brief_trace.md#turn-4))

**Events fired:** OTT 과다 보조금 규제 강화, 넷플릭스 글로벌 히트작의 한국 내 폭발적 인기

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Global Hit Investment`@0.80 | `dominant` ↗ | 62.4% |
| Netflix Korea | `Ad-Tier Optimization`@0.75 | `dominant` ↑ | 87.2% |
| Tving | `CJ ENM Content Leverage`@0.90 | `weak` ↓ | 25.8% |

**Adjudicator narrative:** Coupang Play 는 T1 과 T3 의 생태계 번들 전략이 T4 에 MLB Korea 독점권 확보와 결합하며 규제 리스크를 상쇄하는 강력한 락인 효과를 만들어냈습니다. 반면 Netflix Korea 는 T2 와 T3 의 프리미엄 오리지널 투자와 글로벌 히트작 전략이 누적되어 현금 흐름과 마케팅 시너지를 극대화하며 점유율을 계속 끌어올리고 있습니다. Tving 은 T1 의 스포츠 통합과 T3 의 글로벌 히트 투자에도 불구하고 T2 의 합병 비용과 현금 고갈이 누적되어 콘텐츠 투자 주기를 감당하지 못해 급격히 약화되었습니다. 이로 인해 시장 양극화가 심화되며 Tving 은 생존을 위한 자금 조달 압박에 직면하게 되었습니다.

**경쟁 상호작용 분석:** Coupang Play 와 Netflix Korea 는 각각 생태계 락인과 글로벌 콘텐츠 우위를 통해 시장 양극화를 심화시키며, Tving 은 현금 부족과 규제 리스크로 인해 양쪽의 공세에 밀려 위축된 포지셔닝을 벗어나지 못하고 있습니다. 특히 Tving 의 현금 고갈은 이전 턴들의 투자 집중도가 누적된 결과로, 현재 콘텐츠 생산력 유지조차 어려운 상황으로 이어졌습니다.

### Turn 5  ([C-suite 토론 상세 →](brief_trace.md#turn-5))

**Events fired:** 초개인화 AI 추천 알고리즘 상용화

| 측 | Action | Position | Cash |
|---|---|---|---|
| **Coupang Play** | `Ecosystem Bundle Push`@0.80 | `dominant` ↗ | 64.4% |
| Netflix Korea | `Global Investment Scaling`@0.80 | `dominant` ↑ | 89.2% |
| Tving | `Ad-Tier Optimization`@0.85 | `weak` → | 28.2% |

**Adjudicator narrative:** 쿠팡플레이는 T2와 T4의 글로벌 히트 투자와 T3의 생태계 번들 전략이 누적되어 로켓와우捆绑 효과를 극대화하며 시장 지배력을 강화했습니다. 넷플릭스는 T2와 T3의 프리미엄 오리지널 제작과 T4의 광고 tiers 최적화로 현금 흐름을 극대화, 규제 강화와 경쟁 심화 속에서도 리더십을 유지했습니다. 틱빙은 T2와 T4의 CJ ENM 콘텐츠 활용이 자본 부족으로 인해 공격적 성장으로 이어지지 못해, 쿠팡플레이의 포괄적 제휴 공격에 밀려 위축 추이를 멈추지 못했습니다. 결과적으로 자본과 기술红利를 가진 양강 구도에서 틱빙의 고립화 구조가 더욱 뚜렷해졌습니다.

**경쟁 상호작용 분석:** 쿠팡플레이의 로켓와우捆绑과 스포츠 라이선스 확장이 틱빙의 내수 자산인 CJ ENM 콘텐츠와 KBO 중계권을 상대적으로 약화시키는 구조적 압력으로 작용했습니다. 반면 넷플릭스는 막대한 현금과 글로벌 히트작을 바탕으로 쿠팡플레이의 규제 리스크와 틱빙의 자본 부족이라는 시장 격차를 이용해 우위를 더욱 공고히 했습니다.

## 3. 우리 측 현금 동인

매 턴 cash identity: `starting + action_cost + events_delta + position_revenue = ending`

| Turn | Start | Action | Events | Position rev | End |
|------|-------|--------|--------|--------------|-----|
| T1 | 65.0% | -4.3pp | +0.0pp | +7.0pp | 67.7% |
| T2 | 67.7% | -12.0pp | +0.0pp | +10.0pp | 65.7% |
| T3 | 65.7% | -4.3pp | +0.0pp | +10.0pp | 71.4% |
| T4 | 71.4% | -12.0pp | -7.0pp | +10.0pp | 62.4% |
| T5 | 62.4% | -12.0pp | +4.0pp | +10.0pp | 64.4% |
