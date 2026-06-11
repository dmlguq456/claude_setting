# Figure Index — 에이전트 엔지니어링 매뉴얼

> 신규 도식 F1~F7 (자료팀 figure-gen, 2026-06-11) + 재인용 F8~F9.
> 재현 script: `gen_figures.py` (Noto Sans CJK KR · DPI 200). 실행: `/home/Uihyeop/anaconda3/envs/SS/bin/python gen_figures.py`
> embed 규칙: 문서 본문에서 `<img width=500>` (미리보기 수준).

| # | 파일명 | 형태 | 소속 절 | 캡션 | ground truth |
|---|---|---|---|---|---|
| **F1** | `f1_generations_timeline.png` | 단방향 레인 (좌→우) | 1.0 | prompt → context → harness → loop: 각 세대는 이전 세대의 미해결분을 흡수하며 누적 layer 로 쌓인다 (loop⊃harness⊃context⊃prompt) | research `analysis_summary.md` §1 Gen0~3 · §4 timeline |
| **F2** | `f2_pattern_generation_matrix.png` | 매트릭스 (heatmap) | 1.4 | 11 실무 패턴이 어느 세대에서 파생했나 — maker-verifier(P3)는 harness·loop 두 갈래에서 수렴 | `analysis_summary.md` §1 세대 · §2 패턴 출처 |
| **F3** | `f3_safety_layers.png` | 단방향 레인 (상→하) | 1.4 / 2부 다리 | 자율 실행 안전장치 4층 (permission→classifier→sandbox→hook) — 자율성 ↑ 일수록 hard boundary 로 무게 이동 (93% 승인 / 17% FN / 84% prompt 감소) | research `05_deployment.md` §1 |
| **F4** | `f4_four_track_pipeline.png` | 단방향 레인 (좌→우, 4 레인) | 2.1 | 문서 / 연구·실험 / 앱 / 라이브러리·CLI — research→spec→code 하드 순서 게이트 (artifact-guard.sh 가 생성 순서 강제) | `~/.claude/CLAUDE.md` 워크플로우 맵 · 하드 순서 게이트 |
| **F5** | `f5_team_matrix.png` | 매트릭스 (heatmap) | 2.2 | 8 팀 × 역할 — maker(기획팀·개발팀) vs verifier(품질관리·연구·편집·디자인·자료·codex-review) 분리 | `~/.claude/CONVENTIONS.md` §2 model 매트릭스 · §1.1 QA |
| **F6** | `f6_loop_layers.png` | 단방향 레인 (상→하) | 2.5 | L1 에이전트(초) → L2 과제(분) → L3 작업(일·당직/일지) → L4 메타(주·모의훈련/연수) | `~/.claude/loops/README.md` 계층 표 |
| **F7** | `f7_daily_flow.png` | 단방향 레인 (좌→우) | 3.1 | 새벽 cron (일지 05:03 · 당직 05:37) → 아침 처리 → 작업 디스패치 → 지침 수정 후 모의훈련 → 일요일 연수(06:17) | `loops/README.md` 현역 4종 cron 시간표 |
| **F8** | `../../../research/agent-engineering-principles/figures/arxiv-agentic-context-engineering_fig2.png` | 재인용 (기존 PNG) | 1.1 | monolithic rewrite 시 context 가 18,282→122 tokens 로 붕괴 (ACE context collapse) | arXiv 2510.04618 fig2 |
| **F9** | `../../../research/agent-engineering-principles/figures/arxiv-inside-the-scaffold_fig1.png` | 재인용 (기존 PNG) | 1.2 | 13 OSS coding agent 의 3 layer × 12 dimension scaffold taxonomy | arXiv inside-the-scaffold fig1 |

## 디자인 결정 (feedback memory 준수)

- **edge 교차 회피**: F2(패턴×세대)·F5(팀×역할) = many-to-many → 노드-엣지 금지, 매트릭스 heatmap. F1·F3·F4·F6·F7 = 파이프라인·계층 → 단방향 레인 (좌→우 또는 상→하, 역방향·교차 화살표 없음).
- **palette**: user_profile 01 역할색 차용 — prompt=gray / context=blue(#4472C4) / harness=green(#548235) / loop=orange(#ED7D31), novelty red=#C00000, hook gold=#FFC000.
- **한글 폰트**: Noto Sans CJK KR (`/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`).
- **`↻` 글리프 폴백**: F4 의 반복 표시 `↻` 가 Noto Sans CJK 에 없어 □ 깨짐 발생 → `(반복)` ASCII 라벨로 교체 후 재렌더.

## 자가검증 결과 (각 PNG Read 도구로 렌더 확인)

- F1: 통과 — 단방향 좌→우, 누적 layer 스택 정상, 한글 OK, 텍스트 잘림/겹침 없음.
- F2: 통과 — 순수 heatmap(edge 없음), ●/○ 표식 명확, P3 가 harness·loop 두 칸 ● 수렴 가시화, 한글 OK.
- F3: 통과 — L1→L4 단방향 하향, 정량 수치(93%/17%FN/84%) 우측 주석 잘림 없음, 한글 OK.
- F4: 통과 — `↻`→`(반복)` 교체로 □ 깨짐 해소, 4 레인 단방향 좌→우, 화살표 교차 없음, 한글 OK.
- F5: 통과 — 팀 8 × 역할 4 heatmap, maker/verifier 분리 가독, 한글 OK.
- F6: 통과 — L1→L4 단방향 하향, 루프 호칭 병기, 주기 축 라벨 잘림 없음, 한글 OK.
- F7: 통과 — 6단계 단방향 좌→우, 화살표 교차 없음, cron 시간표 표기 정상, 한글 OK.
