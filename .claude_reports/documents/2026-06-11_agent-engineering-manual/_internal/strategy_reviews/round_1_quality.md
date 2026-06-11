# Strategy Review — Round 1 (plan-review / construction quality)

**검토 대상**: `.claude_reports/documents/2026-06-11_agent-engineering-manual/strategy/strategy.md`
**계획 요약**: 4부 매뉴얼(원칙 세대사 / 우리 세팅 매핑 / 발화 실전 / worklog-board 노트)의 절 단위 설계도. ground truth = research cards(1부) + 라이브 파일 §anchor(2~4부).
**검토 범위**: 5축(구성 완전성 / draft directives 반영 / 논리 일관성 / 참조서 설계 / Risk 처리). 개별 fact citation 검증은 fact-checker 몫이라 제외.
**대조 근거**: `06_implementation.md`, `04_technical_deep_dive.md`, `material_index.md`, `ref_analysis.md`, 라이브 `loops/README.md`·`hooks/*.sh`·`notes/`·`worklog-board/spec/prd.md`.

---

## 🔴 실행 전 반드시 수정할 문제

### 1. 루프·notes 명칭이 라이브 파일과 어긋난다 (2부 2.5 / 3부 4.3 / 4부 4.4 / F7 anchor 전반)

가장 심각하다. 매뉴얼의 핵심 가치가 "라이브 §anchor 로 drift 추적"인데, strategy 가 박아둔 anchor 자체가 _현재 실물과 불일치_ 다.

- **현재 라이브 상태** (`loops/README.md` 현역 표 + `ls loops/`·`ls notes/` 확인):
  - 당직 루프 = **`oncall`** (`loops/oncall.sh`, 보고서 `notes/oncall/<date>.md`)
  - 모의훈련 루프 = **`drill/`** (`drill/run.sh`, 케이스 `drill/cases/`)
  - 일지 = `note` (`loops/note.sh`), 연수 = `study` (`loops/study.sh`) — 이 둘만 strategy 와 일치
- **strategy 가 쓴 명칭** (불일치):
  - 표 4.3a "아침 당직 처리" 행 → `notes/scout/` **또는** `notes/duty/<date>.md` (둘 다 라이브에 없음 — 실물은 `notes/oncall/`)
  - 4.4 표 4.4a 부속 행 → `notes/duty/` (실물 `notes/oncall/`)
  - 표 4.3a "모의훈련 발사" 행 → `golden/run.sh`, 4.3절 "케이스 승격" → `golden/cases/` (실물 `drill/run.sh`·`drill/cases/`)
  - 표 4.2a P6 행 → "golden 모의훈련 루프" / `CLAUDE.md` 트리거 "golden/run.sh"
  - 표 4.2b·여러 곳에서 "golden" 을 루프 파일명으로 사용

- **혼선의 뿌리**: 글로벌 `~/.claude/CLAUDE.md` 가 아직 `scout`/`golden` 표기(`notes/scout/`·`loops/golden/run.sh`·"당직=scout·모의훈련=golden")를 들고 있어 _그 자체가 stale_ 이다. 즉 CLAUDE.md ↔ loops/README.md 사이에 진행 중인 rename drift 가 있고, strategy 는 두 출처를 섞어 인용했다(`scout`+`duty`+`golden`+`oncall` 혼재). loops/README.md 가 더 최신(`> 파일명은 ASCII 유지, 표기는 당직(oncall) 처럼 병기`)이므로 **`oncall`/`drill` 이 진실**.
- **수정**: directive §4 가 "draft 시점 라이브 직접 Read 강제"라 draft 단계에서 교정될 _여지_ 는 있으나, strategy 의 anchor 표가 _틀린 파일명을 못박아_ 두면 draft 가 그대로 베낄 위험이 크다. 표 4.2a P6·P7·P10 / 표 4.2b / 표 4.3a / 표 4.4a / F7 캡션의 `scout`·`duty`·`golden` → `oncall`·`drill` 로 통일하고, "당직(oncall)·모의훈련(drill)" 병기 규칙을 Style Guide 표기 규칙에 추가. **추가로**: 이 CLAUDE.md↔loops/README 명칭 drift 자체를 Risk 절에 "라이브 출처 간 내부 불일치 — 더 최신인 loops/README 를 우선" 으로 명시.

