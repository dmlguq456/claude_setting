# Search Results — 에이전트 엔지니어링 원칙·패턴 종합 조사 (2025-2026)

> mode: technology (web/blog 1차, arXiv 보조) · date: 2026-06-11 · total: 61 sources
> 다운스트림: autopilot-draft --mode doc (사용자 매뉴얼 1부 '원칙의 세대사') 인용용
> 정렬: discovery_count DESC → venue_tier ASC → year DESC
> **Round 2 확장 (2026-06-11)**: headless/cron · worktree 격리 · compaction/영속성 · eval-driven · spec-driven 5 갭 보강 → +16 신규, +1 중복 hit (#16 Demystifying evals). 신규는 §E 참조.

## A. 세대사 backbone (prompt → context → harness → loop)

| # | 제목 | 저자/출처 | 연도 | venue (tier) | disc | 매뉴얼 절 |
|---|---|---|---|---|---|---|
| 1 | Effective context engineering for AI agents | Anthropic | 2025-09 | Anthropic Eng (1) | 4 | **Context Eng** canonical |
| 2 | Context Engineering: Bringing Engineering Discipline to Prompts | Addy Osmani | 2025-07 | Substack (3) | 3 | prompt→context 전이 |
| 3 | Effective harnesses for long-running agents | Anthropic | 2025-11 | Anthropic Eng (1) | 3 | **Harness Eng** canonical |
| 4 | Agent Harness Engineering | Addy Osmani | 2026-04 | Addy Blog (3) | 4 | **Harness** 정의 (config + 오답노트→케이스) |
| 5 | Loop Engineering | Addy Osmani | 2026-06 | Addy Blog/Substack (3) | 4 | **Loop Eng** 명명자 |
| 6 | Loop Engineering (core) | Cobus Greyling | 2026-06 | Medium (3) | 2 | Loop 정의 정리 |
| 7 | The Rise of AI Harness Engineering / Agent = Model + Harness | Cobus Greyling | 2026-03/06 | Medium (3) | 1 | Agent=Model+Harness 등식 |
| 8 | Harness design for long-running application development | Anthropic | 2026-03 | Anthropic Eng (1) | 1 | Harness 구체화 |
| 9 | Long-running Agents | Addy Osmani | 2025-12 | Substack (3) | 1 | context reset/hand-off |
| 10 | Configured, not coded | Cobus Greyling | 2026-05 | Medium (3) | 1 | harness=config |

## B. 실무 패턴 1차 출처

| # | 제목 | 저자/출처 | 연도 | venue (tier) | disc | 패턴 |
|---|---|---|---|---|---|---|
| 11 | Building effective agents | Anthropic (Schluntz/Zhang) | 2024-12 | Anthropic Eng (1) | 4 | workflow vs agent, 5 패턴 (plan/evaluator-optimizer) |
| 12 | Claude Code: Best practices for agentic coding | Anthropic | 2025-04 | Anthropic Eng (1) | 3 | plan-then-execute, worktree, headless, subagent, CLAUDE.md |
| 13 | The GAN-Style Agent Loop (Anthropic harness 분석) | Epsilla | 2026 | Epsilla Blog (3) | 2 | **maker/verifier 분리 (자기채점 금지)** canonical |
| 14 | How we built our multi-agent research system | Anthropic | 2025-06 | Anthropic Eng (1) | 3 | **subagent persona 분업** (orchestrator-worker) |
| 15 | Don't Build Multi-Agents | Walden Yan (Cognition) | 2025 | Cognition (2) | 3 | subagent 분업 **반대 입장** (균형) |
| 16 | Demystifying evals for AI agents | Anthropic | 2026-01 | Anthropic Eng (1) | 2 | **golden set / eval 회귀 / verifier** |
| 17 | Agentic Engineering Patterns | Simon Willison | 2026 | Substack (3) | 2 | 병렬 worktree, subagent, context 절약 |
| 18 | 12-Factor Agents | Dex Horthy (HumanLayer) | 2025 | GitHub (3) | 3 | **상태 파일/영속성** (Factor 5), human-as-tool |
| 19 | A practical guide to building agents | OpenAI | 2025-04 | OpenAI PDF (1) | 2 | vendor cross-ref (agent vs workflow, orchestration) |
| 20 | Building a C compiler with parallel Claudes | Anthropic | 2026-02 | Anthropic Eng (1) | 2 | **병렬 worktree 격리** 실증 |
| 21 | Multi-Agents: What's Actually Working | Cognition | 2026 | Cognition (2) | 1 | subagent nuance (#15 갱신) |
| 22 | Planner-Generator-Evaluator Pattern (GAN-inspired) | MindStudio | 2026 | Blog (4) | 1 | plan+maker/verifier 결합 (secondary) |

## C. 컨텍스트 절약 / 자동화 / 안전 (harness·loop 보조)

| # | 제목 | 출처 | 연도 | tier | 패턴 |
|---|---|---|---|---|---|
| 23 | Equipping agents with Agent Skills | Anthropic | 2025-10 | 1 | progressive disclosure 컨텍스트 절약 |
| 24 | Code execution with MCP | Anthropic | 2025-11 | 1 | code-as-action token 효율 |
| 25 | Scaling Managed Agents (brain/hands 분리) | Anthropic | 2026-04 | 1 | maker/verifier 일반화 |
| 26 | Advanced tool use | Anthropic | 2025-11 | 1 | harness tool layer |
| 27 | The 'think' tool | Anthropic | 2025-03 | 1 | plan 단계 tool 화 |
| 28 | Claude Code auto mode | Anthropic | 2026-03 | 1 | headless 자동화 안전 |
| 29 | Beyond permission prompts (sandboxing) | Anthropic | 2025-10 | 1 | worktree/sandbox 격리 안전 |
| 30 | Designing AI-resistant technical evaluations | Anthropic | 2026-01 | 1 | self-grading 금지 근거 |
| 31 | Quantifying infrastructure noise in agentic coding evals | Anthropic | 2026-02 | 1 | eval 회귀 flakiness |
| 32 | Loop Engineering Playbook | Cobus Greyling | 2026-06 | 3 | headless/cron 구현 |

## D. arXiv 학술 보조 (HF paper_search, tier 4)

| arXiv | 제목 | 연도 | HF↑ | 패턴 대응 |
|---|---|---|---|---|
| 2604.03515 | Inside the Scaffold: Taxonomy of Coding Agent Architectures | 2026-04 | — | control loop / plan-execute / generate-test-repair |
| 2605.18747 | Code as Agent Harness | 2026-05 | 215 | code-as-action 컨텍스트 절약 |
| 2605.27922 | Harness-Bench | 2026-05 | — | harness leverage 정량 |
| 2510.04618 | Agentic Context Engineering (ACE) | 2025-10 | 134 | 오답노트→케이스 (context self-improve) |
| 2512.16970 | PAACE: Plan-Aware Automated Agent Context Engineering | 2025-12 | — | plan-then-execute + context eng |
| 2602.11988 | Evaluating AGENTS.md | 2026-02 | — | repo-level context file 실증 |
| 2603.29919 | SkillReducer | 2026-03 | — | 컨텍스트 절약/압축 |
| 2605.14271 | Auditing Agent Harness Safety | 2026-05 | 54 | harness safety |
| 2504.15228 | A Self-Improving Coding Agent | 2025-04 | — | 자기개선 루프 |
| 2505.18646 | SEW: Self-Evolving Agentic Workflows | 2025-05 | — | 파이프라인 세분화 + 자기개선 |
| 2508.08322 | Context Engineering for Multi-Agent Code Assistants | 2025-08 | — | subagent + context eng |

## E. Round 2 확장 — 갭 보강 (2026-06-11, +16 신규)

갭별 신규 출처. blog 1차 + arXiv 학술 정식화 보완. 기존 #1–#65 와 연속.

### E1. headless / cron 자동화 (loop engineering 구현)

| # | 제목 | 출처 | 연도 | tier | 비고 |
|---|---|---|---|---|---|
| 33 | Claude Code GitHub Actions (docs) | Claude Code Docs | 2025 | 1 | **vendor 1차** — claude-code-action@v1, -p(--print) headless batch |
| 34 | Headless Mode CI/CD Playbook for 2026 | Code With Seb | 2026 | 4 | crontab 환경변수, GitLab/Jenkins/CircleCI, skip-permissions 안전 |
| 35 | What Is Claude Code Headless Mode | MindStudio | 2026 | 4 | headless 개념 정리 (secondary) |

### E2. 병렬 worktree 격리

| # | 제목 | 출처 | 연도 | tier | 비고 |
|---|---|---|---|---|---|
| 36 | Git Worktree Isolation Patterns for Parallel AI Agents | Zylos Research | 2026-02 | 4 | **종합** — 공유 .git store, Claude/Codex/Cursor 네이티브, 8-10 cap, Dagger 하이브리드 |
| 37 | How to Use Git Worktrees for Parallel AI Agent Execution | Augment Code | 2026 | 4 | worktree 실무 가이드 (secondary) |

### E3. compaction / 상태 영속성

| # | 제목 | 출처 | 연도 | tier | 비고 |
|---|---|---|---|---|---|
| 38 | Context Compaction for AI Agents: A Complete Guide | Redis | 2026 | 3 | **종합** — short/long-term 분리, recursive summarization, L1-L4 memory hierarchy |
| 39 | Evaluating Context Compression for AI Agents | Factory.ai | 2026 | 3 | anchored iterative summarization (intent/files/decisions/next steps) |

### E4. eval-driven development (golden set / 회귀)

| # | 제목 | 출처 | 연도 | tier | 비고 |
|---|---|---|---|---|---|
| 40 | What is eval-driven development | Braintrust | 2026 | 3 | **EDD=agent TDD**, golden 40/failure 40/adversarial 20, frozen core vs growing set |
| 41 | Eval-driven development (Red Hat) | Red Hat Developer | 2026-03 | 3 | 5-layer test harness, evaluation gate promotion (secondary) |

### E5. plan-then-execute / spec-driven

| # | 제목 | 저자/출처 | 연도 | venue (tier) | 비고 |
|---|---|---|---|---|---|
| 42 | How to write a good spec for AI agents | Addy Osmani | 2026 | Addy Blog / O'Reilly (3) | **핵심** — 'plan 과 do 를 같은 agent 에 시키지 말라' |
| 43 | How I Code With AI Agents (Spec-Driven) | Owain Lewis | 2026 | Newsletter (4) | spec→human review→구현 워크플로우 (secondary) |
| 44 | Spec-driven development with AI (spec-kit) | GitHub Blog | 2025 | GitHub (2) | **vendor 제도화** — open-source toolkit |

### E6. arXiv 학술 보조 (Round 2, tier 4)

| arXiv | 제목 | 연도 | 패턴 대응 |
|---|---|---|---|
| 2602.00180 | Spec-Driven Development: From Code to Contract | 2026-01 | spec=primary artifact, 3 rigor level |
| 2602.02584 | Constitutional Spec-Driven Development | 2026-01 | spec-as-constraint, security defect −73% |
| 2509.08646 | Architecting Resilient LLM Agents (Secure P-t-E) | 2025-09 | **plan-then-execute foundational** + security |
| 2601.22025 | When Generic Prompt Improvements Hurt (Eval-Driven Iteration) | 2026-01 | **eval 회귀** — prompt change = regression risk |

## 패턴 → 핵심 근거 매핑 (매뉴얼 인용 가이드)

| 매뉴얼 패턴 | 1차 근거 (primary) | 보조 (secondary/arXiv) |
|---|---|---|
| prompt→context→harness→loop 세대 구분 | #1 #3 #4 #5 (Anthropic + Addy) | #6 #7 (Cobus), 2604.03515 |
| plan-then-execute | #11 #12 (Anthropic), #42 (Addy: plan≠do) | 2509.08646, 2604.03515, 2512.16970 |
| spec-driven development | #42 (Addy) #44 (GitHub spec-kit) | 2602.00180, 2602.02584 |
| maker/verifier 분리 (자기채점 금지) | #13 (Epsilla) #16 #25 #30 (Anthropic) | #22 (MindStudio) |
| subagent persona 분업 | #14 (Anthropic) ↔ #15 #21 (Cognition 반대/nuance) | #17, 2508.08322 |
| 파이프라인 세분화 | #11 (5 workflow 패턴) | 2604.03515, 2505.18646 |
| golden set / eval 회귀 | #16 #30 #31 (Anthropic), #40 (Braintrust EDD) | #41, 2601.22025 |
| 오답노트→케이스 승격 | #4 (Addy: '다시는 실수 안 하게 engineer'), #40 (frozen core vs growing set) | 2510.04618, 2504.15228 |
| 상태 파일 / 세션 간 영속성 | #18 (12-factor F5) #3 (hand-off file), #38 #39 (compaction/hierarchy) | 2602.11988 |
| 병렬 worktree 격리 | #20 (parallel Claudes) #12 #17, #36 (Zylos 종합) | #37 (Augment) |
| headless / cron 자동화 | #5 (Loop Eng) #32 #12, #33 (GitHub Actions docs) | #34 #35 |
| 컨텍스트 절약 (고정 오버헤드/압축) | #1 #23 #24 (Anthropic) | 2603.29919, 2605.18747 |

## 비고

- **균형 주의**: subagent 분업은 Anthropic(#14, 찬성)과 Cognition(#15, '쓰기 작업엔 반대')이 정면 대립. 매뉴얼은 read vs write 작업 구분(Cognition 프레임)으로 양쪽을 종합 인용 권장.
- **세대 명명 권위**: Context Eng = Anthropic + Addy(#1 #2), Harness Eng = Anthropic + Addy(#3 #4), Loop Eng = Addy 가 명명자(#5, Peter Steinberger·Boris Cherny 인용). Cobus Greyling 은 정리/대중화 역할.
- **arXiv 는 모두 tier 4 보조** — 블로그 1차 주장을 학술로 뒷받침하는 용도. material claim 의 단독 근거로 쓰지 말 것.
- 모든 URL 은 WebSearch/WebFetch 로 확인됨 (지어내지 않음). 일부 발행일은 '월' 단위까지만 확정 (정확 일자 미확인 항목은 published 필드에 YYYY-MM 표기).
