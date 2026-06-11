# Analysis Summary — 에이전트 엔지니어링 원칙·패턴 종합 조사 (2025–2026)

> mode: technology · date: 2026-06-11 · sources: 61 cards (tier 1 web/blog 1차 + tier 2 popularizer + tier 3 practitioner + tier 4 arXiv 보조)
> 다운스트림: `autopilot-draft --mode doc` — 사용자 매뉴얼 1부 '원칙의 세대사' 근거
> Phase flags: chaining_available=**false** (intentional — technology mode, reference chaining 비활성) · code_search_available=**true** (`_internal/code_search.md` + `code_resources/tier{1,2,3}_*.md`)
>
> 인용 규칙: 모든 claim 에 카드 파일명 `[card-slug]` 표기. 정량 수치는 카드에 명시된 것만 (fabrication 금지). arXiv (tier 4) 는 블로그 1차 주장의 학술 backing 용 — material claim 단독 근거 금지.

---

## 1. Taxonomy

### ① 세대 축 (prompt → context → harness → loop engineering)

세대는 _배타적 단계_ 가 아니라 **누적 layer** 다 — 각 세대는 이전 세대 위에 쌓이고 (loop 는 harness 위에서 돌고, harness 는 context 를 관리하고, context 는 prompt 를 감싼다), 이전 세대의 미해결분을 다음 세대가 흡수한다.

#### Gen 0 — Prompt engineering (배경 세대, ~2023–2024)
- **정의**: 단일 prompt 의 phrasing 최적화. "cleverly phrasing a question" `[osmani-context-engineering]`.
- **한계 (다음 세대 동력)**: demo 용 one-off prompt 로는 production 신뢰성을 못 냄 — "a witty one-off prompt might have wowed us in demos, but building reliable, industrial-strength LLM systems demanded something more comprehensive" `[osmani-context-engineering]`. "As applications grew more complex, the limitations of focusing only on a single prompt became obvious."
- **명명 권위**: 세대로 회고적 명명된 것이지 정초 텍스트는 없음. Karpathy 인용 "Prompt engineering walked so context engineering could run" `[osmani-context-engineering]`.

#### Gen 1 — Context engineering (2025)
- **정의 (canonical)**: "the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference" `[anthropic-effective-context-engineering]`. Addy 판: "constructing an entire information environment so the AI can solve the problem reliably" `[osmani-context-engineering]`.
- **명명 권위**: **Anthropic** ("Effective context engineering for AI agents", 2025-09, prompt→context 세대 전환을 직접 선언) + **Addy Osmani** ("Context Engineering: Bringing Engineering Discipline to Prompts", 2025-07) 가 공동 canonical.
- **등장 배경**: agent 가 multi-turn·long-horizon 으로 확장 → 단일 prompt 최적화 부족, context window 라는 유한 자원을 loop 전체에 걸쳐 관리해야 함. 핵심 개념 — **context rot** (token 증가 시 recall 저하, "this characteristic emerges across all models"), **attention budget** (transformer n² 구조의 유한 주의), **compaction**, **just-in-time retrieval** `[anthropic-effective-context-engineering]`.
- **학술 정식화 (tier 4)**: **context collapse** 정량 측정 — monolithic rewrite 시 18,282 tokens(66.7%) → 122 tokens(57.1%) 붕괴, Generator/Reflector/Curator delta update 로 방지 `[arxiv-agentic-context-engineering]` (ACE, 2510.04618).
- **핵심 소스 카드**: `[anthropic-effective-context-engineering]` `[osmani-context-engineering]` (canonical) · `[arxiv-agentic-context-engineering]` `[arxiv-context-eng-multi-agent]` `[arxiv-paace]` (학술 보조).

