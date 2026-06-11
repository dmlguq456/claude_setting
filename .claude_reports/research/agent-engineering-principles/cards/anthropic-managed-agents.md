---
title: "Scaling Managed Agents: Decoupling the brain from the hands"
authors: Anthropic Engineering
venue: Anthropic Engineering Blog
year-month: 2025
url: https://www.anthropic.com/engineering/managed-agents
raw_type: engineering blog (technology)
tier: 1
---

## Core Claims
1. Managed Agents 서비스는 Claude 의 inference("brain")를 execution environment("hands")·persistent state("session")로부터 **decouple** 해, 미래 모델 개선·harness 진화를 수용하는 stable interface 를 만든다 — 가정이 stale 해지는 걸 방지.
2. **Virtualization 패턴**: session·harness·sandbox 3개 component 를 각각 interface 로 접근시켜 독립 failure·replacement 가능.
3. harness 가 sandbox 를 generic tool 로 호출 (`execute(name, input) → string`), container 는 replaceable, `provision({resources})` 로 필요할 때만 초기화 → stateless scaling.
4. **session 은 Claude 의 context window 가 아니다** — append-only event log 가 context window 밖에 durable 하게 존재, `getEvents()` 로 positional slice 질의.
5. container provisioning 지연으로 p50 TTFT 약 60%, p95 90%+ 개선.

## Key Concepts & Definitions
- **Managed Agents**: 특정 구현 detail 을 outlast 하도록 설계된 stable interface 로 long-horizon agent 작업을 돌리는 hosted service.
- **Brain vs Hands**: "brain" = Claude + harness (decision-making); "hands" = sandbox + tool (action 수행); "session" = append-only event log.
- **harness 가 container 를 떠난다**: tool-call interface 로 harness 가 container 밖에 위치.
- **session = external context object**: context window 밖에 사는 context object 로 동일 benefit 제공.

## Patterns Covered
- **harness decoupling**: "harness leaves the container" — tool-call interface 로 분리.
- **상태 파일·영속성**: session log 가 durable event history 를 context window 밖에 저장.
- **컨텍스트 절약·compaction**: `getEvents()` 로 event stream 의 positional slice 만 질의 (전체 로드 회피).
- **orchestrator-worker (brain-hands)**: stateless brain 다수 + execution hand 다수가 독립 동작.
- **격리·보안**: credential 은 resource 에 bundle 되거나 vault 보관, Claude 생성 코드가 token 을 직접 다루지 않음.
- (미포함) golden set·eval·worktree·오답노트 — 본 글은 infra/interface 층에 집중.

## Generation Mapping
- **harness engineering → 인프라 일반화** 의 근거 — harness 정의(brain=Claude+harness)를 명시적으로 component 화. 사용자 매뉴얼 "상태 파일·영속성 / 컨텍스트 절약" 의 infra-level 출처.
- **context engineering**: session=context window 밖 외부 객체, `getEvents()` slice 가 compaction 의 인프라적 형태.
- **orchestrator-worker** 의 인프라 근거 (brain↔hands 분리, multiple brains/hands).
- 등장 배경: 모든 component 를 단일 container 에 coupling 했더니 container 실패=세션 전체 상실, 디버깅 불투명, VPC 통합 불가("Don't adopt a pet" 섹션)였던 문제를 virtualization 으로 푼 회고. "원칙의 세대사" 에서 harness 가 인프라 interface 로 굳는 단계의 증거.

## Quotable
1. "Decoupling the brain from the hands meant the harness no longer lived inside the container." (Decouple the brain from the hands 섹션) — harness 분리의 핵심.
2. "the session provides this same benefit, serving as a context object that lives outside Claude's context window" (The session is not Claude's context window 섹션) — session=외부 context object.
3. "we aimed to design a system that accommodates future harnesses, sandboxes, or other components around Claude" (Conclusion 섹션) — 미래 수용 stable interface 목표.

## Limitations / Caveats
- multiple brain 이 execution environment 간 reasoning 을 조율해야 함 — "a harder cognitive task than operating in a single shell".
- many-hands 시나리오 처리가 Claude 의 향상된 intelligence 에 의존 (이전 모델은 불가).
- context management 접근이 model-dependent — session interface 는 의도적으로 특정 engineering 전략을 prescribe 안 함.
