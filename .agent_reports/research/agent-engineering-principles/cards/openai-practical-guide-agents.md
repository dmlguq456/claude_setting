---
title: "A Practical Guide to Building Agents"
authors: OpenAI
venue: OpenAI Business Guides and Resources (whitepaper, 32 pages)
year-month: 2025-04
url: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
raw_type: vendor whitepaper (PDF)
tier: 1
fetch_note: "PDF는 binary 라 WebFetch parse 실패 → WebSearch + maginative.com 2차 요약으로 카드 작성. verbatim 인용은 2차 출처 경유라 paraphrase 혼입 가능."
---

## Core Claims
- (verbatim) "systems that independently accomplish tasks on your behalf" — agent 의 정의. LLM 으로 workflow 를 제어하고, context·action 을 위해 tool 에 접근하며, 정의된 guardrail 안에서 동작하는 시스템.
- (verbatim) single-agent 는 "an agent loops through tool calls until exit conditions are met" — 단일 agent 가 exit condition 만족까지 tool call loop 을 도는 구조가 출발점.

## Key Concepts & Definitions
- **Agent 의 3 축 (core components)**: (1) **Models** — accuracy/latency/cost 균형. 강한 모델로 baseline 잡고 필요 시 down-scale. (2) **Tools** — "reusable, well-documented tools for data retrieval and action". (3) **Instructions** — "clear, unambiguous instructions that break tasks into discrete steps and anticipate edge cases".
- **Tool 분류**: data (retrieval) / action (외부 상태 변경) / orchestration (다른 agent 호출).
- **언제 agent 인가**: 전통적 automation 이 부족한 곳 — 복잡한 decision-making, rule system 이 너무 불어난 경우, unstructured data 의존 process.
- **Guardrail = layered defense**: relevance classifier (주제 이탈 방지), safety classifier, PII filter, tool safeguards (실행 전 risk 평가), human-in-the-loop (high-risk action·반복 실패 시).

## Patterns Covered
- **Single-agent first, multi-agent only when complexity demands** — 단일 agent loop 으로 시작, 복잡도가 강제할 때만 multi-agent 로 진화.
- **Manager pattern (agents as tools)**: 중앙 manager agent 가 specialized agent 들을 tool call 로 조율 (각자 특정 task/domain 담당).
- **Decentralized pattern (agents handing off to agents)**: peer agent 들이 specialization 기반으로 서로에게 task 를 handoff.
- **Layered guardrail**: relevance → safety → tool-risk → human escalation 단계 방어.

## Generation Mapping
- 본 family 의 **autopilot-* 라우터 + 서브에이전트(연구팀/품질관리팀/편집팀)** 구조 = OpenAI 의 **Manager pattern** (메인 Claude = manager, agent = tool). "서브에이전트 중첩 1단 한계"는 manager 가 평면적으로 tool 을 부리는 형태와 정합.
- **single-agent first** 원칙 = 본 family 의 "짧은 단발 → 직접 처리 / 추적 필요 + 산출물 누적 → autopilot" 분기와 동형.
- **Guardrail = layered defense** = `hooks/artifact-guard.sh`·`spec-skill-gate.sh`·`git-state-guard` 의 단계적 hard gate, claim-verify 모드의 adversarial 검증 층과 매핑.
- **Instructions: break tasks into discrete steps** = autopilot-spec → code → lab 의 단계 분해 파이프라인 철학과 일치.

## Quotable
- "systems that independently accomplish tasks on your behalf"
- "an agent loops through tool calls until exit conditions are met"
- (paraphrase) "Start with single-agent systems and evolve to multi-agent designs only when complexity demands it."

## Limitations / Caveats
- 2차 출처(maginative/websearch) 경유 — verbatim 인용 일부는 PDF 원문 직접 대조 안 됨. 정밀 인용 필요 시 PDF 직접 확인 요망.
- business/product 팀 대상 vendor 문서 — 학술적 엄밀성보다 실무 best-practice 지향. empirical 평가·ablation 없음.
- OpenAI 제품(Agents SDK 등) 맥락의 prescriptive 가이드 — 다른 stack 일반화 시 주의.