#### Gen 2 — Harness engineering (2025–2026)
- **정의**: "A coding agent is the model plus everything you build around it. Harness engineering treats that scaffolding as a real artifact, and it tightens every time the agent slips" `[osmani-agent-harness-engineering]`. 학술 한 문장 정의: "the software layer that surrounds an LLM with tools, APIs, sandboxes, memory, validators, permission boundaries, execution loops, and feedback channels, thereby turning a stateless model into a functional agent" `[arxiv-code-as-agent-harness]`.
- **명명 권위**: **Viv Trivedy 가 "harness engineering" 용어 coined** `[osmani-agent-harness-engineering]`. **Anthropic** ("Effective harnesses for long-running agents", 2025-11) + **Addy Osmani** ("Agent Harness Engineering") 가 canonical 정초. **Agent = Model + Harness** 등식은 Harness-Bench 논문 발 `[greyling-agent-model-harness]` `[arxiv-harness-bench]`.
- **등장 배경**: "We've spent the last two years arguing about models... That conversation is fine as far as it goes, but it's missing the other half of the system" `[osmani-agent-harness-engineering]`. 모델 한계가 아니라 scaffolding 한계로 문제를 재정의 — "The gap between what today's models can do and what you see them doing is largely a harness gap". harness 가 메우는 이전 단계 미해결분: context rot, early stopping, poor decomposition, incoherence across context windows `[osmani-agent-harness-engineering]`.
- **thesis**: "A decent model with a great harness beats a great model with a bad harness" `[osmani-agent-harness-engineering]`.
- **핵심 명제 (self-aware)**: "Every component in a harness encodes an assumption about what the model can't do on its own, and those assumptions are worth stress testing" `[anthropic-harness-design-long-running-apps]` → harness 는 모델 개선 시 **축소** (v1 sprint construct → v2 제거).
- **정리·대중화 (tier 2)**: Cobus Greyling 이 harness 를 SDK/Framework/Scaffolding 위 **4번째 architectural layer** 로 정리 (Schmid OS analogy, parallel.ai 6-component, "framework collapsing into harness" 80/20) `[greyling-rise-of-harness-engineering]`.
- **학술 정식화 (tier 4)**: 정의 — `[arxiv-code-as-agent-harness]` (UIUC/Meta/Stanford, 200+ works survey, §5.2 "science of harness engineering 부재" open challenge). 측정 — `[arxiv-inside-the-scaffold]` (13 OSS coding agent 소스코드 taxonomy, 3 layer × 12 dim, loop primitive 조합 spectrum, 성능 벤치 없음). 벤치 — `[arxiv-harness-bench]` / `[greyling-agent-model-harness]`.
- **핵심 소스 카드**: `[anthropic-effective-harnesses]` `[osmani-agent-harness-engineering]` `[anthropic-harness-design-long-running-apps]` `[anthropic-managed-agents]` (canonical) · `[greyling-rise-of-harness-engineering]` `[greyling-agent-model-harness]` `[greyling-configured-not-coded]` (정리) · `[arxiv-code-as-agent-harness]` `[arxiv-inside-the-scaffold]` `[arxiv-harness-bench]` (학술).

#### Gen 3 — Loop engineering (2026)
- **정의**: "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead" `[osmani-loop-engineering]`. harness 와의 차이 — "The harness but it runs on a timer, it spawns little helpers, and it feeds itself" → harness **위** 계층.
- **명명 권위**: **Addy Osmani 가 명명자** ("Loop Engineering", 2026-06). 실무 슬로건은 **Peter Steinberger** (OpenClaw: "You should be designing loops that prompt your agents") · **Boris Cherny** (head of Claude Code @Anthropic: "I don't prompt Claude anymore. I have loops running that prompt Claude... My job is to write loops") `[greyling-loop-engineering]`. **Cobus Greyling 은 정리·대중화** (6-block 구조로 묶은 정리자, 명명 권위 아님).
- **등장 배경**: "For like two years the way you got something out of a coding agent was you wrote a good prompt and shared enough context. You type a thing, you read what came back, you type the next thing" — 이 _type/read/type_ 수동 루프가 끝났다 `[osmani-loop-engineering]`. harness engineering 글의 open problem ("agents that run on a timer / self-improving") 이 여기서 실현.
- **6-block 구조**: scheduling(heartbeat) / worktrees / skills / connectors / sub-agents(maker-checker) / memory `[greyling-loop-engineering]`. runtime tiering — Tier A terminal(Claude Code/Grok) / Tier B platform(LangChain durable execution) / Tier C editor `[greyling-loop-engineering-playbook]`.
- **실증 정초**: 16 Claude Opus instance × ~2,000 세션 (~$20,000) 으로 100,000줄 C compiler 자율 구축, 무한 bash loop + lock 기반 task 조율 + 거의 완벽한 verifier `[anthropic-c-compiler-parallel-claudes]`.
- **경계**: "The loop changes the work, it does not delete you from it" — verification 은 여전히 인간 책임, comprehension debt·cognitive surrender 위험 `[osmani-loop-engineering]`.
- **핵심 소스 카드**: `[osmani-loop-engineering]` `[anthropic-c-compiler-parallel-claudes]` (canonical) · `[greyling-loop-engineering]` `[greyling-loop-engineering-playbook]` (정리) · `[osmani-long-running-agents]` (시간 축 확장).

> **세대사 정초 텍스트**: `[anthropic-building-effective-agents]` (2024-12, "Building effective agents") 는 _harness 세대의 정초_ — workflow vs agent 구분 + 6 조합 패턴이 후속 모든 실무 패턴의 어원. 12-factor `[humanlayer-12-factor-agents]` 는 "agents... are comprised of mostly just software" 로 harness/loop 세대의 software-discipline 측 manifesto.

