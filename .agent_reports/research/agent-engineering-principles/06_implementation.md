# 06 — Goal-Adaptive Action Roadmap

> **Inferred goal: write** — 사용자 매뉴얼(개인 ~/.claude 에이전트 시스템 README 확장판) 1부 '원칙의 세대사' 작성이 명시된 목적이다. 이 챕터는 그 1부를 어떻게 쓰기 시작할지에 대한 high-level 계획이다.

---

## 1. Section-by-section outline (매뉴얼 1부 '원칙의 세대사')

```
1부. 원칙의 세대사

1.0 들어가며 — 왜 세대사인가
    · 핵심 프레임: 세대는 대체가 아니라 누적 layer. loop⊃harness⊃context⊃prompt.
    · 인용: [osmani-loop-engineering] [greyling-loop-engineering] (명시적 세대 서사)

1.1 Gen 0 → Gen 1: prompt 에서 context 로
    · prompt engineering 의 한계(production 신뢰성) → context engineering 등장
    · verbatim 정의 + 명명(Osmani+Anthropic 공동)
    · 핵심 개념: context rot · attention budget · compaction · just-in-time
    · 인용: [osmani-context-engineering] [anthropic-effective-context-engineering]

1.2 Gen 2: harness engineering — Agent = Model + Harness
    · "the other half of the system" 서사, Trivedy 명명
    · self-aware caveat: harness 는 모델 개선 시 축소 (가치 감쇠론)
    · 인용: [osmani-agent-harness-engineering] [anthropic-effective-harnesses]
            [anthropic-harness-design-long-running-apps] [greyling-agent-model-harness]

1.3 Gen 3: loop engineering — 인간을 prompt 자리에서 빼다
    · "replacing yourself", self-feeding harness, 6-block 구조
    · 실증: C compiler 16-Claude 자율 구축
    · 경계: "The loop changes the work, it does not delete you from it"
    · 인용: [osmani-loop-engineering] [anthropic-c-compiler-parallel-claudes] [greyling-loop-engineering]

1.4 패턴 카탈로그 (11종 — GoF 식 named pattern)
    · P1~P11 각각: 문제 → 원칙(verbatim) → 메커니즘 → 반론
    · 산출물 기반 소통 원칙을 P8 안에서 정식 등재 (사용자 강조)
    · 인용: [04_technical_deep_dive.md] 의 카드 매핑 그대로
    · Tensions 4종을 패턴 뒤 별도 절로 (균형 서술)

1.5 우리 시스템 매핑 자리 (→ 2부로 연결하는 다리)
    · 1부는 분야 원칙 망라, 2부는 그 원칙이 우리 ~/.claude 세팅에 어떻게 녹았나
    · draft 작성 시점에 CLAUDE.md·CONVENTIONS·loops/README 직접 Read
```

> **망라 원칙 (draft_directives §6)**: 1부는 research 가 발굴한 원칙 _전체_ 를 체계적으로 망라하고, 사용자 강조 항목(산출물 소통 등)은 그 안에서 비중만 키운다. 사용자가 세션 중 짚은 항목은 _하나의 예시_ 일 뿐 전부가 아니다.

---

## 2. Argument scaffolding (핵심 주장별 근거 + 반론 처리)

| 핵심 주장 | 지지 근거 카드 | 반론·caveat 처리 |
|---|---|---|
| 세대는 누적 layer (대체 아님) | `[osmani-loop-engineering]`(harness 위 loop) `[greyling-loop-engineering]`(명시적 세대 서사) | 없음 — 모든 1차 출처 합의 |
| 자기채점 금지 → maker/verifier 분리 | `[anthropic-harness-design-long-running-apps]` `[epsilla-gan-style-agent-loop]` `[mindstudio-planner-generator-evaluator]` | GAN 비유 한계: cooperative review 로 한정, adversarial reviewer 과신 금지 `[anthropic-claude-code-best-practices]` |
| 상태는 filesystem 에 외재화 (산출물 소통) | `[osmani-long-running-agents]` `[humanlayer-12-factor-agents]` `[anthropic-effective-harnesses]` | context file 과다 역효과: minimal requirement 만 `[arxiv-evaluating-agents-md]` |
| 서브에이전트 분업 = read OK, write single-thread | `[anthropic-multi-agent-research-system]` `[cognition-multi-agents-working]` | Cognition 2025 반대 → 2026 조건부 완화, read/write 축 종합 `[cognition-dont-build-multi-agents]` |
| harness 가 행동을 결정 (Agent=Model+Harness) | `[osmani-agent-harness-engineering]` `[greyling-agent-model-harness]` `[arxiv-code-as-agent-harness]` | 가치 감쇠론: harness variance 는 model 강해질수록 축소 `[greyling-agent-model-harness]` |
| 변경은 eval 로 배포 전 검증 | `[braintrust-eval-driven-development]` `[anthropic-demystifying-evals]` | infra noise 6%p, Goodhart 위험 `[anthropic-infrastructure-noise]` `[arxiv-eval-driven-iteration]` |
| context 는 유한 자원, 큰 window 가 해법 아님 | `[anthropic-effective-context-engineering]` `[redis-context-compaction]` | aggressive 압축은 re-fetch 비용 (tokens-per-task) `[factory-evaluating-compression]` |

