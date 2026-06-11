---
title: "Git Worktree Isolation Patterns for Parallel AI Agent Development"
authors: Zylos (research)
venue: zylos.ai/research
year-month: 2026-02
url: https://zylos.ai/research/2026-02-22-git-worktree-parallel-ai-development
raw_type: research blog / technical writeup
tier: 3
---

## Core Claims
- (verbatim) "When two agents operate concurrently in the same tree, the failure modes are severe: File collisions, context contamination, index corruption, and conversation confusion."
- (verbatim) "The 'Rebase Before PR' model is the most widely recommended convention for parallel worktree development."

## Key Concepts & Definitions
- **Worktree 격리 원리**: 각 worktree 가 독립 `HEAD`·index·working tree file 을 유지하되 object database·remote config 는 공유 → "four or more concurrent AI sessions" 를 file-level 충돌 없이.
- **왜 branch/clone 가 아니라 worktree**: 같은 tree 동시 작업 → file collision·context contamination·index corruption·conversation confusion. full clone 대안은 "wastes disk, requires independent remote tracking, and makes rebasing across agents painful."
- **4 primary patterns**: (1) one worktree per agent task (2) comparative/ensemble agents (3) pipeline stages (4) sibling worktree layout.

## Patterns Covered
- **Setup**: `git worktree add -b feature-auth ../project-auth main` / `git worktree list` / `git worktree remove ../project-auth` / `git worktree prune`.
- **Native tooling**: Claude Code, Cursor, OpenAI Codex 가 worktree management 통합.
- **Merge 전략**: sequential integration, rebase-before-PR (가장 권장), pre-merge conflict detection, cherry-pick selection.
- **Pre-flight conflict detection (Clash)**: `git merge-tree $(git merge-base A B) A B` — repo 수정 없이 three-way merge 로 충돌 조기 감지.
- **Real-world**: incident.io, Cursor 2.0, CodeRabbit, ccswarm 채택 사례.

## Generation Mapping
- **one worktree per agent task** = 본 family §5.10 의 **"코드 본작업은 worktree+작업 브랜치에서, 새 독립 요청 → 파일 겹침 triage 후 새 worktree 로 background 병렬 분사"** 와 **정확히 동일한 패턴**. golden g3 재발 방지 정책의 외부 근거.
- **rebase-before-PR / pre-merge conflict detection** = 본 family 의 "merge 는 Claude 선별 책임, diff 실내용 확인·회귀/중복 제외·충돌 양쪽 의도 해석" (§5.10) 과 매핑.
- **failure modes (file collision/index corruption)** = 본 family 가 main 트리 직접 편집을 typo·1줄급만 허용하고 나머지는 무조건 브랜치로 미는 이유의 외부 정당화.
- **pipeline stages worktree** = autopilot-spec→code→lab 단계별 격리 가능성과 연결.
- **conversation confusion 회피** = "오케스트레이션은 항상 main, 서브에이전트 중첩 1단" 격리 원칙과 정합.

## Quotable
- "When two agents operate concurrently in the same tree, the failure modes are severe: File collisions, context contamination, index corruption, and conversation confusion."
- "The 'Rebase Before PR' model is the most widely recommended convention for parallel worktree development."
- (full clones) "wastes disk, requires independent remote tracking, and makes rebasing across agents painful."

## Limitations / Caveats
- research blog (tier 3) — peer-reviewed 아님. 채택 사례 인용은 있으나 정량 벤치마크 얕음.
- worktree 자체 비용 (creation/disk overhead/removal bottleneck) 존재 — 본문이 trade-off 로 인정.
- "four or more concurrent sessions" 는 환경 의존 (디스크·메모리·repo 크기).
