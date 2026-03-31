---
name: init-paper-strategy
description: Create an initial paper strategy document (rebuttal/write/review/survey) based on analyzed reference materials
argument-hint: "<mode> --refs <folder> --output <artifact-dir> <task description>"
---

## Language Rule
- Think and reason in English internally.
- Write all user-facing output in Korean.

## Argument Parsing
Parse `$ARGUMENTS`:
- **mode**: first word — `rebuttal | write | review | survey`
- **--refs <folder>**: path to reference materials
- **--output <dir>**: artifact output directory (`.claude_reports/papers/{date}_{name}/`)
- Remaining text: task description / context

## Pre-Check
- Verify analysis files exist in `{output_dir}/analysis/`:
  - `material_index.md` (required)
  - `reviewer_analysis.md` (required for rebuttal mode)
  - `ref_analysis.md` (required for write/review/survey modes)
- If missing, report error — autopilot-paper Step 1 should have created these.

## Delegate to 연구팀
Invoke the **research-team** (연구팀) agent as a subagent with the following prompt:

````
Paper strategy mode. Create an initial {mode} strategy document.

Mode: {mode}
Task: {task description}
Date: {YYYY-MM-DD}
Reference materials folder: {refs_folder}
Analysis directory: {output_dir}/analysis/
Save English strategy to: {output_dir}/strategy/strategy.md
Target venues: NeurIPS, ICML, ICLR, ICASSP, Interspeech, IEEE/ACM T-ASLP

## Inputs
1. Read all analysis files in the analysis directory (material_index.md, reviewer_analysis.md or ref_analysis.md)
2. Read relevant reference PDFs from the refs folder as needed for deeper understanding
3. Consider venue-specific conventions and expectations

## Mode-Specific Instructions

### If mode = rebuttal
```markdown
---
type: rebuttal
venue: {venue if known, or "TBD"}
status: draft
date: {YYYY-MM-DD}
---

# Rebuttal Strategy: {paper title}

## 1. Meta-Review Summary
- Overall reviewer consensus (positive/mixed/negative), common themes
- Key strengths acknowledged (leverage these), critical weaknesses (prioritize these)
- Estimated acceptance likelihood and what would tip the balance

## 2. Response Priority Matrix
| Priority | Reviewer | Point | Severity | Category | Strategy |
|---|---|---|---|---|---|

Categories: Methodology, Experiments, Writing, Novelty, Comparison, Theory, Reproducibility
Strategies: Defend, Acknowledge+Mitigate, Partial-Agree+Extend, Concede+Revise, Clarify

## 3. Reviewer-by-Reviewer Detailed Strategy

### Reviewer {N} — Score: {X}, Confidence: {Y}
#### Sentiment: {positive/neutral/negative/hostile}
#### Key Leverage Points
#### Point-by-Point Response

##### R{N}.{M}: {summary of reviewer point}
- **Severity**: Critical / Major / Minor / Nitpick
- **Category**: {category}
- **Strategy**: {strategy type}
- **Core Argument**: {1-2 sentence rebuttal logic}
- **Supporting Evidence**: {what data/results/citations support the rebuttal}
- **Tone**: {defensive → neutral → concessive spectrum}
- **Draft Response Outline**:
  - Opening: {acknowledgment or framing}
  - Body: {main argument}
  - Evidence: {specific results to cite}
  - Closing: {what was done / will be done}

## 4. Additional Experiments Plan
| Experiment | Purpose | Addresses Points | Feasibility (days) | Priority |
|---|---|---|---|---|

## 5. Paper Revision Plan
| Section | Proposed Change | Addresses | Priority |
|---|---|---|---|

## 6. Response Tone & Style Guidelines
- Overall tone, per-reviewer adjustments, phrases to use/avoid, word count budget

## 7. Risk Assessment
- Weakest defense points, potential follow-up questions, contingency if experiments fail, AC perspective
```

### If mode = write
```markdown
---
type: write / venue: {target venue} / status: draft / date: {YYYY-MM-DD}
---
# Paper Writing Strategy: {topic}
## 1. Positioning Analysis — research gap, how this fills it, differentiation from closest work
## 2. Contribution Statement — primary (1 sentence), secondary, scope limitations
## 3. Paper Outline — section-by-section with key points and target page allocation
## 4. Key Arguments & Evidence — per section: argument + supporting evidence
## 5. Related Work Strategy — framing prior work to highlight novelty
## 6. Experiment Design Strategy — experiments proving claims, baselines, ablations
## 7. Risk & Weakness Mitigation — anticipated reviewer concerns and preemptive responses
## 8. Venue-Specific Considerations — page limits, formatting, reviewer expectations
```

### If mode = review
```markdown
---
type: review / status: draft / date: {YYYY-MM-DD}
---
# Paper Review: {paper title}
## Summary / ## Strengths / ## Weaknesses / ## Questions for Authors
## Missing References / ## Minor Issues / ## Overall Assessment & Recommendation / ## Confidence
```

### If mode = survey
```markdown
---
type: survey / status: draft / date: {YYYY-MM-DD}
---
# Literature Survey: {topic}
## Taxonomy / ## Chronological Development / ## Method Comparison Table
## Research Gaps / ## Future Directions
```

## Quality Requirements
Every reviewer point must appear in rebuttal strategy (missing a point is a critical error). Severity classification must be justified. All citations must reference actual papers in the refs folder — do NOT fabricate. Strategy must be actionable with specific plans, not vague advice. Apply venue-specific norms (e.g., NeurIPS rebuttal length limits, ICASSP culture).

Write the strategy file directly. Return ONLY the file path and a 3-5 line Korean summary of the strategy. Do NOT return the strategy content itself.
````

**IMPORTANT: Do NOT read, re-write, or duplicate the strategy file yourself.** The agent writes it directly. You only receive paths and a summary.

## QA Scaling
Auto-detect from strategy scope:

| Level | Condition | Action |
|---|---|---|
| **Light** | review/survey mode, ≤3 papers | 1× 품질관리팀 (`model: "sonnet"`) |
| **Standard** | write mode, or rebuttal with ≤3 reviewers | 1× 품질관리팀 (default opus) |
| **Thorough** | rebuttal with ≥4 reviewers, or survey with ≥10 papers | 2× 품질관리팀 in parallel (opus) |

## Post-Strategy Review Loop (max 2 revision rounds)
The log directory is the artifact root folder (parent of `strategy/`).
- `mkdir -p {log_dir}/strategy_reviews` before invoking QA.

After the 연구팀 agent returns:
1. **Invoke 품질관리팀:** "Review this paper strategy for completeness and logical soundness. Strategy file: [path]. Mode: {mode}. For rebuttal mode, verify ALL reviewer points are addressed. Write review to: {log_dir}/strategy_reviews/round_{N}.md. Return ONLY the file path and a one-line verdict."
2. **Check verdict:** No 🔴 issues → proceed to Korean Version Generation. 🔴 issues found → re-invoke 연구팀 to revise (max 2 rounds).
3. **If 🔴 issues remain after 2 rounds**: Add to `## 미해결 이슈` section in the strategy, report to user.

## Korean Version Generation
After review loop completes, invoke 연구팀 one final time:
```
Translate mode. Create the Korean version of the finalized strategy.
English strategy file: {strategy_path}
Save Korean version to: {same directory}/strategy_ko.md
Create a full Korean translation (NOT a summary). All sections with same detail.
Code identifiers, paper titles, and technical terms stay in English.
Return ONLY the file path.
```
Then report to the user: English and Korean strategy paths, strategy summary, and QA verdict.

## Task
$ARGUMENTS
