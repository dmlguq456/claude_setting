---
title: "Agent = Model + Harness"
authors: Cobus Greyling
venue: Medium
year_month: 2026-06 (Jun 2, 2026)
url: https://cobusgreyling.medium.com/agent-model-harness-0d018f3d5014
raw_type: blog
tier: 2
role: 정리·대중화 (1차 논문 해설) — Harness-Bench arXiv 논문을 풀어 소개, 핵심 발견·반전 정리
---

## Core Claims (verbatim)

1. "Agent = Model + Harness" (논문 식 인용 — "the equation is the whole argument")
2. "agent capability should be reported at the model-harness configuration level rather than attributed to the base model alone."

## Key Concepts & Definitions

- **Agent = Model + Harness**: harness = context·tools·state·constraints·permissions·tracing·recovery 를 관리하는 system layer. capability 는 model 단독이 아니라 model-harness 조합 수준에서 보고돼야 함.
- **Harness-Bench (Qihoo360)**: 106 sandboxed tasks, 8 model backends, 6 harnesses, 5,194 trajectories. 8 카테고리(Software Engineering / Data·BI·Analytics / Long-running Autonomy / Research·Synthesis / Personal Productivity / Creative·Media / Operations·DevOps / Security·Compliance·Policy). harness swap 만으로 동일 task·동일 model pool 에서 **23.8 점** 이동. NanoBot 76.2 vs OpenClaw 52.4 (same tasks/pool, "the model was not the variable").
- **Execution alignment (논문 핵심 개념)**: harness 가 네 가지 correspondence 를 보존하는 정도 — (1) agent 가 reason 하는 것 (2) workspace 가 record 하는 것 (3) tool 이 실제 하는 것 (4) evaluator 가 check 하는 것. 유지되면 plausible reasoning → verified work. 깨지면 drift(tool feedback 무시·partial progress 소실·결과 계산되나 never committed).
- **실패는 추론이 아니라 번역**: failed trajectory 빈도순 — Contract/format violations 36.4%(malformed JSON·missing ledger row) / Tool error with no recovery 24.6% / Evidence not tied to claims 14.6% / Reasoning never committed as artefact 11.1%. "not a reasoning failure…a bookkeeping problem" — model 은 답을 알았으나 환경이 검사할 form 으로 적어두지 않음.

## Patterns Covered

- model-harness configuration 단위 평가/보고
- execution alignment (intention ↔ verifiable completion thread 보존)
- harness = translator / ledger = "memory that insists on being consulted"
- output contract / format 검증 (실패 1위 = contract violation)
- artefact 강제 commit (reasoning 을 file 로 render)
- minimal-loop 우월 (NanoBot 76.2 @ 7.3 turns < tokens vs Hermes 71.2 @ 22.6 turns 139.7K tokens)

## Generation Mapping

harness 세대의 **실증 정초**. rise-of-harness(개념) 의 짝 — 여기선 1차 벤치(Harness-Bench)로 "harness 가 변수다"를 측정으로 뒷받침. 단, **반전(inversion)** 으로 harness 만능론을 자기-제한: cross-harness variance 는 model 이 강해질수록 축소. "Weak models are hostages to their harness…Strong models shrug it off…The harness is not a fixed multiplier on intelligence. It is a crutch whose value decays as the model improves." → 세대 서사에 "harness 가치는 model 발전에 따라 감쇠" 라는 캐비엇 추가.

## Quotable

1. "The agent knew the answer. It just never wrote it down where it counts."
2. "The harness is not a thinker. It is the thing that keeps reasoning tethered to reality."
3. "The lesson is not 'add a harness.' It is 'a small loop that keeps its books beats a large one that loses them.'"

## Limitations / Caveats

- **출처 인용 관행**: 이 글은 Greyling 의 _1차 논문 해설(paraphrase)_ 포지션이 가장 뚜렷 — 거의 전부 **Harness-Bench arXiv 논문(Qihoo360)** 의 발견을 풀어 옮김. 수치·개념(execution alignment·23.8pt·실패 분류)은 논문 귀속, 해석/비유(translator·ledger·"crutch")는 Greyling 첨가. 명명 권위는 논문 저자, Greyling 은 대중화 해설자. 매뉴얼에서 "Agent=Model+Harness 식의 권위는 Harness-Bench, Greyling 은 해설" 로 구분.
- 핵심 수치(76.2/52.4/23.8/80.4 Codex/106·8·6·5194)는 Greyling 가 논문에서 옮긴 2차 인용 — fact-check 시 arXiv 원문·www.harness-bench.ai·github.com/Qihoo360/harness-bench 와 verbatim 대조 권장.
- "specialised stack" Codex 80.4 가 configurable harness 가 아니라 model-bound 라는 점 — 벤치 비교 공정성 caveat(configurable vs bound 혼재).
- inversion 결론("harness 가치 감쇠")은 논문 발견이되 미래 추정("model that is about to outgrow it") 부분은 Greyling 의 수사적 확장.
