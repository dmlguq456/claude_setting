---
title: "Quantifying infrastructure noise in agentic coding evals"
authors: [Gian Segato]
venue: Anthropic Engineering blog
year-month: 2026-02
url: https://www.anthropic.com/engineering/infrastructure-noise
raw_type: technology blog
tier: 1
---

## Core Claims
> "Two agents with different resource budgets and time limits aren't taking the same test."

> "A few-point lead might signal a real capability gap—or it might just be a bigger VM."

## Key Concepts & Definitions
- **Infrastructure noise**: 하드웨어·runtime enforcement·시스템 조건에서 오는 confounding variable 로, benchmark score 를 인위적으로 부풀리거나 깎음.
- **Agentic coding eval**: 모델이 full runtime environment 와 상호작용하는 end-to-end 평가 — 인프라 자체가 problem-solving 의 일부.
- **Enforcement methodology**: container runtime 의 resource limit 적용 방식 (guaranteed allocation vs hard kill threshold)이 task success rate 에 크게 영향. Terminal-Bench 2.0 에서 strict↔uncapped 사이 6%p swing.

## Patterns Covered
- Guaranteed allocation 과 hard kill threshold 를 따로 명시 (동일 값으로 pin 하지 말 것).
- Resource spec 의 약 3x headroom 으로 calibrate — infrastructure confounder 중화하되 의미 있는 resource pressure 유지.
- Benchmark score 와 함께 정확한 enforcement methodology·resource config 보고.
- 여러 시각·여러 날에 걸쳐 실행해 temporal noise 평균화.

## Generation Mapping
- **Loop Eng / eval 회귀 신뢰성**: regression 측정이 신뢰 가능하려면 noise floor 를 정량화·통제해야 한다는 근거. "flaky 한 eval 결과를 회귀로 오인하지 말라"의 1차 출처. 매뉴얼 1부 golden set 회귀의 신뢰성 단서.

## Quotable
> "Infrastructure configuration alone can produce differences that exceed those margins [separating top leaderboard performers]."

> "Tight limits inadvertently reward very efficient strategies, while generous limits reward agents exploiting resources."

## Limitations
- 주로 Claude 모델로 테스트 — 타 모델 주장은 anecdotal.
- SWE-bench 분석은 Terminal-Bench 결과보다 덜 rigorous.
- Time-of-day variance 관찰됐으나 formal 정량화 안 됨.
- 전용 하드웨어 없는 외부 evaluator 의 reproducibility 제약 인정.
