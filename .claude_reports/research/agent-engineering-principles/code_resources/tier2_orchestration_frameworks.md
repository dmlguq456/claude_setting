# Tier 2 — Harness / Orchestration 프레임워크

> maker/verifier·plan-execute·handoff 패턴 지원 여부 중심. star/last-update 는 2026-06-11 확인값, 대략치.

---

## langchain-ai/langgraph

- **url**: https://github.com/langchain-ai/langgraph
- **stars**: ~34k
- **language**: Python (~99%)
- **last-update**: 2026-06-10 (cli 0.4.28)
- **패턴 지원**: graph 기반 stateful orchestration · **durable execution / checkpointing** (pause/resume·state 영속 — 12-factor Factor 6 지원) · human-in-the-loop · memory 관리. plan-execute·maker-verifier 를 명시적 graph node 로 표현 가능.
- **매뉴얼 인용 가치**: 매뉴얼의 "상태 파일 영속성 + pause/resume" 를 framework 차원에서 제공하는 대표 low-level orchestration. control-flow 명시화 (Factor 8) 의 graph 형 구현 예시.
- **Quick verify**: `pip install -U langgraph && python -c "import langgraph; print(langgraph.__version__)"`

---

## crewAIInc/crewAI

- **url**: https://github.com/crewAIInc/crewAI
- **stars**: ~53k
- **language**: Python (~99%)
- **last-update**: 2026-05-28 (v1.14.6)
- **패턴 지원**: role-based multi-agent 협업 (manager/worker 역할 분담) · Crews(자율 협업) + Flows(결정론적 제어) 이중 구조. plan-execute (Flow) 와 역할 분업 (maker/verifier 를 role 로) 지원.
- **매뉴얼 인용 가치**: OpenAI "manager pattern" / 매뉴얼의 서브에이전트 역할 분업 (연구팀/품질관리팀) 을 framework 로 구현한 대표 예. 단 다중 자율 agent — 매뉴얼은 "서브에이전트 중첩 1단" 으로 더 평면적임 (대비 인용 가치).
- **Quick verify**: `uv pip install crewai && python -c "import crewai; print(crewai.__version__)"`

---

## ag2ai/ag2 (AutoGen 후속)

- **url**: https://github.com/ag2ai/ag2
- **stars**: ~4.7k (AG2 org; 원조 microsoft/autogen 은 별도·더 높음)
- **language**: Python (~63%)
- **last-update**: 2026-06-05 (v0.13.3)
- **패턴 지원**: multi-agent conversation framework · GroupChat·nested chat·tool-use 협업. maker/verifier 를 대화하는 agent 쌍으로, plan-execute 를 conversational orchestration 으로 구현. Microsoft AutoGen 에서 community fork (Apache 2.0 + 원 MIT).
- **매뉴얼 인용 가치**: conversational multi-agent 패턴의 대표 — 매뉴얼의 평면적 라우터 구조와 대비되는 "다중 agent 대화" 접근의 레퍼런스. (계보 주의: AutoGen=원조, AG2=community 후속)
- **Quick verify**: `pip install "ag2[openai]" && python -c "import autogen; print(autogen.__version__)"`

---

## mastra-ai/mastra

- **url**: https://github.com/mastra-ai/mastra
- **stars**: ~25k
- **language**: TypeScript (~99%)
- **last-update**: 2026-06 초
- **패턴 지원**: TypeScript agent framework · workflow (graph) + agents + tools + eval/memory 통합. plan-execute 를 workflow step 으로, maker/verifier 를 eval 통합으로. (Gatsby 팀 제작)
- **매뉴얼 인용 가치**: TS 생태계의 LangGraph 대응물 — workflow+eval 일체형. 매뉴얼의 eval-driven + 상태 workflow 결합 패턴의 TS 구현 예시.
- **Quick verify**: `npm create mastra@latest` (대화형 scaffold)

---

## openai/openai-agents-python

- **url**: https://github.com/openai/openai-agents-python
- **stars**: ~27k
- **language**: Python (~99%)
- **last-update**: 2026-06-11 (v0.17.5)
- **패턴 지원**: lightweight multi-agent · **handoffs** (agent→agent 위임 = OpenAI decentralized pattern) · **guardrails** (layered defense) · tools. plan-execute·manager pattern·maker/verifier 를 handoff+guardrail 로 구현. provider-agnostic.
- **매뉴얼 인용 가치**: OpenAI "Practical Guide to Building Agents" 의 manager/decentralized/guardrail 패턴을 직접 구현한 공식 SDK — 매뉴얼의 라우터+layered guardrail (hook gate) 구조의 정식 대응물.
- **카드**: `cards/openai-practical-guide-agents.md`
- **Quick verify**: `pip install openai-agents && python -c "import agents; print('ok')"`
