# Strategy Review — research-driven doc / plan-review (audit-aspect 축)

**검토 대상**: `strategy/strategy.md`
**모드**: plan-review (연구팀, 사용자 도메인 전문가 대리)
**중복 회피**: round_1_quality.md(구성 완전성·논리·루프 명칭 drift)·round_1_factcheck.md(verbatim 대조)와 비중복. 본 라운드는 남은 4축 한정 — Coverage(orphan card) / Style Guide compliance / Structure / 2부 매핑 누락. 개별 fact citation 재검증 제외(fact-checker 병렬).
**대조 근거**: `analysis_summary.md`(§1 세대축·§2 tier 표·§3 Tensions), `ref_analysis.md §1` 매핑 축, cards/ 60종 glob diff, 라이브 `notes/`·`_layer2/` 구조.

---

## 축 1 — Coverage (orphan card 탐지)

cards 60종 vs strategy `[slug]` 인용 36종 → orphan 24종. 분류 결과:

### 🔴/🟡 — citation 자리 누락 (memo 삽입)

| orphan card | tier | 누락 자리 | 등급 | memo 위치 |
|---|---|---|---|---|
| `greyling-configured-not-coded` | 2 (named) | **M5 명제** — M5 의 verbatim "A markdown edit without a before/after eval is a vibe" 의 _실제 출처_ 인데 M5 1차 카드 칸은 braintrust/demystifying 만 적음. cards 확인: 이 카드 Quotable 3 가 정확히 그 문장. + "model is rented, harness is owned"·Tension(e) 규율 격차 출처. strategy 전체 미인용. | 🟡(verbatim 출처 누락) | §2 M5 표 아래 |
| `anthropic-ai-resistant-evals` | 1 ○중요 | P6 셀 — saturation·contamination 저항 eval, P6 신뢰성 1차인데 셀이 demystifying/braintrust/infra-noise 만 | 🟡 | 표 4.1a P6 아래 + tier4 주 아래 |
| `openai-practical-guide-agents` | 1 ○중요 | P4 셀 — Manager/Decentralized·single-agent-first, read/write tension 제3 1차 출처(Anthropic·Cognition 외) | 🟡(verbatim 은 2차 caveat) | 표 4.1a P4 아래 |
| `anthropic-writing-tools-for-agents` | 1 ○중요 | P6/P11 — eval-driven tool 개선 | 🟡 | tier4 주 아래(통합) |
| `willison-agentic-engineering-patterns` | 1 ○중요 | P3 — Red/green TDD, maker-verifier 일반화 사례 | 🟡 | 표 4.1a P3 아래 |
| `anthropic-agent-skills` | 1 △참고 | P11 — progressive disclosure 정의 카드. **2부 2.6 "skill progressive disclosure" 매핑의 1부 cross-ref 앵커** — 없으면 2부가 가리킬 1부 자리 부재 | 🟡 | 표 4.1a P11 아래 + tier4 주 |
| `anthropic-think-tool` | 1 △참고 | P11 | 🟢 | 표 4.1a P11 아래(통합) |
| `greyling-rise-of-harness-engineering` | 2 | 1.2 harness 절 — harness=4th architectural layer 정리 메인 카드(Schmid OS·parallel.ai 6-comp·80/20). 셀이 agent-model-harness(감쇠론)만 인용 | 🟡 | 표 4.1 1.2 아래 |
| `greyling-loop-engineering-playbook` | 2 | 1.3 loop 절 — runtime tiering(Tier A/B/C). 6-block 만 다루면 불요, runtime tiering 쓰면 필수 | 🟡 | 표 4.1 1.3 아래 |
| `redhat-eval-driven-development` | 3 | P6 — 8-stage·"known bad" set(=우리 drill cases 연결)·judge calibration | 🟡(tier3, backing 동반 조건) | 표 4.1a P6 아래 |
| `factory-evaluating-compression` | 2 | P11 — tokens-per-task·probe eval | 🟢 | 표 4.1a P11 아래(통합) |

### 🟢 — 정상 위임 (informational memo 1건)

arXiv tier-4 orphan 14종(auditing-harness-safety·code-as-agent-harness·constitutional-spec-driven·context-eng-multi-agent·eval-driven-iteration·harness-bench·inside-the-scaffold·paace·secure-plan-then-execute·self-improving-coding-agent·sew·skillreducer·spec-driven-code-to-contract) — tier 4 단독 근거 금지·backing 전용이라 표 4.1a 가 "04 카드 매핑 그대로" 로 위임함이 설계상 정상. 단 정량값 인용 4종(constitutional −73%/harness-bench 76.2/self-improving 17→53%/skillreducer +2.8%)은 출처 거슬러 표기 리마인더를 §5.3 Gap 아래 informational memo 로 삽입. `augmentcode-git-worktrees`·`codewithseb-headless-cicd`(tier 3) 도 P9/P10 의 04 위임 backing 으로 정상.

> **핵심 발견**: tier 1 필독 12종은 전부 인용됨(누락 0) — 가장 중대한 omission 은 없음. 그러나 (a) M5 verbatim 의 출처 카드 자체가 orphan, (b) ○중요 4종(ai-resistant/openai/writing-tools/willison)·△참고 2종이 표 셀 누락, (c) tier-2 정리 카드 2종(rise-of-harness/loop-playbook)이 세대 절에서 누락 — 특히 P4(openai)·P6(ai-resistant) 는 합의 강도를 떠받치는 1차라 표 셀 명시 권장, anthropic-agent-skills 는 2부 2.6 cross-ref 앵커 역할이라 구조적으로 필요.

---

## 축 2 — Style Guide compliance (본문 자기준수)

