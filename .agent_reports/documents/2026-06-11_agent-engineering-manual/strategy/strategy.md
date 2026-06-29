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
changelog:
  - version: v2
    date: 2026-06-11
    note: |
      draft-refine pipeline — quality review 11 memo + factcheck 3 memo 반영 (applied 13 / overridden 0).
      [§7 Risk] [verified ~/.claude/CLAUDE.md]: "CLAUDE.md 구명 scout/golden 유지 중" 서술 근거 소멸(이미 drill/oncall 갱신 완료) — 이력형 "작성 시점 재확인" 서술로 재작성.
      [Style Guide] [verified ~/.claude/CLAUDE.md]: 루프 호칭 "구명 인용 금지" 줄 삭제 — drift 해소됨, live Read 재확인 안내로 대체.
      [§4.2 P3 / 2.2 / directive §4] [verified autopilot-draft/SKILL.md L808]: "Stage D.5" → 실명 "Step 5.5 (Editorial polish)" 교정.
      [§4.3 표 4.3a / directive §4] [verified CONVENTIONS.md §5.10]: "규칙 3"·"규칙 1~2" 검증불가 번호 라벨 → 서술형 anchor.
      [§2 M5] [verified greyling-configured-not-coded + analysis_summary §3 #5]: verbatim "markdown edit ... is a vibe" 출처 카드 추가.
      [§4.1 1.2/1.3] [verified greyling-rise-of-harness-engineering·loop-engineering-playbook + analysis_summary §1]: harness 4th-layer 정리·loop runtime tiering 카드 추가.
      [표 4.1a P3/P4/P6/P11] [verified willison·openai·ai-resistant·redhat·agent-skills·think-tool 카드 + analysis_summary §2/§3]: orphan tier-1/3 카드 셀 인용 보강 (writing-tools 는 backing 으로 prose 위임).
      [§4.3 STRUCTURE] [verified review_quality 축3]: 표 4.3a·3.2~3.9 절을 lookup 빈도순(라우팅·post-it 앞) 재배열, 3.1 하루 흐름은 시간순 서사 유지.
      [Style Guide] [verified review_quality 축2]: prd.md 첫 인용 전체경로 규칙 추가.
  - version: v1
    date: 2026-06-11
    note: |
      initial strategy — draft-strategy pipeline. 4부 매뉴얼 절 단위 설계도(원칙 세대사 → 우리 세팅 매핑 → 발화 실전 → worklog 노트), ground truth = research cards + 라이브 파일 anchor.
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
| **M5** | **변경은 배포 전 eval 로 검증** — "A markdown edit without a before/after eval is a vibe", golden set 회귀 | ★ (단 infra noise·Goodhart caveat) | `[greyling-configured-not-coded]` `[braintrust-eval-driven-development]` `[anthropic-demystifying-evals]` |


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
| **1.2 Gen2: harness engineering** | "the other half of the system", Agent=Model+Harness. **Trivedy 가 용어 coined**. harness=SDK/Framework/Scaffolding 위 4번째 architectural layer (Schmid OS analogy·parallel.ai 6-component·framework→harness 80/20 collapse — Greyling 정리). self-aware caveat (harness 는 model 개선 시 축소) | `[osmani-agent-harness-engineering]` `[anthropic-effective-harnesses]` `[anthropic-harness-design-long-running-apps]` `[greyling-rise-of-harness-engineering]` `[greyling-agent-model-harness]` | ★ (감쇠론 ▲) |
| **1.3 Gen3: loop engineering** | "replacing yourself as the person who prompts the agent". **Osmani 명명** / Steinberger·Cherny 슬로건 / Greyling 정리 (6-block 구조 + runtime tiering Tier A terminal/B platform/C editor). 실증: C compiler 16-Claude. 경계: "loop changes the work, it does not delete you from it" | `[osmani-loop-engineering]` `[anthropic-c-compiler-parallel-claudes]` `[greyling-loop-engineering]` `[greyling-loop-engineering-playbook]` | ★ |

| **1.4 패턴 카탈로그 (P1~P11)** | GoF 식 named pattern. 각각 문제→원칙(verbatim)→메커니즘→반론. P8 안에 **산출물 소통 원칙 canonical 등재** | `04_technical_deep_dive.md` 카드 매핑 그대로 | 표 4.1a |
| **1.4-T Tensions (4종)** | 패턴 뒤 별도 절, 균형 서술 (①④ 필수 반론 동반) | `[cognition-*]` `[mindstudio-*]` `[greyling-agent-model-harness]` `[arxiv-evaluating-agents-md]` | ▲ |
| **1.5 우리 시스템 매핑 다리** | 1부=분야 망라, 2부=우리 세팅. draft 시점 라이브 Read 강제 명시 | — | — |

**표 4.1a — 패턴 11종 절별 1차 카드·강도** (`04_technical_deep_dive.md` + `06` §4 citation map):

| 패턴 | 1차 카드 | 강도 (`04` Takeaway) |
|---|---|---|
| P1 plan-then-execute | `[anthropic-claude-code-best-practices]` `[owainlewis-spec-driven]` `[osmani-good-spec]` | ★ (작은 작업 plan skip caveat) |
| P2 spec-driven | `[github-spec-kit]` `[owainlewis-spec-driven]` `[osmani-good-spec]` | ★ (over-spec caveat) |
| P3 maker-verifier | `[anthropic-harness-design-long-running-apps]` `[epsilla-gan-style-agent-loop]` `[mindstudio-planner-generator-evaluator]` `[willison-agentic-engineering-patterns]` (Red/green TDD 일반화) | ★ (GAN caveat 필수) |

| P4 서브에이전트 | `[anthropic-multi-agent-research-system]` `[cognition-dont-build-multi-agents]` `[cognition-multi-agents-working]` `[openai-practical-guide-agents]` (Manager/Decentralized·single-agent first — verbatim 은 2차 경유, pattern 명칭 수준만) | ▲ (read/write 축 종합) |

| P5 파이프라인 세분화 | `[anthropic-building-effective-agents]` `[github-spec-kit]` | ★ |
| P6 golden set | `[anthropic-demystifying-evals]` `[anthropic-ai-resistant-evals]` `[braintrust-eval-driven-development]` `[anthropic-infrastructure-noise]` `[redhat-eval-driven-development]` (tier 3 구현 사례 — "known bad" set, P7 drill cases 연결, tier 1 backing 동반) | ★ (noise floor caveat) |

| P7 오답노트 승격 | `[osmani-agent-harness-engineering]` `[braintrust-eval-driven-development]` `[arxiv-agentic-context-engineering]` | ▲ (자동화는 tier 4 만) |
| **P8 상태 영속성·산출물 소통** | `[osmani-long-running-agents]` `[humanlayer-12-factor-agents]` `[anthropic-effective-harnesses]` `[anthropic-managed-agents]` | ★ **(canonical site — 비중 최대)** |
| P9 worktree | `[zylos-git-worktree-isolation]` `[anthropic-c-compiler-parallel-claudes]` `[anthropic-claude-code-sandboxing]` | ▲ (정량은 tier 3) |
| P10 headless·cron | `[claude-code-github-actions]` `[anthropic-claude-code-auto-mode]` `[mindstudio-headless-mode]` | ▲ (cron 디테일 tier 3) |
| P11 컨텍스트 절약 | `[anthropic-effective-context-engineering]` `[anthropic-agent-skills]` (progressive disclosure 1차 — 2부 2.6 cross-ref 앵커) `[anthropic-code-execution-mcp]` `[anthropic-advanced-tool-use]` `[redis-context-compaction]` `[anthropic-think-tool]` | ★ (수치는 카드 명시값만) |


> tier 4 카드는 절대 단독 근거 X — tier 1–2 의 정량 backing 으로만 동반 (Style Guide).
> tier 1 ○중요/△참고 orphan 보강 완료 — P3(willison Red/green TDD)·P4(openai Manager/Decentralized)·P6(ai-resistant·redhat)·P11(agent-skills·think-tool) 셀에 명시 인용. 잔여 backing 카드 `[anthropic-writing-tools-for-agents]` (eval-driven tool 개선) 은 P6/P11 서술의 보조 backing 으로 draft 에서 인용 (별도 셀 X — tool surface 측 보강).


### 4.2 2부 — 우리 세팅 매핑

> 일관된 질문 (directive §6): **"요즘 쏟아지는 에이전트 코딩 원칙들이 우리 세팅에 어디에 어떻게 녹아 있나"**. ref_analysis.md §1 의 매핑 축을 출발점으로, draft 시점 라이브 파일을 직접 Read 해 실제 절 번호·실명 anchor 를 박는다 (기억·요약 인용 금지).

**표 4.2a — P1~P11 × 실물 매핑 (라이브 anchor 확정)**:

| 패턴 | 우리 실물 | 라이브 anchor |
|---|---|---|
| **P1/P2** (plan·spec 분리) | 하드 순서 게이트 (research→spec→code), 신규 산출물 생성 순서 기계 강제 | `WORKFLOW.md §0(a)` 하드 순서 게이트 · `CLAUDE.md §0(0)` · `hooks/artifact-guard.sh` (PreToolUse Edit/Write — 신규 산출물 생성 순서만) · `hooks/spec-skill-gate.sh` + `hooks/spec-read-marker.sh` (prd.md 실제 Read 마커 검증 게이트) |
| **P3** (maker-verifier) | 팀 분업 critic·verifier + QA 5단계 + Step 5.5 편집팀 polish (2026-06-11 신설) | `CONVENTIONS.md §1.1` QA 5단계 (quick~adversarial) · `§2` agent model 매트릭스 (연구팀·품질관리팀·편집팀·디자인팀) · adversarial = thorough + codex-review-team + 연구팀 claim-verify (`§1.1`·`§3` invariant 2) · `autopilot-draft/SKILL.md` Step 5.5 (Editorial polish) |
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
- **2.2 팀 분업·QA 5단계** — P3. 팀 6종 × 모드, QA quick~adversarial 5단계, Step 5.5 편집팀 polish (`autopilot-draft/SKILL.md` Step 5.5).
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
- Step 5.5 편집팀 polish — 2부 2.2 에 반영 (`autopilot-draft/SKILL.md` Step 5.5: Editorial polish).
- 디스패치 등록부 — `CONVENTIONS.md §5.10` job 레지스트리 (`.dispatch/jobs.log`, 당직 7호 감시).
- 머지 시점 게이트 — `CONVENTIONS.md §5.10` 머지 정책 (self-merge 금지, 머지 신호/수확 자리만).
- g0 세팅 세금 ~40k — `CONVENTIONS.md §5.10` 풀 ceremony 주의 ② + `loops/README.md` 연수 (g0 세금 추세 보고).

### 4.3 3부 — 입문·실전 가이드 (발화 중심)

> 형식: "이 상황엔 이 발화". 근거 = `CLAUDE.md` 도메인 트리거 표 + `WORKFLOW.md §7` + `loops/README.md` 발화 규약. 외부 원칙 인용 최소 — 실전 절차가 주.

**표 4.3a — 발화 시나리오**:

| 상황 | 발화 | 무슨 일 | 라이브 anchor |
|---|---|---|---|
| 새 작업 라우팅 | 트랙별 첫 발화 (자연어 한 줄) | WORKFLOW 작업-본질 매핑 → 옵션 자동 구성 → 한 번 컨펌 → invoke | `CLAUDE.md §0(B)` 호출 패턴 · `WORKFLOW.md §2` 작업 본질 매핑 |
| post-it handoff | context ~50%+ / wind-down / 작업 완료 | `/post-it handoff` 제안 (sweep 자동 포함) → 요약 보여주고 저장 여부 confirm | `CLAUDE.md §2` context nudge · post-it SKILL |
| 아침 당직 처리 | `당직 처리` / `당직 보고` | 최신 당직(oncall) 보고 Read → 발견별 triage 제안 → 승인분 실행 | `CLAUDE.md` 도메인 트리거 (당직 보고 처리) · `notes/oncall/<date>.md` |
| 사후 수정 (spec-backed cwd) | 기존 프로젝트 수정·기능 요청 | prd.md 실제 Read → spec-drift 체크 → autopilot-spec update (필요 시) → autopilot-code --qa quick | `WORKFLOW.md §7` · `CLAUDE.md`(프로젝트) 도메인 트리거 (spec-skill-gate 하드 게이트) |
| 병렬 디스패치 | 작업 중 새 독립 요청 | 파일 겹침 triage → 새 worktree background 분사 (겹치면 큐잉) | `CONVENTIONS.md §5.10` 디스패치 규칙 (파일 겹침 triage·background 분사) |
| 케이스 승격 | `이거 drill 케이스로 박아` | 실사고 상황을 fixture 로 재현 → drill/cases/ 추가 | `loops/README.md` "케이스 승격" 절 |
| 모의훈련 발사 | 지침 수정 후 / `drill/run.sh` | fixture 가상 상황 headless 시험·채점, FAIL 시 수정안 | `loops/README.md` 현역 (모의훈련(drill) 사건형) · `CLAUDE.md` 도메인 트리거 |
| 연수 | (cron 자동) 일요일 06:17 / 제안 채택 | 외부 동향 조사 → 세팅 대조 → 개선 제안서 → 채택 서명 → 적용 → 모의훈련 | `loops/README.md` 현역 (연수 study) |

**3부 절 구성**: 3.0 들어가며(발화 중심 안내) → 3.1 하루 일과 흐름(일지→당직→작업→모의훈련→연수, F7 — 시간순 서사) → 3.2~3.9 발화 시나리오별 절(위 표 순서 = lookup 빈도순). 3.1 의 하루 흐름 서사(아침 당직 처리가 하루 첫 발화)는 시간축으로 두되, 개별 lookup 절(3.2~3.9)은 빈도순으로 둔다 — 가장 자주 찾는 발화(새 작업 라우팅·post-it handoff)가 앞, 저빈도(모의훈련·연수)가 뒤. 표 4.3a 도 같은 빈도순.


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
- **tier 4 arXiv orphan (정상 위임)** — arXiv 카드 14종(auditing-harness-safety·code-as-agent-harness·constitutional-spec-driven·context-eng-multi-agent·eval-driven-iteration·harness-bench·inside-the-scaffold·paace·secure-plan-then-execute·self-improving-coding-agent·sew·skillreducer·spec-driven-code-to-contract)은 tier 4(단독 근거 금지·backing 전용)라 표 4.1a 가 "04 카드 매핑 그대로" 로 위임함이 설계상 정상. 단 정량값 인용 4종(constitutional −73% / harness-bench 76.2 / self-improving 17→53% / skillreducer +2.8%)은 draft 가 수치 인용 시 출처 카드로 거슬러 표기.


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
- **라이브 출처 간 내부 명칭 drift (이력형 — 작성 시점 재확인 필수)** — 루프 명칭 체계(당직 `oncall`·일지 `note`·모의훈련 `drill`·연수 `study`)는 글로벌 `~/.claude/CLAUDE.md` 와 `loops/README.md` 양쪽 모두 신명으로 일치 확인됨 (2026-06-11). 단 이 명칭은 과거 rename 이력이 있고(구명 scout/golden → 신명 oncall/drill), 라이브 파일마다 갱신 시점이 어긋날 수 있다. **매뉴얼은 anchor 인용 시점에 `loops/README.md` 실물을 진실로 재확인**하고, 파일 간 불일치가 발견되면 그 사실 자체를 "라이브 §anchor 로 drift 추적" 가치의 _시연_ 으로 등재한다. 특정 파일의 구명/신명 표기는 작성 시점 live Read 로만 인용 — 기억 속 표기 인용 금지.
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
- **prd.md 경로 표기**: 본 프로젝트 cwd 도 자체 `.agent_reports/spec/prd.md` 를 가질 수 있어(spec-backed) 축약형 `prd.md` 는 어느 prd 인지 모호 — 각 절 첫 인용은 `worklog-board/.claude_reports/spec/prd.md` 전체 경로로, 이후 같은 절 안에서만 축약 `prd.md` 허용 (절 독립성 보존).

### 표기 규칙

- **한국어 본문 + 영어 굳은 용어 그대로**: harness · loop · worktree · headless · spec · context · prompt · maker-verifier · golden set · orchestrator · sub-agent · pipeline · scaffold · hook · cron · token · context rot · attention budget · just-in-time · compaction · 3-tier · plan-then-execute · spec-driven 등.
- **비표준·내부 약자 첫 등장 풀이**: 표준 약자라도 한 응답 첫 등장 시 1회 풀이 (예: QA(quality assurance), FN(false negative)). 같은 개념은 같은 표기.
- **고유명사 영어 원어**: 논문/블로그 제목·저자명·venue·모델명·데이터셋명·메트릭명·코드 식별자·파일 경로.
- **루프 호칭**: 한국어+ASCII 병기 — 당직(oncall)·일지(note)·모의훈련(drill)·연수(study). 실물 경로는 `notes/oncall/`·`drill/run.sh`·`drill/cases/`. `loops/README.md` 실명이 진실 — anchor 인용 시 작성 시점 live Read 로 재확인 (과거 rename 이력 있음).
- **figure embed**: `<img width=500>` (미리보기 수준, 통합 PPTX + 개별 PNG — feedback: figure_combined_pptx_only).
- **다이어그램**: many-to-many 는 매트릭스, 파이프라인은 단방향 레인, 납품 전 PNG 렌더 검수 (feedback: diagram_no_edge_tangle).

### 톤

- 참조서 — 평어·개조식 허용 (보고서 라벨·표). 친절 안내체(`~해 드릴게요`) 금지. marketing 어조 금지. administrative 어조도 아님.
- lookup 최적화 — 절 독립성·표 anchor. 배경 설명 최소.

### Paragraph Cohesion 규칙

- P8(산출물 소통)의 canonical site = 1부 P8. 2부 2.3·4부 4.4 는 cross-ref 로 압축 (원칙 재서술 금지).
- 새 절 설계마다 4-step: 중복 확인 → 단락 축 → cross-section 중복 → EDIT/REPLACE/INSERT/DROP 분류.
