# Section Profile Defaults

Starting profiles for the seven standard sections, keyed by target journal family. Copy into the blueprint's `## 3. Section Profiles` block and adapt to the actual target journal using `step8_journal_recommendations.md`.

The three profile families cover ~90% of likely targets:

- **IEEE / technical-engineering** (IEEE TNSRE, IEEE TBE, IEEE TNNLS, J. Neural Eng.) — Methods-heavy, figure-rich, ~7000–9000 words
- **Nature-family / broad-audience** (Nature Methods, Nat. Neurosci., Nat. Biomed. Eng., Comm. Bio) — terse Methods (often supplementary), brief Discussion, strict Abstract, ~3000–5000 words main text
- **Neuroscience / clinical** (NeuroImage, Cortex, J. Neurosci., Brain) — balanced Methods/Results, longer Discussion, moderate citation density, ~6000–8000 words

Word budgets scale linearly with journal limit. If your target limit is 6000 and the family default totals 7200, multiply all budgets by 6000/7200 ≈ 0.83.

---

## Family 1 — IEEE / Technical-Engineering (default for IEEE TNSRE @ 8000 words)

```json
{
  "introduction": {
    "tone": "authoritative, engaging",
    "tense": "present (general truths), past (citing studies)",
    "citation_density": "high (1-3 per paragraph)",
    "hedging_level": "moderate",
    "interpretation_allowed": true,
    "figure_references": false,
    "narrative_pattern": "broad-to-narrow funnel",
    "word_budget": 800
  },
  "related_work": {
    "tone": "comparative, structured",
    "tense": "present perfect / past",
    "citation_density": "very high",
    "hedging_level": "low",
    "interpretation_allowed": false,
    "figure_references": false,
    "narrative_pattern": "thematic grouping, ending with positioning",
    "word_budget": 1000
  },
  "methods": {
    "tone": "precise, neutral, reproducible",
    "tense": "past (what was done), present (model description)",
    "citation_density": "low-moderate (method origins only)",
    "hedging_level": "none",
    "interpretation_allowed": false,
    "figure_references": "architecture diagram only",
    "narrative_pattern": "sequential procedure",
    "word_budget": 2000
  },
  "results": {
    "tone": "objective, data-driven",
    "tense": "past (experiments), present (what figures show)",
    "citation_density": "none (own work only)",
    "hedging_level": "minimal",
    "interpretation_allowed": false,
    "figure_references": "every figure/table must be referenced",
    "narrative_pattern": "figure-driven",
    "word_budget": 1500
  },
  "discussion": {
    "tone": "interpretive, balanced, cautious",
    "tense": "present (implications), past (comparing literature)",
    "citation_density": "high (comparing with others)",
    "hedging_level": "high",
    "interpretation_allowed": true,
    "figure_references": "refer back to results figures",
    "narrative_pattern": "claim → evidence → comparison → implication",
    "word_budget": 1500
  },
  "conclusion": {
    "tone": "concise, forward-looking",
    "tense": "past (summary), present/future (implications)",
    "citation_density": "none",
    "hedging_level": "moderate",
    "interpretation_allowed": true,
    "figure_references": false,
    "narrative_pattern": "contribution list → limitation → future work",
    "word_budget": 400
  },
  "abstract": {
    "tone": "dense, self-contained",
    "tense": "mixed (background=present, method=past, results=past, conclusion=present)",
    "citation_density": "none",
    "hedging_level": "minimal",
    "interpretation_allowed": false,
    "figure_references": false,
    "narrative_pattern": "background → gap → method → key results (with numbers) → conclusion",
    "word_budget": 250
  }
}
```

**Family 1 total: ~7450 words** (plus 250 abstract = 7700, leaves ~300 for headings/captions within 8000-word limit).

---

## Family 2 — Nature-family / Broad-Audience (default for Nat. Methods @ 4000 main words)

```json
{
  "introduction": {
    "tone": "engaging, broad framing first, technical later",
    "tense": "present, past",
    "citation_density": "moderate",
    "hedging_level": "moderate",
    "interpretation_allowed": true,
    "figure_references": false,
    "narrative_pattern": "significance-first funnel",
    "word_budget": 500
  },
  "related_work": {
    "tone": "integrated into Introduction (typically no standalone section)",
    "tense": "present perfect / past",
    "citation_density": "high",
    "hedging_level": "low",
    "interpretation_allowed": false,
    "figure_references": false,
    "narrative_pattern": "woven into Introduction or brief preceding paragraph",
    "word_budget": 0
  },
  "methods": {
    "tone": "minimal main-text, full detail in supplementary",
    "tense": "past",
    "citation_density": "low",
    "hedging_level": "none",
    "interpretation_allowed": false,
    "figure_references": "architecture diagram only",
    "narrative_pattern": "key methodological innovations only",
    "word_budget": 600
  },
  "results": {
    "tone": "objective, data-driven, reader-guiding",
    "tense": "past",
    "citation_density": "low",
    "hedging_level": "minimal",
    "interpretation_allowed": "light (brief interpretation often woven in)",
    "figure_references": "every figure must be referenced",
    "narrative_pattern": "figure-driven, 4-6 figures, ~1 per subsection",
    "word_budget": 1800
  },
  "discussion": {
    "tone": "interpretive, briefer than IEEE",
    "tense": "present, past",
    "citation_density": "moderate-high",
    "hedging_level": "high",
    "interpretation_allowed": true,
    "figure_references": "refer back",
    "narrative_pattern": "key implications → limitations → outlook",
    "word_budget": 800
  },
  "conclusion": {
    "tone": "often merged into Discussion",
    "tense": "present/future",
    "citation_density": "none",
    "hedging_level": "moderate",
    "interpretation_allowed": true,
    "figure_references": false,
    "narrative_pattern": "brief closer if present",
    "word_budget": 100
  },
  "abstract": {
    "tone": "dense, accessible to general scientific audience",
    "tense": "mixed",
    "citation_density": "none",
    "hedging_level": "minimal",
    "interpretation_allowed": false,
    "figure_references": false,
    "narrative_pattern": "background → method → results → conclusion (one paragraph)",
    "word_budget": 200
  }
}
```

