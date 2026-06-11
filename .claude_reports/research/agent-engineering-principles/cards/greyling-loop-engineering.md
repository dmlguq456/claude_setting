---
title: "Loop Engineering"
authors: Cobus Greyling
venue: Medium
year_month: 2026-06 (approx; "1 day ago" relative to extract)
url: https://cobusgreyling.medium.com/loop-engineering-62926dd6991c
raw_type: blog
tier: 2
role: 정리·대중화 (popularizer) — loop engineering 개념을 세대 프레임으로 정리, 원 출처 명시 인용
---

## Core Claims (verbatim)

1. "Loop engineering is the shift from you being the one who prompts the coding agent turn-by-turn to you designing a system (the loop) that discovers work, hands tasks to agents (often sub-agents), verifies results, persists state, and decides the next action…on a schedule or until a goal is met."
2. "The harness equips a single agent run; the loop is what keeps poking agents on a schedule, spawning helpers, and feeding itself."

## Key Concepts & Definitions

- **Loop engineering**: prompt-by-prompt 조작자 역할을 자동 control system 설계로 대체. "recursive goal where you define a purpose and the AI iterates until complete" (Addy Osmani 인용). harness 보다 한 단계 위 layer ("one level above agent harness engineering").
- **Harness vs Loop 구분**: harness = 단일 agent run 을 장비. loop = 스케줄·sub-agent spawn·self-feeding 으로 agents 를 계속 찌르는 외부 control system.
- **Five Building Blocks + Memory (6 parts)**: loop 은 긴 prompt 하나가 아니라 6 개 부품의 작은 system. 5 개는 capability, 6 번째(memory)는 run 간 state 를 잡는 spine.
  1. **Automations / Scheduling (heartbeat)** — cadence 가 one-off session 을 discovery·triage 로 전환. Claude Code `/loop`·`/schedule`·`/goal` (별도 모델이 "done" 채점 — worker 가 자기 숙제 채점 X). Grok `/loop [interval]` + scheduler_create/list/delete. "reliable 하면 clever 할 필요 없다."
  2. **Worktrees** — 동일 파일 동시 편집 = merge 재앙. isolated git worktree 로 각 agent 에 별도 작업 디렉토리, history 공유. orphaned worktree cleanup 중요.
  3. **Skills (persistent project knowledge)** — 매 session cold start. SKILL.md + scripts/references 로 run 간 생존 지식 외부화 = "pay down intent debt". CLAUDE.md/skills, plugin 패키징.
  4. **Plugins & Connectors** — read-only loop = suggester. MCP connector 로 PR open·Linear·Slack·DB·runbook 실행 → commentator → operator.
  5. **Sub-agents (maker/checker split)** — 코드 쓴 agent 는 자기 작업의 나쁜 심판 (model 한계 아니라 structural). 다른(때로 더 강한) model + 다른 instruction 이 spec/skill/test 대조 검증.
  6. **Memory (durable spine)** — STATE.md / LOOP-STATE.json / Linear column / GitHub Project view. 세 질문 답해야: 지금 뭘 하나 / 지난번 뭘 시도했고 결과 / 무엇이 human 대기 중. multi-day loop 엔 non-negotiable.

## Patterns Covered

- maker/checker (separate verifier model, "don't grade your own homework")
- scheduled heartbeat / cadence-driven discovery+triage
- isolated parallel execution (worktrees)
- externalized persistent knowledge (skills/SKILL.md)
- MCP connectors for actuation
- durable state file as primary artifact
- cost-aware triage (cheap triage, spawn sub-agents only when state says actionable)

## Generation Mapping

명시적 세대 서사: "remember when Context Engineering was new, then Harness Engineering…now we have Loop Engineering." → prompt → context → harness → **loop** 의 최상위 세대로 loop 를 위치시킴. loop = harness 위 layer.

## Quotable

1. "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." (Peter Steinberger, OpenClaw creator, Greyling 인용)
2. "I don't prompt Claude anymore. I have loops running that prompt Claude and figuring out what to do. My job is to write loops." (Boris Cherny, head of Claude Code @ Anthropic, Greyling 인용)
3. "Build the loop like someone who intends to stay the engineer — not just the person who presses go."

## Limitations / Caveats

- **출처 인용 관행**: 본 글은 Greyling 의 _정리·종합_ 포지션. loop engineering 명명·프레임의 1차 권위는 **Addy Osmani** ("Addy's framing", "Addy calls this..."), 실무 슬로건은 **Peter Steinberger**(OpenClaw)·**Boris Cherny**(Anthropic) 에게 명시 귀속. 즉 Greyling 은 명명 권위가 아니라 _세 사람의 발언을 6-block 구조로 묶은 정리자_. 매뉴얼에서 명명 권위(Osmani/Cherny) vs 정리 역할(Greyling) 구분에 직접 사용 가능.
- caveats 자기명시: loops are early / 토큰 비용 폭증(5분 loop + maker/checker = "burn through a limited plan before breakfast") / "done" 은 검증 전까지 claim / comprehension debt / cognitive surrender.
- Grok·Claude Code 양대 도구 primitive 수렴 주장 (loop shape tool-agnostic) — 1차 측정 없는 관찰적 주장.
- 인용된 Cherny 발언("loops named as feature they'd be proudest of in 10 years" 등)은 "widely clipped"·"apparently" 등 2차 전언 — verbatim 신뢰도 중간.
