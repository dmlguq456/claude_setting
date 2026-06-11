# 07 — Open-source Code & Tools

> 패턴별 "이 패턴이 실제 구현된 곳" 레퍼런스다. star/last-update 는 WebFetch/WebSearch 확인값(2026-06-11 기준, 대략치)이고, URL 은 전부 검증했다. Quick verify command 는 autopilot-spec Phase 1.5 가 인용하는 source 다.

---

## 패턴 → 구현 매핑 한눈에

| 패턴 (매뉴얼 축) | 1차 구현 | 보조 구현 |
|---|---|---|
| 상태 영속성 / pause-resume / stateless reducer | humanlayer/12-factor-agents, langgraph (checkpointing) | aider (git-as-state), OpenHands (event-sourcing) |
| spec-first / plan-then-execute | github/spec-kit | openai-agents (handoff), crewAI (Flows) |
| harness loop / scaffold | anthropics/claude-code, OpenHands, SWE-agent, aider | claude-agent-sdk (programmatic) |
| trigger from anywhere (headless/CI) | claude-code-action, claude-agent-sdk | — |
| maker/verifier 역할 분업 | openai-agents, crewAI, ag2 | ace-agent/ace (Gen/Refl/Cur), SICA |
| context engineering / 오답노트→승격 | ace-agent/ace | claude-code (skills, progressive disclosure) |
| golden set / eval 회귀 | promptfoo (self-host) | Braintrust, langsmith-sdk (SaaS+SDK) |
| self-improvement / 메타-스킬 진화 | MaximeRobeyns/SICA, ace-agent/ace | — |
| harness 차원 비교 (학술) | Inside-the-Scaffold 13-agent taxonomy | — |

---

## Tier 1 — 패턴의 Canonical 구현

| repo | url | stars | 패턴 매핑 | Quick verify |
|---|---|---|---|---|
| **humanlayer/12-factor-agents** | github.com/humanlayer/12-factor-agents | ~23k | state 영속성(Factor 5/6/12)·control flow(8)·small agents(10) | `git clone https://github.com/humanlayer/12-factor-agents && ls content/` |
| **github/spec-kit** | github.com/github/spec-kit | ~100k+ (편차 큼) | spec-first(Specify→Plan→Tasks→Implement)·living artifact | `uv tool install specify-cli --from git+https://github.com/github/spec-kit.git && specify --help` |
| **anthropics/claude-code** | github.com/anthropics/claude-code | ~132k | harness loop·CLAUDE.md 부트스트랩·skill/plugin·git 자동화 | `curl -fsSL https://claude.ai/install.sh \| bash && claude --version` |
| **anthropics/claude-agent-sdk-python** | github.com/anthropics/claude-agent-sdk-python | ~7.3k | programmatic harness·**hooks for behavior 제어**·headless | `pip install claude-agent-sdk && python -c "import claude_agent_sdk; print(claude_agent_sdk.__version__)"` |
| **anthropics/claude-code-action** | github.com/anthropics/claude-code-action | ~7.9k | headless/CI 진입점·`@claude`→PR·cron schedule | (action) workflow 에 `uses: anthropics/claude-code-action@v1` + `@claude` 멘션 |
| **All-Hands-AI/OpenHands** | github.com/All-Hands-AI/OpenHands | ~76k | full agentic harness·containerized 격리·event-sourcing | `docker run -it -p 3000:3000 -v /var/run/docker.sock:/var/run/docker.sock docker.all-hands.dev/all-hands-ai/openhands:latest` |
| **SWE-agent/SWE-agent** | github.com/SWE-agent/SWE-agent | ~19.5k | ACI 설계·generate-test-repair·SWE-bench 회귀 | `pip install swe-agent && sweagent --help` |
| **Aider-AI/aider** | github.com/Aider-AI/aider | ~46k | repo map(PageRank) retrieval·git-as-state | `python -m pip install aider-install && aider-install && aider --help` |

---

## Tier 2 — Orchestration 프레임워크

| repo | url | stars | maker-verifier / plan-execute / handoff / 상태 영속 | Quick verify |
|---|---|---|---|---|
| **langchain-ai/langgraph** | github.com/langchain-ai/langgraph | ~34k | Partial / Yes / Partial / **Yes**(checkpointing) | `pip install -U langgraph && python -c "import langgraph; print(langgraph.__version__)"` |
| **crewAIInc/crewAI** | github.com/crewAIInc/crewAI | ~53k | Yes(role) / Yes(Flows) / Yes / Partial | `uv pip install crewai && python -c "import crewai; print(crewai.__version__)"` |
| **ag2ai/ag2** (AutoGen 후속) | github.com/ag2ai/ag2 | ~4.7k | Yes(대화) / Partial / Yes(GroupChat) / Partial | `pip install "ag2[openai]" && python -c "import autogen; print(autogen.__version__)"` |
| **mastra-ai/mastra** | github.com/mastra-ai/mastra | ~25k | Yes(eval) / Yes(workflow) / Partial / Yes | `npm create mastra@latest` |
| **openai/openai-agents-python** | github.com/openai/openai-agents-python | ~27k | Yes(guardrail) / Yes(manager) / **Yes**(handoff 1급) / Partial | `pip install openai-agents && python -c "import agents; print('ok')"` |

