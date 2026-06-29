---
title: "Spec-Driven Development: From Code to Contract in the Age of AI Coding Assistants"
authors: "Deepak Babu Piskala"
venue: arXiv
year_month: 2026-01
arxiv_id: 2602.00180
url: https://arxiv.org/abs/2602.00180
raw_type: paper
tier: 4
---

## Abstract Summary
- AI coding assistant가 specification-driven development 개념을 부활시키고 있으며, 코드가 아니라 **specification을 1차 산물**로, 코드를 그로부터 생성·검증되는 2차 output으로 두는 접근을 탐구.
- 구현 methodology에 대한 실무 가이드 — spec 상세도 3 tier(spec-first, spec-anchored, spec-as-source)를 맥락별로 제시.
- BDD부터 GitHub Spec Kit 등 현대 AI-assisted platform까지 기존 도구·framework에서 spec-centric 원칙이 어떻게 구현되는지 분석.
- API 개발·대규모 enterprise·embedded 사례 + 팀이 이 접근의 이점을 평가할 framework로 마무리.

## Patterns Covered
- **spec-driven**: spec을 1차 산물, code를 2차 output으로 두는 방법론의 정면 정의 (3 tier 포함).
- **research → spec → code 파이프**: spec이 code의 전제라는 매뉴얼 하드 게이트와 동형.
- **상태 영속성 / 버전 트래킹**: spec을 versioned contract로 관리.

## Relevance to Manual
매뉴얼의 spec-first 파이프라인(autopilot-spec → autopilot-code)과 하드 순서 게이트의 학술적 토대. 특히 spec-first/anchored/as-source 3 tier는 매뉴얼의 spec 청사진 운영과 직접 매핑.
