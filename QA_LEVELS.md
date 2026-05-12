# QA Levels — Single Source of Truth

> 본 문서가 `--qa` 옵션 5단계의 _공통 정의_(reviewer 구성·model·fact-checker 적용 등)에 대한 **단일 source of truth**.
>
> 각 SKILL.md / README / Notion mirror에서 QA 표를 직접 hard-code하지 말고 _이 파일을 link로 참조_. skill-specific override(default level, max level, fact-checker on/off 등)만 자기 SKILL.md에 명시.
>
> `/sync-skills --check`가 본 정의와 다른 SKILL.md의 표를 cross-doc grep해 drift 보고.

---

## 5단계 공통 정의

| Level | Quality reviewer | Fact-checker (parallel) | Codex (parallel) | 비고 |
|---|---|---|---|---|
| **quick** | 1× sonnet, 1-pass | skip | skip | refine entire skip / loop 1라운드 강제 종료 / 🔴 잔존 시 `unresolved.md`에 기록만 |
| **light** | 1× sonnet, single-pass | skip (quality reviewer가 spot-check 커버) | skip | 경량 리뷰 |
| **standard** | 1× opus, single-pass | 1× sonnet, parallel¹ | skip | _doc/research/refine 한정_ — fact-checker는 cards/PDFs verbatim 대조 (venue/year/metric/citation) |
| **thorough** | 2× opus, parallel (다른 focus²) | 1× sonnet, parallel¹ | skip | 고위험 산출물 (final-version paper draft, public-facing report 등) |
| **adversarial** | 2× opus, parallel (= thorough quality) | 1× sonnet, parallel¹ | 1× `Agent(codex-review-team)` parallel — Codex CLI (GPT-5) external review | _autopilot-code · autopilot-refine 전용_ — autopilot-doc / autopilot-research는 지원 X (thorough까지) |

¹ Fact-checker는 _doc/research/refine 파이프라인_에만 적용. autopilot-code 계열 (init-plan / refine-plan / execute-plan / run-test)은 fact-checker 없음 — code는 ground-truth source가 코드 자신이므로 quality reviewer만 운용.

² thorough에서 2개 quality reviewer는 _다른 axes_ 분담: 예: A=domain expert + methodology / B=content expert + quality / C=safety (in some skills). 각 skill SKILL.md가 자기 axis 분담 명시.

## Codex availability 정책 (adversarial 전용)

- Adversarial 선택 전 `codex --version 2>/dev/null` 실행
- 실패 시:
  - `--qa adversarial` _명시_ 호출 → fail loudly (사용자에게 보고)
  - auto-detect로 adversarial 선택 → Thorough로 silent fallback
- Codex agent는 `adversarial-review --wait --scope auto` 실행 → `_internal/{stage}_reviews/round_{N}_codex.md` 작성

## 모드 forms (autopilot-refine 한정)

autopilot-refine은 `--qa`와 _직교하는_ mode form 별도 보유:
- `"<prompt>"` (default) — 자동 apply
- `--memo <file>` — 별도 메모 파일 일괄 반영
- `--confirm` — 수정 전 chat-pause
- `--review-only` — 점검만 (적용 X)

다른 family skill에는 해당 없음.

## opt-out flags (orthogonal)

- `--no-fact-check` — 모든 level에서 fact-checker 단독 skip (`quick`/`light`는 어차피 skip이라 무의미)
- `--no-style-audit` — Stage B.5 style aspect skip (refine 계열만)

이 두 flag는 `--qa` level 무관하게 적용되며, fact-checker / style audit을 끄는 _유일한_ 메커니즘 (ad-hoc prompt로 무시 불가).

---

## Skill별 사용 매트릭스

| Skill | Supported levels | Default | Adversarial | Fact-checker | 비고 |
|---|---|---|---|---|---|
| `autopilot-research` | quick/light/standard/thorough | `standard` | X | standard+ | thorough max |
| `autopilot-code` | quick/light/standard/thorough/**adversarial** | `standard` | ✓ (dev only; debug는 thorough로 downgrade) | **X** (code는 fact-checker 없음) | adversarial 전용 |
| `autopilot-doc` | quick/light/standard/thorough | `thorough` | X | standard+ | thorough max, default thorough |
| `autopilot-refine` | quick/light/standard/thorough/**adversarial** | `quick` | ✓ | standard+ | adversarial 전용 + default quick |
| `audit` | — | — | — | `--no-fact-check` flag | `--qa` 대신 `--scope` 사용; fact-check는 Stage B.5에서 별도 |
| `init-plan` (sub) | quick/light/standard/thorough/adversarial | auto-detect from scope (plan frontmatter override) | ✓ | X | autopilot-code 내부 |
| `refine-plan` (sub) | quick/light/standard/thorough/adversarial | inherit from plan frontmatter | ✓ | X | autopilot-code 내부 |
| `execute-plan` (sub) | inherit | inherit | inherit | X | autopilot-code 내부 |
| `run-test` (sub) | **forced thorough** (`--qa` 무시) | thorough | auto-upgrade if Codex available | X | 항상 2팀 병렬, Codex 가용 시 자동 상향 |
| `final-report` (sub) | sonnet 1× (level-independent) | — | — | — | 모든 level에서 writer는 항상 sonnet |
| `init-doc-strategy` (sub) | quick/light/standard/thorough | inherit from autopilot-doc | X | standard+ | autopilot-doc 내부 |
| `refine-doc` (sub) | quick/light/standard/thorough | inherit | X | standard+ | autopilot-doc 내부 |

> _Sub-skill_ (init-plan / refine-plan / execute-plan / run-test / final-report / init-doc-strategy / refine-doc): orchestrator가 결정한 `--qa` 값을 그대로 받음. 직접 호출 시는 자체 default 사용.

## Cross-doc invariance — sync-skills `--check`가 강제하는 사항

1. 각 SKILL.md / README / `_notion_mirror`/*에서 위 5단계 정의의 **Quality reviewer / Fact-checker / Codex 컬럼 wording**은 본 문서와 동일해야 함 (사소한 표현 차이는 허용, 의미가 다르면 drift).
2. **adversarial** 정의는 반드시 `thorough + 1× codex-review-team` (자주 잘못 적힌 패턴: `standard + Codex` — _틀림_).
3. autopilot-code의 QA 표에 fact-checker가 적힌 곳이 있으면 drift (code는 fact-checker 없음).
4. `--no-fact-check` / `--no-style-audit`는 autopilot-refine / audit 외 다른 skill에 노출되면 안 됨.

본 문서 자체가 바뀌면 sync-skills `--check`가 `## Skill별 사용 매트릭스`를 기준으로 모든 SKILL.md의 QA 표 wording을 cross-check.

---

*마지막 업데이트: 2026-05-13 — 신규 단일 source 문서 분리. 이전엔 각 SKILL.md / README에 QA 정의가 분산 hard-code되어 drift 발생 (예: README.md와 autopilot-refine/SKILL.md에 `adversarial = standard + Codex`라는 오정의가 한동안 잔존). 다음 sync 시 본 문서를 canonical로 cross-doc scan.*
