---
type: factcheck
round: 2
date: 2026-06-11
mode: report
target: strategy/strategy.md
scope: |
  (1) round_1 🔴 4건 수정 결과 검증
  (2) 신규 클레임 정확성 (Risk CLAUDE.md drift 서술, Style Guide 루프 호칭 줄, 표 4.2~4.4 수정 행)
  (3) 잔여 spot-check (worklog prd.md 절 번호, notes/ 실물 구조, CONVENTIONS §5.10·WORKFLOW §7 표기)
---

# Strategy Fact-Check Round 2

| # | Section | Claim | Source (file:line or section) | Match | Source type | Severity |
|---|---|---|---|---|---|---|
| R1 | §4.2 표 4.2a P6 / §4.3 표 4.3a 모의훈련 발사 / Style Guide 루프 호칭 | "모의훈련(drill)" + `drill/run.sh` + `notes/oncall/` — round_1 #21·#24·#30·#22 수정 결과 | `loops/README.md` 현역 표 (실명 `drill/`, `oncall`) + `ls ~/.claude/loops/` (drill/ 존재 확인) + `ls notes/oncall/` (실재) | ✅ | live-file-verified | 🟢 |
| R2 | §7 Risk "라이브 출처 간 내부 명칭 drift" | "글로벌 `~/.claude/CLAUDE.md` 가 구명(당직 `scout`·모의훈련 `golden`·`notes/scout/`·`loops/golden/run.sh`) 표기를 유지 중인 반면" | `~/.claude/CLAUDE.md` 실물: `drill/run.sh`, `notes/oncall/`, `drill g3`, `루프 호칭: 당직=oncall·모의훈련=drill` — 구명 표기 없음 | ❌ | live-file-verified | 🔴 |
| R3 | Style Guide 루프 호칭 줄 | "글로벌 CLAUDE.md 의 구명 `scout`/`golden`(및 `notes/scout/`·`loops/golden/run.sh`)은 인용하지 않는다 — `loops/README.md` 실명이 진실" | `~/.claude/CLAUDE.md` 실물: 구명 `scout`/`golden` 없음 → drift 자체가 해소됨. 이 Style Guide 줄은 이미 해소된 drift 에 대한 안내로 draft 에서 불필요 | 🟡 (내용 틀림 아니나 근거 소멸 — draft 에서 삭제 가능) | live-file-verified | 🟡 |
| R4 | §4.2 표 4.2a P3 | "Stage D.5 편집팀 polish (2026-06-11 신설)" | `autopilot-draft/SKILL.md` line 808: `### Step 5.5: Editorial polish` — 실명은 "Step 5.5", strategy 표기 "Stage D.5" 는 비실물 명칭 | 🟡 | live-file-verified | 🟡 |
| R5 | §4.2 절 구성 2.2 / directive §4 | "Stage D.5 편집팀 polish — 2부 2.2 에 반영" (3건 동일 표기) | 동상 (SKILL.md Step 5.5 vs strategy Stage D.5) | 🟡 | live-file-verified | 🟡 |
| R6 | §4.4 표 4.4a Layer 1 | "`worklog-board/spec/prd.md §2` 2-Layer · `§2.1`(task)·`§2.2`(project)" | `prd.md` line 75: `### 2.1 할일 카드 (kind: task)`, line 117: `### 2.2 과제 카드 (kind: project)`, line 48: `## 2. 데이터 모델 — 2-Layer 아키텍처` — 절 번호 일치 | ✅ | live-file-verified | 🟢 |
| R7 | §4.4 표 4.4a Layer 2 | "`prd.md §2`·`§4` autopilot-note 흐름 · `§2.3`(backbone)" | `prd.md` line 162: `### 2.3 기술 카드 (kind: tech)` (tech card → Layer 2 backbones), line 542: `## 4. autopilot-note skill` — §2.3·§4 절 번호 일치 | ✅ | live-file-verified | 🟢 |
| R8 | §4.4 표 4.4a 연결 다리 | "`card_id`(→L1) + `backbone_ids`·`task_ids`·`paper_id`(→L2)" | `notes/_layer2/notes/.gitkeep`: `# backbone_ids: [sr-corrnet]`, `# task_ids: [sep]`, `# paper_id: tf-restormer-icml2026` — 필드명 verbatim 일치 | ✅ | live-file-verified | 🟢 |
| R9 | §4.4 표 4.4a 부속 | "`notes/digests/` · `notes/oncall/` · `notes/_triage/`" | `ls notes/`: digests/ + oncall/ + _triage/ 모두 실재. 단 strategy 표기에 `notes/_triage/` 인데 실물 경로는 `notes/_triage` (최상위 디렉터리) — 일치 | ✅ | live-file-verified | 🟢 |
| R10 | §5.2 라이브 파일 목록 | "`notes/` (cards 82·_layer2 4종·digests·oncall·_triage)" | `ls notes/cards/ \| wc -l` = 82. `ls notes/_layer2/` = backbones/notes/papers/tasks (4종). digests/oncall/_triage 실재 | ✅ | live-file-verified | 🟢 |
| R11 | §4.2 표 4.2a P7 | "`CONVENTIONS.md §3` invariant 6 (의도 동반·drill 케이스가 최상위 보존)" | `CONVENTIONS.md §3` line 6번째 invariant: "의도 동반 (2026-06-11)" + "의도의 최상위 보존 형태는 drill 케이스" — invariant 6 번호·내용 일치 | ✅ | live-file-verified | 🟢 |
| R12 | §4.2 표 4.2a P3 | "`CONVENTIONS.md §1.1` QA 5단계 · `§3` invariant 2" | `CONVENTIONS.md §3` invariant 2: "adversarial 정의는 반드시 thorough + 1× codex-review-team" — 번호·내용 일치. §1.1 = QA Levels 절 (`## §1. QA Levels`) — 일치 | ✅ | live-file-verified | 🟢 |
| R13 | §4.2 표 4.2a P10 | "`CONVENTIONS.md §5.10` job 레지스트리 (`.dispatch/jobs.log`)" | `CONVENTIONS.md §5.10` line ~404: `.dispatch/jobs.log` append 의무 + "당직 7호가 고아 job 감시" — 일치 | ✅ | live-file-verified | 🟢 |
| R14 | §5.2 라이브 파일 목록 | "`~/.claude/WORKFLOW.md` §7(사후 수정)" | `WORKFLOW.md` line 121: `## 7. 사후 수정 라우팅 — spec-backed 프로젝트` — §7 실재 | ✅ | live-file-verified | 🟢 |
| R15 | §4.3 표 4.3a / §4.2 표 4.2a P3 | "`CONVENTIONS.md §5.10` 규칙 3 (self-merge 금지, 머지 신호/수확 자리만)" | `CONVENTIONS.md §5.10` (line ~387~): merge 정책 실재 확인. "규칙 3" 번호는 §5.10 내부 번호 체계 — 절 내 순서로 추론된 것. 명시적 "규칙 3" 라벨은 확인 안 됨 (🟡). | 🟡 | live-file-verified | 🟡 |
| R16 | §7 Risk "CLAUDE.md drift" 서술 전반 (Style Guide 루프 호칭 줄) | Strategy 가 loops/ 실명 혼용 방지 지침으로 "CLAUDE.md 구명 인용 금지"를 두는데, CLAUDE.md 는 이미 신명으로 수정됨 | round_1 이 발견한 불일치의 원인(CLAUDE.md 구명)이 수정돼 사라짐 — Risk 항목 자체가 이미 해소됐으나 strategy 는 여전히 현재형 drift 로 서술 | ❌ (동일 사유 R2) | live-file-verified | 🔴 |

