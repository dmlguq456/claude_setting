# 04 — 실무 패턴 Deep Dive

> 가장 중요한 챕터. 패턴 11종 각각: 문제 정의 → 핵심 원칙(verbatim + [card]) → 메커니즘 → 정량 근거(카드 수치만) → 반론·한계 → 매뉴얼 인용 포인트. 이어서 Tensions 4종 + 미해결 과제.

---

## P1. Plan-then-execute (계획·실행 분리)

- **문제**: 같은 agent 에게 계획과 실행을 동시에 맡기면 엉뚱한 문제를 풀거나 edge case 를 놓친다.
- **핵심 원칙 (verbatim)**: "Separate research and planning from implementation to avoid solving the wrong problem" `[anthropic-claude-code-best-practices]`. "don't ask the same agent to plan the work and do the work" — planning(edge-case 분석)과 execution(shipping)은 서로 다른 cognitive mode 다 `[owainlewis-spec-driven]`. "Planning in advance matters even more with an agent - you can iterate on the plan first, then hand it off to the agent" `[osmani-good-spec]`.
- **메커니즘**: explore→plan→implement→commit 4단계 + plan mode `[anthropic-claude-code-best-practices]`. agent 는 "plan and operate independently" `[anthropic-building-effective-agents]`.
- **반론·한계**: plan mode 는 overhead — "If you could describe the diff in one sentence, skip the plan" `[anthropic-claude-code-best-practices]`. tier-4 backing: P-t-E 가 ReAct 대비 predictability·cost 우위 `[arxiv-secure-plan-then-execute]`.
- **매뉴얼 인용 포인트**: 1부 plan-then-execute 절의 1차 verbatim 은 `[anthropic-claude-code-best-practices]` + `[owainlewis-spec-driven]`. "작은 작업은 plan skip" caveat 동반.

## P2. Spec-driven development (spec-first)

- **문제**: 즉흥 prompt 는 agent 가 수십 개의 결정을 추측하게 만들고, 그 추측이 누적된다.
- **핵심 원칙 (verbatim)**: "We're moving from 'code is the source of truth' to 'intent is the source of truth'" `[github-spec-kit]`. "A plan Claude generates lives in a conversation. A spec lives in your repo" `[owainlewis-spec-driven]`. "Specs become the shared source of truth… living, executable artifacts that evolve with the project" `[osmani-good-spec]`. "the bottleneck shifts from implementation to specification" `[owainlewis-spec-driven]`.
- **메커니즘**: spec-kit 4-phase Specify→Plan→Tasks→Implement 에서 Tasks 가 spec 을 small isolated chunk 로 분해한다(TDD 유사) `[github-spec-kit]`. spec 4-요소는 Context/Scope/Constraints/Tasks `[owainlewis-spec-driven]`.
- **정량 근거 (tier 4 보조)**: constitutional spec-driven 에서 **보안 defect −73%** velocity 유지 `[arxiv-constitutional-spec-driven]`.
- **반론·한계**: 작은 작업 over-spec overhead — "Don't under-spec a hard problem… but don't over-spec a trivial one" `[osmani-good-spec]`. 거대 spec 통째 주입은 context/attention 한계로 실패 — "practical context size 안에서 진화하는 spec" `[osmani-good-spec]`.
- **매뉴얼 인용 포인트**: 하드 순서 게이트(spec 없이 code 금지)의 철학적 근거 = "intent is the source of truth". 단계 동형 = spec-kit. _왜_ 분리하나 = owain/good-spec.

## P3. Maker-verifier 분리 (자기채점 금지)

