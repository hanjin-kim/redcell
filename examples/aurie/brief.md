# Red Team Brief

이 전략을 주어진 환경에서 수행할 때, 우리 측과 경쟁사가 어떻게 반응하고 어떤 risk가 emerging 되는지 트레이싱한 결과입니다.

**산업:** `kbeauty_premium_skincare`

**우리 회사:** AURIE  ·  **경쟁사:** Shiseido, Amore Pacific

**검증 대상 전략:**
> 프리미엄-아시아 듀얼 트랙: 고가 anti-aging SKU 집중 + 일본 직영 채널 50개
신설 + 동남아 멀티브랜드 확장 + 중국 의존도 35→20% 축소.
R&D 매출 비중 7%→12% 증가, 면세 30%→15% 축소, D2C 자체몰 25% 비중 확보.
24개월 KPI: EBIT 마진 12→15%, 일본 매출 비중 8→18%, 중국 매출 35→20%.

**주어진 환경:**
> Shiseido가 2025 Q4에 발표한 한국 mass-premium 30% 가격 인하를 2026 Q1부터
실제 집행 — Olive Young / Lotte 면세 / 백화점 동시 적용, AURIE 핵심
anti-aging SKU 가격대(₩80-150K)에 직접 침투. 동남아 (베트남/태국) 시장에서도
Shiseido 채널 확장과 동시 진행.

## 1. 시뮬레이션 결과 요약

각 측의 시작 → 종료 변동:

| 측 | 초기 cash | T-final cash | Δ cash | T-final position |
|---|---|---|---|---|
| **AURIE** | 55.0% | 31.6% | -23.4pp | `weak` |
| Shiseido | 75.0% | 93.1% | +18.1pp | `dominant` |
| Amore Pacific | 62.0% | 64.9% | +2.9pp | `strong` |

## 2. 턴별 전개

### Turn 1  ([C-suite 토론 상세 →](brief_trace.md#turn-1))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Clinical Data Marketing`@0.90 | `contested` ↘ | 48.0% |
| Shiseido | `Aggressive Price Cut`@0.80 | `dominant` ↑ | 76.6% |
| Amore Pacific | `Sulwhasoo Premium Push`@0.70 | `strong` → | 62.7% |

**Adjudicator narrative:** AURIE는 일본 직영 매장 확장과 임상 마케팅을 동시에 진행하며 현금 소모를 집중시켰으나, 이는 단기 마진 압박을 구조화시키는 결과를 낳았습니다. Shiseido는 이러한 AURIE의 취약점을 포착해 풍부한 현금력을 바탕으로 가격 공세와 채널 확장을 병행하며 시장 주도권을 선점했습니다. Amore Pacific은 규제 리스크를 선제적으로 관리하며 프리미엄 포지셔닝을 방어했으나, 중국 시장의 정체로 인해 공격적인 성장 모멘텀을 확보하지는 못했습니다.

**경쟁 상호작용 분석:** Shiseido의 공격적인 가격 공세는 AURIE의 과도한 Capex 투자로 인해 약해진 현금 유동성을 직접적으로 타격하여 시장 점유율 방어 능력을 약화시켰습니다. 반면 Amore Pacific은 규제 준수와 브랜드 방어 전략으로 외부 충격을 흡수하며 안정적인 위치를 유지하고 있습니다.

### Turn 2  ([C-suite 토론 상세 →](brief_trace.md#turn-2))

**Events fired:** 환율 변동성 급증

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Japan Market Entry Blitz`@0.90 | `weak` ↓ | 41.0% |
| Shiseido | `Clinical Data Marketing`@0.80 | `dominant` ↑ | 72.6% |
| Amore Pacific | `Sulwhasoo Premium Push`@0.75 | `strong` ↗ | 64.0% |

**Adjudicator narrative:** AURIE는 T1부터 이어진 일본 직영 점포 확충 전략으로 인해 현금 소진이 가속화되어 시세이도의 가격 공세에 취약한 위치로 밀려났습니다. Shiseido는 T1에서 확보한 압도적인 현금 보유력을 바탕으로 가격 전술을 지속하며 시장 점유율을 방어하고 주도권을 더욱 공고히 했습니다. Amore Pacific은 핵심 프리미엄 브랜드 포트폴리오를 방어하며 외부 충격에 유연하게 대응해 기존 지위를 유지했습니다. 결과적으로 AURIE의 자원 고갈과 Shiseido의 자본 우위가 시장 지위 격차를 결정적으로 벌려놓았습니다.

**경쟁 상호작용 분석:** Shiseido의 압도적인 현금 보유력은 AURIE의 공격적 Capex 전략을 상쇄하며 시장 지배력을 강화했습니다. 반면 Amore Pacific은 가격 조정 의무를 피하는 전략으로 거시적 충격에 탄력적으로 대응하며 중립적 위치를 고수했습니다.

### Turn 3  ([C-suite 토론 상세 →](brief_trace.md#turn-3))

**Events fired:** —

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Clinical Data Marketing`@0.80 | `weak` ↗ | 36.2% |
| Shiseido | `Clinical Data Marketing`@0.80 | `dominant` ↗ | 80.3% |
| Amore Pacific | `Sulwhasoo Premium Push`@0.85 | `strong` ↗ | 63.9% |