---

### ② 실무 패턴 축 (10개 + 보조 1)

각 패턴 — primary 근거 (tier 1–2) + 보조 (tier 4 arXiv) + 카드에 명시된 정량 수치.

#### P1. Plan-then-execute (계획·실행 분리)
- **Primary**: `[anthropic-building-effective-agents]` (agents "plan and operate independently") · `[anthropic-claude-code-best-practices]` (explore→plan→implement→commit; "Separate research and planning from implementation to avoid solving the wrong problem") · `[osmani-good-spec]` ("Planning in advance matters even more with an agent - you can iterate on the plan first, then hand it off to the agent").
- **핵심 분리 원칙**: "don't ask the same agent to plan the work and do the work" — planning(edge-case 분석)과 execution(shipping)은 다른 cognitive mode `[owainlewis-spec-driven]`.
- **보조 (tier 4)**: `[arxiv-secure-plan-then-execute]` (2509.08646, P-t-E foundational + security, ReAct 대비 predictability·cost 우위) · `[arxiv-paace]` · `[arxiv-inside-the-scaffold]` (plan-execute primitive).

#### P2. Spec-driven development (spec-first)
- **Primary**: `[github-spec-kit]` (GitHub 오픈소스 toolkit, Specify→Plan→Tasks→Implement 4-phase, "We're moving from 'code is the source of truth' to 'intent is the source of truth'") · `[osmani-good-spec]` ("Specs become the shared source of truth… living, executable artifacts") · `[owainlewis-spec-driven]` ("A plan lives in a conversation. A spec lives in your repo"; "bottleneck shifts from implementation to specification").
- **보조 (tier 4)**: `[arxiv-spec-driven-code-to-contract]` (2602.00180, spec=primary artifact, 3 rigor tier) · `[arxiv-constitutional-spec-driven]` (2602.02584, spec-as-constraint, **보안 defect −73%** velocity 유지).

#### P3. Maker-verifier 분리 (자기채점 금지)
- **Primary (canonical)**: `[epsilla-gan-style-agent-loop]` — "AI Cannot Judge Itself", model 은 "pathological optimists", Generator/Evaluator dyad ("By engineering conflict, you engineer progress"). `[anthropic-harness-design-long-running-apps]` — "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when... obviously mediocre"; "Separating the agent doing the work from the agent judging it proves to be a strong lever".
- **메커니즘 근거**: autocomplete bias — "When the same model that wrote the code reviews it, it tends to overlook its own mistakes" `[mindstudio-planner-generator-evaluator]`. adversarial reviewer — "a fresh model try to refute the result, so the agent doing the work isn't the one grading it" `[anthropic-claude-code-best-practices]`.
- **일반화**: brain/hands 분리 `[anthropic-managed-agents]` · CitationAgent 별도 검증 `[anthropic-multi-agent-research-system]` · Red/green TDD `[willison-agentic-engineering-patterns]`.
- **GAN 비유 한계 (caveat)**: "the evaluator isn't adversarial in a competitive sense. It's more like a senior engineer reviewing a pull request" `[mindstudio-planner-generator-evaluator]` — GAN 라벨 문자 그대로 적용 금지.

#### P4. 서브에이전트 분업 (orchestrator-worker)
- **Primary (찬성)**: `[anthropic-multi-agent-research-system]` — orchestrator-worker, single-agent 대비 내부 eval **90.2% 향상**, multi-agent 는 chat 대비 **약 15배 token**, subagent 3–5개 병렬 → research time 최대 **90% 단축**. "Multi-agent systems work mainly because they help spend enough tokens to solve the problem."
- **Primary (반대/nuance)**: `[cognition-dont-build-multi-agents]` — "Running multiple agents in collaboration only results in fragile systems" (write/decision 분산 금지) ↔ `[cognition-multi-agents-working]` — enterprise 사용 ~8x 성장, "A clean-context reviewer catches bugs the coder can't see" (read·review 는 OK). **read vs write 축 종합 필수** (§3 참조).
- **보조**: `[anthropic-effective-context-engineering]` (각 sub-agent 가 1,000–2,000 token 요약 반환) · `[openai-practical-guide-agents]` (Manager/Decentralized pattern) · `[arxiv-context-eng-multi-agent]` · `[arxiv-sew]`.

#### P5. 파이프라인 세분화
- **Primary**: `[anthropic-building-effective-agents]` (prompt chaining — "decomposes a task into a sequence of steps") · `[github-spec-kit]` (Tasks 단계가 spec 을 small isolated chunk 로) · `[anthropic-multi-agent-research-system]` (research loop → citation verification → final compilation).
- **보조 (tier 4)**: `[arxiv-inside-the-scaffold]` (loop primitive 조합) · `[arxiv-sew]` (sub-task 분해·self-evolution).

