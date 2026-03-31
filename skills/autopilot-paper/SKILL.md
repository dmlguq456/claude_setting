---
name: autopilot-paper
description: "Paper strategy pipeline — analyze-refs → init-paper-strategy → review → refine-paper-strategy. Supports modes: rebuttal, write, review, survey."
argument-hint: "<mode> <task description> [--refs <folder>] [--qa light|standard|thorough]"
---

## Language Rule
- Write user-facing output in Korean. (Material analysis results and pipeline_summary.md are written directly in the artifacts — no separate user output needed for those steps.)

## Argument Parsing
Parse `$ARGUMENTS` for mode, flags, and task description:

**Mode** (first word, required):
- `rebuttal` — Rebuttal strategy for reviewer comments
- `write` — Paper writing strategy (outline, positioning, contributions)
- `review` — Paper review (as reviewer: strengths/weaknesses/questions)
- `survey` — Related work survey (categorize, gap analysis)

**`--refs <folder>`** — path to reference materials folder (required on first run):
- Contains: PDFs, reviewer comments (txt/md), original paper, conference guidelines, etc.
- If omitted: ask the user for the folder path. Do NOT assume a default location.

**`--qa <level>`** — override QA intensity for the pipeline:
- `--qa light` → 연구팀 review uses sonnet, single-pass review
- `--qa standard` → 연구팀 review uses opus, single-pass review
- `--qa thorough` → 연구팀 review uses opus, parallel reviewers (domain expert + methodology reviewer), cross-validation against all reference materials **(default)**
- If omitted, defaults to `thorough`.
- **Propagation**: Pass `--qa <level>` to init-paper-strategy and refine-paper-strategy as an argument flag.

The remaining text (after removing mode and flags) is the task description.

## Refs Folder Convention
The `--refs` folder is user-specified (no default). May contain PDFs, txt/md reviewer comments, notes, subdirectories. On first invocation, list contents and confirm with the user. For rebuttal mode, warn if no reviewer comments are found.

## Artifact Structure
All outputs go to:
```
.claude_reports/papers/{YYYY-MM-DD}_{short-name}/
├─ strategy/
│  ├─ strategy.md          (English strategy document)
│  └─ strategy_ko.md       (Korean strategy document)
├─ analysis/
│  ├─ reviewer_analysis.md  (rebuttal: per-reviewer breakdown)
│  ├─ ref_analysis.md       (reference paper analysis)
│  └─ material_index.md     (inventory of all input materials)
├─ strategy_reviews/        (QA and 연구팀 reviews)
└─ pipeline_summary.md
```

## Pipeline

### Step 1: Material Analysis
Read and catalog all materials in the refs folder.

1. **Inventory**: List all files with brief descriptions. Write to `analysis/material_index.md`.
2. **Analyze by mode**:
   - **rebuttal**: Parse reviewer comments → `analysis/reviewer_analysis.md` (per-reviewer, per-point breakdown with severity classification)
   - **write**: Analyze reference papers → `analysis/ref_analysis.md` (methods, gaps, positioning opportunities)
   - **review**: Analyze target paper → `analysis/ref_analysis.md` (methodology assessment, experimental analysis)
   - **survey**: Analyze all papers → `analysis/ref_analysis.md` (categorization, timeline, methodology comparison)
3. Read PDF files using the Read tool. For large PDFs (>10 pages), read in page ranges.
4. Present the analysis summary to the user and confirm before proceeding.

### Step 2: init-paper-strategy
Invoke Skill: `init-paper-strategy` with args: `<mode> --refs <folder> --output <artifact-dir> <task description>`. Wait for completion.

### Step 3: Strategy Review (연구팀 as domain expert)
1. Resolve strategy paths:
   - `strategy_folder` = `.claude_reports/papers/{YYYY-MM-DD}_{short-name}/`
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
   - **Reviewer A (Domain Expert)**: Cross-checks strategy against reference materials, academic conventions at top-tier venues (NeurIPS, ICML, ICLR, ICASSP, Interspeech, T-ASLP), and completeness of coverage.
     - Review log: `{strategy_folder}/strategy_reviews/research_review_domain.md`
   - **Reviewer B (Methodology Reviewer)**: Evaluates logical consistency, persuasiveness of arguments, experimental design soundness, and identifies potential weaknesses an adversarial reviewer would exploit.
     - Review log: `{strategy_folder}/strategy_reviews/research_review_methodology.md`
   - Both reviewers write `<!-- memo: ... -->` comments in the Korean strategy.
   - After both complete, merge memos and deduplicate.

   Common prompt for all levels:
   ```
   Review this paper strategy as the user's domain expert proxy.
   Mode: {mode} | KO strategy: {ko_strategy_path} | EN strategy: {en_strategy_path}
   Analysis: {strategy_folder}/analysis/ | Refs: {refs_folder} | Log: {review_log_path}

   Cross-check: actual refs/reviewer comments, academic conventions ({mode} at top-tier venues),
   logical consistency, completeness (any missed reviewer points or gaps?).
   Write memos as `<!-- memo: ... -->` in the Korean strategy.
   Write a structured review log to the log file.
   Return a summary of memos added (or "no issues found").
   ```

3. If memos were added: Invoke Skill: `refine-paper-strategy` with the Korean strategy path as args.
4. If no memos: Skip to Step 4.

### Step 4: Pipeline Summary
**Always write** `{strategy_folder}/pipeline_summary.md` before reporting to the user.

```markdown
# Paper Strategy Pipeline Summary: {task name}

- **Date**: {YYYY-MM-DD} | **Mode**: {mode} | **Status**: done / reviewed / draft
- **Refs folder**: {refs_folder}

## Process Log
| Step | Action | Result | Notes |
|---|---|---|---|
| 1 | Material Analysis | completed | {N} files |
| 2 | init-paper-strategy | created | {strategy path} |
| 3 | 연구팀 Review | memos added / no issues | {memo count} |
| 3b | refine-paper-strategy | refined / skipped | |

## Artifacts
- Strategy (EN/KO): {en_path} / {ko_path}
- Analysis: {reviewer_analysis or ref_analysis path}
- Material Index: {path} | Research Review: {path}
```

Then report to the user: strategy file paths + 2-3 line summary of the strategy.

## Safety Rules
- Do NOT fabricate citations or invent paper results — only reference materials actually present in the refs folder.
- Do NOT generate full paper text (that's the user's job) — output is strategy/plan only.
- For rebuttal mode: ensure EVERY reviewer point is addressed — missing a point is a critical error.
- Always confirm material inventory with the user before proceeding to strategy generation.

## Task
$ARGUMENTS
