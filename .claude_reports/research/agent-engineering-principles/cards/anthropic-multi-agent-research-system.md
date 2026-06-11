---
title: How we built our multi-agent research system
authors: Anthropic Engineering
venue: Anthropic Engineering Blog
year-month: 2025
url: https://www.anthropic.com/engineering/multi-agent-research-system
raw_type: engineering blog (technology)
tier: 1
---

## Core Claims
1. **orchestrator-worker 패턴** — lead agent 가 병렬 specialized subagent 를 조율해 single-agent 대비 내부 eval 에서 90.2% 향상. multi-agent 는 chat 대비 약 15배 token 을 쓰나 복잡 research task 에서 비례 가치.
2. multi-agent 가 통하는 주된 이유는 **충분한 token 을 쓰게 해서**다 ("spend enough tokens to solve the problem"). subagent 는 별도 context window 에서 정보를 병렬 압축, path dependency 를 줄임.
3. research 는 unpredictable·path-dependent — 조사가 풀리며 pivot/tangent 탐색 유연성이 필요해 multi-agent 가 적합.
4. **agent 는 stateful 이고 error 가 compound** 한다 — checkpoint 재개·graceful adaptation 으로 대응. minor 변경이 큰 behavioral 변화로 cascade.

## Key Concepts & Definitions
- **Orchestrator-Worker 패턴**: lead agent 가 과정을 조율하며 병렬 동작 specialized subagent 에 위임.
- **Lead Agent**: user query 분석·전략 수립·subagent spawn·결과 synthesize.
- **Subagents**: search tool 로 여러 측면을 동시 탐색해 findings 를 lead 에 반환하는 specialized agent.

## Patterns Covered
- **plan-then-execute**: lead agent 가 접근을 think-through 후 subagent spawn 전 plan 을 memory 에 저장.
- **maker-verifier 분리**: CitationAgent 가 별도로 문서를 처리해 claim 을 source 에 검증·귀속.
- **서브에이전트 분업**: lead 가 query 를 objective·output format·경계가 명확한 subtask 로 분해.
- **파이프라인 세분화**: research loop → citation verification → final compilation 순차 phase.
- **golden set·eval**: 실사용 패턴을 대표하는 약 20개 test query 로 시작 (조기 impact 감지).
- **상태 파일·영속성**: 200K token truncation 전 research plan 을 memory 에 저장.
- **격리·병렬**: subagent 3-5개 병렬 실행, 각자 3+ tool 병렬 호출 → research time 최대 90% 단축.
- **컨텍스트 절약·compaction**: 완료 phase 를 summarize 해 essential 정보를 external memory 에 저장.
- **오답노트/error handling**: 재시작 대신 checkpoint resume, error 시 graceful adaptation.

## Generation Mapping
- **orchestrator-worker (서브에이전트 분업)** 의 1차 근거 (조사 컨텍스트 #3 지정 역할) — lead/subagent 분업·병렬 압축이 사용자 매뉴얼 "서브에이전트 분업 / 파이프라인 세분화" 출처.
- **context engineering**: 별도 context window 병렬 압축 + memory 외재화 + phase summarize 가 compaction·context 절약의 multi-agent 형태.
- **loop engineering / eval**: 20개 golden query·prompt iteration·"think like your agents" 가 golden set·오답노트 패턴 근거.
- 등장 배경: open-ended research 가 path-dependent·병렬화 가능하다는 task 특성에서 orchestrator-worker 를 채택한 production 회고. 사용자 매뉴얼 maker-verifier(CitationAgent)·plan-then-execute(memory plan)·golden set 의 종합 출처.

## Quotable
1. "Multi-agent systems work mainly because they help spend enough tokens to solve the problem." (Benefits of a multi-agent system 섹션) — multi-agent 효용의 본질=token 예산.
2. "Think like your agents. To iterate on prompts, you must understand their effects." (Prompt engineering and evaluations for research agents 섹션) — prompt iteration 원칙.
3. "Agents are stateful and errors compound." (Production reliability and engineering challenges 섹션) — stateful agent 의 error 누적 위험.

## Limitations / Caveats
- **token economics**: 15배 token 을 정당화할 만큼 가치가 높은 task 에만 적합.
- **coordination 제약**: 모든 agent 가 shared context 를 요하거나 inter-agent dependency 가 무거운 domain 엔 부적합.
- **synchronous bottleneck**: 현재 lead 가 subagent 를 synchronous 실행 — 단일 subagent 완료 대기 중 전체 system block.
- **non-determinism**: 동일 prompt 가 다른 behavior 산출 → 디버깅·검증 난이.
- **emergent behavior**: 작은 prompt 변경이 예측 불가하게 subagent behavior 변화.
- **state complexity**: long-running stateful agent 가 durable execution·error recovery infra 를 요구.
