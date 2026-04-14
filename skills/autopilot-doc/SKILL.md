---
name: autopilot-doc
description: "Document strategy & draft pipeline — [survey: source discovery →] analyze-refs → init-doc-strategy → review → refine-doc-strategy → draft → draft-review. Supports modes: rebuttal, write, review, survey (with active search), report, proposal, presentation."
argument-hint: "<mode> <task description> [--refs <folder>] [--type <survey-type>] [--qa light|standard|thorough] [--autonomy proactive|standard|passive]"
---

## Language Rule
- Write user-facing output in Korean. (Material analysis results and pipeline_summary.md are written directly in the artifacts — no separate user output needed for those steps.)

## Argument Parsing
Parse `$ARGUMENTS` for mode, flags, and task description:

**Mode** (first word, required):
- `rebuttal` — Rebuttal strategy for reviewer comments
- `write` — Paper writing strategy (outline, positioning, contributions)
- `review` — Paper/document review (as reviewer: strengths/weaknesses/questions) [strategy only]
- `survey` — General-purpose research survey with **active source discovery**: literature, market, technology, product, or company analysis. Searches for sources automatically; `--refs` is optional supplementary input.
- `report` — Technical report / white paper (findings, analysis, recommendations)
- `proposal` — Research or project proposal (problem, approach, plan, budget)
- `presentation` — Presentation strategy (story arc, slide structure, key messages) [strategy only]

**`--refs <folder>`** — path to reference materials folder:
- Contains: PDFs, reviewer comments (txt/md), original paper, conference guidelines, data files, etc.
- **Required** for: rebuttal, write, review, report, proposal, presentation.
- **Optional** for: survey (survey mode discovers sources automatically; `--refs` provides supplementary materials to merge with search results).
- If omitted and mode is NOT survey: ask the user for the folder path. Do NOT assume a default location.

**`--qa <level>`** — override QA intensity for the pipeline:
- `--qa light` → 연구팀 review uses sonnet, single-pass review
- `--qa standard` → 연구팀 review uses opus, single-pass review
- `--qa thorough` → 연구팀 review uses opus, parallel reviewers (domain expert + methodology reviewer), cross-validation against all reference materials **(default)**
- If omitted, defaults to `thorough`.
- **Propagation**: Pass `--qa <level>` to init-doc-strategy and refine-doc-strategy as an argument flag.

**`--autonomy <level>`** — same as autopilot-code. Default: `proactive`.
Same validation rules as autopilot-code (invalid value → fallback to `proactive`, with warning).
Pass `--autonomy <level>` to init-doc-strategy and refine-doc-strategy as an argument flag.

**`--type <survey-type>`** — sub-type for survey mode (only used when mode=survey):
- `literature` (default) — academic literature survey
- `market` — market landscape, competitors, trends
- `technology` — technology comparison, maturity assessment
- `product` — product analysis, feature comparison
- `company` — company research, strategy analysis
- If omitted and mode=survey, defaults to `literature`.
- Ignored for all non-survey modes.

> **Note on doc sub-skills**: `init-doc-strategy` and `refine-doc-strategy` do NOT need to parse `--autonomy` themselves — they don't have user-facing decision points. The flag is passed through but they simply ignore it. Unlike `refine-plan` (which has path resolution that could be corrupted), doc sub-skills use positional args so an unrecognized `--autonomy` flag is harmless.

The remaining text (after removing mode and flags) is the task description.

## Autonomy Gating

| Decision Point | Severity | proactive | standard | passive |
|---|---|---|---|---|
| Confirm material analysis | Routine | auto-proceed | auto-proceed | ask |
| Missing refs folder | Critical | ask (always) | ask | ask |
| No reviewer comments for rebuttal | Significant | ask | ask | ask |
| Strategy review → many memos | Routine | auto-refine | auto-refine | ask |
| Draft review → many memos | Routine | auto-refine | auto-refine | ask |
| Skip draft (review/presentation mode) | Routine | auto-skip | auto-skip | inform + auto-skip |
| Survey search results review | Routine | auto-proceed | auto-proceed | ask |
| Survey search found 0 results | Significant | ask | ask | ask |

