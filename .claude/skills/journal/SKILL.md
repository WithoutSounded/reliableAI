---
name: journal
description: "Meta-skill that orchestrates the full Journal Writing Agent pipeline — a 7-step manuscript production system from session init to a submission-ready bundle (LaTeX for Overleaf + bilingual Markdown for Obsidian). Use this skill whenever the user says '/journal', 'start writing a paper', 'write the manuscript', 'run the journal pipeline', '寫論文流程', '產生投稿稿', '走 journal pipeline', or wants to chain multiple journal-* steps together. Also trigger on '/journal new', '/journal continue', '/journal status', '/journal step N', '/journal review' (review-loop shortcut), '/journal import' (bring an existing draft in as step2_draft_v1/), or any intent to manage the overall manuscript workflow rather than a single step. This is the conductor — it decides which sub-skill to invoke, when to pause for human checkpoints, and when to loop back through review/revise. It does NOT duplicate sub-skill logic. NOT for single-step work (use the matching journal-* sub-skill directly), NOT for research/literature work (use /research)."
---

# Journal — Meta-Skill Orchestrator

You are the conductor of a 7-step journal writing pipeline. Your job is to manage the flow between sub-skills, track session state, enforce human-in-the-loop checkpoints, and keep the user oriented on where they are and what comes next.

You do NOT duplicate sub-skill logic. When it's time to execute a step, you invoke the corresponding sub-skill (via the Skill tool, or by reading its SKILL.md and following its instructions directly). Your value is orchestration: knowing which step to run, what files to check, when to pause, and how to resume — including the Step 3 ↔ Step 4 review loop.

## Commands

| Command | Action |
|---------|--------|
| `/journal new` | Start fresh from Step 0. If research/algorithm sessions or target journal aren't supplied, auto-scan and ask. |
| `/journal continue` | Resume from where the session left off. Reads `current_step` and `review_round` from `step0_session_config.json`. |
| `/journal step <N>` | Re-run a specific step (e.g., `/journal step 3` to re-review the latest draft). Useful after checkpoint feedback or if a step needs a redo. |
| `/journal status` | Show progress: completed steps, current review round, pending checkpoints, artifact list. |
| `/journal review` | Shortcut for one more review pass: increment `review_round`, run Step 3 on the latest draft, then pause at Checkpoint 2. |
| `/journal import` | Bring an existing draft (e.g., from `8_Manuscript/`) in as `step2_draft_v1/` so the pipeline can pick up at Step 3. See "Importing an Existing Draft" below. |

If the user just says `/journal` with no subcommand: `/journal continue` if a session exists, else `/journal new`.

## Pipeline Overview

| Step | Sub-Skill | Produces | Checkpoint After? |
|------|-----------|----------|-------------------|
| 0 | `journal-init` | `step0_session_config.json` | No |
| 1 | `journal-blueprint` | `step1_preprocess/`, `step1_blueprint.md` | **Checkpoint 1: 藍圖核准** |
| 2 | `journal-draft` | `step2_draft_v1/{section}.tex`, `step2_global_config.json`, `_sliding_window_state.json` | No |
| 3 | `journal-review` | `step3_review_r{N}.json` | **Checkpoint 2: 審閱確認** |
| 4 | `journal-revise` | `step4_draft_v{N+1}/`, `_revision_log.md` | No (loops back to Step 3 if user requests "再審一輪") |
| 5 | `journal-polish` | `step5_polished/{section}.tex`, `golden_thread_report.md` | **Checkpoint 3: 終稿確認** |
| 6 | `journal-finalize` | `step6_final/latex/`, `step6_final/bilingual/`, `final_check_report.md`, `format_check_report.md` | No (pipeline complete) |

### Format-checker dependency

Every journal has a designated format-checker skill (e.g., `aei-checker` for Advanced Engineering Informatics). Step 0 (`journal-init`) resolves the expected skill name from `references/target_journals.md`, probes whether it exists on disk, and freezes `format_checker_skill` + `format_checker_status` into the session config.

- If the checker is **missing** at Step 0, `journal-init` prints a prominent warning with the expected skill slug and a `/skill-creator` nudge — but does *not* block; Steps 1–5 can proceed while the user authors the checker in parallel.
- At Step 6, `journal-finalize`'s Phase 6.0 re-probes the filesystem. If the checker is still missing, **finalize hard-blocks** — no `step6_final/` output is written. The user must create the skill (reference: `aei-checker`) and re-run `/journal finalize`.
- When the checker is present, Phase 6d invokes it on the assembled LaTeX package. Its verdict drives the overall `READY / REVIEW NEEDED / BLOCKED` outcome of the pipeline.

If a user gets blocked here mid-flow, the right move is not to skip — it's to spawn `/skill-creator` to create the checker (using the suggested slug from the error message), then come back to `/journal continue`.

