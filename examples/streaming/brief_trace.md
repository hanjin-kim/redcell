# Deliberation Trace

각 턴의 C-suite 토론 (CEO/CFO/CTO/CMO/COO 제안 / 검토 / 종합) 과 adjudicator 패널 평가를 펼친 trace 입니다. 헤드라인 결과는 [브리프](.) 참조.

**산업:** `streaming_korea_ott`  ·  **우리 회사:** Coupang Play

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

<a id="turn-1"></a>
## Turn 1

**Events fired:** —

### **Coupang Play** (side_a)

- Final action: `Live Sports Exclusive`@0.85
- Position: `strong` ↑
- Cash: 60.0%
- Adjudicator rationale: Coupang Play 는 Rocket WOW 멤버십 통합과 스포츠 독점 전략을 통해 높은 전환 비용 장벽을 형성하며 시장 영향력을 빠르게 확대하고 있습니다.

##### Phase 1 — 독립 제안

- **CFO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Live Sports Exclusive`@0.20
  - rationale: CEO의 '가입자 수 우선' 편향과 로켓와우 통합 과신에 따라, 넷플릭스 가격 인상 공세 시기에 MAU 1000만 확보를 최우선으로 하여 생태계 내 구매 전환을 극대화하는 전략입니다. EPL 독점과 데이터 결합은 이커머스 LTV 향상이라는 캠페인 핵심 목표에 직접 부합하며, 현금 65% 수준에서도 MAU 기반의 광고 매출 확대가 가장 확실한 ROI 경로입니다.
  - risk: MAU 증대 시 단기 수익성 악화 및 콘텐츠 투자 효율성 저하 가능성
- **CMO**: `Rocket Wow Integration`@0.40, `Live Sports Exclusive`@0.35, `Data Monetization Boost`@0.25
  - rationale: 넷플릭스의 가격 인상과 오징어게임 시즌 3 출시로 인한 강성 경쟁 환경에서, 순수 콘텐츠 경쟁보다는 '스포츠 + 이커머스' 생태계 장벽을 높이는 것이 핵심 전략임. CEO의 쿠팡 출신 배경과 MAU 우선주의에 따라 로켓와우 통합을 최우선으로 배치하여 유입을 극대화하고, EPL 독점 권리로 경쟁사와 차별화된 라이브 트래픽을 확보함. 데이터 모네타이제이션은 기존 850만 사용자 베이스의 ARPU 증대를 통해 수익성을 보완하는 방어적 조치임.
  - risk: 콘텐츠 투자 확대에 따른 단기 적자 심화 및 로켓와우 통합 시 retail churn 리스크
- **CTO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Live Sports Exclusive`@0.20
  - rationale: CEO 의 쿠팡 출신 배경과 MAU 우선주의 (리더십 블라인드) 를 반영하여, 가격 인상을 회피하고 로켓와우 통합을 통한 유입을 최우선으로 설정함. 넷플릭스의 가격 인상과 오리지널 투자 확대에 대응하기 위해, 순수 OTT 경쟁보다는 이커머스 생태계 시너지를 극대화하는 'Commerce-First' 전략에 충실함. R&D(50%)를 유지하며 인프라 안정성을 담보하되, 공격적인 MAU 성장 narrative 에 자원을 집중함.
  - risk: MAU 수치에 집중하며 단기 적자 심화 및 콘텐츠 품질 저하 가능성
- **COO**: `Rocket Wow Integration`@0.45, `Live Sports Exclusive`@0.35, `Data Monetization Boost`@0.20
  - rationale: CEO의 쿠팡 출신 특성상 MAU 숫자와 이커머스 시너지를 최우선으로 여기는 경향 반영. 넷플릭스 가격 인상과 원작 강화에 대응해 '스포츠+멤버십'으로 유입된 트래픽을 즉각 전환시키되, 오리지널 제작비 확대보다는 기존 데이터와 스포츠 권리를 활용한 수익화 구조를 우선시함. CEO의 리더십 맹점인 'MAU 서브가치'와 '로켓와우 통합 과신'을 실행 전략에 명시적으로 반영.
  - risk: 동시 다발적 투자로 현금 소진 속도 가속화 (65% → 40% 예상) 및 콘텐츠 품질 저하 리스크
- **CEO**: `Live Sports Exclusive`@0.40, `Rocket Wow Integration`@0.35, `Data Monetization Boost`@0.25
  - rationale: 넷플릭스 가격 인상 대비 에코시스템 포지셔닝 강화. 로켓와우 가격 동결은 이커머스 KPI 연동과 장기 LTV 확보를 위한 필수 전략으로 판단.
  - risk: 콘텐츠 비용 증대로 단기 적자 확대 및 전환율 지연 리스크

##### Phase 2 — 비판적 검토 (다수안: `Rocket Wow Integration`, DA: `CFO`)

- **CTO**: `Live Sports Exclusive`@0.45, `Rocket Wow Integration`@0.30, `Data Monetization Boost`@0.25
- **CMO**: `Rocket Wow Integration`@0.45, `Live Sports Exclusive`@0.35, `Data Monetization Boost`@0.20
- **COO**: `Rocket Wow Integration`@0.65, `Data Monetization Boost`@0.25, `Live Sports Exclusive`@0.10
  - 변경됨 `Live Sports Exclusive` → 이유: 동시 다발 투자로 현금 소진 위험 감수
- **CEO**: `Live Sports Exclusive`@0.45, `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.10
  - 변경됨 `Rocket Wow Integration` → 이유: MAU 성장 우선순위 반영
- **CFO**: `Ad-Tier Optimization`@0.50, `Churn Prevention Campaign`@0.30, `Data Monetization Boost`@0.20
  - 이의 제기: 제안서에 포함된 Rocket Wow Integration 은 MAU 증대에 집중하여 수익성 훼손 가능성을 내포합니다. 확실한 투자 회수 경로 부재로 현재 현금 보유액 65% 위험 수준에서 추가 소진을 초래하며, 고객 단가와 충성도를 담보하지 않는 확장 전략은 재무 건전성에 직접적인 하자를 만듭니다. 비구조적인 유입 확장은 자본 감가상각으로 이어질 가능성이 높습니다. 현금 소모 속도 관리가 우선되어야 합니다. 현금 잔액 감소 리스크를 피하기 위해 단기 수익 구조 선점이 필요합니다. 대외 환경 변화 시 대응 능력을 잃지 않기 위한 것입니다. 단기 성과 추구보다는 수익 모델 검증이 더 중요합니다. 이는 기업 장기 존속을 위한 필수 조건입니다. 시장 점유율 증가가 곧 수익성 증가는 아닙니다. 특히 65% 현금 수준에서는 더욱 주의해야 합니다. 투자 후 회수 기간과 비용 효율성 분석이 선행되어야 합니다. 지금의 제안은 ROI 기반이 불투명합니다. 팀 전체의 합의가 있더라도 재무 원칙에는 저항이 필연적입니다.

**Position changes:**
- COO: Live Sports Exclusive → Rocket Wow Integration+Data Monetization Boost+Live Sports Exclusive (동시 다발 투자로 현금 소진 위험 감수)
- CEO: Rocket Wow Integration → Live Sports Exclusive+Rocket Wow Integration+Data Monetization Boost (MAU 성장 우선순위 반영)
- [반대] CFO: 제안서에 포함된 Rocket Wow Integration 은 MAU 증대에 집중하여 수익성 훼손 가능성을 내포합니다. 확실한 투자 회수 경로 부재로 현재 현금 보유액 65% 위험 수준에서 추가 소진을 초래하며, 고객 단가와 충성도를 담보하지 않는 확장 전략은 재무 건전성에 직접적인 하자를 만듭니다. 비구조적인 유입 확장은 자본 감가상각으로 이어질 가능성이 높습니다. 현금 소모 속도 관리가 우선되어야 합니다. 현금 잔액 감소 리스크를 피하기 위해 단기 수익 구조 선점이 필요합니다. 대외 환경 변화 시 대응 능력을 잃지 않기 위한 것입니다. 단기 성과 추구보다는 수익 모델 검증이 더 중요합니다. 이는 기업 장기 존속을 위한 필수 조건입니다. 시장 점유율 증가가 곧 수익성 증가는 아닙니다. 특히 65% 현금 수준에서는 더욱 주의해야 합니다. 투자 후 회수 기간과 비용 효율성 분석이 선행되어야 합니다. 지금의 제안은 ROI 기반이 불투명합니다. 팀 전체의 합의가 있더라도 재무 원칙에는 저항이 필연적입니다.

##### Phase 3 — CEO 종합

**Decision:** 스포츠 중계권 독점 확보 및 확장; 로켓와우 멤버십 구독권 자동 부여

**Reasoning:** 스포츠 포티리스 핵심, MAU 성장 우선; 이커머스 연동으로 유입 극대화 전략

### Netflix Korea (side_b)

- Final action: `Ad-Tier Optimization`@0.70
- Position: `dominant` ↗
- Cash: 80.3%
- Adjudicator rationale: Netflix Korea 는 압도적인 자본력과 글로벌 오리지널 콘텐츠 포트폴리오로 시장 지배력을 유지하며 가격 인상에도 충성도 높은 타겟을 확보하고 있습니다.

##### Phase 1 — 독립 제안

- **COO**: `Original Library Expansion`@0.50, `Ad-Tier Optimization`@0.30, `Global Hit Investment`@0.20
  - rationale: CEO 의 '한국 콘텐츠 1 조 투자 narrative'와 '글로벌 본사 metrics 우선'이라는 리더십 편향을 반영하여, 효율성보다 절대적 투자 규모를 우선시함. 강동한 CEO 의 mandate 에 따라 광고 tiers 를 통한 ARPU 방어와 오징어게임 시즌 3 히트 효과를 극대화하되, 동시에 과도한 동시 진행 리스크를 경고함.
  - risk: 과도한 콘텐츠 투자로 인한 현금 고갈 및 가격 민감층 이탈 가속화
- **CTO**: `Global Hit Investment`@0.45, `Original Library Expansion`@0.35, `Ad-Tier Optimization`@0.20
  - rationale: CEO 의 글로벌 ARPU 회복 mandate 에 따라 오징어게임 시즌 3 의 글로벌 히트 효과를 극대화하고, 프리미엄 구독층 유지와 동시에 광고 기반 베이직 요금 인상을 단행하기 위함입니다. 또한 가격 민감도가 높은 사용자의 이탈을 방어하기 위해 한국 오리지널 투자 확대가 필수적입니다. 리더십의 '글로벌 본사 가격 정책 추종'과 '한국 콘텐츠 1 조 투자 narrative 유지 압박'이라는 편향을 반영하여, 효율성보다는 절대적인 투자 규모와 글로벌 히트 의존 전략을 선택했습니다.
  - risk: 한국 시장 가격 민감 계층의 이탈 가속화 가능성
- **CFO**: `Original Library Expansion`@0.45, `Ad-Tier Optimization`@0.35, `Global Hit Investment`@0.20
  - rationale: CEO 의 '글로벌 ARPU 회복' mandate 와 '한국 오리지널 투자 확대'를 직접 실행합니다. 강동한 CEO 의 리더십 하에 효율성보다 규모 중심의 투자 (Original Library Expansion) 가 우선시되며, 이는 경쟁사 대비 가격 민감도 높은 사용자의 이탈을 방어하기 위한 필수 조치입니다. 동시에 오징어게임 시즌 3 의 히트 효과를 극대화하여 프리미엄 구독층을 유지하고, 광고 기반 베이직 요금 인상을 통해 ARPU 를 회복하려 합니다. 기존 캠페인 방향성을 따르되, 현금 보유량 80% 로 리스크 관리가 가능함을 전제로 공격적인 투자를 단행합니다.
  - risk: 가격 민감 계층의 이탈 가속화 가능성
- **CMO**: `Original Library Expansion`@0.50, `Ad-Tier Optimization`@0.30, `Global Hit Investment`@0.20
  - rationale: CEO 의 ARPU 회복 mandate 에 따라 광고 tiers 를 통한 수익 구조 다각화 (Ad-Tier Optimization) 와 가격 민감 계층 유입을 위한 한국 오리지널 확대 (Original Library Expansion) 를 병행합니다. 동시에 강동한 CEO 가 지향하는 글로벌 히트 효과 극대화를 위해 오징어게임 시즌 3 투자 (Global Hit Investment) 를 지속하되, 이는 리더십의 '한국 콘텐츠 1 조 투자 narrative 유지' 편향을 반영한 것입니다. 경쟁사 Coupang Play 와 Tving 이 견제 중인 상황에서 단순 가격 인하가 아닌 콘텐츠와 광고 모델로 방어선을 구축하여 점유율을 유지합니다.
  - risk: 가격 민감도 높은 사용자의 이탈 가속 및 본사 투자 규모 압박으로 인한 비효율 발생
- **CEO**: `Ad-Tier Optimization`@0.40, `Original Library Expansion`@0.40, `Churn Prevention Campaign`@0.20
  - rationale: 강동한 CEO mandate 에 따라 Netflix Korea 오징어게임 시즌 3 기반 ARPU 회복 추구. Coupang Play, Tving 대비 우위 확보 위해 광고 tiers 확대와 한국 오리지널 투자 병행.
  - risk: 가격 민감 계층 반발 및 단기 구독 수 감소

##### Phase 2 — 비판적 검토 (다수안: `Original Library Expansion`, DA: `CFO`)

- **CTO**: `Tech Infrastructure Upgrade`@0.50, `Original Library Expansion`@0.30, `Ad-Tier Optimization`@0.20
  - changed `Global Hit Investment` → because: R&D 투자 부족은 경쟁력 붕괴로 이어짐
- **COO**: `Ad-Tier Optimization`@0.45, `Original Library Expansion`@0.35, `Churn Prevention Campaign`@0.20
- **CMO**: `Original Library Expansion`@0.50, `Ad-Tier Optimization`@0.30, `Global Hit Investment`@0.20
- **CFO**: `Ad-Tier Optimization`@0.60, `Churn Prevention Campaign`@0.40
  - dissent: 오리지널 라이브러리 확장은 자본 지출이 즉시 현금 흐름으로 전환되지 않는 높은 고정비 구조를 띤다. 시장 성장세 둔화 시점에서 신규 콘텐츠는 구독자 유치 효과보다 유지 비용 부담이 더 클 수 있으며, 현금 소모 속도가 매출 창출 주기를 앞지를 경우 재무 건전성이 훼손될 가능성이 존재한다. 초기 자금 여력이 충분하더라도 장기적인 ROE 달성을 위해서는 투자 회수 기간 관리가 선행되어야 한다. 단기적인 현금 흐름 최적화가 기업 생존에 더 직접적인 기여를 할 수 있다. 재무적 손익 균형이 맞지 않는 대규모 콘텐츠 계약은 배분된 자원의 비효율성을 유발할 수 있어 반대한다. 현금 보존 전략이 최우선이 되어야 하는 시점이다. 고정 자산 의존도를 낮추고 유동성 확보에 집중해야 한다. 예측 불가능한 시장 변동성 속에서 레버리지 효과를 내기보다는 안정적 현금 창출 경로를 구축하는 것이 바람직하다. 투자 효율성 분석 없이 진행되는 콘텐츠 확보는 예상치 못한 감가상각을 초래할 위험이 크다. 따라서 본사
- **CEO**: `Global Hit Investment`@0.35, `Ad-Tier Optimization`@0.30, `Original Library Expansion`@0.35
  - changed `Churn Prevention Campaign` → because: 글로벌 ARPU 우선순위

**Position changes:**
- CTO: Global Hit Investment → Tech Infrastructure Upgrade+Original Library Expansion+Ad-Tier Optimization (R&D 투자 부족은 경쟁력 붕괴로 이어짐)
- [반대] CFO: 오리지널 라이브러리 확장은 자본 지출이 즉시 현금 흐름으로 전환되지 않는 높은 고정비 구조를 띤다. 시장 성장세 둔화 시점에서 신규 콘텐츠는 구독자 유치 효과보다 유지 비용 부담이 더 클 수 있으며, 현금 소모 속도가 매출 창출 주기를 앞지를 경우 재무 건전성이 훼손될 가능성이 존재한다. 초기 자금 여력이 충분하더라도 장기적인 ROE 달성을 위해서는 투자 회수 기간 관리가 선행되어야 한다. 단기적인 현금 흐름 최적화가 기업 생존에 더 직접적인 기여를 할 수 있다. 재무적 손익 균형이 맞지 않는 대규모 콘텐츠 계약은 배분된 자원의 비효율성을 유발할 수 있어 반대한다. 현금 보존 전략이 최우선이 되어야 하는 시점이다. 고정 자산 의존도를 낮추고 유동성 확보에 집중해야 한다. 예측 불가능한 시장 변동성 속에서 레버리지 효과를 내기보다는 안정적 현금 창출 경로를 구축하는 것이 바람직하다. 투자 효율성 분석 없이 진행되는 콘텐츠 확보는 예상치 못한 감가상각을 초래할 위험이 크다. 따라서 본사
- CEO: Churn Prevention Campaign → Global Hit Investment+Ad-Tier Optimization+Original Library Expansion (글로벌 ARPU 우선순위)

##### Phase 3 — CEO 종합

**Decision:** 광고 기반 요금 인상으로 ARPU 방어; 한국 오리지널 투자로 이탈 방지

**Reasoning:** 글로벌 본사 지표 우선주의 반영; 가격 민감 계층 리텐션 확보

### Tving (side_c)

- Final action: `KBO Season Spike`@0.85
- Position: `contested` ↘
- Cash: 44.0%
- Adjudicator rationale: Tving 은 KBO 시즌 등 계절성 트래픽에 의존하며 현금 유동성 부족과 Wavve 통합 비용 부담으로 장기적인 재무 건전성이 약화되고 있습니다.

##### Phase 1 — 독립 제안

- **CMO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Aggressive Price Cut`@0.20
  - rationale: CEO 의 보수적 Capex 와 CJ ENM/JTBC 자산 활용 경향을 반영하여, KBO 트래픽과 네이버 플러스를 결합한 저가 전략을 실행합니다. 이는 글로벌 부재를 '한국 시장 스티치'로 대체하는 리더십의 편향을 반영하며, 경쟁사 가격 인상 공백을 노린 공격적 점유율 확보입니다.
  - risk: Wavve 합병 비용 인식 거부로 인한 내부 저항 및 단기 마진 악화
