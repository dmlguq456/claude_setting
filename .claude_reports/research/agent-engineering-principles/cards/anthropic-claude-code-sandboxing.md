---
title: "Beyond permission prompts: Making agents secure with sandboxing"
authors: [David Dworken, Oliver Weller-Davies]
venue: Anthropic Engineering blog
year-month: 2025-10
url: https://www.anthropic.com/engineering/claude-code-sandboxing
raw_type: technology blog
tier: 1
---

## Core Claims
> "In our internal usage, we've found that sandboxing safely reduces permission prompts by 84%."

> "By defining set boundaries within which Claude can work freely, they increase security and agency."

## Key Concepts & Definitions
- **Sandboxing**: per-action permission 요청 없이 자율 동작하게 하는 pre-defined boundary.
- **Filesystem isolation**: 특정 디렉터리로 접근/수정 제한, sensitive system file 차단.
- **Network isolation**: 승인된 server 로만 연결 제한 — data exfiltration·malware download 방지.
- **Permission fatigue**: 끊임없는 approval 요청에서 오는 user 부주의 ('approval fatigue').
- **Autonomous safety**: OS-level enforcement (Linux bubblewrap, macOS seatbelt) 안에서 동작 — 직접 상호작용과 spawned subprocess 모두 포함.

## Patterns Covered
- 디렉터리/도메인 제한 가능한 sandboxed bash tool.
- Claude Code on the web (isolated cloud execution).
- secure proxy 통한 git credential 처리 (sandbox 안에 secret 미노출).
- dual-boundary enforcement 로 prompt injection 봉쇄.

## Generation Mapping
- **Loop Eng / 자율 실행 안전장치 (격리 층)**: 매뉴얼 1부 'worktree 격리·headless 자율 실행'의 OS-level 격리 근거. auto-mode classifier(intent 층)와 상보 — 이쪽은 filesystem/network 의 hard boundary 층. 본 survey 의 worktree 격리 주장과 직접 대응.

## Quotable
> "Constantly clicking 'approve' slows down development cycles and can lead to 'approval fatigue.'"

> "Effective sandboxing requires both filesystem and network isolation."

## Limitations
- 두 격리(filesystem+network) 동시 필요 — 불완전 구현은 취약.
- OS-level primitive (bubblewrap/seatbelt) 의존 — portability 미논의.
- enterprise domain rule 엔 custom proxy 필요, 기본 restrictive posture 미기술.
- performance overhead·edge case 취약점 논의 없음.