#### P6. Golden set · eval 회귀
- **Primary (canonical)**: `[anthropic-demystifying-evals]` — eval anatomy(Task/Trial/Grader/Transcript/Outcome), "what proportion of trials an agent succeeds" (pass@k), eval saturation, 20–50 simple task 출발. `[braintrust-eval-driven-development]` — **frozen core(golden set) + growing set** 이분법, "If your eval correctly captures what 'good' means, then optimizing against it is sufficient".
- **신뢰성 근거**: infrastructure noise — Terminal-Bench 2.0 에서 strict↔uncapped 사이 **6%p swing**, "A few-point lead might signal a real capability gap—or it might just be a bigger VM" `[anthropic-infrastructure-noise]`. AI-resistant 설계 (saturation·contamination 저항) `[anthropic-ai-resistant-evals]`.
- **구현 사례**: `[redhat-eval-driven-development]` (8-stage, "known bad" set, judge calibration, single-big-prompt overfit 폭로) · `[anthropic-writing-tools-for-agents]` (eval-driven tool 개선).
- **보조 (tier 4)**: `[arxiv-eval-driven-iteration]` (2601.22025, generic prompt 개선이 오히려 해침 — Qwen 2.5 RAG 26/30→9/30).

#### P7. 오답노트 → 케이스 승격 (failure-driven evolution)
- **Primary (1차 정의)**: "anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again" `[osmani-agent-harness-engineering]`. `[braintrust-eval-driven-development]` — "failure-driven evolution": production 실패를 correct reference 와 함께 golden dataset 에 추가해 "permanent regression guards" 화. `[redhat-eval-driven-development]` — "known bad" set. `[anthropic-demystifying-evals]` — bug tracker·support queue 를 task 소스로.
- **보조 (tier 4)**: `[arxiv-agentic-context-engineering]` (Reflector→Curator playbook delta update) · `[arxiv-self-improving-coding-agent]` (2504.15228, self-edit 로 SWE-bench **17%→53%**).

#### P8. 상태 파일 · 세션 간 영속성
- **Primary**: `[humanlayer-12-factor-agents]` — Factor 5 (unify execution + business state), Factor 6 (Launch/Pause/Resume), Factor 12 (stateless reducer). `[anthropic-effective-harnesses]` — `claude-progress.txt` / `feature_list.json`(immutable) / git history 세 artifact, "each new engineer arrives with no memory of what happened on the previous shift". `[osmani-long-running-agents]` — "State lives outside the agent's context… the agent itself is amnesiac, but the filesystem isn't"; "git as the coordination substrate".
- **인프라 형태**: session = context window 밖 append-only event log `[anthropic-managed-agents]`. memory hierarchy L1 working(TTL)/L2 long-term(vector) `[redis-context-compaction]`.
- **보조 (tier 4)**: `[arxiv-evaluating-agents-md]` (2602.11988, context file 효과 측정 — 반례 포함).

#### P9. Worktree 병렬 격리
- **Primary**: `[anthropic-c-compiler-parallel-claudes]` (container clone-push 격리, lock 파일 task 조율, "Merge conflicts are frequent, but Claude is smart enough to figure that out") · `[anthropic-claude-code-best-practices]` (worktree로 isolated git checkouts) · `[zylos-git-worktree-isolation]` (종합 — 공유 object store + private HEAD/index, "four or more concurrent sessions", rebase-before-PR, Clash pre-flight conflict detection).
- **기술 근거**: "Each worktree gets a private HEAD, private index, and private working directory" / deferred conflict → PR merge 단계 ("visible git conflicts instead of silent runtime overwrites") `[augmentcode-git-worktrees]`. test baseline 먼저 green 확인 후 hand.
- **안전 층**: filesystem+network sandboxing — "sandboxing safely reduces permission prompts by **84%**" `[anthropic-claude-code-sandboxing]`.
- **보조 (tier 4)**: `[arxiv-secure-plan-then-execute]` (task-scoped tool access, sandboxed execution).

#### P10. Headless · cron 자동화
- **Primary (vendor 1차)**: `[claude-code-github-actions]` — `@claude` mention → PR 자동 생성, `on: schedule: cron`, Agent SDK 기반, `claude_args` passthrough. `[anthropic-claude-code-best-practices]` — `claude -p` CI/pre-commit + fan-out (`for file in ...; do claude -p ... done`).
- **안전장치**: auto mode classifier — "Claude Code users approve **93%** of permission prompts" (17% false-negative rate) `[anthropic-claude-code-auto-mode]`. `--dangerously-skip-permissions` 는 격리 환경에서만 `[codewithseb-headless-cicd]` `[mindstudio-headless-mode]`.
- **운영 패턴**: cron 3원칙 (full path / env 명시 / output redirect) `[mindstudio-headless-mode]`.