When the pipeline reaches a gated decision point:
- If the current autonomy level includes that severity → **pause and ask** the user.
- Otherwise → **proceed with the default action** (described in the proactive column).
- All "ask" prompts must include: (1) the situation summary, (2) available options, (3) the default action if no response.
- **Logging**: After each decision (auto or user), record in memory: `{step} | {decision description} | {user response or "auto"} | {action taken}`. These records are written to the Decision Points table in `pipeline_summary.md` when it is created at pipeline end.

## Refs Folder Convention
The `--refs` folder is user-specified (no default). May contain PDFs, txt/md reviewer comments, notes, data files, subdirectories. On first invocation, list contents and confirm with the user. For rebuttal mode, warn if no reviewer comments are found.

## Artifact Structure
All outputs go to:
```
.claude_reports/documents/{YYYY-MM-DD}_{short-name}/
├─ strategy/
│  ├─ strategy.md          (English strategy document)
│  └─ strategy_ko.md       (Korean strategy document)
├─ draft/                   (generated for: rebuttal, write, report, proposal, survey)
│  ├─ draft.md             (English draft)
│  └─ draft_ko.md          (Korean draft)
├─ discovery/               (survey mode only: search results)
│  └─ search_results.json  (discovered sources with metadata)
├─ analysis/
│  ├─ reviewer_analysis.md  (rebuttal: per-reviewer breakdown)
│  ├─ ref_analysis.md       (reference material analysis)
│  └─ material_index.md     (inventory of all input materials)
├─ strategy_reviews/        (QA and 연구팀 strategy reviews)
├─ draft_reviews/           (QA and 연구팀 draft reviews)
└─ pipeline_summary.md
```

## Pipeline

### Step 0: Source Discovery [survey mode only — skip for all other modes]
**Applicable modes**: survey only. All other modes skip to Step 1.

Survey mode actively searches for sources instead of relying solely on `--refs`. The search approach adapts to `--type`:

**0a. Query Expansion**
Generate 2-3 synonym/alternative queries from the task description using LLM knowledge:
- `literature`: academic terminology variants (e.g., "speech enhancement" → "speech denoising", "noise reduction")
- `market`: industry/business terms (e.g., "음성 향상 시장" → "speech enhancement market", "audio AI industry")
- `technology`: technical variants + product names
- `product`: product category + brand names
- `company`: company name + subsidiaries + competitors

**0b. Multi-Source Search**
Invoke the **research-team** (연구팀) agent for source discovery:

```
Research survey mode: Source discovery for {survey_type} survey.

Queries: {queries_list}
Original query: {original_query}
Survey type: {survey_type}
Output directory: {artifact_dir}/discovery/
{If --refs: 'Supplementary materials folder: {refs_folder}'}

Search sources by survey type:
- literature: HF paper_search, Semantic Scholar, arXiv, WebSearch (Google Scholar)
- market: WebSearch (industry reports, news, analyst coverage), WebFetch (company sites)
- technology: WebSearch (tech blogs, benchmarks, documentation), HF paper_search (if academic)
- product: WebSearch (product reviews, comparisons, official sites), WebFetch
- company: WebSearch (company info, press releases, financials), WebFetch (investor pages)

Max results per source per query: 10
Timeout: 3 minutes per source; skip on timeout.

Save results to: {artifact_dir}/discovery/search_results.json
Schema: {"query": "string", "survey_type": "string", "date": "YYYY-MM-DD",
  "sources_used": ["string"], "total_results": int,
  "results": [{"title": "string", "url": "string", "source": "string",
    "year": int|null, "snippet": "string", "relevance_score": float|null}]}

Return file path + 3-5 line Korean summary of what was found.
```

**0c. Post-Search Validation**
1. Read `search_results.json` — verify valid JSON and non-empty results
2. **Autonomy gate (Significant)**: If 0 results found → ask user whether to proceed with `--refs` only or adjust query
3. **Autonomy gate (Routine)**: Present search summary (N results from M sources) — `proactive`/`standard` auto-proceed, `passive` asks

**0d. Reference Chaining** (literature type only)
For literature surveys, extract references from top-ranked papers and discover additional sources:
1. Read top 5 papers from search results (by citation count or relevance)
2. Extract cited references and check if any important ones are missing from results
3. If new relevant references found: run one additional search round with extracted keywords
4. Merge into `search_results.json` (update discovery_count for duplicates)

**0e. Merge with --refs**
If `--refs` was provided, merge:
1. Inventory `--refs` folder → add to `search_results.json` as source="user_provided"
2. Deduplicate by title similarity
3. User-provided materials get priority (higher relevance score)

