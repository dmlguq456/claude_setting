---
title: "Loop Engineering Playbook"
authors: Cobus Greyling
venue: Medium
year_month: 2026-06 (approx; "16 hours ago" relative to extract, 후속편)
url: https://cobusgreyling.medium.com/loop-engineering-playbook-4460e01e88d8
raw_type: blog
tier: 2
role: 정리·대중화 (실무 map/tiering) — loop 의 "어디서 사는가"·runtime 선택을 LangChain framing 빌려 정리
---

## Core Claims (verbatim)

1. "A loop is not a prompt, it is a recurring process with memory, verification, and boundaries."
2. "reasoning alone does not close the loop. An agent that can only suggest is not running a loop. An agent that can run code, observe the result, fix it, and run again is."

## Key Concepts & Definitions

- **Inner loop vs Outer loop**: "reason, act, observe, repeat…that feedback cycle is the inner loop every outer loop depends on." 코딩 agent 는 local 에서 inner loop 획득(edit·run test·read stderr·iterate). outer loop = scheduling/persistence/isolation 의 control system.
- **Where does the loop live? — 3 layers**: loop 은 집이 필요 — schedule next run, persist state, isolate parallel work, reach real tools.
- **Runtime territory 진입 신호**: loop 이 (a) 3 a.m. terminal 없이 실행 (b) process crash 중간 생존 (c) human approval 위해 3 일 pause (d) agent 마다 isolated machine 필요할 때 → terminal harness 를 넘어 platform runtime 필요.
- **LangChain framing 차용**: "Every agent needs a computer" / "Give your agent its own computer." LangSmith Sandboxes(hardware-isolated microVM per agent), Durable execution(checkpointed graph state, crash 생존), Cron on Agent Server, Human-in-the-loop interrupts(pause→free resources→resume days later from checkpoint).
- **Stateful vs Stateless cron** (LangChain 구분, "worth stealing"): stateful = 같은 thread_id 매 run, agent 가 어제 기억(nightly research·history monitoring) → "append to STATE.md". stateless = fresh thread per run, batch triage·one-off sweep → "read repo and exit."

## Patterns Covered

- inner/outer loop 분해
- 3-layer 거주지 모델 (schedule·persist·isolate·reach)
- tiering by runtime (아래 Generation Mapping 참조)
- stateful/stateless cron 구분 = STATE.md append vs read-and-exit
- cost/safety defaults: cheap triage / spawn sub-agent only when actionable / cap iterations per item (3 attempts → escalate to human)
- comprehension debt 경고

## Generation Mapping

세대 자체보다 **loop 의 runtime 스펙트럼 tiering** 에 집중 (loop = harness 위 layer 라는 전편 전제 계승):
- **Tier A — Terminal harness loops**: solo / small team, Grok·Claude Code (`/loop`·skills·sub-agents·worktrees·MCP 한 곳에), human nearby.
- **Tier B — Platform runtime loops**: production / multi-tenant, restart 생존·audit trail·남이 쓴 코드 실행 → LangChain/LangSmith.
- **Tier C — Editor & lightweight alternatives**: editor lock-in 또는 full platform 없이 cron+webhook 만 원할 때.

## Quotable

1. "If you read Loop Engineering, you already know the shift: stop prompting agents turn-by-turn, and start designing systems that prompt them for you."
2. "The sandbox tweet is not about chat UIs. It is about giving each iteration of the loop a safe place to *work* — which is the prerequisite for unattended operation."
3. "the loop is leverage, not a substitute for judgment."

## Limitations / Caveats

- **출처 인용 관행**: 전편(loop-engineering)의 직속 후속편. 이 글의 차별점은 **LangChain 의 production framing**("Give your agent its own computer", durable execution, cron 구분)을 명시 차용·귀속. Greyling 은 다시 _정리자_ — LangChain 의 runtime vocabulary 를 loop tiering 으로 매핑. Addy Osmani·Boris Cherny 는 전편 권위로 재참조("Addy Osmani said it plainly. So did Boris Cherny from inside Anthropic").
- Grok·Claude Code "dominate the conversation" 이지만 "not the only tech" 가 글의 thesis — 도구 중립 주장이되 LangChain 우호적 편향 있음(LangChain framing 을 "I love" 로 명시 호평).
- tier 표 내용은 extract 에서 이미지로 처리돼 텍스트 부재 — tier 경계 기준만 본문에 서술.
- 1차 측정/벤치 없음 — 실무 권고·매핑 수준.
