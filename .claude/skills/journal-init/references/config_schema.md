# `step0_session_config.json` Schema

Authoritative schema for the file produced by `journal-init`. All downstream journal-* skills depend on this structure — any new field added here must be reflected in the consumer.

## Full Example

```json
{
  "session_id": "20260415",
  "paper_slug": "fuzzy-gating-eeg-gaze-social",
  "research_session": "0_Research/",
  "algorithm_session": "Algorithm/20260104_multimodal-social-interaction/",

  "target_journal": "Advanced Engineering Informatics",
  "short_name": "AEI",
  "publisher": "Elsevier",
  "template": "Elsevier CAS (Compact Article Style, double-column)",
  "documentclass": "\\documentclass[a4paper,fleqn]{cas-dc}",
  "page_target": "12-15 pages",
  "word_limit": 8000,
  "abstract_word_limit": 250,
  "citation_style": "elsarticle-num",
  "section_structure": [
    "Abstract", "Introduction", "Related Work",
    "Methods", "Results", "Discussion", "Conclusion"
  ],
  "writing_order": [
    "Methods", "Results", "Introduction",
    "Related Work", "Discussion", "Conclusion", "Abstract"
  ],

  "format_checker_skill": "aei-checker",
  "format_checker_status": "ready",
  "format_checker_checked_at": "2026-04-15T10:00:00+08:00",

  "current_step": 0,
  "review_round": 0,
  "created_at": "2026-04-15T10:00:00+08:00",

  "artifacts": {
    "from_research": {
      "sota_review":            "0_Research/step6_sota_review.md",
      "gap_analysis":           "0_Research/step7_gap_analysis.md",
      "hypothesis":             "0_Research/step8_hypothesis_specification.md",
      "journal_recommendations":"0_Research/step8_journal_recommendations.md",
      "references_bib":         "0_Research/step4_references.bib",
      "citation_keys":          "0_Research/step4_citation_keys.md",
      "full_text":              "0_Research/step5_full_text/",
      "intro_draft":            "0_Research/step9_manuscript/01_intro.tex",
      "related_work_draft":     "0_Research/step9_manuscript/02_relatedwork.tex"
    },
    "from_algorithm": {
      "architecture_spec": "Algorithm/20260104_multimodal-social-interaction/step1_architecture_spec.md",
      "ablation_matrix":   "Algorithm/20260104_multimodal-social-interaction/step1_ablation_matrix.md",
      "analysis_summary":  "Algorithm/20260104_multimodal-social-interaction/step4_analysis_summary.md",
      "figure_catalog":    "Algorithm/20260104_multimodal-social-interaction/step5_figure_catalog.md",
      "experiment_report": "Algorithm/20260104_multimodal-social-interaction/step6_experiment_report.md",
      "figures_dir":       "8_Manuscript/figures/"
    },
    "warnings": [
      {
        "artifact": "full_text",
        "issue": "coverage_incomplete",
        "detail": "42 of 60 citation keys have full-text entries. Deep citation checks will skip 18 entries."
      }
    ],
    "critical_missing": []
  }
}
```

## Field Groups

### Session identity

| Field | Required | Notes |
|---|---|---|
| `session_id` | yes | `YYYYMMDD` of creation date |
| `paper_slug` | yes | lowercase-hyphenated, ≤40 chars, descriptive of the paper's thesis |
| `research_session` | yes | Path relative to project root. `"0_Research/"` for legacy layouts, `"Research/{id}_{slug}/"` for multi-session. |
| `algorithm_session` | yes | Same convention, typically `"Algorithm/{id}_{slug}/"` |

### Target journal specs

All populated from `references/target_journals.md` or from `step8_journal_recommendations.md`. If a field genuinely doesn't apply to the target journal, use `null` rather than omitting — downstream code checks for presence.

| Field | Required | Notes |
|---|---|---|
| `target_journal` | yes | Full official name |
| `short_name` | no | For display |
| `publisher` | yes | "IEEE", "Elsevier", etc. |
| `template` | yes | LaTeX template description |
| `documentclass` | no | Exact `\documentclass{...}` line |
| `page_target` | no | Informational |
| `word_limit` | yes | Integer; body word count |
| `abstract_word_limit` | yes | Integer; abstract-specific |
| `citation_style` | yes | `.bst` name or style name |
| `section_structure` | yes | Ordered list, journal's actual naming |
| `writing_order` | yes | Default: Methods → Results → Intro → Related → Discussion → Conclusion → Abstract |

### Format checker

`journal-finalize` refuses to run unless the expected format checker skill exists on disk. `journal-init` resolves the expected skill from `target_journals.md`, probes `.claude/skills/{name}/SKILL.md`, and freezes the result here.

| Field | Required | Notes |
|---|---|---|
| `format_checker_skill` | yes | Slug of the expected skill (e.g., `aei-checker`, `tnsre-checker`). Sourced from `target_journals.md` or synthesized from `short_name` when the journal is new. Always set — never `null`. |
| `format_checker_status` | yes | `"ready"` if `.claude/skills/{format_checker_skill}/SKILL.md` exists; `"missing"` otherwise. `journal-finalize` blocks on `"missing"`. |
| `format_checker_checked_at` | no | ISO 8601 timestamp of the last probe. Useful when the user creates the checker later and re-runs `journal-init` to refresh the status. |

When status is `"missing"`, `journal-init` also appends a `format_checker` entry to `artifacts.warnings` so the gap shows up in status reports. Re-running `journal-init` (or any refresh step) should re-probe and flip `"missing"` → `"ready"` once the user has created the skill via `/skill-creator`.

### Progress tracking

| Field | Default | Meaning |
|---|---|---|
| `current_step` | `0` | Highest step completed. Updated by each downstream skill on success. |
| `review_round` | `0` | Incremented by `journal-review` each pass. |
| `created_at` | ISO 8601 | UTC or local with offset |

### Artifact inventory

- `artifacts.from_research` / `artifacts.from_algorithm`: object mapping artifact key (see `artifact_inventory.md` for the complete key list) to resolved path. Missing artifacts map to `null`.
- `artifacts.warnings`: list of non-blocking issues. Each entry: `{artifact, issue, detail}`.
- `artifacts.critical_missing`: list of blocking gaps. Each entry: `{artifact, path_checked, suggested_command}`. If non-empty, downstream steps should refuse to run until resolved.

## Versioning

If the schema changes, add a top-level `"schema_version": "1.1"` field. Downstream skills should read it and migrate or warn. Current schema: unversioned (implicitly v1.0).

## Path Conventions

- All paths stored **relative to project root**, not absolute. Portable across machines.
- Directory paths end in `/`. File paths don't.
- Use forward slashes, even on Windows (BibTeX and LaTeX tooling expect them).
