#!/usr/bin/env python3
"""
Build bilingual Markdown scaffold (Phase 6c.2 of Journal Finalize).

Splits each section .tex file into subsections and emits an Obsidian-flavored
Markdown file per section with:

  ## <section title>

  ### <subsection title>

  > [!quote] EN
  > <en paragraph(s) converted from LaTeX>

  > [!quote] 繁中
  > <!-- 繁中 translation to be filled by LLM -->

  > [!edit] ✏️ Revision Zone
  > <!-- 修改意見或直接修改英文段落 -->

  ---

  ### <next subsection title>
  ...

If a section has no \\subsection, the whole section body becomes a single
subsection-level pair.

LaTeX→Markdown conversion for EN:
  \\cite{K}           → [K]
  \\cite{K1,K2}       → [K1, K2]
  \\ref{fig:X}        → Fig. X
  \\ref{tab:X}        → Table X
  \\ref{eq:X}         → Eq. (X)
  \\eqref{eq:X}       → Eq. (X)
  \\textbf{...}       → **...**
  \\emph{...} / \\textit{...} → *...*
  $...$ and equation envs → kept verbatim (Obsidian MathJax renders them)

Usage (build):
    python build_bilingual_scaffold.py \\
        --latex-dir step6_final/latex \\
        --output-dir step6_final/bilingual

Usage (verify after translation):
    python build_bilingual_scaffold.py --verify \\
        --latex-dir step6_final/latex \\
        --bilingual-dir step6_final/bilingual
"""

import argparse
import json
import re
import sys
from pathlib import Path


SECTIONS = [
    ("00_abstract.tex", "Abstract"),
    ("01_introduction.tex", "Introduction"),
    ("02_related_work.tex", "Related Work"),
    ("03_methods.tex", "Methods"),
    ("04_results.tex", "Results"),
    ("05_discussion.tex", "Discussion"),
    ("06_conclusion.tex", "Conclusion"),
]


# ---------------------------------------------------------------------------
# LaTeX → Markdown conversion (EN side)
# ---------------------------------------------------------------------------

def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


def _convert_ref(match: re.Match) -> str:
    key = match.group(1)
    if key.startswith("fig:"):
        return f"Fig. {key[4:]}"
    if key.startswith("tab:"):
        return f"Table {key[4:]}"
    if key.startswith("eq:"):
        return f"Eq. ({key[3:]})"
    return f"({key})"


def _convert_cite(match: re.Match) -> str:
    keys = [k.strip() for k in match.group(1).split(",")]
    return "[" + ", ".join(keys) + "]"


def latex_to_markdown(body: str) -> str:
    """Convert a LaTeX prose block to Markdown. Preserves math verbatim."""
    t = strip_comments(body)

    # Placeholder math so we don't transform inside it
    math_store: list[str] = []

    def stash_math(m):
        math_store.append(m.group(0))
        return f"\x00MATH{len(math_store) - 1}\x00"

    # Display math first (both \[ ... \] and equation/align/gather)
    t = re.sub(r"\\\[.*?\\\]", stash_math, t, flags=re.DOTALL)
    t = re.sub(
        r"\\begin\{(equation|align|gather|eqnarray)\*?\}.*?\\end\{\1\*?\}",
        stash_math,
        t,
        flags=re.DOTALL,
    )
    # Inline math
    t = re.sub(r"\$[^$\n]+\$", stash_math, t)

    # Citations and refs
    t = re.sub(r"\\cite[tp]?\*?\{([^}]+)\}", _convert_cite, t)
    t = re.sub(r"\\(?:auto)?ref\{([^}]+)\}", _convert_ref, t)
    t = re.sub(r"\\eqref\{eq:([^}]+)\}", lambda m: f"Eq. ({m.group(1)})", t)
    t = re.sub(r"\\eqref\{([^}]+)\}", lambda m: f"Eq. ({m.group(1)})", t)

    # Emphasis
    t = re.sub(r"\\textbf\{([^}]+)\}", r"**\1**", t)
    t = re.sub(r"\\(?:emph|textit)\{([^}]+)\}", r"*\1*", t)
    t = re.sub(r"\\underline\{([^}]+)\}", r"__\1__", t)

    # \label inside prose → drop silently (Markdown has no \label)
    t = re.sub(r"\\label\{[^}]+\}", "", t)

    # Strip remaining LaTeX commands (keep their argument text where simple)
    t = re.sub(r"\\(?:textsc|texttt|textrm)\{([^}]+)\}", r"\1", t)
    # Drop any remaining unknown commands with an argument
    t = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?\{([^}]*)\}", r"\1", t)
    # Drop remaining unknown commands without argument
    t = re.sub(r"\\[a-zA-Z]+\*?", " ", t)

    # Clean up braces
    t = re.sub(r"[{}]", "", t)
    # Normalise whitespace inside paragraphs
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", t)]
    paragraphs = [p for p in paragraphs if p]
    t = "\n\n".join(paragraphs)

    # Restore math
    def restore_math(m):
        i = int(m.group(1))
        return math_store[i]

    t = re.sub(r"\x00MATH(\d+)\x00", restore_math, t)
    return t