- **문제**: 모델은 자기 산출물을 후하게 평가한다 (가장 합의 강한 원칙).
- **핵심 원칙 (verbatim)**: "When asked to evaluate work they've produced, agents tend to respond by confidently praising the work—even when, to a human observer, the quality is obviously mediocre" / "Separating the agent doing the work from the agent judging it proves to be a strong lever" `[anthropic-harness-design-long-running-apps]`. model 은 "pathological optimists", "By engineering conflict, you engineer progress" `[epsilla-gan-style-agent-loop]`. "Models reliably skew positive when they grade their own work" `[osmani-long-running-agents]`.
- **메커니즘 근거**: autocomplete bias — "When the same model that wrote the code reviews it, it tends to overlook its own mistakes" `[mindstudio-planner-generator-evaluator]`. adversarial reviewer — "a fresh model try to refute the result, so the agent doing the work isn't the one grading it" / "A reviewer running in a fresh subagent context sees only the diff and the criteria... not the reasoning that produced the change" `[anthropic-claude-code-best-practices]`.
- **일반화**: brain/hands 분리 `[anthropic-managed-agents]` · CitationAgent 별도 검증 `[anthropic-multi-agent-research-system]` · red/green TDD `[willison-agentic-engineering-patterns]`.
- **반론·한계 (GAN 비유 caveat)**: "the evaluator isn't adversarial in a competitive sense. It's more like a senior engineer reviewing a pull request" `[mindstudio-planner-generator-evaluator]` — GAN 라벨을 문자 그대로 적용하면 안 된다. adversarial reviewer 도 과신하면 안 된다 — "A reviewer prompted to find gaps will usually report some, even when the work is sound... Chasing every finding leads to over-engineering" `[anthropic-claude-code-best-practices]`.
- **매뉴얼 인용 포인트**: 1부 핵심 패턴. verbatim 1차 = `[anthropic-harness-design-long-running-apps]` + `[epsilla-gan-style-agent-loop]`. 메커니즘(왜 실패하나) = `[mindstudio-planner-generator-evaluator]`. GAN caveat 반드시 동반.

## P4. 서브에이전트 분업 (orchestrator-worker)

- **문제**: 단일 agent 는 context window·path dependency 에 갇히고, 다중 agent 는 깨지기 쉬워질(fragile) 위험이 있다.
- **핵심 원칙 (찬성, verbatim)**: orchestrator-worker 가 single-agent 대비 내부 eval **90.2% 향상**, "Multi-agent systems work mainly because they help spend enough tokens to solve the problem" `[anthropic-multi-agent-research-system]`. clean-context 찬성: "A clean-context reviewer catches bugs the coder can't see" `[cognition-multi-agents-working]`.
- **핵심 원칙 (반대, verbatim)**: "Running multiple agents in collaboration only results in fragile systems" — "Actions carry implicit decisions, and conflicting decisions carry bad results" `[cognition-dont-build-multi-agents]`.
- **메커니즘**: 각 sub-agent 가 별도 context window 에서 병렬 압축, 1,000–2,000 token 요약 반환 `[anthropic-effective-context-engineering]`. manager pattern(agents as tools) / decentralized(handoff) `[openai-practical-guide-agents]`.
- **정량 근거**: multi-agent 는 chat 대비 약 **15배 token**, subagent 3–5개 병렬 → research time 최대 **90% 단축** `[anthropic-multi-agent-research-system]`. enterprise 사용 **~8x 성장** `[cognition-multi-agents-working]`.
- **반론·한계**: coordination 제약 — "shared context 를 요하거나 inter-agent dependency 무거운 domain 엔 부적합" `[anthropic-multi-agent-research-system]`. → **read/write 축 종합 필수** (아래 Tension a).
- **매뉴얼 인용 포인트**: read 작업은 병렬 분업 OK, write/decision 은 single-thread. 두 Cognition 글을 보완으로 인용.

## P5. 파이프라인 세분화

