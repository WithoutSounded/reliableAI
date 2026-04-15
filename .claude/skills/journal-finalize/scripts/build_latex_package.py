#!/usr/bin/env python3
"""
Build LaTeX package for Overleaf (Phase 6c.1 of Journal Finalize).

Given:
  - Polished section .tex files (step5_polished/)
  - Revised section .tex files (step4_draft_v{latest}/) — used as fallback for drift
  - Semantic drift decisions (from semantic_drift.py)
  - Upstream references.bib
  - Target journal name

Produces:
  - <output>/<NN>_<section>.tex   (one per section; polished or fallback)
  - <output>/main.tex             (with target-journal preamble, \\input chain)
  - <output>/references.bib       (pruned to only cited entries)

And runs a structural sanity pass (brace balance, \\begin/\\end pair balance,
no forbidden commands in section files, \\input{} targets exist).

Usage:
    python build_latex_package.py \\
        --polished-dir step5_polished \\
        --revised-dir step4_draft_v2 \\
        --drift-decisions step6_final/semantic_drift.json \\
        --bib-file Research/.../step4_references.bib \\
        --target-journal "IEEE TNSRE" \\
        --output-dir step6_final/latex
"""

import argparse
import json
import re
import sys
from pathlib import Path


SECTIONS = [
    "00_abstract.tex",
    "01_introduction.tex",
    "02_related_work.tex",
    "03_methods.tex",
    "04_results.tex",
    "05_discussion.tex",
    "06_conclusion.tex",
]

FORBIDDEN_IN_SECTION = [
    r"\\documentclass",
    r"\\begin\{document\}",
    r"\\end\{document\}",
    r"\\bibliographystyle\{",
    r"\\bibliography\{",
]


# ---------------------------------------------------------------------------
# Journal preamble selection
# ---------------------------------------------------------------------------

def select_preamble(target_journal: str) -> tuple[str, str, str]:
    """Return (preamble, bibstyle, comment) for the given journal name."""
    tj = (target_journal or "").lower()

    ieee_preamble = r"""\documentclass[journal]{IEEEtran}

% --- packages ---
\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{algorithmic}
\usepackage{array}
\usepackage{booktabs}
\usepackage{cite}
\usepackage{url}
\usepackage{hyperref}

\begin{document}
"""
    elsevier_preamble = r"""\documentclass[preprint,review,12pt]{elsarticle}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{hyperref}
\usepackage[authoryear]{natbib}

\begin{document}
"""
    springer_preamble = r"""\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{hyperref}

\begin{document}
"""
    nature_preamble = r"""\documentclass[fleqn,10pt]{wlscirep}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}

\begin{document}
"""
    generic_preamble = r"""\documentclass[11pt,a4paper]{article}

\usepackage{graphicx}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{cite}
\usepackage{hyperref}

\begin{document}
"""

    if "ieee" in tj:
        return ieee_preamble, "IEEEtran", "IEEE journal preamble"
    if any(k in tj for k in ("elsevier", "neuroimage", "advanced engineering informatics", "aei", "patrec")):
        return elsevier_preamble, "model2-names", "Elsevier elsarticle preamble"
    if any(k in tj for k in ("springer", "nature methods", "nature communications", "sn-jnl", "bmc")):
        return springer_preamble, "sn-mathphys-num", "Springer Nature sn-jnl preamble"
    if "scientific reports" in tj or tj == "nature":
        return nature_preamble, "naturemag", "Nature Scientific Reports preamble"
    return generic_preamble, "plain", "Generic article preamble (fallback)"


# ---------------------------------------------------------------------------
# Bib pruning
# ---------------------------------------------------------------------------

def extract_cite_keys_from_tex(tex_dir: Path) -> list[str]:
    """Return cite keys in order of first appearance across reading-order files."""
    ordered = []
    seen = set()
    for name in SECTIONS:
        p = tex_dir / name
        if not p.exists():
            continue
        text = re.sub(r"(?<!\\)%.*$", "", p.read_text(encoding="utf-8"), flags=re.MULTILINE)
        for m in re.finditer(r"\\cite[tp]?\*?\{([^}]+)\}", text):
            for k in m.group(1).split(","):
                k = k.strip()
                if k and k not in seen:
                    seen.add(k)
                    ordered.append(k)
    return ordered