### 2. 4.3 / 표 4.3a 의 "scout" 알리아스 서술이 라이브와 모순

표 4.3a "아침 당직 처리" 행 anchor 가 `notes/scout/` 또는 `notes/duty/<date>.md` 로 _두 개의 존재하지 않는 경로_ 를 OR 로 제시한다. 실물은 단일 `notes/oncall/<date>.md`. lookup 참조서에서 독자가 실제로 따라갈 경로가 틀리면 참조서의 1차 목적이 깨진다. `notes/oncall/<date>.md` 단일로 확정.

---

## 🟡 보완하면 좋은 점

### 3. 1부 골격 채택은 정확하나, 패턴 강도 한 칸이 04 와 어긋난다 (표 4.1a P11)

- **잘 맞은 부분**: 표 4.1a 의 P1~P11 1차 카드 매핑은 `06 §4 citation map` 과 카드 단위로 일치. caveat 귀속(P1 plan-skip / P2 over-spec / P3 GAN / P6 noise / P7 자동화 tier4 / P9 tier3 / P10 cron tier3)도 `04` Takeaway 와 합치. 1.0~1.5 절 구성도 `06 §1` outline 그대로 채택 — 재발명 아님. ✅
- **어긋난 한 칸**: 표 4.1a 가 **P11 강도를 ★** 로 표기. `04` 미해결 과제 Takeaway 는 "P1–P8·P11 단정 가능"이라 ★ 가 맞지만, 본문 P11 절은 압축 수치(98.7%/85%/37%/+2.8%) 의존도가 높고 그중 SkillReducer +2.8% 는 tier 4. 강도 자체는 ★ 유지하되 "수치는 카드 명시값만 + SkillReducer 는 tier 4 backing" 단서를 셀에 한 줄 다는 편이 04 의 정밀도와 맞는다. (Style Guide 정량 규칙엔 이미 들어가 있으니 표에서 한 번 더 anchor.)

### 4. Tensions 4종 — 표 4.1a 에 ②③ 균형 지시가 빠져 있다

`04` 는 Tension 4종 전부를 다루고, strategy Risk·Style Guide 는 ①④ 균형을 강제한다. 그런데 **②(GAN 비유 한계)·③(harness 감쇠론 inversion)** 도 caveat-heavy 다 — ② 는 "GAN 라벨 문자 그대로 적용 금지", ③ 은 "Harness-Bench 76.2/52.4/23.8 = Greyling 2차". strategy 가 ②③ 를 P3·M4·Risk 의 다른 줄에 분산시켜 두긴 했으나, 1.4-T 절 설계에서 "4종 모두 균형, 특히 ①④ 필수 반론" 으로만 적어 ②③ 의 caveat 의무가 표에서 흐려진다. 1.4-T 셀에 "② GAN 라벨 caveat / ③ Harness-Bench 2차 명시" 를 한 줄 추가 권장. (지금도 누락은 아님 — 분산돼 있을 뿐이라 🟡.)

### 5. P8 canonical-site 설계는 일관적이나, 2.3↔4.4 cross-ref 방향이 한 곳에서 모호

- **잘 된 부분**: §3.3 Paragraph Cohesion 이 P8 3중 등장(1부/2부/4부)을 canonical=1부 P8 + cross-ref 로 압축하도록 명확히 설계. 2.3 "비중 최대, 원칙 재서술 금지" / 4.4 "재서술 금지, cross-ref" 가 일관. M2 관통선(`.claude_reports`→핸드오프→pipeline_state→3-tier→headless→worklog 2-layer)도 §3.1·2.3·4.0·4.4 에서 동일 줄기로 반복돼 일관적. ✅
- **모호한 한 곳**: 4.4 "1부 P8 → 2부 2.3 → 4부 종착의 한 줄기 매듭"에서 _매듭(닫힘) 서술_ 을 4.4 에 두는데, 이게 "재서술 금지" 와 충돌할 소지가 있다. 닫힘 문장이 곧 요약 재서술이 되기 쉽다. 4.4 는 "줄기의 _끝점만_ 명시(worklog 2-layer)하고, 전체 줄기 회수는 cross-ref 로" 임을 한 단계 더 못박으면 draft 가 4.4 에서 P8 전체를 다시 풀어쓰는 사고를 막는다.

