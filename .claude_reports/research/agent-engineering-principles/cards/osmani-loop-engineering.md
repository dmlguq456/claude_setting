---
title: "Loop Engineering"
authors: ["Addy Osmani"]
venue: "addyosmani.com (blog)"
year-month: "2026-06"
url: https://addyosmani.com/blog/loop-engineering/
raw_type: blog
tier: 1
---

# Loop Engineering

## Core Claims

- (Introduction) verbatim: **"Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead."** — 세대사의 정점: 인간이 매 turn prompt 하는 자리를 시스템이 대체.
- (Conclusion) verbatim: **"The loop changes the work, it does not delete you from it."** — 자율 loop 에도 engineer 의 verification 책임은 남는다는 경계.

## Key Concepts & Definitions

- **Loop engineering (Introduction):** verbatim — "Loop engineering is replacing yourself as the person who prompts the agent. You design the system that does it instead."
- **Loop = self-feeding harness:** verbatim — "The harness but it runs on a timer, it spawns little helpers, and it feeds itself." → harness 와의 차이를 _timer·spawn·self-feed_ 로 규정 (harness 의 위 계층).
- **Loop 의 작동(자율):** verbatim — "you build a small system that finds the work, hands it out, checks it, writes down what is done and then decides the next thing." (find → hand out → check → log → decide next 사이클.)

## Patterns Covered

- **headless·cron / 파이프라인 세분화** — Automations (scheduled discovery/triage)
- **worktree 격리** — Worktrees (parallel isolation)
- **오답노트 승격 / 프로젝트 지식 코드화** — Skills (codified project knowledge)
- **plugin/connector** — MCP 통한 tool integration
- **maker-verifier 분업 + 서브에이전트 분업** — Sub-agents (separation of maker and verifier); adversarial code review; agent teams
- **상태 파일·영속성** — State (persistence via markdown/Linear)
- **plan-then-execute** — `/goal` (run-until-done condition)

## Generation Mapping

- **이전 세대(수동 prompting) 한계 → loop 등장**, verbatim (Prompt Engineering section): "For like two years the way you got something out of a coding agent was you wrote a good prompt and shared enough context. You type a thing, you read what came back, you type the next thing." → 이 _type/read/type_ 수동 루프가 한계.
- 전환 사유, verbatim: 사용자가 agent 를 "holding [the agent] the entire time, one turn after the other. That part is kind of over." → _사람이 매 turn 붙들던 것_ 이 끝났다 = loop engineering 의 존재 이유. (harness engineering 글의 open problem "agents that run on a timer / self-improving" 이 여기서 실현.)
- 계층 관계: loop engineering 은 harness engineering _위_에 위치 (harness 가 timer 로 돌고 helper 를 spawn 하고 self-feed).

## Quotable

1. "The loop changes the work, it does not delete you from it." (Conclusion)
2. "Build the loop. Stay the engineer." (Conclusion)
3. "Designing the loop is the cure when you do it with judgement and the accelerant when you do it to avoid thinking." (body)

## Limitations

- (What the loop still does not do for you 섹션) — verification 은 여전히 인간 책임; 코드를 안 읽으면 comprehension debt 가 쌓임; cognitive surrender (판단 없이 수동 의존) 위험.
- 저자 결론: "If I weren't reviewing the code myself...my product's quality would suffer." → loop 자동화의 상한은 인간 review.
