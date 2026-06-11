---
title: "Harness-Bench: Measuring Harness Effects across Models in Realistic Agent Workflows"
authors: "Yilun Yao, Xinyu Tan, Chao-Hsuan Liu et al."
venue: arXiv
year_month: 2026-05
arxiv_id: 2605.27922
url: https://arxiv.org/abs/2605.27922
raw_type: paper
tier: 4
---

## Abstract Summary
- LLM agent의 성능은 base model 뿐 아니라 **harness**(context·tools·state·constraints·permissions·tracing·recovery를 관리하는 system layer)에 좌우된다고 주장.
- 실무 agent 사용 패턴에서 도출한 106개 sandboxed offline task로 여러 model backend × harness configuration을 평가하는 diagnostic benchmark 제시.
- 5,194개 execution trajectory 분석 결과 model-harness pairing마다 성능 편차가 커서, agent capability는 base model 단독이 아니라 **model-harness configuration 수준**에서 평가해야 한다고 결론.
- reasoning이 tool feedback·workspace state와 decouple되는 execution-alignment failure를 식별, 재현 가능한 framework 제공.

## Patterns Covered
- **상태 영속성**: harness가 state·workspace를 관리하는 system layer로 정의되며, reasoning-state decoupling이 주요 실패 원인.
- **maker-verifier / 컨텍스트 절약**: harness가 context·tracing·recovery를 담당, execution-alignment 추적이 핵심.
- **headless**: 106개 sandboxed offline task 기반 실행 평가 — agent를 자동 실행 환경에서 측정.

## Relevance to Manual
매뉴얼의 "harness(skill·hook·convention 등 system layer)가 모델만큼 결과를 좌우한다"는 핵심 전제에 직접 대응하는 학술 근거. 단, abstract-only이며 tier 4 보조 근거로만 사용.