- **CTO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Cultural IP Dominance`@0.20
  - rationale: CEO 의 보수적 Capex 관리와 CJ ENM/JTBC 자산 활용 경향을 반영하여 KBO 시즌과 네이버 플러스를 결합한 단기 점유율 선점을 우선시함. 리더십의 '한국 시장 stickiness' 편향에 따라 글로벌 투자나 기술 인프라 확충보다는 기존 자산과 정치적으로 사수된 KBO 중계권을 활용한 전략을 선택함.
  - risk: R&D 50% 유지로 장기 기술 격차 심화, 글로벌 경쟁력 약화
- **CFO**: `KBO Season Spike`@0.35, `Naver Plus Synergy`@0.35, `Wavve Integration Cost Cut`@0.30
  - rationale: CEO 의 '보수적 Capex 관리'와 'CJ ENM/JTBC 자산 활용' 경향에 부합하며, KBO 중계권 포기 시 정치적 비용이 커 사수하려는 모회사 정치 (blind spot) 를 반영해 야구 시즌을 최우선으로 활용함. 또한 글로벌 자산 부재를 인정하지 않고 '한국 시장 stickiness' 논리로 대체하여 네이버 플러스 통합과 기존 지상파 포트폴리오 강화를 통해 저가 세그먼트 선점을 도모함.
  - risk: KBO 시즌 효과 일시적이며, Wavve 통합 비용 매몰 인식 거부로 인해 단기 현금 소모 가속화 가능성 존재
- **COO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Cultural IP Dominance`@0.20
  - rationale: CEO의 보수적 Capex 관리와 CJ ENM/JTBC 자산 활용 경향을 반영하여, KBO 트래픽과 네이버 플러스 통합을 결합하되, 고가 정책 공백을 노린 저가 세그먼트 선점을 위해 JTBC/CJ ENM의 기존 지상파 포트폴리오를 적극 활용합니다. 이는 글로벌 부재를 '한국 시장 stickiness'로 대체하는 리더십의 편향을 반영한 선택입니다.
  - risk: KBO 시즌 종료 후 이탈 재발생 및 과도한 Capex 소모로 인한 현금 흐름 악화
- **CEO**: `KBO Season Spike`@0.40, `Naver Plus Synergy`@0.30, `Ad-Tier Optimization`@0.30
  - rationale: Mandate 준수를 위한 행동 계획. KBO 트래픽, 저가 세그먼트 선점, Naver Plus 연결 강건한 전략 수립. CJ ENM 자산 활용으로 Capex 억제하며 경쟁력 유지.
  - risk: KBO 재계약 불확실성 및 Naver Plus 의존도 상승

##### Phase 2 — 비판적 검토 (다수안: `KBO Season Spike`, DA: `CFO`)

- **CTO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Tech Infrastructure Upgrade`@0.20
  - changed `Cultural IP Dominance` → because: R&D 50% 유지로 기술 격차 방어 필요
- **COO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Cultural IP Dominance`@0.20
- **CMO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Cultural IP Dominance`@0.20
  - changed `Aggressive Price Cut` → because: 저가 정책은 브랜드 가치 훼손 및 마진 악화 초래
- **CFO**: `Wavve Integration Cost Cut`@0.60, `Ad-Tier Optimization`@0.40
  - dissent: 현금 잔고 50% 상태에서의 KBO 시즌 마케팅은 단기 트래픽 증가와 장기 LTV 보장 사이 괴리가 존재한다. 계절성 이벤트 종료 후 구독 이탈이 발생하면 초기 투자 대비 현금 흐름 악화 가능성이 높다. 생존을 위한 유동성 확보가 필수적이며, 시즌성 성장 베팅보다 구조적 비용 절감이 우선되어야 한다. 또한 Wavve 통합 과정에서 발생할 수 있는 예상치 못한 비용 리스크를 고려할 때, 불필요한 마케팅 지출은 현금 고갈 가속화로 이어질 수 있다. 이러한 위험 요인들은 자본 보존 원칙과 상충되므로 대폭 축소해야 한다. 추가적으로 마케팅 예산의 비효율적 배분은 수익성 회복 속도를 지연시킨다. 따라서 성장 지표보다 현금 흐름 안정성을 최우선 순위로 두어야 한다. 이를 위해 기존 제안에서 가장 큰 비중을 차지하는 성장형 마케팅을 배제하고 효율성 중심의 재무 전략으로 전환한다. 결과적으로 회사의 지속 가능성 확보가 가능해지며, 미래 경쟁력을 갖춘 상태를 유지할 수 있다. 이는 단순한 방어 전략
- **CEO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.30, `Cultural IP Dominance`@0.25
  - changed `Ad-Tier Optimization` → because: 문화 IP 우위 확보 목적

**Position changes:**
- CTO: Cultural IP Dominance → KBO Season Spike+Naver Plus Synergy+Tech Infrastructure Upgrade (R&D 50% 유지로 기술 격차 방어 필요)
- CMO: Aggressive Price Cut → KBO Season Spike+Naver Plus Synergy+Cultural IP Dominance (저가 정책은 브랜드 가치 훼손 및 마진 악화 초래)
- [반대] CFO: 현금 잔고 50% 상태에서의 KBO 시즌 마케팅은 단기 트래픽 증가와 장기 LTV 보장 사이 괴리가 존재한다. 계절성 이벤트 종료 후 구독 이탈이 발생하면 초기 투자 대비 현금 흐름 악화 가능성이 높다. 생존을 위한 유동성 확보가 필수적이며, 시즌성 성장 베팅보다 구조적 비용 절감이 우선되어야 한다. 또한 Wavve 통합 과정에서 발생할 수 있는 예상치 못한 비용 리스크를 고려할 때, 불필요한 마케팅 지출은 현금 고갈 가속화로 이어질 수 있다. 이러한 위험 요인들은 자본 보존 원칙과 상충되므로 대폭 축소해야 한다. 추가적으로 마케팅 예산의 비효율적 배분은 수익성 회복 속도를 지연시킨다. 따라서 성장 지표보다 현금 흐름 안정성을 최우선 순위로 두어야 한다. 이를 위해 기존 제안에서 가장 큰 비중을 차지하는 성장형 마케팅을 배제하고 효율성 중심의 재무 전략으로 전환한다. 결과적으로 회사의 지속 가능성 확보가 가능해지며, 미래 경쟁력을 갖춘 상태를 유지할 수 있다. 이는 단순한 방어 전략
- CEO: Ad-Tier Optimization → KBO Season Spike+Naver Plus Synergy+Cultural IP Dominance (문화 IP 우위 확보 목적)

##### Phase 3 — CEO 종합

**Decision:** KBO 시즌 트래픽 집중 활용; 네이버 플러스 통합 마케팅

**Reasoning:** 정치적 요인 포함한 라이선스 사수; 채널 협업으로 CAC 절감 효과

#### Adjudicator panel (3 experts)

**Industry Veteran**: OTT 환경에서 단순 콘텐츠 경쟁보다 이커머스나 플랫폼 파트너십을 통한 생계계 락인이 더 높은 사용자 전환 비용 장벽을 형성하며 구독 유지율에 결정적 영향을 미칩니다.

- side_a: `strong` ↑ — Coupang Play 는 로켓 와우 멤버십 통합을 통해 높은 전환 비용을 확보하며 스포츠 독점 전략으로 이탈률을 방어하고 있어 급격한 성장을 주도하고 있습니다.
- side_b: `dominant` → — Netflix Korea 는 압도적인 현금 보유량과 글로벌 오리지널 콘텐츠 자산으로 시장 지배력을 유지하지만 가격 인상으로 인한 신규 이탈 리스크가 상존합니다.
- side_c: `contested` ↘ — Tving 는 KBO 시즌을 활용한 단기 점유율 확대가 가능하나 낮은 현금 수준과 계절성 의존으로 장기적인 재무 건전성과 지속 가능성이 약화될 우려가 있습니다.

**Strategy Consultant**: Coupang Play 의 이커머스 결합 모델은 단기적으로 참여 계층을 확대하지만 장기적인 콘텐츠 투자 부담은 여전한 반면, Netflix Korea 는 자본 우위로 시장 정석을 주도한다.

- side_a: `strong` ↑ — Coupang Play 는 Rocket WOW 의 광범위 사용자 베이스를 기반으로 마케팅 효율을 높이며 시장 영향력을 확대하고 있다.
- side_b: `dominant` ↗ — Netflix Korea 는 고품질 글로벌 콘텐츠 투자 성과를 인정받아 가격 민감 계층을 제외한 타겟에서 충성도를 유지하고 있다.
- side_c: `contested` ↘ — Tving 은 특정 시즌에 몰린 트래픽과 낮은 현금 보유량 사이의 괴리로 인해 재무 건전성이 취약해지고 있다.

**Regulatory/Policy Expert**: 국내 OTT 시장은 이커머스 기반 결합 판매가 경쟁력 원천이지만 이는 독과점 소지가 있어 규제 당국의 집중적인 공정한 거래 감시 대상이 되고 있습니다.

- side_a: `strong` ↑ — Rocket Wow 결합 판매 및 스포츠 독점권 확보로 시장 점유율 확대 효과가 명확하나 공정거래 관련 리스크 관리가 필요합니다.
- side_b: `dominant` ↗ — 글로벌 규모의 자본과 오리지널 콘텐츠 포트폴리오가 가격 인상에 대한 충격을 흡수하며 안정적인 성장 궤도를 유지합니다.
- side_c: `contested` ↘ — 현금 유동성 부족으로 Wavve 통합 비용 부담이 커지고 시즌성 스파이크 의존도가 성장 제약 요인으로 작용합니다.

#### Adjudicator synthesis

> Coupang Play 는 Rocket WOW 멤버십과의 결합을 통해 기존 이커머스 사용자 기반을 OTT 구독으로 전환시키며 시장 점유율을 빠르게 높이고 있습니다. 반면 Netflix Korea 는 글로벌 자본력을 바탕으로 고품질 콘텐츠를 지속적으로 투자하며 가격 민감 계층을 제외한 충성도 높은 사용자층을 유지하고 있습니다. Tving 은 KBO 시즌을 활용한 단기 트래픽 증가에 성공했으나, 낮은 현금 보유량과 계절성 의존도가 누적되어 장기적인 성장 동력이 약화되는 양상을 보이고 있습니다.

**Interaction analysis:** Coupang Play 의 이커머스 결합 모델이 시장 진입 장벽을 높이는 반면, Netflix Korea 는 자본 우위로 이를 견제하며 시장을 주도하고 있습니다. Tving 은 특정 시즌의 트래픽 급증으로 일시적 점유율을 얻었으나, 지속적인 현금 소모와 계절성 의존도가 경쟁력을 약화시키는 요인으로 작용하고 있습니다.

---

<a id="turn-2"></a>
## Turn 2

**Events fired:** —

### **Coupang Play** (side_a)

- Final action: `Rocket Wow Integration`@0.85
- Position: `dominant` ↑
- Cash: 58.0%
- Adjudicator rationale: 로켓와우 멤버십을 통한 커머스 락인 효과가 시장 진입 장벽을 완성하며, 규제 리스크에도 불구하고 생태계 통합 우위를 점하고 있습니다.

##### Phase 1 — 독립 제안

- **CFO**: `Rocket Wow Integration`@0.40, `Premium Content Acquisition`@0.30, `Data Monetization Boost`@0.30
  - rationale: 넷플릭스 가격 인상으로 인한 이탈 방지 및 티빙의 KBO 시즌 공백 활용을 위해, CEO 의 '쿠팡 로직'에 따라 Rocket Wow 를 통한 MAU 급증 (단기 손실 감수) 을 최우선으로 실행함. Board mandate 에 따른 오리지널 콘텐츠 예산 증액은 필수적이나, 현금 소진 속도를 고려해 스포츠 라이선스 유지와 병행하는 균형 전략임.
  - risk: 고정된 가격 정책과 MAU 중심의 과투자 리스크
- **CTO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Tech Infrastructure Upgrade`@0.20
  - rationale: CEO 의 쿠팡 출신 배경과 'MAU 우선' 편향에 따라 로켓와우 통합을 최우선으로 추진하되, 넷플릭스의 가격 인상과 고품질 콘텐츠 공세에 맞서기 위해 기존 이커머스 데이터를 활용한 타겟팅 광고 (Data Monetization) 로 수익성을 방어해야 함. 또한 라이브 스포츠 독점 전략의 핵심인 MLB/EPL 중계 시 안정적 서비스 제공을 위한 인프라 투자가 필수적이므로 R&D(기술) 비중을 유지하며 경쟁사 대비 기술 우위를 선점함.
  - risk: 라이브 스포츠 트래픽 폭주로 인한 서비스 장애 및 서버 비용 과다 지출
- **CMO**: `Rocket Wow Integration`@0.45, `Ecosystem Bundle Push`@0.35, `Data Monetization Boost`@0.20
  - rationale: 보드는 단일 전략(스포츠) 의존을 경고했으나, CEO의 쿠팡 출신 특성과 'MAU 우선' 문화, 그리고 '로켓와우 통합 과신'이라는 리더십 편향을 반영하여 이커머스 생태계와의 밀착형 방어 및 성장 전략을 선택함. 넷플릭스의 콘텐츠 공격 (오징어게임 시즌 3) 에 대항해 순수 OTT 경쟁보다는 '구매 전환'이라는 쿠팡만의 모터를 통해 차별화된 수익 구조를 구축하는 것이 현재 강세(↑) 위치에서의 가장 합리적인 방어이자 공세적 대응임.
  - risk: 넷플릭스 오징어게임 시즌 3의 강력한 스티키니스로 인해 가격 동결 전략이 MAU 유지에 실패할 수 있음.
- **COO**: `Rocket Wow Integration`@0.45, `Premium Content Acquisition`@0.35, `Data Monetization Boost`@0.20
  - rationale: 보드 mandates(라이브 스포츠 예산 재배분) 에 따라 MLB/EPL 등 기존 스포츠 예산의 일부를 'Premium Content Acquisition'으로 전환하여 오리지널 포트폴리오를 강화한다. CEO 의 로켓와우 통합 과신 (Blind Spot) 을 반영해 'Rocket Wow Integration'을 최우선으로 배치하여 MAU 증대를 꾀하되, 이는 단순 유입이 아닌 e-commerce 전환을 위한 토대다. 'Data Monetization Boost'는 쿠팡의 핵심 강점인 이커머스 데이터를 활용한 ARPU 증대로, 넷플릭스의 가격 인상과 콘텐츠 공세에 맞서 차별화된 수익 모델을 구축하기 위함이다. 다만, 세 가지 대형 투자가 동시 진행될 경우 현금 흐름 (60%) 에 무리를 줄 수 있어 리스크 관리가 시급하다.
  - risk: 동시 다발적 투자로 현금 소진 가속화 및 단일 전략 고착화 우려
- **CEO**: `Premium Content Acquisition`@0.45, `Rocket Wow Integration`@0.35, `Ad-Tier Optimization`@0.20
  - rationale: Board Mandate(스포츠 예산 50% 원작 대체) 반영하여 콘텐츠 포트폴리오 다각화. 넷플릭스 Korea 가격인상 시기와 맞물려 프리미엄 가치제시. 쿠팡 출신으로서 Rocket Wow 를 통한 이커머스 연계는 유지하되 수익성 위주 전환.
  - risk: 콘텐츠 제작비 급증에 따른 단기 손실 확대 위험

##### Phase 2 — 비판적 검토 (다수안: `Rocket Wow Integration`, DA: `CFO`)

- **CTO**: `Tech Infrastructure Upgrade`@0.45, `Rocket Wow Integration`@0.35, `Data Monetization Boost`@0.20
  - changed `Rocket Wow Integration` → because: R&D 투자 확대 필수
- **COO**: `Rocket Wow Integration`@0.45, `Premium Content Acquisition`@0.35, `Ad-Tier Optimization`@0.20
  - changed `Data Monetization Boost` → because: 현금 소진 위험으로 다각화 중단
- **CMO**: `Rocket Wow Integration`@0.45, `Ecosystem Bundle Push`@0.35, `Data Monetization Boost`@0.20
- **CEO**: `Premium Content Acquisition`@0.50, `Rocket Wow Integration`@0.30, `Data Monetization Boost`@0.20
  - changed `Ad-Tier Optimization` → because: 콘텐츠예산증액데이터활용전환
- **CFO**: `Premium Content Acquisition`@0.60, `Ad-Tier Optimization`@0.40
  - dissent: 대부분의 제안에 포함된 Rocket Wow Integration 은 MAU 성장 속도는 높이지만 실질적인 현금 흐름 개선 효과가 불투명하다. 현재 보존된 현금 보유량이 60% 수준에서 고정비 지출이 집중될 경우, 주요 주석인 Rocket WOW 에 대한 지급 조건이 미래 현금 흐름을 제한할 수 있다. 이는 단순히 단일 전략에 의존하는 것을 해결하지 못하며, 이사회에서 요구한 라이브 스포츠 예산 대폭 재배분이 이루어지지 않은 채 마케팅 비용만 낭비하는 결과를 초래한다. 특히 글로벌 시장에서의 수익성 검증을 거치지 않은 통합 방식은 Coupang Play 의 재무 안정성에 직접적인 위협이 된다. 경영상 태세가 미약할 때 MAU 중심의 지표는 오히려 비효율적 자본 배분을 유도한다. 이러한 이유로 단기적 유입보다는 지속적인 현금 창출 메커니즘이 우선되어야 한다. 타 플랫폼인 Netflix Korea 나 Tving 의 사례에서도 볼 수 있듯이 독점 콘텐츠와 구독 수익의 균형이 핵심이다. 즉,

**Position changes:**
- CTO: Rocket Wow Integration → Tech Infrastructure Upgrade+Rocket Wow Integration+Data Monetization Boost (R&D 투자 확대 필수)
- COO: Data Monetization Boost → Rocket Wow Integration+Premium Content Acquisition+Ad-Tier Optimization (현금 소진 위험으로 다각화 중단)
- CEO: Ad-Tier Optimization → Premium Content Acquisition+Rocket Wow Integration+Data Monetization Boost (콘텐츠예산증액데이터활용전환)
- [반대] CFO: 대부분의 제안에 포함된 Rocket Wow Integration 은 MAU 성장 속도는 높이지만 실질적인 현금 흐름 개선 효과가 불투명하다. 현재 보존된 현금 보유량이 60% 수준에서 고정비 지출이 집중될 경우, 주요 주석인 Rocket WOW 에 대한 지급 조건이 미래 현금 흐름을 제한할 수 있다. 이는 단순히 단일 전략에 의존하는 것을 해결하지 못하며, 이사회에서 요구한 라이브 스포츠 예산 대폭 재배분이 이루어지지 않은 채 마케팅 비용만 낭비하는 결과를 초래한다. 특히 글로벌 시장에서의 수익성 검증을 거치지 않은 통합 방식은 Coupang Play 의 재무 안정성에 직접적인 위협이 된다. 경영상 태세가 미약할 때 MAU 중심의 지표는 오히려 비효율적 자본 배분을 유도한다. 이러한 이유로 단기적 유입보다는 지속적인 현금 창출 메커니즘이 우선되어야 한다. 타 플랫폼인 Netflix Korea 나 Tving 의 사례에서도 볼 수 있듯이 독점 콘텐츠와 구독 수익의 균형이 핵심이다. 즉,

##### Phase 3 — CEO 종합

**Decision:** 로켓와우 통합 및 콘텐츠 투자 확대; 로켓와우 통합 및 콘텐츠 투자 확대

**Reasoning:** 이사회 리스크 대응하고 MAU 확대 동시 달성; 이사회 리스크 대응하고 MAU 확대 동시 달성

### Netflix Korea (side_b)