After Step 0, proceed to Step 1 with the combined discovery results as the analysis input.

### Step 1: Material Analysis
Read and catalog all materials from refs folder (non-survey modes) or discovery results (survey mode).

1. **Inventory**: List all files with brief descriptions. Write to `analysis/material_index.md`.
2. **Analyze by mode**:
   - **rebuttal**: Parse reviewer comments → `analysis/reviewer_analysis.md` (per-reviewer, per-point breakdown with severity classification)
   - **write**: Analyze reference papers → `analysis/ref_analysis.md` (methods, gaps, positioning opportunities)
   - **review**: Analyze target paper/document → `analysis/ref_analysis.md` (methodology assessment, quality analysis)
   - **survey**: Analyze all reference materials → `analysis/ref_analysis.md` (categorization, comparison, gap analysis — adapted to survey type: literature/market/technology/product/company)
   - **report**: Analyze source data/papers → `analysis/ref_analysis.md` (findings, evidence assessment, data quality)
   - **proposal**: Analyze related work and context → `analysis/ref_analysis.md` (prior art, feasibility evidence, competitive landscape)
   - **presentation**: Analyze source document/paper → `analysis/ref_analysis.md` (key messages, audience analysis, narrative structure)
3. Read PDF files using the Read tool. For large PDFs (>10 pages), read in page ranges.
4. **Autonomy gate (Routine)**: Present the analysis summary.
   - `proactive` / `standard`: auto-proceed to Step 2 after presenting the summary.
   - `passive`: ask the user for confirmation before proceeding.

### Step 2: init-doc-strategy
Invoke Skill: `init-doc-strategy` with args: `<mode> --refs <folder> --output <artifact-dir> [--type <survey-type>] <task description>`. Wait for completion.

### Step 3: Strategy Review (연구팀 as domain expert)
1. Resolve strategy paths:
   - `strategy_folder` = `.claude_reports/documents/{YYYY-MM-DD}_{short-name}/`
   - `en_strategy_path` = `{strategy_folder}/strategy/strategy.md`
   - `ko_strategy_path` = `{strategy_folder}/strategy/strategy_ko.md`

2. Invoke reviewers based on `--qa` level:

   **`light`** — Single 연구팀 agent (sonnet model):
   - One-pass review focusing on critical issues only.
   - Review log: `{strategy_folder}/strategy_reviews/research_review.md`

   **`standard`** — Single 연구팀 agent (opus model):
   - Thorough single-pass review.
   - Review log: `{strategy_folder}/strategy_reviews/research_review.md`

   **`thorough`** (default) — Two parallel 연구팀 agents (opus model):
   - **Reviewer A (Domain Expert)**: Cross-checks strategy against reference materials, domain conventions (academic venues for paper modes: NeurIPS, ICML, ICLR, ICASSP, Interspeech, T-ASLP; industry standards for report/proposal/presentation modes), and completeness of coverage.
     - Review log: `{strategy_folder}/strategy_reviews/research_review_domain.md`
   - **Reviewer B (Methodology Reviewer)**: Evaluates logical consistency, persuasiveness of arguments, experimental design soundness, and identifies potential weaknesses an adversarial reviewer would exploit.
     - Review log: `{strategy_folder}/strategy_reviews/research_review_methodology.md`
   - Both reviewers write `<!-- memo: ... -->` comments in the Korean strategy.
   - After both complete, merge memos and deduplicate.

   Common prompt for all levels:
   ```
   Review this document strategy as the user's domain expert proxy.
   Mode: {mode} | KO strategy: {ko_strategy_path} | EN strategy: {en_strategy_path}
   Analysis: {strategy_folder}/analysis/ | Refs: {refs_folder} | Log: {review_log_path}

   Cross-check: actual refs/reviewer comments, domain conventions,
   logical consistency, completeness (any missed reviewer points or gaps?).
   Write memos as `<!-- memo: ... -->` in the Korean strategy.
   Write a structured review log to the log file.
   Return a summary of memos added (or "no issues found").
   ```

3. If memos were added: Invoke Skill: `refine-doc-strategy` with the Korean strategy path as args.
4. If no memos: Skip to Step 4.

### Step 4: Draft Generation [decision: routine — skip for review/presentation modes]
**Applicable modes**: rebuttal, write, report, proposal, survey. **Skip for**: review, presentation (these produce strategy only).

