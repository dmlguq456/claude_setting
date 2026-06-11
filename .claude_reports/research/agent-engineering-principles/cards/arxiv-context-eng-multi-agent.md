---
title: "Context Engineering for Multi-Agent LLM Code Assistants Using Elicit, NotebookLM, ChatGPT, and Claude Code"
authors: "Muhammad Haseeb"
venue: arXiv
year_month: 2025-08
arxiv_id: 2508.08322
url: https://arxiv.org/abs/2508.08322
raw_type: paper
tier: 4
---

## Abstract Summary
- LLM이 code generation·SWE에 유망하나 context 한계·knowledge gap으로 복잡한 multi-file project에서 자주 실패.
- Intent Translator, Elicit 기반 semantic literature retrieval, NotebookLM 문서 합성, Claude Code multi-agent system(생성·검증)을 결합한 통합 workflow 제안.
- single-agent baseline 대비 real-world repository에서 accuracy·reliability 향상.
- Next.js codebase 정성 분석, CodePlan·MASAI·HyperAgent 등과 비교, 배포 함의·향후 연구 논의.

## Patterns Covered
- **서브에이전트 분업 / maker-verifier**: Claude Code multi-agent로 code generation과 validation 분리.
- **컨텍스트 절약 / spec-driven**: Intent Translator·document synthesis로 task에 맞는 context를 선별 주입 (context engineering 정면).
- **research → spec → code 파이프**: literature retrieval → 문서 합성 → 코드 생성 순서.

## Relevance to Manual
매뉴얼의 research→spec→code 하드 순서 게이트, maker-verifier(생성·검증 분리), Claude Code 기반 multi-agent 분업을 가장 직접적으로 받치는 실무 근거. 단 single-author·정성 분석 위주라 tier 4 보조로만.
