# Sliding Window Protocol

The sliding window is the mechanism that keeps the draft internally coherent even though sections are drafted in a non-reading order. The core idea: before drafting any subsection, load just enough of the *adjacent-in-reading-order* subsections to write a transition that will read naturally in the final paper — and after drafting, emit a compact summary that the next window can consume without reloading the full text.

This file specifies the exact construction rules. Follow them even when they seem redundant — the window is the single mechanism preventing the drifting-by-compounding failure mode where each subsection reads locally well but the paper globally feels patchwork.

## Terminology

- **Reading order**: the order sections appear in the final PDF. For the default 7-section structure: Abstract → Introduction → Related Work → Methods → Results → Discussion → Conclusion.
- **Writing order**: the order sections are drafted in. Default: Methods → Results → Introduction → Related Work → Discussion → Conclusion (Abstract is drafted in Step 5).
- **Reading-order predecessor of X**: the subsection that appears *just before* X in the final paper. This is *not* the same as "the subsection we drafted just before X" — writing order is different.
- **Reading-order successor of X**: the subsection that appears *just after* X in the final paper.

## Availability of Neighbors

For any subsection X, its reading-order neighbors may or may not already be drafted, depending on whether their parent sections preceded X's parent section in writing order.

| Drafting… | Predecessor section | Successor section | Availability |
|---|---|---|---|
| Methods §3.1 | Related Work §2 (last) | Methods §3.2 | Predecessor: NOT DRAFTED (RW comes later in writing order). Successor: will be drafted in this same section iteration. |
| Results §4.1 | Methods §3 (last) | Results §4.2 | Predecessor: DRAFTED. Successor: drafted later in this iteration. |
| Introduction §1.1 | (none — first section) | Related Work §2.1 | No predecessor. Successor: NOT DRAFTED. |
| Related Work §2 (last) | Related Work §2.(last-1) | Methods §3.1 | Predecessor: drafted. Successor: DRAFTED. |
| Discussion §5.1 | Results §4 (last) | Discussion §5.2 | Predecessor: DRAFTED. Successor: drafted later in this iteration. |
| Conclusion §6 | Discussion §5 (last) | (none — last section) | Predecessor: DRAFTED. No successor. |

**Within a single section** (e.g., drafting Results §4.1 then §4.2 then §4.3), predecessors and successors are being built in reading order — so §4.2's predecessor (§4.1) is always drafted, and §4.2's successor (§4.3) is not yet drafted until the section's final subsection.

**Across sections**, neighbors are available only if their parent section came earlier in writing order.

## Context Slots — Construction Rules

Build the context window for subsection X as follows.

### Slot 1: Global Config

Load the entirety of `step2_global_config.json`. It's small and every field matters for this subsection. Pull out the section profile for X's parent section and make it prominent — the tense, tone, hedging, and word_budget drive everything.

### Slot 2: Blueprint Excerpt

From `step1_blueprint.md`, extract only X's entry in the subsection outline. Fields to extract:

- **Title** (EN — the draft is English; the 繁中 is for Checkpoint 1, not drafting)
- **Thesis statement** — the one-sentence contract for this subsection
- **Evidence list** — figures, tables, citations, equations allocated here
- **Transition plan** — how this subsection hands off to the next
- **Word budget** — if the section-level budget was split per subsection; otherwise allocate proportionally by thesis weight

And from the Evidence Mapping block for X's parent section, extract only the rows relevant to this subsection (a section may have many rows; not all apply to every subsection).

### Slot 3: Reading-Order Predecessor

If the predecessor is drafted (check `_sliding_window_state.json`), load:
- Its **summary** (2–3 sentences)
- Its **last paragraph verbatim**

If not drafted, skip this slot and note "no predecessor drafted yet" in the internal reasoning. The draft for X will still work — it will just open with a self-contained introduction rather than a handoff transition. When the predecessor section is later drafted, its final paragraph is where the upstream author calibrates the handoff.

Special case: if X is the first subsection of its parent section, and the parent's predecessor section (in reading order) is drafted, use **that section's last paragraph** as the predecessor, not the subsection before X within the current section — because there is none.

### Slot 4: Reading-Order Successor

If the successor is drafted, load:
- Its **summary** (2–3 sentences)
- Its **first paragraph verbatim**

If not drafted (the common case for cross-section boundaries), skip. X will close with the transition plan from the blueprint rather than a concrete handoff; a later window (when the successor is drafted) can still shape its opening to receive X cleanly.

### Slot 5: Source Materials

Load **only** the source material allocated to X in the blueprint's evidence mapping. Typical contents:

- Rows from `step4_analysis_summary.md` matching claims planned for X
- Specific captions from `figure_captions.md` / `table_captions.md` for figures/tables placed in X
- Specific citation keys from `step4_citation_keys.md` — read the key's full bib entry + (if available) the relevant paragraphs from `step5_full_text/{key}.md`
- Specific rows from `notation_glossary.md` for symbols used here
- Relevant equation blocks from `equation_plan.md`

**Do not load entire files.** Loading all of `analysis_summary.md` into every Results subsection's window pollutes context and invites cross-contamination (a number meant for §4.3 accidentally appearing in §4.1). Be surgical.

### Slot 6: Brick Layer Rules

Reread the relevant section's block in `references/brick_layer_rules.md` (Methods / Results / Intro / RW / Discussion / Conclusion). In particular, scan the **Prohibited** list and the **Pre-emit checklist** so you know what to avoid before writing, not after.

