---
name: journal-init
description: "Step 0 of the Journal Writing Agent pipeline — the REQUIRED first step before any other journal-* skill. Bootstraps a manuscript session by auto-scanning upstream Research + Algorithm folders, inventorying 15 expected artifacts (marking critical_missing with path_checked + suggested_command per gap), resolving target-journal specs (template, word_limit, citation_style, section_structure, writing_order) via the bundled cheatsheet → journal_recommendations.md → WebSearch fallback chain, and freezing everything into step0_session_config.json under Journal/{YYYYMMDD}_{paper_slug}/. Trigger aggressively whenever the user says 'start writing a paper', 'open a journal session', 'initialize/init the manuscript', '/journal-init', OR mentions a target venue (IEEE TNSRE, NeuroImage, Advanced Engineering Informatics, Computers in Biology and Medicine, Nature Methods, TPAMI, TBME, JNE, Pattern Recognition, etc.) in a drafting/submission context, OR references a Research/Algorithm session they want to turn into a paper. Do NOT skip this step — downstream skills (journal-blueprint, journal-draft, journal-review, journal-revise, journal-polish, journal-finalize) all read step0_session_config.json and will fail or silently use wrong formatting without it."
---

# Journal Init — Step 0 of Journal Writing Agent Pipeline

You are bootstrapping a new journal writing session. The job: locate the user's upstream Research + Algorithm sessions, verify all the artifacts the downstream pipeline will need, extract the target journal's formatting rules, and freeze everything into one config file.

**Why this matters.** Every downstream journal skill (`journal-blueprint`, `journal-draft`, `journal-review`, etc.) reads `step0_session_config.json` to find source material and enforce journal-specific constraints. Missing artifacts discovered here become blocking errors later — catch them now, not during drafting. A clean init saves hours of thrashing downstream.

## Inputs You Need

Three pieces of information — collect them from the conversation or ask:

1. **Research session path** — where the literature review + references + intro draft live
2. **Algorithm session path** — where the architecture spec + figures + experiment report live
3. **Target journal** — e.g., "IEEE TNSRE", "NeuroImage", "Advanced Engineering Informatics"

If any are missing, auto-scan the project root for candidates first (see Procedure §1), then ask the user to confirm or pick. Don't interrogate — propose the best match and let them override.

## Procedure

### 1. Auto-scan for upstream sessions

Before asking the user, look around. The project root typically has:

- `Research/{session_id}_{slug}/` — multi-session layout (standard)
- `0_Research/` — legacy single-session layout (some projects)
- `Algorithm/{session_id}_{slug}/` — multi-session layout

Use `Glob` to find candidates:

```
Research/*/step0_session_config.json
0_Research/step0_session_config.json
Algorithm/*/step0_session_config.json
```

For each candidate, read its `step0_session_config.json` to confirm it's a real session and grab its topic/slug. Present the matches:

```
Found upstream sessions:
  Research: 0_Research/ (topic: "multimodal EEG+gaze for social interaction")
  Algorithm: Algorithm/20260104_multimodal-social-interaction/ (topic: "fuzzy gating fusion")

Target journal? (required)
```

If multiple sessions exist in a folder, list them and ask which one. If zero found, tell the user the expected locations and ask them to point you at the paths manually.

### 2. Generate session ID and folder

- **session_id**: today's date as `YYYYMMDD` (e.g., `20260415`). Use the real current date.
- **paper_slug**: lowercase hyphenated, max 40 chars, derived from the core contribution. Good slugs describe the paper's thesis, not just the domain — e.g., `fuzzy-gating-eeg-gaze-social` beats `eeg-paper`. Ask the user if it's unclear; a 10-second check here saves renaming later.
- **folder**: `Journal/{session_id}_{paper_slug}/`

Create the folder. Don't write the config yet — finish the inventory first so you can write it all in one pass.

### 3. Inventory upstream artifacts

For every artifact the downstream pipeline expects, check whether it exists at the expected path. Record the result in the `artifacts` block of the config.

**Required artifacts** (full list in [references/artifact_inventory.md](references/artifact_inventory.md)):

From **Research session**:

| Artifact | Path (relative to research_session) | Used by |
|---|---|---|
| SOTA review | `step6_sota_review.md` | Intro, Related Work, Discussion |
| Gap analysis | `step7_gap_analysis.md` | Intro |
| Hypothesis spec | `step8_hypothesis_specification.md` | Intro, Methods |
| Journal recommendations | `step8_journal_recommendations.md` | Target journal validation |
| References BibTeX | `step4_references.bib` | Citation pool (all sections) |
| Citation key lookup | `step4_citation_keys.md` | Citation accuracy checks |
| Full-text store | `step5_full_text/` | Deep citation accuracy checks (review) |
| Intro draft (reference) | `step9_manuscript/01_intro.tex` | Cross-agent validation in Step 2 |
| Related Work draft (reference) | `step9_manuscript/02_relatedwork.tex` | Cross-agent validation in Step 2 |

