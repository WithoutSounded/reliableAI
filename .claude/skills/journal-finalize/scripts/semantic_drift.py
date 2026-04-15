#!/usr/bin/env python3
"""
Semantic Drift Check for Journal Finalize (Phase 6b)

Compares each polished section (step5_polished/) against the last revised
version (step4_draft_v{latest}/) and reports signals that polishing may have
altered meaning:

- number_delta    : numeric tokens present in one version but not the other
- citation_delta  : \\cite keys present in one version but not the other
- claim_delta     : paragraphs in polished with no close analogue in revised
                    (Jaccard < threshold on content-word set), and vice versa
- hedge_delta     : changes in count of hedge words / boosting words

The script reports deltas; the calling model decides whether each signal
represents true drift.

Skips 00_abstract — abstract has no pre-polish baseline.

Usage:
    python semantic_drift.py \\
        --polished-dir step5_polished \\
        --revised-dir step4_draft_v2 \\
        --output semantic_drift.json
"""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime


SECTIONS = [
    "01_introduction.tex",
    "02_related_work.tex",
    "03_methods.tex",
    "04_results.tex",
    "05_discussion.tex",
    "06_conclusion.tex",
]

HEDGE_WORDS = {
    "may", "might", "could", "suggests", "suggest", "indicates", "indicate",
    "appears", "appear", "seem", "seems", "possibly", "potentially",
    "likely", "tends", "tend", "one possible", "one possibility",
}

