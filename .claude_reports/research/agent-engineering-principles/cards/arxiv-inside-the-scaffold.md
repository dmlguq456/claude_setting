---
title: "Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures"
authors: "Benjamin Rombaut"
venue: "arXiv preprint"
year_month: "2026-03"
arxiv_id: "2604.03515"
url: "https://arxiv.org/abs/2604.03515"
raw_type: paper
tier: 4
---

**Figures**: ../figures/arxiv-inside-the-scaffold_fig1.png

## Core Claims

- (Abstract) "a source-code-level architectural taxonomy derived from analysis of 13 open-source coding agent scaffolds"
- (§1 Contributions) 핵심 주장 — "scaffold architectures are better characterized as compositions of loop primitives along continuous spectra than as instances of discrete architectural types". 즉 control loop / plan-execute / generate-test-repair 를 _배타적 아키텍처 타입_ 이 아니라 조합 가능한 **loop primitive** 의 spectrum 으로 본다.

## Key Concepts & Definitions

- **Loop primitive (loop 원시 단위)**: ReAct, generate-test-repair, plan-execute, multi-attempt retry, tree search 를 composable building block 으로 정의 — agent 가 이들을 서로 다른 조합으로 layering 한다.
- **3-layer / 12-dimension taxonomy**:
  1. *Control Architecture* — control loop strategy (fixed pipeline → MCTS), loop driver (user/scaffold/LLM-driven), control flow implementation (while loop, recursion, graph, exception)
  2. *Tool and Environment Interface* — tool set design (0–37 tools), edit/patch format, tool discovery (static → dynamic), context retrieval paradigm (keyword search → knowledge graph), execution isolation (local → containerized)
  3. *Resource Management* — state management (destructive list → event sourcing), context compaction (none → LLM-initiated), multi-model routing (single → classifier chain), persistent memory (none → multi-tier extraction)
- **Scaffold = LLM 을 둘러싼 코드**: 모델 자체보다 scaffolding 코드가 "how the agent behaves, what mistakes it makes, and where it spends its token budget" 를 점점 결정한다는 입장 (harness 개념과 동치).

## Patterns Covered

- Loop 패턴: ReAct · generate-test-repair · plan-execute · multi-attempt retry · tree search (MCTS 포함)
- Retrieval: keyword search · PageRank repo map · AST-aware indexing · knowledge graph · embedding semantic search
- Search strategy: fixed pipeline · sequential ReAct · phased workflow · depth-first tree search · full MCTS
- Safety mechanism: human supervision · rule-based policy · LLM-based evaluation · containerization (= maker/verifier·permission boundary 계열)

## Generation Mapping

- **Harness Engineering 세대의 학술 대응물**. 매뉴얼이 블로그(Anthropic "Effective harnesses", Addy "Agent Harness Engineering")로 주장하는 "scaffold/harness 가 행동을 결정한다"를 13개 OSS agent 소스코드로 측정·분류한 1차 학술 근거.
- 매뉴얼의 실무 패턴 직접 대응: **plan-then-execute**(plan-execute primitive), **maker/verifier**(generate-test-repair + LLM-based evaluation), **상태 파일 영속성**(state management: destructive list → event sourcing, persistent memory multi-tier), **compaction**(context compaction dimension), **worktree 격리**(execution isolation: local → containerized).
- 단 tier 4 — 모든 taxonomic claim 은 file path + line number 에 grounding 되어 재현 가능하나, 성능과의 인과는 다루지 않음(아래 Limitations).

## Quotable

1. "The scaffolding code that surrounds the language model ... increasingly determines how the agent behaves, what mistakes it makes, and where it spends its token budget." (§1 Introduction)
2. "Loop primitives function as composable building blocks that agents layer in different combinations." (Abstract)
3. "All taxonomic claims are grounded in file paths and line numbers, providing a reusable reference." (Abstract)

## Method & Evidence

- 대상: **13개 open-source coding agent** (pinned commit hash 기준 분석) — OpenCode, Gemini CLI, Codex CLI, OpenHands, Cline, Aider, SWE-agent, mini-swe-agent, AutoCodeRover, Agentless, Prometheus, Moatless Tools, DARS-Agent.
- taxonomy 규모: **3 layer × 12 dimension**, tool set 범위 0–37 tools.
- 채택 신호(성능 아님): 분석 대상 13개 중 **7개가 각 15,000+ GitHub stars**.
- **성능 벤치 없음** — "No performance benchmarking was conducted, and no claims are made about correlations between scaffold design and task success rates" (§3.5).

## Limitations

- 순수 taxonomic — scaffold 설계와 task success 의 상관/인과 미주장(§3.5). 모델 capability 와 scaffold 효과 분리 불가(confound).
- 대상 선정이 leaderboard/GitHub star/survey 기반 비망라적 → selection bias.
- 단일 저자 분석 → construct validity threat (§6, mitigation 언급).
- proprietary agent(Claude Code, GitHub Copilot, Cursor) 제외 — readable source 있는 OSS 한정.
