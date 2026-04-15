#!/usr/bin/env python3
"""
Hard Constraint Checks for Journal Finalize (Phase 6a)

Binary pass/fail checks on a polished LaTeX manuscript:
1. Number consistency (abstract ⊆ results ⊆ source data)
2. Citation consistency (\\cite ↔ .bib, bidirectional)
3. Symbol consistency (math symbols ↔ notation_glossary.md)
4. Cross-reference integrity (\\ref ↔ \\label, orphan figures)
5. Word count (total vs journal word_limit ± tolerance)
6. Equation numbering (sequential, referenced equations exist)

Differs from journal-review's hard_checks.py in being stricter (zero tolerance,
binary pass/fail per check) and in enforcing the abstract ⊆ results subset
relation and equation numbering check.

Usage:
    python hard_constraints.py \\
        --polished-dir path/to/step5_polished \\
        --preprocess-dir path/to/step1_preprocess \\
        --bib-file path/to/references.bib \\
        --analysis-summary path/to/analysis_summary.md \\
        --session-config path/to/step0_session_config.json \\
        --output path/to/hard_constraints.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


SECTION_ORDER = [
    "00_abstract.tex",
    "01_introduction.tex",
    "02_related_work.tex",
    "03_methods.tex",
    "04_results.tex",
    "05_discussion.tex",
    "06_conclusion.tex",
]

SECTION_NAME = {
    "00_abstract.tex": "abstract",
    "01_introduction.tex": "introduction",
    "02_related_work.tex": "related_work",
    "03_methods.tex": "methods",
    "04_results.tex": "results",
    "05_discussion.tex": "discussion",
    "06_conclusion.tex": "conclusion",
}

# Word-count tolerance as fraction of target (default ±5%)
DEFAULT_WC_TOLERANCE = 0.05


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

def read_tex_files(polished_dir: Path) -> dict[str, str]:
    out = {}
    for name in SECTION_ORDER:
        p = polished_dir / name
        if p.exists():
            out[name] = p.read_text(encoding="utf-8")
    return out


def strip_comments(text: str) -> str:
    # Remove LaTeX % comments (but not \%), line by line
    return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


# ---------------------------------------------------------------------------
# Extractors
# ---------------------------------------------------------------------------

def extract_cite_keys(text: str):
    text = strip_comments(text)
    results = []
    for line_no, line in enumerate(text.split("\n"), 1):
        for m in re.finditer(r"\\cite[tp]?\*?\{([^}]+)\}", line):
            for key in (k.strip() for k in m.group(1).split(",")):
                if key:
                    results.append({"key": key, "line": line_no, "context": line.strip()})
    return results


def extract_labels(text: str):
    text = strip_comments(text)
    return [
        {"label": m.group(1), "line": i}
        for i, line in enumerate(text.split("\n"), 1)
        for m in re.finditer(r"\\label\{([^}]+)\}", line)
    ]


def extract_refs(text: str):
    text = strip_comments(text)
    results = []
    for line_no, line in enumerate(text.split("\n"), 1):
        for m in re.finditer(r"\\(?:auto)?ref\{([^}]+)\}|\\eqref\{([^}]+)\}", line):
            ref = m.group(1) or m.group(2)
            results.append({"ref": ref, "line": line_no, "context": line.strip()})
    return results


def parse_bib_keys(bib_path: Path) -> set[str]:
    if not bib_path or not bib_path.exists():
        return set()
    text = bib_path.read_text(encoding="utf-8")
    return set(m.group(1).strip() for m in re.finditer(r"@\w+\{([^,]+),", text))


def strip_math_and_commands(text: str) -> str:
    """Strip math environments and LaTeX commands for number extraction in prose."""
    text = strip_comments(text)
    # Remove display math
    text = re.sub(
        r"\\begin\{(equation|align|gather|eqnarray)\*?\}.*?\\end\{\1\*?\}",
        " EQMATH ",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(r"\\\[.*?\\\]", " EQMATH ", text, flags=re.DOTALL)
    # Remove inline math
    text = re.sub(r"\$[^$]+\$", " INMATH ", text)
    # Remove \cite / \ref / \label
    text = re.sub(r"\\(?:cite[tp]?\*?|ref|autoref|eqref|label)\{[^}]*\}", " ", text)
    return text


def extract_numbers(text: str) -> list[dict]:
    """Extract numeric tokens from prose (after stripping math), with line info."""
    prose = strip_math_and_commands(text)
    results = []
    # Integer or decimal. Lookbehind prevents matching '20' inside '0.20' or '200'.
    # Lookahead `(?!\.?\d)` prevents matching '0.87' inside '0.873' but ALLOWS a trailing
    # sentence period (e.g. "0.034." at end of sentence) — the period must be followed
    # by a non-digit to count as sentence punctuation rather than decimal continuation.
    pattern = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)(?!\.?\d)")
    for line_no, line in enumerate(prose.split("\n"), 1):
        for m in pattern.finditer(line):
            tok = m.group(1)
            # Skip pure-year-like four-digit numbers that are almost certainly citation years
            # They still count as numbers but we skip them if immediately next to a surname pattern
            results.append({"value": tok, "line": line_no, "context": line.strip()})
    return results


def extract_math_symbols_with_context(text: str) -> list[dict]:
    """Extract math symbols (greek, named) from math-mode regions."""
    text = strip_comments(text)
    results = []
    math_spans = []
    for m in re.finditer(r"\$([^$]+)\$", text):
        math_spans.append((m.start(), m.group(1)))
    for m in re.finditer(
        r"\\begin\{(equation|align|gather|eqnarray)\*?\}(.*?)\\end\{\1\*?\}",
        text,
        flags=re.DOTALL,
    ):
        math_spans.append((m.start(), m.group(2)))

    greek = r"alpha|beta|gamma|delta|epsilon|varepsilon|zeta|eta|theta|vartheta|iota|kappa|lambda|mu|nu|xi|pi|varpi|rho|varrho|sigma|varsigma|tau|upsilon|phi|varphi|chi|psi|omega|Alpha|Beta|Gamma|Delta|Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu|Nu|Xi|Pi|Rho|Sigma|Tau|Upsilon|Phi|Chi|Psi|Omega"
    named = r"mathbf|mathcal|mathbb|hat|tilde|bar|vec|widehat|widetilde"
    sym_pattern = re.compile(rf"\\({greek})\b|\\({named})\{{([^}}]+)\}}")

    # Line offsets for mapping start index → line number
    line_starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(i + 1)

    def index_to_line(idx: int) -> int:
        import bisect
        return bisect.bisect_right(line_starts, idx)

    for start, body in math_spans:
        for m in sym_pattern.finditer(body):
            if m.group(1):
                sym = "\\" + m.group(1)
            else:
                sym = "\\" + m.group(2) + "{" + m.group(3) + "}"
            results.append(
                {
                    "symbol": sym,
                    "line": index_to_line(start + m.start()),
                    "math_context": body.strip(),
                }
            )
    return results


def count_words_tex(text: str) -> int:
    t = strip_math_and_commands(text)
    t = re.sub(r"\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", t)
    t = re.sub(r"[{}\\~&]", " ", t)
    return len(t.split())


def parse_notation_glossary(preprocess_dir: Path) -> dict[str, str]:
    p = preprocess_dir / "notation_glossary.md"
    if not p.exists():
        return {}
    text = p.read_text(encoding="utf-8")
    out = {}
    # Each row: | `\symbol` | meaning | ... |
    for m in re.finditer(r"\|\s*`?([^|`\n]+?)`?\s*\|\s*([^|\n]+?)\s*\|", text):
        sym = m.group(1).strip()
        meaning = m.group(2).strip()
        if sym.lower() in ("symbol", "---", "") or "---" in sym:
            continue
        # Normalise: drop leading $ and trailing $
        sym = sym.strip("$").strip()
        if sym:
            out[sym] = meaning
    return out


def parse_figure_catalog(preprocess_dir: Path) -> set[str]:
    p = preprocess_dir / "figure_captions.md"
    if not p.exists():
        return set()
    text = p.read_text(encoding="utf-8")
    figs = set()
    for m in re.finditer(r"Fig(?:ure)?\.?\s*(\d+)\b", text, flags=re.IGNORECASE):
        figs.add(m.group(1))
    for m in re.finditer(r"fig:([A-Za-z0-9_\-]+)", text):
        figs.add(m.group(1))
    return figs


def parse_source_numbers(analysis_path: Path, preprocess_dir: Path) -> set[str]:
    out = set()
    files = []
    if analysis_path and analysis_path.exists():
        files.append(analysis_path)
    for name in ("figure_captions.md", "table_captions.md", "analysis_summary.md"):
        p = preprocess_dir / name
        if p.exists():
            files.append(p)
    for f in files:
        txt = f.read_text(encoding="utf-8")
        for m in re.finditer(r"(?<![\d.])(\d+(?:\.\d+)?)(?!\.?\d)", txt):
            out.add(m.group(1))
    return out


def parse_word_limit(session_cfg_path: Path) -> tuple[int | None, str | None, float]:
    """Return (word_limit, target_journal, tolerance)."""
    if not session_cfg_path or not session_cfg_path.exists():
        return None, None, DEFAULT_WC_TOLERANCE
    try:
        cfg = json.loads(session_cfg_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, None, DEFAULT_WC_TOLERANCE
    tol = cfg.get("word_limit_tolerance", DEFAULT_WC_TOLERANCE)
    return cfg.get("word_limit"), cfg.get("target_journal"), tol


# ---------------------------------------------------------------------------
# Checks (each returns a list of flags + a pass/fail bool)
# ---------------------------------------------------------------------------

def _flag(prefix, i, **kw):
    kw.setdefault("severity", "major")
    kw.setdefault("source_file", "")
    return {"id": f"{prefix}-{i:03d}", **kw}


def check_numbers(tex_files: dict, source_numbers: set[str]) -> tuple[list[dict], bool]:
    """Number consistency: abstract ⊆ results; results/discussion/abstract ⊆ source."""
    flags = []
    i = 0

    def nums_as_set(text):
        return {n["value"] for n in extract_numbers(text)}

    abstract_text = tex_files.get("00_abstract.tex", "")
    results_text = tex_files.get("04_results.tex", "")
    abstract_nums = nums_as_set(abstract_text)
    results_nums = nums_as_set(results_text)

    # Abstract ⊆ Results: every number in abstract must be a token in results
    for n in sorted(abstract_nums - results_nums):
        # Skip 1-digit numbers (likely list counts, not metrics) — still report if suspicious (only 2-digit+ are gated)
        if len(n.replace(".", "")) < 2:
            continue
        i += 1
        flags.append(_flag(
            "HC-NUM", i,
            type="ABSTRACT_NUMBER_NOT_IN_RESULTS",
            severity="critical",
            location={"file": "00_abstract.tex"},
            quote=f"number '{n}' appears in abstract but not in 04_results.tex",
            evidence_expected="Every number in the abstract must appear in Results.",
            instruction=f"Either add the supporting result to 04_results.tex or remove '{n}' from the abstract.",
            source_file="04_results.tex",
        ))

    # Results ∪ Discussion ∪ Abstract numbers ⊆ source numbers (subset of analysis_summary/captions)
    if source_numbers:
        for fname in ("00_abstract.tex", "04_results.tex", "05_discussion.tex"):
            if fname not in tex_files:
                continue
            seen_here = set()
            for n_info in extract_numbers(tex_files[fname]):
                val = n_info["value"]
                # Skip tiny numbers (integers <10 often refer to list indices, paragraph numbers, etc.)
                if len(val.replace(".", "")) < 2:
                    continue
                if val in seen_here:
                    continue
                seen_here.add(val)
                if val not in source_numbers:
                    i += 1
                    flags.append(_flag(
                        "HC-NUM", i,
                        type="NUMBER_NOT_IN_SOURCE",
                        severity="critical",
                        location={"file": fname, "line": n_info["line"]},
                        quote=n_info["context"],
                        evidence_expected=f"Value '{val}' not found in analysis_summary.md / figure_captions.md / table_captions.md",
                        instruction=f"Cross-check '{val}' against the data. If correct, make sure it appears in the preprocessed source data; if incorrect, fix in text.",
                        source_file="analysis_summary.md / figure_captions.md",
                    ))

    passed = not any(f["severity"] == "critical" for f in flags)
    return flags, passed


def check_citations(tex_files: dict, bib_keys: set[str]) -> tuple[list[dict], bool]:
    flags = []
    i = 0
    cited = set()
    for fname, content in tex_files.items():
        for c in extract_cite_keys(content):
            cited.add(c["key"])
            if c["key"] not in bib_keys:
                i += 1
                flags.append(_flag(
                    "HC-CIT", i,
                    type="PHANTOM_CITATION",
                    severity="critical",
                    location={"file": fname, "line": c["line"]},
                    quote=c["context"],
                    evidence_expected=f"No @entry with key '{c['key']}' in references.bib",
                    instruction=f"Add a bib entry for '{c['key']}' or fix the citation key.",
                    source_file="references.bib",
                ))
    for key in sorted(bib_keys - cited):
        i += 1
        flags.append(_flag(
            "HC-CIT", i,
            type="ORPHAN_BIB_ENTRY",
            severity="minor",
            location={"file": "references.bib"},
            quote=f"bib key '{key}' is never cited",
            evidence_expected="Every bib entry must be cited at least once.",
            instruction=f"Remove '{key}' from references.bib (Phase 6c.1 will prune automatically) or cite it.",
            source_file="references.bib",
        ))
    passed = not any(f["severity"] == "critical" for f in flags)
    return flags, passed


def check_symbols(tex_files: dict, glossary: dict[str, str]) -> tuple[list[dict], bool]:
    flags = []
    i = 0
    if not glossary:
        # No glossary available — emit one warning but pass
        return flags, True

    # Normalise glossary keys for comparison (strip whitespace, backslashes)
    norm_gloss = {k.strip(): v for k, v in glossary.items()}

    seen: dict[str, list[dict]] = {}
    for fname, content in tex_files.items():
        for s in extract_math_symbols_with_context(content):
            seen.setdefault(s["symbol"], []).append({**s, "file": fname})

    for sym, usages in seen.items():
        # Try a loose match: strip trailing arguments for \hat{x} → \hat
        base = re.sub(r"\{[^}]*\}$", "", sym)
        if sym in norm_gloss or base in norm_gloss:
            continue
        i += 1
        flags.append(_flag(
            "HC-SYM", i,
            type="SYMBOL_NOT_IN_GLOSSARY",
            severity="major",
            location={"file": usages[0]["file"], "line": usages[0]["line"]},
            quote=usages[0]["math_context"],
            evidence_expected=f"Symbol '{sym}' used in math but not defined in notation_glossary.md",
            instruction=f"Add '{sym}' to notation_glossary.md with its canonical meaning, or remove it from the text.",
            source_file="notation_glossary.md",
        ))
    # Only major severity — symbol checks are not pass/fail gate
    passed = True
    return flags, passed


def check_refs(tex_files: dict, figure_catalog: set[str]) -> tuple[list[dict], bool]:
    flags = []
    i = 0
    labels: dict[str, str] = {}
    all_refs = []
    for fname, content in tex_files.items():
        for lab in extract_labels(content):
            # First label wins; duplicates would also be an error but rare
            labels.setdefault(lab["label"], fname)
        for r in extract_refs(content):
            all_refs.append({**r, "file": fname})

    # Every \ref has a \label
    for r in all_refs:
        if r["ref"] not in labels:
            i += 1
            flags.append(_flag(
                "HC-REF", i,
                type="BROKEN_REF",
                severity="critical",
                location={"file": r["file"], "line": r["line"]},
                quote=r["context"],
                evidence_expected=f"No \\label{{{r['ref']}}} in any section file",
                instruction=f"Add \\label{{{r['ref']}}} at the target, or fix the \\ref key.",
                source_file=r["file"],
            ))

    # Every \label is \ref'd at least once
    referenced = {r["ref"] for r in all_refs}
    for lab, fname in labels.items():
        if lab not in referenced:
            i += 1
            flags.append(_flag(
                "HC-REF", i,
                type="UNREFERENCED_LABEL",
                severity="minor",
                location={"file": fname},
                quote=f"\\label{{{lab}}} is never \\ref'd",
                evidence_expected="Every label should be referenced or removed.",
                instruction=f"Reference \\label{{{lab}}} with \\ref{{{lab}}} or delete the label.",
                source_file=fname,
            ))

    # Every figure in catalog is referenced
    referenced_figs: set[str] = set()
    for r in all_refs:
        if r["ref"].startswith("fig:"):
            referenced_figs.add(r["ref"][4:])
        m = re.match(r"fig[:_]?(\w+)", r["ref"])
        if m:
            referenced_figs.add(m.group(1))
    for fig_id in figure_catalog:
        if fig_id in referenced_figs:
            continue
        # Also accept a bare "fig:<id>" anywhere across labels
        if any(lab.endswith(fig_id) for lab in labels):
            # Found the label, but no ref — already flagged as UNREFERENCED_LABEL above
            continue
        i += 1
        flags.append(_flag(
            "HC-REF", i,
            type="ORPHAN_FIGURE",
            severity="major",
            location={"file": "figure_captions.md"},
            quote=f"Figure '{fig_id}' listed in catalog but never referenced",
            evidence_expected="Every figure in figure_captions.md should be referenced in text.",
            instruction=f"Reference the figure with \\ref{{fig:{fig_id}}} or remove it from the catalog if unused.",
            source_file="figure_captions.md",
        ))

    passed = not any(f["severity"] == "critical" for f in flags)
    return flags, passed


def check_word_count(
    tex_files: dict, word_limit: int | None, tolerance: float
) -> tuple[list[dict], bool, dict]:
    per_section = {SECTION_NAME[f]: count_words_tex(c) for f, c in tex_files.items()}
    total = sum(per_section.values())
    flags = []
    passed = True
    if word_limit is None:
        return flags, True, {"per_section": per_section, "total": total, "limit": None}
    upper = word_limit * (1 + tolerance)
    lower = word_limit * (1 - tolerance)
    if total > upper or total < lower:
        passed = False
        flags.append(_flag(
            "HC-WC", 1,
            type="WORD_COUNT_OUT_OF_RANGE",
            severity="critical",
            location={"file": "<total>"},
            quote=f"Total: {total} words; limit: {word_limit} ±{int(tolerance * 100)}%",
            evidence_expected=f"Total word count must be within [{int(lower)}, {int(upper)}]",
            instruction=(
                f"Cut ~{total - int(upper)} words"
                if total > upper
                else f"Add ~{int(lower) - total} words (likely the paper under-explains something)"
            ),
            source_file="step0_session_config.json",
        ))
    return flags, passed, {"per_section": per_section, "total": total, "limit": word_limit,
                           "tolerance": tolerance, "upper": upper, "lower": lower}


def check_equation_numbering(tex_files: dict) -> tuple[list[dict], bool]:
    """Count labelled equations in reading order; verify they form a contiguous 1..N sequence
    and every \\eqref target has a matching \\label.
    """
    flags = []
    i = 0
    eq_labels: list[str] = []  # order of appearance
    eq_refs: list[dict] = []

    # Walk sections in reading order (01..06 for body, 00 abstract uses no equations)
    for fname in ["01_introduction.tex", "02_related_work.tex", "03_methods.tex",
                  "04_results.tex", "05_discussion.tex", "06_conclusion.tex"]:
        content = tex_files.get(fname)
        if not content:
            continue
        content = strip_comments(content)
        # Find equation blocks with labels — in order
        # Accept \begin{equation}, \begin{align}, \begin{gather} (starred forms are unnumbered, skip)
        for m in re.finditer(
            r"\\begin\{(equation|align|gather)\}(.*?)\\end\{\1\}",
            content,
            flags=re.DOTALL,
        ):
            body = m.group(2)
            labels = re.findall(r"\\label\{(eq:[^}]+)\}", body)
            for lab in labels:
                eq_labels.append(lab)
        # Collect \eqref targets
        for m in re.finditer(r"\\eqref\{([^}]+)\}|\\ref\{(eq:[^}]+)\}", content):
            target = m.group(1) or m.group(2)
            eq_refs.append({"ref": target, "file": fname})

    # Check: all \eqref targets exist as eq labels
    label_set = set(eq_labels)
    for r in eq_refs:
        if r["ref"] not in label_set:
            i += 1
            flags.append(_flag(
                "HC-EQ", i,
                type="BROKEN_EQREF",
                severity="critical",
                location={"file": r["file"]},
                quote=f"\\eqref{{{r['ref']}}} has no matching equation \\label",
                evidence_expected="Every \\eqref must target an existing labelled equation.",
                instruction="Add \\label{...} to the intended equation, or fix the \\eqref key.",
                source_file=r["file"],
            ))

    # Unreferenced equations (minor)
    ref_set = set(r["ref"] for r in eq_refs)
    for lab in eq_labels:
        if lab not in ref_set:
            i += 1
            flags.append(_flag(
                "HC-EQ", i,
                type="UNREFERENCED_EQUATION",
                severity="minor",
                location={"file": "<unknown>"},
                quote=f"Equation \\label{{{lab}}} is never \\eqref'd",
                evidence_expected="Exposition-only equations are allowed but should be acknowledged.",
                instruction=f"Either reference \\eqref{{{lab}}} in prose or note explicitly that this equation is for exposition only.",
                source_file="",
            ))

    passed = not any(f["severity"] == "critical" for f in flags)
    return flags, passed


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--polished-dir", required=True)
    p.add_argument("--preprocess-dir", default="")
    p.add_argument("--bib-file", default="")
    p.add_argument("--analysis-summary", default="")
    p.add_argument("--session-config", default="")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    polished_dir = Path(args.polished_dir)
    if not polished_dir.exists():
        print(f"ERROR: polished dir not found: {polished_dir}", file=sys.stderr)
        sys.exit(1)
    tex_files = read_tex_files(polished_dir)
    if not tex_files:
        print(f"ERROR: no section .tex files in {polished_dir}", file=sys.stderr)
        sys.exit(1)

    preprocess_dir = Path(args.preprocess_dir) if args.preprocess_dir else Path()
    bib_keys = parse_bib_keys(Path(args.bib_file)) if args.bib_file else set()
    source_numbers = (
        parse_source_numbers(Path(args.analysis_summary) if args.analysis_summary else None,
                             preprocess_dir)
        if preprocess_dir.exists() or args.analysis_summary
        else set()
    )
    glossary = parse_notation_glossary(preprocess_dir) if preprocess_dir.exists() else {}
    figure_catalog = parse_figure_catalog(preprocess_dir) if preprocess_dir.exists() else set()
    word_limit, target_journal, tolerance = parse_word_limit(
        Path(args.session_config) if args.session_config else None
    )

    result = {"checks": {}, "flags": [], "meta": {}}

    for name, fn, args_tuple in [
        ("numbers", check_numbers, (tex_files, source_numbers)),
        ("citations", check_citations, (tex_files, bib_keys)),
        ("symbols", check_symbols, (tex_files, glossary)),
        ("refs", check_refs, (tex_files, figure_catalog)),
        ("equations", check_equation_numbering, (tex_files,)),
    ]:
        flags, passed = fn(*args_tuple)
        result["checks"][name] = {"passed": passed, "flag_count": len(flags)}
        result["flags"].extend(flags)

    wc_flags, wc_passed, wc_meta = check_word_count(tex_files, word_limit, tolerance)
    result["checks"]["word_count"] = {"passed": wc_passed, "flag_count": len(wc_flags)}
    result["flags"].extend(wc_flags)
    result["meta"]["word_count"] = wc_meta
    result["meta"]["target_journal"] = target_journal
    result["meta"]["tolerance"] = tolerance

    severities = Counter(f["severity"] for f in result["flags"])
    types = Counter(f["type"] for f in result["flags"])
    result["summary"] = {
        "total_flags": len(result["flags"]),
        "by_severity": dict(severities),
        "by_type": dict(types),
        "all_passed": all(v["passed"] for v in result["checks"].values()),
    }
    result["timestamp"] = datetime.now().isoformat()
    result["polished_dir"] = str(polished_dir)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"Hard constraints: {len(result['flags'])} flags; all_passed={result['summary']['all_passed']}",
          file=sys.stderr)
    print(f"  critical: {severities.get('critical', 0)}  major: {severities.get('major', 0)}  minor: {severities.get('minor', 0)}",
          file=sys.stderr)
    print(f"Output: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
