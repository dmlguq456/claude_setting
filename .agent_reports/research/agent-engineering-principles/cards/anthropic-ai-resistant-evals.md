---
title: "Designing AI-resistant technical evaluations"
authors: [Tristan Hume]
venue: Anthropic Engineering blog
year-month: 2026-01
url: https://www.anthropic.com/engineering/AI-resistant-technical-evaluations
raw_type: technology blog
tier: 1
---

## Core Claims
> "A take-home that distinguishes well between human skill levels today may be trivially solved by models tomorrow—rendering it useless for evaluation."

> "Realism may be a luxury we no longer have. The original worked because it resembled real work. The replacement works because it simulates novel work."

## Key Concepts & Definitions
- **AI-resistant evaluation**: 모델 능력이 향상돼도 human skill 변별 신호를 유지하도록 설계된 평가.
- **Contamination/gaming risk**: 모델이 candidate reasoning 이 아니라 방대한 training data 기반으로 문제를 풂.
- **Robustness factors**: (1) out-of-distribution 문제 novelty, (2) constrained/unusual instruction set, (3) pattern matching 이 아닌 first-principles reasoning 요구, (4) tool-building judgment 요구.
- 사례: 연속된 Claude 버전(Opus 4 → 4.5)이 time-limited 조건에서 performance engineering take-home 을 차례로 격파 → eval 수명 한계 입증.

## Patterns Covered
- Time-limited 문제는 skill 시연이 아니라 delegation 을 favor 하게 변질됨.
- Real-world inspired task 는 training data 확장에 따라 취약해짐.
- 고도로 constrained 된 game-like puzzle (Zachtronics 스타일)이 더 큰 저항성.
- Debugging tooling 을 평가 일부로 빌드시키면 signal 추가.
- 흔한 optimization domain (data transposition) 제거 시 모델 advantage 감소.

## Generation Mapping
- **Loop Eng / eval 설계 견고성**: golden set 이 시간이 지나도 변별력을 유지하려면 saturation·contamination 에 저항하는 설계가 필요하다는 근거. eval regression 의 '왜 set 을 갱신·강화해야 하나'의 보강.

## Quotable
> "Engineers across many platforms have struggled with data transposition and bank conflicts, so Claude has substantial training data to draw on."

> "The replacement works because it simulates novel work."

## Limitations
- 단일 조직 경험 — generalizability 불명.
- 새 evaluation 이 production candidate 상대로 대규모 미검증.
- Trade-off 인정: novel 문제가 실제 job work 를 대표 못 할 수 있음.
- novel-problem 저항성이 모델 향상에 따라 얼마나 지속되는지 논의 제한적.
