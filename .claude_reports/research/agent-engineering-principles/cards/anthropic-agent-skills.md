---
title: "Equipping agents for the real world with Agent Skills"
authors: [Barry Zhang, Keith Lazuka, Mahesh Murag]
venue: Anthropic Engineering blog
year-month: 2025-10
url: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
raw_type: technology blog
tier: 1
---

## Core Claims
> "Skills let Claude load information only as needed."

Agent Skills 는 "organized folders of instructions, scripts, and resources that agents can discover and load dynamically", general-purpose agent 를 specialized agent 로 전환시킨다.

## Key Concepts & Definitions
- **Agent Skills**: SKILL.md (metadata·instruction) + script + bundled resource 를 담는 directory 기반 capability package.
- **Progressive disclosure**: layered 정보 아키텍처 — startup 시 metadata 만 로드, 관련될 때 full SKILL.md 로드, 추가 파일은 on-demand. "the amount of context that can be bundled into a skill is effectively unbounded."
- **SKILL.md**: YAML frontmatter (name·description) + 상세 instruction 필수 파일, 추가 문서 참조.
- **On-demand loading**: task 관련 시에만 skill 을 읽어 context window 효율 유지.

## Patterns Covered
- Skill anatomy·file structure.
- Skill triggering 중 context window 관리.
- Skill 안 code execution 통합.
- 다층 파일에 걸친 progressive disclosure.
- Skill 설치 시 security audit 권고.

## Generation Mapping
- **Context Eng (canonical 보강)**: progressive disclosure 로 context 절약 — 매뉴얼 1부 '컨텍스트 절약(progressive disclosure)'의 1차 출처. 본 survey 의 ~/.claude SKILL.md 카탈로그 디자인(자동 주입 description + on-demand SKILL.md Read)과 직접 대응.

## Quotable
> "Skills let Claude load information only as needed."

> "The amount of context that can be bundled into a skill is effectively unbounded."

## Limitations
- 적절한 triggering 위해 신중한 skill naming/description 필요.
- 신뢰 안 된 skill 의 보안 취약점 가능 — audit 권고.
- emerging platform — feature 추가 진행 중.
