# Artifact Inventory Reference

Complete list of upstream artifacts the Journal Writing Agent pipeline expects, with severity (critical vs. optional) and which downstream step consumes each.

## From Research Session

| Key | Path | Severity | Consumed by (step) | Notes |
|---|---|---|---|---|
| `sota_review` | `step6_sota_review.md` | critical | Blueprint, Draft (Intro/Related/Discussion), Review | Source material for positioning |
| `gap_analysis` | `step7_gap_analysis.md` | critical | Blueprint, Draft (Intro) | Motivates the paper |
| `hypothesis` | `step8_hypothesis_specification.md` | critical | Blueprint, Draft (Intro/Methods) | Research question & predictions |
| `journal_recommendations` | `step8_journal_recommendations.md` | optional | Init (target journal specs) | Skip if user already picked a journal |
| `references_bib` | `step4_references.bib` | critical | Draft, Review, Finalize | Citation pool — all sections rely on this |
| `citation_keys` | `step4_citation_keys.md` | optional | Review (citation accuracy) | Human-readable lookup |
| `full_text` | `step5_full_text/` | optional | Review (deep citation checks) | Per-paper Markdown; graceful fallback if partial |
| `intro_draft` | `step9_manuscript/01_intro.tex` | optional | Draft (cross-agent validation) | Reference draft, not used as starting point |
| `related_work_draft` | `step9_manuscript/02_relatedwork.tex` | optional | Draft (cross-agent validation) | Same — reference only |

## From Algorithm Session

| Key | Path | Severity | Consumed by (step) | Notes |
|---|---|---|---|---|
| `architecture_spec` | `step1_architecture_spec.md` | critical | Blueprint (pseudocode, notation), Draft (Methods) | Model design document |
| `ablation_matrix` | `step1_ablation_matrix.md` | critical | Draft (Methods, Results) | Experimental design |
| `analysis_summary` | `step4_analysis_summary.md` | critical | Draft (Results, Discussion), Review (number checks) | All quantitative claims trace back here |
| `figure_catalog` | `step5_figure_catalog.md` | critical | Blueprint (figure captions), Draft (all sections with figures) | Inventory of publication figures |
| `experiment_report` | `step6_experiment_report.md` | critical | Draft (Results, Discussion), Review | Full experimental narrative |
| `figures_dir` | `8_Manuscript/figures/` (at project root) | critical | Draft, Finalize (LaTeX packaging) | Actual figure files (PDF/PNG) |

## Severity Semantics

- **critical**: Downstream steps cannot proceed meaningfully without this artifact. If missing, surface prominently at Checkpoint after Init and ask the user to resolve before running `/journal-blueprint`.
- **optional**: Downstream steps will adapt or skip related checks. Record in `artifacts.warnings` in the session config so later steps know to degrade gracefully.

## Resolution Rules

1. **Path resolution order**: check the exact path first. If not found, try common variants (e.g., `refs.bib` vs. `references.bib`, `figures/` vs. `Figures/`) — but only if the variant is unambiguous.
2. **Partial directories** (e.g., `step5_full_text/` exists but contains only 40 of 60 citation keys): treat as "found with warnings" — record the coverage percentage in the config.
3. **Stale artifacts**: if the file exists but is obviously outdated (e.g., `mtime` older than the Algorithm session's `experiment_report.md`), emit a warning. Don't block — the user may have intentionally frozen an earlier version.
4. **Symlinks**: resolve them but store the symlink path in the config (not the target), so the config stays portable.

## When a Critical Artifact Is Missing

1. Report the specific path checked and what step would have consumed it.
2. Suggest the command that produces it (e.g., `/research-sota` produces `step6_sota_review.md`).
3. Offer the user two paths:
   - **Abort**: don't create the journal session; fix the upstream gap first.
   - **Continue with warnings**: proceed, but record the missing artifact in `artifacts.critical_missing[]`. Downstream steps will fail loudly when they hit the gap — that's intentional.

Do not silently proceed. The whole value of Step 0 is catching these gaps before the user has invested time in drafting.