1. Verify strategy is finalized: `{strategy_folder}/strategy/strategy.md` exists and has no `## 미해결 이슈` section (or issues are acceptable).
2. Invoke the **research-team** (연구팀) agent as a subagent:

```
Draft generation mode. Generate a document draft based on the finalized strategy.

Mode: {mode}
Task: {task description}
Strategy (EN): {en_strategy_path}
Strategy (KO): {ko_strategy_path}
Analysis directory: {strategy_folder}/analysis/
Reference materials: {refs_folder}
Save English draft to: {strategy_folder}/draft/draft.md
Save Korean draft to: {strategy_folder}/draft/draft_ko.md

Read the strategy document and all analysis files. Generate a complete first draft following the mode-specific structure below. The draft should be a working document ready for user editing — not a summary of the strategy.

## Mode-Specific Draft Structure

### rebuttal
- Frontmatter: type, venue, status: draft, date
- Per-reviewer response sections following the strategy's priority matrix
- Each response: acknowledgment → core argument → evidence → conclusion
- Tone calibrated per the strategy's tone guidelines
- Additional experiments section with preliminary descriptions
- Revision summary table

### write
- Frontmatter: type, venue, status: draft, date
- Full paper outline with section drafts:
  - Abstract (structured: background → gap → method → results → impact)
  - Introduction (hook → context → gap → contribution → outline)
  - Related Work (organized by strategy's framing)
  - Method (following strategy's outline, with placeholder equations)
  - Experiments (setup → results → ablation, with table skeletons)
  - Conclusion
- Figure/table placeholders with captions

### report
- Frontmatter: type, status: draft, date
- Executive Summary
- Introduction / Background
- Methodology / Approach
- Findings / Analysis (with data tables, charts description)
- Discussion
- Recommendations (prioritized, actionable)
- Appendices (if needed)

### proposal
- Frontmatter: type, status: draft, date
- Executive Summary
- Problem Statement / Motivation
- Proposed Approach / Technical Plan
- Preliminary Results / Feasibility Evidence
- Timeline & Milestones
- Resource Requirements / Budget (if applicable)
- Expected Outcomes / Impact
- Risk Assessment

### survey
- Frontmatter: type, survey_type, status: draft, date
- For literature survey: Taxonomy → Chronological Development → Detailed Comparison → Gaps → Future Directions
- For market survey: Market Overview → Competitor Analysis → Trend Analysis → Opportunity Assessment → Recommendations
- For technology survey: Technology Landscape → Comparison Matrix → Maturity Assessment → Adoption Recommendations
- For product survey: Product Overview → Feature Comparison → User/Market Fit → Recommendations
- For company survey: Company Profile → Strategy Analysis → Competitive Position → Outlook

## Quality Requirements
- Every claim must trace back to a specific reference in the refs folder or analysis.
- Do NOT fabricate citations, data, or results.
- Mark uncertain or placeholder content with `[TODO: ...]`.
- **Mode-specific completeness criteria**:
  - **rebuttal**: 90%+ — every reviewer point MUST have a drafted response (hard constraint). Missing a point is a critical error.
  - **write/report/proposal**: 70-80% — all sections with substantive content, no heading-only sections.
  - **survey**: 60-70% — flexible based on reference volume. Comparison matrices and taxonomy structure are required; individual item details may use [TODO].

Write both files directly. Return ONLY the file paths and a 3-5 line Korean summary.
```

3. **IMPORTANT**: Do NOT read, re-write, or duplicate the draft files yourself. The agent writes them directly.

### Step 5: Draft Review (연구팀 as QA)
**Applicable modes**: same as Step 4 (rebuttal, write, report, proposal, survey). Skip for review, presentation.

1. Resolve draft paths:
   - `en_draft_path` = `{strategy_folder}/draft/draft.md`
   - `ko_draft_path` = `{strategy_folder}/draft/draft_ko.md`

