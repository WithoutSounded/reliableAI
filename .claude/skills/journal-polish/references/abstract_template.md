# Abstract Template

Used in Phase 5c (Abstract Generation). The abstract is the single most-read and most-quoted piece of the paper, and it is generated last — only after all six narrative sections are polished and the Golden Thread check has passed.

## Structure

Exactly five elements, in this order:

1. **Background** (1–2 sentences) — situate the problem in the field. The reader learns what domain they are in and why it matters.
2. **Gap** (1 sentence) — name the specific unresolved issue this paper addresses. The gap must match the one in the Introduction — the same gap, phrased densely.
3. **Method** (2–3 sentences) — what was done. Include the distinctive methodological choice (not every implementation detail). A reader should be able to describe the approach in one sentence after reading the abstract.
4. **Key Results** (2–3 sentences) — specific numbers. At least one headline metric. Compare against baseline / prior work where the Results section does so.
5. **Conclusion** (1 sentence) — the implication. Match the hedging level of the Discussion's concluding claim.

Target length: typical journals allow 150–250 words. Aim for 85–100% of the budget. A 90-word abstract looks thin; a 280-word abstract gets truncated by the journal.

## Hard Rules

These are enforced by `scripts/polish_checks.py --mode abstract`. All must pass.

### Number Rule

**Every number in the abstract must already appear in `04_results.tex`** — same value, same units, same decimal places.

- If the abstract says `84.2% accuracy`, that exact string (or an exact numeric match) must be in Results. `84%` in the abstract with `84.2%` in Results is a mismatch — either round both or neither, and match.
- If the abstract says `p < 0.001`, Results must also say `p < 0.001` or a stricter bound.
- If the abstract contains a number that is NOT in Results, that means Results is missing the result — escalate to the author. Do not fix by inventing it in Results or by removing it from the abstract without asking.

### No Citations

No `\cite{…}` commands. The abstract is self-contained. If the abstract needs to position against prior work, do it with a phrase (`unlike prior deep-learning approaches`, `compared with the standard pipeline`) not a citation.

### No Figure / Table / Section References

No `\ref{fig:…}`, no `\ref{tab:…}`, no "as shown in Fig. X", no "Table Y", no "Section 3", no "(see §4.2)". A reader who has not opened the paper cannot resolve these.

### Self-Contained

No forward references (`as described below`), no backward references (`as noted in the Introduction`). The abstract stands alone.

### Within Word Limit

Exact target is journal-specific (see table below). If `word_limit` in `step0_session_config.json` does not specify an abstract limit, default to the journal's published limit or 250 words.

## Common Abstract Word Limits

Used as a default when the session config is silent.

| Journal family | Typical limit |
|---|---|
| IEEE Transactions (TNSRE, TBME, TPAMI, TNNLS) | 200 words (structured or unstructured) |
| NeuroImage | 250 words |
| Nature Methods, Nature Neuroscience | 150 words (no sections) |
| Nature Communications | 150 words |
| Journal of Neural Engineering (JNE) | 250 words |
| PLOS journals | 300 words |
| Frontiers journals | 250 words |
| PNAS | 250 words (significance statement additional) |

Some journals require a structured abstract with explicit `Background:` / `Methods:` / `Results:` / `Conclusions:` labels. Check the target journal's author guide — if structured, keep the same five-element flow but add the labels.

## Worked Example (Unstructured, 250-word budget)

> Cognitive decline in older adults has been linked to attentional dysregulation, and scalable non-invasive interventions remain limited. Portable EEG-based neurofeedback is a candidate intervention, but its feasibility in community settings — particularly with elderly participants and dynamic difficulty calibration — has not been established. Here we report a feasibility study of a portable EEG neurofeedback protocol with an adaptive thresholding scheme in 20 older adults (ages 65–78). Participants completed eight sessions over four weeks; session completion, adherence, and subjective tolerance were the primary feasibility endpoints, and frontal-theta modulation amplitude was a secondary physiological endpoint. Session completion was 96% (192 of 200 scheduled sessions), with no adverse events reported. Frontal-theta amplitude increased by 18% (95% CI 9–27%, p = 0.003) from baseline to the final session, and within-session up-regulation was observed in 87% of trials. The adaptive threshold converged within three sessions on average (SD = 1.2), suggesting rapid calibration is achievable in this population. These results indicate that portable EEG neurofeedback with dynamic thresholding is feasible and tolerable in older adults, supporting a larger efficacy trial.

Notes on the example:
- Every number (20, 65–78, 8, 4, 96%, 192/200, 18%, 9–27%, 0.003, 87%, 3, 1.2) appears in Results.
- No citations, no figure/table/section references, self-contained.
- Hedging: `suggesting rapid calibration is achievable` — matches Discussion. `These results indicate` — matches Results → Discussion handoff (moderate strength).
- Word count: ~215 — under the 250 budget, substantive.

## Structured Abstract Variant

Some journals require explicit labels. Use this template:

```
\textbf{Background.} {1-2 sentences}
\textbf{Objective.} {1 sentence naming the gap / aim}
\textbf{Methods.} {2-3 sentences}
\textbf{Results.} {2-3 sentences with numbers}
\textbf{Conclusions.} {1 sentence implication}
```

The hard rules above apply identically.

## Generation Workflow

1. Read `04_results.tex` and extract every number with its surrounding clause — this is your permitted number set.
2. Read `05_discussion.tex` conclusion paragraph and `06_conclusion.tex` — this tells you the strength of the concluding claim.
3. Read `01_introduction.tex` opening and gap paragraph — this tells you how Background and Gap were framed; match.
4. Draft the abstract in one pass, using only the permitted number set.
5. Run `scripts/polish_checks.py --mode abstract` and iterate until it is clean.
6. Final pass: read the abstract aloud (mentally). If it reads as a dense coherent paragraph rather than five bolted-together chunks, it's ready.
