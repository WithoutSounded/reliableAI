# Journal Preamble Templates

The `build_latex_package.py` script picks a preamble based on substring matching against `target_journal` from `step0_session_config.json`. This file is the authoritative template list. If you add a journal, update both this file and the `select_preamble()` function in the script.

## Matching rules (first match wins)

| Pattern in `target_journal` | Preamble | Bibstyle |
|---|---|---|
| `ieee` | IEEEtran | `IEEEtran` |
| `elsevier`, `neuroimage`, `advanced engineering informatics`, `aei`, `patrec` | elsarticle | `model2-names` |
| `springer`, `nature methods`, `nature communications`, `sn-jnl`, `bmc` | sn-jnl | `sn-mathphys-num` |
| `scientific reports`, `nature` | wlscirep | `naturemag` |
| (anything else) | `article` | `plain` |

## IEEEtran (IEEE journals — TNSRE, TBME, JBHI, TMI, etc.)

```latex
\documentclass[journal]{IEEEtran}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{array}
\usepackage{booktabs}
\usepackage{cite}
\usepackage{url}
\usepackage{hyperref}

\begin{document}
```

- Word limits: typically 8,000 words for TNSRE full paper; 4,000 for "brief paper" type.
- Abstract: 200 words.
- Uses numeric citations (`\cite{Key}` renders as `[1]`).

## elsarticle (Elsevier — NeuroImage, Advanced Engineering Informatics, Pattern Recognition, etc.)

```latex
\documentclass[preprint,review,12pt]{elsarticle}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage[authoryear]{natbib}

\begin{document}
```

- Word limits vary: NeuroImage 7,000; AEI 7,000; Pattern Recognition 8,000.
- Abstract: 250 words (NeuroImage), 200 (AEI).
- Author-year citations via `natbib`; use `\citep{Key}` for parenthetical.
- Elsevier also provides `cas-sc.cls`/`cas-dc.cls` — if the user specifies CAS explicitly, switch to those.

## sn-jnl (Springer Nature — Nature Methods, Nature Communications, Springer book/journal series)

```latex
\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{hyperref}

\begin{document}
```

- Word limits: Nature Methods ~3,000 (full article); Communications Biology 4,000–5,000.
- Abstract: 150 words (Nature family), 200 words (Communications Biology).
- Numeric citations via `sn-mathphys-num.bst`.
- Sub-options: `sn-basic` (no `natbib`), `sn-mathphys`/`sn-chemistry`/`sn-nature` for discipline-specific.

## wlscirep (Scientific Reports / wellcome-like template)

```latex
\documentclass[fleqn,10pt]{wlscirep}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}

\begin{document}
```

- No hard word limit; typical papers 4,000–6,000 words.
- Abstract: 200 words.
- The actual Scientific Reports class is not strictly `wlscirep` — the template has shifted. For current submissions check the journal page; this is a reasonable starting point for structure.

## article (generic fallback)

```latex
\documentclass[11pt,a4paper]{article}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{cite}
\usepackage{hyperref}

\begin{document}
```

Used when `target_journal` is empty or unknown. Safe for any submission system that accepts vanilla LaTeX.

## Notes on `main.tex` structure

Whatever preamble is used, `main.tex` ends with:

```latex
\input{00_abstract}
\input{01_introduction}
\input{02_related_work}
\input{03_methods}
\input{04_results}
\input{05_discussion}
\input{06_conclusion}

\bibliographystyle{<bibstyle>}
\bibliography{references}

\end{document}
```

Section files must not contain `\documentclass`, `\begin{document}`, `\end{document}`, or `\bibliography{}` — the structural sanity pass fails if any of these appear. This is enforced because when the author pastes the package into Overleaf, the section files are `\input`'d into `main.tex` and extra document-level directives cause compile errors.

## Abstract handling per class

- **IEEEtran**: `\begin{abstract}...\end{abstract}` inside `00_abstract.tex`.
- **elsarticle**: `\begin{frontmatter}\begin{abstract}...\end{abstract}\end{frontmatter}` convention. For a cleaner split, `00_abstract.tex` can hold just the abstract body, and authors move the frontmatter wrapper into `main.tex` if needed.
- **sn-jnl**: `\abstract{...}` inline in `main.tex` before `\maketitle` — or a `\begin{abstract}` block depending on sub-option.
- **article**: `\begin{abstract}...\end{abstract}` after `\maketitle`.

The finalize skill writes `00_abstract.tex` as the abstract body only. If the target journal requires wrapping (e.g. `\begin{frontmatter}` for Elsevier), the author adjusts `main.tex` in Overleaf or the skill's preamble template is extended to include it.
