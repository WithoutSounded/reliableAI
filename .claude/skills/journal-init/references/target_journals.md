# Target Journal Cheatsheet

Common journals in BCI / neuroscience / ML-for-health / engineering informatics. Use these values directly when the user names a match. Always verify against the publisher's latest author guidelines if the submission is imminent — journal rules drift.

## IEEE Transactions on Neural Systems and Rehabilitation Engineering (IEEE TNSRE)

```yaml
target_journal: "IEEE Transactions on Neural Systems and Rehabilitation Engineering"
short_name: "IEEE TNSRE"
publisher: "IEEE"
template: "IEEEtran (journal mode, double-column)"
documentclass: "\\documentclass[journal]{IEEEtran}"
word_limit: 8000       # body only, excludes refs + figures
page_target: "8-12 pages"
abstract_word_limit: 250
citation_style: "IEEEtran"
section_structure: ["Abstract", "Introduction", "Related Work", "Methods", "Results", "Discussion", "Conclusion"]
format_checker_skill: "tnsre-checker"   # not yet authored — prompt user to create via /skill-creator
notes: "Methods section often called 'Materials and Methods'. References use [1] numeric style."
```

## IEEE Transactions on Biomedical Engineering (IEEE TBME)

```yaml
target_journal: "IEEE Transactions on Biomedical Engineering"
short_name: "IEEE TBME"
publisher: "IEEE"
template: "IEEEtran (journal mode, double-column)"
documentclass: "\\documentclass[journal]{IEEEtran}"
word_limit: 7500
page_target: "8-10 pages"
abstract_word_limit: 200
citation_style: "IEEEtran"
section_structure: ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion"]
format_checker_skill: "tbme-checker"   # not yet authored — prompt user to create via /skill-creator
notes: "Related Work typically folded into Introduction. Strict page limit — exceeding incurs page charges."
```

## NeuroImage

```yaml
target_journal: "NeuroImage"
publisher: "Elsevier"
template: "elsarticle (double-column)"
documentclass: "\\documentclass[review,12pt]{elsarticle}"
word_limit: 8000
page_target: "flexible, 10-15 pages typical"
abstract_word_limit: 250
citation_style: "elsarticle-num"
section_structure: ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion"]
format_checker_skill: "neuroimage-checker"   # not yet authored — prompt user to create via /skill-creator
notes: "No separate Related Work — integrate into Introduction. Methods must include 'Data availability' and 'Code availability' subsections."
```

## Nature Methods

```yaml
target_journal: "Nature Methods"
publisher: "Nature Portfolio"
template: "Nature style (single-column submission)"
documentclass: "\\documentclass{nature}"
word_limit: 3000       # main text for Articles; Brief Communications are 1500
page_target: "compact"
abstract_word_limit: 150
citation_style: "nature"
section_structure: ["Abstract", "Introduction", "Results", "Discussion", "Methods"]
format_checker_skill: "nature-methods-checker"   # not yet authored — prompt user to create via /skill-creator
notes: "Methods at the END, not beginning. Strict word limit. Supplementary Methods allowed for detail."
```

## Advanced Engineering Informatics (AEI)

```yaml
target_journal: "Advanced Engineering Informatics"
short_name: "AEI"
publisher: "Elsevier"
template: "Elsevier CAS (Compact Article Style, double-column)"
documentclass: "\\documentclass[a4paper,fleqn]{cas-dc}"
word_limit: 8000
page_target: "12-15 pages"
abstract_word_limit: 250
citation_style: "elsarticle-num"
section_structure: ["Abstract", "Introduction", "Related Work", "Methods", "Results", "Discussion", "Conclusion"]
format_checker_skill: "aei-checker"   # authored — bundled at .claude/skills/aei-checker/
notes: "Uses cas-dc class. Include 'Credit Author Statement' and 'Declaration of Competing Interest'. See aei-checker skill for full compliance check."
```

## Pattern Recognition