**Family 2 total: ~3800 main + 200 abstract = 4000.** If the journal combines Results+Discussion, adjust `results` and `discussion` narrative_pattern to "integrated Results+Discussion".

---

### Family 3 subvariants worth knowing

- **NeuroImage / NeuroImage: Clinical / Cortex**: 7000-word default below applies directly.
- **JAACAP (J. Am. Acad. Child Adolesc. Psych.)**: 5500 main text, no standalone Related Work (woven into Introduction so `related_work` key is **omitted** from the profile JSON), structured abstract up to 250 words. Scale Family-3 budgets by 5500/6950 ≈ 0.79.
- **J. Neurosci.**: 3500 words main text, terse Methods (supplementary-heavy), no abstract subsections. Scale by 3500/6950 ≈ 0.50; treat closer to a Family-2 hybrid.
- **Brain**: 10000-word ceiling, Discussion can be longer. Scale by 10000/6950 ≈ 1.44.

## Family 3 — Neuroscience / Clinical (default for NeuroImage @ 7000 words)

```json
{
  "introduction": {
    "tone": "authoritative, clinically-framed",
    "tense": "present, past",
    "citation_density": "high",
    "hedging_level": "moderate",
    "interpretation_allowed": true,
    "figure_references": false,
    "narrative_pattern": "clinical significance → mechanism → gap → hypothesis",
    "word_budget": 900
  },
  "related_work": {
    "tone": "structured review",
    "tense": "present perfect / past",
    "citation_density": "very high",
    "hedging_level": "low",
    "interpretation_allowed": false,
    "figure_references": false,
    "narrative_pattern": "thematic grouping",
    "word_budget": 800
  },
  "methods": {
    "tone": "precise, reproducibility-focused",
    "tense": "past",
    "citation_density": "moderate (software + method origins)",
    "hedging_level": "none",
    "interpretation_allowed": false,
    "figure_references": "experimental paradigm + architecture",
    "narrative_pattern": "participants → acquisition → preprocessing → analysis",
    "word_budget": 1600
  },
  "results": {
    "tone": "objective, with statistical emphasis",
    "tense": "past, present (figures)",
    "citation_density": "none (own work)",
    "hedging_level": "minimal",
    "interpretation_allowed": false,
    "figure_references": "every figure/table required",
    "narrative_pattern": "hypothesis-driven: one subsection per hypothesis",
    "word_budget": 1400
  },
  "discussion": {
    "tone": "interpretive, integrates literature",
    "tense": "present, past",
    "citation_density": "high",
    "hedging_level": "high",
    "interpretation_allowed": true,
    "figure_references": "refer back",
    "narrative_pattern": "summary → interpretation per finding → limitations → broader impact",
    "word_budget": 1700
  },
  "conclusion": {
    "tone": "concise summary",
    "tense": "present",
    "citation_density": "none",
    "hedging_level": "moderate",
    "interpretation_allowed": true,
    "figure_references": false,
    "narrative_pattern": "takeaway + clinical/translational implication",
    "word_budget": 300
  },
  "abstract": {
    "tone": "structured (Background / Methods / Results / Conclusions)",
    "tense": "mixed",
    "citation_density": "none",
    "hedging_level": "minimal",
    "interpretation_allowed": false,
    "figure_references": false,
    "narrative_pattern": "structured 4-part abstract (or 250-word unstructured)",
    "word_budget": 250
  }
}
```

**Family 3 total: ~6700 main + 250 abstract = 6950** (within 7000-word limit).

---

## Adapting defaults

1. **Identify the family.** Read `step8_journal_recommendations.md` + the target journal's author guidelines. Match by publisher, typical paper length, and field.
2. **Scale budgets.** If target word limit differs from family default, multiply every budget by (target / family_default_total). Round to the nearest 50.
3. **Journal-specific overrides.** Common ones:
    - Short-format (letters, brief communications): scale down heavily; often no standalone Related Work.
    - Interdisciplinary journals (PNAS, Science Advances): scale Introduction up, scale Methods down, put detail in supplementary.
    - Pure-ML venues (NeurIPS, ICML): scale Methods up (often 30–40% of paper), scale Conclusion down.
    - Clinical journals with structured abstract: split Abstract `word_budget` into (Background, Methods, Results, Conclusions) sub-budgets.
4. **Document deviations.** In the blueprint, under `**Profile adaptations.**`, list each override with a one-line reason. Prevents Checkpoint 1 surprise.

---

## When to consider a new field

Don't add profile fields reflexively. Useful signals for adding one:

- A specific section requires a constraint none of the current fields express (e.g., "maximum 5 equations" for a theory-light venue)
- A constraint keeps surfacing as Step 3 review flags across papers
- The target journal has an unusual convention (e.g., "Significance Statement" in PNAS) that needs its own profile

When adding a field, update `references/section_profile_defaults.md` (this file) and `references/blueprint_template.md` together — the template is what Step 2 reads.
