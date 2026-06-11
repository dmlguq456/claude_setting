# refine round 1 — quality / cohesion / audience review

대상: `draft/draft.md` (v2). 점검 축 = 다리 절 cohesion / 표 흐름 / 그림 재번호 정합 / memo·문법 / §1.0 완화 서술. fact 재검증 미수행 (지시대로).

verdict: **PASS (clean)** — 5개 점검 항목 모두 통과, 차단 이슈 없음. 미세 제안 2건.

---

## (1) §1.5 추가 단락 — 다리 절 축 유지 / F3 캡션·번호 정합 ✓

- **다리 축 보존**: 새 "안전장치 4층" 단락(line 293)이 다리 절(§1.5)의 본래 논거를 깨지 않고 오히려 강화한다. 절의 기존 골격은 "원칙은 자율성을 키우고, 안전장치는 hard boundary 를 덧댄다 → 그래서 2부로 넘어간다"인데(line 299·301), 추가 단락이 그 "안전장치" 쪽을 L1~L4 4층으로 구체화한다. 단락 끝 문장("1부에 흩어진 84%·93%/17%FN 수치가 이 4층 위에서 하나의 안전 논리로 묶인다")이 P9·P10 에 흩어진 정량을 회수해, 2부 hook 4종(L4) 매핑으로 자연스럽게 연결된다(line 299). 1부→2부 전환 흐름 손상 없음.
- **F3 embed·캡션 정합**: line 295 `f3_safety_layers.png` embed → line 297 그림 5 캡션. 캡션의 4층 순서(L1 permission 93% → L2 classifier 17%FN → L3 sandbox 84% → L4 hook)가 본문 단락 서술 순서와 정확히 일치하고, figure_index F3 ground-truth(`05_deployment.md §1`, permission→classifier→sandbox→hook)와도 일치한다.
- **미세 제안 (비차단)**: 본문 단락(line 293)은 정량을 "93% 승인 / 17% FN / 84% prompt 감소" 세 개로 명시하나, L4 hook 에는 정량이 없고 인용("Unlike CLAUDE.md instructions which are advisory, hooks are deterministic")만 붙는다. 4층 중 한 층만 정성인 것은 의도된 비대칭(hook 은 deterministic 이라 % 가 없음)으로 읽히지만, 독자가 "L4 수치 누락?"으로 오인할 여지가 약간 있다. 현 서술로도 충분하나, 원하면 "L4 는 확률이 아니라 결정적이라 % 가 없다"는 한 구를 박으면 더 또렷하다.

## (2) §3.2 발화 예시 표 — 절 흐름 자연스러움 ✓

- 표 3.2(line 485~492)는 도입 문장(line 483 "트랙별 대표 발화 예시")과 매끄럽게 이어지고, 표 뒤 문단(line 493 slash 직접 입력 / line 495 발화 분류)으로 자연 복귀한다. 표가 절 중간에 끼어 흐름을 끊지 않는다.
- 표 5행이 4트랙(연구/문서/앱·라이브러리/실험) + 공통 1행을 커버 — §3.0 의 "lookup 빈도순" 취지와 부합하는 lookup 친화 구성. "라우팅" 열이 화살표 표기(`autopilot-research → research/`)로 결과 폴더까지 보여줘 참조서 audience(설계자 본인)에 적합하다.
- 표 3.0a(line 458~467 전체 시나리오 표)와 역할이 겹치지 않는다 — 3.0a 는 8개 시나리오 전반 인덱스, 3.2 표는 "새 작업 라우팅" 한 시나리오의 트랙별 발화 drill-down. 중복 아님, 계층적 보완.
- **미세 관찰 (비차단)**: 표 2행 "이 모듈 새로 만들어줘" 라우팅 셀이 "(spec 없으면) autopilot-spec → autopilot-code, 하드 순서 게이트 통과"로 다소 길다. 표 가독상 문제는 없으나 다른 행보다 정보 밀도가 높다 — 의도된 것이면 그대로 둬도 무방.

## (3) 그림 6~9 재번호 후 캡션-파일 매핑 ✓ (figure_index 대조 완료)

본문 그림(순차 1~9) ↔ PNG ↔ figure_index(F1~F9) 전수 대조 — 어긋남 없음:

| 본문 | src PNG | 절 | index F | 일치 |
|---|---|---|---|---|
| 그림 5 | f3_safety_layers | 1.5 | F3 (1.4/다리) | ✓ |
| 그림 6 | f4_four_track_pipeline | 2.1 | F4 (2.1) | ✓ |
| 그림 7 | f5_team_matrix | 2.2 | F5 (2.2) | ✓ |
| 그림 8 | f6_loop_layers | 2.5 | F6 (2.5) | ✓ |
| 그림 9 | f7_daily_flow | 3.1 | F7 (3.1) | ✓ |

