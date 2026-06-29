---
title: Building a C compiler with a team of parallel Claudes
authors: Anthropic Engineering
venue: Anthropic Engineering Blog
year-month: 2025
url: https://www.anthropic.com/engineering/building-c-compiler
raw_type: engineering blog (technology)
tier: 1
---

## Core Claims
1. 16개 Claude Opus 4.6 instance 가 약 2,000 세션 (~$20,000) 동안 자율적으로 100,000줄 Rust 기반 C compiler 를 구축 — x86·ARM·RISC-V 에서 Linux 6.9 를 compile 하고 Doom 을 돌릴 수준. 최소 human oversight 로 agent team 이 복잡한 long-running 자율 개발을 해냄을 입증.
2. **Autonomous progress loop**: bash harness 가 Claude Code 세션을 무한 loop 로 spawn, 모델은 작업 완료 후 다음 task 를 직접 선택. "to approach the problem by breaking it into small pieces, tracking what it's working on" 지시.
3. **lock 기반 task 조율**: agent 가 `current_tasks/` 에 task lock 을 텍스트 파일로 써서 (예 `current_tasks/parse_if_statement.txt`) 충돌 방지 — git sync 가 두 번째 claim 을 다른 task 로 밀어냄.
4. **task verifier 가 거의 완벽해야** 한다 — Claude 가 주어진 문제를 끝까지 자율로 풀므로 검증기 품질이 결정적.

## Key Concepts & Definitions
- **Agent Teams**: human 개입 없이 공유 codebase 에서 병렬로 일하는 다수 Claude instance.
- **Autonomous Progress Loop**: Claude Code 세션을 끊임없이 spawn 하는 bash harness, 모델이 다음 task 를 골라 small piece 로 쪼개 진행.
- **Online known-good oracle**: Linux kernel 처럼 monolithic task 에서 GCC 를 known-good compiler oracle 로 써, 무작위 compile 한 kernel section 을 비교해 파일별 parallel debugging 가능케 함.

## Patterns Covered
- **worktree 병렬 격리 (= container 격리)**: 각 agent 가 Docker container, repo 를 `/upstream` 에 mount, `/workspace` 로 clone 해 독립 작업 후 push.
- **merge 전략**: "Merge conflicts are frequent, but Claude is smart enough to figure that out" — upstream pull → parallel worker 변경 merge → push → lock 제거.
- **maker-verifier 분리**: 광범위 test harness (GCC torture test·SQLite·Redis·libjpeg 등)가 human 판단 없는 pass/fail 신호.
- **서브에이전트 분업**: code deduplication·performance·output efficiency·quality critique·documentation 에 별도 agent 할당.
- **파이프라인 세분화**: GCC oracle 로 monolithic kernel compile 을 파일별 parallel 로 분해.
- **상태 파일·영속성**: progress·task metadata 를 version-controlled 파일로, spawn 시 read.
- **headless/cron**: 무한 loop harness 가 human operator 없이 동작.
- **컨텍스트 절약·compaction**: test output 엄격 통제 — "should not print thousands of useless bytes...log all important information to a file".
- **오답노트→케이스 승격**: "a running doc of failed approaches and remaining tasks" 를 git history 에 유지.
- **plan-then-execute**: 문제를 small piece 로 쪼개 tracking (loop 내 self-planning).

## Generation Mapping
- **loop engineering** 의 1차 근거 — 무한 bash loop + lock 기반 조율 + 거의 완벽한 verifier 가 "원칙의 세대사" 의 _loop engineering_ 단계 핵심 증거.
- **worktree 병렬 격리 / merge 전략**의 직접 출처 (조사 컨텍스트 #4 지정): container clone-push 격리, lock 파일 task 조율, Claude 자율 merge.
- **서브에이전트 분업 / 파이프라인 세분화 / 오답노트→케이스 승격 / 상태 파일 / headless** 패턴이 한 글에 거의 다 등장 — 실무 패턴 종합 사례.
- 등장 배경: "verifier 가 거의 완벽하면 agent team 을 얼마나 멀리 밀 수 있나" 를 극한 실험한 사례. 사용자 매뉴얼의 maker-verifier·golden test·worktree·loop·오답노트 패턴이 실제로 함께 작동함을 보이는 capstone.

## Quotable
1. "The loop runs forever—although in one instance, I did see Claude pkill -9 bash on accident, thus killing itself." (Enabling long-running Claudes 섹션) — 무한 loop 의 현실적 fragility.
2. "Claude will work autonomously to solve whatever problem I give it. So it's important that the task verifier is nearly perfect." (Write extremely high-quality tests 섹션) — verifier 품질이 자율성의 전제.
3. "Merge conflicts are frequent, but Claude is smart enough to figure that out." (parallel worker 조율 관련) — 자율 merge 전략.

## Limitations / Caveats
- 16-bit x86 real-mode boot compiler 부재 (GCC 호출); x86_32/64 만 native.
- 독립 assembler/linker 없음 — 최종 단계 GCC 의존.
- optimization 끈 GCC 대비 생성 코드 효율 뒤처짐, 모든 project 를 compile 못 함 (drop-in 대체 아님).
- 코드 품질 "nowhere near... an expert Rust programmer".
- project 한계 근처에서 "New features and bugfixes frequently broke existing functionality" (회귀 빈발).
- Opus 4.6 이 32k 미만 16-bit x86 codegen 구현 실패 (60kb 생성).
- 저자 우려: "The thought of programmers deploying software they've never personally verified is a real concern".
