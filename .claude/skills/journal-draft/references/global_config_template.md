# step2_global_config.json — Schema and Conventions

The global config is the frozen style/terminology contract for the draft. It's written once in Phase 2a, not re-edited during Phase 2b, and consumed verbatim by Steps 3, 4, and 5. Changes after Phase 2a require either regenerating the draft from scratch (major) or being entered as user overrides during Step 4 revision (minor).

## Schema

```json
{
  "draft_version": "v1",
  "created_at": "2026-04-14T10:30:00",
  "target_journal": "IEEE TNSRE",
  "granularity": "Expert in BCI and EEG signal processing, familiar with deep learning fundamentals, not specialized in fuzzy logic. Readers expect rigorous methods, detailed ablations, and clinical relevance contextualization.",
  "citation_format": "\\cite{Key}",
  "glossary": [
    {
      "term": "fuzzy gating layer",
      "definition": "A parameterized differentiable gating mechanism that produces soft modality weights from uncertainty features.",
      "first_appears_in": "Methods §3.2",
      "aliases_to_avoid": ["gating module", "fuzzy gate", "soft gating"]
    },
    {
      "term": "EEG",
      "definition": "Electroencephalography — recording of electrical brain activity via scalp electrodes.",
      "first_appears_in": "Introduction",
      "aliases_to_avoid": ["electroencephalogram (use 'EEG' after first mention)"],
      "first_use_expansion": "electroencephalography (EEG)"
    },
    {
      "term": "\\sigma_g",
      "definition": "Gating noise scale; std of the uncertainty-modulated EEG noise estimate.",
      "first_appears_in": "Methods §3.2",
      "type": "math_symbol"
    }
  ],
  "tense_lock": {
    "introduction": {
      "primary": "present",
      "exceptions": ["past for citing specific prior studies"],
      "prohibited": ["future except in contribution preview"]
    },
    "methods": {
      "primary": "past (actions taken)",
      "exceptions": ["present for describing the system/model"],
      "prohibited": ["future", "hedging verbs (may/could/might)"]
    },
    "results": {
      "primary": "past (experiments)",
      "exceptions": ["present for what figures show"],
      "prohibited": ["causal verbs (because/due to/caused by)", "interpretive verbs (suggests/indicates) — belong to Discussion"]
    },
    "related_work": {
      "primary": "past (specific studies) and present perfect (field trajectory)",
      "exceptions": [],
      "prohibited": ["references to the present paper's results"]
    },
    "discussion": {
      "primary": "present (implications)",
      "exceptions": ["past for comparing with prior studies"],
      "prohibited": ["unhedged strong claims", "new data not reported in Results"]
    },
    "conclusion": {
      "primary": "past (summary) + present/future (implications)",
      "exceptions": [],
      "prohibited": ["new information", "citations", "figure/table refs"]
    }
  },
  "section_profiles": {
    "introduction": { /* copied from blueprint */ },
    "methods": { /* copied from blueprint */ },
    "results": { /* copied from blueprint */ },
    "related_work": { /* copied from blueprint */ },
    "discussion": { /* copied from blueprint */ },
    "conclusion": { /* copied from blueprint */ }
  },
  "brick_layer_ref": "references/brick_layer_rules.md",
  "terminology_conventions": {
    "first_mention_expansion": true,
    "prefer_full_name_on_first_use": ["EEG", "ADHD", "BCI", "ERP"],
    "discouraged_abbreviations": ["SOTA", "e.g.", "etc."],
    "use_american_english": true,
    "oxford_comma": true,
    "equation_referencing": "\\eqref{eq:X}",
    "figure_referencing": "Fig.~\\ref{fig:X}",
    "table_referencing": "Table~\\ref{tab:X}",
    "section_referencing": "Section~\\ref{sec:X}"
  }
}
```

## Field Notes

### `granularity`

Single-paragraph description of the target reader. Derived from `step8_journal_recommendations.md` (if available) and the target journal's typical audience. Calibrates how much a concept must be explained vs. cited.