BOOST_WORDS = {
    "demonstrates", "demonstrate", "proves", "prove", "significantly",
    "strongly", "markedly", "clearly", "definitely", "certainly",
    "undoubtedly", "robustly", "conclusively", "establishes", "establish",
}

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been before
being below between both but by could did do does doing down during each few for from
further had has have having he her here hers herself him himself his how i if in into
is it its itself just me more most my myself no nor not now of off on once only or
other our ours ourselves out over own same she should so some such than that the their
theirs them themselves then there these they this those through to too under until up
very was we were what when where which while who whom why will with would you your
yours yourself yourselves our also however therefore thus hence whereas whether either
neither both each few many much several some any all most more less least
""".split())


def strip_comments(text: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)


def strip_latex(text: str) -> str:
    t = strip_comments(text)
    # Remove math
    t = re.sub(
        r"\\begin\{(equation|align|gather|eqnarray)\*?\}.*?\\end\{\1\*?\}",
        " EQMATH ",
        t,
        flags=re.DOTALL,
    )
    t = re.sub(r"\$[^$]+\$", " INMATH ", t)
    # Drop \cite{} \ref{} \label{} — will be extracted separately
    t = re.sub(r"\\(?:cite[tp]?\*?|ref|autoref|eqref|label)\{[^}]*\}", " ", t)
    # Section headers
    t = re.sub(r"\\(?:section|subsection|subsubsection)\*?\{([^}]*)\}", r"\n\n\1\n\n", t)
    # Keep text inside \textbf / \emph / \textit
    t = re.sub(r"\\(?:textbf|emph|textit|underline)\{([^}]*)\}", r"\1", t)
    # Drop remaining commands
    t = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", " ", t)
    # Drop stray braces / backslashes
    t = re.sub(r"[{}\\]", " ", t)
    return t


def split_paragraphs(text: str) -> list[str]:
    plain = strip_latex(text)
    paragraphs = re.split(r"\n\s*\n", plain)
    return [p.strip() for p in paragraphs if len(p.strip().split()) >= 5]


def content_words(text: str) -> set[str]:
    tokens = re.findall(r"[a-zA-Z]{3,}", text.lower())
    return {t for t in tokens if t not in STOPWORDS}


def extract_numbers(text: str) -> set[str]:
    t = strip_latex(text)
    return {m.group(1) for m in re.finditer(r"(?<![\d.])(\d+(?:\.\d+)?)(?![\d.])", t)}


def extract_cites(text: str) -> set[str]:
    text = strip_comments(text)
    keys = set()
    for m in re.finditer(r"\\cite[tp]?\*?\{([^}]+)\}", text):
        for k in m.group(1).split(","):
            k = k.strip()
            if k:
                keys.add(k)
    return keys


def count_word_class(text: str, vocab: set[str]) -> int:
    t = strip_latex(text).lower()
    count = 0
    for w in vocab:
        if " " in w:
            count += len(re.findall(rf"\b{re.escape(w)}\b", t))
        else:
            count += len(re.findall(rf"\b{re.escape(w)}\b", t))
    return count


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def align_paragraphs(
    polished_paras: list[str], revised_paras: list[str], threshold: float
) -> dict:
    """Greedy best-match alignment. Report unmatched paras on each side."""
    # Precompute content-word sets
    p_sets = [content_words(p) for p in polished_paras]
    r_sets = [content_words(p) for p in revised_paras]

    matched_r = set()
    unmatched_polished = []  # likely-added paragraphs
    alignments = []
    for pi, ps in enumerate(p_sets):
        best = (-1, 0.0)
        for ri, rs in enumerate(r_sets):
            if ri in matched_r:
                continue
            sim = jaccard(ps, rs)
            if sim > best[1]:
                best = (ri, sim)
        if best[0] >= 0 and best[1] >= threshold:
            matched_r.add(best[0])
            alignments.append({"polished_idx": pi, "revised_idx": best[0], "jaccard": round(best[1], 3)})
        else:
            unmatched_polished.append({
                "polished_idx": pi,
                "best_jaccard": round(best[1], 3) if best[0] >= 0 else None,
                "preview": polished_paras[pi][:200],
            })
    unmatched_revised = []  # likely-removed paragraphs
    for ri in range(len(r_sets)):
        if ri not in matched_r:
            unmatched_revised.append({"revised_idx": ri, "preview": revised_paras[ri][:200]})

    return {
        "alignments": alignments,
        "unmatched_polished": unmatched_polished,
        "unmatched_revised": unmatched_revised,
    }


def compare_section(polished: str, revised: str, threshold: float) -> dict:
    pol_nums = extract_numbers(polished)
    rev_nums = extract_numbers(revised)
    pol_cites = extract_cites(polished)
    rev_cites = extract_cites(revised)

    pol_paras = split_paragraphs(polished)
    rev_paras = split_paragraphs(revised)
    align = align_paragraphs(pol_paras, rev_paras, threshold)

    return {
        "number_delta": {
            "added_in_polished": sorted(pol_nums - rev_nums),
            "removed_in_polished": sorted(rev_nums - pol_nums),
        },
        "citation_delta": {
            "added_in_polished": sorted(pol_cites - rev_cites),
            "removed_in_polished": sorted(rev_cites - pol_cites),
        },
        "hedge_delta": {
            "boost_polished": count_word_class(polished, BOOST_WORDS),
            "boost_revised": count_word_class(revised, BOOST_WORDS),
            "hedge_polished": count_word_class(polished, HEDGE_WORDS),
            "hedge_revised": count_word_class(revised, HEDGE_WORDS),
        },
        "claim_delta": {
            "paragraphs_polished": len(pol_paras),
            "paragraphs_revised": len(rev_paras),
            "unmatched_polished": align["unmatched_polished"],
            "unmatched_revised": align["unmatched_revised"],
            "aligned_count": len(align["alignments"]),
        },
    }


def heuristic_verdict(section_name: str, delta: dict) -> tuple[bool, str]:
    """Apply simple rules to mark likely drift; the model decides the final call."""
    reasons = []
    num_added = delta["number_delta"]["added_in_polished"]
    num_removed = delta["number_delta"]["removed_in_polished"]
    # Filter out tiny integers (<2 digits) — often paragraph numbering or lists
    num_added_substantive = [n for n in num_added if len(n.replace(".", "")) >= 2]
    num_removed_substantive = [n for n in num_removed if len(n.replace(".", "")) >= 2]
    if num_added_substantive or num_removed_substantive:
        reasons.append(
            f"numbers changed (+{num_added_substantive}, -{num_removed_substantive})"
        )

    cite_added = delta["citation_delta"]["added_in_polished"]
    cite_removed = delta["citation_delta"]["removed_in_polished"]
    if cite_added or cite_removed:
        reasons.append(f"citations changed (+{cite_added}, -{cite_removed})")

    hd = delta["hedge_delta"]
    boost_delta = hd["boost_polished"] - hd["boost_revised"]
    hedge_change = hd["hedge_polished"] - hd["hedge_revised"]
    # Discussion gaining hedges is expected during polish, flag only swing or boost growth
    if "discussion" in section_name or "05" in section_name:
        if boost_delta >= 3:
            reasons.append(f"Discussion boosting-word count grew by {boost_delta} (possible overclaim)")
    else:
        if boost_delta >= 3:
            reasons.append(f"boosting-word count grew by {boost_delta}")
        if abs(hedge_change) >= 4:
            reasons.append(f"hedge-word count changed by {hedge_change}")

    claim = delta["claim_delta"]
    # A whole paragraph appearing or disappearing is a strong signal
    if len(claim["unmatched_polished"]) > 0:
        reasons.append(f"{len(claim['unmatched_polished'])} polished paragraph(s) have no close revised analogue")
    if len(claim["unmatched_revised"]) > 0:
        reasons.append(f"{len(claim['unmatched_revised'])} revised paragraph(s) absent from polished")

    drift = len(reasons) > 0
    return drift, "; ".join(reasons) if drift else "no significant delta"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--polished-dir", required=True)
    p.add_argument("--revised-dir", required=True)
    p.add_argument("--threshold", type=float, default=0.35,
                   help="Jaccard threshold for paragraph alignment (default 0.35)")
    p.add_argument("--output", required=True)
    args = p.parse_args()

    polished_dir = Path(args.polished_dir)
    revised_dir = Path(args.revised_dir)
    if not polished_dir.exists():
        print(f"ERROR: polished dir not found: {polished_dir}", file=sys.stderr)
        sys.exit(1)
    if not revised_dir.exists():
        print(f"ERROR: revised dir not found: {revised_dir}", file=sys.stderr)
        sys.exit(1)

    section_results = {}
    section_decisions = {}

    for fname in SECTIONS:
        pol_path = polished_dir / fname
        rev_path = revised_dir / fname
        if not pol_path.exists():
            section_results[fname] = {"skipped": True, "reason": f"{fname} missing in polished dir"}
            continue
        if not rev_path.exists():
            # No baseline — mark as no-drift-detectable but note
            section_results[fname] = {"skipped": True, "reason": f"{fname} missing in revised dir (no baseline)"}
            section_decisions[fname.replace(".tex", "")] = {
                "drift": False, "use": "polished",
                "reason": "no revised baseline to compare against — using polished",
            }
            continue
        polished = pol_path.read_text(encoding="utf-8")
        revised = rev_path.read_text(encoding="utf-8")
        delta = compare_section(polished, revised, args.threshold)
        drift, reason = heuristic_verdict(fname, delta)
        section_results[fname] = delta
        section_decisions[fname.replace(".tex", "")] = {
            "drift": drift,
            "use": "revised" if drift else "polished",
            "reason": reason,
        }

    # Abstract is polish-only
    if (polished_dir / "00_abstract.tex").exists():
        section_decisions["00_abstract"] = {
            "drift": False, "use": "polished",
            "reason": "abstract is written in Phase 5c — no revised baseline",
        }

    output = {
        "timestamp": datetime.now().isoformat(),
        "polished_dir": str(polished_dir),
        "revised_dir": str(revised_dir),
        "threshold": args.threshold,
        "section_results": section_results,
        "section_decisions": section_decisions,
        "summary": {
            "sections_polished": sum(1 for d in section_decisions.values() if d["use"] == "polished"),
            "sections_fallback": sum(1 for d in section_decisions.values() if d["use"] == "revised"),
        },
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        f"Semantic drift: polished={output['summary']['sections_polished']}  fallback={output['summary']['sections_fallback']}",
        file=sys.stderr,
    )
    for name, dec in section_decisions.items():
        marker = "✗" if dec["drift"] else "✓"
        print(f"  {marker} {name}: {dec['use']} — {dec['reason']}", file=sys.stderr)
    print(f"Output: {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