def parse_bib_entries(bib_text: str) -> dict[str, str]:
    """Parse bib into {key: entry_text} by brace-counting."""
    entries = {}
    i = 0
    n = len(bib_text)
    while i < n:
        # Find next '@'
        at = bib_text.find("@", i)
        if at == -1:
            break
        # Skip comment-style
        # Grab type{key,
        m = re.match(r"@(\w+)\s*\{\s*([^,\s}]+)\s*,", bib_text[at:])
        if not m:
            i = at + 1
            continue
        key = m.group(2).strip()
        # Find matching closing brace
        depth = 0
        start = at + m.end()
        j = at
        # Find opening brace after '@type' again for balance
        brace_start = bib_text.find("{", at)
        j = brace_start
        depth = 0
        while j < n:
            ch = bib_text[j]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    j += 1
                    break
            j += 1
        entry = bib_text[at:j]
        entries[key] = entry
        i = j
    return entries


def prune_bib(bib_path: Path, cited_keys_in_order: list[str]) -> tuple[str, list[str]]:
    """Return (pruned_bib_text, missing_keys)."""
    if not bib_path.exists():
        return "", list(cited_keys_in_order)
    bib_text = bib_path.read_text(encoding="utf-8")
    entries = parse_bib_entries(bib_text)
    missing = [k for k in cited_keys_in_order if k not in entries]
    kept = [entries[k] for k in cited_keys_in_order if k in entries]
    pruned = "\n\n".join(kept) + ("\n" if kept else "")
    return pruned, missing


# ---------------------------------------------------------------------------
# Structural sanity
# ---------------------------------------------------------------------------

def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


def check_brace_balance(text: str) -> int:
    """Return depth after processing (0 = balanced). Ignores \\{ \\}."""
    # Mask escaped braces
    t = re.sub(r"\\[{}]", "  ", text)
    depth = 0
    for ch in t:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return depth
    return depth


def check_env_balance(text: str) -> list[str]:
    """Return list of unmatched \\begin/\\end names."""
    stack = []
    errors = []
    for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", text):
        which, env = m.group(1), m.group(2)
        if which == "begin":
            stack.append(env)
        else:
            if not stack:
                errors.append(f"\\end{{{env}}} without matching \\begin")
            elif stack[-1] != env:
                errors.append(f"\\end{{{env}}} does not match \\begin{{{stack[-1]}}}")
                stack.pop()
            else:
                stack.pop()
    for env in stack:
        errors.append(f"\\begin{{{env}}} without matching \\end")
    return errors


def check_forbidden(text: str) -> list[str]:
    errs = []
    for pat in FORBIDDEN_IN_SECTION:
        if re.search(pat, text):
            errs.append(f"forbidden command in section file: {pat}")
    return errs


def structural_sanity(output_dir: Path) -> list[str]:
    errs = []
    for name in SECTIONS:
        p = output_dir / name
        if not p.exists():
            continue  # missing sections already reported
        text = strip_comments(p.read_text(encoding="utf-8"))
        b = check_brace_balance(text)
        if b != 0:
            errs.append(f"{name}: brace balance = {b}")
        for e in check_env_balance(text):
            errs.append(f"{name}: {e}")
        for e in check_forbidden(text):
            errs.append(f"{name}: {e}")
    # main.tex checks
    main = output_dir / "main.tex"
    if main.exists():
        text = strip_comments(main.read_text(encoding="utf-8"))
        b = check_brace_balance(text)
        if b != 0:
            errs.append(f"main.tex: brace balance = {b}")
        for e in check_env_balance(text):
            errs.append(f"main.tex: {e}")
        # \input targets exist
        for m in re.finditer(r"\\input\{([^}]+)\}", text):
            target = m.group(1)
            if not (target.endswith(".tex")):
                target = target + ".tex"
            if not (output_dir / target).exists():
                errs.append(f"main.tex: \\input{{{m.group(1)}}} → missing file {target}")
    return errs


