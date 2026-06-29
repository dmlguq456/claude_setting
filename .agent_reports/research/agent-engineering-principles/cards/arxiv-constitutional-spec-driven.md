---
title: "Constitutional Spec-Driven Development: Enforcing Security by Construction in AI-Assisted Code Generation"
authors: "Srinivas Rao Marri"
venue: arXiv
year_month: 2026-01
arxiv_id: 2602.02584
url: https://arxiv.org/abs/2602.02584
raw_type: paper
tier: 4
---

## Abstract Summary
- AI-assisted 'vibe coding'이 빠른 개발을 가능케 하나 LLM이 보안보다 functional correctness를 우선해 보안 위험을 키움.
- Constitutional Spec-Driven Development: **비협상 보안 원칙을 spec layer에 박아** AI 생성 코드가 inspection이 아닌 construction으로 보안 요구를 충족하게 함.
- Constitution = CWE/MITRE Top 25·규제 framework에서 도출한 보안 제약을 인코딩한 versioned·machine-readable 문서.
- banking microservice 사례에서 10개 critical CWE를 constitutional constraint로 처리, 원칙→코드 위치 full traceability. 무제약 생성 대비 보안 defect 73% 감소(velocity 유지) — proactive spec이 reactive verification보다 우수.

## Patterns Covered
- **spec-driven / constitution(원칙 문서)**: 비협상 원칙을 versioned machine-readable spec에 박는 구조 — 매뉴얼의 CLAUDE.md/CONVENTIONS 원칙 문서와 동형.
- **hook 강제 / by-construction**: inspection이 아닌 construction으로 제약 enforce (proactive > reactive).
- **버전 트래킹 / traceability**: 원칙→코드 full traceability, versioned constitution.

## Relevance to Manual
매뉴얼의 원칙 문서(CLAUDE.md·CONVENTIONS) 단일 출처 + hook 기반 by-construction 강제 철학을 직접 받치는 근거. "proactive 원칙이 reactive 검증보다 낫다"는 결론이 매뉴얼의 게이트 우선 설계를 지지.