Three worked examples:

- **IEEE TNSRE** (neural engineering, applied): "Expert in BCI and neural engineering. Familiar with deep learning fundamentals. Expects clinical/population contextualization and rigorous ablation. Not specialized in subfields like fuzzy logic or graph theory — brief background citations suffice."
- **NeurIPS** (ML research): "Expert in deep learning. Expects tight methodological novelty framing and full ablation tables. Neuroscience-specific background needs brief explicit framing."
- **Nature Methods** (methodology-focused biomedical): "Expert in biomedical research methodology. Not assumed to be expert in ML specifics. Methods must be explainable to someone who would implement the pipeline from the description. Clinical validation emphasized."

### `glossary`

Every entry has:
- `term` — the canonical form used in the draft
- `definition` — single-sentence meaning
- `first_appears_in` — section (and subsection if relevant) where first used
- `aliases_to_avoid` — alternative spellings/phrasings that must not be used (enforces consistency)

Optional fields:
- `first_use_expansion` — if the term is an acronym, what to write on first mention (e.g., "electroencephalography (EEG)")
- `type` — `"math_symbol"` for notation entries; `"domain_term"` or `"method_term"` otherwise (omit if plain term)

**Seeding the glossary from notation_glossary.md**: `scripts/init_global_config.py` imports every symbol from the notation glossary as a `math_symbol` entry. After bootstrap, manually add:
- Domain terms that appear in ≥2 sections (e.g., "fuzzy gating layer", "session-length drift")
- Acronyms requiring first-use expansion (EEG, ADHD, BCI, ERP, etc.)
- Any term the user wants locked (e.g., "we prefer 'classifier' over 'model' for our system")

Keep the glossary tight. 15–30 entries is typical; over 50 suggests you've captured stylistic preferences that belong in `terminology_conventions` instead.

### `tense_lock`

Per-section tense rules derived from the section profiles. These are the rules Step 3 will machine-check. The `prohibited` list is the most important field — it's what flags violations.

The bootstrap script seeds tense_lock from the profile's `tense` and `hedging_level` fields in the blueprint. Review after bootstrap and tighten where needed (especially `prohibited` lists).

### `section_profiles`

Verbatim copy of the profiles block from `step1_blueprint.md`. Keeping them here means Step 3–5 don't need to re-parse the blueprint just to read a word budget or hedging level.

### `citation_format`

Default `"\\cite{Key}"`. Override if the target journal uses:
- `"\\citep{Key}"` / `"\\citet{Key}"` — natbib style (parenthetical vs. textual)
- `"[Key]"` — custom bracket style (rare in LaTeX but some journals use)

Match what `step4_references.bib` expects and what the journal's template uses. When in doubt, check `step8_journal_recommendations.md`.

### `terminology_conventions`

Journal-style rules that are too general for the glossary. Examples:
- `oxford_comma`: true (IEEE and most scientific journals) vs. false (some humanities journals, British style guides)
- `use_american_english`: true (most journals) vs. false (some UK/EU venues)
- Cross-reference formats (`Fig.~` vs. `Figure~` vs. `Fig.\ `) — check target journal convention

### `brick_layer_ref`

Pointer to `references/brick_layer_rules.md` within the journal-draft skill. Step 3's review code reads this to know what rules to check, so keep it stable.

## Editing after Phase 2a

The config is intended to be **frozen after Phase 2a** for the duration of Phase 2b drafting. If during drafting you discover a glossary entry is wrong or a tense rule is too strict, note it in `_sliding_window_state.json.config_amendments` and continue drafting. At Phase 2d self-check, surface the amendments to the user so they can decide whether to regenerate affected sections or accept the inconsistency until Step 4.

The only exception: if a new math symbol is introduced during drafting that wasn't in `notation_glossary.md` (because a symbol was silently added to pseudocode), append it to `glossary` immediately — otherwise the draft has an undefined symbol.