### 6. drift Risk 대응 ③(일지 루프 publish 후 갱신)이 라이브 일지 정의와 살짝 어긋난다

Risk 절·1.1·4.0 이 "일지(note) 루프가 publish 후 갱신 라우팅" 으로 적었는데, 라이브 `loops/README.md` 의 일지(note) 정의는 "전날 산출물 내용 → worklog-board L2 노트화·라우팅"이지 _매뉴얼 자체의 stale 갱신_ 책임 루프가 아니다. publish 후 매뉴얼 재갱신 트리거는 directive §5(본 범위 밖)에 가깝고, 일지 루프가 그 일을 한다는 보장이 라이브에 없다. "일지 루프가 갱신" 을 "일지 루프가 publish 자리로 _라우팅_ 하고, 갱신 자체는 별도 트랙(directive §5)" 로 약화 권장. (단정 X — 의도한 매핑일 수 있으나 라이브 정의와 대조 필요.)

---

## 🟢 잘 작성된 부분

- **1부 재발명 회피**: `06 §1` outline 을 절 단위로 그대로 채택하고 "재발명 금지" 를 강제 — 점검축 1 충족. 패턴 11종 + Tensions 4종 누락 없음(표 4.1a 11행 전부 + 1.4-T 절).
- **directive 8종 분류 정확**: strategy 영역(§1 figure / §2 P8 한 줄기 / §3 headless 분사 / §4 신설분 / §6 망라)이 Section Plan 에 실제로 들어갔고, 비-strategy(§5 publish·§7 양방향·§8 이관)는 "본 범위 밖, 언급만" 으로 정확히 격리. 망라 원칙(§6)을 "비중만 키움, 강조항목은 하나의 예시" 로 06 §1 단서까지 반영 — 점검축 2 충족.
- **참조서 설계 명시적**: §3.2 lookup 최적화(절 독립성·표 anchor·anchor 형식 일관) + Style Guide 톤(친절 안내체 금지·marketing/administrative 아님·평어 개조식)이 명문화 — 점검축 4 충족.
- **Risk·tier 처리 충실**: P7 자동화 tier4 / P9·P10 tier3 caveat, Tensions ①④ 균형, Greyling 2차·명명 권위(context=Osmani+Anthropic / harness=Trivedy / loop=Osmani), prd vision 단정 금지, 5.3 Gap 절까지 — 점검축 5 의 대부분 충족(라이브 drift 명칭 문제만 별개).
- **figure 정책 일관**: F1~F9 가 many-to-many=매트릭스(F2·F5) / 파이프라인=단방향 레인 분류 정확, edge 교차 회피 feedback 반영, `<img width=500>` embed — directive §1 충실.
- **4부 prd anchor 정확**: Layer 1/2 소유권·card_id soft ref·autopilot-note 흐름·"진행 중 vision 단정 X"(DB 전환 v21·홈 콕핏 v22) 가 라이브 `prd.md §2`·§2.5 와 합치.

---

## 종합

구성 완전성·directive 반영·논리 일관성·참조서 설계는 견고하다. 단 **참조서의 핵심 기능(라이브 §anchor 추적)을 떠받치는 anchor 명칭 자체가 라이브와 어긋나는** 🔴 2건(루프 명칭 drift, 존재하지 않는 notes 경로)이 있어 draft 진입 전 교정이 필요하다. 이 명칭 drift 는 글로벌 CLAUDE.md(stale: scout/golden) ↔ loops/README.md(최신: oncall/drill) 의 내부 불일치에서 왔으므로, loops/README 를 진실로 삼아 통일하고 그 불일치 자체를 Risk 절에 등재하면 매뉴얼이 오히려 drift 를 _시연_ 하는 자산이 된다.