# ---------------------------------------------------------------------------
# Section splitting
# ---------------------------------------------------------------------------

def split_into_subsections(tex: str) -> list[dict]:
    """Return [{'title': str, 'body': str}, ...]. If no \\subsection exists,
    returns a single subsection with title=None."""
    tex = strip_comments(tex)
    # Strip leading \section{...} if present
    # (journal section files typically start with \section{Introduction})
    tex = re.sub(r"^\s*\\section\*?\{[^}]*\}\s*", "", tex, count=1)

    # Find all subsection headings and their spans
    pattern = re.compile(r"\\(subsection|subsubsection)\*?\{([^}]+)\}")
    matches = list(pattern.finditer(tex))
    if not matches:
        return [{"title": None, "level": 3, "body": tex.strip()}]

    subs = []
    # Prelude before first subsection
    prelude = tex[: matches[0].start()].strip()
    if prelude:
        subs.append({"title": None, "level": 3, "body": prelude})

    for i, m in enumerate(matches):
        title = m.group(2).strip()
        level = 3 if m.group(1) == "subsection" else 4
        end = matches[i + 1].start() if i + 1 < len(matches) else len(tex)
        body = tex[m.end():end].strip()
        subs.append({"title": title, "level": level, "body": body})

    return subs


def format_callout(kind: str, title: str, body: str) -> str:
    """Produce an Obsidian callout block. Body is prefixed with '> ' per line."""
    lines = body.split("\n")
    quoted = "\n".join(f"> {ln}" if ln else ">" for ln in lines)
    return f"> [!{kind}] {title}\n{quoted}"


def build_section_md(section_title: str, subsections: list[dict]) -> str:
    out = [f"## {section_title}\n"]
    for sub in subsections:
        if sub["title"]:
            heading_prefix = "#" * sub["level"]
            out.append(f"{heading_prefix} {sub['title']}\n")
        en_md = latex_to_markdown(sub["body"]).strip() or "_(empty)_"
        out.append(format_callout("quote", "EN", en_md))
        out.append("")
        out.append(format_callout("quote", "繁中", "<!-- 繁中 translation to be filled -->"))
        out.append("")
        out.append(format_callout("edit", "✏️ Revision Zone", "<!-- 修改意見或直接修改英文段落 -->"))
        out.append("")
        out.append("---\n")
    return "\n".join(out)


# ---------------------------------------------------------------------------
# Verify mode
# ---------------------------------------------------------------------------