```yaml
target_journal: "Pattern Recognition"
publisher: "Elsevier"
template: "elsarticle (double-column)"
documentclass: "\\documentclass[final,3p,times,twocolumn]{elsarticle}"
word_limit: 8000
page_target: "12-18 pages"
abstract_word_limit: 200
citation_style: "elsarticle-num"
section_structure: ["Abstract", "Introduction", "Related Work", "Methods", "Experiments", "Discussion", "Conclusion"]
format_checker_skill: "pattern-recognition-checker"   # not yet authored — prompt user to create via /skill-creator
notes: "Often 'Experiments' instead of 'Results'. High emphasis on benchmark comparisons."
```

## Journal of Neural Engineering (JNE)

```yaml
target_journal: "Journal of Neural Engineering"
short_name: "JNE"
publisher: "IOP Publishing"
template: "iopart (IOP article class)"
documentclass: "\\documentclass[12pt]{iopart}"
word_limit: 8000
page_target: "10-15 pages"
abstract_word_limit: 250
citation_style: "iopart-num"
section_structure: ["Abstract", "Introduction", "Methods", "Results", "Discussion", "Conclusion"]
format_checker_skill: "jne-checker"   # not yet authored — prompt user to create via /skill-creator
notes: "Related Work folded into Introduction. Requires 'Significance statement' (120 words)."
```

## IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI)

```yaml
target_journal: "IEEE Transactions on Pattern Analysis and Machine Intelligence"
short_name: "IEEE TPAMI"
publisher: "IEEE"
template: "IEEEtran (journal mode, double-column)"
documentclass: "\\documentclass[journal]{IEEEtran}"
word_limit: 14000      # very long — up to 18 pages
page_target: "12-18 pages"
abstract_word_limit: 250
citation_style: "IEEEtran"
section_structure: ["Abstract", "Introduction", "Related Work", "Methods", "Experiments", "Discussion", "Conclusion"]
format_checker_skill: "tpami-checker"   # not yet authored — prompt user to create via /skill-creator
notes: "One of the longest limits in the field. Related Work is expected as a standalone section."
```

## Adding a New Journal

If the user's target isn't listed:

1. Check `step8_journal_recommendations.md` in the Research session — if Research-Agent recommended this journal, it likely captured the specs there.
2. WebSearch for `"{journal name}" author guidelines word limit` and `"{journal name}" LaTeX template`.
3. Populate fields conservatively: if unsure of word limit, default to 8000 with a warning in the config.
4. Populate `format_checker_skill` with a suggested slug based on the journal's short_name (e.g., "Computers in Biology and Medicine" → `cbm-checker`). This is the *expected* skill name the user is asked to create; `journal-init` will detect that the skill directory doesn't exist yet and prompt them.

When you add a new journal spec to this file during a session, keep it inline in the session config — don't force the user to re-look-up next time.

## Field Reference

| Field | Type | Required? | Notes |
|---|---|---|---|
| `target_journal` | string | yes | Full journal name |
| `short_name` | string | no | For display (e.g., "IEEE TNSRE") |
| `publisher` | string | yes | "IEEE", "Elsevier", "Springer", "Nature Portfolio", "IOP Publishing", etc. |
| `template` | string | yes | Descriptive name of the LaTeX class |
| `documentclass` | string | no | Exact `\documentclass{...}` line |
| `word_limit` | int | yes | Main body word count ceiling |
| `page_target` | string | no | Rough page count (informational) |
| `abstract_word_limit` | int | yes | Abstract-specific limit |
| `citation_style` | string | yes | Bibliography style (IEEEtran, elsarticle-num, nature, etc.) |
| `section_structure` | list | yes | Ordered section list — respect the journal's naming |
| `format_checker_skill` | string | yes | Name of the skill that verifies submission-guideline compliance (e.g., `aei-checker`). Must match the directory name under `.claude/skills/`. If no authored checker exists yet, still set a predicted slug — `journal-init` will detect the gap and ask the user to create one via `/skill-creator`. `journal-finalize` blocks until this skill exists. |
| `notes` | string | no | Quirks, required statements, formatting gotchas |
