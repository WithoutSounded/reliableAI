#!/usr/bin/env python3
"""
Bootstrap step2_global_config.json from step1_blueprint.md + step1_preprocess/.

Reads:
  <session>/step0_session_config.json         -- target journal, section structure
  <session>/step1_blueprint.md                -- section profiles, subsection outline
  <session>/step1_preprocess/notation_glossary.md  -- math symbols

Writes:
  <session>/step2_global_config.json          -- scaffold for Phase 2a completion

The output is a scaffold. The user/agent is expected to:
  - Add domain terms to the glossary
  - Review tense_lock.prohibited lists
  - Set the granularity paragraph
  - Adjust citation_format if the target journal requires it
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


def parse_notation_glossary(md_path: Path) -> list[dict]:
    """
    Extract math symbols from notation_glossary.md.

    Expected format is a Markdown table:
        | Symbol | Meaning | First appears in | Dimensions |
        |--------|---------|------------------|------------|
        | \\sigma_g | Gating noise scale | Methods \S3.2 | scalar |

    Returns a list of glossary entries keyed by symbol.
    """
    if not md_path.exists():
        return []

    text = md_path.read_text(encoding="utf-8")
    entries = []
    in_table = False
    header_cols = None

    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            in_table = False
            header_cols = None
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if header_cols is None:
            lower = [c.lower() for c in cells]
            if "symbol" in lower and "meaning" in lower:
                header_cols = lower
                in_table = True
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue  # separator row
        if not in_table or len(cells) != len(header_cols):
            continue
        row = dict(zip(header_cols, cells))
        symbol = row.get("symbol", "").strip()
        if not symbol or symbol.startswith("-"):
            continue
        entry = {
            "term": symbol,
            "definition": row.get("meaning", ""),
            "first_appears_in": row.get("first appears in") or row.get("first_appears_in") or "Methods",
            "type": "math_symbol",
        }
        if "dimensions" in row and row["dimensions"]:
            entry["dimensions"] = row["dimensions"]
        entries.append(entry)
    return entries


def parse_blueprint_section_profiles(md_path: Path) -> dict:
    """
    Extract the section_profiles JSON block from step1_blueprint.md.

    Looks for a fenced ```json block after a heading matching /section profiles?/i.
    Returns {} if not found; the caller fills in defaults.
    """
    if not md_path.exists():
        return {}
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    # Find a heading mentioning "section profile"
    anchor = None
    for i, line in enumerate(lines):
        if re.match(r"^#+\s+.*section profiles?.*", line.strip(), re.IGNORECASE):
            anchor = i
            break
    if anchor is None:
        return {}
    # Find the next ```json block
    for i in range(anchor + 1, len(lines)):
        if lines[i].strip().startswith("```json"):
            buf = []
            for j in range(i + 1, len(lines)):
                if lines[j].strip().startswith("```"):
                    try:
                        return json.loads("\n".join(buf))
                    except json.JSONDecodeError:
                        return {}
                buf.append(lines[j])
            break
    return {}


def default_section_profile(section: str, word_limit: int, n_sections: int) -> dict:
    """Fallback profile if the blueprint does not supply one."""
    section_lower = section.lower().replace(" ", "_")
    defaults = {
        "introduction": {
            "tone": "authoritative, engaging",
            "tense": "present (general), past (citing)",
            "citation_density": "high",
            "hedging_level": "moderate",
            "interpretation_allowed": True,
            "figure_references": False,
            "narrative_pattern": "broad-to-narrow funnel",
        },
        "related_work": {
            "tone": "comparative, structured",
            "tense": "present perfect / past",
            "citation_density": "very high",
            "hedging_level": "low",
            "interpretation_allowed": False,
            "figure_references": False,
            "narrative_pattern": "thematic grouping, ending with positioning",
        },
        "methods": {
            "tone": "precise, neutral, reproducible",
            "tense": "past (actions), present (system description)",
            "citation_density": "low-moderate",
            "hedging_level": "none",
            "interpretation_allowed": False,
            "figure_references": "architecture diagram only",
            "narrative_pattern": "sequential procedure",
        },
        "results": {
            "tone": "objective, data-driven",
            "tense": "past (experiments), present (what figures show)",
            "citation_density": "none",
            "hedging_level": "minimal",
            "interpretation_allowed": False,
            "figure_references": "every figure/table must be referenced",
            "narrative_pattern": "figure-driven",
        },
        "discussion": {
            "tone": "interpretive, balanced, cautious",
            "tense": "present (implications), past (comparing literature)",
            "citation_density": "high",
            "hedging_level": "high",
            "interpretation_allowed": True,
            "figure_references": "refer back to results figures",
            "narrative_pattern": "claim → evidence → comparison → implication",
        },
        "conclusion": {
            "tone": "concise, forward-looking",
            "tense": "past (summary), present/future (implications)",
            "citation_density": "none",
            "hedging_level": "moderate",
            "interpretation_allowed": True,
            "figure_references": False,
            "narrative_pattern": "contribution → limitation → future work",
        },
    }
    profile = defaults.get(section_lower, {
        "tone": "neutral",
        "tense": "mixed",
        "citation_density": "moderate",
        "hedging_level": "moderate",
        "interpretation_allowed": False,
        "figure_references": False,
        "narrative_pattern": "unspecified",
    })
    # Proportional word budget across non-abstract sections
    weights = {
        "introduction": 0.12,
        "related_work": 0.13,
        "methods": 0.28,
        "results": 0.22,
        "discussion": 0.18,
        "conclusion": 0.07,
    }
    weight = weights.get(section_lower, 1.0 / max(n_sections, 1))
    profile["word_budget"] = int(word_limit * weight)
    return profile