def verify_scaffold(latex_dir: Path, bilingual_dir: Path) -> list[str]:
    """Check that each .md file has the same number of subsections as source,
    and that math / citations are preserved."""
    issues = []
    for fname, title in SECTIONS:
        tex_path = latex_dir / fname
        md_path = bilingual_dir / fname.replace(".tex", ".md")
        if not tex_path.exists():
            continue
        if not md_path.exists():
            issues.append(f"{fname}: bilingual .md missing")
            continue
        tex = tex_path.read_text(encoding="utf-8")
        md = md_path.read_text(encoding="utf-8")

        # Subsection count
        subs = split_into_subsections(tex)
        expected = len(subs)
        actual = md.count("> [!quote] EN")
        if actual != expected:
            issues.append(f"{fname}: expected {expected} EN callouts, found {actual}")
        # 繁中 callout count must match
        zh_actual = md.count("> [!quote] 繁中")
        if zh_actual != expected:
            issues.append(f"{fname}: expected {expected} 繁中 callouts, found {zh_actual}")
        # Revision zones
        rz_actual = md.count("> [!edit]")
        if rz_actual != expected:
            issues.append(f"{fname}: expected {expected} Revision Zones, found {rz_actual}")

        # Citations preserved: every \cite{K} in tex → [K] in md (at least once)
        cite_keys = set()
        for m in re.finditer(r"\\cite[tp]?\*?\{([^}]+)\}", strip_comments(tex)):
            for k in m.group(1).split(","):
                cite_keys.add(k.strip())
        for k in cite_keys:
            if f"[{k}" not in md and f", {k}" not in md and f",{k}" not in md:
                issues.append(f"{fname}: citation key '{k}' from .tex not found in .md")

        # Math preserved: every inline math $x$ → $x$ in md (count-based)
        tex_inline = len(re.findall(r"\$[^$\n]+\$", strip_comments(tex)))
        md_inline = len(re.findall(r"\$[^$\n]+\$", md))
        if md_inline < tex_inline:
            issues.append(
                f"{fname}: inline math count: .tex={tex_inline}, .md={md_inline} (some math lost)"
            )

    return issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--latex-dir", required=True)
    ap.add_argument("--output-dir", default="")
    ap.add_argument("--bilingual-dir", default="", help="Only used with --verify")
    ap.add_argument("--verify", action="store_true")
    args = ap.parse_args()

    latex_dir = Path(args.latex_dir)
    if not latex_dir.exists():
        print(f"ERROR: latex dir not found: {latex_dir}", file=sys.stderr)
        sys.exit(1)

    if args.verify:
        biling = Path(args.bilingual_dir or args.output_dir)
        if not biling.exists():
            print(f"ERROR: bilingual dir not found: {biling}", file=sys.stderr)
            sys.exit(1)
        issues = verify_scaffold(latex_dir, biling)
        if issues:
            print(f"Verification FAILED ({len(issues)} issue(s)):", file=sys.stderr)
            for i in issues:
                print(f"  - {i}", file=sys.stderr)
            sys.exit(2)
        print("Verification passed.", file=sys.stderr)
        return

    if not args.output_dir:
        print("ERROR: --output-dir required when not in --verify mode", file=sys.stderr)
        sys.exit(1)
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = {"sections_written": [], "sections_missing": []}
    for fname, title in SECTIONS:
        src = latex_dir / fname
        if not src.exists():
            summary["sections_missing"].append(fname)
            continue
        tex = src.read_text(encoding="utf-8")
        subs = split_into_subsections(tex)
        md = build_section_md(title, subs)
        md_name = fname.replace(".tex", ".md")
        (out_dir / md_name).write_text(md, encoding="utf-8")
        summary["sections_written"].append({"file": md_name, "subsections": len(subs)})

    (out_dir / "_scaffold_log.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    print(f"Bilingual scaffold built → {out_dir}", file=sys.stderr)
    for s in summary["sections_written"]:
        print(f"  ✓ {s['file']} ({s['subsections']} subsection(s))", file=sys.stderr)
    if summary["sections_missing"]:
        print(f"  Missing: {', '.join(summary['sections_missing'])}", file=sys.stderr)


if __name__ == "__main__":
    main()