- **문제**: 거대한 monolithic 작업은 검증이 불가능하고 context 를 넘친다.
- **핵심 원칙 (verbatim)**: prompt chaining — "decomposes a task into a sequence of steps, where each LLM call processes the output of the previous one" `[anthropic-building-effective-agents]`. Tasks 단계가 spec 을 "small, review-able, isolated work chunk" 로 쪼갠다 `[github-spec-kit]`.
- **메커니즘**: research loop → citation verification → final compilation 순차 phase `[anthropic-multi-agent-research-system]`. feature-by-feature 점진 진행 `[anthropic-effective-harnesses]`.
- **반론·한계 (tier 4)**: loop primitive 는 _배타적 타입이 아니라 조합 가능_ — "compositions of loop primitives along continuous spectra" `[arxiv-inside-the-scaffold]`. 즉 세분화 단계 수는 고정 규칙이 아니라 spectrum.
- **매뉴얼 인용 포인트**: 우리 파이프(research→spec→code, plan→dev_logs)의 단계 분해 근거 = building-effective-agents + spec-kit.

## P6. Golden set · eval 회귀

- **문제**: markdown/prompt 변경이 개선인지 측정하지 않고 배포하면 조용히 regress 한다.
- **핵심 원칙 (verbatim)**: "frozen core(golden set) + growing set" 이분법, "If your eval correctly captures what 'good' means, then optimizing against it is sufficient" / "When every change runs through the same eval suite before shipping, regressions surface in development instead of in production" `[braintrust-eval-driven-development]`. "A markdown edit without a before/after eval is a vibe" `[greyling-configured-not-coded]`.
- **메커니즘**: eval anatomy(Task/Trial/Grader/Transcript/Outcome), "what proportion of trials an agent succeeds"(pass@k), eval saturation, 20–50 simple task 로 출발 `[anthropic-demystifying-evals]`. judge calibration, "known bad" set `[redhat-eval-driven-development]`.
- **정량 근거 (신뢰성)**: infrastructure noise — Terminal-Bench 2.0 에서 strict↔uncapped 사이 **6%p swing**, "A few-point lead might signal a real capability gap—or it might just be a bigger VM" `[anthropic-infrastructure-noise]`.
- **반론·한계 (tier 4)**: Goodhart 위험 — eval 이 "good" 을 부정확하게 포착하면 잘못 최적화. generic prompt 개선이 오히려 해침 — Qwen 2.5 RAG 26/30→9/30 `[arxiv-eval-driven-iteration]`.
- **매뉴얼 인용 포인트**: golden set 회귀의 canonical = demystifying-evals + Braintrust. noise floor 정량화 caveat = infrastructure-noise.

## P7. 오답노트 → 케이스 승격 (failure-driven evolution)

- **문제**: 같은 실수를 반복하면 누적 비용이 크다.
- **핵심 원칙 (verbatim, 1차 정의)**: "anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again" `[osmani-agent-harness-engineering]`. "failure-driven evolution" — production 실패를 correct reference 와 함께 golden dataset 에 추가해 "permanent regression guards" 로 굳힌다 `[braintrust-eval-driven-development]`. bug tracker·support queue 를 task 소스로 삼는다 `[anthropic-demystifying-evals]`.
- **메커니즘 (tier 4)**: Reflector→Curator playbook delta update — Generator(생성)/Reflector(insight 추출)/Curator(통합) `[arxiv-agentic-context-engineering]`. self-edit 로 SWE-bench **17%→53%** `[arxiv-self-improving-coding-agent]`.
- **반론·한계**: 블로그 1차에는 _자동_ 승격 절차가 없다 (Gap — 자동화 메커니즘은 tier 4 에만 있다). system prompt 에 "be careful about X" 만 쌓으면 attention 이 옅어진다 — "silent killer" `[greyling-configured-not-coded]`.
- **매뉴얼 인용 포인트**: 우리 post-it·golden loop(실패→지침 승격)의 근거. 단 "자동 승격" 주장은 tier 4 backing 만 있음을 명시.

## P8. 상태 파일 · 세션 간 영속성

