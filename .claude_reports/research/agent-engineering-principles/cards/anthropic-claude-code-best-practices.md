---
title: "Best practices for Claude Code (agentic coding)"
authors: Anthropic
venue: Anthropic Engineering Blog / Claude Code Docs (308 redirect → code.claude.com/docs/en/best-practices)
year_month: 2025
url: https://code.claude.com/docs/en/best-practices
raw_type: blog/docs
tier: 1
---

## Core Claims

1. **거의 모든 best practice 는 단 하나의 제약에서 나온다 — context window 는 빨리 차고, 차오를수록 성능이 떨어진다.** "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills." (intro) "The context window is the most important resource to manage."
2. **Agent 에게 스스로 돌릴 수 있는 verification 수단을 주면 loop 가 자동으로 닫힌다.** "Give Claude something that produces a pass or fail, and the loop closes on its own. Claude does the work, runs the check, reads the result, and iterates until the check passes." ("Give Claude a way to verify its work")
3. **연구·계획을 구현과 분리하라 — 안 그러면 엉뚱한 문제를 푼다.** "Separate research and planning from implementation to avoid solving the wrong problem." ("Explore first, then plan, then code")
4. **CLAUDE.md 는 매 대화 시작에 로드되는 영속 context 파일이며, 길면 오히려 무시된다.** "Bloated CLAUDE.md files cause Claude to ignore your actual instructions!"

## Key Concepts & Definitions

- **CLAUDE.md**: "a special file that Claude reads at the start of every conversation. Include Bash commands, code style, and workflow rules. This gives Claude persistent context it can't infer from code alone." 위치는 home/project root/parent/child 계층. 판단 기준: "Would removing this cause Claude to make mistakes?"
- **Hooks** (verbatim): "Unlike CLAUDE.md instructions which are advisory, hooks are deterministic and guarantee the action happens." — Stop hook 은 check 통과 전까지 turn 종료 차단(8 consecutive blocks 후 override).
- **Subagents**: "run in their own context with their own set of allowed tools" — main 대화를 오염시키지 않고 다파일 탐색·검증 수행.
- **Non-interactive (headless) mode**: `claude -p "prompt"` — CI/pre-commit/script 통합용, output-format text|json|stream-json.
- **Skills**: 가끔만 필요한 도메인 지식·workflow 를 on-demand 로 로드(CLAUDE.md bloat 회피).

## Patterns Covered

- **plan-then-execute**: ✓ explore→plan→implement→commit 4단계 workflow + plan mode. "If you could describe the diff in one sentence, skip the plan."
- **maker-verifier 분리**: ✓ Writer/Reviewer 패턴 + adversarial review subagent — "a fresh model try to refute the result, so the agent doing the work isn't the one grading it".
- **서브에이전트 분업**: ✓ "use subagents to investigate X" — 별도 context 에서 탐색 후 요약 보고 + 검증 subagent.
- **상태 파일·영속성**: ✓ CLAUDE.md(git 체크인, "compounds in value over time") + SPEC.md(interview→spec→fresh session 실행) + checkpoint/resume.
- **worktree 병렬 격리**: ✓ "Worktrees: run separate CLI sessions in isolated git checkouts so edits don't collide" + Agent teams.
- **headless/cron**: ✓ `claude -p` CI/pre-commit + fan-out(`for file in ...; do claude -p ... done`) + auto mode.
- **컨텍스트 절약·compaction**: ✓ `/clear` between unrelated tasks, `/compact <instructions>`, auto-compaction, `/btw` overlay.
- **오답노트→케이스 승격**: △ 약하게 — CLAUDE.md 를 "review it when things go wrong, prune it regularly" 하고 실패 패턴(kitchen sink, correcting over and over)을 명시. golden set/eval 자체는 다루지 않음.

## Generation Mapping

이 글은 매뉴얼 세대사의 **harness + loop engineering 세대의 실무 종합**이다. CLAUDE.md(영속 상태)·hooks(deterministic gate)·subagents(분업)·plan mode(plan-then-execute)·worktrees(병렬 격리)·headless(`-p`)·`/clear`·`/compact`(compaction) 가 한 글에 모여 있어, 매뉴얼의 거의 모든 실무 패턴(plan-then-execute / maker-verifier 분리 / 서브에이전트 분업 / 상태 파일·영속성 / worktree 병렬 격리 / headless·cron / 컨텍스트 절약·compaction)에 1차 근거를 댄다. 등장 배경: building-effective-agents 의 추상 패턴이 실제 coding agent 제품에서 어떻게 구체화되는지를 보여주는 운영 매뉴얼. 매뉴얼의 harness 절은 hooks/CLAUDE.md 를, loop 절은 verify-loop/`/goal`/Stop hook 을 이 글에서 인용하면 된다.

## Quotable

1. "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills." (intro)
2. "Give Claude something that produces a pass or fail, and the loop closes on its own. Claude does the work, runs the check, reads the result, and iterates until the check passes." (Give Claude a way to verify its work)
3. "A reviewer running in a fresh subagent context sees only the diff and the criteria you give it, not the reasoning that produced the change, so it evaluates the result on its own terms." (Add an adversarial review step)

## Limitations / Caveats

- Plan mode 는 overhead — "If you could describe the diff in one sentence, skip the plan."
- Adversarial reviewer 과신 금지: "A reviewer prompted to find gaps will usually report some, even when the work is sound... Chasing every finding leads to over-engineering." correctness/요구사항 영향 gap 만 flag 하도록 지시.
- Checkpoint 은 git 대체 아님 — "Checkpoints only track changes made by Claude, not external processes."
- 패턴은 고정 규칙 아님 — "Sometimes you should let context accumulate... Sometimes you should skip planning." 직관을 길러야 함("Develop your intuition").
- Auto mode `-p` 실행 시 classifier 가 반복 차단하면 fallback 사용자가 없어 abort.