- Final action: `Ad-Tier Optimization`@0.80
- Position: `dominant` ↗
- Cash: 78.3%
- Adjudicator rationale: 글로벌 자본력과 현금 보유량을 바탕으로 아드-티어 최적화와 로컬 오퍼닝을 병행하며 기존 지배력을 공고히 하고 있습니다.

##### Phase 1 — 독립 제안

- **CTO**: `Original Library Expansion`@0.45, `Global Hit Investment`@0.35, `Ad-Tier Optimization`@0.20
  - rationale: CEO의 글로벌 ARPU 회복 mandate 에 따라 오징어게임 시즌 3 효과를 극대화하고, 쿠팡 Play 의 스포츠 독점 전략에 대응하기 위해 '스포츠 연계 오리지널'을 핵심으로 재배분함. 또한, 리더십의 '한국 콘텐츠 1 조 투자 narrative 유지 압박'에 따라 원작 library 확장에 상당 비중을 할당하여 효율성보다 투자 규모를 강조하는 구조적 편향을 반영함.
  - risk: 글로벌 본사의 가격 정책 추종으로 인해 한국 시장 가격 민감 계층 이탈 가속화 가능성
- **CFO**: `Original Library Expansion`@0.55, `Global Hit Investment`@0.25, `Premium Content Acquisition`@0.20
  - rationale: 이사회 mandate 에 따라 쿠팡플레이의 상승세에 대응하기 위해 신규 콘텐츠 예산의 40% 를 로컬 오리지널 제작에 집중했습니다. CEO 의 리더십 특성인 '한국 콘텐츠 1 조 투자 narrative 유지'와 '글로벌 본사 metrics 우선'을 반영하여, 단순 라이선스보다 고비용 제작 위주로 편성했습니다. 또한 경쟁사 (Coupang Play) 의 스포츠 독점 전략에 대응하기 위해 기존 글로벌 히트 효과를 활용하되, KBO 시즌 기간 사용자 유입을 위한 '스포츠 연계 오리지널' 투자를 병행합니다. 이는 가격 민감 계층 이탈 방어를 위한 방어적 전략과 동시에 시장 주도력 유지에 필수적입니다.
  - risk: 높은 현금 소진으로 인한 유동성 압박 및 ROI 불확실성
- **CMO**: `Original Library Expansion`@0.45, `Global Hit Investment`@0.35, `Ecosystem Bundle Push`@0.20
  - rationale: 보통 전략은 '강동한 CEO'의 글로벌 ARPU 회복 mandate 와 '한국 콘텐츠 1조 투자 narrative'를 반영하여, 쿠팡플레이의 스포츠 독점 공세에 대응하기 위해 KBO 시즌 기간 한정 '스포츠 연계 오리지널'을 Ecosystem Bundle Push 에 포함했습니다. 또한, Board mandate 에 명시된 쿠팡플레이와의 직접적 로컬 오리지널 경쟁을 Original Library Expansion 으로 우선 실행하되, 글로벌 히트 효과를 극대화하기 위해 Global Hit Investment 를 병행합니다. 이는 리더십의 '라이브 스포츠 부재'를 오리지널 콘텐츠로 대체하려는 편향과 '절대 투자 규모' 선호를 동시에 충족시킵니다.
  - risk: 글로벌 본사의 ARPU 중심 지표에 따라 한국 시장 가격 민감 계층의 이탈이 가속화될 수 있음.
- **COO**: `Original Library Expansion`@0.60, `Aggressive Price Cut`@0.30, `Global Hit Investment`@0.10
  - rationale: 보드의 쿠팡 플레이 대응 mandate(로컬 오리지널 40%) 를 최우선으로 반영하되, CEO 의 글로벌 ARPU 회복 mandate 와 오징어게임 시즌 3 연계 전략도 일부 포함. 다만, 스포츠 연계 오리지널은 리스크가 높아 현재는 라이브 스포츠 부재에 대한 구조적 약점을 콘텐츠로만 메우려 하는 리더십의 편향성을 반영하여 '가격 민감 계층 방어'를 위해 가격 정책 (Aggressive Price Cut) 을 병행함. 동시 실행 시 자원 분산 위험이 있으나, 시장 주도자로서 쿠팡의 모멘텀을 막기 위한 필수적인 공격-방어 조합임.
  - risk: 동시 다발적 예산 집행으로 현금 소진 속도 가속화 및 조직 병목 발생
- **CEO**: `Original Library Expansion`@0.40, `Ad-Tier Optimization`@0.30, `Global Hit Investment`@0.30
  - rationale: 글로벌 본사 기대치 충족하며 원천 제작비의 중요성을 강조한다. 쿠팡 Play 의 모멘텀에 맞서 대규모 투자로 대응하려 한다. 스포츠 권리 대신 드라마 연계로 비용 효율 극대화한다.
  - risk: 과다 투자로 단기 이익률 감압 가능성

##### Phase 2 — 비판적 검토 (다수안: `Original Library Expansion`, DA: `CFO`)

- **CTO**: `Original Library Expansion`@0.45, `Global Hit Investment`@0.35, `Tech Infrastructure Upgrade`@0.20
  - changed `Ad-Tier Optimization` → because: R&D 투자로 경쟁력 방어 필요
- **COO**: `Original Library Expansion`@0.45, `Ad-Tier Optimization`@0.35, `Global Hit Investment`@0.20
  - changed `Original Library Expansion` → because: 동시 다발 예산으로 현금 소진 가속화 위험
- **CMO**: `Original Library Expansion`@0.45, `Global Hit Investment`@0.30, `Ad-Tier Optimization`@0.25
  - changed `Ecosystem Bundle Push` → because: 가격 민감도 높은 계층 이탈 방어에 직접적 대응 불가
- **CEO**: `Original Library Expansion`@0.45, `Ad-Tier Optimization`@0.30, `Global Hit Investment`@0.25
  - changed `Original Library Expansion` → because: 투자 규모 내러티브 강화
- **CFO**: `Ad-Tier Optimization`@0.40, `Premium Content Acquisition`@0.20, `Original Library Expansion`@0.40
  - dissent: 다수안의 치명적 약점은 대폭 증가한 원천 제작비로 인해 현금 소진 속도가 빨라져 시장 변동성 시 유동성 위험이 발생한다는 점임. 40~60% 의 높은 비중은 ROI 회수에 장기를 요구하나 현금 보유율이 80% 라는 점은 지속 가능한 성장에는 필수적인 조건임에도 불구하고 안전마진을 과도하게 축소할 위험이 있음. 또한 급격한 가격 할인과 병행 시 브랜드 가치 하락 우려가 존재함. 현금 흐름을 최우선으로 확보하는 구조가 필요함. 현재 상태에서 Netflix Korea 의 상승세 대응은 단순 제작비 투입보다 수익 모델 확립을 통한 방어선이 선결과제로 보임. 이견은 단순 비용 절감이 아닌 자산 효율화를 통한 생존 전략 강구임. Coupang Play 는 내부적으로 안정적인 자금 조달을 우선해야 하며 외부 변수에 대한 취약성은 줄여야 함. 경쟁사가 가속화되는 상황에서 오히려 과도한 지출은 향후 가격 전쟁에서 불리한 입지를 만들 수 있음. 재정적 자산을 확보하면 향후 기회비용 대비 효율적인 투하

**Position changes:**
- CTO: Ad-Tier Optimization → Original Library Expansion+Global Hit Investment+Tech Infrastructure Upgrade (R&D 투자로 경쟁력 방어 필요)
- COO: Original Library Expansion → Original Library Expansion+Ad-Tier Optimization+Global Hit Investment (동시 다발 예산으로 현금 소진 가속화 위험)
- CMO: Ecosystem Bundle Push → Original Library Expansion+Global Hit Investment+Ad-Tier Optimization (가격 민감도 높은 계층 이탈 방어에 직접적 대응 불가)
- CEO: Original Library Expansion → Original Library Expansion+Ad-Tier Optimization+Global Hit Investment (투자 규모 내러티브 강화)
- [반대] CFO: 다수안의 치명적 약점은 대폭 증가한 원천 제작비로 인해 현금 소진 속도가 빨라져 시장 변동성 시 유동성 위험이 발생한다는 점임. 40~60% 의 높은 비중은 ROI 회수에 장기를 요구하나 현금 보유율이 80% 라는 점은 지속 가능한 성장에는 필수적인 조건임에도 불구하고 안전마진을 과도하게 축소할 위험이 있음. 또한 급격한 가격 할인과 병행 시 브랜드 가치 하락 우려가 존재함. 현금 흐름을 최우선으로 확보하는 구조가 필요함. 현재 상태에서 Netflix Korea 의 상승세 대응은 단순 제작비 투입보다 수익 모델 확립을 통한 방어선이 선결과제로 보임. 이견은 단순 비용 절감이 아닌 자산 효율화를 통한 생존 전략 강구임. Coupang Play 는 내부적으로 안정적인 자금 조달을 우선해야 하며 외부 변수에 대한 취약성은 줄여야 함. 경쟁사가 가속화되는 상황에서 오히려 과도한 지출은 향후 가격 전쟁에서 불리한 입지를 만들 수 있음. 재정적 자산을 확보하면 향후 기회비용 대비 효율적인 투하

##### Phase 3 — CEO 종합

**Decision:** 광고 tier 전환율 향상과 ARPU 증대; 로컬 오리지널 투자로 Coupang Play 방어; 오징어게임 시즌 3 효과 극대화 투자

**Reasoning:** 현금 흐름 개선 및 가격 민감 고객 방어; 지시 준수 및 Coupang Play 대항; 본사 글로벌 지표 강조와 현금 리스크 균형

### Tving (side_c)

- Final action: `Cultural IP Dominance`@0.80
- Position: `contested` ↘
- Cash: 37.7%
- Adjudicator rationale: KBO 시즌의 일시적 반등에도 불구하고 와브 통합 비용 부담과 현금 유동성 부족으로 장기 생존 능력이 약화되고 있습니다.

##### Phase 1 — 독립 제안

- **COO**: `Cultural IP Dominance`@0.40, `KBO Season Spike`@0.35, `Wavve Integration Cost Cut`@0.25
  - rationale: CEO의 CJ ENM 자산 활용 선호와 KBO 중계권 사수 정치적 무력감을 반영함. Board 의 '오리지널 드라마 집중' 지시와 CEO 의 '스포츠 방어' 충동 사이 타협점으로, 과도한 신규 투자 없이 기존 자산과 정치적 현안을 동시에 처리하여 현금 44% 보존과 전략적 지속성 확보를 도모함.
  - risk: 자사 콘텐츠 제작 지연으로 넷플릭스 추격 불가, KBO 예산 집행 시 현금 소모 가속화
- **CFO**: `Cultural IP Dominance`@0.55, `KBO Season Spike`@0.35, `Wavve Integration Cost Cut`@0.10
  - rationale: 보드 지시대로 단기 이벤트 의존을 줄이고 CJ ENM/JTBC 자산(Cultural IP)에 집중하되, CEO의 정치적 편향(임원진 충돌 비용 감수)과 모회사 IR 논리(와브 합병 매몰 비용 인식 거부)를 반영하여 KBO 시즌 방어와 Wavve 효율화를 병행함. 넷플릭스의 장기 우위를 무너뜨리기 위해 고가 정책이 아닌 자사 자산 활용으로 저가 세그먼트 점유율 선점을 도모.
  - risk: 정치적 비용으로 인한 KBO 전략 실패 가능성, 현금 소모 가속화 리스크
