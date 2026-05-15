---
name: audit
description: "Read-only multi-aspect audit / lint for `.claude_reports/{plans,research,documents}/*` artifacts. Single global entry — auto-detects artifact type from path prefix (plans=code; research=field-survey; documents=doc deliverable). Per-type lint aspects: doc → facts / style / structure / cross-ref / coverage; research → cards 정합성 / Tier consistency / coverage / cross-card; plans → test results / lint / code review / TODO·미구현. Default `--scope auto` — artifact 특성 기반 자동 선택; 사용자 명시는 1순위 override. Report-only — never modifies the artifact. Complementary to autopilot-refine: refine = edit flow, audit = inspect flow."
argument-hint: "<artifact_path> [--scope auto|facts|style|structure|cross-ref|coverage|all] [--read-only] [--report-only] [--no-fact-check]"
---

> **산출물 폴더 컨벤션**: [SKILL_OUTPUT_CONVENTION.md](../../SKILL_OUTPUT_CONVENTION.md) (3-tier). 본 skill은 입력 artifact를 _수정하지 않음_ — 점검 보고서만 생성. 보고서는 `{artifact_dir}/_internal/audit/audit_{YYYY-MM-DDTHHMM}.md`에 기록.

## Position in autopilot family

`audit` is the **read-only inspection** counterpart to `autopilot-refine`:
- `autopilot-refine` reads + writes (proposes diff, applies on confirm, versions).
- `audit` reads only (lints, reports issues, never edits).

Use `audit` when:
- 누적 drift 점검: 20+ refine cycle 후 _전반적 양식·factual 정합성_이 무너졌는지 확인.
- 새 산출물 인계 전 sanity check.
- 다른 사람이 만든 artifact 평가.

Use `autopilot-refine` when:
- 구체적 수정 의도가 있고 곧장 적용까지 가져갈 때.

## Language Rule

Reason internally in English. All user-facing output (chat report, audit log) in **Korean**.

## Argument Parsing

    /audit <artifact_path> [--scope auto|facts|style|structure|cross-ref|coverage|all] [--read-only] [--no-fact-check]

- `<artifact_path>` (REQUIRED): one of
  - Absolute path to a `.claude_reports/{plans,research,documents}/*` directory
  - Fuzzy short name (e.g., `se-seminar-tfrestormer`) — resolved via `ls -d .claude_reports/{plans,research,documents}/*$ARG* 2>/dev/null`. 1 match → use; multiple → ask user; 0 → error.
