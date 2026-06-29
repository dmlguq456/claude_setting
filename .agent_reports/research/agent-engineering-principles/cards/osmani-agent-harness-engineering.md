---
title: "Agent Harness Engineering"
authors: ["Addy Osmani"]
venue: "addyosmani.com (blog)"
year-month: "2025"
url: https://addyosmani.com/blog/agent-harness-engineering/
raw_type: blog
tier: 1
---

# Agent Harness Engineering

## Core Claims

- (What is a harness, really?) verbatim: **"A decent model with a great harness beats a great model with a bad harness."** — harness 가 model 못지않은 leverage 축임을 명제화. 세대사에서 harness engineering 세대의 thesis.
- (The "skill issue" reframe) verbatim: **"The gap between what today's models can do and what you see them doing is largely a harness gap."** — 모델 한계가 아니라 scaffolding 한계로 문제를 재정의.

## Key Concepts & Definitions

- **Harness engineering (operational def, Opening):** verbatim — "anytime you find an agent makes a mistake, you take the time to engineer a solution such that the agent never makes that mistake again." (이 글에서 _오답노트 승격_ 패턴의 1차 정의문.)
- **Coding agent = model + scaffolding (Opening):** verbatim — "A coding agent is the model plus everything you build around it. Harness engineering treats that scaffolding as a real artifact, and it tightens every time the agent slips."
- **Agent = Model + Harness (Viv Trivedy formulation, What is a harness, really?):** verbatim — "Agent = Model + Harness. If you're not the model, you're the harness." 명명 출처: "Viv Trivedy coined the term _harness engineering_."

## Patterns Covered

- **plan-then-execute / 파이프라인 세분화** — "Long-horizon execution: Ralph Loops, planning, verification" (section heading)
- **maker-verifier 분업** — "Planner / generator / evaluator splits"; "separating generation from evaluation into distinct agents outperforms self-evaluation"
- **서브에이전트 분업** — "Subagent spawning, handoffs, model routing"
- **상태 파일·영속성** — filesystem + Git; memory files like `AGENTS.md`
- **컨텍스트 절약** — "Battling context rot"; compaction, tool-call offloading, skills with progressive disclosure
- **worktree 격리** — Claude Code architecture diagram 안 명시
- **headless** — "a headless browser for web interaction"
- (명시 안 됨: golden set·eval standalone 용어, pipeline decomposition 라벨)

## Generation Mapping

- 이 글은 _prompt/context engineering 의 무엇이 안 됐다_는 식의 명시적 한계 서술을 하지 **않는다**. 대신 harness engineering 을 "간과돼 온 leverage 의 인식(recognition)"으로 프레이밍.
- 등장 배경(Opening): verbatim — "We've spent the last two years arguing about models... That conversation is fine as far as it goes, but it's missing the other half of the system." → model-중심 담론의 _other half_ 로 harness 세대 등장.
- 명명 사건(Opening): verbatim — "That discipline now has a name. Viv Trivedy coined the term _harness engineering_." (세대에 이름이 붙은 시점 자체를 사건으로 기록.)
- 모델 한계 → harness 가 메우는 항목(Generation 서사 보조): "Models have no additional knowledge beyond their weights" (Memory and search); "Models get worse at reasoning... as the context window fills up" (Battling context rot); "Early stopping, poor decomposition of complex problems, and incoherence as work stretches across multiple context windows" (Long-horizon execution). → context rot·early stopping·decomposition 실패가 harness 가 해결 대상으로 삼는 _이전 단계의 미해결분_.

## Quotable

1. "A decent model with a great harness beats a great model with a bad harness." (What is a harness, really?)
2. "If you can't name the behaviour a component exists to deliver, it probably shouldn't be there." (Working backwards from behaviour)
3. "The gap between what today's models can do and what you see them doing is largely a harness gap." (The "skill issue" reframe)

## Limitations

- harness engineering _자체_의 한계는 명시 안 함. 대신 미래 과제(Where this is going)로 제시: "Orchestrating many agents working in parallel on a shared codebase; agents that analyze their own traces to identify and fix harness-level failure modes; harnesses that dynamically assemble the right tools and context just-in-time..." → 이 open problems 가 다음 세대(loop engineering / self-improving) 로의 다리.