- **CMO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Cultural IP Dominance`@0.20
  - rationale: 현재 전략 (캠페인) 이 '지역 밀착형 콘텐츠'와 '스포츠 중계권 공동 투자/제휴'를 핵심으로 명시하고 있어, 이를 실행하기 위해 KBO 시즌 트래픽 방어와 네이버 플러스 연동을 우선시함. CJ ENM/JTBC의 기존 자산 활용을 통해 Capex 를 통제하면서도 시장 점유율 하락을 막는 방어적 태세 유지. 단, 보드 mandate 의 '오리지널 드라마 집중' 요구와는 상충되나, 현재 캠페인 실행 의무에 따라 스포츠와 지역 밀착 전략을 최우선으로 배치함.
  - risk: 단기적 이벤트 의존성 심화로 장기 오리지널 경쟁력 확보 지연
- **CTO**: `KBO Season Spike`@0.45, `Cultural IP Dominance`@0.35, `Wavve Integration Cost Cut`@0.20
  - rationale: 현재 캠페인 (지역 밀착 + 스포츠 제휴) 을 실행하되, C-suite 의 '한국 시장 stickiness' 편향과 CJ ENM 모회사 정치를 반영하여 단기 이벤트 의존성을 줄이고 장기 오리지널 우위를 확보해야 함. 쿠팡플레이의 독점 전략에 대응하기 위해 기존 KBO 시즌 마케팅을 단독이 아닌 '공동 투자' 형태로 전환하여 비용 효율을 높이고, Wavve 합병 후 숨겨진 중복 비용을 정리해 그 자금을 신규 드라마 제작에 집중함. 이는 R&D(콘텐츠) 부족으로 인한 경쟁력 침식을 막고, 보편적인 가격 인하보다는 자산 기반의 차별화를 꾀하는 것임.
  - risk: 모회사 정치적 충돌로 KBO 중계권 협상 지연 시 트래픽 급감 리스크
- **CEO**: `Cultural IP Dominance`@0.60, `Ad-Tier Optimization`@0.30, `Naver Plus Synergy`@0.10
  - rationale: -board mandate 에 따라 단기 KBO 의존도 해소를 위해 CJ ENM 과 JTBC 가 보유한 강력한 문화 IP 를 활용해 장기 방어선 구축. 44% 현금 상황에서는 Ad-Tier 로 수익 모델 다변화가 필수적이며 Naver Plus 협력을 통한 기존 마케팅 비용 최적화로 R&D 자금 확보 목표.
  - risk: 콘텐츠 리스크와 집행 시점 지연으로 단기 트래픽 이탈 가능성

##### Phase 2 — 비판적 검토 (다수안: `Cultural IP Dominance`, DA: `CFO`)

- **COO**: `Cultural IP Dominance`@0.45, `Wavve Integration Cost Cut`@0.35, `Churn Prevention Campaign`@0.20
  - changed `KBO Season Spike` → because: 보드 mandate 에 따른 KBO 예산 전면 중단 및 현금 보존
- **CMO**: `Cultural IP Dominance`@0.65, `KBO Season Spike`@0.25, `Naver Plus Synergy`@0.10
  - changed `CMO: KBO Season Spike+Naver Plus Synergy+Cultural IP Dominance` → because: 지정된 '오리지널 드라마' 집중 mandate 반영
- **CTO**: `Tech Infrastructure Upgrade`@0.35, `Cultural IP Dominance`@0.35, `KBO Season Spike`@0.20
  - changed `KBO Season Spike` → because: R&D 투자 부족 시 경쟁력 붕괴
- **CFO**: `Ad-Tier Optimization`@0.60, `Wavve Integration Cost Cut`@0.40
  - dissent: 문화적 IP 우위 제안의 치명적 약점은 확실한 ROI 없이 막대한 선투자 비용 (CAPEX) 을 발생시킨다는 점입니다. 현금 보유율이 44%인 상황에서 예측 불가능한 콘텐츠 반응과 긴 회수 주기는 유동성 위기를 가속화하며, 이는 재무 적정성을 해칩니다. 경쟁사 추격보다 현재 자본 유지가 최우선 과제여야 합니다. 경쟁사가 원천적인 자본력이 있더라도 현금 흐름이 끊기면 시장에서 퇴출당할 수 있습니다. 즉각적인 수익 창출 모델 없이 대규모 제작비를 지출하는 것은 위험한 베팅입니다. 시장 점유율 하락 보다는 재무 건전성이 먼저여야 지속 가능한 경쟁력을 갖출 수 있습니다. 다른 부서들은 KBO 등 단기 이벤트에 의존해 변동성을 키우는 반면, 저는 내부 효율성과 ARPU 증대를 통한 안전 장벽 구축이 필요합니다. 현금 소모 리스크는 생존을 위협하므로, 수익 모델이 검증된 영역에 집중해야 합니다. 단기 트래픽 증가보다는 장기 재정 부담 완화가 우선시 되어야 합니다. 이러한 이유로 대다수의 콘텐츠
- **CEO**: `Cultural IP Dominance`@0.70, `Wavve Integration Cost Cut`@0.20, `Ad-Tier Optimization`@0.10
  - changed `KBO Season Spike` → because: 이벤트 예산 금지

**Position changes:**
- COO: KBO Season Spike → Cultural IP Dominance+Wavve Integration Cost Cut+Churn Prevention Campaign (보드 mandate 에 따른 KBO 예산 전면 중단 및 현금 보존)
- CMO: KBO Season Spike+Naver Plus Synergy+Cultural IP Dominance → Cultural IP Dominance+KBO Season Spike+Naver Plus Synergy (지정된 '오리지널 드라마' 집중 mandate 반영)
- CTO: KBO Season Spike → Tech Infrastructure Upgrade+Cultural IP Dominance+KBO Season Spike (R&D 투자 부족 시 경쟁력 붕괴)
- [반대] CFO: 문화적 IP 우위 제안의 치명적 약점은 확실한 ROI 없이 막대한 선투자 비용 (CAPEX) 을 발생시킨다는 점입니다. 현금 보유율이 44%인 상황에서 예측 불가능한 콘텐츠 반응과 긴 회수 주기는 유동성 위기를 가속화하며, 이는 재무 적정성을 해칩니다. 경쟁사 추격보다 현재 자본 유지가 최우선 과제여야 합니다. 경쟁사가 원천적인 자본력이 있더라도 현금 흐름이 끊기면 시장에서 퇴출당할 수 있습니다. 즉각적인 수익 창출 모델 없이 대규모 제작비를 지출하는 것은 위험한 베팅입니다. 시장 점유율 하락 보다는 재무 건전성이 먼저여야 지속 가능한 경쟁력을 갖출 수 있습니다. 다른 부서들은 KBO 등 단기 이벤트에 의존해 변동성을 키우는 반면, 저는 내부 효율성과 ARPU 증대를 통한 안전 장벽 구축이 필요합니다. 현금 소모 리스크는 생존을 위협하므로, 수익 모델이 검증된 영역에 집중해야 합니다. 단기 트래픽 증가보다는 장기 재정 부담 완화가 우선시 되어야 합니다. 이러한 이유로 대다수의 콘텐츠
- CEO: KBO Season Spike → Cultural IP Dominance+Wavve Integration Cost Cut+Ad-Tier Optimization (이벤트 예산 금지)

##### Phase 3 — CEO 종합

**Decision:** 오리지널 드라마로 시장 차별화; 비용 절감으로 현금 흐름 보호; 광고 tier 확대로 수익성 향상

**Reasoning:** 보드 mandated 전략 반영, 원천 콘텐츠로 경쟁사 대비; 보수적 capex 관리, 중복 콘텐츠 정리; 예산 소모 없이 ARPU 증대 전략

#### Adjudicator panel (3 experts)

**Regulatory/Policy Expert**: 한국 OTT 시장은 Rocket WOW 의 락인 효과로 인해 경쟁사의 독립적 마케팅 여력이 축소되고 있으며, 규제 당국의 플랫폼 집중도 심사가 강화될수록 중소기업 플레이어의 생존률은 급감할 전망이다.

- side_a: `dominant` ↑ — Coupang Play 의 Rocket WOW 를 활용한 회원제 통합이 활성화되어 시장 진입 장벽이 사실상 완성되었으며, 규제 검토 대상임에도 불구하고 생태계 락인 효과는 확실하다.
- side_b: `dominant` → — Netflix Korea 는 현금 보유량과 글로벌 광고 서버 인프라를 바탕으로 가격 변동성을 흡수하며 기존 지배력을 공고히 하고 있으나 신규 성장 동력은 제한적이다.
- side_c: `weak` ↓ — Tving 은 Wavve 통합 비용 부담과 KBO 시즌 외 현금 유동성 부재로 인해 자본 효율성이 저하되어 규제 리스크에 취약한 약세 국면이다.

**Industry Veteran**: 생태계 끼워팔기 모델은 단순 엔터테인먼트 소비를 생활 인프라화하여 고객 이탈 비용을 비선형적으로 상승시키므로, 순수 콘텐츠 경쟁사들은 이를 방어하기 위해 추가적인 마케팅 지출 압력을 받습니다.

- side_a: `dominant` ↗ — 로켓와우 멤버십과의 강력한 결합으로 고객 전환 비용이 상승하고 있어 다른 경쟁사의 콘텐츠 투자 효과를 상쇄하며 우위를 점하고 있습니다.
- side_b: `dominant` → — 글로벌 자본력을 바탕으로 아드 - 티어 최적화와 로컬 오퍼닝을 병행하지만 라이브 스포츠 부재로 인해 점유율 방어에 집중하는 단계입니다.
- side_c: `contested` ↗ — KBO 시즌과 CJ ENM 이 보유하는 문화 IP 가 차단의 역할을 하지만 낮은 현금 유동성으로 단기적 반등 외엔 포지션 변화에는 한계가 있습니다.

**Strategy Consultant**: 시장 구조상 커머스 바운딩과 글로벌 콘텐츠 자원의 유병량 차이가 현금 소모 효율성을 결정하며, 이는 장기적으로 생존 능력을 좌우하는 핵심 변수로 작용한다.

- side_a: `strong` ↑ — Rocket Wow 와의 시너지로 커머스 기반 사용자가 OTT 이용 기반으로 전환되며 MAU 성장이 궤도에 올랐으나 콘텐츠 포트폴리오의 깊이 차이는 여전히 존재한다.
- side_b: `dominant` ↗ — 높은 현금 보유량을 바탕으로 한 오리지널 콘텐츠와 광고 tier 전략이 결합되어 글로벌 히트 기대감 속에서도 시장 지배력을 지속적으로 강화하고 있다.
- side_c: `contested` ↘ — 와브 Wavve 통합 비용 절감과 로컬 IP 강화 노력이 필요하나 부족해진 자금 여력으로 인해 다른 두 플레이어와의 격차를 벌리는 데 한계가 있다.

#### Adjudicator synthesis

> Coupang Play 는 T1 에서 시작한 라이브 스포츠 독점 전략을 로켓와우 멤버십과 결합하며 시장 진입 장벽을 사실상 완성했습니다. Netflix Korea 는 T1 의 광고 tiers 최적화 성과를 바탕으로 현금 보유량을 활용해 점유율 방어와 성장을 동시에 추구하고 있습니다. 반면 Tving 은 T1 의 KBO 시즌 상승세를 일시적 반등으로만 활용했을 뿐, 와브 통합 비용과 자금 부족으로 인해 격차가 벌어지고 있습니다. 결과적으로 커머스 기반의 락인 효과와 글로벌 자본력의 차이가 시장 구조를 재편하며 Tving 은 생존을 위한 추가 자금이 절실한 상황입니다.

**Interaction analysis:** 로켓와우의 락인 효과로 인해 Tving은 순수 콘텐츠 경쟁사로서 마케팅 여력이 극도로 축소된 반면, Netflix 는 글로벌 인프라를 활용해 가격 변동성을 흡수하며 방어에 집중하고 있습니다. 이로 인해 시장 양극화가 심화되어 Tving 의 자본 효율성 저하가 규제 리스크와 맞물려 약세 국면으로 진입했습니다.

---

<a id="turn-3"></a>
## Turn 3

**Events fired:** 제작비 인플레이션 급등, 구독 피로도 및 이탈 대량 발생

### **Coupang Play** (side_a)

- Final action: `Rocket Wow Integration`@0.80
- Position: `dominant` ↑
- Cash: 56.9%
- Adjudicator rationale: Coupang Play 는 Rocket Wow 멤버십 연계를 통해 물류 및 데이터 인프라를 구독 유지의 핵심 자산으로 전환하며, 규제 리스크에도 불구하고 시장 지배력을 공고히 했습니다.

##### Phase 1 — 독립 제안

- **CTO**: `Data Monetization Boost`@0.40, `Live Sports Exclusive`@0.35, `Ad-Tier Optimization`@0.25
  - rationale: CEO의 쿠팡 생태계 시너지 과신과 MAU 우선주의에 따라, 원천적인 R&D(오리지널 제작) 투자 동결은 단기 성장에 치명적이나, 현재 캠페인인 '스포츠+이커머스 포티리스' 실행을 위해 데이터와 라이브 스포츠를 통한 수익성 극대화가 최우선임. 넷플릭스의 가격 인상과 오리지널 공세에 대응할 직접적인 방어책으로 기술적 최적화와 데이터 활용을 선택함.
  - risk: 넷플릭스 오리지널 투자 확대로 인한 콘텐츠 격차 심화 및 제작비 급등 리스크
- **CMO**: `Ecosystem Bundle Push`@0.45, `Live Sports Exclusive`@0.35, `Data Monetization Boost`@0.20
  - rationale: 네트플릭스의 가격 인상과 콘텐츠 공세에 대응하여, '스포츠 + 이커머스'라는 우리만의 방어적 모방을 강화해야 함. 신규 고비용 오리지널 제작은 자금을 소모하므로 배제하고, 기존 MAU 기반의 광고 단가 상승과 멤버십 락인 (lock-in) 에 집중하는 것이 시장 주도자로서의 최적 전략임. 특히 CEO 의 Retail KPI 동조 성향을 반영해 멤버십 가격 인상을 회피하고 유입만 극대화함.
  - risk: 넷플릭스 오리지널 투자 확대로 인한 차별성 약화 및 단기 수익성 악화
- **CFO**: `Ecosystem Bundle Push`@0.45, `Data Monetization Boost`@0.35, `Ad-Tier Optimization`@0.20
  - rationale: 보드 mandate 에 따라 신규 고비용 오리지널 제작을 동결하고, 기존 'Sports + 멤버십 끼워팔기' 캠페인을 통해 로켓와우 기반 1000 만 MAU 를 유지·확장하는 데 집중함. 넷플릭스의 가격 인상과 콘텐츠 투자 확대에 대응하기 위해, 직접적인 콘텐츠 구매 (Global Hit Investment 등) 대신 이커머스 데이터와 결합한 고단가 광고 상품 (Data Monetization) 과 저가 광고 티어 확대 (Ad-Tier Optimization) 로 수익성을 확보하며, CEO 의 쿠팡 KPI 동조 성향을 반영하여 가격 인상을 피하고 로켓와우 통합 효과를 극대화함.
  - risk: 네트플릭스 가격 인상으로 프리미엄 콘텐츠 유출 가속 시 현금 소진률 증가
- **COO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Churn Prevention Campaign`@0.20
  - rationale: 보드 mandate(신규 고비용 오리지널 동결) 를 준수하며, CEO의 'MAU 우선' 및 '로켓와우 과신' 편향을 반영해 유입과 전환에 집중함. 넷플릭스의 가격 인상을 활용해 로켓와우 통합 효과를 극대화하되, 콘텐츠 부재로 인한 이탈을 막기 위해 타겟팅 리텐션을 병행함. 경쟁사(Tving)의 문화 IP 전략은 자금 부족으로 무력화되었으나, 넷플릭스의 자본력은 직접적인 대항이 불가능하므로 방어적 리텐션으로 버티는 것이 현명함.
  - risk: 고비용 오리지널 제작 동결 시 브랜드 위상 하락 및 넷플릭스 '오징어게임 시즌 3'에 대한 사용자의 감정적 이탈 가속화 가능성
- **CEO**: `Rocket Wow Integration`@0.50, `Ecosystem Bundle Push`@0.30, `Data Monetization Boost`@0.20
  - rationale: 본선 Mandate 의 신규 제작 동결 준수와 Rocket Wow MAU 증대를 최우선으로 함. 넷플릭스 가격 인상기 가격 민감층 방어용 패키지 강화. 리더십 특성상 MAU 내러티브와 Retail KPI 동기화 반영
  - risk: 콘텐츠 단독 충성도 하락으로 인한 이탈 위험 존재

##### Phase 2 — 비판적 검토 (다수안: `Data Monetization Boost`, DA: `CTO`)

- **COO**: `Rocket Wow Integration`@0.60, `Ad-Tier Optimization`@0.30, `Churn Prevention Campaign`@0.10
  - changed `Rocket Wow Integration` → because: 고비용 오리지널 동결, 마케팅 예산 재배치 필요
- **CFO**: `Ecosystem Bundle Push`@0.45, `Data Monetization Boost`@0.35, `Ad-Tier Optimization`@0.20
  - changed `Rocket Wow Integration` → because: 고비용 제작 동결 mandates 반영, 현금 소진 최소화
- **CMO**: `Live Sports Exclusive`@0.45, `Ecosystem Bundle Push`@0.35, `Ad-Tier Optimization`@0.20
  - changed `Rocket Wow Integration` → because: 재가공 및 타겟 마케팅 mandates 반영
- **CTO**: `Tech Infrastructure Upgrade`@0.60, `Rocket Wow Integration`@0.40
  - dissent: 다수안이 제시한 데이터 모네티제이션은 사용자의 시청 데이터를 단순 광고 소스로만 활용하는 접근입니다. 이는 단기 매출은 증가할 수 있으나, 네트플릭스와 같은 글로벌 경쟁사와 차별화되는 기술적 우위나 콘텐츠 가치 전달을 저해할 우려가 있습니다. 특히 R&D 투자가 충분하지 않을 경우, 우리 서비스의 기술적 성능이 상대적으로 낙후되어 2-3 년 내에 시장 경쟁력이 빠르게 하락할 수 있는 구조적 리스크가 존재합니다. 또한 쿠팡의 핵심 강점은 플랫폼 통합이므로 데이터 판매보다는 기반 기술 인프라와 에코시스템 효율화에 자원을 배분해야 합니다. 따라서 단순 타겟팅 중심의 수익 모델보다는 플랫폼 자체의 체감을 높이는 기술적 접근이 필요합니다. 결국 데이터 수익성은 부수적 결과여야 하며, 본질적인 서비스 경험 보장이 선행되지 않는다면 사용자 이탈은 가속화될 것입니다. 네트플릭스 역시 기술과 콘텐츠를 동시에 투자하며 점유율을 유지하므로, 우리 역시 기술 인프라에 대한 지속적인 지출이 필수적입니다.Р
- **CEO**: `Rocket Wow Integration`@0.60, `Ecosystem Bundle Push`@0.30, `Ad-Tier Optimization`@0.10
  - changed `데이터 모니타이제이션` → because: 보드 mandate 에 따른 광고 전환

**Position changes:**
- COO: Rocket Wow Integration → Rocket Wow Integration+Ad-Tier Optimization+Churn Prevention Campaign (고비용 오리지널 동결, 마케팅 예산 재배치 필요)
- CFO: Rocket Wow Integration → Ecosystem Bundle Push+Data Monetization Boost+Ad-Tier Optimization (고비용 제작 동결 mandates 반영, 현금 소진 최소화)
- CMO: Rocket Wow Integration → Live Sports Exclusive+Ecosystem Bundle Push+Ad-Tier Optimization (재가공 및 타겟 마케팅 mandates 반영)
- [반대] CTO: 다수안이 제시한 데이터 모네티제이션은 사용자의 시청 데이터를 단순 광고 소스로만 활용하는 접근입니다. 이는 단기 매출은 증가할 수 있으나, 네트플릭스와 같은 글로벌 경쟁사와 차별화되는 기술적 우위나 콘텐츠 가치 전달을 저해할 우려가 있습니다. 특히 R&D 투자가 충분하지 않을 경우, 우리 서비스의 기술적 성능이 상대적으로 낙후되어 2-3 년 내에 시장 경쟁력이 빠르게 하락할 수 있는 구조적 리스크가 존재합니다. 또한 쿠팡의 핵심 강점은 플랫폼 통합이므로 데이터 판매보다는 기반 기술 인프라와 에코시스템 효율화에 자원을 배분해야 합니다. 따라서 단순 타겟팅 중심의 수익 모델보다는 플랫폼 자체의 체감을 높이는 기술적 접근이 필요합니다. 결국 데이터 수익성은 부수적 결과여야 하며, 본질적인 서비스 경험 보장이 선행되지 않는다면 사용자 이탈은 가속화될 것입니다. 네트플릭스 역시 기술과 콘텐츠를 동시에 투자하며 점유율을 유지하므로, 우리 역시 기술 인프라에 대한 지속적인 지출이 필수적입니다.Р
- CEO: 데이터 모니타이제이션 → Rocket Wow Integration+Ecosystem Bundle Push+Ad-Tier Optimization (보드 mandate 에 따른 광고 전환)

##### Phase 3 — CEO 종합

**Decision:** 로켓와우 결합으로 MAU 목표 달성; 기존 콘텐츠 재가공 및 타겟팅 강화

**Reasoning:** 콘텐츠 투자 축소, 유입 수치 우선; 보드 명령에 따른 비용 효율 집중

### Netflix Korea (side_b)

- Final action: `Original Library Expansion`@0.85
- Position: `dominant` ↗
- Cash: 68.3%
- Adjudicator rationale: Netflix Korea 는 안정적인 현금 흐름을 바탕으로 글로벌 인프라를 활용해 제작비 인플레이션을 관리하며, 가격 협상 압박 속에서도 콘텐츠 경쟁력을 확장했습니다.

##### Phase 1 — 독립 제안

- **CMO**: `Original Library Expansion`@0.60, `Premium Content Acquisition`@0.40
  - rationale: 본사 mandates 에 따른 글로벌 ARPU 회복과 한국 시장 가격 민감도 계층 유지를 동시에 달성하기 위해, 쿠팡플레이의 KBO 독점 전략에 맞서 '스포츠 연계 오리지널'로 차별화하고, 글로벌 히트작의 로컬라이징을 통해 이탈 방지 및 브랜드 신뢰도를 높이는 것이 최선입니다. 기존 광고 타이어 최적화 중단 명령에 따라 예산을 신규 콘텐츠 제작으로 즉시 전환합니다.
  - risk: 고비용 콘텐츠 투자 대비 쿠팡 스포츠 독점 효과 상쇄 실패 시 ARPU 하락 및 점유율 방어 실패 가능성 존재
- **COO**: `Original Library Expansion`@0.65, `Global Hit Investment`@0.25, `Ad-Tier Optimization`@0.10
  - rationale: 보드 mandate 에 따라 광고 tiers 최적화는 중단하고, 쿠팡플레이의 스포츠 독점 전략에 대응하기 위해 '스포츠 연계 오리지널' 제작에 자금을 집중해야 함. 글로벌 히트 효과 극대화를 위해 오징어게임 시즌 3 투자도 병행하되, 리스크 관리를 위해 아드-타이어 최적화는 최소한만 유지하여 현금 효율을 확보함.
  - risk: 동일 전술 반복으로 쿠팡플레이 점유율 상승 저지 실패, 현금 소진 속도 가속화
- **CFO**: `Original Library Expansion`@0.55, `Global Hit Investment`@0.30, `Ad-Tier Optimization`@0.15
  - rationale: 이사회 mandates 에 따라 쿠팡플레이의 우위를 무너뜨리기 위해 광고 tiers 최적화를 즉시 중단하고, 경쟁사 (Coupang Play) 의 KBO 독점 전략에 대응하는 '스포츠 연계 오리지널' 예산을 최우선으로 배분합니다. 글로벌 본사의 ARPU 회복 mandate 를 충족하기 위해 오징어게임 시즌 3 히트 효과를 극대화하되, 한국 시장의 가격 민감 계층 이탈 방어를 위해 기존 광고 tiers 개선은 보류합니다. 이는 리더십의 '한국 콘텐츠 1 조 투자 narrative 유지 압박'과 '라이브 스포츠 부재 대체 전략'이라는 인지적 편향을 반영한 공격적 투자입니다.
  - risk: 스포츠 오리지널 투자 ROI 불확실성 및 현금 소진 가속
- **CTO**: `Original Library Expansion`@0.65, `Global Hit Investment`@0.25, `Ad-Tier Optimization`@0.10
  - rationale: 보드 지시에 따라 쿠팡플레이의 스포츠 독점 전략에 대응하기 위해, 기존 광고 tiers 최적화 중단하고 '스포츠 연계 오리지널'에 자원을 집중합니다. CEO 의 글로벌 ARPU 회복 mandate 에 따라 오징어게임 시즌 3 히트 효과를 극대화하되, 한국 시장 가격 민감 계층 이탈을 막기 위해 로컬 오리지널 라인업을 대폭 보강하는 공격적 투자를 단행합니다. 본사 보고에서 약하게 전달되는 한국 시장 특수성을 고려해, 효율성보다 절대 투자 규모를 통한 경쟁력 방어에 주력합니다.
  - risk: 고비용 제작 리스크 및 스포츠 콘텐츠의 즉각적 트래픽 전환 실패 가능성
- **CEO**: `Original Library Expansion`@0.50, `Churn Prevention Campaign`@0.30, `Global Hit Investment`@0.20
  - rationale: 보드 지시 (원전 예산 재배분) 반영. 쿠팡 플레이의 KBO 독점에 맞선 로컬 유입 유도.
  - risk: 콘텐츠 완성도 불확실성 및 초기 수익 회수 지연

##### Phase 2 — 비판적 검토 (다수안: `Original Library Expansion`, DA: `CFO`)

- **CTO**: `Original Library Expansion`@0.45, `Global Hit Investment`@0.35, `Ad-Tier Optimization`@0.20
- **COO**: `Original Library Expansion`@0.65, `Global Hit Investment`@0.25, `Ad-Tier Optimization`@0.10
- **CMO**: `Original Library Expansion`@0.65, `Global Hit Investment`@0.35
  - changed `Original Library Expansion` → because: 보안 투자 비중 축소, 글로벌 히트 집중
- **CFO**: `Premium Content Acquisition`@0.50
  - dissent: 대규모 오리지널 제작은 현금 소모 속도를 불가피하게 높여 유동성 안전선을 위협합니다. 검증된 기존 IP 라이선스가 단기 적자 감소와 ARPU 방어에 더 효과적입니다.