---

## 3. Figure/table 후보

> figure 정책: 자료팀 figure 게이트를 거친다. edge 교차 회피(many-to-many 는 매트릭스·파이프라인은 단방향 레인), 납품 전 PNG 렌더 검수, embed 는 `<img width=500>` (draft_directives §1).

| 후보 | 형태 | 출처/근거 | 캡션 초안 |
|---|---|---|---|
| 세대 4단 타임라인 | 단방향 레인 (대체 아닌 누적 강조) | analysis_summary §4 timeline | "prompt → context → harness → loop: 각 세대는 이전 세대의 미해결분을 흡수하며 누적 layer 로 쌓인다 (2024-12 ~ 2026-06)" |
| 패턴 × 세대 매핑 | 매트릭스 (many-to-many) | [01](01_landscape.md) lineage | "11 실무 패턴이 어느 세대에서 파생했나 — maker-verifier 는 3 갈래에서 수렴" |
| 자율 실행 안전장치 4층 | 단방향 레인 | [05](05_deployment.md) §1 | "Permission → auto-mode classifier → sandboxing → hook gate: 자율성 ↑ 일수록 hard boundary 로 무게 이동 (84%/93%/17%FN)" |
| context collapse 정량 | bar (재인용) | `figures/arxiv-agentic-context-engineering_fig2.png` | "monolithic rewrite 시 context 가 18,282→122 tokens 로 붕괴 (ACE Fig 2)" |
| harness taxonomy | 재인용 | `figures/arxiv-inside-the-scaffold_fig1.png` / `arxiv-code-as-agent-harness_fig1.png` | "13 OSS coding agent 의 3 layer × 12 dimension scaffold taxonomy" |

> 추가 figure 후보(draft_directives §1): 4트랙 파이프 구조도 / 루프 4계층(초·분·일·주) / 하루 일과 흐름 / 팀 분업 매트릭스 — 이들은 2부(우리 시스템) 자산이므로 draft 시점에 생성한다.

---

## 4. Citation map (어느 절에 어느 카드)

