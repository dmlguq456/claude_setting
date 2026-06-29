---
title: "Demystifying evals for AI agents"
authors: [Mikaela Grace, Jeremy Hadfield, Rodrigo Olivares, Jiri De Jonghe]
venue: Anthropic Engineering blog
year-month: 2026-01
url: https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
raw_type: technology blog
tier: 1
---

## Core Claims
> "The capabilities that make agents useful also make them difficult to evaluate."

> "Evals make problems and behavioral changes visible before they affect users, and their value compounds over the lifecycle of an agent."

## Key Concepts & Definitions
- **Eval anatomy**: Task (단일 입력+success criteria) / Trial (한 시도, non-determinism 대응 위해 다수 trial) / Grader (code-based·model-based·human) / Transcript (tool call·reasoning 전체 기록) / Outcome (최종 environment state) / Evaluation harness (eval 실행 인프라) vs Agent harness/scaffold (모델을 agent 로 동작시키는 scaffold).
- **Good task 기준**: "passable by an agent that follows instructions correctly", 두 domain expert 가 독립적으로 같은 pass/fail verdict 에 도달, 양방향 균형 (behavior 가 일어나야/일어나지 말아야 할 케이스 모두).
- **Grader 3종**: code-based (string match·binary·static analysis — fast·objective·brittle) / model-based (rubric·NL assertion·pairwise — flexible·non-deterministic·expensive) / human (SME·crowdsource·A/B — gold standard·slow).
- **Eval saturation**: 100% pass rate 도달 시 더 어려운 task 로 refresh 필요.
- **Eval-driven development**: capability 가 존재하기 전에 eval 을 먼저 정의.

## Patterns Covered
- **Failure→case 승격 (오답노트 핵심 근거)**: "Start with manual checks already performed pre-release", bug tracker·support queue 를 task 소스로 활용, user impact 로 우선순위. 실제 failure 에서 시작해 20-50 simple task 로 출발.
- **Regression 측정**: trial 비율로 success rate 측정 ("what proportion of trials an agent succeeds") — pass@k 사고.
- Partial credit (multi-component task) / transcript 정기 리뷰로 grader 공정성 검증.
- 전담 팀이 인프라 소유, domain expert 가 task 기여하는 분업.

## Generation Mapping
- **Loop Eng / eval-driven 회귀**: golden set + failure→case 승격 + regression 측정의 1차 근거. 매뉴얼 1부 '오답노트→케이스 승격' 주장의 canonical 출처.
- frozen core vs growing set (Braintrust EDD) 의 Anthropic 측 뒷받침.

## Quotable
> "When a task that passed on one eval run fails on the next, we want to measure how often—what proportion of trials—an agent succeeds."

> "The people closest to product requirements and users are best positioned to define success."

## Limitations
- Frontier 모델이 의도 안 된 loophole 발견 시 (Opus 4.5 policy loophole) "fail" 로 찍히지만 실제론 더 잘 푸는 역설.
- Broken task 는 agent 무능이 아니라 0% pass@100·spec ambiguity 신호일 때가 많음.
- LLM grader 는 빈번한 calibration 필요, subjective task 는 hallucination 취약.
- Eval 유지보수 부담이 시간에 따라 증가 — framework 가 high-quality test case 를 대체 못 함.
