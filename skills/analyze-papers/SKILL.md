---
name: analyze-papers
description: Read reference papers (PDFs in .claude_reports/refs/) and generate/update docs_paper/ documentation including 00_overview_and_constraints.md
argument-hint: "[specific paper or 'all']"
---

## Language Rule
- Think and reason in English internally. Write all user-facing output in Korean.

## Delegate to 연구팀
Invoke the **research-team** (연구팀) agent as a subagent with the following prompt:

```
Analyze reference papers and generate paper documentation.

Scope: {$ARGUMENTS or "all"}
Date: {YYYY-MM-DD}

## Inputs
- Reference PDFs: .claude_reports/refs/*.pdf
- Existing paper docs: .claude_reports/docs_paper/*.md
- Existing code docs: .claude_reports/docs_code/*.md (for paper-code mapping)
- Source code: models/ (for verifying paper-code alignment)

## Procedure

### 1. Read all reference PDFs
Read these PDFs in `.claude_reports/refs/`: SPL_TF_CorrNet, IS_IF_CorrNet, NeurIPS_SepReformer, TASLP_SR_CorrNet, thesis_presentation.
Extract: core contributions, architecture design, key equations, experimental findings, design constraints, ablation results.

### 2. Read existing docs_paper/ files
Check what already exists and what needs updating.

### 3. Read code docs and source code
Read .claude_reports/docs_code/ and relevant source files to verify paper-code alignment.

### 4. Generate/Update individual paper summaries
For each paper, create or update its summary file in `.claude_reports/docs_paper/` (agent decides filenames).
Each file should contain: paper title/venue/year, core contribution, architecture overview, key design decisions and why, important equations, ablation results that constrain design, paper-to-code mapping.

### 5. Generate/Update 00_overview_and_constraints.md
This is the MOST IMPORTANT file — it's the primary reference for 연구팀 during plan review.

Structure:
```markdown
# Project Overview and Design Constraints

## Paper Evolution
## Paper → Code Variant Mapping
## Core Design Principles
(each principle: what it is, why it matters with paper evidence, how it maps to code)
## Architecture Constraints
Hard Constraints (must NOT be changed):
- correlation input: spatial correlation as network input
- early-split: speaker split before main processing
- filter estimation: filter-based output, not direct waveform
- 3 model variants separate: SE/SS/CSS must remain independent
- network.py extraction on hold: SS/CSS have different dropout behavior
## Terminology Mapping
## Cross-Paper Relationships
```

### 6. Verify paper-code alignment
For each major component, verify alignment and document discrepancies or code-only features.

Write in English. Code identifiers stay as-is.
Return ONLY the list of created/updated file paths and a brief Korean summary.
```

## Post-Analysis
After the 연구팀 agent returns:
1. Relay the file paths and summary to the user.
2. Recommend reviewing `00_overview_and_constraints.md` first.

## Task
Analyze papers: $ARGUMENTS