#### (보조) P11. 컨텍스트 절약 (고정 오버헤드 / 압축)
- **Primary**: `[anthropic-effective-context-engineering]` (just-in-time retrieval, compaction) · `[anthropic-agent-skills]` (progressive disclosure — "Skills let Claude load information only as needed") · `[anthropic-code-execution-mcp]` (**150,000→2,000 tokens, 98.7% 절감**) · `[anthropic-advanced-tool-use]` (Tool Search **85% 절감**, programmatic calling 43,588→27,297 = **37% 절감**).
- **압축 평가**: `[redis-context-compaction]` (raw → reversible → lossy 단계 폴백, L1/L2 hierarchy) · `[factory-evaluating-compression]` ("tokens per task" 최적화, probe-based eval, artifact trail 공통 취약 2.19–2.45).
- **think tool**: `[anthropic-think-tool]` (tool chain 도중 reasoning 공간).
- **보조 (tier 4)**: `[arxiv-skillreducer]` (2603.29919, 48% description/39% body 압축에 quality +2.8% — less-is-more) · `[arxiv-evaluating-agents-md]` (과한 context file 이 success rate 낮추고 inference cost +20%).

---

## 2. Core Sources (tier 분류표)

| Tier | 정의 | 카드 (필독 grade) |
|---|---|---|
| **1** | 1차 권위 (Anthropic/Addy/Cognition/OpenAI/GitHub vendor docs·named-author 영향력 블로그) | **★필독**: `anthropic-effective-context-engineering` · `anthropic-effective-harnesses` · `osmani-context-engineering` · `osmani-agent-harness-engineering` · `osmani-loop-engineering` · `anthropic-building-effective-agents` · `anthropic-claude-code-best-practices` · `anthropic-harness-design-long-running-apps` · `anthropic-multi-agent-research-system` · `anthropic-c-compiler-parallel-claudes` · `humanlayer-12-factor-agents` · `anthropic-demystifying-evals`. **○중요**: `osmani-long-running-agents` · `osmani-good-spec` · `cognition-dont-build-multi-agents` · `cognition-multi-agents-working` · `anthropic-managed-agents` · `anthropic-writing-tools-for-agents` · `anthropic-claude-code-auto-mode` · `anthropic-claude-code-sandboxing` · `anthropic-ai-resistant-evals` · `anthropic-infrastructure-noise` · `claude-code-github-actions` · `willison-agentic-engineering-patterns` · `openai-practical-guide-agents`. **△참고**: `anthropic-agent-skills` · `anthropic-code-execution-mcp` · `anthropic-advanced-tool-use` · `anthropic-think-tool` |
| **2** | 정리·대중화 (popularizer / vendor 종합 블로그) | `greyling-rise-of-harness-engineering` · `greyling-agent-model-harness` · `greyling-loop-engineering` · `greyling-loop-engineering-playbook` · `greyling-configured-not-coded` · `epsilla-gan-style-agent-loop` · `mindstudio-planner-generator-evaluator` · `github-spec-kit` · `redis-context-compaction` · `factory-evaluating-compression` · `braintrust-eval-driven-development` |
| **3** | practitioner / research blog (peer-review 아님) | `owainlewis-spec-driven` · `redhat-eval-driven-development` · `zylos-git-worktree-isolation` · `augmentcode-git-worktrees` · `codewithseb-headless-cicd` · `mindstudio-headless-mode` |
| **4** | arXiv 학술 보조 (블로그 1차 backing 전용, material claim 단독 근거 금지) | `arxiv-code-as-agent-harness` · `arxiv-inside-the-scaffold` · `arxiv-harness-bench` · `arxiv-agentic-context-engineering` · `arxiv-secure-plan-then-execute` · `arxiv-eval-driven-iteration` · `arxiv-spec-driven-code-to-contract` · `arxiv-constitutional-spec-driven` · `arxiv-paace` · `arxiv-context-eng-multi-agent` · `arxiv-evaluating-agents-md` · `arxiv-skillreducer` · `arxiv-auditing-harness-safety` · `arxiv-self-improving-coding-agent` · `arxiv-sew` |

> **명명 권위 vs 정리 역할 (인용 시 구분 필수)**: Greyling (tier 2) 는 _명명자가 아니라 정리·대중화자_ — 매 글이 외부 1차 권위를 명시 호명 (loop=Osmani 명명/Steinberger·Cherny 슬로건, harness=OpenAI·Anthropic·Fowler·parallel.ai·Schmid, Agent=Model+Harness=Harness-Bench 논문). material claim 인용 시 Greyling 카드를 통해 _원 출처로 거슬러_ 인용. 예외: `greyling-configured-not-coded` 는 자기-코퍼스 종합 (외부 권위 적음).

