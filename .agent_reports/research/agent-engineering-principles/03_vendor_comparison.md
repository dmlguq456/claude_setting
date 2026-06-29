# 03 — Harness·도구 비교

> "전통적 vendor 비교" 를 이 분야에 맞게 바꿔, coding-agent harness 제품 / orchestration framework / eval 도구를 패턴 지원 관점에서 비교한다. star·last-update 는 code_search 확인값(2026-06-11, 대략치) — star caveat 는 [07_resources.md](07_resources.md) 참조.

---

## Harness 제품 비교 (coding-agent)

| 제품 | 철학 | loop 구조 | 패턴 지원 강점 | 카드/repo |
|---|---|---|---|---|
| **Claude Code** | terminal agentic coding, CLAUDE.md 계층 부트스트랩 | explore→plan→code→commit + verify loop(pass/fail로 자동 close) + hooks(deterministic gate) | plan-then-execute·maker-verifier(adversarial review subagent)·worktree·headless(`-p`)·compaction 한 제품에 종합 | `[anthropic-claude-code-best-practices]` / anthropics/claude-code (~132k) |
| **OpenHands** | full agentic harness, event-sourcing state | control loop + tool/env interface + containerized 실행 격리 | execution isolation·event-sourcing 상태 영속의 production-scale OSS | `[arxiv-inside-the-scaffold]` 분석 대상 / All-Hands-AI/OpenHands (~76k) |
| **SWE-agent** | Agent-Computer Interface(ACI) 설계 | generate-test-repair loop, SWE-bench 회귀 평가 | tool/환경 인터페이스 설계가 성능 좌우 — eval-driven(벤치 기반) 루프 | `[arxiv-inside-the-scaffold]` 분석 대상 / SWE-agent/SWE-agent (~19.5k) |
| **Aider** | terminal pair-programming, 경량 | repo map(PageRank retrieval) + git 자동 commit | context retrieval(repo map) + git-as-state 경량 reference | `[arxiv-inside-the-scaffold]` 분석 대상 / Aider-AI/aider (~46k) |
| **Devin** (Cognition) | 자율 SWE agent | single-threaded write + read/review 보조 | write/decision single-thread 원칙의 산실 (multi-agent 입장 진화) | `[cognition-dont-build-multi-agents]` `[cognition-multi-agents-working]` (closed) |

> Inside-the-Scaffold 논문은 위 OSS 들을 포함한 13개를 3 layer × 12 dimension 으로 taxonomy 로 정리했고, control loop / plan-execute / generate-test-repair 를 _배타적 타입이 아니라 조합 가능한 loop primitive_ 로 본다 `[arxiv-inside-the-scaffold]`. 단 성능 벤치는 없다("No performance benchmarking was conducted").

**Takeaway**: Claude Code 는 매뉴얼이 기술하는 거의 모든 실무 패턴(plan/verify/hooks/subagent/worktree/headless/compaction)을 한 제품에서 구현한 reference 다. OpenHands·SWE-agent·Aider 는 execution isolation·ACI·repo-map retrieval 등 특정 harness 차원의 대표 예시로 인용한다.

---

## Orchestration framework 비교

maker-verifier·plan-execute·handoff 패턴 지원 여부 중심.

| Framework | maker-verifier | plan-execute | handoff | 상태 영속(pause/resume) | 비고 |
|---|---|---|---|---|---|
| **LangGraph** | Partial (graph node로 표현) | Yes (graph) | Partial | **Yes** (durable execution/checkpointing) | low-level orchestration, Factor 6 지원 |
| **CrewAI** | Yes (role로) | Yes (Flows) | Yes (manager/worker) | Partial | role-based, Crews+Flows 이중 구조 |
| **AG2** (AutoGen 후속) | Yes (agent 쌍 대화) | Partial (conversational) | Yes (GroupChat/nested) | Partial | conversational multi-agent. ⚠ AG2≠원조 microsoft/autogen |
| **Mastra** | Yes (eval 통합) | Yes (workflow step) | Partial | Yes (memory) | TS 생태계 LangGraph 대응, workflow+eval 일체형 |
| **OpenAI Agents SDK** | Yes (guardrail) | Yes (manager pattern) | **Yes** (handoffs 1급) | Partial | OpenAI practical guide 의 manager/decentralized/guardrail 직접 구현 |