- **CEO**: `Original Library Expansion`@0.90
  - changed `Ad-Tier Optimization` → because: 보드 명령에 의한 광고 전략 폐기

**Position changes:**
- CMO: Original Library Expansion → Original Library Expansion+Global Hit Investment (보안 투자 비중 축소, 글로벌 히트 집중)
- [반대] CFO: 대규모 오리지널 제작은 현금 소모 속도를 불가피하게 높여 유동성 안전선을 위협합니다. 검증된 기존 IP 라이선스가 단기 적자 감소와 ARPU 방어에 더 효과적입니다.
- CEO: Ad-Tier Optimization → Original Library Expansion (보드 명령에 의한 광고 전략 폐기)

##### Phase 3 — CEO 종합

**Decision:** 오리지널 라인업 대폭 증액 확장; 오징어게임 글로벌 파급력 증폭

**Reasoning:** Coupang Play 대응 및 보드 명령 준수; 글로벌 ARPU 회복 전략 병행

### Tving (side_c)

- Final action: `Wavve Integration Cost Cut`@0.80
- Position: `weak` ↓
- Cash: 25.8%
- Adjudicator rationale: Tving 은 Wavve 통합으로 비용 효율화를 시도했으나, 누적된 현금 소진과 낮은 자본 효율성으로 인해 외부 자본 의존도가 높아지며 시장 주도권을 잃었습니다.

##### Phase 1 — 독립 제안

- **CTO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Wavve Integration Cost Cut`@0.20
  - rationale: CEO 의 '지역 밀착 + KBO' 전략을 실행하되, Board 의 비용 절감 지시에 따라 Wavve 합병 비용 정리 (Cost Cut) 를 병행합니다. 단, R&D 투자 축소 없이 기존 예산 내에서 운영 효율화만 추구하여 장기 경쟁력 붕괴를 막습니다. CJ ENM 모회사 정치적 부담 (Wavve 매몰비용 인식 거부) 을 반영해 단순 해체보다는 내부 정합성 확보에 초점을 둡니다.
  - risk: R&D 50% 유지 불가 시 기술 격차 심화, 현금 고갈 가속
- **CMO**: `Wavve Integration Cost Cut`@0.40, `KBO Season Spike`@0.35, `Naver Plus Synergy`@0.25
  - rationale: 보장된 Mandate(고비용 중단, 저예산 전환) 와 현재 전략(지역 밀착, 네이버 결합) 을 가장 잘 반영한 조합입니다. Wavve 통합 비용 절감은 현금 고갈 위험을 해결하는 필수 조건이며, KBO 시즌과 네이버 플러스 시너지를 통해 경쟁사(Coupang Play, Netflix Korea) 의 공격에 맞서 기존 IP 기반의 저비용 유입을 극대화합니다. 특히 CJ ENM 모회사 정치적 요인으로 인해 비합리적일 수 있는 KBO 투자 강행을 포함하여 리더십의 실제 의사결정 패턴을 반영했습니다.
  - risk: CJ ENM 모회사 정치적 압박으로 KBO 중계권 유지 비용이 추가 발생할 수 있음 (채산성 무시)
- **COO**: `Wavve Integration Cost Cut`@0.50, `KBO Season Spike`@0.30, `Naver Plus Synergy`@0.20
  - rationale: 현재 현금 31% 위험수위와 Board 의 '고비용 투자 중단' mandates 에 따라, 신규 IP 구매는 배제하고 기존 Wavve 자산의 중복 정리를 통해 즉각적인 현금 흐름 개선 (Cash Flow) 을 최우선으로 합니다. CEO 의 KBO 중계권 사수 욕구를 반영하여 저예산 마케팅과 결합한 'KBO Season Spike'를 실행하되, 절대적 신작 제작은 피합니다. Naver Plus 는 타사 대비 높은 CAC 절감을 위한 유일한 수단입니다.
  - risk: 고비용 KBO 중계권 유지로 인한 현금 고갈 가속화 (임원진 정치적 사수 요인)
- **CFO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Wavve Integration Cost Cut`@0.20
  - rationale: CEO 의 정치적 이해관계 (KBO 사수) 와 현금 고갈 (31%) 사이의 갈등을 해결하기 위해, 캠페인 핵심인 '지역 밀착'과 '네이버 플러스'를 통해 저예산 유입을 극대화하되, 내부 비효율 (Wavve 중복) 을 먼저 제거하여 생존 기반을 마련함. 경쟁사 Coupang Play 의 로켓와우 통합에 대응하는 공동 투자 요소를 직접 실행하기엔 현금 부족이므로, 기존 자산을 활용한 효율화로 대체함.
  - risk: KBO 중계권 유지로 인한 고비용 구조 지속 가능성 위험
- **CEO**: `Wavve Integration Cost Cut`@0.50, `Cultural IP Dominance`@0.30, `KBO Season Spike`@0.20
  - rationale: 보드 미션에 따라 현금 보존을 최우선 하였고, Wavve 중복 제거를 통해 비용 절감을 달성한다. CJ ENM·JTBC 자산 활용으로 입지 약화를 막으며, 정치적 부담으로 KBO 세그먼트는 최소 자본 유지하면서 트래픽 방어에 집중한다. 이는 현 자금 상황을 고려한 생존 중심 전술이다.
  - risk: Wavve 효율화 지연 시 현금 유출 심화 및 이탈률 증가

##### Phase 2 — 비판적 검토 (다수안: `KBO Season Spike`, DA: `CFO`)

- **CTO**: `Tech Infrastructure Upgrade`@0.40, `KBO Season Spike`@0.35, `Naver Plus Synergy`@0.25
  - changed `Wavve Integration Cost Cut` → because: R&D 50% 유지 필수, 비용 절감은 경쟁력 저해
- **CMO**: `Wavve Integration Cost Cut`@0.45, `KBO Season Spike`@0.30, `Cultural IP Dominance`@0.25
  - changed `이전에 선택한 카테고리명 (변경 없으면 null)` → because: 고비용 KBO 유지, 저예산 IP 재가공 필요
- **COO**: `Wavve Integration Cost Cut`@0.60, `KBO Season Spike`@0.25, `Naver Plus Synergy`@0.15
  - changed `Cultural IP Dominance` → because: 고비용 문화 IP 투자 중단 필요
- **CEO**: `Wavve Integration Cost Cut`@0.60, `Cultural IP Dominance`@0.30, `Naver Plus Synergy`@0.10
  - changed `KBO Season Spike` → because: 현금 위기 대응 위해 KBO 축소 및 IP 집중
- **CFO**: `Wavve Integration Cost Cut`@0.70, `Ad-Tier Optimization`@0.30
  - dissent: 다수의견 KBO Season Spike 는 높은 라이선스 비용 진입 장벽으로 현금 소진이 가속화된다. 현재 현금 보유량 31% 는 안전선 하회이며, 고비용 콘텐츠 투자는 재무 건전성과 모순된다. 단기 시청률 상승 효과만 강조하여 지속 가능한 이익구조 부재가 문제다. 팀 내 리스크 관리 관점에서 이 전략은 현금 고갈 속도를 늦추기 위한 목표와 배치된다. 주주 입장에서 자본 유지 전략으로서의 우선순위 하락이 명확하다. 현금 유출 구조가 불투명한 상태에서 추가 투자 확장은 자칫 브랜드 신뢰도에 악영향을 줄 수 있다. 따라서 재무 안정성 확보를 위해 비용 통제 조치가 선행되어야 한다. 이는 생존을 위한 필수 조건이며, 무리한 수익 창출 시도보다는 리스크 감축이 더 시급한 상황이다. 경쟁사 추격보다 내부 역량 재정립이 시급하다는 점을 고려할 때 해당 제안은 수정되어야 한다. 특히 고정비 삭감이 중요한 변수이다. 고정비를 줄임으로써 변동비 부담이 낮아져 현금 흐름에 여유가 생긴다. 이를 통해

**Position changes:**
- CTO: Wavve Integration Cost Cut → Tech Infrastructure Upgrade+KBO Season Spike+Naver Plus Synergy (R&D 50% 유지 필수, 비용 절감은 경쟁력 저해)
- COO: Cultural IP Dominance → Wavve Integration Cost Cut+KBO Season Spike+Naver Plus Synergy (고비용 문화 IP 투자 중단 필요)
- CEO: KBO Season Spike → Wavve Integration Cost Cut+Cultural IP Dominance+Naver Plus Synergy (현금 위기 대응 위해 KBO 축소 및 IP 집중)
- [반대] CFO: 다수의견 KBO Season Spike 는 높은 라이선스 비용 진입 장벽으로 현금 소진이 가속화된다. 현재 현금 보유량 31% 는 안전선 하회이며, 고비용 콘텐츠 투자는 재무 건전성과 모순된다. 단기 시청률 상승 효과만 강조하여 지속 가능한 이익구조 부재가 문제다. 팀 내 리스크 관리 관점에서 이 전략은 현금 고갈 속도를 늦추기 위한 목표와 배치된다. 주주 입장에서 자본 유지 전략으로서의 우선순위 하락이 명확하다. 현금 유출 구조가 불투명한 상태에서 추가 투자 확장은 자칫 브랜드 신뢰도에 악영향을 줄 수 있다. 따라서 재무 안정성 확보를 위해 비용 통제 조치가 선행되어야 한다. 이는 생존을 위한 필수 조건이며, 무리한 수익 창출 시도보다는 리스크 감축이 더 시급한 상황이다. 경쟁사 추격보다 내부 역량 재정립이 시급하다는 점을 고려할 때 해당 제안은 수정되어야 한다. 특히 고정비 삭감이 중요한 변수이다. 고정비를 줄임으로써 변동비 부담이 낮아져 현금 흐름에 여유가 생긴다. 이를 통해 재무 안정성을 회복할 수 있다.

##### Phase 3 — CEO 종합

**Decision:** 합병 비용 절감 및 자본 효율화; 네이버 플러스 통합으로 유입 확대

**Reasoning:** 고비용 투자 중지, 합병 비용 최소화; 지역 시장 고수, 해외 자산 지연

#### Adjudicator panel (3 experts)

**Strategy Consultant**: OTT 시장의 경쟁력 차이는 이제 단독 서비스 역량보다 생태계 연동성과 자본력 여부에 따라 결정되는 구조로 전환되었다.

- side_a: `dominant` ↑ — Coupang Play 는 로켓와우 멤버십 연계 전략으로 구독 피로도가 심화되는 환경에서도 사용자 유지력을 강화했다.
- side_b: `dominant` ↗ — Netflix Korea 는 안정적인 현금 흐름을 바탕으로 콘텐츠 투자 규모를 늘리며 글로벌 경쟁력의 핵심 자산을 확장했다.
- side_c: `weak` ↓ — 경쟁사 Tving 은 Wavve Integration 을 통해 비용 효율화를 도모하고 있으나, 낮은 현금 보유율은 지속적인 마진 압박 요인이 된다.

**Industry Veteran**: 공급망과 기술 인프라를 락인으로 활용하는 모델이 콘텐츠 가격 변동성에 노출된 전통적 OTT 모델보다 높은 생존율을 보입니다.

- side_a: `dominant` ↑ — Coupang Play 는 Rocket Wow 와 연계된 데이터 및 물류 인프라 전환 비용 활용이 구독 감소를 상쇄하는 안정성을 제공합니다.
- side_b: `dominant` ↗ — Netflix Korea 는 전 세계적으로 분산된 인프라가 한국 오리지널 제작비 급등을 관리하면서도 수익성은 유지합니다.
- side_c: `weak` ↘ — Tving 은 Naver Plus 시너지가 단기적 유입을 창출했으나 자본 효율화를 위한 내부 구조 조정이 현금 소진을 늦추지 못합니다.

**Regulatory/Policy Expert**: 한국 OTT 시장 규모의 성숙기에 접어들면서 쿠팡플레이, 넷플릭스, 티빙 등의 주요 사업자 간 경쟁 구도는 기존 콘텐츠 품질 뿐 아니라 규제 준수 비용 지불 능력과 자본 효율성의 관점에서 다시 재편되고 있습니다. 자금력이 약한 플레이어는 정부의 기업 구조조정 지원 정책과도 연동되어 생존 가능성에 큰 차이가 발생합니다.

- side_a: `dominant` ↑ — `Rocket WOW` 를 활용한 결합 전략은 Coupang Play 의 이용자 수를 확대했으나, 이는 공정위원회의 시장 지배적 사업자 감시에 부합하여 향후 높은 규제 준수 비용과 시장 접근성 제한 우려를 야기합니다.
- side_b: `dominant` ↗ — `Netflix Korea` 는 오리지널 라인업 확장으로 경쟁 우위를 점하고 있으나, 제작비 인플레이션으로 인해 가격 인하 압박이 커지며 정부가 가격 협상에 개입할 가능성이 존재합니다.
- side_c: `weak` ↓ — `Tving` 은 `Wavve` 합병 후 통합 비용을 절감 중이지만, 현금 흐름 부족과 구독 이탈율이 높아져 향후 시장 주도권 확보 과정에서 외부 자본 의존도 증가 및 규제 승인 지연 위험이 상존합니다.

#### Adjudicator synthesis

> Coupang Play 는 T1 의 라이브 스포츠 독점과 T2 의 Rocket Wow 통합을 통해 물류 및 데이터 인프라를 구독 유지의 핵심 자산으로 전환하며, 규제 리스크에도 불구하고 시장 지배력을 공고히 했습니다. Netflix Korea 는 T1 과 T2 의 Ad-Tier 최적화로 안정적인 현금 흐름을 확보한 뒤, 글로벌 인프라를 활용해 제작비 인플레이션을 관리하며 콘텐츠 경쟁력을 확장했습니다. 반면 Tving 은 T1 의 KBO 시즌과 T2 의 문화 IP 우위를 바탕으로 유입을 늘렸으나, Wavve 통합 후에도 현금 소진과 낮은 자본 효율성으로 인해 외부 자본 의존도가 높아지며 시장 주도권을 잃었습니다.

**Interaction analysis:** Coupang Play 의 생태계 연동 전략과 Netflix 의 글로벌 인프라 활용이 시장 양극화를 심화시키며, Tving 은 자본 효율성 부족으로 인해 양측의 압력 사이에서 고립되었습니다. 특히 Coupang Play 의 Rocket Wow 통합이 규제 감시 대상이 되면서 시장 진입 장벽이 높아진 반면, Tving 은 내부 구조 조정 실패로 인해 이러한 장벽을 넘지 못했습니다.

---

<a id="turn-4"></a>
## Turn 4

**Events fired:** OTT 콘텐츠 과세안 도입 논의, 글로벌 OTT 플랫폼 통합 가속화

### **Coupang Play** (side_a)

- Final action: `Rocket Wow Integration`@0.80
- Position: `dominant` ↗
- Cash: 50.9%
- Adjudicator rationale: 로켓와우 멤버십과의 생태계 통합이 콘텐츠 부족을 상쇄하며 신규 유입을 주도하고 있어 시장 지배력을 공고히 하고 있습니다.

##### Phase 1 — 독립 제안

- **CMO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Churn Prevention Campaign`@0.20
  - rationale: 보드 mandates(신규 고비용 콘텐츠 중단) 와 CEO의 쿠팡 KPI 동조 성향을 반영, 로켓와우 통합을 통한 유입 확보와 데이터 기반 수익화로 현금을 보존하며 넷플릭스 가격 인상 공세를 타겟팅한다.
  - risk: 콘텐츠 투자 지연으로 장기적 오리지널 가치 하락 및 넷플릭스 '오징어게임 시즌 3'에 대한 대응력 약화
- **COO**: `Rocket Wow Integration`@0.40, `Data Monetization Boost`@0.40, `Churn Prevention Campaign`@0.20
  - rationale: 보드 manda te 에 따른 고비용 콘텐츠 투자 전면 중단 명령을 준수하면서도, CEO 의 'MAU 우선' 및 '로켓와우 통합 과신' 편향을 반영하여 저비용 고효율 액션을 선택함. 넷플릭스의 가격 인상을 기회로 삼아 기존 회원 이탈 방지 및 신규 유입에 집중함으로써, 전략적 정체기인 현재 시점에서 가장 실행 가능한 방어-공격 전술임.
  - risk: 고비용 콘텐츠 투자 중단과 MAU 중심 경영 간 모순 심화, 현금 소모 가속화 가능성
- **CFO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Ad-Tier Optimization`@0.20
  - rationale: 보드 mandate(고비용 콘텐츠 투자 중단, 현금 보존) 에 따라 신규 라이선스 예산을 배제하고, 현재 보유한 1000 만 명 로켓와우 기반의 e-commerce 시너지 (Data Monetization) 와 기존 멤버십 통합 (Rocket Wow Integration) 을 통해 ARPU 를 극대화하는 것이 현금 흐름 확보에 가장 효율적입니다. 넷플릭스의 가격 인상과 오리지널 확장 공격에는 단순 구독료 경쟁보다는 쿠팡 생태계 내에서의 높은 전환율과 데이터 기반 광고 수익 모델이 유일한 방어선입니다.
  - risk: 콘텐츠 투자 중단으로 인한 장기적 MAU 성장 둔화 가능성
- **CTO**: `Rocket Wow Integration`@0.40, `Data Monetization Boost`@0.35, `Tech Infrastructure Upgrade`@0.25
  - rationale: 넷플릭스의 가격 인상과 원작 콘텐츠 확대에 맞서, 'Sports + 멤버십 끼워팔기' 전략의 핵심인 로켓와우 통합 효과를 극대화하고, 쿠팡의 이커머스 데이터를 활용한 고단가 광고 수익 (ARPU) 을 창출하는 것이 가장 합리적입니다. 특히 CEO 의 'MAU 우선' 성향을 반영하여 Rocket Wow Integration 을 최우선으로 배치하되, CTO 관점에서 R&D(기술 인프라) 투자를 동시 수행하여 단순 마케팅 의존도를 낮추고 장기적인 플랫폼 안정성을 확보합니다. 이는 Board 의 '신규 고비용 콘텐츠 투자 중단' 지시를 준수하면서도, 기존 자산을 효율화하여 차별화된 공격을 펼치는 방안입니다.
  - risk: R&D 예산 50% 유지 필요성 vs 단기 매출 증대 압박 간 균형 실패 시 기술적 경쟁력 약화
- **CEO**: `Ecosystem Bundle Push`@0.40, `Live Sports Exclusive`@0.30, `Data Monetization Boost`@0.30
  - rationale: 보드 미션의 고비용 중단 수용하며, 와우 통합 효과 정량적 증명이 핵심임. 넷플릭스 가격 인상 격차 활용, 티빙 데이터 약점 공격
  - risk: 단기 콘텐츠 감소로 시청 질 저하 우려 발생 가능

##### Phase 2 — 비판적 검토 (다수안: `Data Monetization Boost`, DA: `CTO`)

- **CFO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Ad-Tier Optimization`@0.20
- **CMO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Ad-Tier Optimization`@0.20
  - changed `Churn Prevention Campaign` → because: 수동 방어보다 광고 수익화 집중