**Adjudicator narrative:** AURIE는 T1과 T2에 걸쳐 일본 시장 진입과 임상 데이터 마케팅을 병행하며 현금 소모를 감수했으나, T2의 환율 급변동으로 인해 현금 보유율이 41%로 하락하며 재무 압박이 가중되었습니다. Shiseido는 T1과 T2에 걸쳐 가격 인하와 임상 데이터 마케팅을 연속으로 실행하며 풍부한 현금(73%)을 바탕으로 환율 리스크를 방어하고 시장 지배력을 확장했습니다. Amore Pacific은 T1과 T2에 걸쳐 Sulwhasoo 프리미엄 전략을 유지하며 임상 데이터를 공유함으로써 Shiseido의 침공을 막아내고 강세 추세를 이어갔습니다.

**경쟁 상호작용 분석:** 환율 변동성 급증이라는 공통의 외부 충격 속에서 Shiseido와 Amore Pacific은 각각 현금 풀과 프리미엄 포트폴리오를 활용해 선제적으로 대응하며 시장 주도권을 공고히 했습니다. 반면 AURIE는 자원을 절감하며 생존 기반을 다지려 했으나, Shiseido의 공격적인 가격 정책으로 인해 구조적 약세에서 벗어나지 못했습니다.

### Turn 4  ([C-suite 토론 상세 →](brief_trace.md#turn-4))

**Events fired:** 세파라 글로벌 프레스티지 채널 재편, J-뷰티 히스토리 부활 트렌드

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Cash Reserve Hedging`@0.80 | `weak` ↘ | 30.6% |
| Shiseido | `Clinical Data Marketing`@0.85 | `dominant` ↑ | 93.1% |
| Amore Pacific | `Whitening Tech Dominance`@0.90 | `strong` ↗ | 65.6% |

**Adjudicator narrative:** AURIE는 T1부터 T3까지 임상 데이터 마케팅과 일본 시장 진출을 병행하며 자산을 축적하려 했으나, 환율 변동성이라는 외부 충격과 Shiseido의 T1-T3 연속 가격 공세로 인해 현금 소모가 누적되었습니다. 특히 T2와 T3에서 Shiseido가 강화한 임상 마케팅과 가격 전략은 AURIE의 방어적 자산 배분을 무력화시키며, T4 현재 AURIE는 공격적 성장 기회를 상실한 채 생존을 위한 비용 절감 모드로 고착되었습니다. 반면 Amore Pacific은 T1-T3 동안 일관되게 유지한 Sulwhasoo 프리미엄 전략과 임상 데이터 투자를 통해 Shiseido의 가격 공세에도 불구하고 프리미엄 시장에서의 입지를 더욱 견고히 했습니다. 결과적으로 Shiseido는 현금 파워와 헤리티지를 결합해 시장 지배력을 극대화한 반면, AURIE는 자금 부족과 채널 장벽으로 인해 시장 분열 구조에서 소외되는 결과를 맞이했습니다.

**경쟁 상호작용 분석:** Shiseido의 T1-T3 연속된 가격 공세와 임상 마케팅은 AURIE의 자원을 고갈시키며 시장 진입 장벽을 높이는 효과를 낳았습니다. 반면 Amore Pacific은 가격 경쟁에 휘말리지 않고 임상 데이터 기반의 프리미엄 전략을 유지하며 Shiseido의 공격을 우회하는 데 성공했습니다. 이로 인해 AURIE는 현금 부족과 채널 제약으로 인해 방어적 태세만 유지할 수밖에 없는 구조적 약세에 빠졌습니다.

### Turn 5  ([C-suite 토론 상세 →](brief_trace.md#turn-5))

**Events fired:** 글로벌 안티에이징 원료 수급 위기, 올리브영 해외 진출 가속

| 측 | Action | Position | Cash |
|---|---|---|---|
| **AURIE** | `Cash Reserve Hedging`@0.90 | `weak` ↘ | 31.6% |
| Shiseido | `Clinical Data Marketing`@0.85 | `dominant` ↑ | 93.1% |
| Amore Pacific | `Clinical Data Marketing`@0.80 | `strong` ↗ | 64.9% |

**Adjudicator narrative:** AURIE는 T2부터 T4까지 일본 시장 진출과 임상 마케팅에 집중하며 자산을 소진했으나, T4의 현금 방어 전략이 원자재 위기 속에서 오히려 시장 점유율 하락을 부추겼습니다. Shiseido는 T2-T4 동안 쌓아올린 막대한 현금과 임상 데이터를 바탕으로 가격 인하 카드를 통해 시장 충격까지 방어하며 지배적 지위를 확장했습니다. Amore Pacific은 T2-T4 동안 프리미엄 라인 판매와 whitening 기술 투자를 통해 마진을 보호했으나, 중국 시장의 침체가 신규 성장 동력을 제한하는 요인으로 작용했습니다.

**경쟁 상호작용 분석:** Shiseido의 공격적인 가격 공세와 현금 기반 헤징 전략은 AURIE의 현금 고갈을 가속화하며 시장 격차를 벌렸습니다. 반면 Amore Pacific은 자체 임상 센터와 프리미엄 포트폴리오로 원가 상승 리스크를 분산시키며 Shiseido의 공세에도 불구하고 견고한 입지를 유지했습니다.

## 3. 우리 측 현금 동인

매 턴 cash identity: `starting + action_cost + events_delta + position_revenue = ending`

| Turn | Start | Action | Events | Position rev | End |
|------|-------|--------|--------|--------------|-----|
| T1 | 55.0% | -12.0pp | +0.0pp | +5.0pp | 48.0% |
| T2 | 48.0% | -12.0pp | +2.0pp | +3.0pp | 41.0% |
| T3 | 41.0% | -7.8pp | +0.0pp | +3.0pp | 36.2% |
| T4 | 36.2% | -2.6pp | -6.0pp | +3.0pp | 30.6% |
| T5 | 30.6% | -3.0pp | +1.0pp | +3.0pp | 31.6% |
