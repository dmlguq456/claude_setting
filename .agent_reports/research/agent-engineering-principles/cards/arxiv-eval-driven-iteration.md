---
title: "When Generic Prompt Improvements Hurt: Evaluation-Driven Iteration for LLM Applications"
authors: "Daniel Commey"
venue: arXiv
year_month: 2026-01
arxiv_id: 2601.22025
url: https://arxiv.org/abs/2601.22025
raw_type: paper
tier: 4
---

## Abstract Summary
- Minimum Viable Evaluation Suite(MVES): application type을 failure mode·metric에 연결해 LLM application을 평가하는 framework.
- local model(Llama 3 8B, Qwen 2.5 7B)로 extraction·RAG compliance·instruction-following에서 5개 prompt 변형을 30-case test suite로 검증.
- 핵심 발견: **generic prompt enhancement가 일관된 개선을 주지 않음** — Qwen 2.5 RAG에서 generic rule을 user prompt에 붙이자 26/30→9/30으로 최대 폭 하락.
- prompt 수정을 배포 전 테스트가 필요한 **잠재 위험**으로 취급하는 evaluation-driven iteration을 주창.

## Patterns Covered
- **golden set·eval**: 30-case test suite로 prompt 변경을 검증 — golden set 회귀 테스트와 동형.
- **오답노트 승격 (역설)**: generic 개선이 오히려 해칠 수 있음 — 변경마다 eval 게이트 필요.
- **eval-driven iteration**: 수정을 위험으로 보고 배포 전 측정.

## Relevance to Manual
매뉴얼의 golden loop(지침 수정 후 회귀 테스트)과 "변경을 eval로 검증" 원칙을 직접 받치는 근거. 특히 generic 개선이 성능을 해친 정량 사례는 매뉴얼/지침 수정 시 golden 미실행을 경계하는 강한 근거.
