---
title: "Architecting Resilient LLM Agents: A Guide to Secure Plan-then-Execute Implementations"
authors: "Ron F. Del Rosario, Klaudia Krawiecka, Christian Schroeder de Witt"
venue: arXiv
year_month: 2025-09
arxiv_id: 2509.08646
url: https://arxiv.org/abs/2509.08646
raw_type: paper
tier: 4
---

## Abstract Summary
- strategic planning과 tactical execution을 분리하는 **Plan-then-Execute(P-t-E)** architectural pattern을 다루며, ReAct 같은 reactive pattern 대비 predictability·cost-efficiency·reasoning quality 우위를 분석.
- 보안 함의 중심 — indirect prompt injection에 대한 control-flow integrity 기반 resilience, Principle of Least Privilege·task-scoped tool access·sandboxed execution의 defense-in-depth.
- LangChain(LangGraph)·CrewAI·AutoGen 3개 framework의 P-t-E 구현 blueprint 제공 (stateful graph·declarative tool scoping·Docker sandbox).
- dynamic re-planning loop, DAG 기반 parallel execution, Human-in-the-Loop 검증 등 고급 패턴 논의.

## Patterns Covered
- **plan-then-execute**: planner-executor 분리 아키텍처의 정면 가이드 (ReAct 대비 우위).
- **maker-verifier / Human-in-the-Loop**: HITL 검증·dynamic re-planning loop.
- **worktree / 격리**: task-scoped tool access·sandboxed execution·least privilege (작업 격리 원칙).
- **서브에이전트 분업**: DAG 기반 parallel execution.

## Relevance to Manual
매뉴얼의 plan-then-execute(autopilot-code의 plan→execute), 작업 격리(worktree·least privilege), HITL 컨펌 게이트를 가장 폭넓게 받치는 근거. abstract만으로도 다수 패턴을 cover하는 핵심 보조 출처.