- **COO**: `Rocket Wow Integration`@0.45, `Data Monetization Boost`@0.35, `Ad-Tier Optimization`@0.20
  - changed `Live Sports Exclusive` → because: 지시사항 위반, 고비용 중단 필요
- **CTO**: `Tech Infrastructure Upgrade`@0.60
  - dissent: 데이터 수익화 증대 방안은 단기적인 ARPU 상승에는 도움이 되지만, 핵심 경쟁력인 기술적 안정성을 약화시킬 우려가 있습니다. 사용자 경험 (UX) 이 떨어지면 콘텐츠와 상관없이 이탈률이 증가하며, 이는 경쟁사인 Netflix Korea 나 Tving 에 대한 실질적인 방어벽 역할을 하지 못합니다. 또한 현재 R&D 비중 50% 를 유지하는 것이 필수적인데, 데이터 판매 중심의 예산 편성은 실제 엔지니어링 자원 분배를 저해하여 장기적인 기술 우위를 훼손합니다. 2~3 년 내 경쟁력이 하락할 수 있는 리스크를 감당할 수 없습니다. 단순한 데이터 팔로는 플랫폼 본질인 미디어 경험을 대체할 수 없습니다. 기술적 성능이 뒷받침되지 않는 마케팅 활동은 유입된 트래픽을 충만한 전환율로 연결하지 못할 것입니다. 결국 사용자는 끊김 없는 서비스를 제공하는 플랫폼으로 이동합니다. 이는 우리의 지속 가능성을 위협하는 근본적인 문제입니다. 따라서 단순 데이터 상품 확대보다는 기술적 경쟁력을 선제적으로 확보해야 합니다.
- **CEO**: `Rocket Wow Integration`@0.50, `Ecosystem Bundle Push`@0.30, `Data Monetization Boost`@0.20
  - changed `Ecosystem Bundle Push, Live Sports Exclusive, Data Monetization Boost` → because: 고비용 중단, 로켓와우 집중

**Position changes:**
- CMO: Churn Prevention Campaign → Rocket Wow Integration+Data Monetization Boost+Ad-Tier Optimization (수동 방어보다 광고 수익화 집중)
- COO: Live Sports Exclusive → Rocket Wow Integration+Data Monetization Boost+Ad-Tier Optimization (지시사항 위반, 고비용 중단 필요)
- [반대] CTO: 데이터 수익화 증대 방안은 단기적인 ARPU 상승에는 도움이 되지만, 핵심 경쟁력인 기술적 안정성을 약화시킬 우려가 있습니다. 사용자 경험 (UX) 이 떨어지면 콘텐츠와 상관없이 이탈률이 증가하며, 이는 경쟁사인 Netflix Korea 나 Tving 에 대한 실질적인 방어벽 역할을 하지 못합니다. 또한 현재 R&D 비중 50% 를 유지하는 것이 필수적인데, 데이터 판매 중심의 예산 편성은 실제 엔지니어링 자원 분배를 저해하여 장기적인 기술 우위를 훼손합니다. 2~3 년 내 경쟁력이 하락할 수 있는 리스크를 감당할 수 없습니다. 단순한 데이터 팔로는 플랫폼 본질인 미디어 경험을 대체할 수 없습니다. 기술적 성능이 뒷받침되지 않는 마케팅 활동은 유입된 트래픽을 충만한 전환율로 연결하지 못할 것입니다. 결국 사용자는 끊김 없는 서비스를 제공하는 플랫폼으로 이동합니다. 이는 우리의 지속 가능성을 위협하는 근본적인 문제입니다. 따라서 단순 데이터 상품 확대보다는 기술적 경쟁력을 선제적으로 확보해야 합니다.
- CEO: Ecosystem Bundle Push, Live Sports Exclusive, Data Monetization Boost → Rocket Wow Integration+Ecosystem Bundle Push+Data Monetization Boost (고비용 중단, 로켓와우 집중)

##### Phase 3 — CEO 종합

**Decision:** 로켓와우 연동으로 신규 유입 확대 및 유지; Coupang Play 등 기존 혜택과 OTT 결합 강화; 쇼핑 시청 데이터 합쳐 광고 매출 최적화

**Reasoning:** 고비용 콘텐츠 투자 중단하며 통합 성과 입증; 이커머스 시너지로 순차적 전환율 제고; 현금 보존 하면서 ARPU 극대화 위한 핵심

### Netflix Korea (side_b)

- Final action: `Original Library Expansion`@0.80
- Position: `dominant` ↗
- Cash: 62.6%
- Adjudicator rationale: 글로벌 자금력과 광고 tiers 안정화로 세제 부담을 소화할 유동성을 확보하며 프리미엄 광고 인프라를 통해 지배적 지위를 유지하고 있습니다.

##### Phase 1 — 독립 제안

- **CTO**: `Ad-Tier Optimization`@0.45, `Original Library Expansion`@0.35, `Tech Infrastructure Upgrade`@0.20
  - rationale: 쿠팡플레이의 Rocket Wow Integration 이후 시장 장벽이 완성됨에 따라, 단순 가격 경쟁보다는 '저예산 고효율 장르'와 '추천 알고리즘'을 통한 구독 피로도 해소가 시급함. 글로벌 본사의 KPI(ARPU) 요구에 부응하며, 스포츠 권리 부재를 콘텐츠 다각화로 상쇄하는 전략적 대응.
  - risk: 글로벌 본사의 절대적 투자 규모 압박으로 인해 데이터 효율성보다 대형 콘텐츠 편중 재발 가능성
- **CFO**: `Original Library Expansion`@0.55, `Churn Prevention Campaign`@0.30, `Global Hit Investment`@0.15
  - rationale: 쿠팡플레이의 로켓와우 통합으로 시장 장벽이 완성됨에 따라, 저예산 고효율 장르 (로맨스/리얼리티) 를 통해 ARPU 회복과 구독 피로도 해소를 동시에 달성해야 함. 특히 쿠팡플레이의 우위 선점 전략에 대응하기 위해 특정 장르 투자를 20% 이상 조정하는 보드 지시를 이행함. 단, 리더십의 '한국 콘텐츠 1조 투자 narrative'와 '글로벌 hit 의존' 편향을 반영하여 예산의 일부는 여전히 대규모 글로벌 오리지널에 할당하되, 핵심은 데이터 기반 효율성 확보에 둠.
  - risk: 고비용 대형 콘텐츠 축소 시 단기 브랜드 이미지 하락 가능성 및 글로벌 본사의 투자 규모 압박으로 인한 내부 갈등 발생
- **COO**: `Original Library Expansion`@0.55, `Ad-Tier Optimization`@0.30, `Global Hit Investment`@0.15
  - rationale: 쿠팡플레이의 로켓와우 통합으로 인한 시장 장벽 강화에 대응해, 저예산 고효율 장르 (로맨스/리얼리티) 와 광고 tier 최적화로 ARPU 회복을 도모하되, 글로벌 본사의 '1조 투자' 서사 유지 압박과 한국 시장 특수성 간 괴리를 반영해 일부 거대 투자를 병행함. 이는 과도한 동시 추진을 피하면서도 리더십의 편향을 수용한 실행 가능성 중심의 배분임.
  - risk: 초거대 투자로 인한 현금 흐름 압박 및 ROI 미달 리스크
- **CMO**: `Original Library Expansion`@0.60, `Global Hit Investment`@0.30, `Churn Prevention Campaign`@0.10
  - rationale: 시점 (Turn 4) 에서 쿠팡플레이는 Rocket Wow 통합으로 우위를 점하며 시장 장벽을 완성했으므로, 단순 가격 경쟁이나 소규모 투자로는 방어 불가. 본사의 '한국 콘텐츠 1 조 투자' 서브와 '글로벌 M&A 가속화' 리스크를 고려해, 캠페인 방향인 '저예산 고효율 장르 다각화'를 핵심 (60%) 으로 하되, 리더십의 '절대 투자 규모' 편향과 '글로벌 히트 의존' 성향을 반영해 고비용 대형 콘텐츠 투자 (30%) 를 병행하여 브랜드 위상 유지. 이는 쿠팡플레이의 상승세를 막기 위한 방어적 lock-in 전략이며, 기존 인기 콘텐츠 재가공 (10%) 을 통해 구독 피로도를 해소함.
  - risk: 대형 콘텐츠 투자 비중 유지를 위해 저예산 고효율 장르 예산이 부족할 수 있으며, 글로벌 본사의 '1 조 원 투자' 서브에 대한 정치적 압박으로 비효율적 고비용 프로젝트가 지속될 리스크 존재
- **CEO**: `Original Library Expansion`@0.50, `Global Hit Investment`@0.30, `Ad-Tier Optimization`@0.20
  - rationale: Q4 장르 조정 보장을 위해 원조 라이브러리 지분을 확실히 배정하였다. CEO 리더십 특성상 글로벌 히트 작 편입은 필수적인 서브 전략이며, 이는 KBO/EPL 부재를 메우는 간접적 수단이 된다. 쿠팡플레이에 대한 직접 비교보다는 아너 플랫폼 내부 효율화에 초점을 맞추어 예산 균형을 맞춘다.
  - risk: 제작비 인플레이션 및 초기 ROI 지연

##### Phase 2 — 비판적 검토 (다수안: `Original Library Expansion`, DA: `CFO`)

- **COO**: `Original Library Expansion`@0.60, `Ad-Tier Optimization`@0.25, `Churn Prevention Campaign`@0.15
  - changed `Global Hit Investment` → because: 현금 리스크 및 과투자 방지
- **CTO**: `Tech Infrastructure Upgrade`@0.45, `Original Library Expansion`@0.35, `Ad-Tier Optimization`@0.20
- **CMO**: `Original Library Expansion`@0.65, `Global Hit Investment`@0.25, `Churn Prevention Campaign`@0.10
  - changed `Original Library Expansion` → because: 보수적 장르 축소 불가, 본사 압력 반영
- **CEO**: `Original Library Expansion`@0.50, `Ad-Tier Optimization`@0.30, `Global Hit Investment`@0.20
  - changed `Original Library Expansion` → because: 원본 재가공 및 저예산 집중
- **CFO**: `Ad-Tier Optimization`@0.50, `Churn Prevention Campaign`@0.30, `Premium Content Acquisition`@0.20
  - dissent: 과잉 원본 제작 비용은 쿠팡플레이의 지속 가능성을 위협합니다. 다수안은 특정 장르별 20% 이상 조정이라는 사내 지침을 충족하지 못하며, 고정비 증가를 통해 현금 소모를 가속화하는 구조입니다. 쿠팡플레이의 현재 주도권을 유지하려면 신중한 투자보다 수익성 있는 자원 배분이 우선되어야 합니다. 특히 넷플릭스 코리아 등 시장 상황에 대응할 유동성이 확보되지 않으면 중기적으로 성장 잠재력이 제한됩니다. 이 전략은 재정의된 장르 투자 목표를 반영하지 않은 채 대규모 예산을 사용하는 것이므로 반대합니다. 또한 글로벌 본사의 투자 압박보다는 내부 재무 건전성을 유지하는 것이 생존에 필수적입니다. 콘텐츠 품질과 플랫폼 안정성을 강조하는 장기 브랜드 이미지 캠페인도 필요하지만, 즉각적인 현금 흐름 개선을 위한 조치를 병행해야 합니다. 이를 통해 운영 효율성을 높이고, 향후 선택적 투자를 위한 자본 여유를 확보할 수 있습니다. 단순히 라이브러리를 늘리는 것보다 기존 회원을 유지하고 수익 모델을 다양화

**Position changes:**
- COO: Global Hit Investment → Original Library Expansion+Ad-Tier Optimization+Churn Prevention Campaign (현금 리스크 및 과투자 방지)
- CMO: Original Library Expansion → Original Library Expansion+Global Hit Investment+Churn Prevention Campaign (보수적 장르 축소 불가, 본사 압력 반영)
- CEO: Original Library Expansion → Original Library Expansion+Ad-Tier Optimization+Global Hit Investment (원본 재가공 및 저예산 집중)
- [반대] CFO: 과잉 원본 제작 비용은 쿠팡플레이의 지속 가능성을 위협합니다. 다수안은 특정 장르별 20% 이상 조정이라는 사내 지침을 충족하지 못하며, 고정비 증가를 통해 현금 소모를 가속화하는 구조입니다. 쿠팡플레이의 현재 주도권을 유지하려면 신중한 투자보다 수익성 있는 자원 배분이 우선되어야 합니다. 특히 넷플릭스 코리아 등 시장 상황에 대응할 유동성이 확보되지 않으면 중기적으로 성장 잠재력이 제한됩니다. 이 전략은 재정의된 장르 투자 목표를 반영하지 않은 채 대규모 예산을 사용하는 것이므로 반대합니다. 또한 글로벌 본사의 투자 압박보다는 내부 재무 건전성을 유지하는 것이 생존에 필수적입니다. 콘텐츠 품질과 플랫폼 안정성을 강조하는 장기 브랜드 이미지 캠페인도 필요하지만, 즉각적인 현금 흐름 개선을 위한 조치를 병행해야 합니다. 이를 통해 운영 효율성을 높이고, 향후 선택적 투자를 위한 자본 여유를 확보할 수 있습니다. 단순히 라이브러리를 늘리는 것보다 기존 회원을 유지하고 수익 모델을 다양화

##### Phase 3 — CEO 종합

**Decision:** 저비용 로맨틱 장르 확대 및 라인업 강화; 광고 tiers 확대로 매출 및 아루피 동시 증대

**Reasoning:** 장르기 투자 20% 조정 목표 달성 및 투자 서브시션 확보; 본사 실적 지표 우선시하여 현금 흐름 안정화

### Tving (side_c)

- Final action: `Premium Content Acquisition`@0.80
- Position: `weak` ↓
- Cash: 7.8%
- Adjudicator rationale: 과도한 현금 소모와 글로벌 표준 미흡으로 인해 구조적 생존 리스크가 가장 크며, 단기 이벤트 효과만으로는 자금 압박을 해결할 수 없습니다.

##### Phase 1 — 독립 제안

- **CTO**: `KBO Season Spike`@0.50, `Naver Plus Synergy`@0.30, `Tech Infrastructure Upgrade`@0.20
  - rationale: CEO 의 보수적 Capex 관점과 CJ ENM 모회사 정치 (KBO 중계권 사수) 를 반영하여 단기 트래픽 방어에 집중합니다. 하지만 본 CTO 의 입장에서 R&D 투자 (50%) 가 부족해 2-3 년 내 기술 격차가 벌어질 수 있음을 경고하며, 기존 캠페인 실행을 위한 최소한의 인프라 개선만 수행합니다.
  - risk: R&D 예산 부족으로 장기적 기술 경쟁력 약화 및 이탈 가속
- **COO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Wavve Integration Cost Cut`@0.20
  - rationale: CEO 의 모회사 정치 편향 (Wavve 합병 매몰 비용 인식 거부) 과 콘텐츠 소싱 강점을 반영하여 야구 시즌과 네이버 연동을 우선시함. 보드 지시의 'Coupang Play 대응을 위한 오리지널 예산 50%'는 현금 부족으로 즉시 실행 불가능하므로, 기존 자산(KBO/네이버) 을 활용한 저비용 고효율 전략으로 우회적 대응.
  - risk: 과도한 KBO 투자로 현금 19% 위험, Wavve 비효율 지속
- **CFO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Wavve Integration Cost Cut`@0.20
  - rationale: CEO의 CJ ENM 모회사 정치와 Wavve 매몰비용 인식 거부 편향을 반영하여, 현금 효율성이 낮은 'Wavve Integration Cost Cut'을 우선순위를 낮게 책정하고 대신 'KBO Season Spike'와 'Naver Plus Synergy'로 충성도 높은 스포츠 팬과 저비용 유입에 집중합니다. 이는 경쟁사 (Coupang Play) 의 로켓와우 통합에 맞서 스포츠 중계권을 핵심 차별화 포인트로 삼는 현재 캠페인을 실행하되, 현금 19%라는 제약 하에서 생존 가능한 최소한의 비용 구조를 유지하기 위함입니다.
  - risk: 현금 19% 소진 가속화 및 Wavve 통합 실패 리스크
- **CMO**: `KBO Season Spike`@0.45, `Cultural IP Dominance`@0.35, `Wavve Integration Cost Cut`@0.20
  - rationale: CEO 의 모회사 정치 (KBO 사수) 와 Wavve 매몰 비용 인식 거부 (IR narrative 훼손 우려) 라는 리더십 편향을 반영하여, 예산의 50% 를 확보하라는 보드 지시를 부분적으로 수용하면서도 기존 캠페인 (스포츠+지역 밀착) 을 실행합니다. KBO 와 JTBC 자산은 내부 정치적 리스크를 줄이면서 충성도 높은 사용자를 선점하는 핵심 수단입니다. 다만, '차별화된 오리지널 투자' 지시와 상충되는 Wavve 통합 비용 절감 (20%) 은 임원진의 조직적 관성을 고려해 최소한으로 포함시켰으나, 이는 현금 흐름 방어보다는 내부 정치 타협에 가깝습니다.
  - risk: 보수적 Capex 유지로 인해 현금 소진 속도 가속화 및 경쟁사 대응 지연 가능성
- **CEO**: `Wavve Integration Cost Cut`@0.30, `Cultural IP Dominance`@0.50, `Premium Content Acquisition`@0.20
  - rationale: ボード mandates 에 따라 Wavve 통합 비용 절감 전략 즉시 중단 (0.3) 후 잔여 예산의 대부분을 CJ ENM/JTBC 자산 기반 차별화 오리지널 콘텐츠에 집중 (0.7). 기존 KBO 중계권 유지 정치 비용은 무시하고 브랜드 모방 방어 강화.
  - risk: 콘텐츠 투자가 예상보다 낮은 반응을 보일 경우 현금 소진 가속화 및 추가 구조조정 압력

##### Phase 2 — 비판적 검토 (다수안: `KBO Season Spike`, DA: `CFO`)

- **CTO**: `KBO Season Spike`@0.45, `Tech Infrastructure Upgrade`@0.35, `Naver Plus Synergy`@0.20
  - changed `CTO` → because: R&D 비중 확대, Wavve 비용 절감 반대
- **COO**: `KBO Season Spike`@0.45, `Naver Plus Synergy`@0.35, `Cultural IP Dominance`@0.20
  - changed `Wavve Integration Cost Cut` → because: 보드 지시 즉시 중단
- **CMO**: `Cultural IP Dominance`@0.55, `KBO Season Spike`@0.35, `Wavve Integration Cost Cut`@0.10
  - changed `KBO Season Spike, Cultural IP Dominance, Wavve Integration Cost Cut` → because: 보안 예산 확보 및 콘텐츠 모호성 제거