> 매뉴얼 대비 인용 가치: 이 framework 들은 다중 자율 agent 협업을 지원하지만, 매뉴얼 시스템은 "서브에이전트 중첩 1단" 으로 **더 평면적**이다 — OpenAI manager pattern(메인=manager, agent=tool)에 가깝고 CrewAI/AG2 식 다중 자율 대화와는 대비된다 `[openai-practical-guide-agents]`. 이 대비 자체가 인용 가치다.

**Takeaway**: handoff·다중 자율 agent 가 필요하면 OpenAI Agents SDK(handoff 1급)·CrewAI(role), 상태 영속 graph 가 핵심이면 LangGraph(checkpointing), TS 면 Mastra 다. 단 Cognition 의 "write/decision 분산 금지" 원칙상 매뉴얼은 평면적 manager pattern 을 선호한다 ([04](04_technical_deep_dive.md) Tension a 참조).

---

## Eval 도구 비교

| 도구 | 형태 | golden set | 오답노트 승격 | self-host | 비고 |
|---|---|---|---|---|---|
| **promptfoo** | CLI/library (OSS) | Yes (YAML test suite + assertion) | Yes | **Yes** | 가장 접근성 높은 OSS, red-teaming 포함 (~22k) |
| **Braintrust** | SaaS 플랫폼 + SDK | Yes (frozen core) | Yes (failure-driven evolution) | No | "eval=working spec" 개념 명명 출처. SDK star로 판단 부적합 |
| **LangSmith** | SaaS + SDK | Yes (dataset) | Partial | No | trace 기반 eval + dataset regression, LangGraph 통합 |

> 개념 출처: `[braintrust-eval-driven-development]`("frozen core + growing set", "failure-driven evolution") + `[anthropic-demystifying-evals]`(eval anatomy) + `[redhat-eval-driven-development]`("known bad" set). 구현은 self-host 라면 promptfoo 를 권한다 (Braintrust/LangSmith 는 SaaS).

**Takeaway**: 개념(eval-as-spec, frozen core/growing set)은 Braintrust·Anthropic 에서 인용하되, 실제 self-hosted golden loop 구현 도구로는 promptfoo 를 권한다 — SaaS 종속 없이 YAML golden set + assertion 으로 "변경 전 회귀 검증" 이 된다.

---

## Capability checklist: 패턴 × 도구

| 패턴 | Claude Code | OpenHands | LangGraph | OpenAI SDK | promptfoo |
|---|---|---|---|---|---|
| plan-then-execute | Yes | Yes | Yes | Yes | No |
| maker-verifier 분리 | Yes (adversarial review) | Partial | Partial | Yes (guardrail) | Partial (assertion) |
| 서브에이전트 분업 | Yes (subagent) | Partial | Yes | Yes (handoff) | No |
| 상태 파일·영속성 | Yes (CLAUDE.md·checkpoint) | Yes (event-sourcing) | Yes (checkpoint) | Partial | No |
| worktree 병렬 격리 | Yes | Yes (container) | No | No | No |
| headless·cron | Yes (`-p`·Actions) | Yes | Partial | Partial | Yes (CI) |
| golden set·eval 회귀 | Partial | Partial | Partial (LangSmith) | No | **Yes** |
| 컨텍스트 절약·compaction | Yes (`/compact`) | Yes | Yes | Partial | No |

> "Yes/Partial/No" 는 카드·code_search 가 명시하거나 강하게 시사하는 범위만 표기했다. 미확인 칸은 보수적으로 Partial/No 로 뒀다.

**Takeaway (시나리오별 추천)**:
- **terminal 단일 개발자 + 전 패턴 종합** → Claude Code (매뉴얼 시스템의 실제 토대).
- **컨테이너 격리·event-sourcing 상태** → OpenHands.
- **graph 형 durable 상태 orchestration** → LangGraph.
- **handoff·layered guardrail multi-agent** → OpenAI Agents SDK.
- **self-host golden set 회귀** → promptfoo.
- 매뉴얼 시스템은 Claude Code(harness) + 자체 hook gate(guardrail) + 산출물 파일(상태) + worktree(격리) + `claude -p`/GitHub Actions(headless)를 조합해, 위 도구들의 패턴을 평면적 manager pattern 으로 통합한 형태다.
