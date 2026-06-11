---
title: "PAACE: A Plan-Aware Automated Agent Context Engineering Framework"
authors: "Kamer Ali Yuksel"
venue: arXiv
year_month: 2025-12
arxiv_id: 2512.16970
url: https://arxiv.org/abs/2512.16970
raw_type: paper
tier: 4
---

## Abstract Summary
- multi-step workflow를 다루는 LLM agent는 context가 계속 팽창해 curation·compression이 필요하다는 문제를 다룸.
- PAACE는 next-k-task relevance modeling, plan-structure analysis, instruction co-refinement, function-preserving compression으로 agent state를 최적화하는 framework.
- 두 component: PAACE-Syn(compression supervision이 붙은 synthetic agent workflow 생성), PAACE-FT(teacher demonstration으로 학습한 distilled compressor).
- distilled model이 97% 성능을 유지하면서 inference cost를 크게 낮춰, accuracy 향상과 context load 감소를 동시 달성.

## Patterns Covered
- **컨텍스트 절약**: context curation·compression이 framework의 핵심 목표 (function-preserving compression).
- **plan-then-execute**: plan-structure analysis와 next-k-task relevance modeling으로 plan을 인지한 context 관리.
- **상태 영속성**: agent state 최적화를 명시적 대상으로 삼음.

## Relevance to Manual
매뉴얼의 컨텍스트 절약(post-it·progressive disclosure)과 plan-aware 상태 관리 패턴을 받치는 근거. plan 구조를 인지한 압축이라는 점에서 plan-then-execute와도 연결.
