# Polish Rubric

Authoritative rules and heuristics for Phase 5a (per-section polish) and Phase 5b (global polish). Read this when you start polishing a section and again before the Golden Thread pass.

## Contents

1. [Per-Section Polish Dimensions](#per-section-polish-dimensions)
2. [Hedging Calibration Table](#hedging-calibration-table)
3. [Paragraph-Length Heuristics](#paragraph-length-heuristics)
4. [Sentence Variety Patterns](#sentence-variety-patterns)
5. [Vocabulary Precision: Vague → Precise](#vocabulary-precision-vague--precise)
6. [Transitions Between Paragraphs](#transitions-between-paragraphs)
7. [Golden Thread Report Template](#golden-thread-report-template)

---

## Per-Section Polish Dimensions

Apply every dimension to every section, but the emphasis differs by section. Emphasis matters because time spent polishing dimensions the section does not depend on is wasted, and over-polishing can drift the meaning.

| Section | Primary emphasis | Secondary | Light touch |
|---|---|---|---|
| 01_introduction | Narrative funnel (broad → specific), transitions between paragraphs | Vocabulary precision | Sentence variety (usually already varied) |
| 02_related_work | Sentence variety (it's citation-dense and tends to read like a list), transitions | Vocabulary precision | Hedging (keep neutral-comparative tone) |
| 03_methods | Vocabulary precision (must be exact), grammar (past tense consistency) | Paragraph-length balance | Hedging — Methods does not hedge |
| 04_results | Sentence variety (the "we found X, we found Y" trap), hedging — **strong language allowed, remove unwarranted hedging** | Transitions | Vocabulary (already constrained by the data) |
| 05_discussion | **Hedging calibration — this is where undercalibrated hedging causes reviewer pushback**, transitions | Vocabulary precision | Grammar (usually fine) |
| 06_conclusion | Conciseness (cut redundancy with Results / Discussion), transitions back to Introduction's promises | Vocabulary precision | Paragraph length (usually single-paragraph anyway) |

---

## Hedging Calibration Table

Hedging calibration is the single most consequential dimension in polish. Apply this table deliberately.

| Evidence strength | Example source | Permitted verbs | Forbidden verbs |
|---|---|---|---|
| **Strong** (p<0.01, large N, large effect, replicated) | `F1=0.91 with p<0.001, N=120` | `demonstrates`, `shows`, `achieves`, `establishes`, `confirms` | (none) |
| **Moderate** (p<0.05, moderate effect, single-study) | `accuracy 84% vs baseline 78%, p=0.03` | `shows`, `indicates`, `supports` | `confirms`, `establishes`, `proves` |
| **Weak** (trend, small N, borderline p, indirect measure) | `trend toward improvement, p=0.09` | `suggests`, `may indicate`, `is consistent with`, `one possible interpretation is` | `demonstrates`, `shows`, `confirms` |
| **Absent test** (no statistic reported) | `"the model performs well"` | — rewrite with a number or cite a test — | any boosting verb |

**Section-level hedging rules:**

- **Results**: the default is Strong language where the numbers support it. If you see `our model may achieve high accuracy` in Results, strip the hedge — the Results section reports what happened, it does not interpret. But if a statistic is borderline (`p=0.08`), Results should report the number honestly without decorating it with `significantly`.
- **Discussion**: the default is Moderate to Weak language for interpretive claims. `These findings demonstrate that attention weights cause behavior changes` is almost always an OVERCLAIM in Discussion; rewrite to `These findings are consistent with attention weights influencing behavior, though we cannot establish causality from correlational data.`
- **Conclusion**: match Discussion hedging. Do not ratchet up the strength in the Conclusion compared with how the same point was stated in Discussion — that is a known reviewer trigger.
- **Abstract**: match Results for numerical claims; match Discussion for the concluding interpretation.

**Common hedging failures to watch for:**

- `significantly` used without a reported test in the nearby sentences. Either delete it or attach the test.
- `It is clear that …` / `Obviously …` — delete these openers. If the claim needs defending, defend it; if it doesn't, skip the opener.
- Triple-hedged sentences: `We tentatively suggest that it may possibly indicate that X`. One hedge per sentence is enough.

### Worked example: hedging calibration in Discussion

This is the single edit that most often separates a publishable Discussion from a reviewer-pushback Discussion. Study the shape of the change — the polish is mechanical once you see it, but only if you recognise that the *direction* of the edit is determined by the evidence underneath, not by the draft's self-presentation.

**Before** (Discussion draft, moderate evidence misrepresented as strong):

> These results demonstrate that portable EEG neurofeedback with a participant-adaptive threshold produces meaningful neural plasticity in older adults. A session completion rate of 96% and no reported adverse events clearly show that the protocol is well tolerated, and the low fatigue ratings prove that a forty-minute session length is acceptable. Compared with earlier laboratory-based neurofeedback trials in older adults, which reported completion rates in the 70–80% range, our community-based portable protocol significantly outperforms existing work.

Diagnosis. The underlying evidence is: (a) feasibility endpoints with no statistical test against a baseline (tolerability is descriptive, `demonstrates` / `prove` / `clearly show` are not warranted); (b) a single-arm study with no head-to-head comparison against the laboratory protocols (`significantly outperforms` without a between-study test is an OVERCLAIM). The claims may turn out to be true, but this paper does not contain the evidence to state them at this strength.

**After** (same meaning, calibrated hedging):

> These findings indicate that portable EEG neurofeedback with a participant-adaptive threshold is feasible and well tolerated in community-dwelling older adults. A session completion rate of 96%, no reported adverse events, and consistently low fatigue ratings together suggest that the forty-minute session length is acceptable to this cohort. The completion rate is higher than those reported in earlier laboratory-based neurofeedback trials with older adults (typically 70–80%), though the absence of a direct between-study comparison means this difference should be interpreted as descriptive rather than as a demonstrated improvement.

What changed and why. `demonstrate` → `indicate` (feasibility evidence supports indication, not demonstration). `clearly show` → `together suggest` (descriptive ratings cannot show; at best they are consistent with). `prove` → removed (no test). `significantly outperforms` → `is higher than … though … interpreted as descriptive` (no between-study test was performed, so the comparison cannot be framed as statistical superiority). No numbers changed; no claims removed; the same facts are on the page — at the strength the evidence actually supports. That is the shape of every hedging-calibration edit in Discussion.

An edit that changes *what* the paper says belongs in Step 3/4. An edit that changes *how strongly* the paper says the same thing at the same evidence level is what polish is for.

---

## Paragraph-Length Heuristics

**Target band: 3–8 sentences per paragraph.** Counted as sentences terminating in `.`, `?`, or `!` (ignore display equations, figure/table captions, and list items).

| Observation | Likely cause | Fix |
|---|---|---|
| 1–2 sentence paragraph | Undeveloped thought; or a one-liner conclusion that should be absorbed into the previous paragraph | Expand with the supporting reasoning, or merge with the adjacent paragraph |
| 9+ sentence paragraph | Two ideas fused, or a list-that-should-have-been-a-list | Split at the second topic sentence, or convert to an `itemize` if genuinely a list |
| Paragraphs all the same length (±1 sentence) throughout a section | Artificial rhythm — the prose sounds generated | Vary deliberately: compress some, expand others |

**Exceptions that are fine:**

- Single-sentence paragraphs *as intentional emphasis* (rare — at most once per section).
- Short final paragraphs that serve as a section hinge (e.g., a two-sentence wrap-up before moving to the next section).
- Methods paragraphs describing a single step (sometimes 2 sentences is all you need for a well-known procedure).

Note the exception in `polish_notes.md` when you leave one in place so the human reviewer sees that it was deliberate.

---

## Sentence Variety Patterns

Monotonous prose is usually one of these three patterns.

| Pattern | Example | Fix |
|---|---|---|
| **Same opener** | `We recorded EEG. We extracted features. We trained a classifier. We evaluated on the test set.` | Vary openers: `EEG was recorded... Feature extraction proceeded... The classifier was trained... On the held-out test set, ...` |
| **Same length bucket** | All sentences 10–12 words | Mix in a short sharp sentence (5–7 words) or a longer reasoned sentence (20–25 words) |
| **Same structure** | All simple SVO: `X does Y. A does B. P does Q.` | Mix in a participial opener, a conditional clause, a "Although X, Y," construction |

**Limit: 3 consecutive sentences with the same opening word or structural shape.** On the 4th, vary.

**Do not over-vary.** Intro and Discussion tolerate more syntactic variety; Methods should remain plain and sequential. "Varied for the sake of variety" is a different failure mode.

---

## Vocabulary Precision: Vague → Precise

Replace vague words with precise ones **only when the precision is already committed to in the draft**. Do not invent precision.

| Vague | Precise (if the draft supports it) |
|---|---|
| `good performance` | `high classification accuracy` / `F1 of 0.87` |
| `a lot of data` | the actual N |
| `various methods` | the actual list of methods |
| `things`, `stuff`, `aspects` | the specific noun |
| `recent work` | `Smith et al. (2024)` / `recent deep-learning approaches` |
| `significantly better` (no test) | `outperforms by X percentage points` |
| `works well` | `generalizes to unseen participants (N=20, accuracy 82%)` |
| `a small number` | the actual number |
| `approximately` without a number | delete or add the approximation |

**If the precision is not in the draft**, do not invent it. Leave the vague term, and note it in `polish_notes.md` as a potential content gap for the human to resolve.

---

## Transitions Between Paragraphs

Every paragraph's first sentence should link to the previous paragraph's last sentence — usually by topic continuity, sometimes by a connective word, rarely by explicit signposting.

**Types of transition (in order of preference — prefer the lighter touch):**

1. **Topic continuity** — the new paragraph's first sentence picks up a noun or concept from the previous paragraph's last sentence. No connective needed.
2. **Connective word** — `However,` / `In contrast,` / `Nevertheless,` / `Consequently,`. Use sparingly (at most one per 2–3 paragraphs).
3. **Explicit signpost** — `Having established X, we now turn to Y.` Use at section hinges, not between every paragraph.

**Red flags:**

- A paragraph that opens with a completely unrelated topic (the reader has to re-orient).
- A `However,` that does not actually contrast with anything (check the preceding paragraph — if there is no claim to contrast with, drop the `However`).
- Every paragraph starting with the same connective word (`However, …`, `Furthermore, …`, `Moreover, …` — pick one and rotate, or remove).

---

## Golden Thread Report Template

Use this exact structure for `step5_polished/golden_thread_report.md`:

```markdown
# Golden Thread Report

## Core Argument

> "{verbatim quote of the paper's one-sentence core argument}"

Source: {step1_blueprint.md § Core argument | derived from blueprint narrative objective + contributions (see Note below)}

{If derived: one-paragraph note explaining the derivation and inviting the human to correct.}

## Section Verdicts

### 01_introduction — {PRESENT | IMPLIED | ATTENUATED | CONTRADICTS}

> "{quote from the polished section that carries the thread, or the passage that attenuates / contradicts it}"

**Reasoning:** {one to three sentences}

{If ATTENUATED: proposed fix — "Add to the end of §1.3: '…'"}
{If CONTRADICTS: author question — "Which is the intended claim?"}

### 02_related_work — …

### 03_methods — …

### 04_results — …

### 05_discussion — …

### 06_conclusion — …

## Overall Verdict

{one short paragraph}

- **Load-bearing through the whole paper?** Yes / No / Partially.
- **Where it fades (if anywhere):** {section(s)}
- **Recommended action:** {"Proceed to Checkpoint 3 — no thread fixes needed." | "Apply proposed fix in §X before Checkpoint 3." | "Author input needed on contradiction in §Y."}
```

**Verdict definitions (for consistency):**

- `PRESENT` — the section contains at least one sentence that explicitly states or restates the core argument, or one of its defining components.
- `IMPLIED` — the section does not state the argument but establishes a necessary premise. Methods and Related Work commonly land here; that is fine as long as the premise relationship is clear.
- `ATTENUATED` — the section is on-topic and does not contradict, but never closes the loop. Common in Conclusion (drifts into generic future work) and in long Discussions (last paragraph forgets what the first paragraph was arguing).
- `CONTRADICTS` — the section asserts something whose truth would make the core argument false or meaningless. Rare but critical — a single `CONTRADICTS` blocks Checkpoint 3.