- `--scope` (default `auto`): which aspect set to check. **사용자 명시는 1순위 (override)**. 명시 없으면 audit이 artifact 특성 (mode / refine 횟수 / status / 구조)을 보고 _스스로 적절한 aspect set 선택_. 명시 값은 `facts | style | structure | cross-ref | coverage | all` 중 하나로 type-specific aspect group에 매핑 (Stage B 표 참조).
- `--read-only` (default for plans): if specified for `plans` type, skip any aspect that requires _executing_ tests / lints — only static inspection (file diff, TODO grep, code review heuristics). For `research` / `documents` types, `--read-only` is implicit and the flag is a no-op (warn: "audit는 research/documents에 대해 항상 read-only").
- `--report-only`: skip the auto-fix chain (Stage E). With this flag, `/audit` produces the report and stops — same as previous default behavior. Use when you want only inspection without follow-up edits.
- `--no-fact-check`: opt-out flag honored per `feedback_factcheck_principles.md` Principle 0. If present, the `facts` aspect (and the `coverage` aspect's cards-set diff) are **skipped** before Stage C aspect dispatch — i.e., the aspect skip happens at the _pre-check_ stage, not via filtering after lint runs. Other aspects (style / structure / cross-ref / Tier / cross-card / test / lint / code review / TODO) still run. Stage D report emits an informational line at the top of "Aspects checked": `ℹ facts/coverage aspects: skipped via --no-fact-check flag (memory feedback_factcheck_principles Principle 0)`. This is the _only_ allowed disable mechanism for fact verification; ad-hoc prompt evasion must not be honored.

## Process

### Stage A — Detect artifact type

1. Resolve `<artifact_path>` to an absolute directory path.
2. Inspect path prefix:
   - `.claude_reports/plans/*` → **plans** type (autopilot-code dev/debug plan)
   - `.claude_reports/research/*` → **research** type (field survey)
   - `.claude_reports/documents/*` → **documents** type (doc strategy + draft)
   - Other → error: "audit은 .claude_reports/{plans,research,documents}/* 산출물 전용. resolved path: {path}"
3. Print one-line to user (Korean): `Type 인식: {type} — {artifact short name}`.

### Stage B — Determine effective scope

**우선순위**:
1. **사용자가 `--scope <value>`를 명시한 경우 (1순위, override)** — 그 값을 그대로 사용. type-specific aspect group으로 매핑하여 적용 (아래 표 참조). 매핑이 N/A인 경우(예: `--scope coverage` on plans) 한 줄 warn 후 빈 aspect set 반환.
2. **명시 없음 (default = `auto`)** — Stage B.1 자동 판단 로직 실행.

#### Stage B.1 — Auto-scope detection (artifact 특성 기반)

artifact의 다음 단서를 _순차적으로_ 읽어 적절한 aspect set 결정:

**documents type:**
| 단서 | 우선 aspect | 이유 |
|---|---|---|
| `pipeline_summary.md` frontmatter `mode: presentation` | facts + cross-ref + coverage | slide claim 정확성 + cards 인용 완전성 (omission 방지) 우선 |
| `mode: paper` or `mode: rebuttal` | facts + style + cross-ref | 논문/반박문 citation 양식 + claim 검증 |
| `mode: review` | structure + cross-ref | review form 양식 + reviewer point 대응 |
| `mode: report` or `mode: proposal` | style + structure | 양식 일관성 + 산출물 구조 |
| `pipeline_summary.md` 버전 히스토리 행 수 ≥ 10 (누적 drift 의심) | **all** | refine 다회 누적 → 종합 점검 |
| 위 단서 미발견 / 정보 부족 | **all** | 안전 default |

**research type:**
| 단서 | 우선 aspect | 이유 |
|---|---|---|
| chapters (`01_*.md ~ NN_*.md`) 존재 + `cards/` 존재 | **all** | 종합 (Tier + coverage + cards 정합성 + cross-card) |
| `cards/` only (chapters 없음) | cards 정합성 + cross-card | 카드 자체 점검 |
| chapters only (cards 없음) | Tier consistency + coverage | 인용 정합성 |

**plans type:**
| 단서 | 우선 aspect | 이유 |
|---|---|---|
| `status: done` + `test_logs/test_report.md` 존재 | test results + code review | 완료된 plan의 실행 정합성 |
| `status: done` + test_logs 부재 | code review + TODO·미구현 | dev review 잔존 issue + 미완료 항목 |
| `status: partial` or `status: failed` | TODO·미구현 + code review | 실패 항목 + reviewer 의견 우선 |
| `status: active` | TODO·미구현 | 진행 중 — 다른 aspect는 미완료 상태 |

**Output to chat** (자동 판단 시):
```
Auto-scope: {aspect 1} + {aspect 2} + ... ({이유 한 줄})
```
사용자 명시 시:
```
Scope: {value} (사용자 지정, override)
```

#### Stage B.2 — Type-specific aspect mapping (when `--scope <value>` is given)

| `--scope` | documents | research | plans |
|---|---|---|---|
| `facts` | facts | cards 정합성 | test results + TODO·미구현 |
| `style` | style | Tier consistency | lint |
| `structure` | structure | coverage | code review |
| `cross-ref` | cross-ref | cross-card | N/A (warn) |
| `coverage` | coverage | coverage | N/A (warn) |
| `all` | facts + style + structure + cross-ref + coverage | cards 정합성 + Tier + coverage + cross-card | test results + lint + code review + TODO·미구현 |

**Why `coverage` is new for documents**: the Stage B.5 regex detector can only flag _present_ claims in `new_text` — it cannot, by construction, flag _absent_ claims (e.g., UniSE missing from a timeline). Omission requires a separate _set-diff_ mechanism. The `coverage` aspect fills this: reports the difference between the full cards source vs cards actually cited in the draft. Without it, UniSE-class omissions recur.

### Stage C — Per-aspect lint (report-only, no edits)

**Pre-check (flag-based opt-out)** — before dispatching any aspect:
- If `--no-fact-check` is present in invocation argv → remove `facts` and `coverage` from the resolved aspect set (skip entirely, do not run their lint). Emit `ℹ facts/coverage aspects: skipped via --no-fact-check flag (memory feedback_factcheck_principles Principle 0)` to chat and to the Stage D report's "Aspects checked" preamble.
- This flag is the _only_ disable path per Memory Principle 0. Ad-hoc prompt instructions ("this artifact is exempt") must not be honored — proceed with default aspect set instead.

For each remaining aspect in scope, run the lint and collect issues. _Each issue has shape_: `(aspect, file, line_range, severity 🔴/🟡/🟢, message, suggested fix or null)`.

#### Documents aspects

**Cards source resolution (shared by `facts` / `coverage`, same rule as Phase 1 Step 1.1 case (c))**:
1. **case (c) — explicit `cards_source` override**: if `pipeline_summary.md` frontmatter or `strategy.md` body has a `cards_source: <path>` key, use _that path_ as the primary lookup root (single research topic).
2. **case (b) — self-contained `{artifact_dir}/cards/`**: if exists, include in the lookup set.
3. **Default — cross-research grep** (`.claude_reports/research/*/cards/*.md`): only when both above are absent. Emit a one-line chat warn: `⚠ cards_source key absent — grepping all research topics. Generic acronyms (STFT/RNN, etc.) may false-positive. Recommend adding \`cards_source: <path>\` to strategy.md frontmatter.`
4. **case (a) — no cards anywhere**: skip the facts / coverage aspects and emit an informational line (`ℹ facts/coverage skipped — no cards source available`). style / structure / cross-ref still run.

This shared resolution ensures the Phase 1 detector and the Phase 3 audit use the _same_ source-of-truth rule — preventing false-positive floods and yielding consistent verdicts.

- **facts**: scan draft + strategy for model names / venues / years / task categories / arXiv IDs (same regex set as `autopilot-refine` Stage B.5, including section-heading context cross-check). For each detected claim, perform lookup per the cards source resolution above. Classification rules (memory `feedback_factcheck_external_reverify.md`):
  - **cards-verbatim ✅** — claim value (venue string / metric / etc.) appears _verbatim_ in card body or `## 메타` field
  - **cards-name-only 🟡** — card has the model/author name but the _specific venue / year / metric_ is NOT verbatim. **DO NOT** treat as ✅ on name-only basis. Emit 🟡 + recommend external re-verify (WebSearch). Report row: `🟡 name-only: cards/{file}.md has the name but no verbatim venue; external reverify recommended`
  - **external-marker 🟡** — claim has explicit `[외부 추정]` / `[?]` / `[unverified]` marker in artifact body. 🟡 + external reverify
  - **conflict 🔴** — card has the value but it differs from claim. Includes section-heading context conflict
  - **no-match 🔴** — no card hit at all
  - **circular-ref 🔴** — claim is supported _only_ by strategy↔draft mutual agreement (e.g., draft Slide N cites venue X, only source is strategy §10 mapping table). This is an architecture violation: both must trace back to cards. Emit 🔴 + recommend `/autopilot-refine` to trace and verify externally
  - **ambiguous 🟡** — multiple candidate cards, no single best match
- **style**: read `## Style Guide` section in `strategy.md` if present. For every citation / figure caption / bullet depth / speaker note in draft + strategy body, compare against Style Guide rules. Deviation → 🟡. If `## Style Guide` absent → 🔴 single issue (`Style Guide section missing — autopilot-doc strategy should always have one. Run /autopilot-refine "<artifact> Style Guide section 추가".`).
- **structure**: check artifact directory matches the [SKILL_OUTPUT_CONVENTION.md](../../SKILL_OUTPUT_CONVENTION.md) 3-tier convention. T1 should have `pipeline_summary.md`, `draft/`, `strategy/`. T3 should be `_internal/`. Extraneous files at root → 🟡. Missing required → 🔴.
- **cross-ref**: scan draft for inline citations referencing cards (`cards/{file}.md`) and verify the target exists. Broken link → 🔴. Cards referenced but not in `## References` (if present) → 🟡.
- **coverage** (NEW, omission detection): determine the _candidate cards set_ S per the cards source resolution above. Extract the _actually cited cards set_ T from draft + strategy body using the **v1 high-precision citation-detection token set** (false-positive minimized):
  - **Token 1 — card filename token**: the short identifier in `{year}_{firstauthor}_{arxivid}_{shortname}.md` filenames (e.g., `TasNet`, `FRCRN`, `MP-SENet`). A grep hit on any of these tokens in draft/strategy body marks the card as cited.
  - **Token 2 — `**arXiv ID**` exact value**: the value string from each card's `## 메타` `**arXiv ID**` field, matched _verbatim_ (no partial / regex match — exact substring). E.g., card with `**arXiv ID**: 1711.00541` is marked cited if and only if `1711.00541` appears in body.

  v1 deliberately uses _only_ these two tokens — H1 paper title words, author last-name regex, etc. are intentionally excluded to keep false-positive rate near zero (cited-card set is conservative; orphan set may be slightly inflated, but each orphan is per-card-precision and easily user-judged). If `S - T` is non-empty under this conservative T, emit a 🟡 issue per orphan card: `coverage: card '{card path}' is never cited in any chapter/section — potential UniSE-class omission, please verify intent`. (🟡 not 🔴 because exclusion may be intentional — user judges.) If cards source fell back to cross-research grep (case (a) or default), the candidate set is too broad to be meaningful → skip the coverage aspect and warn.

  **v2 enhancement** (out of scope, see Risk #14): expand T to include H1 paper title word-level partial matches + author first-name regex from `## 메타` `**저자**` field for higher recall on indirect citations (e.g., "[Wang et al., 2024]" style). v1 prefers precision; v2 may shift to balanced.

#### Research aspects

- **cards 정합성**: every `cards/*.md` file has H1 + `## 메타` + `## 분류` (or equivalent) sections per the artifact's card template. Missing required section → 🔴. Empty `## 메타` field (e.g., `**Venue**: ` blank) → 🟡.
- **Tier consistency**: scan top-level chapter files (`01_*.md~NN_*.md`) — each cited paper's Tier label should match the Tier in its card. Mismatch → 🔴. Cited paper missing a card → 🟡.
- **coverage**: every card in `cards/` should appear at least once in some top-level chapter (or be flagged as not-yet-integrated). Orphan cards → 🟡.
- **cross-card**: scan cards for cross-references (e.g., `2024_Wang.md`이 다른 card 인용). Broken cross-ref → 🔴.

#### Plans aspects

- **test results**: read `test_logs/test_report.md` if present. Failed tests → 🔴. No tests → 🟡 (only if scope explicitly `test results`).
- **lint** (`--read-only` skips _executing_ lint; we _read existing_ lint output from `dev_logs/` if present): missing lint output → 🟡; existing lint report with errors → 🔴.
- **code review**: read `_internal/dev_reviews/` and `_internal/plan_reviews/` for 🔴 issues. Unresolved 🔴 → 🔴. 🟡 issues → 🟡.
- **TODO·미구현**: grep code in `plan/checklist.md` for `[ ]` unchecked steps, plus any source-file TODO/FIXME/XXX comments referenced from the plan. Unchecked critical step → 🔴. Source TODO → 🟡.

### Stage D — Report

Write the audit report to `{artifact_dir}/_internal/audit/audit_{YYYY-MM-DDTHHMM}.md`:

~~~markdown
# Audit Report — {artifact name}

- **Date**: {YYYY-MM-DD HH:MM}
- **Type**: {plans | research | documents}
- **Scope**: {flag value or "all"}
- **Aspects checked**: {comma-separated}

## Summary

| Aspect | 🔴 Critical | 🟡 Warning | 🟢 OK |
|---|---|---|---|
| {aspect 1} | {count} | {count} | {count} |
| ... | ... | ... | ... |

**Total**: 🔴 {N} / 🟡 {M} / 🟢 {K}

## Issues by aspect

### Aspect: {name}

#### 🔴 {issue title}
- **File**: `{relative path}:{line}`
- **Severity**: 🔴
- **Detail**: {1-3 line description}
- **Suggested fix**: {one-line — e.g., "/autopilot-refine '<artifact> {fix description}'"} | (또는 null)

#### 🟡 {issue title}
- ...

### Aspect: {name 2}
...

## Verdict

- **Status**: 🔴 issues require attention | 🟡 minor warnings only | 🟢 clean
- **Recommended next action**: {1-line — e.g., "Run /autopilot-refine 'X' to fix the 5 critical facts issues" or "No action required"}

---

> Generated by `/audit` skill. Report-only — no edits applied.
~~~

Then print to chat (Korean), in ≤8 lines:

    ✓ /audit 완료 — {artifact short name} ({type})
    • Aspects: {comma-separated}
    • Total: 🔴 {N} / 🟡 {M} / 🟢 {K}
    • Report: {audit log path}
    • Verdict: {one-line}
    {if 🔴 > 0:}
    권장 후속: /autopilot-refine "{artifact short name} {fix prompt suggestion}"

### Stage E — Auto-fix chain (default behavior)

After Stage D's report write + chat output, **automatically trigger a fix flow** for the issues found — _unless `--report-only` was specified_.

**Behavior**:
1. **Skip conditions**: if `--report-only` is set, OR if Stage D produced 0 🔴 issues AND 0 🟡 issues (clean), skip Stage E. Print: `✓ Audit clean — no auto-fix needed.` and exit.
2. **Generate fix prompt**: synthesize a single prompt text describing the 🔴 + significant 🟡 issues. Format:
   ~~~
   audit 결과 자동 fix:
   - {issue 1 short description} → {suggested fix from report}
   - {issue 2 short description} → {suggested fix from report}
   ...
   Source audit report: {audit log path}
   ~~~
   Each line of the prompt corresponds to one issue from Stage D's "Issues by aspect" section. Include the audit log path so downstream skill can read the full detail.
3. **Dispatch by artifact type**:
   - **plans (code)** → invoke `autopilot-code` skill with `--mode dev` and the generated prompt as the task description.
   - **research** / **documents** → invoke `autopilot-refine` skill with the artifact name + generated prompt.
4. **Chat alert before dispatch**: print `▶ Auto-fix chain 시작 — {dispatched skill} (🔴 N + 🟡 M issues 반영)`. If user wants to stop, they can interrupt before the next skill runs.
5. **Logging**: append a single line to the audit log's "## Verdict" section: `**Auto-fix dispatched**: yes (→ {skill name}) | no (--report-only or clean)`.

**Why default is auto-chain**: the user's stated incident (5 factual drifts unnoticed across 20+ refine cycles) shows that "report-only" reports get ignored. Auto-chain provides a _forcing function_ — the user must explicitly opt out via `--report-only` to skip the fix. This matches the "빈칸 > 잘못 채우기" Principle 0 spirit at the system level.

**Why `--report-only` opt-out exists**: occasionally the user wants only inspection (e.g., handoff review, exploratory check) without committing to immediate edits. The flag preserves that path.

## Constraints

- **Audit pass is read-only** — Stage A-D never modify the audited artifact (the audit log is written under `_internal/audit/`). Stage E _dispatches a separate skill_ (`autopilot-code` or `autopilot-refine`) which then makes edits per its own confirmation flow. With `--report-only`, Stage E is skipped entirely.
- **No web fetch** — all lookups are local (`.claude_reports/*` files only). Cards grep, Style Guide read, regex scan. Cost is small.
- **No agent invocation** — `/audit` is a single-Claude task. No 연구팀 / 품질관리팀 subagent calls. (Future enhancement may add `--qa` levels with agent-backed lint; out of scope for v1.)
- **Type-specific aspects** — research aspects do not run on documents artifacts and vice versa. `--scope cross-ref` on plans warns and skips.
- **Suggestion only (Stage A-D)** — every 🔴 / 🟡 finding may include a "Suggested fix" line. Stage E dispatches these suggestions to the appropriate skill, which follows its own protocol (autopilot-refine: default 자동 apply + STRUCT halt + 사후 git diff 검토; autopilot-code: phase QA gates + safety commit + final report).

## Examples

    # Full audit of the SE seminar document artifact
    /audit 2026-05-06_se-seminar-tfrestormer

    # Facts-only check of the same artifact (after a 20-cycle refine session)
    /audit 2026-05-06_se-seminar-tfrestormer --scope facts

    # Audit a research artifact's cards consistency
    /audit speech-enhancement-trends --scope facts

    # Read-only static audit of a code plan (skip test execution)
    /audit 2026-05-11_audit-skill-infra --scope all --read-only

    # Inspection only (no auto-fix)
    /audit 2026-05-06_se-seminar-tfrestormer --report-only

## When NOT to use

- 산출물을 _수정_하고 싶은 경우 → `/autopilot-refine`.
- 단일 typo / cosmetic 점검 → 그냥 `grep` / `Read`.
- Full pipeline 재실행 필요 → `/autopilot-{research,doc,code}` 또는 `--from <stage>`.
- 산출물 자체가 존재하지 않음 (사전 분석부터 필요) → `/analyze-project` 또는 `/autopilot-research`.

## Post-Audit Checklist

After audit, the auto-fix chain (Stage E) dispatches automatically. If you used `--report-only`:
1. 🔴 이슈 존재 → `/autopilot-refine "<fix prompt suggested by audit log>"` 또는 `/autopilot-code --mode dev "<fix>"` 직접 호출
2. 🟡 only → 사용자 판단으로 deferred or batch-fix
3. clean → 추가 조치 불필요