From **Algorithm session**:

| Artifact | Path (relative to algorithm_session) | Used by |
|---|---|---|
| Architecture spec | `step1_architecture_spec.md` | Methods |
| Ablation matrix | `step1_ablation_matrix.md` | Methods, Results |
| Analysis summary | `step4_analysis_summary.md` | Results, Discussion |
| Figure catalog | `step5_figure_catalog.md` | Figure/table inventory (all sections) |
| Experiment report | `step6_experiment_report.md` | Results, Discussion |
| Figures directory | `8_Manuscript/figures/` (project root) | Actual figure files for LaTeX |

**Use the helper script** — it handles scanning and missing-file reporting consistently:

```
python .claude/skills/journal-init/scripts/inventory_artifacts.py \
    --research-session <research_path> \
    --algorithm-session <algorithm_path> \
    --figures-dir 8_Manuscript/figures/ \
    --output /tmp/journal_inventory.json
```

The script returns a JSON with `found`, `missing`, and `severity` (critical vs. optional) per artifact. Read it back, present the missing-items list to the user, and decide:

- **Critical missing** (e.g., no `step4_references.bib`, no `step1_architecture_spec.md`): Flag loudly. Downstream will fail without these. Offer to abort or continue with warnings recorded.
- **Optional missing** (e.g., no `step5_full_text/`): Note in the config under `artifacts.warnings` and continue. Citation accuracy will skip deep checks, but drafting can proceed.

Don't silently drop missing items — the whole point of this step is catching them now.

### 4. Extract target journal formatting requirements

Look up the target journal's submission rules. For well-known journals, use the bundled cheatsheet at [references/target_journals.md](references/target_journals.md) — it has the common ones (IEEE TNSRE, IEEE TBME, NeuroImage, Nature Methods, Advanced Engineering Informatics, Pattern Recognition, etc.) with word limits, section structures, LaTeX templates, citation styles.

If the journal is in the cheatsheet, copy the relevant fields. If it's not, and the user has `step8_journal_recommendations.md` from Research, read that — it often contains the specs. Otherwise, ask the user or offer to WebSearch the journal's author guidelines.

Fields to capture:

```json
"target_journal": "Advanced Engineering Informatics",
"publisher": "Elsevier",
"template": "CAS LaTeX Double-Column",
"page_target": "12-15 pages",
"word_limit": 8000,
"section_structure": ["Abstract", "Introduction", "Related Work", "Methods", "Results", "Discussion", "Conclusion"],
"citation_style": "elsarticle-num",
"abstract_word_limit": 250
```

**Section structure variations**: some journals merge Methods+Results (Nature style), some require "Background" instead of "Introduction", some forbid a standalone Related Work section. Use the journal's actual convention, not a default. The cheatsheet notes these.

**Writing order** stays the default unless the user overrides: `Methods → Results → Introduction → Related Work → Discussion → Conclusion → Abstract`. This order is deliberate (Methods/Results are most concrete; Abstract is written last because it summarizes everything), so keep it unless there's a specific reason to change.

### 4.5. Resolve the format-checker skill

Every target journal has a designated format-checker skill — a separate skill that verifies submission-guideline compliance (e.g., Elsevier CAS front matter, highlight length, CRediT, bib DOIs). `journal-finalize` (Step 6) **blocks** unless this skill exists on disk, so we detect the gap **now** and nudge the user to create it early.

Procedure:

1. **Resolve the expected skill name.** Read `format_checker_skill` from the journal's entry in `references/target_journals.md`. If the journal isn't in the cheatsheet, synthesize a slug from its `short_name` — lowercase-hyphenated + `-checker` (e.g., "Computers in Biology and Medicine" → `cbm-checker`). Always set a value; never leave it null.

2. **Probe the filesystem.** Check whether `.claude/skills/{format_checker_skill}/SKILL.md` exists (also probe `~/.claude/skills/{format_checker_skill}/SKILL.md` for user-level skills). Use `Glob` rather than assuming a fixed skills root — some projects have local skills and some ship global ones.

3. **Set status in the config:**
   - `format_checker_status: "ready"` — skill found. Record `format_checker_checked_at` as now.
   - `format_checker_status: "missing"` — skill not found. Record the timestamp, and also append to `artifacts.warnings`:
     ```json
     {
       "artifact": "format_checker",
       "issue": "skill_missing",
       "detail": "Expected skill '{name}' for '{target_journal}' not found under .claude/skills/. journal-finalize will block until it's created. Run /skill-creator to scaffold it."
     }
     ```

4. **Surface the gap loudly to the user.** A missing format checker is not a silent warning — it's something the user must act on before Step 6. Print a dedicated block in the Step 6 summary (see §6) with:
   - The journal name
   - The expected skill slug (so they know exactly what to name it when they run `/skill-creator`)
   - The concrete next action: "Run `/skill-creator` and create a skill named `{slug}` that verifies {journal}'s submission guidelines. Use `aei-checker` as a reference implementation — it's the canonical example."
   - A reminder that `journal-finalize` will refuse to run without it

