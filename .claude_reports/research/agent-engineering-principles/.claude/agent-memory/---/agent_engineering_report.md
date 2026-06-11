---
name: agent-engineering-report
description: 에이전트 엔지니어링 원칙 종합 보고서(7-file technology mode) 생성 완료 — 세대사 4단·패턴 11종·tension 4종 구조와 핵심 인용 규칙
metadata:
  type: project
---

`agent-engineering-principles` research 의 7-file 보고서(00~07)를 2026-06-11 생성 완료. 다운스트림은 `autopilot-draft --mode doc` 매뉴얼 1부 '원칙의 세대사'.

**Why**: 사용자 ~/.claude 에이전트 시스템 README 확장판 매뉴얼의 근거 자료. 61 cards + code_search 기반.

**How to apply** (draft/refine/fact-check 자리에서):
- 세대 4단 = prompt→context→harness→loop, **누적 layer**(대체 아님). 명명 귀속 고정: context=Osmani+Anthropic 공동, harness=Trivedy 명명, loop=Osmani 명명/Cherny·Steinberger 슬로건, "Agent=Model+Harness"=Harness-Bench 논문.
- **Greyling(tier 2)은 명명자 아니라 정리·대중화자** — 인용 시 원 1차 출처로 거슬러 귀속.
- **tier 4 arXiv 단독 인용 금지** — 블로그 1차 주장의 정량 backing 으로만.
- fact-check 권장 수치: Harness-Bench 76.2/52.4/23.8pt(Greyling 2차 인용), context collapse 18,282→122 tokens, multi-agent 90.2%/15x token, sandboxing 84%, auto-mode 93%/17%FN, code-exec MCP 98.7%.
- Tensions 4종 반드시 균형 서술: ①서브에이전트 read/write 축 ②GAN 비유 한계 ③harness 가치 감쇠 ④context file 과다 역효과.
- 보고서 위치: research root 의 00~07 .md. analysis_project/paper·code 없음(research-only, 정상).
- 산출물 이관 예정(draft_directives §8): 본 폴더를 `~/.claude/.claude_reports/research/` 로 승격 이관.

관련: [[agent_engineering_survey]] [[code_resources_map]]
