---
title: "Long-running Agents"
authors: ["Addy Osmani"]
venue: "addyo.substack.com (Substack)"
year-month: "2025"
url: https://addyo.substack.com/p/long-running-agents
raw_type: blog
tier: 1
---

# Long-running Agents

## Core Claims

- (Opening) verbatim: **"A long-running AI agent can keep making progress over hours, days, or weeks. It can do this across many context windows and sandboxes, recover from failure, leave structured artifacts behind, and resume where it left off."** — long-running 의 정의이자 단일-session agent 와의 변별점.
- (body) verbatim: **"State lives outside the agent's context…the agent itself is amnesiac, but the filesystem isn't."** — 영속성 패턴의 thesis (상태 파일이 amnesia 를 메움).

## Key Concepts & Definitions

- **Long-running agent (정의):** verbatim — "A long-running AI agent can keep making progress over hours, days, or weeks... across many context windows and sandboxes, recover from failure, leave structured artifacts behind, and resume where it left off."
- **amnesiac agent + durable filesystem:** verbatim — "State lives outside the agent's context…the agent itself is amnesiac, but the filesystem isn't."
- **git as substrate:** verbatim — "A long task runs in a cloud sandbox with git as the coordination substrate."

## Patterns Covered

- **상태 파일·영속성** — plan files (`prd.json`, `feature-list.json`, explicit done-conditions); progress logs (`progress.txt`, `CHANGELOG.md`)
- **checkpointing / recovery** — checkpoint-and-resume (per N units of work); context resets and compaction (rebuild from structured handoffs)
- **서브에이전트 분업 / 파이프라인 세분화** — brain/hands/session decomposition (model loop · execution sandbox · durable log); planner/worker/judge pipeline
- **maker-verifier 분업** — split generation from evaluation (judge)
- **worktree 격리** — worktree isolation (git-based cross-run coordination)
- **Ralph Loop** — minimalist state mgmt: bash loop over task list, read/write persistent JSON+text
- **golden set·eval 관련(test 보호)** — "It is unacceptable to remove or edit tests..."

## Generation Mapping

- **short-horizon agent 의 3 한계 → long-running 등장:**
  1. **finite context**, verbatim: "A 24-hour run is not going to fit in any context window the field has on its roadmap." → context window 로는 장시간 작업을 못 담음.
  2. **no persistent state**, verbatim(Anthropic 인용): agents 를 "engineers working in shifts with no memory" 로 비유 — "every shift change is a productivity disaster." → 외부 영속성 없으면 교대마다 생산성 붕괴.
  3. **no self-verification**, verbatim: "Models reliably skew positive when they grade their own work." → 자가 채점 편향 = maker-verifier 분리(judge) 의 근거.
- 세대사 위치: harness/loop engineering 의 _시간 축 확장_. 영속성·checkpoint·judge 분리·worktree 가 "여러 context window 를 가로지르는" 작업의 전제로 묶임. ("amnesiac agent + durable filesystem" 이 핵심 서사.)

## Quotable

1. "State lives outside the agent's context…the agent itself is amnesiac, but the filesystem isn't."
2. "A long task runs in a cloud sandbox with git as the coordination substrate."
3. "It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

## Limitations

- **cost:** "A 24-hour run with a frontier model…is not cheap."
- **security:** API key·shell access 보유 long-running agent 은 attack surface 가 큼.
- **alignment drift:** re-summarization 사이클을 거치며 goal fidelity 손실.
- **verification difficulty:** 24 시간 자율 작업 audit 에는 observability infra 필요.
- **specification skill:** "Defining work crisply enough that an agent can run for a day on it is harder than doing the work yourself." → good-spec 글로 이어지는 다리.

(Substack — paywall 없음, 핵심 추출 확보.)
