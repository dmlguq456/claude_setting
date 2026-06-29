---
title: "Auditing Agent Harness Safety"
authors: "Chengzhi Liu, Yichen Guo, Yepeng Liu et al."
venue: arXiv
year_month: 2026-05
arxiv_id: 2605.14271
url: https://arxiv.org/abs/2605.14271
raw_type: paper
tier: 4
---

## Abstract Summary
- LLM agent가 tool·resource·inter-component 통신을 관리하는 execution harness 안에서 동작하는데, harness가 올바른 output을 내면서도 unauthorized resource 접근·민감 정보 오전달을 할 수 있다는 문제 — output-level 평가로는 안 보이는 mid-trajectory violation.
- harness가 user intent 유지·permission boundary 준수·information-flow constraint를 실행 전체에서 지키는지를 검증.
- HarnessAudit: 전체 execution trajectory를 boundary compliance·execution fidelity·system stability 측면(특히 multi-agent)에서 감사하는 framework. HarnessAudit-Bench는 8개 domain 210 task(single/multi-agent, 내장 safety constraint).
- 10개 harness 분석: task completion과 safe execution이 괴리되고, violation이 trajectory 길이에 따라 누적되며, resource access·inter-agent 정보 전달에 violation이 집중.

## Patterns Covered
- **maker-verifier / hook 강제**: trajectory 전체를 감사해 boundary·permission violation 탐지 — output이 아닌 과정 검증.
- **서브에이전트 분업**: multi-agent 구성에서 inter-agent 정보 전달이 주요 violation 지점 — 분업 시 정보 경계 관리 필요성.
- **상태 영속성 / 권한 경계**: permission boundary·information-flow constraint를 실행 전반에서 enforce.

## Relevance to Manual
매뉴얼의 hook 기반 강제(artifact-guard·git-state-guard)와 서브에이전트 정보 경계 관리를 받치는 근거. violation이 trajectory 길이에 누적된다는 발견은 단계 게이트·중간 검증 원칙을 지지.