- **문제**: agent 는 amnesiac 이다 — 매 세션이 교대 근무자처럼 기억이 없다.
- **핵심 원칙 (verbatim)**: "State lives outside the agent's context… the agent itself is amnesiac, but the filesystem isn't" / "git as the coordination substrate" `[osmani-long-running-agents]`. "each new engineer arrives with no memory of what happened on the previous shift" `[anthropic-effective-harnesses]`. Factor 5(unify execution+business state)/6(pause/resume)/12(stateless reducer) `[humanlayer-12-factor-agents]`.
- **메커니즘**: 세 artifact — `claude-progress.txt`(로그)/`feature_list.json`(immutable acceptance)/git history `[anthropic-effective-harnesses]`. session = context window 밖 append-only event log, `getEvents()` slice `[anthropic-managed-agents]`. L1 working(TTL)/L2 long-term(vector) hierarchy `[redis-context-compaction]`.
- **반론·한계 (tier 4)**: context file 과다는 역효과 (아래 Tension d). stateless reducer 는 이상형 — 실제 LLM 은 완전 pure 하기 어려움 `[humanlayer-12-factor-agents]`.
- **매뉴얼 인용 포인트**: **산출물 기반 소통 원칙** 의 1차 근거 — agent 는 context 를 공유하는 게 아니라 파일 산출물로 소통한다(`.claude_reports` 통신 버스). verbatim = `[osmani-long-running-agents]` + 12-factor.

## P9. Worktree 병렬 격리

- **문제**: 두 agent 가 같은 tree 에서 동시에 작업하면 file collision·index corruption 이 난다.
- **핵심 원칙 (verbatim)**: "When two agents operate concurrently in the same tree, the failure modes are severe: File collisions, context contamination, index corruption, and conversation confusion" / "The 'Rebase Before PR' model is the most widely recommended convention" `[zylos-git-worktree-isolation]`. "Each worktree gets a private HEAD, private index, and private working directory" `[augmentcode-git-worktrees]`.
- **메커니즘**: 공유 object store + private HEAD/index, container clone-push 격리 + lock 파일 task 조율 — "Merge conflicts are frequent, but Claude is smart enough to figure that out" `[anthropic-c-compiler-parallel-claudes]`. deferred conflict → PR merge 단계("visible git conflicts instead of silent runtime overwrites") `[augmentcode-git-worktrees]`.
- **정량 근거 (안전 층)**: filesystem+network sandboxing — "sandboxing safely reduces permission prompts by **84%**" `[anthropic-claude-code-sandboxing]`. "four or more concurrent sessions" cap (환경 의존) `[zylos-git-worktree-isolation]`.
- **반론·한계**: 정량 비교는 tier 3 위주, peer-review 없음 (Gap). worktree 자체 비용(creation/disk/removal) 존재 `[zylos-git-worktree-isolation]`.
- **매뉴얼 인용 포인트**: 우리 §5.10 worktree 본작업 정책의 외부 근거 = zylos(패턴) + C compiler(실증) + sandboxing(격리 층).

## P10. Headless · cron 자동화

- **문제**: 사람이 매 turn 붙어 있는 한 자율 운영이 안 된다.
- **핵심 원칙 (verbatim)**: `@claude` mention → PR 자동 생성, `on: schedule: cron`, Agent SDK 기반 `[claude-code-github-actions]`. "claude -p" CI/pre-commit + fan-out(`for file in ...; do claude -p ... done`) `[anthropic-claude-code-best-practices]`.
- **메커니즘 (안전장치)**: auto mode classifier — "Claude Code users approve **93%** of permission prompts"(17% false-negative) `[anthropic-claude-code-auto-mode]`. `--dangerously-skip-permissions` 는 격리 환경에서만 `[mindstudio-headless-mode]`.
- **운영 패턴**: cron 3원칙(full path / env 명시 / output redirect) `[mindstudio-headless-mode]`.
- **반론·한계 (Gap)**: tier 1 은 docs + auto-mode 뿐, cron 운영 디테일은 tier 3(`codewithseb-headless-cicd` 본문 403 차단, `mindstudio-headless-mode`) — verbatim 정밀도 약함.
- **매뉴얼 인용 포인트**: headless/cron 절 = github-actions(진입점) + auto-mode(안전장치). cron 3원칙은 tier 3 출처 명시.

