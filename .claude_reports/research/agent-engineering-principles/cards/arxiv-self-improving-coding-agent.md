---
title: "A Self-Improving Coding Agent"
authors: "Maxime Robeyns, Martin Szummer, Laurence Aitchison"
venue: arXiv
year_month: 2025-04
arxiv_id: 2504.15228
url: https://arxiv.org/abs/2504.15228
raw_type: paper
tier: 4
---

## Abstract Summary
- LLM은 LLM call을 orchestrate하고 tool을 제공하는 agent system 안에서 배포되는데, 기본 coding tool을 갖춘 agent system이 **스스로를 편집해** 성능을 개선할 수 있음을 보임.
- SWE-bench Verified random subset에서 17%→53% 성능 향상, LiveCodeBench·synthetic agent benchmark에서도 추가 향상.
- gradient 없이 LLM reflection + code update로 구동되는 data-efficient learning mechanism.
- agentic system의 자동·open-ended 설계로 가는 진전을 대표.

## Patterns Covered
- **오답노트 승격 / self-improvement**: LLM reflection으로 자기 코드를 갱신 — 경험을 시스템 개선으로 승격.
- **maker-verifier**: benchmark 성능을 신호로 self-edit 루프를 돌림.
- **상태 영속성**: agent system 자체(코드·tool)가 영속 개선 대상.

## Relevance to Manual
매뉴얼의 오답노트 승격(post-it·golden loop으로 실패를 원칙·지침에 반영)과 self-improving 루프 철학을 받치는 근거. reflection-driven, non-gradient 개선이라는 점이 매뉴얼의 메타-스킬 진화와 부합.
