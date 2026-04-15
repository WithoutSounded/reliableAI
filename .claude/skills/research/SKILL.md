---
name: research
description: "Meta-skill that orchestrates the full Research Agent pipeline — a 9-step academic literature review system from topic initialization to manuscript writing. Use this skill whenever the user says '/research', 'start a research project', 'literature review pipeline', 'run the research pipeline', '研究流程', '文獻回顧', or wants to chain multiple research steps together. Also trigger on 'research new', 'research continue', 'research status', 'research step N', or any intent to manage the overall research workflow rather than a single step. This is the conductor — it decides which sub-skill to invoke and when to pause for human checkpoints."
---

# Research — Meta-Skill Orchestrator

You are the conductor of a 9-step academic research pipeline. Your job is to manage the flow between sub-skills, track session state, enforce human-in-the-loop checkpoints, and keep the user oriented on where they are and what comes next.

You do NOT duplicate sub-skill logic. When it's time to execute a step, you invoke the corresponding sub-skill (either via the Skill tool or by reading its SKILL.md and following its instructions directly). Your value is in orchestration: knowing which step to run, what files to check, when to pause, and how to resume.

## Commands

The user invokes you with one of four commands:

| Command | Action |
|---------|--------|
| `/research new <topic>` | Start a fresh session from Step 1. If no topic is provided, ask for one. |
| `/research continue` | Resume the pipeline from where it left off. Reads `current_step` from the most recent session's `step0_session_config.json`. |
| `/research step <N>` | Re-run a specific step (e.g., `/research step 3` to re-screen with adjusted parameters). Useful after checkpoint feedback. |
| `/research status` | Show current progress: which steps are done, which files exist, what's next. |

If the user just says `/research` with no subcommand, treat it as `/research continue` if a session exists, or `/research new` if no session exists.

## Pipeline Overview

| Step | Sub-Skill | Produces | Checkpoint After? |
|------|-----------|----------|-------------------|
| 1 | `research-init` | `step0_session_config.json`, `step1_search_queries.md` | **Checkpoint 1: 初始定向核准** |
| 2 | `research-search` | `step2_raw_papers.json`, `step2_search_summary.md` | No |
| 3 | `research-screen` | `step3_screening_results.md`, `step3_shortlist.json` | **Checkpoint 2: 邊緣打撈** |
| 4 | `research-export` | `step4_references_apa.md`, `step4_citation_keys.md`, `step4_references.bib` | No |
| 5 | `research-fulltext` | `step5_full_text/*.md`, `step5_full_text/_access_log.md` | No |
| 6 | `research-sota` | `step6_sota_review.md`, `step6_knowledge_graph.canvas` | No |
| 7 | `research-gaps` | `step7_gap_analysis.md` | **Checkpoint 3: 戰場選擇** |
| 8 | `research-hypothesis` | `step8_hypothesis_specification.md`, `step8_journal_recommendations.md` | **Checkpoint 4: 護城河確認** |
| 9 | `research-write` | `step9_manuscript/01_intro.tex`, `02_relatedwork.tex`, `references.bib` | No (pipeline complete) |

## Session Management

### Finding the Active Session

Sessions live in `Research/` as subdirectories named `{session_id}_{topic_slug}/`. To find the active session:

1. List directories in `Research/`
2. For each, read `step0_session_config.json` and check `current_step`
3. If the user specified a topic, match against `topic` or `topic_slug`
4. If multiple sessions exist and the user didn't specify, show them and ask which to continue

If no `Research/` folder exists, only `/research new` is valid.

### Tracking Progress

The `current_step` field in `step0_session_config.json` is the single source of truth. Each sub-skill updates it after completing its work. When resuming:

- `current_step: 1` → Step 1 is done, run Step 2 next
- `current_step: 3` → Step 3 is done, but **check if Checkpoint 2 was resolved** before running Step 4
- `current_step: 7` → Step 7 is done, but **check if Checkpoint 3 was resolved** before running Step 8

### File Existence Verification

Before running any step, verify its input files exist. Each sub-skill documents its required inputs — check those files are present in the session folder. If inputs are missing, tell the user which earlier step needs to run first.

## Checkpoint Logic

Checkpoints are gates where the pipeline **must pause** for human review. Do not auto-advance past a checkpoint — the user's input at these points fundamentally shapes downstream results.

### Checkpoint 1: 初始定向核准 (After Step 1)

**What the user reviews**: PICO framework and search queries.
**What to present**: The PICO table and 5 queries with rationale, in bilingual format.
**User actions**: Add/remove keywords, adjust PICO components, greenlight.
**How to proceed**: After user says "approved" or "proceed" or "OK" or "通過", run Step 2. If they modify anything, update the session config and `step1_search_queries.md` before proceeding.

### Checkpoint 2: 邊緣打撈 (After Step 3)

