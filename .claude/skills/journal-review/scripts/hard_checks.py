#!/usr/bin/env python3
"""
Automated Hard Checks for Journal Review (Phase 3a)

Performs five machine-verifiable checks on a LaTeX manuscript draft:
1. Citation completeness — \cite{} vs .bib entries
2. Figure/table references — \ref{} vs \label{}, orphan figures
3. Number consistency — text numbers vs analysis_summary / figure_captions
4. Symbol consistency — math symbols vs notation_glossary
5. Word count — per-section vs blueprint budget

Usage:
    python hard_checks.py \
        --draft-dir path/to/step2_draft_v1 \
        --bib-file path/to/references.bib \
        --preprocess-dir path/to/step1_preprocess \
        --blueprint path/to/step1_blueprint.md \
        --analysis-summary path/to/analysis_summary.md \
        --output path/to/hard_checks_output.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from collections import Counter
from datetime import datetime


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_tex_files(draft_dir: Path) -> dict[str, str]:
    """Read all .tex files from draft directory, keyed by filename."""
    result = {}
    for f in sorted(draft_dir.glob("*.tex")):
        result[f.name] = f.read_text(encoding="utf-8")
    return result


def extract_cite_keys(text: str) -> list[dict]:
    """Extract all \\cite{...} keys with approximate location info."""
    results = []
    lines = text.split("\n")
    for line_no, line in enumerate(lines, 1):
        for m in re.finditer(r"\\cite\{([^}]+)\}", line):
            keys = [k.strip() for k in m.group(1).split(",")]
            for key in keys:
                results.append({"key": key, "line": line_no, "context": line.strip()})
    return results


def parse_bib_keys(bib_path: Path) -> set[str]:
    """Extract all @type{key, entries from a .bib file."""
    if not bib_path.exists():
        return set()
    text = bib_path.read_text(encoding="utf-8")
    return set(re.findall(r"@\w+\{([^,]+),", text))


def extract_labels(text: str) -> list[dict]:
    """Extract all \\label{...} with location."""
    results = []
    lines = text.split("\n")
    for line_no, line in enumerate(lines, 1):
        for m in re.finditer(r"\\label\{([^}]+)\}", line):
            results.append({"label": m.group(1), "line": line_no})
    return results


def extract_refs(text: str) -> list[dict]:
    """Extract all \\ref{...} and \\autoref{...} with location."""
    results = []
    lines = text.split("\n")
    for line_no, line in enumerate(lines, 1):
        for m in re.finditer(r"\\(?:auto)?ref\{([^}]+)\}", line):
            results.append({"ref": m.group(1), "line": line_no, "context": line.strip()})
    return results


def extract_numbers_from_text(text: str) -> list[dict]:
    """Extract numeric values that look like metrics (accuracy, F1, p-value, etc.)."""
    results = []
    lines = text.split("\n")
    # Patterns for common scientific numbers
    patterns = [
        # Percentage: 85.3%, 0.853
        (r"(\d+\.\d+)\s*\\?%", "percentage"),
        # F1/accuracy/precision/recall with value
        (r"(?:F1|accuracy|precision|recall|AUC|AUROC)\s*(?:=|:|\s+of\s+)\s*(\d+\.?\d*)", "metric"),
        # p-value
        (r"p\s*[<=]\s*(\d+\.?\d*)", "p_value"),
        # N = number
        (r"[Nn]\s*=\s*(\d+)", "sample_size"),
        # Generic decimal that could be a metric (0.xx pattern)
        (r"(?<!\d)0\.\d{2,4}(?!\d)", "decimal_metric"),
    ]
    for line_no, line in enumerate(lines, 1):
        # Skip comments
        if line.strip().startswith("%"):
            continue
        for pattern, num_type in patterns:
            for m in re.finditer(pattern, line, re.IGNORECASE):
                results.append({
                    "value": m.group(0),
                    "type": num_type,
                    "line": line_no,
                    "context": line.strip(),
                })
    return results


def extract_math_symbols(text: str) -> list[dict]:
    """Extract math-mode symbols from LaTeX text."""
    results = []
    lines = text.split("\n")
    # Match inline math $...$ and display math \[...\] and equation environments
    math_pattern = re.compile(
        r"\$([^$]+)\$"
        r"|\\begin\{(?:equation|align|gather)\*?\}(.*?)\\end\{(?:equation|align|gather)\*?\}",
        re.DOTALL,
    )
    for line_no, line in enumerate(lines, 1):
        if line.strip().startswith("%"):
            continue
        for m in math_pattern.finditer(line):
            math_content = m.group(1) or m.group(2) or ""
            # Extract individual symbols (Greek letters, operators, etc.)
            symbols = re.findall(
                r"\\(?:alpha|beta|gamma|delta|epsilon|zeta|eta|theta|iota|kappa|lambda|mu|nu|xi|pi|rho|sigma|tau|upsilon|phi|chi|psi|omega|"
                r"Alpha|Beta|Gamma|Delta|Epsilon|Zeta|Eta|Theta|Iota|Kappa|Lambda|Mu|Nu|Xi|Pi|Rho|Sigma|Tau|Upsilon|Phi|Chi|Psi|Omega|"
                r"mathbf|mathcal|mathbb|hat|tilde|bar|vec)\{?[a-zA-Z]?\}?",
                math_content,
            )
            for sym in symbols:
                results.append({
                    "symbol": sym,
                    "line": line_no,
                    "context": line.strip(),
                    "math_context": math_content.strip(),
                })
    return results


def count_words_tex(text: str) -> int:
    """Count words in LaTeX text, stripping commands and math."""
    # Remove comments
    text = re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)
    # Remove math environments
    text = re.sub(r"\$[^$]+\$", " MATH ", text)
    text = re.sub(r"\\begin\{(?:equation|align|gather)\*?\}.*?\\end\{(?:equation|align|gather)\*?\}", " MATH ", text, flags=re.DOTALL)
    # Remove LaTeX commands but keep their text arguments
    text = re.sub(r"\\(?:cite|ref|autoref|label|eqref)\{[^}]*\}", "", text)
    text = re.sub(r"\\(?:textbf|textit|emph|underline|section|subsection|subsubsection)\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+(?:\{[^}]*\})?", "", text)
    # Remove braces, special chars
    text = re.sub(r"[{}\\~&]", " ", text)
    # Count remaining words
    words = text.split()
    return len(words)


def parse_word_budgets(blueprint_path: Path) -> dict[str, int]:
    """Extract per-section word budgets from blueprint markdown."""
    if not blueprint_path.exists():
        return {}
    text = blueprint_path.read_text(encoding="utf-8")
    budgets = {}
    # Look for word_budget patterns in various formats
    # Pattern 1: "word_budget": 800 (JSON-like)
    section_pattern = re.compile(
        r'"(introduction|methods|results|discussion|related_work|conclusion|abstract)".*?"word_budget"\s*:\s*(\d+)',
        re.DOTALL | re.IGNORECASE,
    )
    for m in section_pattern.finditer(text):
        budgets[m.group(1).lower()] = int(m.group(2))
    # Pattern 2: markdown table or list with section: N words
    budget_pattern = re.compile(
        r"(introduction|methods|results|discussion|related.?work|conclusion|abstract)\s*[:|]\s*~?(\d+)\s*(?:words?)?",
        re.IGNORECASE,
    )
    for m in budget_pattern.finditer(text):
        section = m.group(1).lower().replace(" ", "_").replace("-", "_")
        if section not in budgets:
            budgets[section] = int(m.group(2))
    return budgets


def parse_figure_catalog(preprocess_dir: Path) -> set[str]:
    """Extract figure identifiers from figure_captions.md."""
    cap_file = preprocess_dir / "figure_captions.md"
    if not cap_file.exists():
        return set()
    text = cap_file.read_text(encoding="utf-8")
    # Match "Fig N", "Figure N", "fig:something"
    figs = set()
    for m in re.finditer(r"(?:Fig(?:ure)?\.?\s*(\d+))|(?:fig:(\w+))", text, re.IGNORECASE):
        figs.add(m.group(1) or m.group(2))
    return figs


def parse_numbers_from_source(analysis_path: Path, preprocess_dir: Path) -> set[str]:
    """Extract ground-truth numbers from analysis_summary and figure_captions."""
    numbers = set()
    files_to_check = []
    if analysis_path and analysis_path.exists():
        files_to_check.append(analysis_path)
    for name in ["figure_captions.md", "table_captions.md"]:
        p = preprocess_dir / name
        if p.exists():
            files_to_check.append(p)
    for f in files_to_check:
        text = f.read_text(encoding="utf-8")
        # Extract all decimal numbers
        for m in re.finditer(r"\d+\.\d+", text):
            numbers.add(m.group(0))
        # Extract integers in metric context
        for m in re.finditer(r"(?:N|n)\s*=\s*(\d+)", text):
            numbers.add(m.group(1))
    return numbers


def parse_notation_glossary(preprocess_dir: Path) -> dict[str, str]:
    """Parse notation_glossary.md into symbol -> meaning mapping."""
    glossary_file = preprocess_dir / "notation_glossary.md"
    if not glossary_file.exists():
        return {}
    text = glossary_file.read_text(encoding="utf-8")
    glossary = {}
    # Parse markdown table rows: | symbol | meaning | ...
    for m in re.finditer(r"\|\s*`?\\?([^|`]+)`?\s*\|\s*([^|]+)\|", text):
        symbol = m.group(1).strip()
        meaning = m.group(2).strip()
        if symbol.lower() not in ("symbol", "---", ""):
            glossary[symbol] = meaning
    return glossary


# ---------------------------------------------------------------------------
# Section name mapping
# ---------------------------------------------------------------------------

SECTION_MAP = {
    "01_introduction.tex": "introduction",
    "02_related_work.tex": "related_work",
    "03_methods.tex": "methods",
    "04_results.tex": "results",
    "05_discussion.tex": "discussion",
    "06_conclusion.tex": "conclusion",
    "00_abstract.tex": "abstract",
}


# ---------------------------------------------------------------------------
# Check runners
# ---------------------------------------------------------------------------

def check_citations(tex_files: dict[str, str], bib_keys: set[str]) -> list[dict]:
    """Check 1: Citation completeness."""
    flags = []
    cited_keys = set()
    flag_id = 0

    for fname, content in tex_files.items():
        cites = extract_cite_keys(content)
        for cite in cites:
            cited_keys.add(cite["key"])
            if cite["key"] not in bib_keys:
                flag_id += 1
                flags.append({
                    "id": f"HC-CIT-{flag_id:03d}",
                    "type": "MISSING_CITATION",
                    "severity": "major",
                    "location": {
                        "file": fname,
                        "line": cite["line"],
                    },
                    "quote": cite["context"],
                    "evidence_expected": f"No entry for '{cite['key']}' in references.bib",
                    "instruction": f"Add bib entry for '{cite['key']}' or correct the citation key.",
                    "source_file": "references.bib",
                })

    # Check for orphan bib entries (in bib but never cited)
    orphans = bib_keys - cited_keys
    for key in sorted(orphans):
        flag_id += 1
        flags.append({
            "id": f"HC-CIT-{flag_id:03d}",
            "type": "ORPHAN_BIB_ENTRY",
            "severity": "minor",
            "location": {"file": "references.bib"},
            "quote": "",
            "evidence_expected": f"Bib entry '{key}' is never \\cite'd in the manuscript",
            "instruction": f"Either cite '{key}' or remove it from references.bib.",
            "source_file": "references.bib",
        })

    return flags


def check_figure_table_refs(
    tex_files: dict[str, str], figure_catalog: set[str]
) -> list[dict]:
    """Check 2: Figure/table reference integrity."""
    flags = []
    flag_id = 0

    all_labels = {}  # label -> file
    all_refs = []    # (ref, file, line, context)

    for fname, content in tex_files.items():
        for lab in extract_labels(content):
            all_labels[lab["label"]] = fname
        for ref in extract_refs(content):
            all_refs.append((ref["ref"], fname, ref["line"], ref["context"]))

    # Check: every \ref has a \label
    for ref, fname, line, context in all_refs:
        if ref not in all_labels:
            flag_id += 1
            flags.append({
                "id": f"HC-REF-{flag_id:03d}",
                "type": "BROKEN_REF",
                "severity": "major",
                "location": {"file": fname, "line": line},
                "quote": context,
                "evidence_expected": f"No \\label{{{ref}}} found in any .tex file",
                "instruction": f"Add \\label{{{ref}}} to the corresponding figure/table/equation, or fix the \\ref key.",
                "source_file": fname,
            })

    # Check: every figure in catalog is referenced
    referenced_figs = set()
    for ref, *_ in all_refs:
        if ref.startswith("fig:"):
            referenced_figs.add(ref.replace("fig:", ""))
        # Also catch numeric refs that match figure numbers
        m = re.match(r"fig:?(\d+)", ref)
        if m:
            referenced_figs.add(m.group(1))

    for fig_id in figure_catalog:
        if fig_id not in referenced_figs:
            # Also check if referenced by number in text
            found = False
            for fname, content in tex_files.items():
                if re.search(rf"\\ref\{{fig:{fig_id}\}}", content):
                    found = True
                    break
            if not found:
                flag_id += 1
                flags.append({
                    "id": f"HC-REF-{flag_id:03d}",
                    "type": "ORPHAN_FIGURE",
                    "severity": "major",
                    "location": {"file": "figure_catalog"},
                    "quote": "",
                    "evidence_expected": f"Figure {fig_id} from catalog is never referenced in the manuscript",
                    "instruction": f"Add a \\ref{{fig:{fig_id}}} reference where this figure is discussed, or remove it from the figure catalog if unused.",
                    "source_file": "figure_captions.md",
                })

    return flags


def check_numbers(
    tex_files: dict[str, str],
    source_numbers: set[str],
) -> list[dict]:
    """Check 3: Number consistency (text vs source data)."""
    flags = []
    flag_id = 0

    # Only check Results and Discussion sections for number accuracy
    sections_to_check = ["04_results.tex", "05_discussion.tex", "00_abstract.tex"]

    for fname in sections_to_check:
        if fname not in tex_files:
            continue
        content = tex_files[fname]
        text_numbers = extract_numbers_from_text(content)
        for num_info in text_numbers:
            # Extract the core numeric value
            value_match = re.search(r"(\d+\.?\d*)", num_info["value"])
            if not value_match:
                continue
            value = value_match.group(1)
            # Check if this number exists in source data
            if value not in source_numbers and num_info["type"] in ("metric", "percentage", "decimal_metric"):
                flag_id += 1
                flags.append({
                    "id": f"HC-NUM-{flag_id:03d}",
                    "type": "NUMBER_MISMATCH",
                    "severity": "critical",
                    "location": {"file": fname, "line": num_info["line"]},
                    "quote": num_info["context"],
                    "evidence_expected": f"Value '{value}' not found in analysis_summary or figure_captions. Verify this number against source data.",
                    "instruction": f"Cross-check '{value}' with the original data source. If incorrect, replace with the correct value.",
                    "source_file": "analysis_summary.md / figure_captions.md",
                })

    return flags


def check_symbols(
    tex_files: dict[str, str],
    notation_glossary: dict[str, str],
) -> list[dict]:
    """Check 4: Symbol consistency with notation glossary."""
    flags = []
    flag_id = 0

    if not notation_glossary:
        return flags

    # Collect all symbols and their contexts across sections
    symbol_usage: dict[str, list[dict]] = {}
    for fname, content in tex_files.items():
        symbols = extract_math_symbols(content)
        for sym_info in symbols:
            sym = sym_info["symbol"]
            if sym not in symbol_usage:
                symbol_usage[sym] = []
            symbol_usage[sym].append({
                "file": fname,
                "line": sym_info["line"],
                "context": sym_info["context"],
                "math_context": sym_info["math_context"],
            })

    # Check for symbols used with potentially different meanings across sections
    for sym, usages in symbol_usage.items():
        files_used = set(u["file"] for u in usages)
        if len(files_used) > 1:
            # Check if symbol is defined in glossary
            if sym not in notation_glossary:
                flag_id += 1
                flags.append({
                    "id": f"HC-SYM-{flag_id:03d}",
                    "type": "SYMBOL_CONFLICT",
                    "severity": "minor",
                    "location": {"file": list(files_used)[0]},
                    "quote": usages[0]["context"],
                    "evidence_expected": f"Symbol '{sym}' used across {', '.join(sorted(files_used))} but not defined in notation_glossary.md",
                    "instruction": f"Add '{sym}' to notation_glossary.md with its canonical meaning, or verify consistent usage.",
                    "source_file": "notation_glossary.md",
                })

    return flags


def check_word_count(
    tex_files: dict[str, str],
    word_budgets: dict[str, int],
) -> list[dict]:
    """Check 5: Per-section word count vs budget."""
    flags = []
    flag_id = 0

    for fname, content in tex_files.items():
        section_name = SECTION_MAP.get(fname)
        if section_name and section_name in word_budgets:
            actual = count_words_tex(content)
            budget = word_budgets[section_name]
            ratio = actual / budget if budget > 0 else 0

            if ratio > 1.15:  # >15% over budget
                severity = "major" if ratio > 1.3 else "minor"
                flag_id += 1
                flags.append({
                    "id": f"HC-WC-{flag_id:03d}",
                    "type": "OVER_BUDGET",
                    "severity": severity,
                    "location": {"file": fname},
                    "quote": f"Section '{section_name}': {actual} words (budget: {budget}, {ratio:.0%} of budget)",
                    "evidence_expected": f"Word budget from blueprint: {budget} words",
                    "instruction": f"Reduce '{section_name}' by ~{actual - budget} words. Consider cutting redundant paragraphs or tightening prose.",
                    "source_file": "step1_blueprint.md",
                })
            elif ratio < 0.7 and budget > 100:  # <70% of budget (ignore small sections)
                flag_id += 1
                flags.append({
                    "id": f"HC-WC-{flag_id:03d}",
                    "type": "UNDER_BUDGET",
                    "severity": "minor",
                    "location": {"file": fname},
                    "quote": f"Section '{section_name}': {actual} words (budget: {budget}, {ratio:.0%} of budget)",
                    "evidence_expected": f"Word budget from blueprint: {budget} words",
                    "instruction": f"Section '{section_name}' is significantly under budget. Consider whether important content is missing or the budget needs adjustment.",
                    "source_file": "step1_blueprint.md",
                })

    return flags


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Automated hard checks for journal review")
    parser.add_argument("--draft-dir", required=True, help="Path to step2_draft_vN/")
    parser.add_argument("--bib-file", default="", help="Path to references.bib")
    parser.add_argument("--preprocess-dir", default="", help="Path to step1_preprocess/")
    parser.add_argument("--blueprint", default="", help="Path to step1_blueprint.md")
    parser.add_argument("--analysis-summary", default="", help="Path to analysis_summary.md")
    parser.add_argument("--output", required=True, help="Output JSON path")
    args = parser.parse_args()

    draft_dir = Path(args.draft_dir)
    if not draft_dir.exists():
        print(f"ERROR: Draft directory not found: {draft_dir}", file=sys.stderr)
        sys.exit(1)

    # Read inputs
    tex_files = read_tex_files(draft_dir)
    if not tex_files:
        print(f"ERROR: No .tex files found in {draft_dir}", file=sys.stderr)
        sys.exit(1)

    bib_keys = parse_bib_keys(Path(args.bib_file)) if args.bib_file else set()
    preprocess_dir = Path(args.preprocess_dir) if args.preprocess_dir else Path(".")
    blueprint_path = Path(args.blueprint) if args.blueprint else Path("nonexistent")
    analysis_path = Path(args.analysis_summary) if args.analysis_summary else None

    # Parse supporting data
    figure_catalog = parse_figure_catalog(preprocess_dir) if preprocess_dir.exists() else set()
    source_numbers = parse_numbers_from_source(analysis_path, preprocess_dir) if preprocess_dir.exists() else set()
    notation_glossary = parse_notation_glossary(preprocess_dir) if preprocess_dir.exists() else {}
    word_budgets = parse_word_budgets(blueprint_path)

    # Run all checks
    all_flags = []

    print("Running citation checks...", file=sys.stderr)
    all_flags.extend(check_citations(tex_files, bib_keys))

    print("Running figure/table reference checks...", file=sys.stderr)
    all_flags.extend(check_figure_table_refs(tex_files, figure_catalog))

    print("Running number consistency checks...", file=sys.stderr)
    all_flags.extend(check_numbers(tex_files, source_numbers))

    print("Running symbol consistency checks...", file=sys.stderr)
    all_flags.extend(check_symbols(tex_files, notation_glossary))

    print("Running word count checks...", file=sys.stderr)
    all_flags.extend(check_word_count(tex_files, word_budgets))

    # Summary
    severity_counts = Counter(f["severity"] for f in all_flags)
    type_counts = Counter(f["type"] for f in all_flags)

    # Per-section word counts (always include for reference)
    word_counts = {}
    for fname, content in tex_files.items():
        section = SECTION_MAP.get(fname, fname)
        word_counts[section] = count_words_tex(content)

    output = {
        "check_type": "automated_hard_checks",
        "timestamp": datetime.now().isoformat(),
        "draft_dir": str(draft_dir),
        "summary": {
            "total_flags": len(all_flags),
            "by_severity": dict(severity_counts),
            "by_type": dict(type_counts),
        },
        "word_counts": word_counts,
        "word_budgets": word_budgets,
        "flags": all_flags,
    }

    # Write output
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nHard checks complete: {len(all_flags)} flags found", file=sys.stderr)
    print(f"  Critical: {severity_counts.get('critical', 0)}", file=sys.stderr)
    print(f"  Major: {severity_counts.get('major', 0)}", file=sys.stderr)
    print(f"  Minor: {severity_counts.get('minor', 0)}", file=sys.stderr)
    print(f"Output: {output_path}", file=sys.stderr)


if __name__ == "__main__":
    main()