## P11. 컨텍스트 절약 (고정 오버헤드 / 압축)

- **문제**: context 는 유한 자원, attention budget 은 token 마다 소진된다.
- **핵심 원칙 (verbatim)**: "Find the smallest possible set of high-signal tokens that maximize the likelihood of your desired outcome" `[anthropic-effective-context-engineering]`. progressive disclosure — "Skills let Claude load information only as needed" `[anthropic-agent-skills]`. "The right optimization target is not tokens per request. It is tokens per task" `[factory-evaluating-compression]`.
- **정량 근거**: code execution MCP **150,000→2,000 tokens, 98.7% 절감** `[anthropic-code-execution-mcp]`. Tool Search **85% 절감**, programmatic calling 43,588→27,297 = **37% 절감** `[anthropic-advanced-tool-use]`. SkillReducer 48% description/39% body 압축에 quality **+2.8%** `[arxiv-skillreducer]`.
- **메커니즘**: raw → reversible compaction → lossy summarization 단계 폴백, L1/L2 hierarchy `[redis-context-compaction]`. just-in-time retrieval(lightweight identifier) `[anthropic-effective-context-engineering]`.
- **반론·한계**: aggressive 압축은 re-fetch 로 token 낭비 (tokens-per-task) `[factory-evaluating-compression]`. compaction 공통 약점 — artifact trail preservation 모든 방법 2.19–2.45 `[factory-evaluating-compression]`. overly aggressive compaction 은 "subtle but critical context" 손실 `[anthropic-effective-context-engineering]`.
- **매뉴얼 인용 포인트**: CLAUDE.md 얇은 부트스트랩·on-demand Read·skill progressive disclosure 의 근거. 정량 수치는 카드 명시값만.

---

## Tensions (논쟁점 종합)

### ① 서브에이전트 분업 찬반 — read/write 축 종합

정면으로 대립하지만 시점·작업유형으로 종합할 수 있다.

| 출처 | 입장 | 단서 |
|---|---|---|
| Cognition 2025 | "Running multiple agents in collaboration only results in fragile systems" — decision 분산 반대 `[cognition-dont-build-multi-agents]` | "agents today" 시점 한정 명시 |
| Cognition 2026 | 입장 _조건부 완화_ — read(search/review)·planning 보조는 OK, write/decision 은 single-thread `[cognition-multi-agents-working]` | 모델 ~10개월 발전 |
| Anthropic | orchestrator-worker 90.2% 향상 `[anthropic-multi-agent-research-system]` | "shared context/heavy dependency domain 엔 부적합" |

> **종합 규칙**: **read 작업(search/review/citation)은 병렬 분업 OK, write/decision 은 single-thread.** 두 Cognition 글은 대립이 아니라 보완이다. tier-4 backing — multi-agent violation 은 주로 inter-agent 정보 전달에서 일어난다 `[arxiv-auditing-harness-safety]`.

### ② GAN 비유의 한계

- 차용: generator-discriminator adversarial loop 가 self-scoring 금지를 잘 설명한다 `[epsilla-gan-style-agent-loop]`.
- 한계: 저자 스스로 "evaluator ≠ pure GAN, more like a senior engineer reviewing a PR" 라고 못박는다 — competitive adversarial 이 아니다 `[mindstudio-planner-generator-evaluator]`. enterprise 에선 evaluator 가 "in a vacuum" 으로 동작한다 (compliance·org state 에 접근하지 못함) `[epsilla-gan-style-agent-loop]`. **GAN 라벨을 문자 그대로 적용하면 오해를 부른다 — cooperative review 로 한정해 인용한다.**

### ③ Harness 가치 감쇠론 (inversion)