---

## 3. Themes & Tensions

### 합의점 (consensus)
1. **자기채점은 신뢰 불가 → maker/verifier 분리**: model 은 자기 산출을 후하게 평가한다는 점에 모든 출처가 일치 — "pathological optimists" `[epsilla-gan-style-agent-loop]`, "confidently praising... obviously mediocre" `[anthropic-harness-design-long-running-apps]`, "skew positive when they grade their own work" `[osmani-long-running-agents]`, autocomplete bias `[mindstudio-planner-generator-evaluator]`. clean-context reviewer 우위는 Cognition 도 동의 `[cognition-multi-agents-working]`.
2. **context 는 유한 자원, 더 큰 window 가 해법 아님**: "context windows of all sizes will be subject to context pollution" `[anthropic-effective-context-engineering]`, "Context management has become a practical design problem, not just a model-capability problem" `[redis-context-compaction]`.
3. **상태는 context 밖 filesystem 에 외재화**: amnesiac agent + durable filesystem 합의 `[osmani-long-running-agents]` `[anthropic-effective-harnesses]` `[humanlayer-12-factor-agents]` `[anthropic-managed-agents]`.
4. **단순하게 시작, 복잡도는 측정이 정당화할 때만**: "adding complexity only when it demonstrably improves outcomes" `[anthropic-building-effective-agents]`, single-agent first `[openai-practical-guide-agents]`, "reliable 하면 clever 할 필요 없다" `[greyling-loop-engineering]`.
5. **변경은 배포 전 eval 로 검증**: "regressions surface in development instead of in production" `[braintrust-eval-driven-development]`, "A markdown edit without a before/after eval is a vibe" `[greyling-configured-not-coded]`.

### 논쟁점 (tensions)

**(a) 서브에이전트 분업 — read/write 축 종합**
정면 대립이되 시점·작업유형으로 종합 가능:
- Cognition 2025: "Running multiple agents in collaboration only results in fragile systems" — decision-making 분산이 conflicting premise 를 낳음 `[cognition-dont-build-multi-agents]`. 단 "agents today" 단서 명시.
- Cognition 2026: model 발전(~10개월)으로 입장 _조건부 완화_ — read(search/review)·planning 보조는 OK, write/decision 은 single-thread 유지 `[cognition-multi-agents-working]`.
- Anthropic: orchestrator-worker 가 90.2% 향상 — 단 "coordination 제약... shared context 를 요하거나 inter-agent dependency 무거운 domain 엔 부적합" `[anthropic-multi-agent-research-system]`.
- **종합 규칙**: **read 작업(search/review/citation)은 병렬 분업 OK, write/decision 은 single-thread**. 두 Cognition 글은 대립이 아니라 보완. tier-4 backing — multi-agent violation 은 inter-agent 정보 전달에 집중 `[arxiv-auditing-harness-safety]`.

**(b) GAN 비유의 한계**
- 차용: generator-discriminator adversarial loop 가 self-scoring 금지를 잘 설명 `[epsilla-gan-style-agent-loop]`.
- 한계: 저자 스스로 "evaluator ≠ pure GAN, more like a senior engineer reviewing a PR" — competitive adversarial 아님 `[mindstudio-planner-generator-evaluator]`. enterprise 에선 evaluator 가 "in a vacuum" 동작 (compliance·org state 접근 못 함) `[epsilla-gan-style-agent-loop]`. **GAN 라벨 문자 그대로 적용하면 오해** — cooperative review 로 한정 인용.

**(c) Harness 가치 감쇠론 (inversion)**
harness 만능론의 자기-제한:
- "harness 복잡도는 모델 개선에 따라 줄어야 한다" — v1 sprint construct → v2 제거 `[anthropic-harness-design-long-running-apps]`.
- **정량**: harness swap 만으로 23.8pt 이동하나, cross-harness variance 는 model 강해질수록 축소 — "Weak models are hostages to their harness… Strong models shrug it off… a crutch whose value decays as the model improves" `[greyling-agent-model-harness]` `[arxiv-harness-bench]`.
- minimal-loop 우월 — NanoBot 76.2 @ 7.3 turns < Hermes 71.2 @ 22.6 turns/139.7K tokens; "a small loop that keeps its books beats a large one that loses them" `[greyling-agent-model-harness]`.
- **caveat**: 이 inversion 의 미래 추정 부분("model that is about to outgrow it")은 Greyling 수사적 확장 — 측정은 논문 귀속.