---

## 요약

**🔴 수정 필요 (2건)**:
1. **R2 / R16** — Risk §, Style Guide 루프 호칭 줄: "CLAUDE.md 가 구명(scout/golden) 표기를 유지 중" 서술이 사실과 다름. 2026-06-11 기준 `~/.claude/CLAUDE.md` 는 이미 drill/oncall 으로 수정 완료. draft 에서 이 Risk 항목 및 Style Guide "구명 인용 금지" 줄을 "이미 해소된 사례" 로 재서술하거나 삭제 요망. memo 삽입 완료 (strategy.md line 288 부근).

**🟡 Caveat (3건)**:
- **R3** — Style Guide 루프 호칭 줄: 근거(CLAUDE.md 구명 drift)가 소멸됐으므로 draft 에서 삭제 가능. 오류는 아님.
- **R4 / R5** — "Stage D.5" 표기: autopilot-draft/SKILL.md 실명은 `Step 5.5`. draft 에서 라이브 anchor 표기인 `Step 5.5` 사용 권장. memo 삽입 완료.
- **R15** — "§5.10 규칙 3" 번호 라벨: §5.10 내부에 "규칙 1/2/3" 명시 라벨 확인 못함 — 순서 번호 추론. 🟡.

**Round 1 🔴 4건 수정 확인 (✅)**:
- #21 (모의훈련 golden→drill): ✅ 수정됨
- #22 (notes/scout→notes/oncall): ✅ 수정됨
- #24 (golden 모의훈련→모의훈련(drill)): ✅ 수정됨
- #30 (golden/run.sh→drill/run.sh): ✅ 수정됨

**수치·절 번호·실물 구조 (✅)**:
prd.md §2/§2.1/§2.2/§2.3/§2.5/§4 절 번호 일치. notes/ 실물(cards 82·_layer2 4종·digests/oncall/_triage) 일치. backbone_ids·task_ids·paper_id 필드명 verbatim 일치. CONVENTIONS §3 invariant 2/6 번호·내용 일치. WORKFLOW §7 실재 확인.
