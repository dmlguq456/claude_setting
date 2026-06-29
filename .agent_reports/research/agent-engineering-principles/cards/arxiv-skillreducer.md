---
title: "SkillReducer: Optimizing LLM Agent Skills for Token Efficiency"
authors: "Yudong Gao, Zongjie Li, Yuanyuanyuan et al."
venue: arXiv
year_month: 2026-03
arxiv_id: 2603.29919
url: https://arxiv.org/abs/2603.29919
raw_type: paper
tier: 4
---

## Abstract Summary
- coding agent의 skill(pre-packaged instruction set)이 context window에 주입되는 모든 token이 비용·attention dilution을 일으킨다는 문제.
- 55,315개 공개 skill 실증 조사: 26.4%가 routing description 없음, body의 60%+가 non-actionable, reference file이 invocation당 수만 token 주입.
- SkillReducer는 2-stage 최적화 — Stage 1은 routing layer(verbose description 압축·adversarial delta debugging으로 누락 생성), Stage 2는 skill body 재구조화(taxonomy 분류 + progressive disclosure로 actionable core와 supplementary 분리, faithfulness check·self-correcting loop).
- 48% description / 39% body 압축에 functional quality 2.8% 향상 — non-essential 제거가 distraction을 줄이는 **less-is-more** 효과. 5개 model에서 retention 0.965.

## Patterns Covered
- **컨텍스트 절약 / progressive disclosure**: actionable core와 on-demand supplementary 분리가 framework 핵심.
- **서브에이전트 분업 (skill 라우팅)**: routing description 최적화 — skill을 description으로 라우팅하는 구조.
- **maker-verifier**: faithfulness check + self-correcting feedback loop로 압축 검증.

## Relevance to Manual
매뉴얼의 skill 카탈로그·description 라우팅, progressive disclosure(SKILL.md 얇게 + on-demand Read) 패턴을 거의 1:1로 받치는 근거. less-is-more 효과는 컨텍스트 절약 원칙의 정량 지지.
