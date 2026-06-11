---
name: agent-engineering-survey
description: 에이전트 엔지니어링 원칙·패턴 종합 조사 (2025-2026) 핵심 출처 — 세대사(prompt→context→harness→loop) + 실무 패턴, 매뉴얼 1부 근거
metadata:
  type: project
---

에이전트 엔지니어링 원칙·패턴 종합 조사 (technology mode, 사용자 매뉴얼 '원칙의 세대사' 근거). 산출물: `.claude_reports/research/agent-engineering-principles/`.

**Why:** 사용자 매뉴얼 1부가 prompt→context→harness→loop 세대 전이 + 실무 패턴(plan-then-execute, maker/verifier, subagent 분업, golden set/eval 회귀, 오답노트→케이스 승격, 상태 파일 영속성, worktree 격리, headless/cron)을 주장하므로 외부 1차 근거 필요.

**How to apply:** 이 도메인 재조사·인용 시 `_internal/search_results.json`(61 papers) + `search_results.md`(패턴→근거 매핑 표) 먼저 읽기.

세대 명명 권위:
- Context Eng = Anthropic "Effective context engineering" + Addy Osmani (canonical)
- Harness Eng = Anthropic "Effective harnesses for long-running agents" + Addy "Agent Harness Engineering"
- Loop Eng = **Addy Osmani 가 명명자** ("Loop Engineering", 2026-06), Cobus Greyling 이 정리/대중화

핵심 대립 (균형 인용 필수): subagent 분업 — Anthropic "multi-agent research system"(찬성) ↔ Cognition "Don't Build Multi-Agents"(쓰기 작업 반대). read vs write 구분으로 종합.

maker/verifier 자기채점 금지 canonical: Epsilla "GAN-Style Agent Loop" (generator-critic = GAN generator-discriminator).

Round 2 확장 갭(2026-06-11): headless/cron(Claude Code GitHub Actions docs), worktree 격리(Zylos Research 종합), compaction/영속성(Redis 가이드 — L1-L4 memory hierarchy), eval-driven(Braintrust EDD — frozen core vs growing set, golden 40/failure 40/adversarial 20), spec-driven(Addy "good spec" + GitHub spec-kit). arXiv 정식화: 2509.08646(Secure P-t-E), 2601.22025(Eval-Driven Iteration), 2602.00180/2602.02584(Spec-Driven).

세대별 arXiv tier-4 정식화 카드 (`cards/`, 2026-06-11 추가):
- Context Eng → `arxiv-agentic-context-engineering` (2510.04618, ACE) — **context collapse** 정량 측정(18,282→122 tokens, 66.7→57.1%), Generator/Reflector/Curator delta update. AppWorld +10.6%.
- Harness Eng (정의) → `arxiv-code-as-agent-harness` (2605.18747, UIUC/Meta/Stanford) — harness 한 문장 정식 정의("turns a stateless model into a functional agent"), 200+ works survey, §5.2 "science of harness engineering 부재" open challenge.
- Harness Eng (측정) → `arxiv-inside-the-scaffold` (2604.03515, Rombaut) — 13 OSS coding agent 소스코드 taxonomy(3 layer×12 dim), loop primitive 조합 spectrum. 성능 벤치 없음.

주의: arXiv 출처는 모두 tier 4 보조 — 블로그 1차 주장의 학술 뒷받침용, material claim 단독 근거 금지.

Cobus Greyling 정리·대중화 배치 (`cards/greyling-*`, tier 2, 2026-06-11 추가, 5장):
- `greyling-rise-of-harness-engineering` (2026-03) — harness=4번째 architectural layer(SDK/Framework/Scaffolding 위), Schmid OS analogy, parallel.ai 6-component, "framework collapsing into harness" 80/20.
- `greyling-agent-model-harness` (2026-06) — **Harness-Bench(Qihoo360) 논문 해설**. Agent=Model+Harness 식, execution alignment(4-way correspondence), 실패=번역(contract violation 36.4%), harness swap 23.8pt, **inversion**(harness 가치는 model 강해질수록 감쇠 — 만능론 자기제한), minimal-loop 우월(NanoBot 76.2).
- `greyling-loop-engineering` (2026-06) — loop=harness 위 layer, 6-block(scheduling/worktrees/skills/connectors/sub-agents/memory), maker-checker "don't grade own homework".
- `greyling-loop-engineering-playbook` (2026-06) — inner/outer loop, runtime tiering(A terminal/B platform-LangChain/C editor), stateful/stateless cron.
- `greyling-configured-not-coded` (2026-05) — "configuration is code in a different costume", markdown-as-programming-surface, discipline gap(diff/predict/rollback/measure/prune), "model rented harness owned".

**Greyling 출처-인용 관행 (매뉴얼 명명-권위 vs 정리-역할 구분에 사용)**: Greyling 은 _명명자가 아니라 정리·대중화자_. 매 글이 외부 1차 권위를 명시 호명 — loop=Addy Osmani 명명/Steinberger·Cherny 슬로건, harness=OpenAI·Anthropic·Fowler·parallel.ai·Schmid, Agent=Model+Harness=Harness-Bench 논문. 예외: `configured-not-coded` 는 자기-코퍼스 종합(외부 권위 적음). material claim 인용 시 Greyling 카드를 통해 _원 출처로 거슬러_ 인용할 것 — Greyling 자체는 2차.
