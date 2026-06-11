# Material Index — 에이전트 엔지니어링 매뉴얼 (2026-06-11)

> mode: doc (manual / README 확장판 — 입문서·참조서) · qa: standard
> 독자: 시스템 설계자 본인. 참조서 톤, 친절 안내체 회피.

## 1. Primary input — research artifact

`.claude_reports/research/agent-engineering-principles/` (autopilot-research --mode technology, 2026-06-11)

| 파일 | 내용 | 매뉴얼 사용처 |
|---|---|---|
| `analysis_summary.md` (212줄) | 세대 taxonomy(Gen0~3) + 패턴 11종 + tier 분류표 + tensions 4종 + timeline + gaps | 1부 전체 골격 |
| `04_technical_deep_dive.md` (150줄) | 패턴 11종 각각 문제→verbatim 원칙→메커니즘→정량→반론→매뉴얼 인용 포인트 | 1부 1.4 패턴 카탈로그 1차 근거 |
| `06_implementation.md` (127줄) | 1부 section-by-section outline + argument scaffolding + figure 후보 + citation map + 작성 우선순위(🔴🟡🟢) | strategy 의 1부 설계 직접 입력 |
| `01_landscape.md` / `02_standards.md` / `03_vendor_comparison.md` / `05_deployment.md` / `07_resources.md` | 세대 lineage·표준·벤더 비교·배포 안전장치·자료 목록 | 1부 보조 + 3부 안전장치 절 |
| `cards/` (63장) | 출처별 카드 — tier 1(Anthropic/Osmani/Cognition 등 1차) ~ tier 4(arXiv 보조) | 모든 인용의 단일 ground truth |
| `figures/` (27 PNG + figure_index.md) | arXiv 논문 figure (ACE context collapse, scaffold taxonomy 등) | 1부 재인용 figure |
| `_internal/draft_directives.md` | **세션 누적 지시 8종** (아래 §3) | 파이프라인 전체 구속 |

## 2. Live sources — draft 시점 직접 Read 대상 (2부~4부)

directive §4: draft 는 _작성 시점의_ 라이브 파일을 직접 읽는다 (research 경유 X — stale 방지).

| 파일 | 매뉴얼 사용처 |
|---|---|
| `~/.claude/CLAUDE.md` | 2부 — §0 라우팅·하드 게이트·§1~3 응답 원칙·도메인 트리거 |
| `~/.claude/CONVENTIONS.md` | 2부 — QA 5단계·agent model 매트릭스·3-tier 산출물·§5.10 worktree/디스패치 |
| `~/.claude/WORKFLOW.md` | 2부 — 4트랙 라우팅·spec mode·§7 사후 수정 |
| `~/.claude/loops/README.md` | 2부+3부 — 루프 4종 (scout 당직·note 일지·golden 모의훈련·study 연수) |
| `~/.claude/hooks/*.sh` (6종) | 2부 — artifact-guard·spec-skill-gate·spec-read-marker·git-state-guard·design-postwrite·herdr-agent-state |
| `~/.claude/agents/*.md`, `~/.claude/skills/*/SKILL.md` | 2부 팀 분업 매트릭스 (필요 절만 on-demand) |
| `/home/nas/user/Uihyeop/worklog-board/.claude_reports/spec/` (prd.md·stack.md·design/·ship.md) | 4부 — worklog-board 에이전틱 노트 |
| `/home/nas/user/Uihyeop/notes/` (cards·digests·duty·_layer2) | 4부 — 2-layer 실물 구조 + 5부 publish 대상 트리 |

## 3. Draft directives (8종 — `_internal/draft_directives.md`)

1. 그림 적극 포함 — 자료팀 figure 게이트, edge 교차 회피, PNG 렌더 검수, `<img width=500>` embed
2. 산출물 기반 소통 원칙 강조 — 1부 P8 정식 등재 + 2부 한 줄기 매핑 (`.claude_reports`=통신 버스 → 핸드오프 → pipeline_state 재개 → 3-tier → headless 분사 → worklog 2-layer)
3. headless 디스패치 사례 — Agent 툴 중첩 1단 제한 vs `claude -p` 프로세스 분사 우회 (2026-06-11 실증, §5.10 2모드)
4. 2026-06-11 신설분 반영 — 연수(study) 루프·일지(note) 개명·Stage D.5 편집팀 polish·디스패치 등록부·머지 시점 게이트·g0 세팅 세금(~40k)
5. 완성본 publish — `notes/` 트리 (worklog-board 가 읽는 자리), 일지 루프가 라우팅
6. 망라 원칙 — 1부는 research 발굴 원칙 전체 망라, 사용자 강조 항목은 비중만 키움
7. 양방향 — 스킬·지침 보강 후보 actionable 목록 별도 제안 (draft 와 분리 트랙, 연수 보고 형식)
8. 산출물 이관 — 완료 후 research 폴더 + documents 산출물을 `~/.claude/.claude_reports/research/` 로 이관

## 4. Format spec

`analysis_project/doc/*/formats/` 매치 0 → generic prose fallback (매뉴얼 장르, 기관 template 불요 — 무방).
