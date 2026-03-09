#!/usr/bin/env python3
"""
Bundle a research report for the Source-Linked Viewer.

Complete pipeline: parse report → generate citation map → capture snapshots → validate.

Usage:
    python bundle_report.py <report.md> --sources sources.json --output ~/Desktop/

This is the main integration point for the research-orchestrator pipeline.
After dto-writer produces report.md and dto-scout produces sources.json,
this script bundles everything into a viewer-ready directory.
"""

import argparse
import asyncio
import json
import shutil
import sys
from pathlib import Path

# Import sibling modules
sys.path.insert(0, str(Path(__file__).parent))
from generate_citation_map import build_citation_map
from capture_snapshots import capture_all, find_singlefile


def validate_bundle(bundle_dir: Path) -> list[str]:
    """Validate the bundle is complete and well-formed."""
    issues = []

    report_md = bundle_dir / "report.md"
    citation_map = bundle_dir / "citation_map.json"

    if not report_md.exists():
        issues.append("Missing report.md")
    if not citation_map.exists():
        issues.append("Missing citation_map.json")
        return issues

    with open(citation_map) as f:
        data = json.load(f)

    citations = data.get("citations", [])
    snapshots_dir = bundle_dir / "snapshots"

    for c in citations:
        if c["source"]["type"] == "video":
            continue

        snapshot_file = bundle_dir / c["snapshot"]["file"] if c.get("snapshot", {}).get("file") else None
        if not snapshot_file or not snapshot_file.exists():
            issues.append(f"Missing snapshot for [{c['index']}] {c['source'].get('title', '')[:40]}")

        if not c.get("anchors"):
            issues.append(f"No anchors for [{c['index']}] — source highlighting won't work")

    return issues


async def bundle(
    report_path: Path,
    sources_path: Path | None,
    output_dir: Path,
    title: str | None,
    timeout: int,
    skip_capture: bool,
):
    """Run the full bundling pipeline."""
    # 1. Setup output directory
    report_name = report_path.stem
    bundle_dir = output_dir / report_name
    bundle_dir.mkdir(parents=True, exist_ok=True)
    (bundle_dir / "snapshots").mkdir(exist_ok=True)
    (bundle_dir / "media").mkdir(exist_ok=True)

    # 2. Copy report
    shutil.copy2(report_path, bundle_dir / "report.md")
    print(f"[1/4] Copied report.md")

    # 3. Generate citation map
    sources = None
    if sources_path and sources_path.exists():
        with open(sources_path) as f:
            sources = json.load(f)

    citation_map = build_citation_map(report_path, sources, title)
    citation_map_path = bundle_dir / "citation_map.json"

    with open(citation_map_path, "w", encoding="utf-8") as f:
        json.dump(citation_map, f, ensure_ascii=False, indent=2)
    print(f"[2/4] Generated citation_map.json ({citation_map['stats']['total_citations']} citations)")

    # 4. Capture snapshots
    if not skip_capture:
        singlefile = find_singlefile()
        print(f"[3/4] Capturing snapshots...")
        await capture_all(citation_map_path, singlefile, timeout)
    else:
        print(f"[3/4] Skipped snapshot capture (--skip-capture)")

    # 5. Validate
    issues = validate_bundle(bundle_dir)
    if issues:
        print(f"\n[4/4] Validation warnings:")
        for issue in issues:
            print(f"  ⚠ {issue}")
    else:
        print(f"[4/4] Validation passed ✓")

    print(f"\nBundle ready: {bundle_dir}")
    print(f"View at: http://127.0.0.1:8400/report/{report_name}")


def main():
    parser = argparse.ArgumentParser(description="Bundle a report for Source-Linked Viewer")
    parser.add_argument("report", type=Path, help="Path to report.md")
    parser.add_argument("--sources", type=Path, help="Path to sources.json")
    parser.add_argument("--output", type=Path, default=Path("demo"), help="Output directory")
    parser.add_argument("--title", type=str, help="Report title override")
    parser.add_argument("--timeout", type=int, default=30, help="Snapshot capture timeout")
    parser.add_argument("--skip-capture", action="store_true", help="Skip snapshot capture")
    args = parser.parse_args()

    if not args.report.exists():
        print(f"Error: Report not found: {args.report}", file=sys.stderr)
        sys.exit(1)

    asyncio.run(bundle(args.report, args.sources, args.output, args.title, args.timeout, args.skip_capture))


if __name__ == "__main__":
    main()
