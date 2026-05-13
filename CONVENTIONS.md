# Conventions — Family-Wide Operational Rules

> 본 문서는 autopilot family 전체에 적용되는 _운영 규칙·정의_의 **단일 source of truth**. `DESIGN_PRINCIPLES.md`가 _architectural design_(orchestrator/skill/agent 분리, interface contract 등)을 다룬다면, 본 문서는 _operational conventions_(QA level 정의, model 표기, family-wide flag 정책 등)을 다룬다.
>
> **자동 로드 메커니즘**: `CLAUDE.md`의 "Source of Truth"에 본 파일이 등재되어 세션 시작 시 README 부트스트랩을 통해 인지. QA·model·family-wide flag 관련 작업 시 메인 Claude가 본 파일을 직접 read해 정의를 가져옴.
>
> **자동 propagation**: `/sync-skills`의 Step 5b.5가 본 문서를 canonical로 cross-doc grep해 drift 보고. `--auto-fix` flag로 자동 propagation 수행 (default는 report-only).

---

## §1. QA Levels (canonical)

### §1.1. 5단계 공통 정의

| Level | Quality reviewer | Fact-checker (parallel) | Codex (parallel) | 비고 |
|---|---|---|---|---|
| **quick** | 1× sonnet, 1-pass | skip | skip | refine entire skip / loop 1라운드 강제 종료 / 🔴 잔존 시 `unresolved.md`에 기록만 |
| **light** | 1× sonnet, single-pass | skip (quality reviewer가 spot-check 커버) | skip | 경량 리뷰 |
| **standard** | 1× opus, single-pass | 1× sonnet, parallel¹ | skip | _doc/research/refine 한정_ — fact-checker는 cards/PDFs verbatim 대조 (venue/year/metric/citation) |
| **thorough** | 2× opus, parallel (다른 focus²) | 1× sonnet, parallel¹ | skip | 고위험 산출물 (final-version paper draft, public-facing report 등) |
| **adversarial** | 2× opus, parallel (= thorough quality) | 1× sonnet, parallel¹ | 1× `Agent(codex-review-team)` parallel — Codex CLI (GPT-5) external review | _autopilot-code · autopilot-refine 전용_ — autopilot-doc / autopilot-research는 지원 X (thorough까지) |

¹ Fact-checker는 _doc/research/refine 파이프라인_에만 적용. autopilot-code 계열 (init-plan / refine-plan / execute-plan / run-test)은 fact-checker 없음 — code는 ground-truth source가 코드 자신이므로 quality reviewer만 운용.

² thorough에서 2개 quality reviewer는 _다른 axes_ 분담: 예: A=domain expert + methodology / B=content expert + quality / C=safety. 각 skill SKILL.md가 자기 axis 분담 명시.

### §1.2. Codex availability 정책 (adversarial 전용)

- Adversarial 선택 전 `codex --version 2>/dev/null` 실행
- 실패 시: `--qa adversarial` _명시_ 호출 → fail loudly / auto-detect로 adversarial 선택 → Thorough로 silent fallback
- Codex agent는 `adversarial-review --wait --scope auto` 실행 → `_internal/{stage}_reviews/round_{N}_codex.md` 작성

### §1.3. opt-out flags (orthogonal)

- `--no-fact-check` — 모든 level에서 fact-checker 단독 skip (`quick`/`light`는 어차피 skip이라 무의미)
- `--no-style-audit` — Stage B.5 style aspect skip (refine 계열만)

이 두 flag는 `--qa` level 무관하게 적용되며, fact-checker / style audit을 끄는 _유일한_ 메커니즘 (ad-hoc prompt로 무시 불가). **autopilot-refine · audit 전용** — 다른 skill의 argument-hint에 노출되면 drift.

### §1.4. Skill별 사용 매트릭스

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

---

## §2. Agent Model 표기 (canonical)

각 agent의 frontmatter `model:` 필드는 _sub-agent runtime_ model. 실제 작업 시 가변 또는 외부 LLM 호출이 있는 경우 본문·매트릭스에 명시.

| Agent | frontmatter `model:` | 실제 작동 |
|---|---|---|
| `기획팀` (plan-team) | opus | opus 단일 |
| `품질관리팀` (qa-team) | opus | **가변** — Light=1× sonnet / Standard=1× opus / Thorough=2× opus parallel |
| `연구팀` (research-team) | opus | **가변** — default opus (Plan Review·domain reviewer); fact-checker subrole·light QA는 sonnet (cost-aware verbatim matching) |
| `테스트팀` (test-team) | opus | opus + sonnet 혼합 (Agent A=sonnet coverage / Agent B=opus accuracy) |
| `탐색팀` (browser-team) | sonnet | sonnet 단일 |
| `개발팀` (dev-team) | sonnet | sonnet 단일 |
| `codex-review-team` | opus | **Codex CLI (GPT-5)** — actual review·analysis는 외부 Codex CLI에서; sub-agent 본체(opus)는 호출·결과 한국어 재정리만 담당 |

