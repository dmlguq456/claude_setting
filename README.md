# Claude Setting

> Source: `~/.claude/skills/*/SKILL.md` + `~/.claude/agents/*.md` (`/sync-skills` 자동 갱신 — 직접 편집 금지)
> Notion 대문: [Agents/Skills](https://www.notion.so/34987c2bb75380d68df4d6ce4d469bff)  ·  운영 가이드: [`notion_guide.md`](notion_guide.md)

---

## 🗣️ 사용 방식 — 자연어로 부르면 알아서 컨펌받고 진행

세부 옵션을 외울 필요 없음. 작업 의도를 자연어로 말하면, 메인 Claude 가 컨텍스트 (cwd / `.claude_reports/` 산출물 / 사용자 발화) 를 보고 적절한 skill + 옵션 + task description 을 짜서 **자연어 한 줄 요약으로 컨펌**을 받습니다. yes 한 마디면 invoke.

### 자연어 발화 예시

| 사용자 발화 | 메인 Claude 컨펌 (자연어 요약) |
|---|---|
| "ICML camera-ready 마무리 도와줘" | autopilot-draft paper 모드로 camera-ready 본문 다듬기 (qa standard) |
| "이 에러 디버그해봐" | autopilot-code debug 모드로 root-cause 분석 + 수정 (qa light) |
| "diffusion 분야 최근 동향 조사해줘" | autopilot-research academic 모드, depth medium, 최근 1년 (qa light) |
| "이 문서 v2 로 정리" | autopilot-refine major-level (qa quick, 자동 apply) |
| "X 기능 새로 만들어줘" | autopilot-code dev 모드로 plan→execute→test→report (qa standard) |
| "이번 발표 자료 만들어줘" | autopilot-draft presentation 모드로 슬라이드 markdown 작성 (qa standard) |

컨펌 받은 뒤 yes / 수정 요청 ("qa thorough 로", "X 빼고") / cancel 중 선택. 답 없으면 10-30 분 후 추천대로 자율 진행.

ceremony 큰 갈래 (`autopilot-code` / `autopilot-draft` / `autopilot-research` / `autopilot-refine`) 4 개만 컨펌 의무. `audit` / `notes` / `analyze-project` 같은 가벼운 갈래는 컨펌 없이 그냥 invoke. 상세 룰은 글로벌 [`CLAUDE.md`](CLAUDE.md) §6.

### 직접 slash 입력도 그대로

세부 옵션을 명시하고 싶을 때 / 매번 컨펌이 거추장스러울 때는 slash command 그대로 입력:

- `/autopilot-code --mode dev --qa standard "<task>"`
- `/autopilot-draft --mode paper --user-refine "<task>"`
- `/autopilot-research <topic> --mode academic --depth deep`

직접 입력 시 의도 명시로 간주 → 컨펌 skip 하고 즉시 invoke. 세부 옵션은 각 SKILL.md 의 `## Usage` 섹션 참조 (아래 Skills 표의 링크).

---

## 📊 워크플로우 큰 그림

> Claude 는 프로젝트 루트에서 실행. `.claude_reports/` 는 현재 dir 에 생성. cross-project 는 `cd <other>` 후 별도 세션. 외부 `--refs` flag 없음 — 모든 입력은 `.claude_reports/` 영속 산출물에서 자동 발견.

```mermaid
flowchart LR
    ANA["analyze-project<br/>(code/paper/doc)"]
    RES["autopilot-research"]
    CODE["autopilot-code"]
    DOC["autopilot-draft"]
    REF["autopilot-refine<br/>(doc + research 정정)"]
    AUD["audit<br/>(모든 산출물 점검)"]
    ANA --> CODE
    ANA --> DOC
    RES --> CODE
    RES --> DOC
    RES --> REF
    DOC --> REF
    RES --> AUD
    DOC --> AUD
    CODE --> AUD
    AUD -.->|auto-fix doc/research| REF
    AUD -.->|auto-fix plans| CODE
```

5 카테고리:

- **A. 사전 조사 & 분석** — `analyze-project` (code/paper/doc) / `autopilot-research` (외부 분야 조사)
- **B. 코드 개발 & 디버그** — `autopilot-code` (dev/debug)
- **C. 문서 작성** — `autopilot-draft` (paper/presentation/doc, markdown 만)
- **D. 사후 점검** — `audit` (다각도 점검 + 기본 auto-fix chain)
- **E. 사후 정정** — `autopilot-refine` (doc/research major-level ceremony)

> **3-tier 산출물 컨벤션** ([CONVENTIONS.md §5](CONVENTIONS.md#5-skill-output-convention-3-tier-t1t2t3)): T1 root = 메인 산출물 / T2 named subdir = 검토 자료 / T3 `_internal/` = audit·raw·versions. 사용자는 보통 T1 만 보면 됨.

산출물 위치 / scope 경계 / 자주 빠지는 함정은 글로벌 [`CLAUDE.md`](CLAUDE.md) "Drift-Free Essentials" 섹션.

---

## 📋 Skills

| Skill | 역할 |
|---|---|
| [`analyze-project`](skills/analyze-project/SKILL.md) | code/paper/doc 자료 → `analysis_project/` 영속화 |
| [`autopilot-research`](skills/autopilot-research/SKILL.md) | 분야 조사 — mode 별 보고서 (academic/technology/market) |
| [`autopilot-code`](skills/autopilot-code/SKILL.md) | 코드 dev/debug — plan → execute → test → report |
| [`autopilot-draft`](skills/autopilot-draft/SKILL.md) | 문서 strategy + draft (paper/presentation/doc, markdown 만) |
| [`autopilot-refine`](skills/autopilot-refine/SKILL.md) | doc/research 사후 정정 — major ceremony, prompt + memo 통합 entry |
| [`audit`](skills/audit/SKILL.md) | 산출물 multi-aspect 점검 + 기본 auto-fix chain |
| [`notes`](skills/notes/SKILL.md) | per-project 메모 — `.claude_reports/NOTES.md` 단일 파일 |
| [`sync-skills`](skills/sync-skills/SKILL.md) | 본 README + 노션 대시보드 동기화 |

> sub-skill (`init-plan`, `refine-plan`, `init-doc-strategy`, `refine-doc`, `execute-plan`, `run-test`, `final-report`) 은 autopilot 내부에서 자동 호출. 사용자가 직접 부르지 않음.

세부 옵션 (`--mode`, `--qa`, `--from`, `--user-refine` 등) 은 각 SKILL.md. QA 5단계 단일 정의는 [`CONVENTIONS.md`](CONVENTIONS.md) §1.

---

## 🤝 Agents

| Agent | 모델 | 역할 |
|---|---|---|
| [기획팀](agents/plan-team.md) | opus | 구현 plan 문서 작성·갱신 (source code 기반 step-by-step) |
| [품질관리팀](agents/qa-team.md) | opus (light: sonnet) | 코드/문서/plan diff 리뷰 — 구조적 한국어 feedback (🔴/🟡/🟢) |
| [연구팀](agents/research-team.md) | opus (fact-check: sonnet) | user proxy — paper knowledge + 도메인 cross-check + audit-aligned axes |
| [테스트팀](agents/test-team.md) | opus | graduated verification tests (syntax → import → smoke → functional → integration) |
| [탐색팀](agents/browser-team.md) | sonnet | Playwright fetch (paywall/SPA) + PDF figure 추출 + reference 그림 |
| [codex-review-team](agents/codex-review-team.md) | Codex CLI (GPT-5) + opus orchestrator | 외부 hostile reader 관점 review (`--qa adversarial` 자동) |
| [개발팀](agents/dev-team.md) | sonnet | refactor / rename / cleanup — 기능 보존 우선 |
| [편집팀](agents/editorial-team.md) | opus | 사용자 영역 문서 점검·수정 (옮기기 / 다듬기 / 점검만) |

**직접 호출** — 작은 작업 / 단발성 검토는 `Agent(개발팀)` / `Agent(품질관리팀)` / `Agent(연구팀)` / `Agent(편집팀)` 등으로 autopilot 우회. plan/log 가 안 남으므로 추적 필요한 작업은 autopilot 으로.

> Notion 작업은 sub-agent 위임 X (MCP 도구 접근 제약). 메인 Claude 가 `mcp__claude_ai_Notion__*` 직접 호출 — [`notion_guide.md`](notion_guide.md).

---

## ⚙️ 운영 룰

자동 호출 패턴은 글로벌 [`CLAUDE.md`](CLAUDE.md) 가 단일 source of truth:

- **§6 autopilot-\* 호출 패턴** — 옵션 자동 구성 + 자연어 요약 컨펌 + §5 자율 진행 적용
- **도메인 트리거 표** — Notion 작업 / doc·research major-level 수정 / QA·model invariant 작업 / 세션 시작

skill 별 세부 trigger 신호 (예: autopilot-refine 의 3-criteria) 는 각 SKILL.md `## Default Invocation Rule` 섹션 — `/sync-skills` 자동 동기화.

---

## 🔁 동기화

- `/sync-skills` — 본 README + 노션 대시보드 갱신
- `/sync-skills --check` — drift 확인만

GitHub: [dmlguq456/claude_setting](https://github.com/dmlguq456/claude_setting)
