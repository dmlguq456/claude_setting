---
type: report
status: draft
date: 2026-06-11
genre: 에이전트 엔지니어링 매뉴얼 (README 확장판 — 입문서·참조서, markdown prose)
tone: default (참조서 — administrative 아님, marketing 어조 금지, 평어·개조식)
language: Korean (한국어 본문 + 굳은 영어 용어 유지)
audience: 시스템 설계자 본인 (lookup 최적화, 친절 안내체 회피)
qa: standard
sources:
  research: .agent_reports/research/agent-engineering-principles/ (cards/ = 단일 ground truth)
  live: ~/.claude/{CLAUDE.md,CONVENTIONS.md,WORKFLOW.md,loops/README.md,hooks/*.sh} + worklog-board/.claude_reports/spec/prd.md + notes/
---

# Report Strategy: 에이전트 엔지니어링 매뉴얼

> 본 strategy 는 4부 매뉴얼의 _절 단위 설계도_. ground truth 는 `research/agent-engineering-principles/cards/` (1부) + 라이브 파일 `파일경로 §절번호` anchor (2~4부). draft 작성 시 본 strategy 의 Section Plan 을 채택·구체화한다 — 재발명 금지.

---

## 1. Objective & Scope

### 1.1 목적

`~/.claude/` 에이전트 시스템의 **README 확장판**. 업계의 쏟아지는 에이전트 엔지니어링 원칙(prompt→context→harness→loop 세대 + 실무 패턴 11종)을 망라하고, 그 원칙들이 _우리 세팅에 어떻게 녹아 있나_ 를 실물 anchor 로 매핑한 뒤, 발화 중심 실전 가이드와 worklog-board 에이전틱 노트 활용까지 잇는다.

- 위상: 세팅 자체의 **자기 문서화** — 외부 독자를 위한 홍보물이 아니라 _찾아보는 참조서_.
- publish 예정 자리: `notes/` 트리 (일지 루프가 라우팅, worklog-board L2 가 읽는 자리). draft directives §5 — 본 strategy 범위 밖, 언급만.

### 1.2 독자

시스템 설계자 본인 (단일 사용자). 배경 설명 최소, 절 독립성·표 anchor 로 lookup 최적화. 친절 안내체(`~해 드릴게요`) 금지, 평어·개조식 허용. ML 능숙·telephony DSP 용어는 깊지 않음 (단 본 매뉴얼은 도메인 무관 — 에이전트 엔지니어링 자체가 주제).

### 1.3 범위

- **포함**: 1부 원칙 세대사 + 패턴 11종 + Tensions 4종 / 2부 우리 세팅 매핑 (CLAUDE.md·CONVENTIONS·WORKFLOW·loops·hooks 6종) / 3부 발화 중심 실전 / 4부 worklog-board 노트.
- **제외 (draft 본문 밖, 언급만 가능)**: draft directives §5(publish)·§7(양방향 보강 제안)·§8(이관) — 파이프라인 종료 후 별도 트랙.
- **관통 주제 (비중 최대)**: 산출물 기반 소통 원칙 (P8). 1부에 canonical 등재 → 2부 한 줄기 매핑 → 4부 종착(worklog 2-layer). draft directives §2.

---

## 2. Key Findings Summary — 매뉴얼이 전달할 핵심 명제

> 매뉴얼 전체가 떠받치는 명제 5종. 각 명제에 근거 강도(★단정 가능 / ▲caveat 동반)를 표시.

| # | 핵심 명제 | 근거 강도 | 1차 카드 |
|---|---|---|---|
| **M1** | 세대는 대체가 아니라 **누적 layer** — loop⊃harness⊃context⊃prompt, 각 세대가 이전 세대의 미해결분을 흡수 | ★ (모든 1차 출처 합의) | `[osmani-loop-engineering]` `[greyling-loop-engineering]` |
| **M2** | **산출물 기반 소통** — agent 는 context 공유가 아니라 filesystem 산출물로 소통한다 (amnesiac agent + durable filesystem). 우리 세팅의 관통 철학 | ★ | `[osmani-long-running-agents]` `[humanlayer-12-factor-agents]` `[anthropic-effective-harnesses]` |
| **M3** | **자기채점 불가 → maker/verifier 분리** — model 은 "pathological optimists", 산출 agent ≠ 채점 agent | ★ (가장 강한 합의) | `[anthropic-harness-design-long-running-apps]` `[epsilla-gan-style-agent-loop]` |
| **M4** | **harness 가 행동을 결정** (Agent = Model + Harness) — 단 가치는 model 강해질수록 감쇠 (inversion) | ▲ (감쇠론 caveat·Greyling 2차 수치) | `[osmani-agent-harness-engineering]` `[greyling-agent-model-harness]` |
| **M5** | **변경은 배포 전 eval 로 검증** — "A markdown edit without a before/after eval is a vibe", golden set 회귀 | ★ (단 infra noise·Goodhart caveat) | `[braintrust-eval-driven-development]` `[anthropic-demystifying-evals]` |
<!-- memo: [COVERAGE] M5 의 verbatim "A markdown edit without a before/after eval is a vibe" 의 실제 출처는 `[greyling-configured-not-coded]` (cards 확인: Quotable 3 "A markdown edit without a before/after eval is a vibe", + "model is rented, harness is owned", Tension (e) configuration 세대 규율 격차). 1차 카드 칸이 이 verbatim 의 출처 카드를 누락하고 braintrust/demystifying 만 적었다. M5 verbatim 이 우리 세팅의 P6/drill 회귀 철학과 직결되는 관통 인용인데 그 출처 카드(`greyling-configured-not-coded`, tier 2 named-source)가 strategy 전체에서 단 한 번도 인용되지 않는 orphan. M5 1차 카드 칸에 `[greyling-configured-not-coded]` 추가하고, draft 에서 이 verbatim 은 Greyling(정리·대중화자) 귀속으로 표기. -->


> 매뉴얼의 _서사 골격_ = M1 (세대사 프레임) 위에 M2~M5 (패턴 합의) 가 걸리고, 2부가 이 5 명제 각각을 우리 실물 anchor 로 내린다. M2 가 비중 최대 (directive §2).

---

## 3. Analysis Framework — 4부 구성 논리

### 3.1 4부 흐름: 원칙 → 실물 → 실전 → 노트

```
1부 원칙 (업계 망라)  →  2부 매핑 (우리 실물)  →  3부 실전 (발화)  →  4부 노트 (산출물 종착)
  research 근거          라이브 파일 anchor       CLAUDE.md 트리거     prd.md + notes/ 실물
  "무엇이 원칙인가"      "어디에 녹았나"          "이 상황엔 이 발화"  "산출물을 어떻게 다시 찾나"
```

- **1부 → 2부**: 1부 패턴 P1~P11 각각이 2부 매핑 표의 행이 된다. 1.5 다리 절이 명시 연결.
- **2부 → 4부 관통선 (M2 산출물 소통)**: `.agent_reports`=통신 버스 → plan/dev_logs 핸드오프 → pipeline_state 재개 → 3-tier(T1 사용자/T3 기계) → headless 분사(프로세스 경계를 산출물이 넘음) → worklog 2-layer. 이 한 줄기가 1부 P8 → 2부 → 4부 를 꿰뚫는다.

### 3.2 lookup 최적화 설계 원칙

- **절 독립성**: 각 절은 단독으로 읽혀도 의미가 닫히게. cross-section 중복은 canonical site + cross-ref 로 압축 (Paragraph Cohesion 참조).
- **표 anchor**: 매핑·tier·발화 시나리오는 표로 — 본문 산문보다 표가 lookup 빠르다.
- **anchor 형식 일관**: 1부 카드 `[card-slug]`, 2~4부 라이브 `파일경로 §절번호`. drift 추적 가능하게.

### 3.3 Paragraph Cohesion — P8(산출물 소통) 3중 등장 처리

P8 산출물 소통이 1부·2부·4부 세 곳에 걸친다. canonical site 를 **1부 P8** 로 정하고:
- 1부 P8: 원칙 정의 + verbatim (canonical — 전체 서술).
- 2부: 우리 실물 매핑만 (`.agent_reports` 통신 버스 한 줄기) — 원칙 재설명 금지, "1부 P8 의 원칙이 우리 세팅에선…" cross-ref.
- 4부: 종착점만 (worklog 2-layer 가 P8 줄기의 끝) — cross-ref.

draft 시 새 절 설계마다 4-step (중복 확인 → 단락 축 → cross-section 중복 → EDIT/REPLACE/INSERT/DROP 분류) 적용.

---

## 4. Section Plan — 4부 절 단위 outline

### 4.1 1부 — 원칙의 세대사 (골격: `06_implementation.md` §1 채택)

> `06_implementation.md` §1 outline 을 **그대로 채택·구체화** (재발명 금지). 패턴 11종 상세는 `04_technical_deep_dive.md` 의 문제→verbatim→메커니즘→정량→반론 구조 유지.

| 절 | 내용 | 1차 카드 (citation map `06` §4) | 강도 |
|---|---|---|---|
| **1.0 들어가며 — 왜 세대사인가** | 핵심 프레임: 세대는 누적 layer (loop⊃harness⊃context⊃prompt). Karpathy "Prompt engineering walked so context engineering could run" | `[osmani-loop-engineering]` `[greyling-loop-engineering]` | ★ |
| **1.1 Gen0→Gen1: prompt→context** | prompt engineering 한계(production 신뢰성) → context engineering 등장. context rot·attention budget·compaction·just-in-time. 명명 = Osmani+Anthropic 공동 | `[osmani-context-engineering]` `[anthropic-effective-context-engineering]` | ★ |
| **1.2 Gen2: harness engineering** | "the other half of the system", Agent=Model+Harness. **Trivedy 가 용어 coined**. self-aware caveat (harness 는 model 개선 시 축소) | `[osmani-agent-harness-engineering]` `[anthropic-effective-harnesses]` `[anthropic-harness-design-long-running-apps]` `[greyling-agent-model-harness]` | ★ (감쇠론 ▲) |
<!-- memo: [COVERAGE] 1.2 harness 절의 tier-2 정리 카드 `[greyling-rise-of-harness-engineering]` 가 strategy 전체 orphan. analysis_summary §1 Gen2 가 이 카드를 "harness 를 SDK/Framework/Scaffolding 위 4번째 architectural layer 로 정리 (Schmid OS analogy, parallel.ai 6-component, framework→harness collapse 80/20)" 로 명시 — 1.2 절의 "정리·대중화" 측 1차 정리 출처다. 1.2 셀이 greyling-agent-model-harness(감쇠론) 만 Greyling 으로 인용하고 정작 harness 세대 정리의 메인 카드를 빠뜨렸다. 1.2 셀에 `[greyling-rise-of-harness-engineering]` 추가 (Greyling=정리자 귀속 유지). -->
| **1.3 Gen3: loop engineering** | "replacing yourself as the person who prompts the agent". **Osmani 명명** / Steinberger·Cherny 슬로건 / Greyling 정리. 실증: C compiler 16-Claude. 경계: "loop changes the work, it does not delete you from it" | `[osmani-loop-engineering]` `[anthropic-c-compiler-parallel-claudes]` `[greyling-loop-engineering]` | ★ |
<!-- memo: [COVERAGE] 1.3 loop 절의 tier-2 카드 `[greyling-loop-engineering-playbook]` orphan. analysis_summary §1 Gen3 가 이 카드를 "runtime tiering — Tier A terminal / Tier B platform / Tier C editor" 의 출처로, 6-block 구조와 함께 loop 세대 정리의 보조 1차로 등재. 1.3 셀이 greyling-loop-engineering 만 인용하고 playbook(runtime tiering) 을 빠뜨렸다. loop 세대 서술에서 6-block + runtime tiering 을 다루려면 playbook 셀 추가 권장 (🟡 — 6-block 만 다루면 greyling-loop-engineering 단독으로 충분, runtime tiering 까지 쓰면 playbook 필수). -->

| **1.4 패턴 카탈로그 (P1~P11)** | GoF 식 named pattern. 각각 문제→원칙(verbatim)→메커니즘→반론. P8 안에 **산출물 소통 원칙 canonical 등재** | `04_technical_deep_dive.md` 카드 매핑 그대로 | 표 4.1a |
| **1.4-T Tensions (4종)** | 패턴 뒤 별도 절, 균형 서술 (①④ 필수 반론 동반) | `[cognition-*]` `[mindstudio-*]` `[greyling-agent-model-harness]` `[arxiv-evaluating-agents-md]` | ▲ |
| **1.5 우리 시스템 매핑 다리** | 1부=분야 망라, 2부=우리 세팅. draft 시점 라이브 Read 강제 명시 | — | — |

**표 4.1a — 패턴 11종 절별 1차 카드·강도** (`04_technical_deep_dive.md` + `06` §4 citation map):

| 패턴 | 1차 카드 | 강도 (`04` Takeaway) |
|---|---|---|
| P1 plan-then-execute | `[anthropic-claude-code-best-practices]` `[owainlewis-spec-driven]` `[osmani-good-spec]` | ★ (작은 작업 plan skip caveat) |
| P2 spec-driven | `[github-spec-kit]` `[owainlewis-spec-driven]` `[osmani-good-spec]` | ★ (over-spec caveat) |
| P3 maker-verifier | `[anthropic-harness-design-long-running-apps]` `[epsilla-gan-style-agent-loop]` `[mindstudio-planner-generator-evaluator]` | ★ (GAN caveat 필수) |
<!-- memo: [COVERAGE] P3 셀에 일반화 사례 카드 누락 — analysis_summary §2 P3 "일반화" 항목: `[anthropic-managed-agents]` (brain/hands 분리)·`[anthropic-multi-agent-research-system]` (CitationAgent 별도 검증)·`[willison-agentic-engineering-patterns]` (tier 1 ○중요, Red/green TDD). 앞 둘은 다른 셀(P8/P4)에서 이미 인용되므로 P3 일반화 서술 시 cross-ref 가능하나, willison 은 strategy 전체 orphan — TDD red/green 이 maker-verifier 의 가장 친숙한 일반화 비유라 P3 서술의 도입 사례로 유용. 🟡 (canonical 3 종으로 P3 단정은 충분, willison 은 일반화 backing). -->

| P4 서브에이전트 | `[anthropic-multi-agent-research-system]` `[cognition-dont-build-multi-agents]` `[cognition-multi-agents-working]` | ▲ (read/write 축 종합) |
<!-- memo: [COVERAGE] P4 셀에 `[openai-practical-guide-agents]` (tier 1 ○중요, Manager/Decentralized pattern, single-agent first) 누락. analysis_summary §3 Tension (a) read/write 종합이 Anthropic·Cognition×2 에 더해 OpenAI 의 single-agent-first 를 합의점 #4 의 한 축으로 인용 — P4 의 "단순하게 시작" 측 제3 1차 출처. 단 verbatim 은 PDF parse 실패 2차 경유(§5.3 Gap·Risk 명시)라 verbatim 직접 인용 대신 pattern 명칭(Manager/Decentralized) 수준 인용으로 제한. P4 셀 추가 권장. -->

| P5 파이프라인 세분화 | `[anthropic-building-effective-agents]` `[github-spec-kit]` | ★ |
| P6 golden set | `[anthropic-demystifying-evals]` `[braintrust-eval-driven-development]` `[anthropic-infrastructure-noise]` | ★ (noise floor caveat) |
<!-- memo: [COVERAGE] P6 셀에서 `[redhat-eval-driven-development]` (tier 3, 8-stage·"known bad" set·judge calibration·single-big-prompt overfit 폭로) + `[anthropic-ai-resistant-evals]` (tier 1 ○중요) 누락. analysis_summary §2 P6 가 둘 다 P6 primary/구현 사례로 등재. redhat 은 "known bad" set 이 우리 drill cases (P7 케이스 승격) 와도 연결되는 구현 사례라 P6/P7 양쪽 anchor 후보. tier 3 이므로 tier 1 backing 동반 조건이면 추가, 단독 단정 X. -->

| P7 오답노트 승격 | `[osmani-agent-harness-engineering]` `[braintrust-eval-driven-development]` `[arxiv-agentic-context-engineering]` | ▲ (자동화는 tier 4 만) |
| **P8 상태 영속성·산출물 소통** | `[osmani-long-running-agents]` `[humanlayer-12-factor-agents]` `[anthropic-effective-harnesses]` `[anthropic-managed-agents]` | ★ **(canonical site — 비중 최대)** |
| P9 worktree | `[zylos-git-worktree-isolation]` `[anthropic-c-compiler-parallel-claudes]` `[anthropic-claude-code-sandboxing]` | ▲ (정량은 tier 3) |
| P10 headless·cron | `[claude-code-github-actions]` `[anthropic-claude-code-auto-mode]` `[mindstudio-headless-mode]` | ▲ (cron 디테일 tier 3) |
| P11 컨텍스트 절약 | `[anthropic-effective-context-engineering]` `[anthropic-code-execution-mcp]` `[anthropic-advanced-tool-use]` `[redis-context-compaction]` | ★ (수치는 카드 명시값만) |
<!-- memo: [COVERAGE] P11 셀에서 `[anthropic-agent-skills]` (progressive disclosure 1차 — 2부 2.6 "skill progressive disclosure" 매핑의 1부 앵커) + `[anthropic-think-tool]` + `[factory-evaluating-compression]` (tier 2, "tokens per task"·probe-based eval) 누락. 특히 anthropic-agent-skills 는 progressive disclosure 의 정의 카드인데, 2부 2.6 이 "skill progressive disclosure" 를 우리 실물(skill 자동 description 주입)로 매핑하면서 1부 P11 에 그 원칙 앵커가 없으면 2부 cross-ref 대상이 사라진다. P11 셀에 `[anthropic-agent-skills]` 추가 권장. -->


> tier 4 카드는 절대 단독 근거 X — tier 1–2 의 정량 backing 으로만 동반 (Style Guide).
<!-- memo: [COVERAGE] tier 1 (○중요/△참고) orphan 카드 — 표 4.1a 패턴 매핑 어느 셀에도 citation 자리가 없는 1차 권위 카드: ① `[anthropic-writing-tools-for-agents]` (○중요, eval-driven tool 개선 — P6 또는 P11 backing) ② `[anthropic-ai-resistant-evals]` (○중요, saturation·contamination 저항 eval — P6 의 핵심 신뢰성 근거인데 P6 셀이 demystifying/braintrust/infra-noise 만 인용) ③ `[willison-agentic-engineering-patterns]` (○중요, Red/green TDD — P3 maker-verifier 일반화 사례) ④ `[openai-practical-guide-agents]` (○중요, Manager/Decentralized pattern — P4 셀이 anthropic+cognition 만, OpenAI 1차가 빠짐) ⑤ `[anthropic-agent-skills]` (△참고, progressive disclosure — P11 셀이 effective-context/code-exec/advanced-tool 만, skill disclosure 1차가 빠짐 — 2부 2.6 "skill progressive disclosure" 매핑의 1부 앵커가 됨) ⑥ `[anthropic-think-tool]` (△참고, P11). 표 4.1a 가 "04 카드 매핑 그대로" 로 위임하긴 하나, 위 6종은 04 deep-dive 의 해당 패턴 절에 실재하므로 draft 가 04 를 베끼면 자동 포함될 여지는 있다. 다만 ②④ 는 P6/P4 의 합의 강도를 떠받치는 1차라 strategy 표 셀에 명시 추가 권장 (특히 ④ OpenAI 는 P4 read/write tension 의 제3 1차 출처). ①③⑤⑥ 는 draft 위임으로 충분 (🟡). -->


### 4.2 2부 — 우리 세팅 매핑

> 일관된 질문 (directive §6): **"요즘 쏟아지는 에이전트 코딩 원칙들이 우리 세팅에 어디에 어떻게 녹아 있나"**. ref_analysis.md §1 의 매핑 축을 출발점으로, draft 시점 라이브 파일을 직접 Read 해 실제 절 번호·실명 anchor 를 박는다 (기억·요약 인용 금지).

**표 4.2a — P1~P11 × 실물 매핑 (라이브 anchor 확정)**:

| 패턴 | 우리 실물 | 라이브 anchor |
|---|---|---|
| **P1/P2** (plan·spec 분리) | 하드 순서 게이트 (research→spec→code), 신규 산출물 생성 순서 기계 강제 | `WORKFLOW.md §0(a)` 하드 순서 게이트 · `CLAUDE.md §0(0)` · `hooks/artifact-guard.sh` (PreToolUse Edit/Write — 신규 산출물 생성 순서만) · `hooks/spec-skill-gate.sh` + `hooks/spec-read-marker.sh` (prd.md 실제 Read 마커 검증 게이트) |
| **P3** (maker-verifier) | 팀 분업 critic·verifier + QA 5단계 + Stage D.5 편집팀 polish (2026-06-11 신설) <!-- memo: [FACT] autopilot-draft/SKILL.md 실명은 "Step 5.5" (not "Stage D.5") — draft 에서 라이브 파일 anchor 따라 "Step 5.5" 로 표기 요망. --> | `CONVENTIONS.md §1.1` QA 5단계 (quick~adversarial) · `§2` agent model 매트릭스 (연구팀·품질관리팀·편집팀·디자인팀) · adversarial = thorough + codex-review-team + 연구팀 claim-verify (`§1.1`·`§3` invariant 2) |
| **P4** (서브에이전트) | orchestrator=main 고정, read 병렬 / write 브랜치 single-thread, **중첩 1단 한계** | `CONVENTIONS.md §5.10` 작업 격리·병렬 디스패치 (Agent 툴 중첩 1단 — 서브에이전트엔 Agent 툴 미노출) |
| **P5** (파이프라인 세분화) | autopilot-* 4트랙 파이프, sub-skill 단계 | `WORKFLOW.md §1` 4트랙 청사진 · `§5` entry→서브에이전트 분기 · `CONVENTIONS.md §6.2` 호출 흐름 3패턴 |
| **P6** (golden set) | 모의훈련(drill) 루프 (지침 회귀 테스트, g0 세팅 세금 ~40k) | `loops/README.md` 현역 표 (모의훈련(drill) — 사건형) · `CLAUDE.md` 도메인 트리거 (지침 파일 수정 후 drill/run.sh) |
| **P7** (오답노트 승격) | post-it sweep·졸업, feedback 메모리→지침 승격, 당직 발견→triage, 케이스 승격(오답노트→drill) | `loops/README.md` "케이스 승격" 절 · 당직(oncall) 발견 보고 · `CONVENTIONS.md §3` invariant 6 (의도 동반·drill 케이스가 최상위 보존) |
| **P8** (상태·산출물 소통) | **`.agent_reports`=통신 버스 → plan/dev_logs 핸드오프 → pipeline_state 재개 → 3-tier → headless 분사 → worklog 2-layer** (한 줄기) | `CONVENTIONS.md §5` 3-tier T1/T2/T3 · `§5.4` skill별 폴더 매핑 · `§5.8` pipeline lock (worktree 공유 가드) · `§5.10` headless 분사 (cross-ref → 4부) |
| **P9** (worktree) | §5.10 본작업 브랜치 강제, 머지 시점 게이트, git 상태 preflight | `CONVENTIONS.md §5.10` 규모 분기·디스패치 규칙 · `§5.9` git working-state preflight (STOP/WARN/DONE-BRANCH) · `hooks/git-state-guard.sh` (merge/rebase 중 편집 hard deny — drill g2) |
| **P10** (headless·cron) | loops 4종 + `claude -p` 디스패치 + 디스패치 등록부 | `loops/README.md` 계층 표 (L1~L4, 초→분→일→주) · 현역 4종 (당직(oncall) / 일지(note) / 모의훈련(drill) / 연수(study)) · `CONVENTIONS.md §5.10` job 레지스트리 (`.dispatch/jobs.log`) |
| **P11** (컨텍스트 절약) | 얇은 CLAUDE.md 부트스트랩, on-demand Read, skill progressive disclosure | `CLAUDE.md` 헤더 (얇은 부트스트랩·WORKFLOW on-demand Read) · `WORKFLOW.md §0` (지침 기반 on-demand·hook 주입 아님) · user_profile lazy 로드 |

**2부 절 구성**:
- **2.0 매핑의 원리** — "원칙이 어디에 녹나" 질문 + 라이브 anchor 형식 안내 + drift 주의 (이 표는 작성 시점 스냅샷).
- **2.1 파이프 철학 (하드 순서 게이트)** — P1/P2/P5 묶음. research→spec→code 단방향, artifact-guard 가 _생성 순서만_ 강제·기존 편집/소스는 convention. spec-skill-gate + read-marker = "인용 ≠ 읽기" 검증 게이트.
- **2.2 팀 분업·QA 5단계** — P3. 팀 6종 × 모드, QA quick~adversarial 5단계, Stage D.5 편집팀 polish.
- **2.3 산출물 통신 버스 (M2 관통선)** — P8. `.agent_reports` 통신 버스 한 줄기 (canonical 은 1부 P8, 여기선 우리 실물만). 3-tier·핸드오프·pipeline_state·headless 분사가 _가능한 이유_(프로세스 경계를 산출물이 넘음). **비중 최대**.
- **2.4 worktree·병렬 디스패치** — P4/P9. §5.10 2모드 (경량 팀 위임 / 풀 ceremony headless 분사). **directive §3 헤드리스 사례**: Agent 툴 중첩 1단 제한 vs `claude -p` 프로세스 분사 우회 (2026-06-11 실증, §5.10). 머지 시점 게이트·git-state preflight.
- **2.5 loops 4종 + hooks 6종** — P6/P7/P10. 루프 L1~L4 계층 (초·분·일·주), 현역 4종. hooks 6종 역할 표.
- **2.6 컨텍스트 절약 규율** — P11. 얇은 부트스트랩·on-demand·progressive disclosure.

**표 4.2b — hooks 6종 역할** (라이브 헤더 확인):

| hook | trigger | 역할 | 매핑 패턴 |
|---|---|---|---|
| `artifact-guard.sh` | PreToolUse(Edit/Write/MultiEdit) | `.agent_reports` 산출물 _생성 순서_ 강제 (📌tracked / ⚡untracked 우회) | P1/P2 |
| `spec-skill-gate.sh` | PreToolUse(Skill) | spec-backed cwd 에서 prd.md 실제 Read 마커 없으면 autopilot-code/spec/note DENY | P1/P2 |
| `spec-read-marker.sh` | PostToolUse(Read) | prd.md Read 시 세션 마커 + mtime 기록 (gate 통과 증거) | P1/P2 |
| `git-state-guard.sh` | PreToolUse(Edit/Write/MultiEdit/NotebookEdit) | merge/rebase/cherry-pick 진행 중 편집 DENY (drill g2, 2026-06-11) | P9 |
| `design-postwrite.sh` | PostToolUse(Edit/Write/MultiEdit) | DESIGN HTML 저장 시 headless 렌더 + console error alert | (디자인 트랙 — 보조 언급) |
| `herdr-agent-state.sh` | (herdr 설치) | 외부 integration 관리 (herdr) | (외부 — 보조 언급) |

**directive §4 — 2026-06-11 신설분 반영 (라이브 확인)**:
- 연수(study) 루프 — `loops/README.md` 현역 표 (cron 일요일 06:17, 외부 동향 × 현 세팅 → 개선 제안서 + g0 세금 추세).
- 일지(note) 개명 — `loops/README.md` (이전 명칭 → note, cron 05:03).
- Stage D.5 편집팀 polish — 2부 2.2 에 반영.
- 디스패치 등록부 — `CONVENTIONS.md §5.10` job 레지스트리 (`.dispatch/jobs.log`, 당직 7호 감시).
- 머지 시점 게이트 — `CONVENTIONS.md §5.10` 규칙 3 (self-merge 금지, 머지 신호/수확 자리만).
- g0 세팅 세금 ~40k — `CONVENTIONS.md §5.10` 풀 ceremony 주의 ② + `loops/README.md` 연수 (g0 세금 추세 보고).

### 4.3 3부 — 입문·실전 가이드 (발화 중심)

> 형식: "이 상황엔 이 발화". 근거 = `CLAUDE.md` 도메인 트리거 표 + `WORKFLOW.md §7` + `loops/README.md` 발화 규약. 외부 원칙 인용 최소 — 실전 절차가 주.

**표 4.3a — 발화 시나리오**:

| 상황 | 발화 | 무슨 일 | 라이브 anchor |
|---|---|---|---|
| 아침 당직 처리 | `당직 처리` / `당직 보고` | 최신 당직(oncall) 보고 Read → 발견별 triage 제안 → 승인분 실행 | `CLAUDE.md` 도메인 트리거 (당직 보고 처리) · `notes/oncall/<date>.md` |
| 새 작업 라우팅 | 트랙별 첫 발화 (자연어 한 줄) | WORKFLOW 작업-본질 매핑 → 옵션 자동 구성 → 한 번 컨펌 → invoke | `CLAUDE.md §0(B)` 호출 패턴 · `WORKFLOW.md §2` 작업 본질 매핑 |
| 병렬 디스패치 | 작업 중 새 독립 요청 | 파일 겹침 triage → 새 worktree background 분사 (겹치면 큐잉) | `CONVENTIONS.md §5.10` 디스패치 규칙 1~2 |
| 사후 수정 (spec-backed cwd) | 기존 프로젝트 수정·기능 요청 | prd.md 실제 Read → spec-drift 체크 → autopilot-spec update (필요 시) → autopilot-code --qa quick | `WORKFLOW.md §7` · `CLAUDE.md`(프로젝트) 도메인 트리거 (spec-skill-gate 하드 게이트) |
| 모의훈련 발사 | 지침 수정 후 / `drill/run.sh` | fixture 가상 상황 headless 시험·채점, FAIL 시 수정안 | `loops/README.md` 현역 (모의훈련(drill) 사건형) · `CLAUDE.md` 도메인 트리거 |
| 연수 | (cron 자동) 일요일 06:17 / 제안 채택 | 외부 동향 조사 → 세팅 대조 → 개선 제안서 → 채택 서명 → 적용 → 모의훈련 | `loops/README.md` 현역 (연수 study) |
| post-it handoff | context ~50%+ / wind-down / 작업 완료 | `/post-it handoff` 제안 (sweep 자동 포함) → 요약 보여주고 저장 여부 confirm | `CLAUDE.md §2` context nudge · post-it SKILL |
| 케이스 승격 | `이거 drill 케이스로 박아` | 실사고 상황을 fixture 로 재현 → drill/cases/ 추가 | `loops/README.md` "케이스 승격" 절 |

**3부 절 구성**: 3.0 들어가며(발화 중심 안내) → 3.1 하루 일과 흐름(일지→당직→작업→모의훈련→연수, F7) → 3.2~3.8 위 표 시나리오별 절.
<!-- memo: [STRUCTURE] 3부 시나리오 절 순서(3.2~3.8)가 "위 표 순서대로" 인데, 표 4.3a 는 하루 일과 시간순(당직→라우팅→디스패치→사후수정→모의훈련→연수→post-it→케이스)에 가깝다. lookup 참조서에선 _사용 빈도순_ 이 lookup 을 빠르게 한다(독자가 가장 자주 찾는 발화가 앞). 실제 빈도: ① 새 작업 라우팅(매 작업, 최빈) ② post-it handoff(매 세션 wind-down, 고빈도 — 현재 7번째로 후미) ③ 아침 당직 처리(일 1회) ④ 사후 수정(spec-backed cwd, 빈번) ⑤ 병렬 디스패치 ⑥ 케이스 승격(이벤트성) ⑦ 모의훈련 발사(지침 수정 후) ⑧ 연수(주 1회, 최저빈). 3.1 하루 일과 흐름은 시간순 서사가 맞으나, 3.2~3.8 개별 lookup 절은 빈도순(라우팅·post-it 을 앞으로, 연수를 뒤로) 재배열 권장. 특히 post-it handoff 가 매 세션 발생하는데 표·절 모두 후미라 lookup 동선과 어긋남. 🟡 -->


### 4.4 4부 — worklog-board 활용 (에이전틱 노트)

> 근거: worklog-board `spec/prd.md` 2-Layer 아키텍처 (§2) + `notes/` 실물 2-layer 구조. P8 산출물 소통 줄기의 **종착점** (directive §2 끝 항목 — cross-ref from 1부 P8 / 2부 2.3).

**표 4.4a — 2-layer 실물**:

| layer | 위치 | 주인 | 단위 | 라이브 anchor |
|---|---|---|---|---|
| **Layer 1** | `notes/cards/` (82 cards 실재) | 사용자 (보드 직접 생성) | `kind: task` · `kind: project` 카드 | `worklog-board/spec/prd.md §2` 2-Layer · `§2.1`(task)·`§2.2`(project) |
| **Layer 2** | `notes/_layer2/` (backbones·tasks·papers·notes 4 디렉터리 실재) | 에이전트 (autopilot-note 정리) | 산출물 노트화 row + 카탈로그 | `prd.md §2`·`§4` autopilot-note 흐름 · `§2.3`(backbone) |
| 연결 다리 | `_layer2/notes/<id>.md` row | — | `card_id`(→L1) + `backbone_ids`·`task_ids`·`paper_id`(→L2) | `prd.md §2` 연결 고리 · `§2.5` 관계형 DB 분해 (soft ref card_id) |
| 부속 | `notes/digests/` · `notes/oncall/` · `notes/_triage/` | 에이전트 / 루프 | 다이제스트 · 당직(oncall) 보고 · triage 제안 큐 | `notes/README.md` · `loops/README.md` (일지(note)·당직(oncall) 산출) |

**4부 절 구성**:
- **4.0 왜 에이전틱 노트인가** — P8 종착점. "쏟아지는 산출물 md 를 하나하나 안 읽고도 따라가고 다시 찾기" (`prd.md` 제품 비전 v18).
- **4.1 2-Layer 아키텍처** — L1(사용자 소유)·L2(에이전트 정돈)·연결 다리(card_id soft ref). 경계 규칙 = 에이전트는 L1 직접 못 건드림 (제안만).
- **4.2 실물 구조** — `notes/cards/`·`_layer2/`·`digests/`·`oncall/`·`_triage/`. autopilot-note 흐름 (산출물 → L2 notes row → card_id 연결 → 매칭 없으면 신규 카드 triage 제안).
- **4.3 진행 줄 마커·triage 운영** — `✓`(보고 가능)·`-`(내부)·`×`(private), 아침 triage 한 글자 조정.
- **4.4 산출물 소통의 닫힘** — 줄기의 _끝점만_ 명시(worklog 2-layer 가 P8 줄기의 종착)하고, 전체 줄기(1부 P8 → 2부 2.3 → 4부) 회수는 cross-ref 로만. 닫힘 문장이 P8 전체 요약 재서술이 되지 않게 (canonical=1부 P8, 재서술 금지).

> 주의: prd.md 는 v2~v33 누적 (DB 전환 v21·홈 콕핏 v22 등 진행 중). 매뉴얼은 _현재 실재하는 실물_(notes/ 파일 구조 + prd 확정 결정)만 anchor, 미구현 vision(DB 마이그레이션 등)은 "진행 중" 으로 표시하고 단정 X.

---

## 5. Data & Evidence Inventory

### 5.1 카드 tier 표 요약 (`analysis_summary.md §2`)

| Tier | 정의 | 매뉴얼 사용 |
|---|---|---|
| **1** | 1차 권위 (Anthropic/Addy/Cognition/OpenAI/GitHub vendor·named-author 블로그) | 단정 서술 근거 |
| **2** | 정리·대중화 (Greyling 등 popularizer) | _명명 권위 아님_ — 원 출처로 거슬러 인용 |
| **3** | practitioner blog (peer-review 아님) | tier 3 명시 + caveat |
| **4** | arXiv 학술 보조 | **단독 근거 금지** — tier 1–2 정량 backing 으로만 |

### 5.2 라이브 파일 목록 (2~4부 anchor source, draft 시점 재Read)

| 파일 | 절 anchor 확정 | 사용 부 |
|---|---|---|
| `~/.claude/CLAUDE.md` | §0(라우팅·하드 게이트)·§1~3(응답 원칙)·도메인 트리거 표 | 2부·3부 |
| `~/.claude/CONVENTIONS.md` | §1.1(QA)·§2(model)·§3(invariant)·§5(3-tier)·§5.4·§5.8·§5.9·§5.10 | 2부 |
| `~/.claude/WORKFLOW.md` | §0(하드 게이트)·§1(4트랙)·§2(매핑)·§5(분기)·§7(사후 수정) | 2부·3부 |
| `~/.claude/loops/README.md` | 계층 표(L1~L4)·현역 4종·케이스 승격 | 2부·3부 |
| `~/.claude/hooks/*.sh` (6종) | 헤더 역할 (표 4.2b) | 2부 |
| `worklog-board/.claude_reports/spec/prd.md` | §2(2-Layer)·§2.1~2.5·§4(autopilot-note) | 4부 |
| `notes/` (cards 82·_layer2 4종·digests·oncall·_triage) | README + 실물 구조 | 4부 |

### 5.3 Gap (근거 얇은 자리 — `analysis_summary.md §5` + `04` 미해결 과제)

- **P7 자동화 메커니즘** — 자동 승격 알고리즘은 tier 4(ACE/SICA)만. 블로그 1차에 자동화 절차 부재 → 매뉴얼에서 "자동 승격" 단정 금지.
- **P9 worktree 정량 벤치** — 합의 강하나 정량은 tier 3(zylos/augmentcode), "four or more" cap 환경 의존.
- **P10 headless/cron 안전장치** — tier 1 은 docs + auto-mode(93%/17% FN)뿐, cron 디테일 tier 3 → verbatim 정밀도 약함.
- **GAN 메커니즘 근거** — autocomplete bias 는 tier 2 단일 출처 `[mindstudio-planner-generator-evaluator]` 만.
- **Harness-Bench 수치** — 76.2/52.4/23.8 등은 Greyling 경유 2차 인용 → arXiv 원문 대조 권장, 2차임을 명시.
- **누락 디렉터리** — `analysis_project/paper/`·`analysis_project/code/` 없음 (research-only 도메인, 정상). 2부~4부는 라이브 파일 직접 Read 로 보강 — 본 매뉴얼은 코드 분석 산출물에 의존 안 함.
<!-- memo: [COVERAGE] tier 4 arXiv orphan 카드 14종 (strategy 본문 미인용, 표 4.1a 가 "04 카드 매핑 그대로" 로 위임): arxiv-auditing-harness-safety · arxiv-code-as-agent-harness · arxiv-constitutional-spec-driven(−73%, P2 backing) · arxiv-context-eng-multi-agent · arxiv-eval-driven-iteration · arxiv-harness-bench(76.2/52.4/23.8, M4 backing) · arxiv-inside-the-scaffold(F9 figure) · arxiv-paace · arxiv-secure-plan-then-execute(P1) · arxiv-self-improving-coding-agent(17→53%, P7) · arxiv-sew · arxiv-skillreducer(+2.8%, P11) · arxiv-spec-driven-code-to-contract(P2). 이들은 tier 4(단독 근거 금지·backing 전용)라 strategy 표 미인용은 설계상 정상 — draft 가 04 deep-dive 의 패턴별 "보조(tier 4)" 줄을 채택하면 자동 backing 으로 들어온다. 단 정량값을 인용하는 4종(constitutional −73% / harness-bench 76.2 / self-improving 17→53% / skillreducer +2.8%)은 Style Guide·M4·§5.3 에 이미 명시돼 있으므로 draft 가 해당 수치 인용 시 출처 카드로 거슬러 표기할 것. 이 줄은 orphan 추적용 informational (🟢) — 추가 인용 자리 강제 아님. -->


---

## 6. Key Visuals — Figure 계획 (F1~F9)

> directive §1: 신규 F1~F7 = 자료팀 figure-gen 게이트 경유 (edge 교차 회피 — many-to-many 는 매트릭스 / 파이프라인은 단방향 레인, 납품 전 PNG Read 렌더 검수). embed = `<img width=500>`. F8~F9 = 기존 PNG 재인용.

| # | figure | 형태 | 소속 절 | 캡션 초안 |
|---|---|---|---|---|
| **F1** | 세대 4단 누적 타임라인 (2024-12~2026-06) | 단방향 레인 | 1.0 | "prompt → context → harness → loop: 각 세대는 이전 세대의 미해결분을 흡수하며 누적 layer 로 쌓인다" |
| **F2** | 패턴 11종 × 세대 매핑 | 매트릭스 | 1.4 | "11 실무 패턴이 어느 세대에서 파생했나 — maker-verifier 는 여러 갈래에서 수렴" |
| **F3** | 자율 실행 안전장치 4층 (permission→classifier→sandbox→hook) | 단방향 레인 | 1.4/2부 다리 | "자율성 ↑ 일수록 hard boundary 로 무게 이동 (84% sandboxing / 93% approve·17% FN)" |
| **F4** | 4트랙 파이프 구조도 | 단방향 레인 | 2.1 | "연구·실험 / 라이브러리·CLI / 문서 / 앱 — research→spec→code 하드 순서 게이트" |
| **F5** | 팀 분업 매트릭스 (팀 × 역할/모드) | 매트릭스 | 2.2 | "6 팀 × QA 모드 — maker(개발팀·기획팀) vs verifier(품질관리·연구·편집·디자인·codex)" |
| **F6** | 루프 4계층 (초·분·일·주) | 단방향 레인 | 2.5 | "L1 에이전트(초) → L2 과제(분) → L3 작업(일·당직/일지) → L4 메타(주·모의훈련/연수)" |
| **F7** | 하루 일과 흐름 (일지→당직→작업→모의훈련→연수) | 단방향 레인 | 3.1 | "새벽 cron(일지 05:03·당직 05:37) → 아침 처리 → 작업 디스패치 → 지침 수정 후 모의훈련 → 일요일 연수" |
| **F8** | 재인용: ACE context collapse | 기존 PNG | 1.1 | "monolithic rewrite 시 context 가 18,282→122 tokens 로 붕괴 (`figures/arxiv-agentic-context-engineering_fig2.png`)" |
| **F9** | 재인용: scaffold taxonomy | 기존 PNG | 1.2 | "13 OSS coding agent 의 3 layer × 12 dimension scaffold taxonomy (`figures/arxiv-inside-the-scaffold_fig1.png`)" |

> F2·F5 는 many-to-many → 매트릭스. F1·F3·F4·F6·F7 은 파이프라인·계층 → 단방향 레인. edge 교차 회피 (feedback memory: diagram_no_edge_tangle).

---

## 7. Risk & Limitations

- **drift 위험 (최대)** — 2~4부는 라이브 파일 anchor 에 묶여 있다. CLAUDE.md·CONVENTIONS·prd.md 가 바뀌면 매뉴얼이 stale. 대응: ① anchor 를 `파일경로 §절번호` 로 명시해 추적 가능 ② "작성 시점 스냅샷" 명시 ③ 일지(note) 루프가 publish 자리로 _라우팅_ 하고, 매뉴얼 stale 재갱신 자체는 별도 트랙(directive §5, 본 범위 밖) — 일지 루프 정의(전날 산출물 → worklog L2 노트화)에 매뉴얼 재갱신 책임은 포함되지 않으므로 단정 X.
- **라이브 출처 간 내부 명칭 drift** — 글로벌 `~/.claude/CLAUDE.md` 가 구명(당직 `scout`·모의훈련 `golden`·`notes/scout/`·`loops/golden/run.sh`) 표기를 유지 중인 반면, `loops/README.md` 는 신명(당직 `oncall`·모의훈련 `drill`·`notes/oncall/`·`drill/run.sh`)으로 이미 rename 됐다. **매뉴얼은 `loops/README.md` 실물(oncall/drill)을 진실로 채택**하고, CLAUDE.md 의 구명 drift 는 _별도 정정 대상_ 으로 둔다. 이 내부 불일치 자체를 매뉴얼에 등재하면 "라이브 §anchor 로 drift 추적" 이라는 매뉴얼의 핵심 가치를 _시연_ 하는 자산이 된다 (CLAUDE.md 구명 표기는 인용하지 않음). <!-- memo: [FACT] 2026-06-11 기준 ~/.claude/CLAUDE.md 는 이미 drill/oncall 으로 수정 완료 — "CLAUDE.md 가 구명 표기를 유지 중" 서술은 사실과 다름. draft 에서 이 Risk 항목을 "이미 해소된 사례" 로 재서술하거나 삭제 요망. Style Guide 루프 호칭 줄 "글로벌 CLAUDE.md 의 구명 scout/golden 은 인용하지 않는다" 도 해소됨 — 삭제 가능. -->
- **tier 약한 패턴 단정 금지** — P7(자동화)·P9·P10 은 tier 3/4 의존. caveat 동반, 출처 tier 명시. Tensions ①(서브에이전트 read/write)·④(context file 과다)는 반론 균형 필수.
- **Greyling 2차 인용** — Greyling 은 정리·대중화자(명명자 아님). material claim 은 원 출처로 거슬러 인용. Harness-Bench 수치는 Greyling 경유 2차임을 명시.
- **명명 권위 정확성** — context=Osmani+Anthropic 공동 / harness=Trivedy coined / loop=Osmani. 혼동 금지 (agent memory: research_agent_engineering_principles 균형 주의).
- **prd.md 진행 중 vision** — DB 전환(v21)·홈 콕핏(v22) 등 미구현. 실재 실물만 anchor, vision 은 "진행 중" 표시·단정 X.
- **OpenAI guide·codewithseb verbatim** — PDF binary / 403 차단으로 2차 경유. verbatim 인용은 원문 재확인 caveat.

---

## Style Guide

### 인용 규칙 (ground truth 단일 출처)

- **1부 카드**: `research/agent-engineering-principles/cards/*.md` 단일 출처. 표기 `[card-slug]`.
- **정량 수치**: 카드 명시값만 (90.2% / 15배 / 98.7% / 85% / 84% / 93% / 17% FN / 23.8pt / 6%p / −73% / +20% / +2.8% / 18,282→122 등). fabrication 금지 ("빈칸 > 잘못 채우기").
- **Harness-Bench 수치** (76.2/52.4/23.8/Codex 80.4 등): Greyling 경유 **2차 인용** 명시.
- **Greyling** = 정리·대중화자 (명명자 아님). material claim 은 원 출처로 거슬러 표기. **명명 권위**: context=Osmani+Anthropic 공동 / harness=Trivedy coined / loop=Osmani.
- **tier 4 (arXiv)**: 단독 근거 금지 — tier 1–2 의 정량 backing 으로만 동반.
- **caveat 강제**: P7(자동화)·P9·P10 은 tier 3/4 의존 caveat. Tensions ①④ 균형 서술.
- **2~4부 라이브 인용**: `파일경로 §절번호` anchor 형식 (예: `CONVENTIONS.md §5.10`, `prd.md §2`). 기억·요약 인용 금지 — 작성 시점 실제 Read.
<!-- memo: [STYLE] anchor 형식은 본문 전반 일관(`파일 §절` 형). 단 prd.md 가 본문에서 `prd.md §2`(축약, 3회) ↔ `worklog-board/spec/prd.md §2`(전체 경로, 1회) 로 혼용. 본 프로젝트 cwd 도 자체 `.agent_reports/spec/prd.md` 를 가질 수 있어(spec-backed) 축약형 `prd.md` 는 4부 절 독립성(절만 펴서 읽을 때)에서 어느 prd 인지 모호. 표기 규칙에 "prd.md 첫 등장·각 절 첫 인용은 `worklog-board/.claude_reports/spec/prd.md` 전체 경로, 이후 같은 절 내 축약 허용" 추가 권장. 🟢 -->

### 표기 규칙

- **한국어 본문 + 영어 굳은 용어 그대로**: harness · loop · worktree · headless · spec · context · prompt · maker-verifier · golden set · orchestrator · sub-agent · pipeline · scaffold · hook · cron · token · context rot · attention budget · just-in-time · compaction · 3-tier · plan-then-execute · spec-driven 등.
- **비표준·내부 약자 첫 등장 풀이**: 표준 약자라도 한 응답 첫 등장 시 1회 풀이 (예: QA(quality assurance), FN(false negative)). 같은 개념은 같은 표기.
- **고유명사 영어 원어**: 논문/블로그 제목·저자명·venue·모델명·데이터셋명·메트릭명·코드 식별자·파일 경로.
- **루프 호칭**: 한국어+ASCII 병기 — 당직(oncall)·일지(note)·모의훈련(drill)·연수(study). 실물 경로는 `notes/oncall/`·`drill/run.sh`·`drill/cases/`. 글로벌 CLAUDE.md 의 구명 `scout`/`golden`(및 `notes/scout/`·`loops/golden/run.sh`)은 인용하지 않는다 — `loops/README.md` 실명이 진실.
- **figure embed**: `<img width=500>` (미리보기 수준, 통합 PPTX + 개별 PNG — feedback: figure_combined_pptx_only).
- **다이어그램**: many-to-many 는 매트릭스, 파이프라인은 단방향 레인, 납품 전 PNG 렌더 검수 (feedback: diagram_no_edge_tangle).

### 톤

- 참조서 — 평어·개조식 허용 (보고서 라벨·표). 친절 안내체(`~해 드릴게요`) 금지. marketing 어조 금지. administrative 어조도 아님.
- lookup 최적화 — 절 독립성·표 anchor. 배경 설명 최소.

### Paragraph Cohesion 규칙

- P8(산출물 소통)의 canonical site = 1부 P8. 2부 2.3·4부 4.4 는 cross-ref 로 압축 (원칙 재서술 금지).
- 새 절 설계마다 4-step: 중복 확인 → 단락 축 → cross-section 중복 → EDIT/REPLACE/INSERT/DROP 분류.
