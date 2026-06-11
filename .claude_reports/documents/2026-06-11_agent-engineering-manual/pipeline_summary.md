# Document Pipeline Summary: 에이전트 엔지니어링 매뉴얼

- **Date**: 2026-06-11 | **Mode**: doc (manual / README 확장판 — report 라벨) | **Format-ref**: fallback-generic | **Status**: done (draft v2, polished)
- **User-Refine**: false | **QA**: standard
- **Discovered inputs**: `research/agent-engineering-principles/` (cards 63 + figures 27 + draft_directives 8종)
- **Primary language**: Korean (단일본 — mirror 없음)

## Process Log
| Step | Action | Result | Notes |
|---|---|---|---|
| 0 | Scope Clarification | skipped | task description 충분히 구체적 (4부 구성·독자·톤 명시) |
| 1 | Material Analysis | completed | material_index.md + ref_analysis.md (figure 계획 F1~F9 포함) |
| 2 | draft-strategy | created | strategy/strategy.md — Style Guide 절 확인 |
| 2-QA | draft-strategy 내부 QA r1 | 🔴 6 → fixed | 루프 실명 drift (golden→drill, scout/duty→oncall) — 라이브 직접 대조 후 교정 |
| 3 | Strategy Review (연구팀) | memos 14 | quality 11 (orphan card 9종 등) + factcheck 3 (CLAUDE.md 14:48 갱신으로 drift 서술 근거 소멸 등) |
| 3b | draft-refine (strategy) | refined → v2 | applied 13 / overridden 0. post-refine 검증 🔴 0 |
| 4.0 | Figure 생성 (자료팀) | F1~F7 PNG 7장 | + figure_index.md (F8·F9 재인용). 자가검증 + orchestrator 렌더 검수 (F2·F4) 통과 |
| 4 | Draft Generation (연구팀) | created | draft/draft.md 549줄, figure embed 8 |
| 4b | Post-draft factual detector | ✅ 0/0/0 | card slug 전수 실재 + 정량 수치 전수 카드 일치 |
| 5 | Draft Review (연구팀) | memos 8 | quality 5 (F3 미embed·3.2 발화 예시 등) + factcheck 3 (❌ oncall 항목 번호 1) |
| 5b | draft-refine (draft) | refined → v2 | applied 8 / overridden 0, 596줄·figure 9. post-refine 검증 🔴 0 (🟡 2 advisory) |
| 5.5 | 편집팀 polish (모드 B) | polished | in-place 11건 (판교체·번역체·호흡) |
| 6 | Pipeline Summary | written | 본 파일 |

## Artifacts
- Strategy (KO 단일본): `strategy/strategy.md` (v2, changelog frontmatter)
- Draft (KO 단일본): `draft/draft.md` (v2, 596줄, 4부 30절, 그림 9장)
- Figures: `assets/figures/` (f1~f7 PNG + gen_figures.py + figure_index.md)
- Analysis: `analysis/material_index.md` · `analysis/ref_analysis.md`
- Reviews: `_internal/strategy_reviews/` (round_1 ×2 · research_review ×2 · refine_round_1 ×2) · `_internal/draft_reviews/` (draft_review ×2 · refine_round_1 ×2)
- Versions: `_internal/versions/v1/{strategy,draft}/`

## Decision Points
| Step | Decision | User Response | Action Taken |
|---|---|---|---|
| 2-QA | 루프 명칭 ground truth 충돌 (리뷰어 vs 세션 주입 CLAUDE.md) | auto (라이브 파일 직접 대조) | loops/ 실물 (oncall/note/drill/study) 채택, strategy 교정 |
| 3 | CLAUDE.md 가 세션 도중 (14:48) drill/oncall 로 갱신됨 발견 | auto | strategy 의 "CLAUDE.md drift" 서술 근거 소멸 → 이력형 재서술 |
| 5b | 그림 재번호 (F3 삽입 → 그림 5~9) | auto | 본문 번호 cross-ref 없음 확인 후 진행 |

## 잔여 트랙 (draft directives §5·§7·§8 — draft 본문 밖, 사용자 결정 대기)
- **§5 publish**: 완성본 확정 후 `/home/nas/user/Uihyeop/notes/` 트리로 publish (일지 note 루프가 라우팅). draft 단계라 보류.
- **§7 양방향 보강 제안**: research 발견 → 우리 스킬·지침 보강 후보 actionable 목록 (연수 보고 형식) — 별도 트랙, 미실행.
- **§8 산출물 이관**: research 폴더 + 본 documents 산출물 → `~/.claude/.claude_reports/research/` (스킬셋 repo 승격) — 완료 후 이관, 보류.