Do **not** block `journal-init` itself on a missing checker — the user still needs Steps 1–5 to produce a draft before a checker is useful. The point is early visibility, not early blocking. Step 6 is where the hard gate lives.

### 5. Write `step0_session_config.json`

Assemble the final config using [references/config_schema.md](references/config_schema.md) as the authoritative schema. Key fields:

```json
{
  "session_id": "20260415",
  "paper_slug": "fuzzy-gating-eeg-gaze-social",
  "research_session": "0_Research/",
  "algorithm_session": "Algorithm/20260104_multimodal-social-interaction/",
  "target_journal": "Advanced Engineering Informatics",
  "publisher": "Elsevier",
  "template": "CAS LaTeX Double-Column",
  "page_target": "12-15 pages",
  "word_limit": 8000,
  "abstract_word_limit": 250,
  "citation_style": "elsarticle-num",
  "section_structure": ["Abstract", "Introduction", "Related Work", "Methods", "Results", "Discussion", "Conclusion"],
  "writing_order": ["Methods", "Results", "Introduction", "Related Work", "Discussion", "Conclusion", "Abstract"],
  "format_checker_skill": "aei-checker",
  "format_checker_status": "ready",
  "format_checker_checked_at": "2026-04-15T10:00:00+08:00",
  "current_step": 0,
  "review_round": 0,
  "created_at": "2026-04-15T10:00:00+08:00",
  "artifacts": {
    "from_research": { /* resolved paths, or null if missing */ },
    "from_algorithm": { /* resolved paths, or null if missing */ },
    "warnings": [ /* list of missing optional artifacts */ ],
    "critical_missing": [ /* list of missing critical artifacts, if any */ ]
  }
}
```

**Path convention**: store paths as **relative to the project root**, not absolute. This keeps the config portable across machines.

Write the file to `Journal/{session_id}_{paper_slug}/step0_session_config.json`.

### 6. Report to the user

Show a concise summary inline:

```
✓ Session created: Journal/20260415_fuzzy-gating-eeg-gaze-social/
✓ Research: 0_Research/ (9/9 artifacts found)
✓ Algorithm: Algorithm/20260104_multimodal-social-interaction/ (6/6 artifacts found)
✓ Target journal: Advanced Engineering Informatics (Elsevier)
  - Word limit: 8000
  - Template: CAS LaTeX Double-Column
✓ Format checker: aei-checker (ready)

⚠ Warnings:
  - step5_full_text/ has only 42/60 citation keys resolved — deep citation checks will skip 18 entries

Next: run /journal-blueprint to preprocess materials and design the paper blueprint.
```

When the format-checker skill is **missing**, replace the `✓ Format checker` line with a prominent block and keep it above the "Next" line — the user needs to see this before moving on:

```
🛑 Format checker MISSING
  - Target journal 'NeuroImage' expects skill 'neuroimage-checker'
  - Probed:  .claude/skills/neuroimage-checker/SKILL.md  (not found)
            ~/.claude/skills/neuroimage-checker/SKILL.md (not found)
  - journal-finalize (Step 6) will BLOCK until this skill is authored.
  - Action: run /skill-creator to scaffold 'neuroimage-checker'.
            Reference implementation: .claude/skills/aei-checker/
  - You can still run /journal-blueprint → /journal-draft → /journal-review → /journal-revise → /journal-polish meanwhile;
    just make sure 'neuroimage-checker' exists before /journal-finalize.
```

If any **critical** artifacts were missing, surface that *before* the "next step" line — the user needs to resolve those first.

## Output

- `Journal/{session_id}_{paper_slug}/step0_session_config.json` — session metadata, artifact inventory, target journal specs

No other files at this stage. Downstream steps write their own step-prefixed outputs.

## Edge Cases

- **User has no Research or Algorithm session yet**: Tell them Step 0 presupposes both. Suggest running `/research` or `/algo` first. Don't create a half-initialized journal session.
- **Multiple Research sessions match**: List them and ask which is canonical for this paper. Research sessions are usually topic-wide; one paper might use a subset.
- **Target journal not in the cheatsheet and no `step8_journal_recommendations.md`**: Offer to WebSearch the journal's author guidelines. If the user declines, capture placeholder values (`word_limit: null`, `template: "unknown"`) and add a warning — downstream steps will use conservative defaults.
- **Session folder already exists**: Don't silently overwrite. Read the existing config, tell the user, and ask: resume (keep config, advance `current_step`), re-init (backup old config to `.bak`, write fresh), or pick a new slug.
- **Non-standard folder layout**: If the user's Research/Algorithm sessions live somewhere unusual, accept explicit paths they provide. Store them verbatim in the config.

## Bilingual Output

The downstream pipeline produces bilingual content (EN + 繁中), but the config file itself stays in English — it's machine-readable metadata. When reporting to the user in conversation, feel free to mix EN + 繁中 naturally; many users run this skill in a Chinese-speaking context.