2. Invoke reviewers based on `--qa` level (same scaling as Step 3 strategy review):

   **`light`** — Single 연구팀 agent (sonnet model):
   - One-pass review focusing on critical issues only.
   - Review log: `{strategy_folder}/draft_reviews/draft_review.md`

   **`standard`** — Single 연구팀 agent (opus model):
   - Thorough single-pass review.
   - Review log: `{strategy_folder}/draft_reviews/draft_review.md`

   **`thorough`** — Two parallel 연구팀 agents (opus model):
   - **Reviewer A (Content Expert)**: Cross-checks draft against strategy, verifies all strategy points are addressed, checks factual accuracy against refs.
     - Review log: `{strategy_folder}/draft_reviews/draft_review_content.md`
   - **Reviewer B (Quality Reviewer)**: Evaluates writing quality, logical flow, completeness, identifies gaps and weak arguments.
     - Review log: `{strategy_folder}/draft_reviews/draft_review_quality.md`
   - Both reviewers write `<!-- memo: ... -->` comments in the Korean draft.
   - After both complete, merge memos and deduplicate.

   Common prompt for all levels:
   ```
   Review this document draft as the user's domain expert proxy.
   Mode: {mode} | KO draft: {ko_draft_path} | EN draft: {en_draft_path}
   Strategy: {en_strategy_path} | Analysis: {strategy_folder}/analysis/ | Refs: {refs_folder}
   Log: {review_log_path}

   Cross-check: strategy coverage (all points addressed?), factual accuracy against refs,
   logical flow, writing quality, completeness, [TODO] items.
   For rebuttal: verify every reviewer point has a response.
   Write memos as `<!-- memo: ... -->` in the Korean draft.
   Write a structured review log to the log file.
   Return a summary of memos added (or "no issues found").
   ```

3. If memos were added: Invoke Skill: `refine-doc-strategy` with the Korean draft path as args.
   - Note: refine-doc-strategy handles draft paths (draft/draft.md ↔ draft/draft_ko.md) via auto-detection.
4. If no memos: Skip to Step 6.

### Step 6: Pipeline Summary
**Always write** `{strategy_folder}/pipeline_summary.md` before reporting to the user.

```markdown
# Document Strategy Pipeline Summary: {task name}

- **Date**: {YYYY-MM-DD} | **Mode**: {mode} | **Type**: {survey_type or "N/A"} | **Status**: done / reviewed / draft
- **Autonomy**: {autonomy_level}
- **Refs folder**: {refs_folder}

## Process Log
| Step | Action | Result | Notes |
|---|---|---|---|
| 0 | Source Discovery | completed / skipped (non-survey) | {N} results from {M} sources |
| 1 | Material Analysis | completed | {N} files |
| 2 | init-doc-strategy | created | {strategy path} |
| 3 | Strategy Review (연구팀) | memos added / no issues | {memo count} |
| 3b | refine-doc-strategy | refined / skipped | |
| 4 | Draft Generation | created / skipped (review/presentation) | {draft path or "N/A"} |
| 5 | Draft Review (연구팀) | memos added / no issues / skipped | {memo count or "N/A"} |
| 5b | refine-doc-strategy (draft) | refined / skipped | |

## Artifacts
- Strategy (EN/KO): {en_path} / {ko_path}
- Draft (EN/KO): {draft_en_path} / {draft_ko_path} (or "N/A — strategy-only mode")
- Analysis: {reviewer_analysis or ref_analysis path}
- Material Index: {path} | Strategy Review: {path} | Draft Review: {path or "N/A"}

## Decision Points
| Step | Decision | User Response | Action Taken |
|---|---|---|---|
| (filled from orchestrator's in-memory decision log) |
```

When writing pipeline_summary.md, populate the Decision Points table from the in-memory decision records. If no decisions were recorded (proactive mode, clean run), write: `| - | No gated decisions triggered | - | - |`. Note: autopilot-doc typically has fewer decision points (material analysis confirmation at passive level is the main one).

Then report to the user:
- Strategy file paths + 2-3 line summary of the strategy.
- Draft file paths + 2-3 line summary of the draft (if applicable).
- For review/presentation modes: note that these modes produce strategy only (no draft).

## Safety Rules
- Do NOT fabricate citations or invent results — only reference materials actually present in the refs folder.
- The draft is a working first draft for user editing, NOT a final document. Mark uncertain content with `[TODO: ...]`.
- For rebuttal mode: ensure EVERY reviewer point is addressed — missing a point is a critical error.
- Present material inventory to the user. Proceed per the Autonomy Gating table (material analysis confirmation).
- For review/presentation modes: do NOT attempt draft generation — these are strategy-only modes.

## Task
$ARGUMENTS
