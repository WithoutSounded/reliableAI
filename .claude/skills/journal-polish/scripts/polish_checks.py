#!/usr/bin/env python3
"""Deterministic checks for the journal-polish skill (Step 5).

Three modes, all producing a JSON report on stdout plus a short
human-readable summary on stderr:

  section-checks   Paragraph length + same-opener runs + in-section
                   terminology variants. Run on one polished section
                   during Phase 5a.

  terminology      Global terminology variants across all polished
                   sections. Run during Phase 5b.3.

  abstract         Abstract hard-rule compliance: word count, forbidden
                   constructs (\\cite, \\ref, "Section", "Fig.", "Table"
                   refs, "as described"), and that every number in the
                   abstract appears verbatim in Results. Run during
                   Phase 5c.

Exit code is 0 if no issues found, 1 otherwise (so the caller can gate
on success).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from typing import Iterable

# --------------------------------------------------------------------------
# LaTeX-aware utilities
# --------------------------------------------------------------------------

# Strip LaTeX commands / math / comments so downstream text analysis sees
# approximately "what the reader reads." Not a full LaTeX parser — the
# goal is good-enough text extraction for prose heuristics.

_COMMENT_RE = re.compile(r"(?<!\\)%.*")
_MATH_INLINE_RE = re.compile(r"\$[^$]*\$")
_MATH_DISPLAY_RE = re.compile(r"\\\[[\s\S]*?\\\]|\\begin\{equation\*?\}[\s\S]*?\\end\{equation\*?\}|\\begin\{align\*?\}[\s\S]*?\\end\{align\*?\}")
_FLOAT_ENV_RE = re.compile(r"\\begin\{(figure|table)\*?\}[\s\S]*?\\end\{\1\*?\}")
# Sectioning commands carry a title but are not prose: they must be
# removed *before* paragraph splitting, otherwise the title becomes a
# spurious 1-sentence paragraph.
_SECTION_CMD_RE = re.compile(r"\\(?:(?:sub){0,2}section|paragraph|subparagraph)\*?\{[^}]*\}")
_CITE_RE = re.compile(r"\\cite[a-zA-Z]*\{[^}]*\}")
_REF_RE = re.compile(r"\\(?:ref|eqref|autoref|pageref)\{[^}]*\}")
_LABEL_RE = re.compile(r"\\label\{[^}]*\}")
# Single-arg control sequences whose argument we want to keep as plain
# text (\\textbf{word} -> word). Multi-arg commands we just drop.
_TEXT_ARG_RE = re.compile(r"\\(?:textbf|textit|emph|texttt|textsc|underline)\{([^}]*)\}")
_CMD_NO_ARG_RE = re.compile(r"\\[a-zA-Z]+\*?")


def strip_latex(text: str) -> str:
    """Return an approximate plaintext rendering of LaTeX source."""
    t = _COMMENT_RE.sub("", text)
    t = _SECTION_CMD_RE.sub("", t)
    t = _FLOAT_ENV_RE.sub(" [FLOAT] ", t)
    t = _MATH_DISPLAY_RE.sub(" [MATH] ", t)
    t = _MATH_INLINE_RE.sub(" [MATH] ", t)
    t = _CITE_RE.sub(" [CITE] ", t)
    t = _REF_RE.sub(" [REF] ", t)
    t = _LABEL_RE.sub("", t)
    t = _TEXT_ARG_RE.sub(r"\1", t)
    t = _CMD_NO_ARG_RE.sub(" ", t)
    t = re.sub(r"[{}]", "", t)
    t = re.sub(r"[ \t]+", " ", t)
    return t


def split_paragraphs(plain: str) -> list[str]:
    """Split plaintext into paragraphs on blank-line boundaries. Drops
    paragraphs that are only placeholder tokens (pure float/math/caption)."""
    paragraphs = []
    for chunk in re.split(r"\n\s*\n", plain):
        chunk = chunk.strip()
        if not chunk:
            continue
        # Skip chunks that are essentially only placeholder tokens.
        residual = re.sub(r"\[(FLOAT|MATH|CITE|REF)\]", "", chunk).strip()
        if len(residual) < 20:
            continue
        paragraphs.append(chunk)
    return paragraphs


_SENTENCE_END_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'(])")


def split_sentences(paragraph: str) -> list[str]:
    # Collapse whitespace so placeholder tokens don't spawn spurious breaks.
    p = re.sub(r"\s+", " ", paragraph).strip()
    if not p:
        return []
    # Protect a few abbreviations that shouldn't terminate sentences.
    for abbr in ["Fig.", "Eq.", "e.g.", "i.e.", "et al.", "vs.", "cf.", "Eqs.", "Figs."]:
        p = p.replace(abbr, abbr.replace(".", "\u0001"))
    sentences = _SENTENCE_END_RE.split(p)
    return [s.replace("\u0001", ".").strip() for s in sentences if s.strip()]


def count_words(plain: str) -> int:
    """Word count on plaintext — alphanumeric tokens only."""
    return len(re.findall(r"[A-Za-z][A-Za-z0-9\-']*", plain))


# --------------------------------------------------------------------------
# Issue reporting
# --------------------------------------------------------------------------


@dataclass
class Issue:
    kind: str
    severity: str  # "minor" | "major"
    location: str
    detail: str
    suggestion: str = ""


@dataclass
class Report:
    mode: str
    target: str
    issues: list[Issue] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    def dump(self) -> dict:
        return {
            "mode": self.mode,
            "target": self.target,
            "issues": [asdict(i) for i in self.issues],
            "stats": self.stats,
            "pass": len(self.issues) == 0,
        }


# --------------------------------------------------------------------------
# Mode: section-checks (paragraph length + same-opener + local terminology)
# --------------------------------------------------------------------------


def load_glossary_terms(global_config_path: str) -> list[dict]:
    """Extract terminology info from step2_global_config.json. Tolerates a
    few shapes because the exact schema in the broader pipeline is still
    settling."""
    if not global_config_path or not os.path.exists(global_config_path):
        return []
    try:
        with open(global_config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
    except (json.JSONDecodeError, OSError):
        return []
    glossary = cfg.get("glossary") or cfg.get("Glossary") or {}
    terms: list[dict] = []
    if isinstance(glossary, dict):
        for canonical, meaning in glossary.items():
            entry = {"canonical": canonical, "variants": []}
            if isinstance(meaning, dict):
                entry["variants"] = meaning.get("variants", []) or []
            terms.append(entry)
    elif isinstance(glossary, list):
        for item in glossary:
            if isinstance(item, dict) and "canonical" in item:
                terms.append({
                    "canonical": item["canonical"],
                    "variants": item.get("variants", []) or [],
                })
    return terms


# Concepts that authors commonly alternate between without meaning to.
# These are flagged when two or more of the variants co-occur in the
# same section/paper AND the glossary does not authorize the variety.
_DEFAULT_SYNONYM_GROUPS: list[list[str]] = [
    ["method", "approach", "technique", "framework", "methodology"],
    ["model", "network", "architecture", "system"],
    ["dataset", "corpus", "data set"],
    ["participant", "subject", "user", "individual"],
    ["feature", "attribute", "variable", "predictor"],
    ["accuracy", "correctness", "performance"],
]


def flag_paragraph_length(paragraphs: list[str], section_label: str) -> list[Issue]:
    issues: list[Issue] = []
    for idx, para in enumerate(paragraphs, start=1):
        sents = split_sentences(para)
        n = len(sents)
        if n < 3:
            issues.append(Issue(
                kind="PARAGRAPH_TOO_SHORT",
                severity="minor",
                location=f"{section_label} ¶{idx}",
                detail=f"{n} sentence(s).",
                suggestion="Expand with supporting reasoning or merge with the adjacent paragraph. If deliberate emphasis, note in polish_notes.md.",
            ))
        elif n > 8:
            issues.append(Issue(
                kind="PARAGRAPH_TOO_LONG",
                severity="minor",
                location=f"{section_label} ¶{idx}",
                detail=f"{n} sentences.",
                suggestion="Split at the second topic sentence, or convert to an itemize list if genuinely a list.",
            ))
    return issues


def flag_same_opener_runs(paragraphs: list[str], section_label: str) -> list[Issue]:
    """Flag runs of 3+ consecutive sentences opening with the same word
    within a single paragraph — the 'We did X. We did Y.' trap."""
    issues: list[Issue] = []
    for idx, para in enumerate(paragraphs, start=1):
        sents = split_sentences(para)
        if len(sents) < 3:
            continue
        openers = []
        for s in sents:
            m = re.match(r"\s*([A-Za-z][A-Za-z\-']*)", s)
            openers.append(m.group(1).lower() if m else "")
        run_start = 0
        for i in range(1, len(openers) + 1):
            if i < len(openers) and openers[i] and openers[i] == openers[run_start]:
                continue
            run_len = i - run_start
            if run_len >= 3 and openers[run_start]:
                issues.append(Issue(
                    kind="MONOTONOUS_OPENERS",
                    severity="minor",
                    location=f"{section_label} ¶{idx} sentences {run_start + 1}-{i}",
                    detail=f"{run_len} consecutive sentences open with '{openers[run_start].capitalize()}'.",
                    suggestion="Vary sentence structure: use a participial opener, a subordinate clause, or passive voice on one of the sentences.",
                ))
            run_start = i
    return issues


def flag_terminology_variants(
    plain_text: str,
    section_label: str,
    glossary_terms: list[dict],
) -> list[Issue]:
    """Report synonym groups whose members co-occur in the text when the
    glossary has not explicitly authorized the variety."""
    issues: list[Issue] = []
    lowered = plain_text.lower()
    authorized_variants: set[tuple[str, str]] = set()
    for term in glossary_terms:
        canonical = term.get("canonical", "").lower()
        for variant in term.get("variants", []) or []:
            authorized_variants.add((canonical, variant.lower()))

    for group in _DEFAULT_SYNONYM_GROUPS:
        present = []
        for word in group:
            pat = re.compile(r"\b" + re.escape(word) + r"s?\b", re.IGNORECASE)
            if pat.search(lowered):
                present.append(word)
        if len(present) >= 2:
            # Treat the first present word as the provisional canonical.
            canonical = present[0]
            alternates = present[1:]
            unauthorized = [
                alt for alt in alternates
                if (canonical, alt) not in authorized_variants
                and (alt, canonical) not in authorized_variants
            ]
            if unauthorized:
                issues.append(Issue(
                    kind="TERMINOLOGY_VARIANT",
                    severity="minor",
                    location=section_label,
                    detail=(
                        f"Concept group alternates between: "
                        f"'{canonical}' and {', '.join(repr(a) for a in unauthorized)}."
                    ),
                    suggestion=(
                        f"Pick one term for this concept (commonly '{canonical}') and unify. "
                        "If the alternation is intentional, add the variants to the glossary "
                        "in step2_global_config.json under the canonical term."
                    ),
                ))
    return issues


def mode_section_checks(args: argparse.Namespace) -> Report:
    with open(args.section_file, "r", encoding="utf-8") as f:
        raw = f.read()
    plain = strip_latex(raw)
    paragraphs = split_paragraphs(plain)
    label = os.path.basename(args.section_file)
    glossary_terms = load_glossary_terms(args.glossary) if args.glossary else []
    report = Report(mode="section-checks", target=args.section_file)
    report.issues.extend(flag_paragraph_length(paragraphs, label))
    report.issues.extend(flag_same_opener_runs(paragraphs, label))
    report.issues.extend(flag_terminology_variants(plain, label, glossary_terms))
    report.stats = {
        "paragraph_count": len(paragraphs),
        "word_count": count_words(plain),
        "sentence_count": sum(len(split_sentences(p)) for p in paragraphs),
    }
    return report


# --------------------------------------------------------------------------
# Mode: terminology (global across polished directory)
# --------------------------------------------------------------------------


def mode_terminology(args: argparse.Namespace) -> Report:
    polished_dir = args.polished_dir
    report = Report(mode="terminology", target=polished_dir)
    glossary_terms = load_glossary_terms(args.glossary) if args.glossary else []
    authorized_variants: set[tuple[str, str]] = set()
    for term in glossary_terms:
        canonical = term.get("canonical", "").lower()
        for variant in term.get("variants", []) or []:
            authorized_variants.add((canonical, variant.lower()))

    # Aggregate counts across sections.
    group_locations: dict[str, dict[str, list[str]]] = {}
    for fname in sorted(os.listdir(polished_dir)):
        if not fname.endswith(".tex"):
            continue
        if fname.startswith("00_abstract"):
            # Abstract is short and has its own checks.
            continue
        with open(os.path.join(polished_dir, fname), "r", encoding="utf-8") as f:
            raw = f.read()
        plain = strip_latex(raw).lower()
        for group in _DEFAULT_SYNONYM_GROUPS:
            gkey = group[0]
            for word in group:
                pat = re.compile(r"\b" + re.escape(word) + r"s?\b", re.IGNORECASE)
                if pat.search(plain):
                    group_locations.setdefault(gkey, {}).setdefault(word, []).append(fname)

    for gkey, words in group_locations.items():
        if len(words) < 2:
            continue
        canonical = gkey
        alternates = [w for w in words if w != canonical]
        unauthorized = [
            alt for alt in alternates
            if (canonical, alt) not in authorized_variants
            and (alt, canonical) not in authorized_variants
        ]
        if unauthorized:
            per_word = {w: sorted(set(files)) for w, files in words.items()}
            report.issues.append(Issue(
                kind="GLOBAL_TERMINOLOGY_VARIANT",
                severity="minor",
                location="all sections",
                detail=(
                    f"Concept group '{canonical}' alternates across sections: "
                    + ", ".join(f"{w} in {files}" for w, files in per_word.items())
                ),
                suggestion=(
                    f"Unify on one term (commonly '{canonical}'). If variety is intentional, "
                    "add variants to the glossary in step2_global_config.json."
                ),
            ))
    report.stats = {"sections_scanned": sum(1 for f in os.listdir(polished_dir) if f.endswith(".tex") and not f.startswith("00_abstract"))}
    return report


# --------------------------------------------------------------------------
# Mode: abstract (hard-rule compliance)
# --------------------------------------------------------------------------


# Pattern that matches numeric literals the way they appear in Results
# prose: integers, decimals, percentages, p-values, scientific notation,
# ranges. The match includes an optional unit glued to the number
# (e.g. "84.2%", "p<0.001") to support exact-string lookup in Results.
_NUMBER_TOKEN_RE = re.compile(
    r"(?:[<>]=?\s*)?"                  # optional comparator prefix (p < 0.001)
    r"\d+(?:\.\d+)?"                   # integer or decimal
    r"(?:\s*[\u2013\u2014\-]\s*\d+(?:\.\d+)?)?"  # optional range
    r"(?:\s*%|\s*ms|\s*Hz|\s*s\b|\s*min)?"       # optional unit
)

_FORBIDDEN_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("CITE", re.compile(r"\\cite[a-zA-Z]*\{[^}]*\}")),
    ("REF", re.compile(r"\\(?:ref|eqref|autoref|pageref)\{[^}]*\}")),
    ("SECTION_REF", re.compile(r"\b(?:Section|Sect\.|§)\s*\d+", re.IGNORECASE)),
    ("FIGURE_REF", re.compile(r"\b(?:Figure|Fig\.)\s*\d+", re.IGNORECASE)),
    ("TABLE_REF", re.compile(r"\bTable\s*\d+", re.IGNORECASE)),
    ("META_REF", re.compile(r"\bas (?:described|shown|noted|discussed) (?:below|above|in (?:the|our) (?:introduction|methods|results|discussion))\b", re.IGNORECASE)),
]


def normalize_number_token(tok: str) -> str:
    """Normalize a number token for cross-text lookup: strip whitespace,
    unify dashes."""
    t = tok.strip()
    t = re.sub(r"\s+", "", t)
    t = t.replace("\u2013", "-").replace("\u2014", "-")
    return t


def extract_numbers(plain: str) -> list[tuple[str, str]]:
    """Return list of (normalized_token, raw_token_with_context) from plaintext.

    Bare single-digit integers are kept: a claim like "converged within 3
    sessions" is a quantitative claim worth checking. Word-boundary
    matching in number_matches_in_results prevents false matches inside
    decimals or longer integers."""
    out: list[tuple[str, str]] = []
    for m in _NUMBER_TOKEN_RE.finditer(plain):
        raw = m.group(0).strip()
        out.append((normalize_number_token(raw), raw))
    return out


def number_matches_in_results(token: str, results_plain: str) -> bool:
    """Return True if the (normalized) token appears in the Results
    plaintext as a standalone number — not as a fragment of a decimal
    or a longer integer.

    Boundary rule: the matched span must not be adjacent (on either
    side) to a digit or a decimal point. This prevents '20' from
    matching '200' or '3' from matching the '3' inside '6.3'.
    """
    results_norm = re.sub(r"\s+", "", results_plain)
    token_norm = re.sub(r"\s+", "", token)
    boundary_before = r"(?<![\d.])"
    boundary_after = r"(?![\d.])"
    pattern = boundary_before + re.escape(token_norm) + boundary_after
    if re.search(pattern, results_norm):
        return True
    # Percent fallback: abstract '18%' should also match the LaTeX-escaped
    # '18\%' form sometimes present in Results. Keep the digit-boundary
    # rule on the numeric part.
    if token_norm.endswith("%"):
        bare = token_norm[:-1]
        if bare:
            pat2 = boundary_before + re.escape(bare) + r"(?:%|\\%)" + boundary_after
            if re.search(pat2, results_norm):
                return True
    return False


def mode_abstract(args: argparse.Namespace) -> Report:
    with open(args.abstract_file, "r", encoding="utf-8") as f:
        abs_raw = f.read()
    with open(args.results_file, "r", encoding="utf-8") as f:
        res_raw = f.read()
    abs_plain = strip_latex(abs_raw)
    res_plain = strip_latex(res_raw)

    report = Report(mode="abstract", target=args.abstract_file)

    # Forbidden constructs (check the raw source so \cite etc. are caught).
    for label, pat in _FORBIDDEN_PATTERNS:
        for m in pat.finditer(abs_raw):
            report.issues.append(Issue(
                kind=f"FORBIDDEN_{label}",
                severity="major",
                location="abstract",
                detail=f"Contains {label.lower().replace('_', ' ')}: '{m.group(0)}'.",
                suggestion="The abstract must be self-contained. Rewrite without citations, figure/table/section references, or meta-references.",
            ))

    # Word count.
    wc = count_words(abs_plain)
    limit = args.word_limit
    report.stats["word_count"] = wc
    report.stats["word_limit"] = limit
    if limit and wc > limit:
        report.issues.append(Issue(
            kind="OVER_WORD_LIMIT",
            severity="major",
            location="abstract",
            detail=f"Word count {wc} exceeds limit {limit}.",
            suggestion=f"Tighten by {wc - limit} words. The Background and Method segments are usually the easiest to compress.",
        ))
    if limit and wc < int(limit * 0.6):
        report.issues.append(Issue(
            kind="UNDER_WORD_LIMIT",
            severity="minor",
            location="abstract",
            detail=f"Word count {wc} is below 60% of the {limit}-word budget.",
            suggestion="A short abstract looks thin. Aim for 85-100% of the budget: strengthen Background, expand Method, or add a secondary result.",
        ))

    # Number rule: every abstract number must appear in Results.
    abs_numbers = extract_numbers(abs_plain)
    missing = []
    for token, raw in abs_numbers:
        if not number_matches_in_results(token, res_plain):
            missing.append(raw)
    report.stats["abstract_numbers"] = [r for _, r in abs_numbers]
    report.stats["missing_from_results"] = missing
    for raw in missing:
        report.issues.append(Issue(
            kind="ABSTRACT_NUMBER_NOT_IN_RESULTS",
            severity="major",
            location="abstract",
            detail=f"Number '{raw}' does not appear verbatim in 04_results.tex.",
            suggestion=(
                "Either match the Results exactly (same value, units, decimals), "
                "or, if the number genuinely belongs in the abstract but is missing "
                "from Results, escalate: Results is incomplete. Do not fix by "
                "silently adding the number to either section."
            ),
        ))

    return report


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def _summary_stderr(report: Report) -> None:
    total = len(report.issues)
    if total == 0:
        print(f"[polish_checks:{report.mode}] PASS  ({json.dumps(report.stats)})", file=sys.stderr)
        return
    by_kind: dict[str, int] = {}
    for i in report.issues:
        by_kind[i.kind] = by_kind.get(i.kind, 0) + 1
    parts = ", ".join(f"{k}={v}" for k, v in sorted(by_kind.items()))
    print(f"[polish_checks:{report.mode}] FAIL  {total} issue(s): {parts}", file=sys.stderr)
    for i in report.issues[:10]:
        print(f"  - [{i.severity}] {i.kind} @ {i.location}: {i.detail}", file=sys.stderr)
    if total > 10:
        print(f"  (+ {total - 10} more — see JSON)", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Polish checks for journal-polish (Step 5).")
    p.add_argument("--mode", required=True, choices=["section-checks", "terminology", "abstract"])

    # section-checks
    p.add_argument("--section-file", help="Path to a polished section .tex (mode=section-checks).")

    # terminology
    p.add_argument("--polished-dir", help="Path to step5_polished/ (mode=terminology).")

    # abstract
    p.add_argument("--abstract-file", help="Path to 00_abstract.tex (mode=abstract).")
    p.add_argument("--results-file", help="Path to 04_results.tex (mode=abstract).")
    p.add_argument("--word-limit", type=int, default=None, help="Abstract word limit (mode=abstract).")

    # shared
    p.add_argument("--glossary", help="Path to step2_global_config.json (optional).")
    p.add_argument("--output", help="Write JSON report to this path (also printed to stdout).")

    args = p.parse_args(argv)

    if args.mode == "section-checks":
        if not args.section_file:
            p.error("--section-file is required for mode=section-checks")
        report = mode_section_checks(args)
    elif args.mode == "terminology":
        if not args.polished_dir:
            p.error("--polished-dir is required for mode=terminology")
        report = mode_terminology(args)
    elif args.mode == "abstract":
        if not args.abstract_file or not args.results_file:
            p.error("--abstract-file and --results-file are required for mode=abstract")
        report = mode_abstract(args)
    else:  # pragma: no cover
        p.error(f"unknown mode: {args.mode}")

    payload = report.dump()
    serialized = json.dumps(payload, indent=2, ensure_ascii=False)
    print(serialized)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(serialized)
    _summary_stderr(report)
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
