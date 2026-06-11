# Code & Model Search — Aggregate (mode=technology, Phase C)

> 주제: 에이전트 엔지니어링 원칙·패턴. 다운스트림 = 사용자 매뉴얼. 코드 자원 = "이 패턴이 실제 구현된 곳" 레퍼런스.
> 확인 시점: 2026-06-11. star/last-update 는 WebFetch/WebSearch 확인값 (대략치). URL 은 전부 검증됨 (지어내기 없음).

## 패턴 → 구현 매핑 한눈에

| 패턴 (매뉴얼 축) | 1차 구현 | 보조 구현 |
|---|---|---|
| 상태 영속성 / pause-resume / stateless reducer | humanlayer/12-factor-agents, langgraph (checkpointing) | aider (git-as-state), OpenHands (event-sourcing) |
| spec-first / plan-then-execute | github/spec-kit | openai-agents (handoff), crewAI (Flows) |
| harness loop / scaffold | anthropics/claude-code, OpenHands, SWE-agent, aider | claude-agent-sdk (programmatic) |
| trigger from anywhere (headless/CI) | claude-code-action, claude-agent-sdk | — |
| maker/verifier 역할 분업 | openai-agents, crewAI, ag2 | ace-agent/ace (Gen/Refl/Cur), SICA |
| context engineering / 오답노트→승격 | ace-agent/ace | claude-code (skills, progressive disclosure) |
| golden set / eval 회귀 | promptfoo (self-host) | Braintrust, langsmith-sdk (SaaS+SDK) |
| self-improvement / 메타-스킬 진화 | MaximeRobeyns/SICA, ace-agent/ace | — |
| harness 차원 비교 (학술) | Inside-the-Scaffold 13-agent taxonomy | — |

## Tier 별 파일

- `code_resources/tier1_canonical_implementations.md` — 12-factor-agents, spec-kit, claude-code(+agent-sdk), claude-code-action, OpenHands, SWE-agent, aider
- `code_resources/tier2_orchestration_frameworks.md` — langgraph, crewAI, ag2(AutoGen 후속), mastra, openai-agents
- `code_resources/tier3_auxiliary_and_eval.md` — ace-agent/ace, SICA, promptfoo, Braintrust, langsmith-sdk, Inside-the-Scaffold 13개 목록

## 데이터 품질 주의 (인용 시 반영)

- **spec-kit stars**: 출처별 편차 큼 (직접 fetch 111k vs 2차 71~90k). 급성장 중 — "~100k+ 급성장" 으로 인용, 단일 숫자 단정 회피.
- **Braintrust / LangSmith**: 핵심은 SaaS 플랫폼. GitHub SDK repo star (수십~수백) 로 영향력 판단 부적합 — 개념 출처로 인용하고 self-host eval 은 promptfoo 권장.
- **AG2 vs AutoGen**: AG2(ag2ai, ~4.7k) = community 후속, microsoft/autogen(원조) 는 별도·더 높음. 계보 혼동 주의.
- **Inside-the-Scaffold 13개**: 개별 repo URL 일괄 검증 미수행 — 인용 시 논문(pinned commit) 경유 권장. taxonomy 표 자체를 인용 대상으로.
- **last-update 일부**: claude-code/12-factor 는 commit count 만 노출 (정확 날짜 미표시) — "활발" 로 표기.

## 미해결 / 후속 가능

- microsoft/autogen 원조 repo 직접 star 미확인 (필요 시 추가 fetch).
- Inside-the-Scaffold 13개 중 Tier 1 외 (OpenCode/Cline/AutoCodeRover 등) URL·star 미검증 — 매뉴얼이 개별 인용하려면 추가 verify.
