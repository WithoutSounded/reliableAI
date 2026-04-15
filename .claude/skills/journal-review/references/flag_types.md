# Flag Types Reference

Complete list of flag types used by journal-review, organized by review phase.

## Phase 3a: Automated Hard Checks

| Flag Type | Default Severity | Description |
|-----------|-----------------|-------------|
| `MISSING_CITATION` | major/minor | `\cite{Key}` in text has no matching entry in references.bib. Major if the claim depends on this citation for credibility; minor if it's a supplementary reference. |
| `ORPHAN_BIB_ENTRY` | minor | Entry exists in references.bib but is never `\cite{}`'d. Usually just cleanup, but could indicate a dropped paragraph. |
| `ORPHAN_FIGURE` | major | Figure listed in figure_catalog.md is never `\ref{}`'d in the manuscript. Every figure should earn its place. |
| `BROKEN_REF` | major | `\ref{fig:X}` or `\ref{tab:X}` has no corresponding `\label{}`. Will render as "??" in compiled PDF. |
| `NUMBER_MISMATCH` | critical | A numeric value in the text (accuracy, F1, p-value, N) doesn't match the source data in analysis_summary.md or figure_captions.md. |
| `SYMBOL_CONFLICT` | minor/major | A math symbol is used across sections without a glossary definition, or with inconsistent meaning. Major if the conflicting meanings could confuse the reader. |
| `OVER_BUDGET` | minor/major | Section word count exceeds blueprint budget by >15%. Minor if 15-30% over; major if >30% over. |
| `UNDER_BUDGET` | minor | Section word count is <70% of budget. May indicate missing content. |

## Phase 3b: Scientific Claims Review

| Flag Type | Default Severity | Description |
|-----------|-----------------|-------------|
| `HALLUCINATION` | critical | A quantitative claim in Results or Discussion has no data support whatsoever — the number or result was invented. This is the most serious flag. |
| `EXAGGERATION` | major | Data partially supports the claim but the text overstates it. E.g., "significant improvement" when p=0.08, or "outperforms all baselines" when it only beats 3 of 5. |
| `LOGIC_BREAK` | major | A later section contradicts or ignores something established in an earlier section. E.g., Methods describes 5 conditions but Results only reports 4. |
| `OVERCLAIM` | major | An interpretive claim (usually in Discussion) is stronger than the evidence warrants. E.g., using "demonstrates" when the evidence only "suggests". |
| `UNDERCLAIM` | minor | Evidence is strong but the language is unnecessarily hedged. This wastes the paper's impact — if you have p<0.001 with large effect size, say "demonstrates" not "may suggest". |

## Phase 3c: Adversarial Questioning

| Flag Type | Default Severity | Description |
|-----------|-----------------|-------------|
| `EXPENDABLE` | minor | A paragraph doesn't contribute unique information — it's redundant, off-topic, or repeats what's already established elsewhere. Suggestion: cut, merge, or justify. |
| `CROSS_SECTION_INCONSISTENCY` | major | Claims don't align across sections. E.g., Introduction promises 4 contributions but Conclusion lists 3. Always includes quotes from both locations. |
| `VISUAL_TEXT_MISMATCH` | major | Text description of a figure/table doesn't match what the figure/table actually shows (per captions). E.g., text says "monotonically increasing" but figure shows a plateau. |
| `MISATTRIBUTION` | critical | A cited paper doesn't support the claim attributed to it. Only flagged when full text is available for verification. Credibility-destroying if caught by reviewers. |

## Severity Decision Guide

When the default severity isn't clearly right, use this rubric:

- **Critical**: Would a reviewer reject the paper based on this alone? Would it damage the authors' credibility? (Wrong numbers, fabricated claims, misattributed citations)
- **Major**: Would a reviewer flag this in their report and require revision? Does it weaken the paper's argument? (Logical inconsistencies, broken references, overclaims)
- **Minor**: Would a careful reader notice this but not reject over it? Is it a style/completeness issue? (Budget overruns, orphan bib entries, underclaims, expendable paragraphs)

Context matters: a `MISSING_CITATION` for "EEG is widely used in neuroscience" is minor (common knowledge). A `MISSING_CITATION` for "Smith et al. showed that X outperforms Y" is major (specific attributable claim).
