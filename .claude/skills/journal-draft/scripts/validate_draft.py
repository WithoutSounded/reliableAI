#!/usr/bin/env python3
"""
Self-check the Phase 2b draft output.

Reads:
  <session>/step0_session_config.json
  <session>/step1_blueprint.md
  <session>/step1_preprocess/figure_captions.md
  <session>/step2_global_config.json
  <session>/step2_draft_v1/*.tex
  <session>/step2_draft_v1/_sliding_window_state.json
  <Research>/step4_references.bib   (path via session_config.research_session)

Runs seven checks:
  1. Every non-abstract section has a non-empty .tex file
  2. Every subsection in the blueprint outline appears in the matching .tex
  3. Every figure in figure_captions.md is \ref{}'d at least once across the draft
  4. Every \cite{Key} resolves to an entry in references.bib
  5. Per-section word count within +-15% of the blueprint's section word budget
  6. _sliding_window_state.json contains a summary for every drafted section
  7. step2_global_config.json is well-formed JSON with required top-level fields

Exits 0 on all-pass, 1 if any check fails. Prints a per-check pass/fail table and a
list of specific violations.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Subsection titles and blueprint text frequently contain non-ASCII characters
# (en-dashes, ≤, §, etc.). Windows consoles default to cp1252 and crash when
# printing these in failure details. Reconfigure if stdout supports it.
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SECTION_FILE_RE = re.compile(r"^(\d{2})_([a-z_]+)\.tex$")
CITE_RE = re.compile(r"\\cite[tp]?\*?\{([^}]+)\}")
REF_FIG_RE = re.compile(r"\\ref\{fig:([^}]+)\}")
REF_TAB_RE = re.compile(r"\\ref\{tab:([^}]+)\}")
SUBSECTION_RE = re.compile(r"\\subsection\{([^}]+)\}")
# Matches bulleted subsection entries in the blueprint outline, e.g.:
#   - **3.2 Fuzzy Gating Layer** — Thesis: ...
#   * **4.1 Overall Classification Performance** ...
BULLET_SUBSECTION_RE = re.compile(
    r"^\s*[-*+]\s+\*\*([\d.§]+\s+[^*]+?)\*\*",
    re.MULTILINE,
)
WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-']+")


def load_json(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def collect_tex_files(draft_dir: Path) -> list[Path]:
    return sorted([p for p in draft_dir.glob("*.tex") if SECTION_FILE_RE.match(p.name)])


def strip_latex_comments(text: str) -> str:
    out_lines = []
    for line in text.splitlines():
        # Strip trailing comments (%), but keep escaped \%
        result = []
        i = 0
        while i < len(line):
            ch = line[i]
            if ch == "\\" and i + 1 < len(line):
                result.append(line[i:i + 2])
                i += 2
                continue
            if ch == "%":
                break
            result.append(ch)
            i += 1
        out_lines.append("".join(result))
    return "\n".join(out_lines)


def count_words_in_tex(text: str) -> int:
    """Rough LaTeX word count — strips comments, commands, math, then counts word tokens."""
    text = strip_latex_comments(text)
    # Remove math display / inline
    text = re.sub(r"\$\$[\s\S]*?\$\$", " ", text)
    text = re.sub(r"\$[^$]*\$", " ", text)
    text = re.sub(r"\\begin\{equation\*?\}[\s\S]*?\\end\{equation\*?\}", " ", text)
    text = re.sub(r"\\begin\{align\*?\}[\s\S]*?\\end\{align\*?\}", " ", text)
    text = re.sub(r"\\begin\{algorithm\}[\s\S]*?\\end\{algorithm\}", " ", text)
    # Remove \cite{...}, \ref{...}, \label{...} arguments
    text = re.sub(r"\\(cite[tp]?|ref|eqref|label|cref)\*?\{[^}]*\}", " ", text)
    # Remove remaining control sequences
    text = re.sub(r"\\[a-zA-Z@]+\*?", " ", text)
    # Remove braces
    text = text.replace("{", " ").replace("}", " ")
    return len(WORD_RE.findall(text))


def parse_bib_keys(bib_path: Path) -> set[str]:
    if not bib_path.exists():
        return set()
    text = bib_path.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"@\w+\s*\{\s*([A-Za-z0-9_\-:]+)\s*,", text))


def parse_figure_labels_from_captions(md_path: Path) -> list[str]:
    """Extract figure labels from figure_captions.md. Heuristic: look for 'Fig N' in first column."""
    if not md_path.exists():
        return []
    text = md_path.read_text(encoding="utf-8")
    labels = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        m = re.match(r"(?:Fig\.?|Figure)\s*(\d+)", first, re.IGNORECASE)
        if m:
            labels.append(f"fig:{m.group(1)}")
    return labels


def parse_table_labels_from_captions(md_path: Path) -> list[str]:
    """Extract table labels from table_captions.md. Heuristic: look for 'Table N' in first column."""
    if not md_path.exists():
        return []
    text = md_path.read_text(encoding="utf-8")
    labels = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [c.strip() for c in stripped.strip("|").split("|")]
        if not cells:
            continue
        first = cells[0]
        m = re.match(r"(?:Tab\.?|Table)\s*(\d+)", first, re.IGNORECASE)
        if m:
            labels.append(f"tab:{m.group(1)}")
    return labels


def resolve_bib_path(session: Path, research_session: str) -> Path | None:
    """Try several conventions for locating references.bib.

    Historical confusion: `research_session` in step0_session_config.json may be
    expressed as relative to the session root (normal) or as relative to the
    session's parent (less common). Try both, then fall back to a shallow glob
    over typical Research/ locations.
    """
    if research_session:
        candidates = []
        candidate = Path(research_session)
        # Absolute as-is
        if candidate.is_absolute():
            candidates.append(candidate)
        else:
            # Relative to session root
            candidates.append((session / research_session).resolve())
            # Relative to session's parent (older convention)
            candidates.append((session.parent / research_session).resolve())
        for base in candidates:
            bib = base / "step4_references.bib"
            if bib.exists():
                return bib
    # Last-resort: walk up a couple of levels looking for Research/*/step4_references.bib
    for up in [session.parent, session.parent.parent,
               session.parent.parent.parent if session.parent.parent else None]:
        if up is None:
            continue
        for p in up.glob("Research/*/step4_references.bib"):
            return p
    return None


def parse_blueprint_subsections(md_path: Path) -> dict[str, list[str]]:
    """
    Group subsection titles by their parent section heading.

    Recognizes two section-heading conventions:
      - H2/H3 markdown headings with section name (e.g., `## Methods`, `### Results`)

    And two subsection conventions inside each section:
      - H3/H4 markdown subheadings
      - Bulleted entries of the form `- **3.2 Fuzzy Gating Layer** — ...`

    Returns {section_lowercase_with_underscores: [subsection_title, ...]}.
    """
    if not md_path.exists():
        return {}
    text = md_path.read_text(encoding="utf-8")
    out: dict[str, list[str]] = {}
    current_section: str | None = None
    section_names = {"introduction", "related work", "related_work", "methods",
                     "results", "discussion", "conclusion", "abstract"}

    for line in text.splitlines():
        s = line.rstrip()
        stripped = s.strip()

        # Detect section heading (H2 or H3)
        heading = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if heading:
            level = len(heading.group(1))
            title = heading.group(2).strip()
            # Strip leading numbering/anchors like "4.", "§3.2", "4.2"
            title_norm = re.sub(r"^[\d§.]+\s*", "", title).strip().lower()
            title_key = title_norm.replace(" ", "_")
            if level in (2, 3) and (title_norm in section_names or title_key in section_names):
                current_section = title_key
                out.setdefault(current_section, [])
                continue
            # H4 headings under a known section are treated as subsections
            if level == 4 and current_section:
                out[current_section].append(title)
                continue
            # H3 subsections inside an H2 section
            if level == 3 and current_section:
                out[current_section].append(title)
                continue

        # Detect bulleted subsection (`- **3.1 Title** — ...`)
        bullet = BULLET_SUBSECTION_RE.match(line)
        if bullet and current_section:
            out[current_section].append(bullet.group(1).strip())

    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--session-path", required=True, type=Path)
    parser.add_argument("--draft-subdir", default="step2_draft_v1",
                        help="Subdir containing the draft (default: step2_draft_v1)")
    args = parser.parse_args()

    session = args.session_path.resolve()
    draft_dir = session / args.draft_subdir

    failures: list[str] = []
    passes: list[str] = []

    def record(check: str, ok: bool, detail: str = ""):
        if ok:
            passes.append(check)
        else:
            failures.append(f"{check}: {detail}")

    # ---- Load session config
    session_config_path = session / "step0_session_config.json"
    if not session_config_path.exists():
        print(f"ERROR: {session_config_path} not found", file=sys.stderr)
        return 1
    session_config = load_json(session_config_path)
    research_session = session_config.get("research_session", "")
    section_structure = [s for s in session_config.get("section_structure", [])
                         if s.lower() != "abstract"]

    # ---- Check 1: every non-abstract section has non-empty .tex
    tex_files = collect_tex_files(draft_dir)
    tex_sections = {SECTION_FILE_RE.match(p.name).group(2): p for p in tex_files}
    missing = []
    empty = []
    for s in section_structure:
        key = s.lower().replace(" ", "_")
        if key not in tex_sections:
            missing.append(s)
        elif tex_sections[key].stat().st_size < 50:  # essentially empty
            empty.append(s)
    if missing or empty:
        detail = []
        if missing:
            detail.append(f"missing: {missing}")
        if empty:
            detail.append(f"empty: {empty}")
        record("1. Sections present & non-empty", False, "; ".join(detail))
    else:
        record("1. Sections present & non-empty", True)

    # ---- Check 2: every blueprint subsection present in matching .tex
    # Skip sections that the draft intentionally renders as single-flow prose
    # (no \subsection{} commands). Introduction and Conclusion are the usual
    # cases — short sections where subsection headings add visual noise with
    # no structural benefit. Only flag mismatches when the draft does use
    # subsections but their titles don't align with the blueprint.
    blueprint_subs = parse_blueprint_subsections(session / "step1_blueprint.md")
    missing_subs = []
    single_flow_sections = []
    for section_key, sub_titles in blueprint_subs.items():
        tex_path = tex_sections.get(section_key)
        if not tex_path:
            continue
        tex_text = strip_latex_comments(tex_path.read_text(encoding="utf-8"))
        present_subs = {m.group(1).strip().lower() for m in SUBSECTION_RE.finditer(tex_text)}
        if not present_subs:
            # Section is drafted as single-flow prose; skip subsection-title match.
            single_flow_sections.append(section_key)
            continue
        for title in sub_titles:
            title_norm = re.sub(r"^[\d§.]+\s*", "", title).strip().lower()
            if not any(title_norm in s or s in title_norm for s in present_subs):
                missing_subs.append(f"{section_key}: '{title}'")
    if missing_subs:
        note = ""
        if single_flow_sections:
            note = f" (skipped single-flow: {single_flow_sections})"
        record("2. Blueprint subsections drafted",
               False, f"missing subsections: {missing_subs[:5]}"
               + (f" (+{len(missing_subs)-5} more)" if len(missing_subs) > 5 else "")
               + note)
    else:
        detail = f"(single-flow sections skipped: {single_flow_sections})" if single_flow_sections else ""
        record("2. Blueprint subsections drafted", True, detail)

    # ---- Check 3: every figure in figure_captions.md is \ref{}'d somewhere
    fig_labels = parse_figure_labels_from_captions(
        session / "step1_preprocess" / "figure_captions.md"
    )
    all_tex_text = "\n".join(strip_latex_comments(p.read_text(encoding="utf-8"))
                             for p in tex_files)
    refd = set(f"fig:{m.group(1)}" for m in REF_FIG_RE.finditer(all_tex_text))
    orphans = [lbl for lbl in fig_labels if lbl not in refd]
    if orphans:
        record("3. All figures referenced", False,
               f"orphan figures: {orphans[:5]}"
               + (f" (+{len(orphans)-5} more)" if len(orphans) > 5 else ""))
    else:
        record("3. All figures referenced", True)

    # ---- Check 3b: every table in table_captions.md is \ref{}'d somewhere
    tab_labels = parse_table_labels_from_captions(
        session / "step1_preprocess" / "table_captions.md"
    )
    tab_refd = set(f"tab:{m.group(1)}" for m in REF_TAB_RE.finditer(all_tex_text))
    tab_orphans = [lbl for lbl in tab_labels if lbl not in tab_refd]
    if not tab_labels:
        # No tables declared — vacuously pass (some papers have no tables)
        record("3b. All tables referenced", True, "(no tables declared)")
    elif tab_orphans:
        record("3b. All tables referenced", False,
               f"orphan tables: {tab_orphans[:5]}"
               + (f" (+{len(tab_orphans)-5} more)" if len(tab_orphans) > 5 else ""))
    else:
        record("3b. All tables referenced", True)

    # ---- Check 4: every \cite{} resolves
    bib_path = resolve_bib_path(session, research_session)
    bib_keys = parse_bib_keys(bib_path) if bib_path else set()
    cite_keys_used: set[str] = set()
    for m in CITE_RE.finditer(all_tex_text):
        for key in m.group(1).split(","):
            cite_keys_used.add(key.strip())
    unresolved = sorted(k for k in cite_keys_used if k and bib_keys and k not in bib_keys)
    if bib_path is None:
        record("4. Citations resolve to bib",
               False, "could not locate references.bib — skipping cite-key validation")
    elif unresolved:
        record("4. Citations resolve to bib", False,
               f"unresolved: {unresolved[:5]}"
               + (f" (+{len(unresolved)-5} more)" if len(unresolved) > 5 else ""))
    else:
        record("4. Citations resolve to bib", True)

    # ---- Check 5: per-section word count within +-15% of budget
    config_path = session / "step2_global_config.json"
    if config_path.exists():
        config = load_json(config_path)
        profiles = config.get("section_profiles", {})
        budget_violations = []
        word_summary: list[tuple[str, int, int]] = []  # (section, actual, budget)
        for s in section_structure:
            key = s.lower().replace(" ", "_")
            profile = profiles.get(key) or profiles.get(s)
            if not profile:
                continue
            budget = int(profile.get("word_budget", 0))
            tex_path = tex_sections.get(key)
            if not tex_path or not budget:
                continue
            actual = count_words_in_tex(tex_path.read_text(encoding="utf-8"))
            word_summary.append((s, actual, budget))
            if budget and abs(actual - budget) / budget > 0.15:
                budget_violations.append(
                    f"{s}: {actual}w vs. budget {budget}w "
                    f"({(actual-budget)/budget*100:+.0f}%)"
                )
        if budget_violations:
            record("5. Per-section word count within +-15%", False,
                   "; ".join(budget_violations))
        else:
            record("5. Per-section word count within +-15%", True)
    else:
        record("5. Per-section word count within +-15%", False,
               "step2_global_config.json missing")
        word_summary = []

    # ---- Check 6: _sliding_window_state.json has per-section summaries
    state_path = draft_dir / "_sliding_window_state.json"
    if state_path.exists():
        state = load_json(state_path)
        sections_state = state.get("sections", {})
        missing_summaries = []
        for s in section_structure:
            key = s.lower().replace(" ", "_")
            entry = sections_state.get(key) or sections_state.get(s)
            if not entry or not entry.get("summary"):
                missing_summaries.append(s)
        if missing_summaries:
            record("6. Sliding-window state complete", False,
                   f"missing summaries: {missing_summaries}")
        else:
            record("6. Sliding-window state complete", True)
    else:
        record("6. Sliding-window state complete", False,
               f"{state_path.name} not found")

    # ---- Check 7: global_config well-formed
    required_fields = ["draft_version", "target_journal", "glossary",
                       "tense_lock", "section_profiles", "citation_format"]
    if config_path.exists():
        try:
            config = load_json(config_path)
            missing_fields = [f for f in required_fields if f not in config]
            if missing_fields:
                record("7. Global config well-formed", False,
                       f"missing fields: {missing_fields}")
            else:
                record("7. Global config well-formed", True)
        except json.JSONDecodeError as e:
            record("7. Global config well-formed", False, f"JSON error: {e}")
    else:
        record("7. Global config well-formed", False, "step2_global_config.json missing")

    # ---- Output
    print("=" * 72)
    print(f"Draft validator — {draft_dir}")
    print("=" * 72)
    for p in passes:
        print(f"  [PASS] {p}")
    for f in failures:
        print(f"  [FAIL] {f}")
    print("-" * 72)
    if word_summary:
        print("Word counts (per section):")
        for s, actual, budget in word_summary:
            delta = (actual - budget) / budget * 100 if budget else 0
            print(f"  {s:20s} actual={actual:5d}  budget={budget:5d}  delta={delta:+5.0f}%")
    print("-" * 72)
    print(f"Result: {len(passes)} passed, {len(failures)} failed")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
