#!/usr/bin/env python3
"""
validate_blueprint.py — Phase 1c self-check for journal-blueprint.

Runs structural checks on a journal session's step1_preprocess/ and
step1_blueprint.md before Checkpoint 1. Prints a pass/fail report and
exits 0 if all critical checks pass, 1 otherwise (warnings do not fail).

Usage:
    python validate_blueprint.py --session-path <path_to_journal_session>
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Ensure emoji / CJK survive Windows consoles (cp1252 default).
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
except Exception:
    pass


REQUIRED_PREPROCESS_FILES = [
    "figure_captions.md",
    "table_captions.md",
    "pseudocode.md",
    "notation_glossary.md",
    "equation_plan.md",
]

REQUIRED_BLUEPRINT_HEADINGS = [
    "Narrative Objective",
    "Core Argument",
    "Section Profiles",
    "Evidence Mapping",
    "Subsection Outline",
    "Writing Order",
    "Cross-Agent Validation Plan",
]

DEFAULT_SECTIONS = [
    "introduction",
    "related_work",
    "methods",
    "results",
    "discussion",
    "conclusion",
    "abstract",
]


class CheckResult:
    def __init__(self, name: str, passed: bool, detail: str = "", severity: str = "critical"):
        self.name = name
        self.passed = passed
        self.detail = detail
        self.severity = severity  # "critical" or "warning"

    def __str__(self) -> str:
        icon = "[PASS]" if self.passed else ("[FAIL]" if self.severity == "critical" else "[WARN]")
        line = f"{icon} {self.name}"
        if self.detail:
            line += f"\n       {self.detail}"
        return line


def check_preprocess_files(session: Path) -> list[CheckResult]:
    results = []
    preprocess_dir = session / "step1_preprocess"
    if not preprocess_dir.is_dir():
        results.append(CheckResult(
            "step1_preprocess/ directory exists", False,
            f"Not found at {preprocess_dir}"
        ))
        return results

    for fname in REQUIRED_PREPROCESS_FILES:
        fpath = preprocess_dir / fname
        if not fpath.is_file():
            results.append(CheckResult(
                f"step1_preprocess/{fname} exists", False,
                f"File missing: {fpath}"
            ))
            continue
        text = fpath.read_text(encoding="utf-8", errors="replace")
        # Non-empty. Table required for the four tabular files; pseudocode
        # may legitimately be code blocks or numbered algorithm listings,
        # so it only needs substantive content.
        needs_table = fname != "pseudocode.md"
        has_table = bool(re.search(r"^\s*\|.*\|.*\|", text, flags=re.MULTILINE))
        if needs_table:
            if len(text.strip()) < 50 or not has_table:
                results.append(CheckResult(
                    f"step1_preprocess/{fname} has content + table", False,
                    "File exists but is empty or has no table rows"
                ))
            else:
                results.append(CheckResult(
                    f"step1_preprocess/{fname} has content + table", True
                ))
        else:
            # pseudocode.md — just require substantive content
            if len(text.strip()) < 100:
                results.append(CheckResult(
                    f"step1_preprocess/{fname} has substantive content", False,
                    "File is too short (< 100 chars)"
                ))
            else:
                results.append(CheckResult(
                    f"step1_preprocess/{fname} has substantive content", True
                ))
    return results


def check_blueprint_structure(session: Path) -> tuple[list[CheckResult], str | None]:
    bp_path = session / "step1_blueprint.md"
    if not bp_path.is_file():
        return [CheckResult("step1_blueprint.md exists", False, str(bp_path))], None

    text = bp_path.read_text(encoding="utf-8", errors="replace")
    results = [CheckResult("step1_blueprint.md exists", True)]

    for heading in REQUIRED_BLUEPRINT_HEADINGS:
        # Match "## <n>. <heading>" or "## <heading>" — case-insensitive
        pattern = rf"^#{{1,3}}\s*(\d+\.\s*)?{re.escape(heading)}"
        if re.search(pattern, text, flags=re.MULTILINE | re.IGNORECASE):
            results.append(CheckResult(f"heading: {heading}", True))
        else:
            results.append(CheckResult(
                f"heading: {heading}", False,
                f"Required heading '{heading}' not found"
            ))
    return results, text


def check_core_argument(blueprint_text: str) -> list[CheckResult]:
    # Locate the Core Argument block and verify it has non-placeholder content
    m = re.search(
        r"#{1,3}\s*(?:\d+\.\s*)?Core Argument.*?\n(.*?)(?=\n## |\Z)",
        blueprint_text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    if not m:
        return [CheckResult("Core Argument block non-empty", False, "Block not locatable")]
    body = m.group(1).strip()
    # Heuristic: must contain at least 30 non-whitespace chars and not be solely template placeholder
    has_real_content = (
        len(body) > 30
        and not re.fullmatch(r"[\s\-_:*#|\[\]]+", body)
        and "{placeholder" not in body.lower()
        and "TODO" not in body
        and "TBD" not in body
    )
    if has_real_content:
        return [CheckResult("Core Argument block non-empty", True)]
    return [CheckResult(
        "Core Argument block non-empty", False,
        "Block is empty, placeholder, or contains TODO/TBD"
    )]


def check_section_profiles(session: Path, blueprint_text: str) -> list[CheckResult]:
    config_path = session / "step0_session_config.json"
    sections = DEFAULT_SECTIONS
    word_limit = None
    if config_path.is_file():
        try:
            cfg = json.loads(config_path.read_text(encoding="utf-8"))
            if isinstance(cfg.get("section_structure"), list):
                sections = [
                    s.lower().replace(" ", "_")
                    for s in cfg["section_structure"]
                ]
            word_limit = cfg.get("word_limit")
        except Exception:
            pass

    results = []
    # Extract the Section Profiles block
    m = re.search(
        r"#{1,3}\s*(?:\d+\.\s*)?Section Profiles.*?\n(.*?)(?=\n## |\Z)",
        blueprint_text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    profiles_block = m.group(1) if m else ""

    for sec in sections:
        if re.search(rf'"{re.escape(sec)}"\s*:', profiles_block):
            results.append(CheckResult(f"profile: {sec}", True))
        else:
            results.append(CheckResult(
                f"profile: {sec}", False,
                f"No JSON key '\"{sec}\":' found in Section Profiles block"
            ))

    # Word-budget total check
    budget_matches = re.findall(r'"word_budget"\s*:\s*(\d+)', profiles_block)
    if budget_matches and word_limit:
        total = sum(int(b) for b in budget_matches)
        lower, upper = word_limit * 0.70, word_limit * 1.05
        if lower <= total <= upper:
            results.append(CheckResult(
                f"total word_budget ({total}) within ~[70%, 105%] of journal limit ({word_limit})",
                True,
            ))
        else:
            results.append(CheckResult(
                f"total word_budget ({total}) within ~[70%, 105%] of journal limit ({word_limit})",
                False,
                f"Out of band. Total={total}, lower={int(lower)}, upper={int(upper)}",
                severity="warning",
            ))
    return results


def check_evidence_mapping_orphans(session: Path, blueprint_text: str) -> list[CheckResult]:
    results = []
    preprocess_dir = session / "step1_preprocess"

    def collect_ids(fname: str, pattern: str) -> set[str]:
        fpath = preprocess_dir / fname
        if not fpath.is_file():
            return set()
        content = fpath.read_text(encoding="utf-8", errors="replace")
        return set(re.findall(pattern, content, flags=re.IGNORECASE))

    figure_ids = collect_ids("figure_captions.md", r"\bFig\s*(\d+)\b")
    table_ids = collect_ids("table_captions.md", r"\bTable\s*(\d+)\b")

    # Extract Evidence Mapping section text
    m = re.search(
        r"#{1,3}\s*(?:\d+\.\s*)?Evidence Mapping.*?\n(.*?)(?=\n## |\Z)",
        blueprint_text,
        flags=re.DOTALL | re.IGNORECASE,
    )
    evidence_block = m.group(1) if m else ""

    mapped_figs = set(re.findall(r"\bFig\s*(\d+)\b", evidence_block, flags=re.IGNORECASE))
    mapped_tables = set(re.findall(r"\bTable\s*(\d+)\b", evidence_block, flags=re.IGNORECASE))

    if figure_ids:
        orphan_figs = figure_ids - mapped_figs
        if orphan_figs:
            results.append(CheckResult(
                "figures placed in Evidence Mapping (orphan check)", False,
                f"Figures in preprocess not placed in any section: {sorted(orphan_figs, key=lambda x: int(x))}"
            ))
        else:
            results.append(CheckResult(
                "figures placed in Evidence Mapping (orphan check)", True,
                f"All {len(figure_ids)} figures placed"
            ))

    if table_ids:
        orphan_tables = table_ids - mapped_tables
        if orphan_tables:
            results.append(CheckResult(
                "tables placed in Evidence Mapping (orphan check)", False,
                f"Tables in preprocess not placed: {sorted(orphan_tables, key=lambda x: int(x))}"
            ))
        else:
            results.append(CheckResult(
                "tables placed in Evidence Mapping (orphan check)", True,
                f"All {len(table_ids)} tables placed"
            ))
    return results


def check_citation_keys(session: Path, blueprint_text: str) -> list[CheckResult]:
    """Verify every citation key referenced in the blueprint exists in the
    Research Agent's step4_citation_keys.md. This catches the 'phantom
    citation' hallucination class at blueprint time, before drafting."""

    # Locate the research session via step0_session_config.json
    config_path = session / "step0_session_config.json"
    if not config_path.is_file():
        return [CheckResult(
            "citation keys exist in step4_citation_keys.md", False,
            "step0_session_config.json missing; cannot resolve research_session",
            severity="warning",
        )]
    try:
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [CheckResult(
            "citation keys exist in step4_citation_keys.md", False,
            f"Could not parse step0_session_config.json: {e}",
            severity="warning",
        )]

    research_rel = cfg.get("research_session")
    if not research_rel:
        return [CheckResult(
            "citation keys exist in step4_citation_keys.md", False,
            "No research_session in step0_session_config.json",
            severity="warning",
        )]

    research_path = (session / research_rel).resolve()
    keys_file = research_path / "step4_citation_keys.md"
    if not keys_file.is_file():
        return [CheckResult(
            "citation keys exist in step4_citation_keys.md", False,
            f"File not found: {keys_file}",
            severity="warning",
        )]

    # Extract known keys: match tokens that look like citation keys
    # (CamelCase / PascalCase with digits, e.g., PindiEtAl2022, ZotevEtAl2016).
    keys_text = keys_file.read_text(encoding="utf-8", errors="replace")
    key_pattern = re.compile(r"\b([A-Z][A-Za-z]+(?:Et[A-Z][A-Za-z]*)?\d{4}[a-z]?)\b")
    known_keys = set(key_pattern.findall(keys_text))

    if not known_keys:
        return [CheckResult(
            "citation keys exist in step4_citation_keys.md", False,
            "No citation keys detected in step4_citation_keys.md",
            severity="warning",
        )]

    # Extract keys referenced in the blueprint
    cited_keys = set(key_pattern.findall(blueprint_text))
    # Filter: ignore obviously non-citation CamelCase (e.g., YearMonth tokens in dates).
    # Heuristic: must have at least one lowercase letter after the leading capital.
    cited_keys = {k for k in cited_keys if re.search(r"[a-z]", k)}

    missing = cited_keys - known_keys
    results: list[CheckResult] = []
    if missing:
        results.append(CheckResult(
            "citation keys exist in step4_citation_keys.md", False,
            f"Keys referenced but NOT found in research citation pool: {sorted(missing)}",
        ))
    elif cited_keys:
        results.append(CheckResult(
            "citation keys exist in step4_citation_keys.md", True,
            f"All {len(cited_keys)} referenced keys verified",
        ))
    else:
        results.append(CheckResult(
            "citation keys exist in step4_citation_keys.md", True,
            "No explicit citation keys referenced in blueprint",
            severity="warning",
        ))

    # Abstinence guard: if the research pool is substantial, require the
    # blueprint to actually reference some of its keys. Otherwise the Introduction
    # and Discussion will have no planned evidence and Step 2 will improvise.
    if len(known_keys) >= 5:
        expected_min = 3
        if len(cited_keys) >= expected_min:
            results.append(CheckResult(
                f"blueprint references ≥ {expected_min} citation keys from the pool",
                True,
                f"{len(cited_keys)} of {len(known_keys)} pool keys referenced",
            ))
        else:
            results.append(CheckResult(
                f"blueprint references ≥ {expected_min} citation keys from the pool",
                False,
                f"Only {len(cited_keys)} keys referenced; Research pool has {len(known_keys)}. Introduction / Discussion evidence mapping likely under-specified.",
                severity="warning",
            ))
    return results