def build_tense_lock(profiles: dict) -> dict:
    """Derive tense_lock from section profiles."""
    prohibitions = {
        "introduction": ["future tense except in contribution preview"],
        "methods": [
            "hedging verbs (may/could/might)",
            "interpretive verbs (suggests/demonstrates)",
            "comparative claims about competing methods",
        ],
        "results": [
            "causal verbs (because/due to/caused by)",
            "interpretive verbs (suggests/indicates) — those belong in Discussion",
            "external citations for performance comparison",
        ],
        "related_work": ["references to the present paper's results"],
        "discussion": [
            "unhedged strong claims without statistical support",
            "introduction of data not already in Results",
        ],
        "conclusion": [
            "new information not stated earlier",
            "\\cite{} commands",
            "\\ref{fig:*} or \\ref{tab:*}",
        ],
    }
    tense_lock = {}
    for section_name, profile in profiles.items():
        key = section_name.lower().replace(" ", "_")
        tense_lock[key] = {
            "primary": profile.get("tense", "mixed"),
            "exceptions": [],
            "prohibited": prohibitions.get(key, []),
        }
    return tense_lock


def build_config(session_path: Path) -> dict:
    session_config_path = session_path / "step0_session_config.json"
    blueprint_path = session_path / "step1_blueprint.md"
    notation_path = session_path / "step1_preprocess" / "notation_glossary.md"

    if not session_config_path.exists():
        raise FileNotFoundError(f"Missing {session_config_path}")
    session_config = json.loads(session_config_path.read_text(encoding="utf-8"))

    target_journal = session_config.get("target_journal", "unspecified")
    word_limit = int(session_config.get("word_limit", 8000))
    section_structure = [
        s for s in session_config.get("section_structure", [])
        if s.lower() != "abstract"
    ]  # Abstract is drafted in Step 5

    profiles = parse_blueprint_section_profiles(blueprint_path)
    if not profiles:
        profiles = {
            s: default_section_profile(s, word_limit, len(section_structure))
            for s in section_structure
        }
    else:
        # Ensure every section has a profile; fill missing ones with defaults
        for s in section_structure:
            key = s.lower().replace(" ", "_")
            if key not in profiles and s not in profiles:
                profiles[key] = default_section_profile(s, word_limit, len(section_structure))

    # Normalize profile keys to lowercase_with_underscores
    profiles = {
        k.lower().replace(" ", "_"): v for k, v in profiles.items()
    }

    glossary = parse_notation_glossary(notation_path)

    tense_lock = build_tense_lock(profiles)

    config = {
        "draft_version": "v1",
        "created_at": datetime.utcnow().isoformat() + "Z",
        "target_journal": target_journal,
        "granularity": (
            "TODO: fill in one-paragraph description of target reader, derived from "
            "step8_journal_recommendations.md and the target journal's typical audience."
        ),
        "citation_format": "\\cite{Key}",
        "glossary": glossary,
        "tense_lock": tense_lock,
        "section_profiles": profiles,
        "brick_layer_ref": ".claude/skills/journal-draft/references/brick_layer_rules.md",
        "terminology_conventions": {
            "first_mention_expansion": True,
            "prefer_full_name_on_first_use": ["EEG", "ADHD", "BCI", "ERP"],
            "discouraged_abbreviations": ["SOTA", "e.g.", "etc."],
            "use_american_english": True,
            "oxford_comma": True,
            "equation_referencing": "\\eqref{eq:X}",
            "figure_referencing": "Fig.~\\ref{fig:X}",
            "table_referencing": "Table~\\ref{tab:X}",
            "section_referencing": "Section~\\ref{sec:X}",
        },
        "_todos": [
            "Fill in `granularity` with target-reader description",
            "Add domain terms (not just math symbols) to `glossary`",
            "Review `tense_lock.*.prohibited` lists for section-specific tightening",
            "Confirm `citation_format` matches target journal (natbib? numeric?)",
        ],
    }
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-path", required=True, type=Path,
                        help="Path to the Journal session folder")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output path (default: <session>/step2_global_config.json)")
    args = parser.parse_args()

    session_path = args.session_path.resolve()
    if not session_path.is_dir():
        print(f"ERROR: {session_path} is not a directory", file=sys.stderr)
        return 1

    output = args.output or (session_path / "step2_global_config.json")

    try:
        config = build_config(session_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    output.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {output}")
    print(f"  glossary: {len(config['glossary'])} entries (math symbols from notation_glossary.md)")
    print(f"  section_profiles: {len(config['section_profiles'])} sections")
    print(f"  todos: {len(config['_todos'])} items to review")
    return 0


if __name__ == "__main__":
    sys.exit(main())
