---
title: "Eval-driven development: Build and evaluate reliable AI agents"
authors: Red Hat Developer
venue: Red Hat Developer
year_month: 2026-03
url: https://developers.redhat.com/articles/2026/03/23/eval-driven-development-build-evaluate-ai-agents
raw_type: blog
tier: 3
---

## Core Claims

1. **agent 검증은 exact-match 가 불가능하다.** "It's not as simple as checking that the agent said exactly, 'Yes, you are eligible'—the agent might communicate that in any number of different ways." — 같은 개념을 여러 방식으로 표현하므로 flexible rubric 이 필요.
2. **single big prompt 가 작동하는 듯 보인 건 overfit 이었다.** "We initially believed a smaller model would work with a single 'big' prompt, but automated evaluations revealed this only appeared to work because we had overfit the prompt to our limited manual tests." — 자동 eval 이 manual test 의 overfit 을 폭로.
3. **intermittent failure 는 다회·장기 실행으로만 잡힌다.** "You need to do a larger number of runs, over a larger time period to catch subtle and intermittent failures."

## Key Concepts & Definitions

- **Eval-driven development (EDD)**: evaluation framework 가 iterative 개발을 이끄는 체계적 접근 (model variability 에도 business req 충족 보장).
- **Develop–Evaluate loop**: 기능 구축 → predefined+generated conversation 에 자동 eval → 실패 식별 → prompt/metric 조정 → 재검증.
- **8-stage framework**: (1) manual testing → (2) basic 자동 eval → (3) use-case-specific metric → (4) multi-type coverage(predefined + generated + known bad) → (5) CI/CD 통합 → (6) cost-awareness → (7) OpenTelemetry context → (8) continuous monitoring.
- **"Known bad" set**: agent 가 특정 실수를 한 실패 conversation 모음 — eval metric 이 실제로 의도한 실패를 잡는지 검증 (false negative 방지).
- **Judge calibration**: "The more capable the model, the more accurate your evaluations will be." frontier model(llama-3-3-70b)은 모든 실패를 잡았고, 작은 model 은 known-bad 4–5건을 놓침.
- **CI gate**: GitHub CI 로 PR review + nightly 20+ generated conversation 실행으로 subtle·intermittent 실패 포착.

## Patterns Covered

- **golden set/eval 회귀**: ✓ 본 글의 핵심 — "golden dataset drawn from real failures" + CI gate 가 regression 차단.
- **오답노트 → 케이스 승격**: ✓ "known bad" conversation set 이 곧 실패 케이스의 영구 회귀 가드.
- **maker-verifier (인접)**: ✓ DeepEval "LLM as a judge" — model 이 verifier, judge calibration 강조.
- **headless/cron (인접)**: ✓ nightly run + CI 통합으로 자동 회귀 실행.
- 다루지 않음: compaction/memory hierarchy, spec-first/plan-then-execute, worktree, sub-agent 분업.

## Generation Mapping

매뉴얼의 **golden set/eval + 오답노트→케이스 승격** 축의 *vendor 구현 사례* 출처 — braintrust-eval-driven 의 원칙적 진술에 대한 구체 case study. "known bad set" 은 braintrust 의 "failure-driven evolution" 을 실무로 구현한 것으로, 둘을 짝지으면 (원칙 + 구현)의 강한 근거 쌍이 된다. 특히 **judge calibration**(model 능력 ↔ eval 정확도)과 **single-big-prompt overfit 폭로**는 매뉴얼이 *왜* manual test 만으로 부족하고 자동 eval·다회 실행이 필요한지를 verbatim 으로 뒷받침. CI gate·nightly run 은 headless/cron 축과도 인접.

## Quotable

1. "It's not as simple as checking that the agent said exactly, 'Yes, you are eligible'—the agent might communicate that in any number of different ways."
2. "We initially believed a smaller model would work with a single 'big' prompt, but automated evaluations revealed this only appeared to work because we had overfit the prompt to our limited manual tests."
3. "You need to do a larger number of runs, over a larger time period to catch subtle and intermittent failures."

## Limitations / Caveats

- tier 3 (medium skim) — 원 URL(slug 의 .../eval-driven-development)은 404, WebSearch 로 정정 URL 확보 후 fetch.
- judge 로 쓰는 model 능력에 eval 정확도가 종속 — 작은 model judge 는 실패를 놓침 (비용 vs 정확도 trade-off).
- Red Hat OpenShift AI·DeepEval·Llama Stack 특정 스택 맥락 — 도구 디테일은 환경 종속.
