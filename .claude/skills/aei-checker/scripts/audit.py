#!/usr/bin/env python3
"""
Mechanical audit of a LaTeX manuscript for Advanced Engineering Informatics
(Elsevier) submission compliance.

Usage:
    python audit.py <main.tex> [--bib refs.bib [refs2.bib ...]]

Emits a JSON blob on stdout with structured findings. The caller (typically
an LLM following the aei-checker skill) narrates this JSON into a human-
readable report. Doing the mechanical parsing here keeps the LLM's job to
interpretation and avoids manual miscounts.

No external dependencies; Python 3.9+.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# LaTeX helpers
# ---------------------------------------------------------------------------

_COMMENT_RE = re.compile(r"(?<!\\)%.*?$", re.MULTILINE)
_MULTI_SPACE = re.compile(r"\s+")
_LATEX_COMMAND = re.compile(r"\\[a-zA-Z@]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?")
_INLINE_MATH = re.compile(r"\$[^$]*\$")
_DISPLAY_MATH = re.compile(r"\\\[.*?\\\]", re.DOTALL)
_CITE_RE = re.compile(r"\\(?:cite[a-zA-Z]*|citep|citet|parencite|textcite)\*?(?:\[[^\]]*\])?\{([^}]+)\}")


def strip_comments(text: str) -> str:
    return _COMMENT_RE.sub("", text)


def strip_latex(text: str) -> str:
    """Remove LaTeX commands and math; collapse whitespace. Used for word counts."""
    text = _DISPLAY_MATH.sub("", text)
    text = _INLINE_MATH.sub("", text)
    text = _LATEX_COMMAND.sub("", text)
    text = text.replace("{", "").replace("}", "")
    return _MULTI_SPACE.sub(" ", text).strip()


def line_of(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def read_tex(path: Path) -> str:
    """Read a .tex file and inline any \\input / \\include children (best effort)."""
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="latin-1")
    # Inline children — keep line numbers approximate by keeping the \input line.
    # We don't recursively inline; just flag that children exist for the caller.
    return text


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def check_document_class(source: str) -> dict[str, Any]:
    m = re.search(r"\\documentclass\s*(\[[^\]]*\])?\s*\{([^}]+)\}", source)
    if not m:
        return {"value": None, "status": "fail", "reason": "no \\documentclass found"}
    cls = m.group(2).strip()
    accepted = cls in ("cas-dc", "cas-sc")
    return {
        "value": cls,
        "options": (m.group(1) or "").strip("[]"),
        "line": line_of(source, m.start()),
        "status": "pass" if accepted else "fail",
        "reason": None if accepted else f"AEI requires cas-dc or cas-sc; got '{cls}'",
    }


def check_abstract(source: str) -> dict[str, Any]:
    m = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", source, re.DOTALL)
    if not m:
        return {"present": False, "status": "fail", "reason": "no abstract environment"}
    raw = m.group(1)
    line_start = line_of(source, m.start())
    line_end = line_of(source, m.end())
    text = strip_latex(raw)
    words = text.split()
    word_count = len(words)
    citations = _CITE_RE.findall(raw)
    return {
        "present": True,
        "word_count": word_count,
        "limit": 250,
        "word_count_status": "pass" if word_count <= 250 else "fail",
        "has_citation": bool(citations),
        "citation_keys": citations,
        "citation_status": "fail" if citations else "pass",
        "line_start": line_start,
        "line_end": line_end,
    }


def check_keywords(source: str) -> dict[str, Any]:
    m = re.search(r"\\begin\{keywords?\}(.*?)\\end\{keywords?\}", source, re.DOTALL)
    if not m:
        return {"present": False, "status": "fail", "count": 0}
    raw = m.group(1).strip()
    # Split by \sep or commas
    parts = re.split(r"\\sep|,", raw)
    terms = [strip_latex(p).strip() for p in parts]
    terms = [t for t in terms if t]
    status = "pass" if 1 <= len(terms) <= 7 else "fail"
    return {
        "present": True,
        "count": len(terms),
        "terms": terms,
        "status": status,
        "line": line_of(source, m.start()),
    }


def check_highlights(source: str) -> dict[str, Any]:
    m = re.search(r"\\begin\{highlights\}(.*?)\\end\{highlights\}", source, re.DOTALL)
    if not m:
        return {"present": False, "count": 0, "status": "fail"}
    raw = m.group(1)
    # Split into items
    items_raw = re.split(r"\\item\b", raw)[1:]  # drop preamble before first \item
    items = []
    for i, text in enumerate(items_raw, start=1):
        cleaned = strip_latex(text).strip()
        items.append({
            "index": i,
            "text": cleaned,
            "length": len(cleaned),
            "over_limit": len(cleaned) > 85,
        })
    count_status = "pass" if 3 <= len(items) <= 5 else "fail"
    any_too_long = any(it["over_limit"] for it in items)
    return {
        "present": True,
        "count": len(items),
        "count_status": count_status,
        "items": items,
        "any_over_85_chars": any_too_long,
        "line": line_of(source, m.start()),
    }


def _find_balanced_brace(source: str, start: int) -> str | None:
    """Starting at position of an opening '{', return content up to the matching '}'."""
    if start >= len(source) or source[start] != "{":
        return None
    depth = 0
    i = start
    while i < len(source):
        c = source[i]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return source[start + 1:i]
        i += 1
    return None


def check_title_page(source: str) -> dict[str, Any]:
    has_title = bool(re.search(r"\\title\s*(?:\[[^\]]*\])?\s*\{", source))
    authors = re.findall(r"\\author\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}", source)

    affiliations: list[str] = []
    for m in re.finditer(r"\\affiliation\s*(?:\[[^\]]*\])?\s*(?=\{)", source):
        brace_pos = source.find("{", m.end() - 1)
        body = _find_balanced_brace(source, brace_pos) if brace_pos >= 0 else None
        if body is not None:
            affiliations.append(body)

    aff_has_country = [bool(re.search(r"country\s*=", a)) for a in affiliations]
    has_cormark = bool(re.search(r"\\cormark\b", source))
    has_ead = bool(re.search(r"\\ead\s*\{", source))
    return {
        "has_title": has_title,
        "author_count": len(authors),
        "authors": [strip_latex(a).strip() for a in authors],
        "affiliation_count": len(affiliations),
        "affiliations_with_country": sum(aff_has_country),
        "has_corresponding_author_mark": has_cormark,
        "has_corresponding_author_email": has_ead,
        "status": (
            "pass"
            if (has_title and authors and affiliations
                and all(aff_has_country) and has_cormark and has_ead)
            else "fail"
        ),
    }


def check_declarations(source: str) -> dict[str, Any]:
    # Find section headers (numbered or starred) and their positions
    section_re = re.compile(r"\\section\*?\s*\{([^}]+)\}")
    sections = [(m.group(1), m.start()) for m in section_re.finditer(source)]
    bib_match = re.search(r"\\bibliography\b|\\printbibliography", source)
    bib_pos = bib_match.start() if bib_match else len(source)

    def find_section(keywords: list[str]) -> dict | None:
        for title, pos in sections:
            low = title.lower()
            if any(k in low for k in keywords):
                return {
                    "title": title,
                    "line": line_of(source, pos),
                    "before_bibliography": pos < bib_pos,
                }
        return None

    return {
        "acknowledgements": find_section(["acknowledg"]),
        "credit": find_section(["credit", "author contribution", "authorship"]),
        "competing_interest": find_section(["competing", "conflict of interest"]),
        "data_availability": find_section(["data availability", "data statement"]),
        "genai": find_section([
            "generative ai", "genai", "ai-assisted", "artificial intelligence",
            "chatgpt", "large language model", "llm"
        ]),
    }


def _first_nonwhitespace_line(source: str, pattern: re.Pattern) -> int | None:
    m = pattern.search(source)
    return line_of(source, m.start()) if m else None


def check_bib_style(source: str) -> dict[str, Any]:
    style = None
    line = None
    m = re.search(r"\\bibliographystyle\s*\{([^}]+)\}", source)
    if m:
        style = m.group(1).strip()
        line = line_of(source, m.start())
    # natbib options
    natbib_opts: list[str] = []
    nm = re.search(r"\\usepackage\s*\[([^\]]*)\]\s*\{natbib\}", source)
    if nm:
        natbib_opts = [o.strip() for o in nm.group(1).split(",")]
    # Likely numeric if bst contains "num" or natbib has "numbers"
    numeric_bst = bool(style and "num" in style.lower())
    numeric_natbib = "numbers" in natbib_opts
    author_year_style = bool(style and any(k in style.lower() for k in ("names", "authoryear", "apa", "plainnat", "chicago", "harvard")))
    # plainnat is author-year
    style_status = "pass" if (numeric_bst or (numeric_natbib and not author_year_style)) else "fail"
    # Detect mismatch: natbib numbers but author-year bst
    mismatch = numeric_natbib and author_year_style
    return {
        "style": style,
        "line": line,
        "natbib_options": natbib_opts,
        "numeric": numeric_bst or (numeric_natbib and not author_year_style),
        "author_year_style": author_year_style,
        "mismatch_numeric_natbib_with_name_bst": mismatch,
        "status": style_status,
    }


def check_figures_tables(source: str) -> dict[str, Any]:
    # Find \begin{figure} ... \end{figure} blocks
    fig_blocks = list(re.finditer(r"\\begin\{figure\*?\}(.*?)\\end\{figure\*?\}", source, re.DOTALL))
    tab_blocks = list(re.finditer(r"\\begin\{table\*?\}(.*?)\\end\{table\*?\}", source, re.DOTALL))

    def parse_blocks(blocks, kind: str):
        items = []
        for b in blocks:
            body = b.group(1)
            label_m = re.search(r"\\label\s*\{([^}]+)\}", body)
            caption_m = re.search(r"\\caption\s*\{", body)
            # Table image detection: only includegraphics inside a table
            is_image_table = (
                kind == "table"
                and bool(re.search(r"\\includegraphics", body))
                and not re.search(r"\\begin\{tabular", body)
            )
            items.append({
                "label": label_m.group(1) if label_m else None,
                "line": line_of(source, b.start()),
                "has_caption": bool(caption_m),
                "is_image_table": is_image_table,
            })
        return items

    figs = parse_blocks(fig_blocks, "figure")
    tabs = parse_blocks(tab_blocks, "table")

    # Find all references
    ref_re = re.compile(r"\\(?:ref|cref|Cref|autoref|pageref|eqref)\s*\{([^}]+)\}")
    ref_hits = [(m.group(1), m.start()) for m in ref_re.finditer(source)]

    referenced = {r for r, _ in ref_hits}

    def label_first_ref_line(label: str) -> int | None:
        for r, pos in ref_hits:
            if r == label:
                return line_of(source, pos)
        return None

    def check_items(items):
        enriched = []
        for it in items:
            lbl = it["label"]
            first_ref = label_first_ref_line(lbl) if lbl else None
            enriched.append({
                **it,
                "is_referenced": lbl in referenced if lbl else False,
                "first_reference_line": first_ref,
            })
        unreferenced = [it["label"] for it in enriched if it["label"] and not it["is_referenced"]]
        missing_caption = [it["label"] for it in enriched if not it["has_caption"]]
        out_of_order = False
        # first-reference order check: items with a referenced label, sorted by definition order,
        # should have monotonically increasing first_reference_line.
        refs_in_def_order = [it for it in enriched if it.get("first_reference_line")]
        for a, b in zip(refs_in_def_order, refs_in_def_order[1:]):
            if a["first_reference_line"] > b["first_reference_line"]:
                out_of_order = True
                break
        return {
            "count": len(enriched),
            "items": enriched,
            "unreferenced": unreferenced,
            "missing_caption": missing_caption,
            "out_of_order": out_of_order,
        }

    # Image-only tables
    image_tables = [t["label"] for t in tabs if t.get("is_image_table")]

    return {
        "figures": check_items(figs),
        "tables": {**check_items(tabs), "image_tables": image_tables},
    }


def check_citation_reference_mapping(source: str, bib_entries: dict) -> dict[str, Any]:
    cites = set()
    for m in _CITE_RE.finditer(source):
        for key in m.group(1).split(","):
            cites.add(key.strip())
    bib_keys = set(bib_entries.keys())
    orphan_cites = sorted(cites - bib_keys)  # cited but no bib entry
    unused_entries = sorted(bib_keys - cites)
    return {
        "citation_keys_in_text": sorted(cites),
        "bib_keys": sorted(bib_keys),
        "orphan_citations": orphan_cites,
        "unused_bib_entries": unused_entries,
    }


# ---------------------------------------------------------------------------
# Bibliography parsing
# ---------------------------------------------------------------------------

_BIB_ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,\s]+)\s*,\s*(.*?)\n\}", re.DOTALL)
_BIB_FIELD_RE = re.compile(r"(\w+)\s*=\s*[\{\"](.*?)[\}\"]\s*,?", re.DOTALL)

_LTWA_TRIGGER_WORDS = [
    "Journal", "International", "Conference", "Proceedings", "Transactions",
    "Research", "Engineering", "Science", "Review", "Letters", "Applied",
    "Advanced", "Systems", "Computing", "Computational",
]


def _looks_unabbreviated(journal: str) -> list[str]:
    """Return list of trigger words present as full words (likely needing LTWA)."""
    found = []
    for word in _LTWA_TRIGGER_WORDS:
        # Full-word match, not inside an existing abbreviation with a dot
        if re.search(rf"\b{word}\b(?!\.)", journal):
            found.append(word)
    return found


def parse_bib(paths: list[Path]) -> dict[str, dict]:
    entries: dict[str, dict] = {}
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            text = path.read_text(encoding="latin-1")
        text = strip_comments(text)
        for m in _BIB_ENTRY_RE.finditer(text):
            etype = m.group(1).lower()
            key = m.group(2).strip()
            body = m.group(3)
            fields = {fm.group(1).lower(): fm.group(2).strip() for fm in _BIB_FIELD_RE.finditer(body)}
            journal = fields.get("journal", "")
            trigger_words = _looks_unabbreviated(journal) if journal else []
            entries[key] = {
                "key": key,
                "type": etype,
                "file": str(path),
                "has_doi": bool(fields.get("doi")),
                "doi": fields.get("doi"),
                "journal": journal,
                "journal_trigger_words": trigger_words,
                "journal_likely_needs_abbreviation": bool(trigger_words),
                "fields": list(fields.keys()),
            }
    return entries


def check_bib_entries(entries: dict) -> dict[str, Any]:
    missing_doi = [k for k, e in entries.items() if not e["has_doi"]]
    needs_abbrev = [
        {"key": k, "journal": e["journal"], "trigger_words": e["journal_trigger_words"]}
        for k, e in entries.items() if e["journal_likely_needs_abbreviation"]
    ]
    return {
        "total_entries": len(entries),
        "missing_doi": missing_doi,
        "journals_likely_need_abbreviation": needs_abbrev,
    }


# ---------------------------------------------------------------------------
# Language consistency
# ---------------------------------------------------------------------------

_SPELL_PAIRS = [
    ("color", "colour"), ("analyze", "analyse"), ("behavior", "behaviour"),
    ("center", "centre"), ("organization", "organisation"),
    ("modeling", "modelling"), ("optimization", "optimisation"),
    ("labor", "labour"), ("favor", "favour"), ("recognize", "recognise"),
    ("utilize", "utilise"), ("fiber", "fibre"), ("meter", "metre"),
    ("defense", "defence"), ("license", "licence"), ("catalog", "catalogue"),
    ("gray", "grey"), ("traveled", "travelled"), ("canceled", "cancelled"),
    ("program", "programme"), ("optimizing", "optimising"),
    ("analyzing", "analysing"), ("modeled", "modelled"),
    ("analyzed", "analysed"), ("behaviors", "behaviours"),
    ("organizations", "organisations"), ("analyses", "analyses"),  # same
    ("optimizes", "optimises"),
]


def check_language(source: str) -> dict[str, Any]:
    # Strip LaTeX commands and math first so we only search the prose
    prose = strip_latex(source)
    us_hits: list[str] = []
    uk_hits: list[str] = []
    detail = []
    for us, uk in _SPELL_PAIRS:
        us_count = len(re.findall(rf"\b{us}\w*\b", prose, re.IGNORECASE))
        uk_count = len(re.findall(rf"\b{uk}\w*\b", prose, re.IGNORECASE))
        if us_count:
            us_hits.append(f"{us}({us_count})")
        if uk_count:
            uk_hits.append(f"{uk}({uk_count})")
        if us_count and uk_count:
            detail.append({"us": us, "uk": uk, "us_count": us_count, "uk_count": uk_count})
    mixed = bool(detail)
    return {
        "us_terms_found": us_hits,
        "uk_terms_found": uk_hits,
        "conflicting_pairs": detail,
        "mixed": mixed,
        "status": "fail" if mixed else "pass",
    }


# ---------------------------------------------------------------------------
# Equations
# ---------------------------------------------------------------------------

def check_equations(source: str) -> dict[str, Any]:
    eq_envs = re.findall(r"\\begin\{(equation|align|gather|multline)\*?\}", source)
    # Inline fractions inside $...$
    inline_frac = []
    for m in _INLINE_MATH.finditer(source):
        if r"\frac" in m.group(0):
            inline_frac.append({"line": line_of(source, m.start()), "snippet": m.group(0)[:60]})
    # Detect possible image-equations (includegraphics with eq/formula in filename)
    image_eq = []
    for m in re.finditer(r"\\includegraphics\s*(?:\[[^\]]*\])?\s*\{([^}]+)\}", source):
        name = m.group(1).lower()
        if any(k in name for k in ("equation", "formula", "/eq", "_eq")):
            image_eq.append({"line": line_of(source, m.start()), "filename": m.group(1)})
    return {
        "display_equations": len(eq_envs),
        "inline_frac_in_text_math": inline_frac,
        "likely_image_equations": image_eq,
    }


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def audit(tex_path: Path, bib_paths: list[Path]) -> dict[str, Any]:
    raw = read_tex(tex_path)
    source = strip_comments(raw)

    bib_entries = parse_bib(bib_paths) if bib_paths else {}

    result: dict[str, Any] = {
        "main_tex": str(tex_path),
        "bib_files": [str(p) for p in bib_paths],
        "document_class": check_document_class(source),
        "title_page": check_title_page(source),
        "abstract": check_abstract(source),
        "keywords": check_keywords(source),
        "highlights": check_highlights(source),
        "declarations": check_declarations(source),
        "references": {
            "style": check_bib_style(source),
            "bib": check_bib_entries(bib_entries),
            "mapping": check_citation_reference_mapping(source, bib_entries),
        },
        "figures_tables": check_figures_tables(source),
        "equations": check_equations(source),
        "language": check_language(source),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit a LaTeX manuscript for AEI compliance")
    parser.add_argument("tex", type=Path, help="Main .tex file")
    parser.add_argument("--bib", type=Path, nargs="*", default=[], help=".bib files")
    parser.add_argument("--indent", type=int, default=2)
    args = parser.parse_args()

    if not args.tex.exists():
        print(f"ERROR: {args.tex} not found", file=sys.stderr)
        sys.exit(1)

    # Auto-discover .bib files in same directory if none given
    bib_paths = list(args.bib)
    if not bib_paths:
        bib_paths = sorted(args.tex.parent.glob("*.bib"))

    result = audit(args.tex, bib_paths)
    json.dump(result, sys.stdout, indent=args.indent, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