def check_appendix_a(blueprint_text: str) -> list[CheckResult]:
    """Warning-level check: when the skill's mismatch-handling guidance has
    been invoked, the blueprint should surface it via an Appendix A block.
    Absent Appendix A is fine if there really are no mismatches, but worth
    surfacing so the human knows whether the author checked or skipped."""
    pattern = r"^#{1,3}\s*Appendix\s*A\b"
    if re.search(pattern, blueprint_text, flags=re.MULTILINE | re.IGNORECASE):
        return [CheckResult("Appendix A (Known Gaps / Deferred Decisions) present", True)]
    return [CheckResult(
        "Appendix A (Known Gaps / Deferred Decisions) present", False,
        "No Appendix A heading found. If there really are no deferred decisions or upstream mismatches, this is OK; otherwise add one per SKILL.md 'Handling upstream artifact mismatches'.",
        severity="warning",
    )]


def check_bilingual_coverage(blueprint_text: str) -> list[CheckResult]:
    # Require that at least the Narrative Objective and Core Argument sections
    # contain CJK characters (heuristic for Chinese content)
    has_cjk = bool(re.search(r"[\u4e00-\u9fff]", blueprint_text))
    if not has_cjk:
        return [CheckResult(
            "bilingual: blueprint contains 繁體中文", False,
            "No CJK characters found anywhere in the blueprint"
        )]

    results = [CheckResult("bilingual: blueprint contains 繁體中文", True)]

    for heading in ["Narrative Objective", "Core Argument"]:
        m = re.search(
            rf"#{{1,3}}\s*(?:\d+\.\s*)?{re.escape(heading)}.*?\n(.*?)(?=\n## |\Z)",
            blueprint_text,
            flags=re.DOTALL | re.IGNORECASE,
        )
        block = m.group(1) if m else ""
        if re.search(r"[\u4e00-\u9fff]", block):
            results.append(CheckResult(f"bilingual: {heading} has 繁中", True))
        else:
            results.append(CheckResult(
                f"bilingual: {heading} has 繁中", False,
                "Chinese version missing or untranslated",
                severity="warning",
            ))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-path", required=True, type=Path,
                        help="Path to the journal session folder")
    args = parser.parse_args()

    session = args.session_path.resolve()
    if not session.is_dir():
        print(f"ERROR: session path not found: {session}", file=sys.stderr)
        return 2

    all_results: list[CheckResult] = []
    all_results.extend(check_preprocess_files(session))

    structure_results, bp_text = check_blueprint_structure(session)
    all_results.extend(structure_results)

    if bp_text is not None:
        all_results.extend(check_core_argument(bp_text))
        all_results.extend(check_section_profiles(session, bp_text))
        all_results.extend(check_evidence_mapping_orphans(session, bp_text))
        all_results.extend(check_citation_keys(session, bp_text))
        all_results.extend(check_appendix_a(bp_text))
        all_results.extend(check_bilingual_coverage(bp_text))

    # Report
    critical_fails = sum(1 for r in all_results if not r.passed and r.severity == "critical")
    warning_fails = sum(1 for r in all_results if not r.passed and r.severity == "warning")
    passes = sum(1 for r in all_results if r.passed)

    print(f"\n=== Blueprint Self-Check: {session.name} ===\n")
    for r in all_results:
        print(r)

    print(f"\nSummary: {passes} passed, {critical_fails} failed (critical), {warning_fails} warnings\n")

    if critical_fails:
        print("❌ Critical failures — fix before Checkpoint 1.")
        return 1
    if warning_fails:
        print("⚠️  Warnings — review manually; non-blocking.")
    else:
        print("✅ All checks passed — ready for Checkpoint 1.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