**(d) Context file 과다의 역효과 (반례 데이터)**
- "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" `[anthropic-claude-code-best-practices]`.
- **정량 반례**: AGENTS.md 류 context file 이 오히려 task success rate 를 _낮추고_ inference cost +20% — broader exploration(과한 testing·file traversal) 유발. 결론: "human-written context file 은 minimal requirement 만" `[arxiv-evaluating-agents-md]`. less-is-more — SkillReducer 48% 압축에 quality +2.8% `[arxiv-skillreducer]`.
- system prompt as dumping ground 경고 — "attention 이 wall of text 에 thin 해짐(silent killer)" `[greyling-configured-not-coded]`.

**(e) configuration 세대의 규율 격차**
- prompt→harness collapse 는 "win"(less infra)이되, "Configuration is code in a different costume" — markdown edit 에 diff/predict/rollback/measure/prune 규율이 따라오지 않음 `[greyling-configured-not-coded]`. "model is rented, harness is owned".

---

## 4. Evolution Timeline

| 시점 | 사건 / 개념 | 카드 | 세대 |
|---|---|---|---|
| 2024-12 | **Building effective agents** (workflow vs agent, 6 조합 패턴) — harness 세대 정초 | `anthropic-building-effective-agents` | harness 정초 |
| 2025-03 | think tool (tool chain 도중 reasoning) | `anthropic-think-tool` | harness |
| 2025-04 | Claude Code best practices · OpenAI practical guide · Self-Improving Coding Agent (17→53%) | `anthropic-claude-code-best-practices` `openai-practical-guide-agents` `arxiv-self-improving-coding-agent` | harness/loop |
| 2025 (전반) | 12-Factor Agents · Writing tools for agents · Managed Agents (brain/hands) | `humanlayer-12-factor-agents` `anthropic-writing-tools-for-agents` `anthropic-managed-agents` | harness |
| 2025 | **Don't Build Multi-Agents** (Cognition, write 분산 반대) | `cognition-dont-build-multi-agents` | — |
| 2025-05 | SEW (self-evolving workflow) | `arxiv-sew` | — |
| 2025-06 | **Multi-agent research system** (orchestrator-worker, 90.2%) | `anthropic-multi-agent-research-system` | harness |
| 2025-07 | **Context Engineering** (Addy, prompt→context 명명) | `osmani-context-engineering` | **context** |
| 2025-08 | Context Eng for Multi-Agent Code Assistants | `arxiv-context-eng-multi-agent` | context |
| 2025-09 | **Effective context engineering** (Anthropic, canonical) · Secure Plan-then-Execute | `anthropic-effective-context-engineering` `arxiv-secure-plan-then-execute` | **context** |
| 2025-10 | Agent Skills (progressive disclosure) · Sandboxing (84%) · ACE (context collapse 측정) | `anthropic-agent-skills` `anthropic-claude-code-sandboxing` `arxiv-agentic-context-engineering` | context |
| 2025-11 | **Effective harnesses for long-running agents** (Anthropic, canonical) · Code execution MCP (98.7%) · Advanced tool use (85%) | `anthropic-effective-harnesses` `anthropic-code-execution-mcp` `anthropic-advanced-tool-use` | **harness** |
| 2025-12 | Long-running Agents (Addy, 시간 축) · PAACE | `osmani-long-running-agents` `arxiv-paace` | harness→loop |
| 2025 | Agent Harness Engineering (Addy, Trivedy 명명) · GitHub spec-kit · GAN-Style Loop (Epsilla) | `osmani-agent-harness-engineering` `github-spec-kit` `epsilla-gan-style-agent-loop` | harness |
| 2026-01 | Demystifying evals · AI-resistant evals · Eval-Driven Iteration · Spec-Driven(code-to-contract, constitutional) | `anthropic-demystifying-evals` `anthropic-ai-resistant-evals` `arxiv-eval-driven-iteration` `arxiv-spec-driven-code-to-contract` `arxiv-constitutional-spec-driven` | loop/eval |
| 2026-02 | C compiler with parallel Claudes (실증) · Infrastructure noise · Agentic Engineering Patterns (Willison) · Worktree(Zylos) · spec-driven(Owain) · Evaluating AGENTS.md | `anthropic-c-compiler-parallel-claudes` `anthropic-infrastructure-noise` `willison-agentic-engineering-patterns` `zylos-git-worktree-isolation` `owainlewis-spec-driven` `arxiv-evaluating-agents-md` | **loop** |
| 2026-03 | Harness design long-running apps · Claude Code auto mode · Rise of Harness Eng (Greyling) · Red Hat EDD · SkillReducer | `anthropic-harness-design-long-running-apps` `anthropic-claude-code-auto-mode` `greyling-rise-of-harness-engineering` `redhat-eval-driven-development` `arxiv-skillreducer` | harness/loop |
| 2026-04 | MindStudio Planner-Generator-Evaluator · Inside the Scaffold (taxonomy) | `mindstudio-planner-generator-evaluator` `arxiv-inside-the-scaffold` | harness |
| 2026-05 | Configured not coded (Greyling) · Code as Agent Harness (정식 정의) · Harness-Bench · Auditing Harness Safety | `greyling-configured-not-coded` `arxiv-code-as-agent-harness` `arxiv-harness-bench` `arxiv-auditing-harness-safety` | harness |
| 2026-06 | **Loop Engineering** (Addy 명명) · Loop Eng + Playbook (Greyling 정리) · Agent=Model+Harness (Greyling) | `osmani-loop-engineering` `greyling-loop-engineering` `greyling-loop-engineering-playbook` `greyling-agent-model-harness` | **loop** |

