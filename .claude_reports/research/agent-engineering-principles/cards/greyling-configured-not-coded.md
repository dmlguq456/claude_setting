---
title: "Configured, not coded — The engineering discipline gap in agent development"
authors: Cobus Greyling
venue: Medium
year_month: 2026-05 (May 7, 2026)
url: https://medium.com/@cobusgreyling/configured-not-coded-the-engineering-discipline-gap-in-agent-development-e6dbeb9ddaf9
raw_type: blog
tier: 2
role: 정리·대중화 (의견·논평) — markdown-as-code 규율 격차를 제기, 자기 이전 글들을 엮는 thesis 글
---

## Core Claims (verbatim)

1. "When the artefact moves from code to configuration, the engineering discipline does not move with it."
2. "Configuration is code in a different costume."

## Key Concepts & Definitions

- **Configured, not coded**: universal agent = "one loop, configured". same model·same tool harness·same execution scaffold. task 간 바뀌는 것은 코드가 아니라 system prompt·tool list·markdown instruction.
- **Three collapses**: (1) integration layer collapsed — CLI 가 일상 task 에서 MCP 대체(다리가 이미 존재) (2) orchestration layer collapsed — prompt 가 framework 대체, 수백 줄 multi-agent 조정이 CLAUDE.md 의 영어 한 문단으로 (3) development environment collapsing — IDE optional(agent 는 file tree·debugger·syntax highlight 불필요).
- **Markdown is the new programming surface**: CLAUDE.md·AGENTS.md·system prompts·skill files·memory entries = agent 가 가치 ship 하는지 토큰 낭비하는지 결정하는 lever. "Nobody calls this code, so nobody treats it like code."
- **Discipline gap**: Python 시절 습관(version control·code review·tests·line-by-line diff·rollback·real changelog)이 markdown 으로 옮겨가며 조용히 누락. "The artefact looks like prose, so it gets edited like prose. But it behaves like code" — 작은 wording 변화가 success rate 를 뒤집고, instruction 이 turn 마다 decay, confident edit 이 측정 안 한 task 를 조용히 regress.
- **세 격차 발현 지점**: (1) system prompt as dumping ground — 새 실패마다 "be careful about X" 문단 추가, 제거 없음 → attention 이 wall of text 에 thin 해짐("silent killer") (2) no falsifiable change — 무엇을 fix/break 할지 예측 없이 ship, rollback 기계 없음("self-improving" agent 는 대개 defensive prediction 없는 rationale loop) (3) prose treated as portable — CLAUDE.md 를 repo 간 복붙(durable 한 건 tools·middleware·memory structure 뿐).

## Patterns Covered

- diff every edit (prompt change = code change, read line by line)
- predict before shipping (무엇을 fix/regress 할지 적고 next rollout 에 verify)
- rollback at file granularity when prediction misses
- measure what you change (before/after eval 없는 markdown edit = "a vibe")
- treat tools/memory/middleware as durable IP (prose 는 안 travel, 이것들은 travel)
- prune ruthlessly (every paragraph competes for attention; more words ≠ more discipline)

## Generation Mapping

세대 서사에 대한 **규율 측 메타-논평**. prompt→harness collapse 가 "win"(less infra·faster iteration)이라 인정하되, configuration 세대로 옮겨가며 engineering rigour 가 따라오지 않은 "discipline gap" = "the bill that comes with it" 를 제기. harness 세대의 그림자/책임론을 매뉴얼에 보강하는 위치. "model is rented, harness is owned" 로 harness 영속성(loop·tools·markdown)을 IP 로 규정.

## Quotable

1. "We replaced thousands of lines of orchestration code with a paragraph of English, and quietly walked away from the rigour that used to come with it."
2. "The model is rented, the harness is owned."
3. "A markdown edit without a before/after eval is a vibe."

## Limitations / Caveats

- **출처 인용 관행**: 이 글은 다른 넷과 달리 **자기-참조 종합(self-referential synthesis)** — 외부 권위 호명보다 본인 이전 Medium 글들("Anthropic Says Coding Agents…", "Universal Agents", "The Rise of AI Harness Engineering", "Two-Thirds of Multi-Agent Intelligence Is Harness", "silent killer")을 엮어 thesis 구성. 즉 정리자 중에서도 _자기 코퍼스 위 의견 글_. 1차 외부 출처·측정 없음.
- 모든 주장이 경험·관찰("I keep seeing in the wild") 기반 — 정량 근거 부재. fact-check 대상 수치 거의 없음(주로 규범적 권고).
- "CLI replaced MCP for most everyday tasks" 같은 단정은 트렌드 관찰일 뿐 측정 미동반.
- 규율 권고(diff·predict·rollback·measure·prune)는 소프트웨어 공학 일반 원칙의 markdown 적용 — 신규성보다 환기 가치. 매뉴얼에서 "harness=code 규율" 근거 인용에 적합하나 1차 출처로는 약함.