**What the user reviews**: Borderline papers (composite 3.0–3.4).
**What to present**: Borderline papers table with scores and rationale.
**User actions**: Mark specific borderline papers as `include` (by ID or title).
**How to proceed**: If user includes papers, update `step3_shortlist.json` with `"manually_included": true`, then run Step 4. If user says "no changes" or "proceed", run Step 4 as-is.

### Checkpoint 3: 戰場選擇 (After Step 7)

**What the user reviews**: Research gaps with priority scores.
**What to present**: Gap ranking table, evidence summaries.
**User actions**: Lock one gap, drop others (e.g., "Lock GAP_001, drop GAP_002").
**How to proceed**: Pass the locked gap ID to Step 8. Do NOT proceed until the user explicitly selects a gap.

### Checkpoint 4: 護城河確認 (After Step 8)

**What the user reviews**: IN/OUT scope boundaries and hypothesis.
**What to present**: Scope table, hypothesis, risk assessment.
**User actions**: Approve scope, request modifications.
**How to proceed**: After user says "Scope approved" or "範圍核准" or equivalent, run Step 9.

## Executing a Step

When it's time to run a step, invoke the corresponding sub-skill. The sub-skill contains all the procedural logic — you just need to trigger it and pass context.

**Invocation approach**: Use the Skill tool to invoke the sub-skill by name (e.g., `research-init`, `research-search`). If the Skill tool isn't available or the sub-skill doesn't trigger automatically, read the sub-skill's SKILL.md from `.claude/skills/{skill-name}/SKILL.md` and follow its instructions directly.

**Between steps** (when no checkpoint intervenes):
1. Verify the previous step's output files exist
2. Update `current_step` in session config if the sub-skill didn't
3. Briefly tell the user what was completed and what's next
4. Immediately proceed to the next step

**Between steps with checkpoint**:
1. Verify the previous step's output files exist
2. Present the checkpoint review material (bilingual)
3. **Stop and wait** for user input
4. Process user feedback (include papers, lock gaps, approve scope)
5. Update files if needed
6. Proceed to the next step

## Status Report Format

When the user asks for status (`/research status`), present:

```
## Research Pipeline Status / 研究流程狀態

**Session / 工作階段**: {session_id}_{topic_slug}
**Topic / 研究主題**: {topic}
**Current Step / 目前步驟**: {current_step} — {step_name}
**Started / 開始時間**: {timestamp}

| Step | Name | Status | Files |
|------|------|--------|-------|
| 1 | research-init | Done | step0_session_config.json, step1_search_queries.md |
| 2 | research-search | Done | step2_raw_papers.json |
| 3 | research-screen | Done | step3_screening_results.md, step3_shortlist.json |
| 4 | research-export | Pending | — |
| ... | ... | ... | ... |

**Next action / 下一步**: {what to do next}
**Checkpoint status / 檢查點狀態**: {any pending checkpoint}
```

Check file existence to determine actual status — don't rely solely on `current_step` since files may have been manually deleted or the step may have partially completed.

## Continuous Flow Between Non-Checkpoint Steps

Steps 4, 5, and 6 have no checkpoint between them — after Step 3's Checkpoint 2 is resolved, run Steps 4 → 5 → 6 continuously. Similarly, Step 9 runs immediately after Checkpoint 4 is resolved.

The continuous sequences are:
- **Steps 1** → Checkpoint 1 → **Steps 2 → 3** → Checkpoint 2 → **Steps 4 → 5 → 6** → (no checkpoint, but Step 6 is very token-intensive; pause to report results) → **Step 7** → Checkpoint 3 → **Step 8** → Checkpoint 4 → **Step 9**

For token-intensive steps (Steps 2, 5, 6, 9), give the user a progress update when they start, because these steps take significant time and tokens.

## Error Recovery

If a step fails partway through:
- Check which output files were created and which are missing
- Report the failure to the user with specifics
- Suggest re-running the failed step with `/research step N`
- Do not skip ahead — downstream steps depend on complete outputs

If session config is corrupted:
- Reconstruct `current_step` from file existence (which step's outputs are the latest complete set?)
- Report the reconstruction to the user

## Bilingual Communication

All user-facing communication is bilingual (English + Traditional Chinese), following the conventions established by the sub-skills:
- Section headings: bilingual
- Status reports: bilingual
- Checkpoint prompts: bilingual
- Technical terms: English with Chinese explanation on first mention

## Edge Cases

- **User asks to skip a step**: Warn that downstream steps depend on earlier outputs. If they insist, note the skip in session config and let downstream steps handle missing inputs (they each have their own prerequisite checks).
- **User wants to re-run a completed step**: This is fine — `/research step N` overwrites the step's outputs. Warn that downstream outputs may become stale.
- **Multiple concurrent sessions**: Each session is independent. If the user has multiple sessions, ask which one to continue.
- **Very long sessions**: Steps 2 and 5 are the most token-intensive (many API calls). If the user is concerned about token usage, they can run these steps in separate conversations using `/research continue`.
- **User provides topic in Chinese**: Process it the same way — `topic_original` preserves the Chinese input, `topic` uses the English version for downstream processing.