| 절 | 1차 카드 | rationale |
|---|---|---|
| 1.0 들어가며 | `[osmani-loop-engineering]` `[greyling-loop-engineering]` | 누적 세대 프레임의 명시적 서사 |
| 1.1 context | `[osmani-context-engineering]` `[anthropic-effective-context-engineering]` | 공동 canonical, verbatim 정의·명명 |
| 1.2 harness | `[osmani-agent-harness-engineering]` `[anthropic-effective-harnesses]` `[anthropic-harness-design-long-running-apps]` | 명명·canonical·self-aware caveat |
| 1.3 loop | `[osmani-loop-engineering]` `[anthropic-c-compiler-parallel-claudes]` | 명명·실증 |
| 1.4 P1 plan | `[anthropic-claude-code-best-practices]` `[owainlewis-spec-driven]` `[osmani-good-spec]` | "wrong problem 회피", plan/execute 분리 |
| 1.4 P2 spec | `[github-spec-kit]` `[owainlewis-spec-driven]` `[osmani-good-spec]` | "intent is source of truth", 단계 동형 |
| 1.4 P3 maker-verifier | `[anthropic-harness-design-long-running-apps]` `[epsilla-gan-style-agent-loop]` `[mindstudio-planner-generator-evaluator]` | self-eval 불가 + 메커니즘 + GAN caveat |
| 1.4 P4 서브에이전트 | `[anthropic-multi-agent-research-system]` `[cognition-dont-build-multi-agents]` `[cognition-multi-agents-working]` | read/write 축 종합 |
| 1.4 P5 파이프라인 | `[anthropic-building-effective-agents]` `[github-spec-kit]` | prompt chaining 어원, Tasks 분해 |
| 1.4 P6 golden set | `[anthropic-demystifying-evals]` `[braintrust-eval-driven-development]` `[anthropic-infrastructure-noise]` | eval anatomy, frozen/growing, noise floor |
| 1.4 P7 오답노트 | `[osmani-agent-harness-engineering]` `[braintrust-eval-driven-development]` `[arxiv-agentic-context-engineering]` | 1차 정의, failure-driven, 자동화 backing |
| 1.4 P8 상태 영속성 | `[osmani-long-running-agents]` `[humanlayer-12-factor-agents]` `[anthropic-effective-harnesses]` `[anthropic-managed-agents]` | amnesiac+filesystem, Factor 5/6/12, **산출물 소통 원칙** |
| 1.4 P9 worktree | `[zylos-git-worktree-isolation]` `[anthropic-c-compiler-parallel-claudes]` `[anthropic-claude-code-sandboxing]` | 패턴·실증·격리 층 |
| 1.4 P10 headless | `[claude-code-github-actions]` `[anthropic-claude-code-auto-mode]` `[mindstudio-headless-mode]` | 진입점·classifier·cron 3원칙 |
| 1.4 P11 컨텍스트 절약 | `[anthropic-effective-context-engineering]` `[anthropic-code-execution-mcp]` `[anthropic-advanced-tool-use]` `[redis-context-compaction]` | just-in-time, 98.7%/85%, compaction 폴백 |
| Tensions | `[cognition-*]` `[mindstudio-*]` `[greyling-agent-model-harness]` `[arxiv-evaluating-agents-md]` | 4 tension 균형 서술 |

> tier 4 카드는 절대 단독 근거로 쓰지 않는다 — 항상 위 tier 1–2 카드의 _정량 backing_ 으로만 동반한다.

---

## 5. Writing-stage timeline

> Day/Phase 달력 태그 금지 (사용자 feedback). Tier 🔴🟡🟢 + 위치 순서만.

- 🔴 **세대 서사 골격 (1.0~1.3)**: 4세대 verbatim 정의·명명 귀속·등장 배경. 가장 먼저 쓴다 — 나머지가 이 위에 걸린다. 근거: [01](01_landscape.md) + [02](02_standards.md).
- 🔴 **패턴 카탈로그 P3·P8 (1.4)**: maker-verifier·상태 영속성(산출물 소통) — 사용자 강조 + 합의가 가장 강하다. 먼저 쓴다.
- 🟡 **나머지 패턴 P1·P2·P4·P5·P6·P11**: mainstream 패턴이라 단정적으로 서술해도 된다.
- 🟡 **Tensions 4종**: ①④ 는 반드시 균형 있게 서술한다. emerging·contested caveat 동반.
- 🟢 **caveat-heavy 패턴 P7(자동화)·P9·P10**: tier 3/4 의존 — 출처 tier 명시. 미해결 과제 절에 둔다.
- 🟢 **1.5 다리 절**: 2부로 연결한다. draft 시점에 CLAUDE.md/CONVENTIONS Read 후 작성.

---

## Next Pipeline

추천 명령 (verbatim):

```
/autopilot-draft "에이전트 엔지니어링 매뉴얼 1부 '원칙의 세대사' — research/agent-engineering-principles 근거" --mode doc
```

> high-stakes(매뉴얼·장기 자산) 신호가 있으면 `--qa thorough` 로 상향을 고려한다. 사용자 검토를 끼우려면 `--user-refine` 을 명시적으로 추가한다 (자동으로는 켜지 않음).

**Boundary disclaimer**: 이 `06_implementation.md` 는 분야 분석에서 도출한 high-level 계획입니다. 본격적인 문서 작성·코드 구현은 `autopilot-draft` / `autopilot-code` 로 넘어갑니다. 또한 draft_directives §7(양방향)에 따라, 이 research 의 발견 중 _우리 스킬·지침 보강 후보_ 를 별도 actionable 목록(무엇/왜·출처/어디에/비용/우선순위)으로 사용자에게 제안하는 연수 보고는 draft 와 분리된 트랙입니다.