harness 만능론을 스스로 제한하는 논의다:
- "harness 복잡도는 모델 개선에 따라 줄어야 한다" — v1 sprint construct → v2 제거 `[anthropic-harness-design-long-running-apps]`.
- **정량**: harness 만 바꿔도 **23.8pt 이동**(동일 task·동일 model pool), NanoBot 76.2 vs OpenClaw 52.4 — 단 cross-harness variance 는 model 이 강해질수록 줄어든다. "Weak models are hostages to their harness… Strong models shrug it off… a crutch whose value decays as the model improves" `[greyling-agent-model-harness]`.
- minimal-loop 가 더 낫다 — NanoBot 76.2 @ 7.3 turns < Hermes 71.2 @ 22.6 turns/139.7K tokens; "a small loop that keeps its books beats a large one that loses them" `[greyling-agent-model-harness]`.
- **caveat**: 수치는 Harness-Bench 논문에 귀속된다(Greyling 2차 인용). 미래 추정("model that is about to outgrow it")은 Greyling 의 수사적 확장이다.

### ④ Context file 과다의 역효과 (반례 데이터)

- "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!" `[anthropic-claude-code-best-practices]`.
- **정량 반례 (tier 4)**: AGENTS.md 류 context file 이 오히려 task success rate 를 _낮추고_ inference cost 를 **+20%** 늘린다 — broader exploration(과한 testing·file traversal)을 유발하기 때문이다. "human-written context file 은 minimal requirement 만" `[arxiv-evaluating-agents-md]`. less-is-more — SkillReducer 48% 압축에 quality +2.8% `[arxiv-skillreducer]`.
- system prompt 를 dumping ground 로 쓰지 말라는 경고 — "attention 이 wall of text 에 옅어진다(silent killer)" `[greyling-configured-not-coded]`.
- **추가 메타-tension (configuration 규율 격차)**: prompt→harness collapse 는 "win"(less infra)이지만, "Configuration is code in a different costume" — markdown edit 에는 diff/predict/rollback/measure/prune 규율이 따라오지 않는다. "The model is rented, the harness is owned" `[greyling-configured-not-coded]`.

---

## 미해결 과제 (근거 얇은 패턴 — 매뉴얼에서 단정 금지)

1. **Headless/cron 안전장치의 1차 측정**: tier 1 은 docs + auto-mode(93%/17% FN)뿐이고, cron 운영 디테일은 tier 3 — verbatim 정밀도가 약하다.
2. **Worktree 격리 정량 벤치**: 합의는 강하지만(C compiler 실증) 정량 비교는 tier 3(zylos/augmentcode)에 머물고, "four or more" cap 은 환경에 따라 다르며 peer-review 도 없다.
3. **오답노트→케이스 승격의 자동화 메커니즘**: 원칙·구현 사례는 있으나 _자동 승격 알고리즘_ 은 tier 4(ACE/SICA)뿐이다 — 블로그 1차에는 자동화 절차가 없다.
4. **GAN 비유의 메커니즘 근거**: maker/verifier 합의는 tier 1 에서 강하지만, _왜_ self-eval 이 실패하는지(autocomplete bias)는 tier 2 단일 출처 `[mindstudio-planner-generator-evaluator]` 에서만 명료하다.
5. **Spec-driven 의 과명세 역효과**: spec-first 찬성은 다수지만, _작은 작업 over-spec overhead_ 는 `[osmani-good-spec]`("don't over-spec a trivial one") 한 줄 외에 깊이 다룬 출처가 없다.
6. **"science of harness engineering" 부재**: 학술 survey 가 principled design methodology 결여를 open challenge 로 명시한다 `[arxiv-code-as-agent-harness]`(§5.2) — harness 가 아직 정립된 분과가 아님을 인정하는 셈이다.

**Takeaway**: P1–P8·P11 은 매뉴얼에서 단정적으로 서술할 수 있고, P9·P10·P7(자동화)은 tier 3/4 의존 caveat 를 동반하며, Tension ①④와 미해결 과제는 반드시 반론과 함께 균형 있게 서술한다. 정량 수치는 위 카드 명시값만 쓰고, fact-check 권장 항목(Harness-Bench 76.2/52.4/23.8)은 arXiv 원문과 대조한다.