- **CFO**: `Premium Content Acquisition`@0.50, `Ad-Tier Optimization`@0.30, `Churn Prevention Campaign`@0.20
  - dissent: 19% 현금 보유 상태에서 KBO 시즌 등 단기 이벤트성 스파이크는 자산을 축적하지 못하고 재고를 고갈시킵니다. 팀 제안안은 이커머스 연동이나 운영 효율화를 통한 '비용 절감' 위주로 구성되어 있으나, 보드 지시는 통합 비용 절감 전략의 '중단'과 콘텐츠 투자 50% 확보입니다. 이를 무시하는 것은 자금 여력 허비를 의미하며, 전략적 정체와 현금 위험 신호인 현재 상황을 악화시킵니다. 단기간의 트래픽 상승은 브랜드 충성도로 직결되지 않아 지속 가능한 성장 경로를 제공하지 못합니다. 오히려 현금 소진 속도가 빨라져 금융 리스크가 급증할 가능성이 높습니다. 차별화된 콘텐츠 자산 구축이 생존을 위한 필수 조건입니다. Wavve 통합 비용 절감 대신 해당 자원을 본질적인 제품 혁신과 콘텐츠 품질 향상에 투입하여 장기 수익성을 담보해야 합니다. 이는 단순 마케팅 캠페인이 아닌 사업의 기본기를 다지는 행위입니다. KBO 투자는 계절적 요인에 의한 변수로 남았을 뿐, 구조적 경쟁력을 개선하지는못
- **CEO**: `Premium Content Acquisition`@0.50, `Naver Plus Synergy`@0.30, `KBO Season Spike`@0.20
  - changed `Wavve Integration Cost Cut` → because: Wavve 배제 콘텐츠 확보

**Position changes:**
- COO: Wavve Integration Cost Cut → KBO Season Spike+Naver Plus Synergy+Cultural IP Dominance (보드 지시 즉시 중단)
- CMO: KBO Season Spike, Cultural IP Dominance, Wavve Integration Cost Cut → Cultural IP Dominance+KBO Season Spike+Wavve Integration Cost Cut (보안 예산 확보 및 콘텐츠 모호성 제거)
- [반대] CFO: 19% 현금 보유 상태에서 KBO 시즌 등 단기 이벤트성 스파이크는 자산을 축적하지 못하고 재고를 고갈시킵니다. 팀 제안안은 이커머스 연동이나 운영 효율화를 통한 '비용 절감' 위주로 구성되어 있으나, 보드 지시는 통합 비용 절감 전략의 '중단'과 콘텐츠 투자 50% 확보입니다. 이를 무시하는 것은 자금 여력 허비를 의미하며, 전략적 정체와 현금 위험 신호인 현재 상황을 악화시킵니다. 단기간의 트래픽 상승은 브랜드 충성도로 직결되지 않아 지속 가능한 성장 경로를 제공하지 못합니다. 오히려 현금 소진 속도가 빨라져 금융 리스크가 급증할 가능성이 높습니다. 차별화된 콘텐츠 자산 구축이 생존을 위한 필수 조건입니다. Wavve 통합 비용 절감 대신 해당 자원을 본질적인 제품 혁신과 콘텐츠 품질 향상에 투입하여 장기 수익성을 담보해야 합니다. 이는 단순 마케팅 캠페인이 아닌 사업의 기본기를 다지는 행위입니다. KBO 투자는 계절적 요인에 의한 변수로 남았을 뿐, 구조적 경쟁력을 개선하지는못
- CEO: Wavve Integration Cost Cut → Premium Content Acquisition+Naver Plus Synergy+KBO Season Spike (Wavve 배제 콘텐츠 확보)

##### Phase 3 — CEO 종합

**Decision:** 차별 콘텐츠 집중 투자; 야구 시즌 집중 마케팅

**Reasoning:** 보드 지시 반영 및 현금 확보; 지역 밀착형 팬 유입 확보

#### Adjudicator panel (3 experts)

**Regulatory/Policy Expert**: 국회 상정된 OTT 과세안이 글로벌 기업인 Netflix Korea 에 직접 타격을 주며, 이는 국내 지분율 높은 Coupang Play 와 Tving 에게 비교 우위를 부여하는 구조적 변수가 됩니다.

- side_a: `dominant` ↑ — 로켓와우 멤버십과의 강인한 생태계 결합으로 신규 유입을 주도하며 시장 지배력을 공고히 하였으나 데이터 활용에 대한 반독점 감시가 강화될 가능성이 높습니다.
- side_b: `dominant` ↗ — 글로벌 자금력과 광고 tiers 안정화로 새로 추가되는 세제 부담을 소화해낼 유동성이 확보되어 있지만 한국 내 독자적 제작비 인상은 수익성 완충 요인이 될 것입니다.
- side_c: `weak` ↓ — KBO 시즌 이벤트로 일시적인 관심도는 얻을 수 있으나 과도한 현금 소모와 글로벌 표준 미흡으로 장기적인 규제 대응 능력과 생존 리스크가 가장 큽니다.

**Industry Veteran**: OTT 생태계는 이제 단발성 콘텐츠보다 데이터 시너지를 갖춘 통합 멤버십과 현금 흐름 지속 가능성이 차별화 요소로 부상 중

- side_a: `dominant` ↗ — 로켓와우 매핑이 라이브 스포츠 및 쇼핑 연계 효과를 극대화하여 콘텐츠 풀 부족도 상쇄하며 시장 지배력을 공고히 함
- side_b: `dominant` ↗ — 글로벌 오리지널 히트작과 프리미엄 광고 인프라가 재무 건전성을 보장하며 가격 민감도와 충성도 사이 균형을 유지
- side_c: `marginal` ↓ — 현금 보유량 고갈 우려가 야구 시즌 집중 마케팅 효과보다 우선하며 구조적 생존 위험에 직면했음

**Strategy Consultant**: 플랫폼 업계에서의 생존은 이제 콘텐츠 경쟁뿐만 아니라 현금 흐름의 탄력성과 규제 대응 능력을 동시에 확보하느냐에 달려 있다. 따라서 자본 규모가 작을수록 외부 충격에 대한 방어선이 취약해질 수밖에 없다.

- side_a: `dominant` ↗ — Coupang Play 는 Rocket Wow 와의 통합 효과를 활용해 콘텐츠 단점을 보완하며 시장 선점 우위를 더욱 견고하게 다진다.
- side_b: `dominant` ↗ — Netflix Korea 는 충분한 현금 보유력과 글로벌 아카이브 운영으로 마케팅 비용 대비 효과를 극대화하여 지배적 지위를 유지한다.
- side_c: `weak` ↓ — Tving 은 심각한 자금 압박 상황에서도 고비용 콘텐츠 확보에 나섰으나 이는 현금 고갈 속도를 높여 구조적 악순환을 초래한다.

#### Adjudicator synthesis

> T1부터 T3까지 지속된 제작비 인플레이션과 구독 피로도는 모든 플랫폼에 부정적 영향을 미쳤으나, Coupang Play는 T2와 T3의 로켓와우 통합을 통해 콘텐츠 단점을 상쇄하며 시장 선점 우위를 더욱 견고하게 다졌습니다. 반면 Netflix Korea는 T3의 오리지널 라이브러리 확장으로 글로벌 아카이브와 프리미엄 광고 인프라를 결합하여 가격 민감도를 관리하며 지배적 지위를 유지했습니다. Tving은 T1의 KBO 시즌과 T2의 문화적 IP 공세에도 불구하고 T3의 비용 절감 노력이 늦게 시작되어 현금 고갈 속도가 빨라졌고, 이로 인해 구조적 생존 위험이 극대화되었습니다.

**Interaction analysis:** Coupang Play와 Netflix Korea는 각각 로켓와우 통합과 글로벌 자본력을 바탕으로 규제 환경 변화에도 불구하고 시장 지배력을 강화하는 반면, Tving은 고비용 콘텐츠 확보 전략이 현금 고갈을 가속화하며 경쟁사들과의 격차가 벌어지고 있습니다. 특히 제작비 인플레이션과 구독 이탈이라는 공통된 외부 충격 앞에서 자본력과 생태계 결합도가 높은 두 강자는 방어선을 유지하는 반면, 자본이 약한 Tving은 구조적 악순환에 빠지게 되었습니다.

---

<a id="turn-5"></a>
## Turn 5

**Events fired:** 한국 드라마 글로벌 바이럴 현상, 주요 IP 저작권 분쟁 발생

### **Coupang Play** (side_a)

- Final action: `Rocket Wow Integration`@0.90
- Position: `dominant` ↑
- Cash: 47.9%
- Adjudicator rationale: 로켓와우 통합과 MLB 독점 효과를 통해 생태계 잠금 효과가 극대화되어 시장 지배력을 더욱 공고히 하고 있습니다.

##### Phase 1 — 독립 제안

- **CTO**: `Tech Infrastructure Upgrade`@0.40, `Data Monetization Boost`@0.35, `Rocket Wow Integration`@0.25
  - rationale: 넷플릭스의 가격 인상과 글로벌 히트 콘텐츠 (오징어게임 시즌 3) 에 대한 사용자의 높은 기대감은 단순한 가격 경쟁이나 기존 스포츠 콘텐츠로는 방어 불가능합니다. CEO 의 'MAU 우선' 기조와 쿠팡의 이커머스 데이터를 활용한 수익 모델 (Ecosystem Bundle Push 캠페인) 을 실행하되, CTO 관점에서 핵심인 '기술적 차별화'를 위해 R&D 투자를 최우선으로 배정해야 합니다. 특히 MLB/EPL 중계와 같은 라이브 스포츠는 네트워크 안정성과 저지연 전송 기술 없이는 사용자 이탈을 막을 수 없습니다. 또한, 로켓와우 통합 효과를 극대화하기 위해서는 단순 가입자 수 증가가 아닌, 이커머스 데이터 기반의 정교한 개인화 추천 알고리즘 (Data Monetization) 이 뒷받침되어야 ARPU 증대와 churn 감소가 가능합니다. 이는 단순한 마케팅 전술이 아닌, 장기적인 기술적 해자 (Moat) 를 구축하는 필수 조치입니다.
  - risk: R&D 투자 지연 시 2-3 년 내 기술적 우위 상실 및 넷플릭스 라이브러리 확장 대응 불가
- **COO**: `Rocket Wow Integration`@0.40, `Data Monetization Boost`@0.35, `Ad-Tier Optimization`@0.25
  - rationale: 보드의 '전략 재사용 정체' 지적에 따라, 기존 캠페인(스포츠+멤버십)의 핵심 메커니즘인 '로켓와우 통합'을 최우선으로 강화하여 넷플릭스의 가격 인상 공세를 방어한다. 동시에 콘텐츠 투자 (Global Hit Investment 등) 를 보류하고, 확보된 MAU를 즉시 현금화하는 '데이터 기반 광고'와 '광고 인벤토리 최적화'에 자원을 집중하여 현금 흐름 (Cash Flow) 을 개선한다. 이는 CEO 의 'MAU 우선' 편향과 '쿠팡 시너지' 믿음을 반영하되, Cash 49.9%라는 제약 하에서 단일 전략의 과도한 확장을 방지하기 위한 실행 가능성 중심의 선택이다.
  - risk: 과다한 동시 실행으로 인한 운영 리소스 과부하 및 ROI 지연
- **CMO**: `Ecosystem Bundle Push`@0.45, `Live Sports Exclusive`@0.35, `Data Monetization Boost`@0.20
  - rationale: 보드는 '로켓와우 통합 효과 분석 후 넷플릭스 추격 전략 전환'을 명했다. 기존 스포츠 유입 전략은 성장이 정체되었으나, 넷플릭스의 가격 인상 (베이직 7,900원) 과 오징어게임 시즌 3 기대감은 우리에 대한 유일한 기회다. CEO의 'MAU 우선'과 '가격 인상에 대한 Retail KPI 우려'라는 편향을 반영하여, 경쟁사가 가격을 올리는 시점에 로켓와우 멤버십 가격을 동결하고 쿠팡 배송권을 강화하는 '생존형 번들'로 방어선을 구축한다. 이는 단순한 가격 경쟁이 아닌, 이커머스 생태계(LTV)와의 결합을 통해 넷플릭스가 모방할 수 없는 '고비용 진입 장벽'을 만든다. Tving의 약세를 공략하기 위한 별도 공격보다는, 넷플릭스의 가격 민감 계층을 흡수하는 '공격적 방어'가 핵심이다.
  - risk: 넷플릭스 가격 인상으로 인한 프리미엄 콘텐츠 이탈 가속화 가능성
- **CFO**: `Data Monetization Boost`@0.55, `Ad-Tier Optimization`@0.30, `Rocket Wow Integration`@0.15
  - rationale: 보arded mandate 에 따라 '로켓와우 통합 효과 분석' 후 넷플릭스 추격 전략 전환이 필요함. 현재 현금 보유량 49.9% 로 낮아 고위험의 'Global Hit Investment' 는 배제하고, 기존 생태계 (이커머스) 를 활용한 즉각적인 현금 흐름 창출에 집중함. 리더십의 편향 (MAU 우선, 가격 동결 고집) 을 반영하여 Rocket Wow Integration 을 통해 신규 유입을 극대화하되, 수익성은 데이터 기반 고단가 광고 (Data Monetization) 로 흡수하는 구조를 취함. 넷플릭스의 가격 인상은 저가 광고 tier 수요를 늘려 우리 Ad-Tier Optimization 의 효과를 증폭시킴.
  - risk: 넷플릭스 가격 인상과 오징어게임 시즌 3 방영으로 인한 프리미엄 콘텐츠 유출 위험 (Cash burn 증가)
- **CEO**: `Live Sports Exclusive`@0.50, `Rocket Wow Integration`@0.30, `Data Monetization Boost`@0.20
  - rationale: Turn 4 정체 해소를 위해 순수 콘텐츠 대항 전략은 변경합니다. Netflix Korea 의 가격 인상기에 대비해 쿠팡 Play 의 가격 동결로 시장 침투율을 유지하되, 라이브러리 싸움은 피합니다. Tving 는 KBO 시즌 소모전에서 약세이므로 글로벌 스포츠 권리로 선점합니다. Rocket WOW 통합 효과 분석 결과를 활용해 시청 행동만 강조하던 전략에서 쇼핑몰 구매 데이터까지 연결해 광고 단가 (ARPU) 상향에 주력합니다. 이는 이사회가 요구한 즉시적 전략 전환과 CEO 의 로켓와우 과신 성향을 모두 반영합니다.
  - risk: 높은 초기 라이선스 비용 및 단기 마진률 압박

##### Phase 2 — 비판적 검토 (다수안: `Data Monetization Boost`, DA: `CTO`)

- **CMO**: `Rocket Wow Integration`@0.45, `Live Sports Exclusive`@0.35, `Data Monetization Boost`@0.20
- **CFO**: `Data Monetization Boost`@0.50, `Ad-Tier Optimization`@0.30, `Rocket Wow Integration`@0.20
- **COO**: `Rocket Wow Integration`@0.60, `Ad-Tier Optimization`@0.40
  - changed `Live Sports Exclusive` → because: 동시 실행 과부하 방지 및 현금 보존
- **CEO**: `Live Sports Exclusive`@0.40, `Rocket Wow Integration`@0.45, `Ecosystem Bundle Push`@0.15
  - changed `CEO Proposal` → because: 와우효과분석후이커머스전환
- **CTO**: `Tech Infrastructure Upgrade`@1.00
  - dissent: 대안안은 단기적인 데이터 가치 추출에 집중하지만, 장기적인 플랫폼 안정성 확보에는 부족하다. 이는 로켓와우 통합 효과를 극대화하기 위한 기술적 기반을 간과하는 조치다. 데이터 상품을 확대하면 오히려 기존 인프라 과부하로 시스템 장애가 발생할 우려가 있다. 사용자가 서비스 속도에 민감하므로, 콘텐츠 소비 환경 자체의 안정성이 선행되지 않으면 매수율 회복에도 한계가 있을 것이다. 또한 현재 제안된 방향성은 넷플릭스가 보유하고 있는 레퍼런스 기술과의 격차를 좁히는 데 도움이 되지 않는다. 우리는 하드웨어 측면에서의 효율성과 소프트웨어 아키텍처 유연성을 먼저 점검해야 지속 가능한 성장을 꾀할 수 있다. 따라서 단순 데이터 판매보다는 전체적인 기술적 기반 확충이 우선이다.

**Position changes:**
- COO: Live Sports Exclusive → Rocket Wow Integration+Ad-Tier Optimization (동시 실행 과부하 방지 및 현금 보존)
- [반대] CTO: 대안안은 단기적인 데이터 가치 추출에 집중하지만, 장기적인 플랫폼 안정성 확보에는 부족하다. 이는 로켓와우 통합 효과를 극대화하기 위한 기술적 기반을 간과하는 조치다. 데이터 상품을 확대하면 오히려 기존 인프라 과부하로 시스템 장애가 발생할 우려가 있다. 사용자가 서비스 속도에 민감하므로, 콘텐츠 소비 환경 자체의 안정성이 선행되지 않으면 매수율 회복에도 한계가 있을 것이다. 또한 현재 제안된 방향성은 넷플릭스가 보유하고 있는 레퍼런스 기술과의 격차를 좁히는 데 도움이 되지 않는다. 우리는 하드웨어 측면에서의 효율성과 소프트웨어 아키텍처 유연성을 먼저 점검해야 지속 가능한 성장을 꾀할 수 있다. 따라서 단순 데이터 판매보다는 전체적인 기술적 기반 확충이 우선이다.

##### Phase 3 — CEO 종합

**Decision:** 로켓와우 통합 확대 및 신규 유입 가속; MLB 독점으로 Netflix 대비 차별화 유지; 이커머스 연계로 고객 생애 가치 증대

**Reasoning:** Coupang Play, Rocket Wow, KOREA 시장 선점; Live Sports, MLB, EPL, Korea 시장 견제; Tving 약점 공략, 쿠팡 시너지 창출

### Netflix Korea (side_b)

- Final action: `Ad-Tier Optimization`@0.80
- Position: `dominant` ↗
- Cash: 66.0%
- Adjudicator rationale: 광고 tiers 최적화와 글로벌 콘텐츠 헤리티지로 수익성을 개선하며 우위를 유지하고 있으나, 쿠팡플레이와의 격차는 좁혀지고 있습니다.

##### Phase 1 — 독립 제안

- **CTO**: `Original Library Expansion`@0.45, `Global Hit Investment`@0.35, `Ecosystem Bundle Push`@0.20
  - rationale: 보드가 지시한 예산 50% 삭감에도 불구하고, R&D 50% 유지를 통해 경쟁력 유지가 필수적입니다. 글로벌 본사의 '1 조 투자' 서브 Narrative 와 한국 시장 특수성 간 괴리를 해소하기 위해, 고비용 대형 콘텐츠 (Global Hit) 는 축소하되 전 세계적 성공 가능성이 높은 프로젝트는 우선 확보합니다. 동시에 쿠팡플레이의 쇼핑 연동 전략에 대응해 자체 커머스 모델을 도입하고, 저예산 고효율 장르를 확대하여 수익 다변화를 꾀합니다. 이는 보드의 비용 효율성 요구와 장기 기술 혁신 필요성을 절충한 전략입니다.
  - risk: 예산 삭감 요구로 인한 핵심 인재 이탈 및 콘텐츠 품질 저하 가능성
