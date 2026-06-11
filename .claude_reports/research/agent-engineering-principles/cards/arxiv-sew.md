---
title: "SEW: Self-Evolving Agentic Workflows for Automated Code Generation"
authors: "Siwei Liu, Jinyuan Fang, Han Zhou et al."
venue: arXiv
year_month: 2025-05
arxiv_id: 2505.18646
url: https://arxiv.org/abs/2505.18646
raw_type: paper
tier: 4
---

## Abstract Summary
- 복잡한 coding task를 sub-task로 분해해 specialized agent에 배정하는 multi-agent agentic workflow가 효과적이나, 기존 방식은 agent topology·prompt를 수작업 설계해 적응성이 제한됨.
- SEW(Self-Evolving Workflow): multi-agent workflow를 **자동 생성·최적화**하는 self-evolving framework.
- LiveCodeBench 포함 3개 coding benchmark에서 backbone LLM 단독 대비 최대 12% 향상.
- workflow의 다양한 representation scheme을 조사해 workflow 정보를 text로 인코딩하는 최적 방식에 대한 insight 제공.

## Patterns Covered
- **서브에이전트 분업**: complex task를 sub-task로 분해해 specialized agent에 배정 — 분업 워크플로우의 정면 연구.
- **오답노트 승격 / self-evolution**: workflow를 self-evolution으로 자동 최적화.
- **plan-then-execute**: agent topology(워크플로우 구조)를 먼저 설계 후 실행하는 구조.

## Relevance to Manual
매뉴얼의 서브에이전트 분업(연구팀·품질관리팀·편집팀)과 워크플로우 진화 패턴을 받치는 근거. 수작업 토폴로지 한계를 self-evolution으로 푼다는 점에서 메타-스킬 개선과 연결.
