# post-it

> 본 README 는 `SKILL.md` 의 GitHub 표시용 mirror. 권위 있는 동작 명세는 `SKILL.md`.

## 개요

사용자가 **직접 통제하는** _임시 포스트잇_ 메모리. `~/.claude/projects/*/memory/`의 자동 메모리와 별개 layer로, 사용자가 명시적으로 `/post-it` 명령을 호출할 때만 변경된다. 세션 종료 시 conversation이 사라지는 휘발성을 메우는 목적.

**핵심 비유 — 포스트잇.** post-it 은 영구 기록이 아니다. 영구 진실은 산출물(`plans/`·`documents/`·`spec/`·code·git)·구조화 프로필(`user_profile/`)에 있고, post-it 은 그 사이를 잇는 휘발성 작업면. 산출물로 _졸업_ 하면 떼어낸다.

> **불변식 — 사용자는 post-it 을 읽지 않는다.** Claude 의 세션-간 연속성 작업면이지 사용자 읽기용 문서가 아니다. lean 유지·prune 은 Claude 책임 (사용자에겐 한 줄 요약만).

## 생애주기 (모든 엔트리는 졸업하거나 만료)

| 상태 | 의미 | 처리 |
|---|---|---|
| **graduated** | 산출물·구조화 절에 영구 반영됨 | 제거 (`sweep`/`promote`) |
| **stale** | 오래된 `[in-progress]`·끝난 hint | 제거 (`sweep`/`resolve`) |
| **live** | post-it 에만 있고 유효 | 유지 |

## Scope — project vs user

| Scope | 위치 | 갱신 경로 |
|---|---|---|
| `project` (default) | `.claude_reports/post-it.md` (legacy `memo.md` 자동 read) | `/post-it` — 글로벌 CLAUDE.md 도메인 트리거로 세션 시작 Read |
| `user <aspect>` | `~/.claude/user_profile/0X_*.md` 의 `## 사용자 수동 메모` 절 | `/post-it --scope user <aspect>` — analyze-user 사이 상시 수동 채널 |

## 파일 형식 (5 카테고리)

```markdown
# Project Post-it

- **Project**: {프로젝트 이름}
- **Last Updated**: YYYY-MM-DD

## Conventions
- (영속 규약 — 노션 위치, 커밋 메시지 언어 등)

## External Resources
- (외부 링크/경로 — 데이터셋, Overleaf 등)

## Open Threads
- [in-progress YYYY-MM-DD] (진행 중 작업 — 날짜 = 추가·갱신 시점)
- [blocked YYYY-MM-DD] (사용자 수동 편집)

## Decisions
- YYYY-MM-DD: (그 시점 의사결정과 사유)

## Next Session Hints
(가장 마지막 `/post-it handoff` 결과로 **덮어쓰여짐** — 누적 X)
- (다음 세션에 알아야 할 진행 상황·다음 할 일·주의사항)
```

## Sub-Actions

| 명령 | 동작 | Confirm |
|---|---|---|
| `/post-it` (또는 `show`) | 표시 (`post-it.md` → 없으면 legacy `memo.md`; 둘 다 없으면 init 안내) | — |
| `/post-it init` | `.claude_reports/post-it.md` 템플릿 생성 (legacy `memo.md` 있으면 이전 제안) | — |
| `/post-it add <category> <text>` | 섹션 bullet 추가. category ∈ {convention, resource, thread, decision} (alias conv/res/th/dec). thread→`[in-progress YYYY-MM-DD]`, decision→`YYYY-MM-DD:` 자동 | **즉시** (`--confirm`) |
| `/post-it resolve <hint>` | Open Threads fuzzy 매칭 제거 | preview→confirm (`--no-confirm`) |
| `/post-it decide <text>` | Decisions 추가 | **즉시** (`--confirm`) |
| `/post-it sweep` | 산출물(`plans`·`documents`·`spec`·git)과 대조 → graduated·stale **prune** | 수동 호출 preview→confirm / 자동(nudge) 확실분 자동+한 줄 보고 |
| `/post-it promote [--scope user <aspect>]` | `## 사용자 수동 메모` 의 안정 항목을 구조화 aspect 절로 졸업 후 manual 제거 | preview→confirm |
| `/post-it handoff [--no-confirm]` | sweep 먼저 → conversation review → 5-10 bullet 요약 → Next Session Hints **전체 교체** | preview→confirm (`--no-confirm`) |

## Confirm 원칙

사용자가 직접 적은 텍스트(add/decide)는 즉시; Claude 가 만들거나 매칭·분류·졸업(resolve/sweep/promote/handoff)하는 건 검토. 단 _사용자는 post-it 을 안 보므로_ 자동 nudge 자리의 sweep 은 확실분만 자동 prune + 한 줄 보고 (줄 단위 검토 강요 X).

## 간결성 원칙 (post-it.md 작성 시 강제)

세션 시작 시 항상 읽히는 컨텍스트 — **짧고 dense하게.**
- 한 bullet = 한 줄 (최대 2줄). 명사구·사실 문장. 약어·기호(`→`,`&`,`vs`) 적극.
- 같은 정보는 한 카테고리에만. Open Threads는 `[상태 YYYY-MM-DD]` 필수, Decisions는 `YYYY-MM-DD:` 필수.

## What this skill is NOT

- **자동 메모리 시스템 대체 X** — post-it 은 store 의 _working tier 사람-편집 자리_(`mem recall` 한 면에서 검색). 하네스 auto-memory(`projects/*/memory/` → store durable mirror)와 역할이 다르다. `/post-it` alias 유지(spec D-2).
- **영구 기록 X** — 포스트잇. 영구 진실은 산출물·코드·git·구조화 프로필. 졸업하면 뗀다.
- **코드/문서 변경 기록 X** — `autopilot-code` plans/ · `autopilot-draft` documents/.

## Auto-memory와의 경계

store 단일소스 모델에서 두 경로는 같은 store 의 다른 면이다.

| 경로 | store 위치 | 갱신 |
|---|---|---|
| `~/.claude/projects/*/memory/` (하네스 auto-memory write 면) | SessionEnd `mem sync` → store **durable** mirror | 하네스 자동 write → sync |
| `.claude_reports/post-it.md` (store working cwd 면) | SessionEnd `mem sync` → store **working** mirror | 사용자가 `/post-it`로만 |

이 레포에만 적용되는 사실 → post-it.md / 사용자·일반 작업 선호 → durable auto-memory 또는 `--scope user`. `mem recall` 이 양쪽을 한 면에서 검색.