## Session Management

### Finding the Active Session

Sessions live under `Journal/{session_id}_{paper_slug}/`. To find the active one:

1. List directories in `Journal/`.
2. For each, read `step0_session_config.json` and check `current_step` + `review_round`.
3. If multiple sessions exist and the user didn't specify, list them and ask which to continue.

If `Journal/` doesn't exist, only `/journal new` and `/journal import` are valid.

### Tracking Progress

`current_step` and `review_round` in `step0_session_config.json` are the single source of truth. When resuming, **trust files over the config** — if a downstream artifact exists but the config thinks the step isn't done, the config is stale and you should reconstruct progress from file existence and report the reconstruction to the user.

Sub-skills are responsible for incrementing `current_step` after they finish; if one didn't, update it yourself.

### File Existence Verification

Before running any step, verify its declared inputs exist (each sub-skill's SKILL.md lists them). If something is missing, name the missing artifact and the earlier step that produces it — don't push forward and let the sub-skill fail mid-execution.

## Checkpoint Logic

Checkpoints are gates where the pipeline **must pause** for human review. Do not auto-advance past one. The user's input here shapes everything downstream.

### Checkpoint 1: 藍圖核准 (After Step 1)

**Review**: narrative arc, evidence mapping (no orphan figures, no unsupported claims), per-section word budget vs. journal limit, writing order.
**Present**: condensed bilingual summary of `step1_blueprint.md` — Golden Thread, section profiles table, evidence map, writing order.
**Proceed**: on "approved / 通過 / 核准 / OK", run Step 2. If user requests changes, edit `step1_blueprint.md` (and `step1_preprocess/` if a preprocess artifact is wrong) before drafting.

### Checkpoint 2: 審閱確認 (After Step 3)

**Review**: every flag in `step3_review_r{N}.json` — accept, override with custom instruction, add new flags, or dismiss false positives.
**Present**: bilingual flag table grouped by severity (critical → major → minor), with location quote and proposed fix.
**Proceed**: two paths.
- **"修訂" / "proceed to revise"** → run Step 4, then Step 5 (skip another review).
- **"再審一輪" / "another review round"** → run Step 4, increment `review_round`, then loop back to Step 3 with `step4_draft_v{N+1}/` as input. Typical: 1–2 rounds suffice; 3+ rounds suggest a blueprint-level problem — surface that observation to the user and ask whether they want to revisit Step 1 instead of looping further.

Apply user overrides by writing them into the same `step3_review_r{N}.json` (e.g., add an `"override"` field on the flagged item) before invoking `journal-revise`, so the revision context is self-contained.

### Checkpoint 3: 終稿確認 (After Step 5)

**Review**: polished draft (bilingual Markdown is faster to read than .tex) + Golden Thread report.
**Present**: TL;DR of `golden_thread_report.md` and per-section "what changed" highlights from polish.
**Proceed**: on "通過 / approved", run Step 6. If user requests targeted fixes, re-run Step 5 on just the affected section (`/journal step 5` with a section filter), don't loop back to Step 3 unless content (not prose) needs changing.

## Executing a Step

When it's time to run a step, invoke the matching sub-skill — don't reimplement.

**Invocation**: prefer the Skill tool with the sub-skill's name (`journal-init`, `journal-blueprint`, etc.). If the Skill tool isn't available or the sub-skill doesn't trigger, read its `SKILL.md` and follow the procedure inline.

**Between steps without a checkpoint** (Step 0→1, Step 2→3, Step 4→5 unless looping, Step 5→6):
1. Verify the previous step's outputs exist.
2. Update `current_step` if the sub-skill didn't.
3. One sentence to the user about what completed and what's next.
4. Continue immediately.

**Between steps with a checkpoint**:
1. Verify outputs exist.
2. Present the checkpoint review material (bilingual).
3. **Stop. Wait.** Do not run the next sub-skill until the user responds.
4. Apply the user's edits (modify blueprint / annotate review JSON / target a polish re-run).
5. Proceed.

## The Review Loop (Step 3 ↔ Step 4)

This is the journal pipeline's distinctive control flow. Treat it as a deliberate cycle, not a stuck state:

```
Step 2 (draft v1)
  └─> Step 3 (review r1) ──> CHECKPOINT 2
                                 │
              ┌───── "再審一輪" ───┐
              ▼                    │
         Step 4 (draft v2)        │
              └─> Step 3 (review r2) ──> CHECKPOINT 2 ──┘
                                                         │
                                                    "修訂"
                                                         │
                                                         ▼
                                  Step 4 (final revise) → Step 5 → CP 3 → Step 6
```

`review_round` is the loop counter. Each Step 3 run produces `step3_review_r{N}.json`; each Step 4 run produces `step4_draft_v{N+1}/`. The user controls loop exit at Checkpoint 2.

## Importing an Existing Draft

If the user already has a manuscript draft they want to bring into the pipeline (e.g., the project's `8_Manuscript/` folder), use `/journal import`. This shortcut creates a synthetic Step 0–2 state so review/revise/polish/finalize can run on it.

Procedure:

1. Run `journal-init` normally (Step 0) to capture upstream Research + Algorithm artifacts and target journal.
2. Run `journal-blueprint` (Step 1) — even with an existing draft, the blueprint is needed because Step 3 review checks the draft against the blueprint's evidence map and section profiles. If the user objects to spending time here, at minimum produce `step1_preprocess/` (figure_captions, table_captions, notation_glossary) — Step 3 cannot fact-check without these.
3. **Convert the existing draft** into `step2_draft_v1/`:
   - One `.tex` file per section, named per blueprint (`01_introduction.tex` … `06_conclusion.tex`, `00_abstract.tex` if drafted).
   - Strip Markdown wrappers around `\begin{...}\end{...}` blocks; keep LaTeX as-is.
   - If the source is mixed Markdown/LaTeX (e.g., `8_Manuscript/2_Methods (LaTex).md`), extract the LaTeX content and discard pure-Markdown commentary.
4. Generate `step2_global_config.json` from the blueprint's section profiles + any `DRAFTER_GLOBAL_CONFIG.md` the user provides.
5. Build `_sliding_window_state.json` by writing 2–3 sentence summaries per section from the imported text (these enable downstream tools to reason about the paper without re-reading every section).
6. Set `current_step: 2`, `review_round: 0`. Now `/journal continue` will proceed to Step 3.

Tell the user explicitly which sections were imported, which were missing, and whether any LaTeX extraction was lossy. Imported drafts often have inconsistent figure/equation labels — flag this so they're not surprised when Step 3 produces many `MISSING_LABEL` flags on the first review pass.

## Status Report Format

When the user runs `/journal status`:

```
## Journal Pipeline Status / 論文寫作流程狀態

**Session / 工作階段**: {session_id}_{paper_slug}
**Target journal / 目標期刊**: {journal_name} (limit: {word_limit} words)
**Current step / 目前步驟**: {N} — {step_name}
**Review round / 審閱輪次**: {review_round}
**Started / 開始時間**: {timestamp}

| Step | Sub-skill | Status | Latest artifact |
|------|-----------|--------|-----------------|
| 0 | journal-init | Done | step0_session_config.json |
| 1 | journal-blueprint | Done | step1_blueprint.md (CP1 approved) |
| 2 | journal-draft | Done | step2_draft_v1/ |
| 3 | journal-review | Done (round 1) | step3_review_r1.json — 12 flags |
| 4 | journal-revise | Pending | — |
| 5 | journal-polish | — | — |
| 6 | journal-finalize | — | — |

**Next action / 下一步**: {what to do next, including any pending checkpoint}
```

Determine status from file existence, not just `current_step` — files may have been deleted or partially produced.

## Error Recovery

- **Step fails partway**: list which output files exist vs. expected, report specifics, suggest `/journal step N` to retry. Do not skip ahead.
- **Config corrupted / missing**: reconstruct `current_step` and `review_round` from file existence (highest `step3_review_r{N}.json` and `step4_draft_v{N}/` indices), regenerate `step0_session_config.json`, report what was reconstructed.
- **Sub-skill won't trigger via Skill tool**: read its SKILL.md from `.claude/skills/{name}/SKILL.md` and execute the procedure inline.
- **User asks to skip a step**: warn that downstream depends on it. If they insist, note the skip in session config and let the next step's prerequisite check decide whether it can proceed.
- **3+ review rounds with similar flags**: this signals a blueprint-level problem (e.g., section was assigned the wrong evidence). Recommend `/journal step 1` to revisit the blueprint instead of continuing to loop.

## Bilingual Communication

All user-facing communication is bilingual (English + 繁體中文), matching the sub-skills:
- Section headings, status reports, checkpoint prompts: bilingual.
- Technical terms: English with Chinese explanation on first mention.
- File paths and command names stay English.

## Edge Cases

- **Multiple concurrent journal sessions**: each is independent; if more than one exists, ask which to act on.
- **User wants to re-run a completed step**: fine — `/journal step N` overwrites that step's outputs. Warn that downstream artifacts may go stale; recommend re-running them too.
- **Token-heavy steps**: Steps 1, 2, 5 are the most expensive (large context, full-paper reasoning). Give the user a heads-up before starting and offer to split across conversations via `/journal continue`.
- **User wants to inspect, not advance**: respect that. Don't auto-run the next step on `/journal status` or read-only requests.
- **Upstream artifacts missing at Step 0**: `journal-init` reports them with `path_checked` and `suggested_command`. Surface this verbatim — don't silently fall back; the user needs to decide whether to fix upstream or proceed with a known gap.
