#!/usr/bin/env python3
"""Inventory upstream Research + Algorithm artifacts for journal-init.

Scans the given session folders and reports which expected artifacts exist.
Outputs a JSON structure that the journal-init skill composes into
step0_session_config.json.

Usage:
    python inventory_artifacts.py \
        --research-session 0_Research/ \
        --algorithm-session Algorithm/20260104_multimodal-social-interaction/ \
        --figures-dir 8_Manuscript/figures/ \
        --project-root . \
        --output /tmp/journal_inventory.json

All paths may be relative to --project-root (default: current directory).
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Optional


# Artifact spec: key -> (relative_path_from_session, severity, consumed_by)
RESEARCH_ARTIFACTS = {
    "sota_review":              ("step6_sota_review.md",                "critical", "Blueprint, Draft(Intro/Related/Discussion), Review"),
    "gap_analysis":             ("step7_gap_analysis.md",               "critical", "Blueprint, Draft(Intro)"),
    "hypothesis":               ("step8_hypothesis_specification.md",   "critical", "Blueprint, Draft(Intro/Methods)"),
    "journal_recommendations":  ("step8_journal_recommendations.md",    "optional", "Init (target journal specs)"),
    "references_bib":           ("step4_references.bib",                "critical", "Draft, Review, Finalize"),
    "citation_keys":            ("step4_citation_keys.md",              "optional", "Review (citation accuracy)"),
    "full_text":                ("step5_full_text/",                    "optional", "Review (deep citation checks)"),
    "intro_draft":              ("step9_manuscript/01_intro.tex",       "optional", "Draft (cross-agent validation)"),
    "related_work_draft":       ("step9_manuscript/02_relatedwork.tex", "optional", "Draft (cross-agent validation)"),
}

ALGORITHM_ARTIFACTS = {
    "architecture_spec": ("step1_architecture_spec.md",  "critical", "Blueprint, Draft(Methods)"),
    "ablation_matrix":   ("step1_ablation_matrix.md",    "critical", "Draft(Methods, Results)"),
    "analysis_summary":  ("step4_analysis_summary.md",   "critical", "Draft(Results, Discussion), Review"),
    "figure_catalog":    ("step5_figure_catalog.md",     "critical", "Blueprint, Draft (all sections with figures)"),
    "experiment_report": ("step6_experiment_report.md",  "critical", "Draft(Results, Discussion), Review"),
}

# Commands that produce each artifact, for error messaging
PRODUCER_COMMANDS = {
    "sota_review": "/research-sota",
    "gap_analysis": "/research-gaps",
    "hypothesis": "/research-hypothesis",
    "journal_recommendations": "/research-hypothesis",
    "references_bib": "/research-export",
    "citation_keys": "/research-export",
    "full_text": "/research-fulltext",
    "intro_draft": "/research-write",
    "related_work_draft": "/research-write",
    "architecture_spec": "/algo-design",
    "ablation_matrix": "/algo-design",
    "analysis_summary": "/algo-analyze",
    "figure_catalog": "/algo-figures",
    "experiment_report": "/algo-report",
    "figures_dir": "/algo-figures",
}


@dataclass
class ArtifactResult:
    key: str
    expected_path: str
    resolved_path: Optional[str]
    found: bool
    severity: str
    consumed_by: str
    notes: Optional[str] = None
    suggested_command: Optional[str] = None


@dataclass
class InventoryReport:
    research_session: Optional[str]
    algorithm_session: Optional[str]
    figures_dir: Optional[str]
    from_research: dict = field(default_factory=dict)
    from_algorithm: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    critical_missing: list = field(default_factory=list)
    summary: dict = field(default_factory=dict)


def check_path(full_path: Path) -> tuple[bool, Optional[str]]:
    """Return (found, notes). For directories, also report coverage."""
    if not full_path.exists():
        return False, None
    if full_path.is_dir():
        # Count non-hidden entries for a coverage hint
        entries = [p for p in full_path.iterdir() if not p.name.startswith(".")]
        if not entries:
            return True, "directory exists but is empty"
        return True, f"directory with {len(entries)} entries"
    size = full_path.stat().st_size
    if size == 0:
        return True, "file exists but is empty"
    return True, None


def inventory_group(
    session_path: Optional[Path],
    project_root: Path,
    session_rel: Optional[str],
    spec: dict,
) -> dict:
    """Scan a session folder for its expected artifacts."""
    results = {}
    if session_path is None or session_rel is None:
        for key, (rel_path, severity, consumed_by) in spec.items():
            results[key] = asdict(ArtifactResult(
                key=key,
                expected_path=rel_path,
                resolved_path=None,
                found=False,
                severity=severity,
                consumed_by=consumed_by,
                notes="session path not provided",
                suggested_command=PRODUCER_COMMANDS.get(key),
            ))
        return results

    for key, (rel_path, severity, consumed_by) in spec.items():
        full_path = session_path / rel_path
        found, notes = check_path(full_path)
        resolved = None
        if found:
            # Store path relative to project_root for portability
            try:
                resolved = str(full_path.resolve().relative_to(project_root.resolve()))
                if full_path.is_dir() and not resolved.endswith("/"):
                    resolved += "/"
            except ValueError:
                resolved = str(full_path)
        results[key] = asdict(ArtifactResult(
            key=key,
            expected_path=f"{session_rel.rstrip('/')}/{rel_path}",
            resolved_path=resolved,
            found=found,
            severity=severity,
            consumed_by=consumed_by,
            notes=notes,
            suggested_command=PRODUCER_COMMANDS.get(key) if not found else None,
        ))
    return results


def check_figures_dir(project_root: Path, figures_rel: Optional[str]) -> dict:
    spec_entry = ("figures_dir", "8_Manuscript/figures/", "critical", "Draft, Finalize (LaTeX packaging)")
    key, default_rel, severity, consumed_by = spec_entry
    rel = figures_rel or default_rel
    full_path = project_root / rel
    found, notes = check_path(full_path)
    # Count figure files specifically
    if found and full_path.is_dir():
        fig_exts = {".pdf", ".png", ".jpg", ".jpeg", ".eps", ".svg"}
        figs = [p for p in full_path.rglob("*") if p.is_file() and p.suffix.lower() in fig_exts]
        notes = f"{len(figs)} figure files found"
    return asdict(ArtifactResult(
        key=key,
        expected_path=rel,
        resolved_path=(rel if found else None),
        found=found,
        severity=severity,
        consumed_by=consumed_by,
        notes=notes,
        suggested_command=PRODUCER_COMMANDS.get(key) if not found else None,
    ))


def build_summary(report: InventoryReport) -> dict:
    def tally(group: dict) -> dict:
        total = len(group)
        found = sum(1 for r in group.values() if r["found"])
        critical_missing = sum(
            1 for r in group.values()
            if not r["found"] and r["severity"] == "critical"
        )
        return {"total": total, "found": found, "critical_missing": critical_missing}

    return {
        "from_research": tally(report.from_research),
        "from_algorithm": tally(report.from_algorithm),
        "figures_dir_found": report.from_algorithm.get("figures_dir", {}).get("found", False),
        "total_warnings": len(report.warnings),
        "total_critical_missing": len(report.critical_missing),
    }


def collect_warnings_and_missing(report: InventoryReport) -> None:
    for group in (report.from_research, report.from_algorithm):
        for key, r in group.items():
            if not r["found"]:
                if r["severity"] == "critical":
                    report.critical_missing.append({
                        "artifact": key,
                        "path_checked": r["expected_path"],
                        "suggested_command": r.get("suggested_command"),
                        "consumed_by": r["consumed_by"],
                    })
                else:
                    report.warnings.append({
                        "artifact": key,
                        "issue": "missing_optional",
                        "detail": f"Optional artifact not found at {r['expected_path']}. "
                                  f"Downstream: {r['consumed_by']} will degrade gracefully.",
                    })
            elif r.get("notes") and ("empty" in r["notes"] or "0 entries" in r["notes"]):
                report.warnings.append({
                    "artifact": key,
                    "issue": "empty",
                    "detail": r["notes"],
                })


def parse_args():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--research-session", help="Path to Research session folder (relative or absolute)")
    p.add_argument("--algorithm-session", help="Path to Algorithm session folder")
    p.add_argument("--figures-dir", default="8_Manuscript/figures/",
                   help="Path to publication figures directory (default: 8_Manuscript/figures/)")
    p.add_argument("--project-root", default=".", help="Project root for relative path resolution")
    p.add_argument("--output", help="Output JSON file path (default: stdout)")
    return p.parse_args()


def main():
    args = parse_args()
    project_root = Path(args.project_root).resolve()

    research_path = (project_root / args.research_session).resolve() if args.research_session else None
    algorithm_path = (project_root / args.algorithm_session).resolve() if args.algorithm_session else None

    report = InventoryReport(
        research_session=args.research_session,
        algorithm_session=args.algorithm_session,
        figures_dir=args.figures_dir,
    )

    report.from_research = inventory_group(
        research_path, project_root, args.research_session, RESEARCH_ARTIFACTS,
    )
    report.from_algorithm = inventory_group(
        algorithm_path, project_root, args.algorithm_session, ALGORITHM_ARTIFACTS,
    )
    report.from_algorithm["figures_dir"] = check_figures_dir(project_root, args.figures_dir)

    collect_warnings_and_missing(report)
    report.summary = build_summary(report)

    payload = asdict(report)
    out = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
        print(f"Inventory written to {args.output}")
        print(f"Summary: {json.dumps(report.summary, indent=2)}")
    else:
        print(out)


if __name__ == "__main__":
    main()