> 발행일 일부는 '월' 단위까지만 확정 (정확 일자 미확인). Greyling loop-engineering 류는 "1 day ago"/"16 hours ago" relative extract 로 2026-06 근사. Addy 블로그 frontmatter 는 "2025" 로 표기되나 글 내용·survey 매핑은 위 시점.

---

## 5. Gaps (근거 얇은 패턴 — 단일 소스 / tier 3 이하만)

- **Headless/cron 안전장치의 1차 측정**: tier 1 은 `claude-code-github-actions`(docs)·`anthropic-claude-code-auto-mode`(93% approve / 17% FN) 뿐. cron 운영 디테일은 tier 3 (`codewithseb-headless-cicd` 는 본문 403 차단으로 WebSearch snippet 경유, `mindstudio-headless-mode` 도 tier 3) — **verbatim 인용 정밀도 약함**.
- **Worktree 격리 정량 벤치**: 패턴 합의는 강하나 (`anthropic-c-compiler-parallel-claudes` 실증) 정량 비교는 tier 3 (`zylos`/`augmentcode`) 위주 — "four or more concurrent sessions" cap 은 환경 의존, peer-review 없음.
- **오답노트→케이스 승격의 자동화 메커니즘**: 원칙(`osmani-agent-harness-engineering` 정의)·구현 사례(`braintrust`/`redhat` "known bad")는 있으나 _자동 승격 알고리즘_ 은 tier 4 (`arxiv-agentic-context-engineering` ACE / `arxiv-self-improving-coding-agent`) 뿐 — 블로그 1차에는 자동화 절차 부재.
- **GAN 비유의 메커니즘 근거**: maker/verifier 합의는 tier 1 강하나, _왜_ self-eval 이 실패하는지(autocomplete bias)는 tier 2 단일 출처 `[mindstudio-planner-generator-evaluator]` 에만 명료.
- **Spec-driven 의 비용·과명세 역효과**: spec-first 찬성은 다수 (tier 1–4), 단 _작은 작업 over-spec overhead_ 는 `osmani-good-spec`("don't over-spec a trivial one") 한 줄 외 깊이 다룬 출처 없음.
- **OpenAI practical guide verbatim**: PDF binary parse 실패로 2차 출처 경유 — verbatim 인용은 원문 재확인 필요 `[openai-practical-guide-agents]`.
- **arXiv 수치 2차 인용**: Harness-Bench 핵심 수치(76.2/52.4/23.8/Codex 80.4)는 Greyling 카드 경유 2차 — fact-check 시 arXiv 원문·harness-bench.ai 와 verbatim 대조 권장 `[greyling-agent-model-harness]`.

---

## 6. Phase Flags

- **chaining_available: false** (intentional) — technology mode 는 reference chaining(Phase B) 비활성. `chaining_results.md` 부재는 설계상 정상. 학술 인용망 추적이 필요하면 별도 academic-mode 재조사 필요.
- **code_search_available: true** — `_internal/code_search.md` + `code_resources/tier{1,2,3}_*.md` 에 패턴별 canonical 구현 repo 매핑 존재 (12-factor-agents · spec-kit · claude-code · OpenHands · SWE-agent · aider · langgraph · crewAI · ace-agent · promptfoo 등). 인용 caveat — spec-kit star "~100k+ 급성장"(편차 큼), Braintrust/LangSmith 는 플랫폼 가치로(SDK star 부적합), AG2≠원조 AutoGen, Inside-the-Scaffold 13개는 taxonomy 표 인용.

> **누락 디렉터리 알림**: 본 조사 산출물에는 `analysis_project/paper/`·`analysis_project/code/` 가 없음 (research-only 도메인 — 정상). 결론은 61 cards + code_search + agent memory 에 근거. 매뉴얼 2부(우리 실물 매핑)는 draft 작성 시점의 CLAUDE.md·CONVENTIONS·loops/README 를 직접 Read 할 것 (`draft_directives` §4 staging 지시).