(그림 1~4 도 확인 — f1/§1.0, arxiv fig2/§1.1, arxiv fig1/§1.2, f2/§1.4 모두 index 와 일치.) 본문은 순차 "그림 N", index 는 자료팀 자산 ID "FN" 이라 두 번호 체계가 다르나, **절 기준 PNG 매핑이 양쪽 동일**하므로 정합. 그림 6~9 캡션 텍스트도 index 캡션과 동일 의미(루프 호칭 병기 포함). 재번호 누락·중복·skip 없음(1~9 연속).

- **참조서 audience 주의 (비차단)**: 본문 "그림 5"와 index "F3"이 같은 도식을 다른 번호로 가리킨다. 매뉴얼 본문만 읽는 독자에겐 무관하나, figure_index 를 함께 여는 설계자가 "그림 5 = F3"을 한 번 매핑해야 한다. 현재 어느 쪽에도 교차표가 없다. 차단은 아니지만, figure_index 표에 "본문 그림 #" 열을 하나 추가하면 두 체계가 묶인다(자료팀 산출물 영역이라 본 refine 범위 밖 — 메모만).

## (4) memo 잔존 / 표 문법 / changelog YAML ✓

- **memo 잔존 없음**: 본문에 inline `<!-- memo: ... -->` 0건. "memo" 문자열은 전부 changelog 서술("review memo 8건 반영", "memo만 제거") 또는 "memory" 단어 — 잔존 메모 아님. v2 changelog 가 applied 8/overridden 0 으로 기록한 것과 정합(8 note 줄 = memo 8건).
- **표 문법**: §3.2 표·표 3.0a·2부 매핑 표 등 변경 인접 표 모두 파이프 정렬·구분행(`|---|`) 정상, 셀 내 `|` 누출 없음.
- **changelog YAML**: block scalar(`notes: |`) 파싱 검증 통과 — `yaml.safe_load` OK, versions=[v2, v1], v2 notes 8줄. 들여쓰기·콜론 escape 문제 없음. anchor 표기(`[§1.5 verified ...]`)도 block scalar 안 평문이라 문법 영향 없음.

## (5) §1.0 Karpathy 귀속 완화 — 어색함 점검 ✓

- line 37 완화 서술: `Osmani 가 인용한 한 줄("One analysis quipped:")이 ... — "Prompt engineering walked so context engineering could run" [osmani-context-engineering] (카드는 Karpathy 풍 quip 으로 표기하나 원문은 출처를 한 분석으로만 돌려, 직접 발언 귀속은 단정하지 않는다).`
- **어색하지 않음**: "Karpathy 의 한 줄" 단정 → "한 분석(One analysis)" + 괄호 caveat 로 정확히 완화됐다. 인용 부호 안 원문(`"One analysis quipped:"`)을 그대로 노출해 근거를 보여주고, 괄호에서 카드 표기와 원문 출처의 차이를 명시 — 매뉴얼 전체의 "인용 규칙"(귀속 정확성, frontmatter·intro 의 anchor 규율)과 톤이 일관된다. 참조서 audience(설계자 본인 = 인용 엄밀성 중시)에 오히려 부합한다.
- 한국어 자연스러움: "직접 발언 귀속은 단정하지 않는다"가 매뉴얼 전반의 caveat 어투("단정하지 않는다", "단정 X")와 동일 패턴 — 절 안에서 톤 이질감 없음.

---

## 칭찬할 부분

- §1.5 4층 단락은 단순 추가가 아니라 1부 전반(P9 84% / P10 93%·17%FN)에 흩어진 정량을 **회수해 하나의 안전 논리로 묶는** 역할을 해, 다리 절의 본래 기능(1부 종합 → 2부 전환)을 강화한다. 추가가 절 목적과 동형이다.
- 두 번호 체계(본문 그림 N / 자료팀 FN)를 쓰면서도 절 기준 PNG 매핑을 양쪽에서 일관 유지 — 재번호 작업에서 가장 깨지기 쉬운 지점인데 누락·skip 없이 정합.
- "당직 7호 → 항목 8" 교정이 2곳(§2.4·§3.6) 모두 반영, oncall.md 실물 항목 번호와 맞춤. changelog 도 "2곳" 으로 정확히 기록.

## 비차단 제안 요약 (적용은 개발/문서팀 위임)

1. §1.5 본문(line 293) L4 에 % 없음이 의도임을 한 구로 명시 (오인 방지) — optional.
2. figure_index 표에 "본문 그림 #" 열 추가로 그림 N ↔ FN 교차 매핑 (자료팀 산출물 영역) — optional.

두 건 모두 cohesion·정합을 깨지 않는 선택적 개선이며, 현 v2 는 그대로 ship 가능.
