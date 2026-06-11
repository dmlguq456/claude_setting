# Research Survey Pipeline Summary: agent-engineering-principles
- **Date**: 2026-06-11
- **Query**: 에이전트 엔지니어링 원칙·패턴 종합 조사 (2025-2026) — 사용자 매뉴얼(README 확장판) 1부 '원칙의 세대사' 근거 자료
- **Mode**: technology
- **Depth**: medium
- **QA**: standard
- **Status**: done
- **From-Stage**: N/A (신규)

## Process Log
| Step | Action | Result | Notes |
|---|---|---|---|
| 1 | Input parsing | keyword query | topic: agent-engineering-principles, mode=technology 명시 |
| 1.5 | Scope clarification | skip | query 충분히 구체적 (범위·목적·seed 명시) |
| 2a | Query expansion | 5 queries | original + 4 variants |
| 2b | HF pre-fetch | 11 papers | paper_search 2회 — arXiv 보조 tier 4 |
| 2c-d | Source search (Agent) | 45 sources | blog 32 / paper 11 / docs 2, URL 전수 WebSearch/WebFetch 검증 |
| 2e | Expansion round | 1 round (+16, 중복 1) | 45 → 61. 갭 보강: headless·worktree·compaction·EDD·spec-driven. medium cap 도달 |
| 3a | Playwright + 자료팀 pre-fetch | 5/5 Medium 전문 추출 | node playwright fallback (python 모듈 부재) |
| 3b | Phase A skimming (Agent ×10 병렬) | 61 cards | full skim: tier 1-2 블로그·docs 전체 + arXiv 3편 / abstract-only: arXiv 12편 |
| 3c | Phase B chaining | skip (intentional) | technology mode 비활성 |
| 3d | Phase C code search | 17 repos | tier 1/2/3 + Quick verify command |
| 3.5 | Figure extraction (자료팀) | 27 figures (3 papers) | ar5iv 3/3 성공 — full-read arXiv 한정 (blog 중심 주제라 대상 축소) |
| 3e | analysis_summary | 212줄 | 세대 4축 + 패턴 11종 + tensions 5 + gaps |
| 4a | Report generation (Agent) | 8 files (technology=7 구조 + analysis_summary) | 00_briefing ~ 07_resources, [card-slug] 인용 체계 |
| 4a' | Editorial polish (편집팀 모드 B) | 8 files in-place | 판교체·번역체 정리, 내용 불변 |
| 4b | QA round 1 (품질관리팀 opus + fact-checker sonnet 병렬) | 🔴 0 / 🟡 9 | quality 🟡4 (권고) + factcheck 🟡5 → 5건 전부 오케스트레이터 직접 패치 (Rust 명시 ×2, Cherny 2차 전언 caveat, Agent=Model+Harness 2차 귀속 caveat, card 연월 2026-06 정정, ~8x 카드 대조 확인) |
| 4c | Status check | pass | 00_briefing.md 존재 |

## Artifacts
- Search: `_internal/search_results.json` (61 sources)
- Cards: `cards/` (61장) + `figures/` (27 PNG + figure_index.md)
- Code: `code_resources/` (tier 1/2/3) 
- Analysis: `analysis_summary.md`
- Reports: `00_briefing.md` ~ `07_resources.md` (technology mode 7-file 구조)
- Reviews: `_internal/reviews/round_1_{quality,factcheck}.md`

## Decision Points
| Step | Decision | Response | Action |
|---|---|---|---|
| 1.5 | Clarification 필요? | query 구체적 → skip | auto-proceed |
| 2e | 추가 라운드? | medium → 1회 | +16 sources 후 cap 종료 |
| 3.5 | Figure 추출 범위 | blog 중심 주제 — arXiv full-read 3편만 | 자료팀 1회 호출 |
| 4b | QA 종료 | 🔴 0 → exit | 🟡 fact 5건은 직접 패치 후 종료 |

## 인용 시 주의 (다운스트림 autopilot-draft 용)
- tier 4 arXiv 카드는 단독 근거 금지 — 블로그 1차 소스의 보조로만.
- Greyling(tier 2) 경유 claim 은 원 출처로 거슬러 귀속 (01_landscape §명명 권위 박스).
- Cherny 슬로건·Agent=Model+Harness 등식은 2차 전언/귀속 — verbatim 인용 시 원문 대조.