---

## Tier 3 — 보조·실험 코드 + Eval 도구

| repo | url | stars | 패턴 매핑 | Quick verify |
|---|---|---|---|---|
| **ace-agent/ace** (ACE) | github.com/ace-agent/ace | ~1.1k | Generator/Reflector/Curator 3-role·delta update·evolving playbook (오답노트→승격 정식화) | `git clone https://github.com/ace-agent/ace.git && cd ace && uv sync` |
| **MaximeRobeyns/self_improving_coding_agent** (SICA) | github.com/MaximeRobeyns/self_improving_coding_agent | ~343 | 자기 codebase 편집 self-edit 루프·Docker 격리 (SWE-bench 17%→53%) | `git clone ... && cd self_improving_coding_agent && make image` (Docker 필수) |
| **promptfoo/promptfoo** | github.com/promptfoo/promptfoo | ~22k | golden set(YAML)+assertion·red-teaming·provider 비교 (self-host eval) | `npm install -g promptfoo && promptfoo --version` |
| **Braintrust** (braintrustdata/*) | github.com/braintrustdata | SDK 소규모 (SaaS 핵심) | frozen core+growing set·failure-driven evolution (개념 출처) | `npm install braintrust autoevals` (platform API key 필요) |
| **langchain-ai/langsmith-sdk** | github.com/langchain-ai/langsmith-sdk | ~0.9k (SaaS 핵심) | trace 기반 eval·dataset regression·LangGraph 통합 | `pip install -U langsmith && python -c "import langsmith; print(langsmith.__version__)"` |

### Inside-the-Scaffold 13개 분석 대상 (arXiv 2604.03515)

source-code taxonomy 논문의 분석 대상 — harness 차원(control loop·tool interface·resource management) 비교 레퍼런스다. 13개 중 **7개가 각 15k+ stars**(채택 신호). 개별 repo: OpenCode · Gemini CLI · Codex CLI · **OpenHands** · Cline · **Aider** · **SWE-agent** · mini-swe-agent · AutoCodeRover · Agentless · Prometheus · Moatless Tools · DARS-Agent. → 개별 repo 를 깊이 인용하기보다 **taxonomy 표 자체**를 harness 차원 비교에 인용하고, 개별 URL 은 논문 내 pinned commit 을 참조한다 `[arxiv-inside-the-scaffold]`.

---

## Star 수 caveat (code_search.md 데이터 품질 주의 — 인용 시 반영)

- **spec-kit stars**: 출처별 편차가 크다 (직접 fetch 111k vs 2차 71~90k). 급성장 중이라 단일 숫자로 단정하지 말고 **"~100k+ 급성장"** 으로 인용한다.
- **Braintrust / LangSmith**: 핵심은 SaaS 플랫폼이다. GitHub SDK repo star(수십~수백)로 영향력을 판단하기 부적합하니, 개념 출처로만 인용하고 self-host eval 은 **promptfoo 를 권장**한다.
- **AG2 vs AutoGen**: AG2(ag2ai, ~4.7k)는 community 후속이고, microsoft/autogen(원조)은 별도이며 star 가 더 높다. **계보 혼동 주의** (인용 시 AutoGen=원조, AG2=후속 으로 명시).
- **Inside-the-Scaffold 13개**: 개별 repo URL 을 일괄 검증하지 않았다 — 인용 시 논문(pinned commit)을 거치길 권하고, taxonomy 표 자체를 인용 대상으로 삼는다.
- **last-update 일부**: claude-code/12-factor 는 commit count 만 노출하고 정확한 날짜는 안 보인다 — "활발" 로 표기한다.

## Quick verify command 자리 안내 (autopilot-spec Phase 1.5 인용 source)

위 표의 **Quick verify** 열은 각 repo 가 실제로 설치·동작하는지 한 줄로 확인하는 명령이다. autopilot-spec Phase 1.5(stack 검증)가 이 열을 인용해, 매뉴얼이 언급한 도구를 실제로 검증 가능한 형태로 제시한다. 단 `--dangerously-skip-permissions` 류 위험 명령은 격리 환경을 전제로 한다 ([05_deployment.md](05_deployment.md) §2 참조).

**Takeaway**: 패턴별 canonical 구현은 — 상태 영속성=12-factor-agents/langgraph, spec-first=spec-kit, harness=claude-code/OpenHands, headless=claude-code-action, maker-verifier=openai-agents/ace, golden set self-host=promptfoo, self-improvement=ace/SICA 다. star 수치는 모두 대략치이며, spec-kit·SaaS SDK·AG2 계보는 위 caveat 를 동반해 인용한다.
