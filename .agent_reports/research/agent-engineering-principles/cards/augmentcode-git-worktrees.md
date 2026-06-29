---
title: "How to Use Git Worktrees for Parallel AI Agent Execution"
authors: Augment Code
venue: augmentcode.com/guides
year-month: 2025
url: https://www.augmentcode.com/guides/git-worktrees-parallel-ai-agent-execution
raw_type: vendor guide
tier: 3
---

## Core Claims
- (verbatim) "Each worktree gets a private `HEAD`, private `index`, and private working directory. Agent A's uncommitted edits in `/project/.trees/TASK-123/` are invisible to Agent B."
- (verbatim) "The conflict problem moves to the PR merge stage. Standard git conflict detection, diff tooling, and rebase workflows handle these deferred conflicts at merge time, where they surface as visible git conflicts instead of silent runtime overwrites."

## Key Concepts & Definitions
- **Worktree = isolated working dir + git index, shared object store**: 여러 agent 가 동시 작업.
- **Setup**: `git worktree add -b agent/TASK-123 .trees/TASK-123 origin/main` → `cd .trees/TASK-123 && npm ci --prefer-offline`.
- **Lock contention 제거**: 여러 agent 가 `.git/index.lock` 경쟁 안 함 (이전엔 동시 git op 시 fatal error).
- **Deferred conflict resolution**: 충돌을 PR merge 단계로 이연 — silent runtime overwrite 대신 visible git conflict 로 표면화.

## Patterns Covered
- **Branch 대비 우위**: sequential `git checkout` 은 한 branch 만 active → parallelism 차단. worktree 는 동시 격리 (full clone 처럼 history 중복 X).
- **Test baseline 먼저**: "Create the worktree, run `npm lint` and `npm test` immediately, confirm the suite passes green, then hand the worktree to the agent." → 새 실패가 agent 도입분임을 입증.
- **2-gate human review**: merge 전 spec 대조 검증을 위한 두 review checkpoint.

## Generation Mapping
- **private HEAD/index/working dir 격리** = 본 family §5.10 worktree 병렬 분사의 기술적 근거 — "Agent A 의 uncommitted edit 이 Agent B 에 invisible" = 본 family 의 파일 겹침 triage·큐잉 정책 정당화.
- **deferred conflict → PR merge 단계** = 본 family 의 "merge 는 Claude 선별 책임, 본작업은 브랜치에 남기고 main 불변으로 turn 종료" 와 동형 — 충돌을 명시적 merge 자리로 미룸.
- **test baseline 먼저 (green 확인 후 hand)** = 본 family 의 빌드 검증·회귀 제외 원칙 (§5.10) 과 매핑. autopilot-code/lab 의 baseline 확보 단계와 연결.
- **lock contention 제거** = "오케스트레이션은 항상 main, background 병렬 job" 구조에서 동시 git op 안전성의 외부 근거.
- **2-gate human review** = 본 family 의 사용자 머지 신호·diff 실내용 확인 게이트와 정합.

## Quotable
- "Each worktree gets a private `HEAD`, private `index`, and private working directory."
- "where they surface as visible git conflicts instead of silent runtime overwrites."
- "Create the worktree, run `npm lint` and `npm test` immediately, confirm the suite passes green, then hand the worktree to the agent."

## Limitations / Caveats
- vendor guide (Augment Code 제품 맥락, tier 3) — 자사 tooling 홍보 bias 가능.
- 예시가 npm/node 중심 — 다른 stack (Python 등) 일반화 시 baseline 명령 치환 필요.
- `.trees/` layout 은 컨벤션일 뿐 — repo 별 .gitignore·CI 경로 조정 필요.
