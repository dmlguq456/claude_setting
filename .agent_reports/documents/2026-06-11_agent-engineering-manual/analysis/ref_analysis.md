# Ref Analysis — 에이전트 엔지니어링 매뉴얼

> research artifact 자체가 이미 정제된 분석(taxonomy·deep dive·citation map)이므로 여기서는 _매뉴얼 4부 구성으로의 매핑_ 과 서술 시 주의점만 정리한다. 원칙·수치·verbatim 의 ground truth 는 `research/agent-engineering-principles/cards/` 단일 출처.

## 1. 4부 구성 ↔ 근거 매핑

### 1부 — 원칙의 세대사 (업계 원칙 망라)
- 골격: `06_implementation.md` §1 outline 그대로 (1.0 들어가며 → 1.1 context → 1.2 harness → 1.3 loop → 1.4 패턴 11종 + Tensions → 1.5 2부 다리 절).
- 핵심 프레임: 세대는 대체가 아니라 **누적 layer** (loop⊃harness⊃context⊃prompt).
- 패턴 11종: `04_technical_deep_dive.md` 의 문제→verbatim→메커니즘→정량→반론 구조 유지. P8(상태 영속성) 안에 **산출물 기반 소통 원칙** 정식 등재 (directive §2).
- 서술 강도 규칙 (`04` Takeaway): P1–P8·P11 단정 서술 가능 / P7(자동화)·P9·P10 은 tier 3/4 caveat 동반 / Tensions ①(서브에이전트 read/write 축)·④(context file 과다)는 반론 균형 필수.
- 정량 수치는 카드 명시값만 (90.2% / 15배 / 98.7% / 85% / 84% / 93% / 23.8pt / −73% / +20% 등). Harness-Bench 수치는 Greyling 2차 인용임을 명시.
- 명명 권위 구분: Greyling 은 정리·대중화자 (명명자 아님) — 인용 시 원 출처로 거슬러 표기.

### 2부 — 우리 세팅 매핑 ("그 원칙이 어디에 어떻게 녹아 있나")
- 일관된 질문 (directive §6): "요즘 쏟아지는 에이전트 코딩 원칙들이 우리 세팅에 어떻게 녹아 있나".
- 매핑 축 (원칙 → 실물):
  - P1/P2 (plan·spec 분리) → 하드 순서 게이트 (research→spec→code), artifact-guard.sh, spec-skill-gate.sh + Read 마커
  - P3 (maker-verifier) → 팀 분업 (연구팀/품질관리팀/편집팀/디자인팀 critic·verifier), QA 5단계 (quick~adversarial), Stage D.5 편집팀 polish (2026-06-11 신설)
  - P4 (서브에이전트) → orchestrator=main 고정, read 병렬 / write 브랜치 single-thread (§5.10)
  - P5 (파이프라인 세분화) → autopilot-* 4트랙 파이프, sub-skill 단계 (strategy→refine→draft→refine→finalize)
  - P6 (golden set) → golden 모의훈련 루프 (지침 회귀 테스트, g0 세팅 세금 ~40k)
  - P7 (오답노트) → post-it sweep·졸업, feedback 메모리 → 지침 승격, 당직(scout) 발견 → triage
  - P8 (상태 영속성·산출물 소통) → `.agent_reports` 통신 버스, plan/dev_logs 핸드오프, pipeline_state.yaml 재개, 3-tier (T1 사용자/T3 기계), worklog 2-layer — **한 줄기로 서술** (directive §2)
  - P9 (worktree) → §5.10 본작업 브랜치 강제, 머지 시점 게이트, git-state-guard
  - P10 (headless·cron) → loops 4종 (scout 시간형 / golden 사건형 / note / study), `claude -p` 디스패치 (directive §3 사례), 디스패치 등록부
  - P11 (컨텍스트 절약) → 얇은 CLAUDE.md 부트스트랩, on-demand Read (WORKFLOW·user_profile), skill progressive disclosure
- 작성 시점 라이브 Read 강제 (directive §4) — research 의 우리-세팅 서술이 아니라 현재 파일이 진실.

### 3부 — 입문·실전 가이드 (발화 중심)
- 형식: "이 상황엔 이 발화" — 아침 당직 처리(`당직 처리`), 새 작업 라우팅(트랙별 첫 발화), 병렬 디스패치, 사후 수정(spec-backed cwd), 모의훈련 발사, 연수, post-it handoff.
- 근거: CLAUDE.md 도메인 트리거 표 + WORKFLOW §7 + loops/README 발화 규약. 외부 원칙 인용은 최소 — 실전 절차가 주.

### 4부 — worklog-board 활용 (에이전틱 노트)
- 근거: worklog-board `.agent_reports/spec/prd.md` + `notes/` 실물 (cards/digests/duty/_layer2) + autopilot-note 2-layer 라우팅.
- P8 산출물 소통 줄기의 종착점으로 연결 (directive §2 끝 항목).

## 2. Figure 계획 (directive §1)

| # | 후보 | 형태 | 소속 |
|---|---|---|---|
| F1 | 세대 4단 누적 타임라인 (2024-12~2026-06) | 단방향 레인 | 1부 |
| F2 | 패턴 11종 × 세대 매핑 | 매트릭스 | 1부 |
| F3 | 자율 실행 안전장치 4층 (permission→classifier→sandbox→hook) | 단방향 레인 | 1부/2부 다리 |
| F4 | 4트랙 파이프 구조도 | 단방향 레인 | 2부 |
| F5 | 팀 분업 매트릭스 (팀 × 역할/모드) | 매트릭스 | 2부 |
| F6 | 루프 4계층 (초·분·일·주 — 디스패치/당직/일지/모의훈련·연수) | 단방향 레인 | 2부/3부 |
| F7 | 하루 일과 흐름 (일지→당직→작업→모의훈련→연수) | 단방향 레인 | 3부 |
| F8 | 재인용: ACE context collapse (`figures/arxiv-agentic-context-engineering_fig2.png`) | 기존 PNG | 1부 |
| F9 | 재인용: scaffold taxonomy (`figures/arxiv-inside-the-scaffold_fig1.png`) | 기존 PNG | 1부 |

신규 (F1~F7) 는 자료팀 figure-gen 게이트 경유, edge 교차 회피 (many-to-many 는 매트릭스 / 파이프라인은 단방향 레인), 납품 전 PNG Read 렌더 검수. embed 는 `<img width=500>`.

## 3. 서술 주의점

- 독자는 시스템 설계자 본인 — 배경 설명 최소, lookup 최적화 (절 단위 독립성, 표 anchor). 친절 안내체 금지, 평어·개조식 허용.
- 한국어 본문 + 굳어진 영어 용어 (harness·loop·worktree·headless 등) 그대로. 비표준 약자 첫 등장 시 풀이.
- 매뉴얼은 장기 자산 — 라이브 파일 인용 시 파일 경로·절 번호 anchor 를 명시해 drift 시 추적 가능하게.
- directive §7 (보강 후보 제안)·§8 (이관) 은 draft 본문이 아니라 파이프라인 종료 후 별도 트랙.
