---
title: "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?"
authors: "Thibaud Gloaguen, Niels Mündler, Mark Müller et al."
venue: arXiv
year_month: 2026-02
arxiv_id: 2602.11988
url: https://arxiv.org/abs/2602.11988
raw_type: paper
tier: 4
---

## Abstract Summary
- AGENTS.md 같은 repository-level context file로 coding agent를 맞추는 관행이 실제로 효과 있는지를 rigorous하게 검증.
- SWE-bench task(LLM 생성 context file)와 developer-committed context file 보유 repo의 신규 issue 두 setting에서 task completion 평가.
- 여러 agent·LLM에서 context file이 오히려 task success rate를 **낮추고** inference cost를 20%+ 증가시킴.
- LLM 생성/개발자 작성 모두 broader exploration(과한 testing·file traversal)을 유발 — 불필요한 requirement가 task를 어렵게 만듦. 결론: human-written context file은 **minimal requirement만** 기술해야.

## Patterns Covered
- **컨텍스트 절약 / less-is-more**: 과도한 context file이 성능을 해치며 minimal requirement만 남기라는 직접 근거.
- **AGENTS.md / 매뉴얼 자체**: repository-level instruction file의 효과를 정면으로 측정한 드문 연구 (counter-evidence 포함).

## Relevance to Manual
매뉴얼이 곧 AGENTS.md/CLAUDE.md류 context file이라는 점에서 가장 직접적인 경고성 근거 — "얇은 부트스트랩·minimal requirement" 원칙(과적재 회피)을 학술적으로 지지. tier 4지만 반례 데이터를 담아 비판적 인용 가치 높음.
