# Draft Review — 연구팀 plan-review (도메인 전문가 proxy)

> 대상: `draft/draft.md` (549줄) | 기준: `strategy/strategy.md` v2 §4 Section Plan + Style Guide
> 리뷰어: 연구팀 plan-review mode | 일자: 2026-06-11
> fact verbatim 검증은 fact-checker 병렬 — 본 리뷰 범위 밖.

## 축별 요약

| 축 | 판정 | memo 수 |
|---|---|---|
| 1. Strategy coverage | F3 figure 미embed (실질 누락) | 1 |
| 2. 절 충실도 (3부) | 대체로 lookup 가능, 3.2 전제·산출물 보강 여지 | 2 |
| 3. Style Guide compliance | 위반 없음 (prd 첫인용·F5 캡션 모두 통과) | 0 |
| 4. 절 독립성·lookup | P8 canonical/cross-ref 잘 작동 | 1 보강 |
| 5. Figure embed | 8개 경로 전부 정상, F3 누락이 핵심 | (축1 과 통합) |

총 삽입 memo: 5 (COVERAGE 1 · QUALITY 2 · STRUCTURE 2; 1.5 절에 COVERAGE+STRUCTURE 묶음)

### 통과 확인 (memo 미삽입)
- [STYLE] F5 캡션: draft L320 실제 캡션은 "품질관리·연구·편집·디자인·**자료**·codex-review" 로 figure_index(8팀)와 일치 — 초기 false-positive, 위반 아님.
- [STYLE] prd.md 첫 인용 전체경로: 4.0·4.1·4.2 첫 인용 모두 전체경로, 절 내 후속 축약 — Style Guide 부합.
- [STYLE] 루프 호칭 병기·anchor 형식·평어 개조식·친절 안내체 금지: 전반 준수.
- 8개 figure embed 상대경로(`../assets/figures/`·`../../../research/...`) 전부 파일시스템 검증 통과.

---

## [COVERAGE] F3 safety_layers 미embed (핵심 누락)

- strategy §6 + `assets/figures/figure_index.md` 둘 다 F3(`f3_safety_layers.png`)을 계획·렌더·자가검증 통과로 등재 (소속 절 "1.4 / 2부 다리").
- 그러나 draft 에 8개만 embed — F3 만 빠짐. 자산은 실재(`assets/figures/f3_safety_layers.png`)하고 자가검증도 통과(figure_index L30)인데 본문 참조가 없음.
- 더 큰 문제: F3 이 시각화하는 **"자율 실행 안전장치 4층(permission→classifier→sandbox→hook)"** 개념 자체가 draft 에 _합성된 형태로 등장하지 않음_. 84%(P9 L208)·93%/17%FN(P10 L218)이 패턴별로 흩어져 있을 뿐, "자율성 ↑ 일수록 hard boundary 로 무게 이동" 이라는 F3 의 종합 명제가 본문에 없다.
- strategy 가 이 figure 의 자리를 "1.4 / 2부 다리"(=1.5 절)로 배정했는데, 현재 1.5 절은 순수 연결 산문뿐.
- 조치 후보: (a) 1.5 다리 절(또는 1.4 말미)에 안전장치 4층 합성 단락 + F3 embed 추가, 또는 (b) strategy 에서 F3 을 drop 으로 정정. **(a) 권장** — figure 가 이미 검증 완료라 매몰비용 회수 + 자율성-안전 축은 매뉴얼에 실질 누락.

## [QUALITY] 3.2 전제조건·기대산출물 (보강 여지)

- 3.2(새 작업 라우팅)는 가장 빈번 시나리오인데, "트랙별 첫 발화" 의 _구체 예시_ 가 없다 — 표 3.0a 도 "트랙별 첫 발화(자연어 한 줄)" 추상 표현뿐.
- lookup 독자가 "그래서 뭐라고 치지" 에 답을 못 받음. 4트랙(문서/연구·실험/앱/라이브러리·CLI)별 발화 예시 한 줄씩(예: "이 논문 정리 좀" → autopilot-research / "X 기능 붙여줘" → spec→code)이 있으면 입문 가치가 큼.
- 분량 채우기 아님 — 발화 중심 가이드의 핵심 산출물(발화 예시)이 빠진 실질 누락.

## [QUALITY] 3.5/3.7/3.9 기대산출물·후속흐름 (경미)

- 3.5(사후 수정)·3.7(케이스 승격)·3.9(연수)는 절차는 명확하나 _기대 산출물 위치_ 가 절 안에서 안 닫힘 (3.5 는 plans/, 3.7 은 drill/cases/, 3.9 는 notes/study/ — 표 3.0a 엔 일부만). 절 독립 lookup 시 "결과물이 어디 떨어지나" 를 표 왕복 없이 절 안에서 답하면 좋음. 단 경미 — 표 3.0a anchor 로 보완되므로 강제 아님.

## [STYLE] prd.md 첫 인용 전체경로 (4.0)

- Style Guide(L318): "각 절 첫 인용은 `worklog-board/.claude_reports/spec/prd.md` 전체경로". 4.0 절(L493) 첫 prd 인용은 전체경로 OK. 4.2 절(L521) autopilot-note 흐름 첫 인용도 전체경로 OK. 4.1 OK.
- **4.2 본문 마지막(L529) `prd.md §4.3 v22 정정`**, **4.3(L539) `prd.md §4.3 v19`·`prd.md §4.3` 후속** — 같은 절 내 후속이라 축약 허용 범위. 다만 4.2 첫 인용(L521)이 전체경로면 절 내 축약은 규칙 부합. → 위반 아님(확인 완료, 통과 기록용).

## [STRUCTURE] P8 canonical/cross-ref 작동 — 통과 확인

- 1부 P8(L186 박스)이 canonical site 선언, 2.3(L330 박스)·4.4 가 "원칙 재서술 금지, cross-ref" 규율 준수. 2.3 은 우리 실물만, 4.4 는 종착점만 — 재서술 없이 압축 성공.
- 절 독립성: 각 2부/3부/4부 절이 "이 절은 ~ 자리다" 로 열어 단독 가독성 확보. 양호.

## [STRUCTURE] 1.5 다리 절 — F3 합성 자리 (보강)

- 1.5 가 "1부=망라 / 2부=매핑" 연결만 하고 끝남. strategy 가 F3(안전장치 4층)을 여기 배정한 의도는, 자율성-안전 trade-off 가 1부 원칙→2부 hard boundary(hooks) 전환의 _다리 논거_ 이기 때문으로 보임. 현재 다리가 그 논거 없이 형식적. → COVERAGE memo (a) 와 연동.