---

## §3. Removed Flags (family에서 폐기)

| Flag | 폐기일 | 대체 |
|---|---|---|
| `--refs <folder>` | 2026-05-08 | implicit input discovery from `.claude_reports/{analysis_project,research}/*`. 외부 raw 자료는 `/analyze-project --mode {paper\|doc}`로 사전 영속화. |
| `--format-ref <path>` | 2026-05-12 | `analysis_project/doc/{matching}/formats/` auto-discovery (no flag). 사전에 `/analyze-project --mode doc <folder>`로 materialize. |
| `--autonomy proactive\|standard\|passive` | 2026-04 | `--user-refine` 패턴으로 단일화. |

위 flag가 SKILL.md / README / agent.md / notion mirror 본문에 _사용 예시_로 잔존하면 drift (취소선·"제거됨" 안내 형태는 OK).

---

## §4. Deprecated Names (family에서 폐기)

| Name | 폐기일 | 대체 |
|---|---|---|
| `analyze-papers` skill | 2026-04 | `analyze-project --mode paper`로 통합 |
| `autopilot-dev` / `autopilot-audit` / `autopilot-debug` 별도 skill | 2026-04-10 | `autopilot-code --mode dev\|debug`로 통합 (audit은 별도 `/audit` skill로 분리) |
| `refine-doc-strategy` skill 이름 | 2026-05-06 | `refine-doc`로 rename (strategy + draft 양쪽 처리) |
| `기록팀` agent | 2026-05-06 | 제거. Notion 작업은 메인 Claude가 `~/.claude/notion_guide.md` 참조해 직접 수행 |
| Paper card 단일 ground-truth 경로 `{refs}/cards/*.md` | 2026-05-12 | `.claude_reports/analysis_project/paper/*.md` (analyze-project --mode paper 산출물; cards/ 서브디렉토리 폐기) |

---

## §5. Hard Cross-Doc Invariants (sync-skills `--check`가 자동 검사)

1. 각 SKILL.md / README / `_notion_mirror`/*에서 §1.1 5단계 정의의 **Quality reviewer / Fact-checker / Codex 컬럼 wording**은 본 문서와 의미 일치 (사소한 표현 차이는 허용, 의미가 다르면 drift).
2. **adversarial** 정의는 반드시 `thorough + 1× codex-review-team`. 자주 잘못 적힌 패턴: `standard + Codex` — _틀림_.
3. autopilot-code의 QA 표에 fact-checker가 적힌 곳이 있으면 drift (code는 fact-checker 없음).
4. `--no-fact-check` / `--no-style-audit`는 autopilot-refine / audit 외 다른 skill에 노출되면 안 됨.
5. §3 Removed Flags 어느 것이든 SKILL.md / README / agent.md / mirror 본문에 _사용 예시_로 등장하면 drift.
6. §4 Deprecated Names 어느 것이든 _현재 호출 명령_으로 등장하면 drift (역사 안내는 OK).
7. `codex-review-team`의 model 표기가 `opus` 단독이면 drift — 실제 review는 Codex CLI (GPT-5). §2 매트릭스에 따라 "Codex CLI (GPT-5) + opus orchestrator" 같이 분리 표기.

새 invariant 추가는 본 섹션 list에 한 행 추가하면 sync-skills Step 5b.5의 자동 검사 list에 포함.

---

## §6. 자동 fix 정책

`/sync-skills --auto-fix` (default는 report-only):
- §5의 hard invariants 위반 발견 시 canonical wording을 다른 곳으로 propagate
- _Wording 자체_가 다를 경우 (의미 동일·표현 차이): skip (사람 결정 사항)
- _의미가 다른_ 명백한 drift: canonical로 강제 교체 + commit 안내
- `--auto-fix --dry-run`으로 미리보기

---

*마지막 업데이트: 2026-05-13 — 신규 문서. 이전 분산 hard-code 위치(README.md, autopilot-refine/SKILL.md 등)에서 정의 일관성 부재로 인한 drift (예: `adversarial = standard + Codex` 오정의가 한동안 잔존) 해결. CLAUDE.md "Source of Truth"에 등재, sync-skills Step 5b.5가 본 문서 기반으로 cross-doc scan.*