- **CMO**: `Original Library Expansion`@0.45, `Ecosystem Bundle Push`@0.35, `Global Hit Investment`@0.20
  - rationale: 보드 mandate 의 '저예산 고효율 장르'와 '라이프스타일 커머스' 전략을 실행하되, 글로벌 본사의 '1 조 원 투자 서사'와 한국 시장 가격 민감도 간 괴리를 반영하기 위해 고비용 대형 투자를 일부 병행합니다. 이는 쿠팡플레이의 물류-콘텐츠 통합 장벽에 대응하면서도 내부 정치적 요구를 충족시키는 방어적 접근입니다.
  - risk: 고비용 대형 콘텐츠의 ROI 미달로 예산 낭비 발생 시 브랜드 이미지 훼손
- **COO**: `Ad-Tier Optimization`@0.50, `Original Library Expansion`@0.30, `Churn Prevention Campaign`@0.20
  - rationale: 보드 미션인 '오리지널 제작비 50% 삭감'과 '비용 효율성'을 충족하기 위해, 고비용 대형 콘텐츠 대신 데이터 기반 저예산 장르로 포트폴리오를 전환함. 쿠팡플레이의 쇼핑 연동 강세에 대응해 자체 커머스 도입은 실행 리스크가 높아 이번 분기에는 기존 라이브러리 최적화 (ARPU 회복) 에 자원을 집중하되, 글로벌 본사의 '1 조 투자 서브' 압력을 반영해 일부 대형 프로젝트는 유지하며 균형 잡힌 실행 계획 수립.
  - risk: 글로벌 본사의 절대 투자 규모 압박으로 인해 저예산 전략이 예산 편성 시 축소될 수 있음
- **CFO**: `Original Library Expansion`@0.45, `Ecosystem Bundle Push`@0.35, `Global Hit Investment`@0.20
  - rationale: 보통 전략 반복으로 쿠팡플레이 점유율 추격 실패를 인정, 보드 지시대로 신규 오리지널 예산 50% 삭감(전체 포트폴리오 기준) 하되, '로맨스/리얼리티' 등 고효율 장르로 전환하여 비용 효율성 확보. 또한 쿠팡플레이의 쇼핑 연동 트렌드에 대응해 자체 커머스 모델 도입으로 수익원 다변화 추진. 단, 글로벌 본사의 '1조 투자' 내러티브와 한국 시장 가격 민감도 간 괴리를 반영, 리더십의 편향 (효율보다 규모 강조) 을 고려해 일부 대형 IP 투자는 유지하되 비중은 축소하여 리스크 관리.
  - risk: 대형 콘텐츠 ROI 불확실성 및 현금 소진 가속화
- **CEO**: `Ad-Tier Optimization`@0.40, `Churn Prevention Campaign`@0.30, `Ecosystem Bundle Push`@0.30
  - rationale: 보통 투자 예산 삭감 mandate 수용하고, ARPU 회복과 리테이션을 통한 지수적 성장은 Coupang Play 등 경쟁사 대비 차별화 가능
  - risk: 광고 인벤토리 부족 및 커머스 전환 지연

##### Phase 2 — 비판적 검토 (다수안: `Original Library Expansion`, DA: `CFO`)

- **CMO**: `Original Library Expansion`@0.45, `Ecosystem Bundle Push`@0.35, `Ad-Tier Optimization`@0.20
  - changed `Global Hit Investment` → because: 예산 삭감 mandates 에 따른 대형 투자 축소
- **COO**: `Ad-Tier Optimization`@0.50, `Churn Prevention Campaign`@0.30, `Original Library Expansion`@0.20
- **CTO**: `Original Library Expansion`@0.45, `Tech Infrastructure Upgrade`@0.35, `Global Hit Investment`@0.20
  - changed `CTO: Original Library Expansion, Global Hit Investment, Ecosystem Bundle Push` → because: R&D 50% 미달 시 경쟁력 붕괴, 비용절감 반대
- **CFO**: `Ad-Tier Optimization`@0.30, `Churn Prevention Campaign`@0.30, `Ecosystem Bundle Push`@0.25
  - dissent: 팀 대다수안이 제시하는 신규 오리지널 제작 확대는 현금 잔고 65% 상태에서의 고갈 리스크를 초래하며, 보드에서 지정한 신규 오리지널 예산 50% 삭감 지시와 직접적으로 충돌합니다. 높은 제작비에 비해 ROI 불확실성이 큰 전략으로 인해 재무 건전성을 훼손할 우려가 큽니다. 또한 글로벌 히트 베팅은 단기 현금 흐름에 부정적 영향을 미칩니다. 넷플릭스 코리아와의 격차를 좁히기 위해선 단순 규모 확장보다 효율성 위주의 운영 전환이 필요합니다. 티빙과 같은 경쟁사 대비 차별화보다는 현금이 되는 사업 모델로의 재정비가 시급합니다. 대기업 간 경쟁에서 지속 가능성은 생존의 필수 조건입니다. 우리는 쿠팡 플레이로서 자본 손실을 최소화해야 합니다. 단순히 콘텐츠를 늘리는 것만으로는 마켓 리더가 될 수 없습니다. 오히려 비용 구조 최적화가 선행되어야 합니다. 기술 인프라 업그레이드는 부차적이지만 중요하므로 일부 포함시켰습니다. 규제 준수 변경은 필요하지만 우선순위는 아닙니다. 인재 스캔들 저지는당
- **CEO**: `Ad-Tier Optimization`@0.50, `Churn Prevention Campaign`@0.30, `Ecosystem Bundle Push`@0.20
  - changed `기기제안서` → because: 보드 지시 준수 및 수익 최적화

**Position changes:**
- CMO: Global Hit Investment → Original Library Expansion+Ecosystem Bundle Push+Ad-Tier Optimization (예산 삭감 mandates 에 따른 대형 투자 축소)
- CTO: Original Library Expansion, Global Hit Investment, Ecosystem Bundle Push → Original Library Expansion+Tech Infrastructure Upgrade+Global Hit Investment (R&D 50% 미달 시 경쟁력 붕괴, 비용절감 반대)
- [반대] CFO: 팀 대다수안이 제시하는 신규 오리지널 제작 확대는 현금 잔고 65% 상태에서의 고갈 리스크를 초래하며, 보드에서 지정한 신규 오리지널 예산 50% 삭감 지시와 직접적으로 충돌합니다. 높은 제작비에 비해 ROI 불확실성이 큰 전략으로 인해 재무 건전성을 훼손할 우려가 큽니다. 또한 글로벌 히트 베팅은 단기 현금 흐름에 부정적 영향을 미칩니다. 넷플릭스 코리아와의 격차를 좁히기 위해선 단순 규모 확장보다 효율성 위주의 운영 전환이 필요합니다. 티빙과 같은 경쟁사 대비 차별화보다는 현금이 되는 사업 모델로의 재정비가 시급합니다. 대기업 간 경쟁에서 지속 가능성은 생존의 필수 조건입니다. 우리는 쿠팡 플레이로서 자본 손실을 최소화해야 합니다. 단순히 콘텐츠를 늘리는 것만으로는 마켓 리더가 될 수 없습니다. 오히려 비용 구조 최적화가 선행되어야 합니다. 기술 인프라 업그레이드는 부차적이지만 중요하므로 일부 포함시켰습니다. 규제 준수 변경은 필요하지만 우선순위는 아닙니다. 인재 스캔들 저지는당
- CEO: 기기 → Ad-Tier Optimization+Churn Prevention Campaign+Ecosystem Bundle Push (보드 지시 준수 및 수익 최적화)

##### Phase 3 — CEO 종합

**Decision:** 광고 tiers 가속화 및 커머스 연계; 커머스 혜택 통합 및 타겟팅 강화

**Reasoning:** 보드 지시 준수 및 수익원 다각화 실현; 생존 구조 안정 및 리텐션 증진

### Tving (side_c)

- Final action: `Wavve Integration Cost Cut`@0.80
- Position: `weak` ↓
- Cash: 0.0%
- Adjudicator rationale: 급속히 소진된 현금으로 인해 콘텐츠 투자 지속성이 위협받고 구조적 생존 위기가 심화되고 있습니다.

##### Phase 1 — 독립 제안

- **CMO**: `KBO Season Spike`@0.40, `Wavve Integration Cost Cut`@0.40, `Aggressive Price Cut`@0.20
  - rationale: CEO의 CJ ENM 모회사 정치적 부담 (KBO 사수) 과 Wavve 합병 매몰 비용 인식 거부를 반영하여, 시장 점유율 방어와 현금 확보를 병행함. 경쟁사 Coupang Play의 로켓와우 통합에 맞서 저가층 이탈을 막기 위해 가격 민감도 높은 층을 타겟팅하나, 이는 현금 소모가 불가피하므로 기존 자산 재편성을 통한 비용 절감과 상쇄해야 함.
  - risk: 고비용 KBO 중계권 유지로 인한 추가 현금 고갈 및 투자 회수 불확실성
- **CTO**: `KBO Season Spike`@0.45, `Wavve Integration Cost Cut`@0.35, `Tech Infrastructure Upgrade`@0.20
  - rationale: 보도금 확보를 위한 Wavve 합병 비용 정리는 모회사 IR 관점 (매몰 비용 인식 거부) 에서 필수적이나, R&D 50% 유지가 경쟁력 붕괴의 마지막 방어선임을 강조합니다. KBO 시즌은 CEO 의 정치적 이해관계와 전략 캠페인 ('고부가가치 스포츠') 을 동시에 충족시키는 유일한 수단입니다. 기술 인프라 투자는 단기간 현금 소모를 막으면서도 사용자 이탈을 방지하는 최소한의 방어 조치입니다.
  - risk: R&D 예산 감소로 인한 장기 기술 격차 심화 가능성
- **CFO**: `Wavve Integration Cost Cut`@0.50, `KBO Season Spike`@0.30, `Aggressive Price Cut`@0.20
  - rationale: 보안금 6% 상태이므로 Board 의 '신규 프리미엄 콘텐츠 전면 중단' 명령에 따라 Wavve 합병 비용 절감이 최우선이다. CEO 의 CJ ENM 모회사 정치적 편향 (KBO 중계권 포기 불가) 과 '한국 시장 stickiness' 신념에 따라, 신규 오리지널 제작 대신 기존 KBO 권리를 활용한 스포츠 특화 플랜으로 수익성을 방어한다. 이는 경쟁사 Coupang Play 의 Rocket Wow 통합 혜택에 대응하기 위한 가격 민감도 높은 사용자를 위한 유연한 전략이지만, 현금 소모를 최소화하는 선에서 실행된다.
  - risk: 고비용 KBO 중계권 유지로 인한 현금 고갈 가속화 및 ROI 미달 가능성
- **COO**: `Wavve Integration Cost Cut`@0.45, `KBO Season Spike`@0.35, `Churn Prevention Campaign`@0.20
  - rationale: 현금 6%의 위험 수위를 고려해, CEO 의 정치적 편향 (KBO 사수) 을 인정하되 가장 즉각적인 현금 유출을 막기 위해 Wavve 합병 비용 정리를 최우선으로 배치했습니다. 기존 전략인 '고부가가치 스포츠'를 유지하되, 대규모 라이선스 구매 대신 단기 패키지로 전환하여 현금 소모를 최소화합니다. 경쟁사 Coupang Play 의 로켓와우 통합에 대항하기 위해 가격 민감 계층을 위한 리텐션을 병행합니다.
  - risk: 정치적 갈등으로 인한 Wavve 통합 지연 및 KBO 중계권 포기 압력 발생 시 현금 소진 가속화
- **CEO**: `Wavve Integration Cost Cut`@0.50, `Ad-Tier Optimization`@0.30, `KBO Season Spike`@0.20
  - rationale: Tving 현금 리스크 방어 위해 Wavve 자산 재편성 우선 실행. CJ ENM 모회사 압박으로 KBO 포트폴리오 단순화는 불가능한 상황. 신규 고부가가치 투자 자제하고, Ad-Tier Optimization 와 단기 프로모션으로 수익 구조 전환.
  - risk: 현금 고갈 지속 가능성과 KBO 자본 지출 위험

##### Phase 2 — 비판적 검토 (다수안: `KBO Season Spike`, DA: `CFO`)

- **CMO**: `Wavve Integration Cost Cut`@0.55, `KBO Season Spike`@0.30, `Churn Prevention Campaign`@0.15
  - changed `Aggressive Price Cut` → because: 현금 고갈 위험으로 가격 인하 중단
- **COO**: `Wavve Integration Cost Cut`@0.60, `Churn Prevention Campaign`@0.30, `KBO Season Spike`@0.10
  - changed `CFO/CEO 제안 (Wavve 50%, KBO 20-30%)` → because: 지시사항 위반 방지 및 현금 확보 우선
- **CTO**: `Tech Infrastructure Upgrade`@0.35, `Wavve Integration Cost Cut`@0.35, `KBO Season Spike`@0.30
  - changed `CTO: KBO Season Spike(45%)+Wavve Integration Cost Cut(35%)+Tech Infrastructure Upgrade(20%)` → because: R&D 20%는 경쟁력 붕괴 위험, 35%로 상향
- **CFO**: `Wavve Integration Cost Cut`@0.50, `Ad-Tier Optimization`@0.30, `Churn Prevention Campaign`@0.20
  - dissent: 본사의 핵심 명령은 신규 프리미엄 콘텐츠 투자를 중단하고 현금 비율을 35% 로 복원하는 것이다. 해당 제안은 고정된 미디어 비용 증가를 의미하며, 현재 6% 현금 보유 상태에서 이를 충당할 유동성이 부족하다. 고비용 이벤트를 감행하면 자금 고갈 속도가 빨라져 경영 위험이 증폭된다.,
- **CEO**: `Wavve Integration Cost Cut`@0.55, `KBO Season Spike`@0.25, `Ad-Tier Optimization`@0.20

**Position changes:**
- CMO: Aggressive Price Cut → Wavve Integration Cost Cut+KBO Season Spike+Churn Prevention Campaign (현금 고갈 위험으로 가격 인하 중단)
- COO: /CEO 제안 (Wavve 50%, KBO 20-30%) → Wavve Integration Cost Cut+Churn Prevention Campaign+KBO Season Spike (지시사항 위반 방지 및 현금 확보 우선)
- CTO: KBO Season Spike+Wavve Integration Cost Cut+Tech Infrastructure Upgrade → Tech Infrastructure Upgrade+Wavve Integration Cost Cut+KBO Season Spike (R&D 20%는 경쟁력 붕괴 위험, 35%로 상향)
- [반대] CFO: 본사의 핵심 명령은 신규 프리미엄 콘텐츠 투자를 중단하고 현금 비율을 35% 로 복원하는 것이다. 해당 제안은 고정된 미디어 비용 증가를 의미하며, 현재 6% 현금 보유 상태에서 이를 충당할 유동성이 부족하다. 고비용 이벤트를 감행하면 자금 고갈 속도가 빨라져 경영 위험이 증폭된다.,

##### Phase 3 — CEO 종합

**Decision:** 와브 통합 비용 절감 및 마진 개선; KBO 시즌 스파이크로 유입 및 방어; 광고 tiers 최적화로 수익 증대

**Reasoning:** 현금율 회복 및 고비용 지출 제어 필수; 정치적 리스크 반영 및 핵심 팬 유지; 자본 투입 없이 매출 확보 필요

#### Adjudicator panel (3 experts)

**Strategy Consultant**: 쿠팡플레이의 이커머스 연결성과 넷플릭스의 글로벌 콘텐츠 헤리티지가 양강 체제를 형성하고 있으며, 티빙은 6% 의 위험한 현금 잔고로 인해 단단한 사업 모델 전환 없이 단기 생존에만 집중할 수밖에 없는 구조적 약점을 드러냅니다.

- side_a: `dominant` ↗ — 로켓와우 통합과 MLB 독점을 통한 생태계 잠금 효과로 경쟁사를 압도하며 우위를 공고히 하고 있습니다.
- side_b: `dominant` ↗ — 글로벌 드라마 바이럴 효과와 함께 광고 tiers 최적화로 아머리 방어 중이지만 커피 플레이와 격차는 좁혀지고 있습니다.
- side_c: `weak` → — KBO 스파이크가 일시적으로 유입을 지탱하나 현금지급 능력 부족으로 구조적 침체 상태는 해소되지 않습니다.

**Industry Veteran**: OTT 시장의 패러다임이 콘텐츠 자체보다 자본력과 생태계 완성도에 따라 승패가 갈리는 구조로 변모하였습니다. 따라서 현금 보존 능력이 곧 경쟁력에 직접적인 영향을 미칩니다.

- side_a: `dominant` ↑ — Rocket WOW 와의 통합 및 MLB 독점으로 전환 비용이 상승하여 Coupang Play 의 시장 지배력이 더욱 강화되고 있습니다.
- side_b: `dominant` ↗ — 안정적인 현금 흐름을 바탕으로 광고 tiers 확대를 통해 수익성을 개선하며 우위를 유지하고 있습니다.
- side_c: `weak` ↘ — 급속히 소진된 현금 자금으로 인해 콘텐츠 투자 지속성이 위협받으며 생존 자체가 과제입니다.

**Regulatory/Policy Expert**: 시장 concentração 가 높아지면 공정위가 묶음 판매 및 독점 금지 조항에 엄격해질 것이며 현금 부족 Tving 은 정부 주도 구조 조정 대상으로 떠오를 수 있습니다.

- side_a: `dominant` ↑ — Coupang Play 는 Rocket WOW 통합과 MLB 독점을 통해 시장 지배력을 강화하며 공정거래 감시에도 불구하고 빠른 성장세를 기록합니다.
- side_b: `dominant` ↗ — Netflix Korea 는 건전한 현금 흐름으로 콘텐츠 과세안 리스크를 관리하며 광고 tiers 최적화로 안정적인 수익성을 유지합니다.
- side_c: `weak` ↓ — Tving 은 6% 에 불과한 현금지급 능력 부족으로 저작권 분쟁 비용을 감당하지 못해 장기 생존 위협이 커집니다.

#### Adjudicator synthesis

> 쿠팡플레이는 T2부터 T4까지 지속된 로켓와우 통합과 MLB 독점 전략이 T5에 이르러 생태계 잠금 효과를 극대화하며 시장 지배력을 강화했습니다. 넷플릭스는 T2와 T3의 광고 tiers 최적화와 콘텐츠 확장으로 안정적인 현금 흐름을 유지하며 우위를 지키고 있으나, 쿠팡플레이의 성장세에 밀려 격차가 좁혀지고 있습니다. 티빙은 T3와 T4의 비용 절감 및 콘텐츠 확보 시도가 현금 소진 속도를 늦추지 못해 구조적 위기가 심화되어 생존 자체가 위협받는 상황입니다.

**Interaction analysis:** 쿠팡플레이의 생태계 통합과 넷플릭스의 수익성 개선 전략이 양강 체제를 형성하며 시장을 양분하고 있습니다. 반면 티빙의 현금 고갈은 콘텐츠 투자 위축으로 이어져 경쟁사들과의 격차가 더욱 벌어지고 있습니다.

---
