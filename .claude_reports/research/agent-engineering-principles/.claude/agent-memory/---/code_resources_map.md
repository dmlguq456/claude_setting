---
name: agent-eng-code-resources-map
description: 에이전트 엔지니어링 매뉴얼용 코드 자원 — 패턴별 canonical 구현 repo 매핑 + 데이터 품질 caveat (2026-06-11 검증)
metadata:
  type: project
---

에이전트 엔지니어링 원칙 survey 의 Phase C (code & model search) 결과. 산출물: `code_resources/tier{1,2,3}_*.md` + `_internal/code_search.md`.

**패턴→repo 핵심 매핑** (전부 URL 검증됨):
- 상태 영속성/12-factor: humanlayer/12-factor-agents (~23k, TS)
- spec-first: github/spec-kit (~100k+ 급성장, Python)
- harness 구현: anthropics/claude-code (~132k), OpenHands (~76k), SWE-agent (~19.5k), aider (~46k)
- headless/CI: anthropics/claude-code-action (~7.9k), claude-agent-sdk-python (~7.3k, hook 제어)
- orchestration: langgraph (~34k, checkpointing), crewAI (~53k), ag2 (~4.7k, AutoGen 후속), mastra (~25k TS), openai-agents (~27k, handoff+guardrail)
- self-improvement: ace-agent/ace (~1.1k, arXiv 2510.04618 공식), MaximeRobeyns/SICA (~343, arXiv 2504.15228)
- eval/regression: promptfoo (~22k, self-host CLI 권장), Braintrust·langsmith (SaaS — 개념 출처)

**Why**: 다운스트림 매뉴얼이 "이 패턴 실제 구현된 곳" 으로 인용.
**How to apply**: 인용 시 caveat 준수 — spec-kit star 는 편차 커서 "~100k+ 급성장" 으로, Braintrust/LangSmith 는 SDK star 말고 플랫폼 가치로, AG2≠원조 AutoGen 계보 구분, Inside-the-Scaffold 13개는 taxonomy 표 인용 (개별 URL 미검증). 관련 [[agent_engineering_survey]].