## The Drafting Step

With all six slots loaded, draft the subsection's LaTeX content. Conventions:

- Subsection heading: `\subsection{Title}` with `\label{sec:<section-num>.<subsection-num>}` (e.g., `\label{sec:3.1}`)
- Cross-references: `\ref{fig:X}`, `\ref{tab:X}`, `\ref{eq:X}`, `\ref{sec:X}` — always via `\ref{}`, never hardcoded numbers
- Citations: `\cite{Key2024}` unless `step2_global_config.json.citation_format` says otherwise
- Equations: `\begin{equation}\label{eq:X} ... \end{equation}` using the number assigned by `equation_plan.md`
- Algorithm blocks: `\begin{algorithm}\caption{...}\label{alg:X} ... \end{algorithm}` with content matching `pseudocode.md`
- Hard wrap at ~80 columns for readable diffs (optional but helpful at review)

Aim for the word budget. Going over by >15% is a self-check failure; going under by >15% likely means a subsection was underscoped — check whether a planned claim was silently dropped.

## Summary Emission

After drafting X, write two artifacts:

### Subsection Summary (2–3 sentences)

Captures what X established and how it hands off. Example template:

> **{Section}.{Subsection}**: [What this subsection established in one sentence]. [Key evidence or mechanism, one sentence]. [How it transitions to the next subsection, one sentence — mirroring the blueprint's transition plan].

Worked example for a fictional Results §4.2:

> **4.2 Ablation of Fuzzy Gating**: The gating layer contributes 0.08 F1 in aggregate, with larger gains under high-EEG-noise regimes. Table 2 isolates per-component contributions; Fig. 4 shows the gain is noise-regime dependent. Section 4.3 next examines whether these gains hold across session lengths.

Store under `_sliding_window_state.json.subsections["{section}.{subsection_id}"]`.

### Citation/Figure/Equation Tracking

Also record:
- `citations_used`: list of `\cite{}` keys present in this subsection
- `figures_referenced`: list of `\ref{fig:*}` labels
- `tables_referenced`: list of `\ref{tab:*}` labels
- `equations_referenced`: list of `\ref{eq:*}` labels

Store alongside the summary. These lists let Step 3 cross-check against the blueprint's planned allocations.

## Section-Level Summary Emission

After every subsection of a section is drafted, emit a section-level summary (3–5 sentences) plus capture the section's first paragraph and last paragraph verbatim. These feed later sections' predecessor/successor slots, so they must be **the full paragraphs as they appear in the `.tex` file** — not sentence excerpts, not paraphrases. Downstream handoff logic needs the exact text to shape transitions.

- `sections[{section}].summary` — 3–5 sentences capturing the section's argumentative arc
- `sections[{section}].first_paragraph` — **verbatim** full first paragraph of the section's first subsection (copy the LaTeX content, citations and all, as a single string)
- `sections[{section}].last_paragraph` — **verbatim** full last paragraph of the section's last subsection

Example entry:

```json
"sections": {
  "methods": {
    "summary": "Describes the 45-child cohort, 64-channel EEG + Tobii gaze acquisition, the three-component architecture (encoders + fuzzy gate + classifier head), and the training protocol (Adam, 80/10/10 participant split, 10-fold CV). Sets up the robustness evaluation along session-length and noise-regime axes that Results will report.",
    "first_paragraph": "Forty-five children aged 6--12 years (mean age 9.2, standard deviation 1.8; 22 female, 23 male) ... yielding binary trial-level ground truth.",
    "last_paragraph": "The cohort was split 80/10/10 at the participant level ... ablation variants that remove individual components of the architecture are described in Section~\\ref{sec:results:ablation}."
  }
}
```

## Section-Boundary Handoff

Between sections in writing order, pause before opening the next section's first subsection. Ask:

1. **Does the new section's reading-order predecessor exist?** (If yes, read that section's `last_paragraph` and craft the opening of the new section to flow from it.)
2. **Does the new section's reading-order successor exist?** (If yes, you have a fixed downstream — the section you're about to draft must end such that the successor's opening paragraph flows naturally from it. You may reshape the last subsection's closing paragraph to match.)

When both exist (rare — happens for sections in the middle of writing order when many neighbors are already drafted), you're drafting a section wedged between two fixed endpoints. Respect both.

## Handling "No Predecessor" and "No Successor"

- **Introduction §1.1 drafts with no predecessor** (Intro is first in reading order). Open with the field's broad context; do not reference anything prior.
- **Conclusion §6 drafts with no successor** (Conclusion is last). Close with the forward-looking future-work sentence; do not try to transition into anything.
- **Any subsection whose cross-section neighbors are not yet drafted** uses only the blueprint's transition plan to shape its opening/closing. A later window's handoff work will smooth the seam.

## When to Flag vs. Push Through

If during drafting X you realize:

- The blueprint's evidence mapping for X is missing a source that the thesis clearly needs → stop, record in `_sliding_window_state.json.blueprint_gaps`, surface at Phase 2d's self-check
- A citation key in the evidence list doesn't resolve to `references.bib` → stop, record under `blueprint_gaps`
- Two allocated claims contradict each other → stop, record under `blueprint_gaps`, propose a reconciliation for the user to review
- A symbol in the equation plan clashes with `notation_glossary.md` → stop, record, propose the symbol to rename

Otherwise, push through with the blueprint as written. The blueprint is the contract; Step 3 will catch violations; Step 4 will revise. Don't overcorrect at draft time.
