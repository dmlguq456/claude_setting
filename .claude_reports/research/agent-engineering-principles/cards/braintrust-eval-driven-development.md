---
title: "What is eval-driven development"
authors: Braintrust
venue: Braintrust Articles
year_month: 2025
url: https://www.braintrust.dev/articles/eval-driven-development
raw_type: blog
tier: 2
---

## Core Claims

1. **eval 이 LLM 앱의 working specification 이다.** quality criteria 를 upfront 정의 → measurable eval 로 encode → eval score 로 변경의 개선 여부를 배포 전에 판정. 주관적 판단을 대체한다.
2. **eval 이 곧 "good" 의 정의라면, 그것을 최적화하는 것으로 충분하다.** "If your eval correctly captures what 'good' means, then optimizing against it is sufficient."
3. **모든 변경이 측정 가능한 실험이 된다.** "Every prompt tweak, model swap, and pipeline change becomes a measurable experiment with a clear outcome: score went up, or score went down."
4. **regression 은 production 이 아니라 development 에서 드러나야 한다.** "When every change runs through the same eval suite before shipping, regressions surface in development instead of in production."

## Key Concepts & Definitions

- **Eval-driven development (EDD)**: eval 을 release discipline·working spec 으로 삼아 변경의 개선 여부를 score 로 판정하는 개발 방식.
- **Golden Sets (Frozen Core)** (verbatim 개념): "Curated collections of approved input-output pairs form a regression baseline that remains stable for consistent measurement across changes." — 안정적 회귀 기준선.
- **Expanding Datasets (Growing set)**: production 이 드러내는 edge case·새 behavior 를 real-world example 로 계속 추가해 coverage 확장.
- **Failure-driven evolution**: production 실패를 correct reference output 과 함께 golden dataset 에 추가 — incident 를 "permanent regression guards" 로 전환.
- **Three-phase loop**: Define evals(business req → measurable criteria) → Optimize(변경을 eval suite 로 검증) → Refine evals(req 진화에 맞춰 갱신).

## Patterns Covered

- **golden set/eval 회귀**: ✓ 본 글의 핵심 — frozen core(golden set) + growing set 이중 구조.
- **오답노트 → 케이스 승격**: ✓ 명시적. production failure 를 correct reference 와 함께 golden dataset 에 추가해 영구 회귀 가드화 ("failure-driven evolution").
- **maker-verifier (인접)**: ✓ eval 이 verifier 역할 — 단 본 글은 verifier-as-separate-agent 가 아니라 eval suite 로서의 검증.
- 다루지 않음: compaction/memory hierarchy, spec-first/plan-then-execute(코드 spec 의미), worktree, headless/cron, sub-agent 분업.

## Generation Mapping

매뉴얼의 **golden set/eval 회귀 + 오답노트→케이스 승격** 축을 정의하는 1차 출처. "frozen core vs growing set" 의 이분법을 명확히 제시해, 매뉴얼이 *고정 회귀 baseline* 과 *진화하는 case 집합* 을 구분하는 근거가 된다. "If your eval captures what good means, optimizing against it is sufficient" 는 eval-as-spec 철학의 핵심 인용. failure→golden 승격 메커니즘은 매뉴얼의 "오답노트→케이스 승격" 패턴을 verbatim 으로 뒷받침하며, redhat-eval-driven 의 "known bad set" 과 짝을 이룬다 (vendor-agnostic 진술 + vendor 구현).

## Quotable

1. "If your eval correctly captures what 'good' means, then optimizing against it is sufficient."
2. "Every prompt tweak, model swap, and pipeline change becomes a measurable experiment with a clear outcome: score went up, or score went down."
3. "When every change runs through the same eval suite before shipping, regressions surface in development instead of in production."

## Limitations / Caveats

- eval 이 "good" 을 *부정확*하게 포착하면 그것을 최적화하는 것은 잘못된 방향으로 최적화하는 것 — eval 설계 자체의 품질이 전제 (Goodhart 위험).
- vendor(Braintrust) 자사 플랫폼 맥락 — 일반 원칙은 도구 독립적이나 운영 디테일은 플랫폼 종속.
- golden set 의 큐레이션·라벨링 비용은 본 글에서 깊이 다루지 않음.