# ---------------------------------------------------------------------------
# Main assembly
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--polished-dir", required=True)
    ap.add_argument("--revised-dir", default="")
    ap.add_argument("--drift-decisions", default="")
    ap.add_argument("--bib-file", default="")
    ap.add_argument("--target-journal", default="")
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    polished_dir = Path(args.polished_dir)
    if not polished_dir.exists():
        print(f"ERROR: polished-dir not found: {polished_dir}", file=sys.stderr)
        sys.exit(1)
    revised_dir = Path(args.revised_dir) if args.revised_dir else None
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load drift decisions
    decisions = {}
    if args.drift_decisions and Path(args.drift_decisions).exists():
        drift = json.loads(Path(args.drift_decisions).read_text(encoding="utf-8"))
        decisions = drift.get("section_decisions", {})

    # Copy sections
    fallbacks = []
    missing_sections = []
    for name in SECTIONS:
        stem = name.replace(".tex", "")
        dec = decisions.get(stem, {"use": "polished"})
        use_revised = dec.get("use") == "revised"

        src = None
        if use_revised and revised_dir and (revised_dir / name).exists():
            src = revised_dir / name
            fallbacks.append({"section": stem, "reason": dec.get("reason", "drift")})
        elif (polished_dir / name).exists():
            src = polished_dir / name
        else:
            missing_sections.append(name)
            continue

        content = src.read_text(encoding="utf-8")
        if use_revised:
            header = (
                f"% [FINALIZE] This section uses step4 (revised) text — "
                f"semantic drift detected during Phase 6b.\n"
                f"% Reason: {dec.get('reason', '—')}\n"
                f"% See final_check_report.md for details.\n\n"
            )
            content = header + content
        (output_dir / name).write_text(content, encoding="utf-8")

    # Prune bib
    pruned_text = ""
    missing_keys = []
    cited_keys = extract_cite_keys_from_tex(output_dir)
    if args.bib_file:
        pruned_text, missing_keys = prune_bib(Path(args.bib_file), cited_keys)
        (output_dir / "references.bib").write_text(pruned_text, encoding="utf-8")

    # Write main.tex
    preamble, bibstyle, preamble_note = select_preamble(args.target_journal)
    inputs = "\n".join(
        f"\\input{{{name.replace('.tex', '')}}}"
        for name in SECTIONS
        if (output_dir / name).exists()
    )
    main_tex = (
        f"% {preamble_note} — target journal: {args.target_journal or 'unspecified'}\n"
        f"{preamble}\n"
        f"{inputs}\n\n"
        f"\\bibliographystyle{{{bibstyle}}}\n"
        f"\\bibliography{{references}}\n\n"
        f"\\end{{document}}\n"
    )
    (output_dir / "main.tex").write_text(main_tex, encoding="utf-8")

    # Structural sanity
    errors = structural_sanity(output_dir)

    # Build log
    log = {
        "target_journal": args.target_journal,
        "preamble": preamble_note,
        "bibstyle": bibstyle,
        "sections_written": [n for n in SECTIONS if (output_dir / n).exists()],
        "missing_sections": missing_sections,
        "fallbacks": fallbacks,
        "cited_keys_count": len(cited_keys),
        "missing_bib_keys": missing_keys,
        "structural_errors": errors,
    }
    (output_dir / "_build_log.json").write_text(
        json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # Report
    print(
        f"LaTeX package built → {output_dir}", file=sys.stderr,
    )
    print(f"  sections: {len(log['sections_written'])}  fallbacks: {len(fallbacks)}",
          file=sys.stderr)
    print(f"  cited keys: {len(cited_keys)}  missing in bib: {len(missing_keys)}",
          file=sys.stderr)
    if errors:
        print(f"  STRUCTURAL ERRORS:", file=sys.stderr)
        for e in errors:
            print(f"    - {e}", file=sys.stderr)
        sys.exit(2)
    print("  structural sanity: passed", file=sys.stderr)


if __name__ == "__main__":
    main()