- **카드 인용 표기 `[card-slug]`**: 본문 전반 일관 ✅. M5·표 4.1a 등 모든 카드 인용이 backtick `[slug]` 형.
- **라이브 anchor `파일 §절`**: 일관 ✅ (CONVENTIONS.md §5.10 ×8·WORKFLOW.md §0(a)·prd.md §2 등 동일 형). 단 `prd.md` 축약(3회) ↔ `worklog-board/spec/prd.md`(1회) 혼용 — spec-backed cwd 에서 어느 prd 인지 절 독립성 깨질 소지. 🟢 memo(첫 등장 전체 경로 규칙 추가 권장).
- **영어 용어 유지 목록 ↔ 본문**: Style Guide 표기 목록(harness·loop·worktree·headless·spec·context·maker-verifier·golden set 등)과 본문 표기 일치 ✅. 한국어 본문 + 굳은 영어 용어 패턴 준수.
- **정량 수치 whitelist**: §5.2 가 "등" 으로 비배타 명시, 본문이 list 밖 수치(37%/90%단축/17→53%) 를 직접 쓰지 않음(해당 수치는 analysis 에만) → 준수 ✅. 누락 아님.
- **루프 호칭 병기(oncall/drill/note/study)**: round_1 에서 수정 완료분 — 본 라운드 재확인 결과 본문·Style Guide·Risk 일관 ✅.

→ Style Guide 위반 없음. anchor 축약 1건만 🟢.

---

## 축 3 — Structure (참조서 lookup 적합성)

- **절 독립성**: 4부 절 구성이 표 anchor 중심(4.1~4.4 각 표 self-contained) — 단독 lookup 가능 ✅. 단 4부 prd.md 축약 anchor 가 절 독립성 약화(축 2 memo 참조).
- **표 anchor 배치**: 매핑·tier·발화·2-layer 전부 표로 — lookup 빠름 ✅.
- **3부 발화 시나리오 순서**: 🟡 — 표 4.3a + 3.2~3.8 절이 "하루 일과 시간순"(당직→라우팅→디스패치→사후수정→모의훈련→연수→post-it→케이스)에 가까운데, lookup 참조서는 _빈도순_ 이 동선에 맞음. 실제 빈도: 새 작업 라우팅(최빈)·post-it handoff(매 세션 wind-down) 가 앞이어야 하나 각각 2번째·7번째. 연수(주1회)·케이스 승격(이벤트성)은 뒤가 맞음. 3.1 시간순 서사는 OK, 3.2~3.8 개별 lookup 절만 빈도순 재배열 권장 → memo 삽입.
- **4부 종착 닫힘**: round_1 #5 가 이미 4.4 "끝점만 명시·전체 줄기 cross-ref" 로 처리 — 본 라운드 재확인 일관 ✅.

---

## 축 4 — 2부 매핑 누락

`ref_analysis.md §1` 매핑 축(P1/P2~P11) vs 표 4.2a 대조 + task 지정 항목(P11→얇은 부트스트랩·Stage D.5·디스패치 등록부·g0 세금·머지 게이트):

| 매핑 축 | 표 4.2a 반영 | 비고 |
|---|---|---|
| P1/P2 하드 순서 게이트 | ✅ P1/P2 행 (artifact-guard·spec-skill-gate·read-marker) | — |
| P3 팀 분업·Stage D.5 | ✅ P3 행 + 2.2 + directive §4 | Stage D.5 반영됨 |
| P4 orchestrator·중첩 1단 | ✅ P4 행 | — |
| P5 sub-skill 단계 | ✅ P5 행(§6.2 호출 흐름 3패턴) | — |
| P6 g0 세금 ~40k | ✅ P6 행 + directive §4 | g0 세금 반영됨 |
| P7 sweep·승격·triage | ✅ P7 행 | — |
| P8 통신 버스 한 줄기 | ✅ P8 행 + 2.3 | 비중 최대 일관 |
| P9 머지 게이트·git preflight | ✅ P9 행 + 2.4 + directive §4 | 머지 게이트 반영됨 |
| P10 디스패치 등록부 | ✅ P10 행(.dispatch/jobs.log) + directive §4 | 디스패치 등록부 반영됨 |
| P11 얇은 부트스트랩 | ✅ P11 행 + 2.6 | 얇은 부트스트랩 반영됨 |

→ **2부 매핑 누락 없음**. task 지정 5개 항목(P11·Stage D.5·디스패치 등록부·g0 세금·머지 게이트) 전부 표/절/directive 에 존재. round_1 의 명칭 drift 수정과 합쳐 매핑 축은 완전.

---

## 종합

- 삽입 memo **11건**: COVERAGE 8(M5 verbatim 출처 / tier1 ○중요·△참고 6종 통합 / 1.2 rise-of-harness / 1.3 loop-playbook / P6 redhat+ai-resistant / P11 agent-skills+factory / P4 openai / P3 willison / tier4 informational) + STRUCTURE 1(3부 빈도순) + STYLE 1(prd anchor 축약).
- 가장 load-bearing: **M5 verbatim 의 출처 카드(`greyling-configured-not-coded`) orphan** — fact-checker 가 귀속 오류로도 잡을 수 있으나, _omission_ 축에선 그 1차 카드가 strategy 전체에서 인용 자리를 못 받은 것이 본질. + **P4 openai / P6 ai-resistant / P11 agent-skills** — 합의 강도·2부 cross-ref 앵커를 떠받치는 1차 누락.
- tier 1 필독 12종 누락 0, 2부 매핑 누락 0, Style Guide 위반 0(anchor 축약 🟢 1건) — 전반 견고. Coverage 가 유일한 실질 보강 지점.

> 참고: `analysis_project/paper/`·`analysis_project/code/` 부재(research-only 도메인, 정상). 본 리뷰는 research cards + analysis_summary + 라이브 notes 구조 + agent memory 에 근거.
