---
title: "Evaluating Context Compression for AI Agents"
authors: Factory AI
venue: Factory AI News
year_month: 2025
url: https://factory.ai/news/evaluating-compression
raw_type: blog
tier: 2
---

## Core Claims

1. **최적화 대상은 request 당 token 이 아니라 task 당 token 이다.** "The right optimization target is not tokens per request. It is tokens per task." 공격적 압축은 re-fetching·re-exploration 으로 token 을 낭비해 초기 절감을 상쇄한다.
2. **압축 평가는 ROUGE 류 surface metric 이 아니라 probe-based 기능 평가여야 한다.** 압축 후 truncated history 의 구체 정보를 요구하는 질문을 던져 agent 가 계속 작업할 수 있는지 직접 측정.
3. **structured·anchored 접근이 silent information loss 를 막는다.** 명시적 section (intent·file modifications·decisions·next steps) 을 가진 구조적 요약이 generic summarization 보다 file path·기술 디테일 보존에 우수.

## Key Concepts & Definitions

- **Probe-based evaluation**: 압축 후 agent 에게 truncated history 의 세부를 묻는 질문으로 기능 품질 측정 (전통 metric 대체).
- **Six evaluation dimensions (0–5)**: Accuracy / Context Awareness / Artifact Trail / Completeness / Continuity / Instruction Following.
- **Anchored iterative summarization**: 매 cycle 마다 요약을 regenerate 하지 않고 기존 요약에 **merge** — 다중 압축 cycle 간 consistency 유지.
- **Tokens per task** (verbatim 핵심): request 단위가 아닌 task 완수 단위 token 비용을 최적화 목표로.

## Patterns Covered

- **컨텍스트 절약·compaction (평가)**: ✓ 본 글의 주제 — 압축 전략의 측정·비교 프레임워크.
- **golden set/eval·회귀 (인접)**: ✓ probe-based eval 은 압축 품질의 회귀 측정 수단으로, eval-driven 발상과 인접 (단 golden set/오답노트 승격 메커니즘은 미언급).
- **anchored summarization**: ✓ regenerate 대신 merge 하는 anchored iterative 방식이 redis-context-compaction 의 structured summarization 과 연결.
- 다루지 않음: maker-verifier, spec-first/plan-then-execute, 상태 파일 hierarchy(L1/L2), worktree, headless/cron.

## Generation Mapping

매뉴얼의 **컨텍스트 절약·compaction** 축을 *평가* 관점에서 보강하는 출처. Anthropic·Redis 가 compaction *방법*을 정의했다면, 이 글은 그 방법을 어떻게 *측정·비교*하는지를 vendor 벤치마크(Factory 3.70 vs OpenAI 3.35 vs Anthropic 3.44)로 제시한다. 핵심 메시지 "tokens per task" 는 매뉴얼이 compaction 의 trade-off(aggressive 압축의 re-fetch 비용)를 논할 때 인용 가능한 1차 근거. probe-based eval 은 eval-driven development 축과 compaction 축의 교차점 — "압축도 eval 로 검증한다"는 연결고리.

## Quotable

1. "The right optimization target is not tokens per request. It is tokens per task."
2. "All methods struggled with artifact trail preservation (2.19–2.45)." (압축 공통 약점 — 어떤 파일을 읽고 고쳤는지 추적이 미해결 과제)

## Limitations / Caveats

- vendor 자사 benchmark — Factory 가 최고점(3.70)을 받는 자기 평가라 selection bias 가능, 절대 점수보다 차원별 패턴(특히 artifact trail 공통 취약)에 주목.
- artifact trail preservation 은 모든 방법(2.19–2.45)이 약함 — 압축 일반의 미해결 한계.
- 99.3% 같은 극단 압축 ratio 는 functional quality 를 희생 — 높은 압축률 자체가 목표가 아님.
