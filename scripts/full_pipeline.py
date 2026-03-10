#!/usr/bin/env python3
"""
Full Verified Pipeline — From raw report to fully verified SLV bundle.

Runs all steps in sequence:
  1. Import:   Parse citations, build citation_map.json
  2. Snapshot:  Capture source pages as local HTML (SingleFile or HTTP)
  3. Anchor:   Match report claims to source text (TextQuoteSelector)
  4. Verify:   Set status to 'verified' if coverage ≥ 50%

Usage:
    python full_pipeline.py report.md --output demo/my-report/
    python full_pipeline.py report.md --output demo/my-report/ --tags "AI" --category "技術研究"
    python full_pipeline.py report.md --output demo/my-report/ --skip-snapshots  # offline mode

Result: A report bundle where clicking any citation highlights the
        exact source passage — just like the Edge AI demo report.
"""

import argparse
import asyncio
import subprocess
import sys
from pathlib import Path


SCRIPTS_DIR = Path(__file__).parent
VENV_PYTHON = SCRIPTS_DIR.parent / ".venv" / "bin" / "python"


def run_step(name: str, cmd: list[str], timeout: int = 60) -> bool:
    """Run a pipeline step and return success."""
    print(f"\n{'='*60}")
    print(f"  Step: {name}")
    print(f"{'='*60}\n")

    try:
        result = subprocess.run(cmd, timeout=timeout)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"  TIMEOUT after {timeout}s")
        return False
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def detect_format(report_path: Path) -> str:
    """Detect report citation format."""
    text = report_path.read_text(encoding="utf-8")

    if "[VERIFIED:" in text:
        return "cortex"

    import re
    if re.search(r"\[@?\d+\]", text):
        return "numeric"

    if re.search(r">\s*來源[：:]", text) or re.search(r"##.*參考", text):
        return "inline"

    return "unknown"


def main():
    parser = argparse.ArgumentParser(
        description="Full verified pipeline: import → snapshot → anchor → verify",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Pipeline steps:
  1. Import    — Detect format, parse citations, generate citation_map.json
  2. Snapshot  — Capture each source URL as local HTML (requires internet)
  3. Anchor    — Match report text ↔ source text, create TextQuoteSelectors
  4. Verify    — Validate and set status to 'verified'

Example:
  %(prog)s ~/Desktop/my-research.md --output demo/my-research/ --tags "AI"
        """,
    )
    parser.add_argument("report", type=Path, help="Path to report.md")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")
    parser.add_argument("--category", type=str, help="Category name")
    parser.add_argument("--title", type=str, help="Title override")
    parser.add_argument("--skip-snapshots", action="store_true",
                        help="Skip snapshot capture (offline mode)")
    args = parser.parse_args()

    if not args.report.exists():
        print(f"Error: {args.report} not found", file=sys.stderr)
        sys.exit(1)

    # Detect format
    fmt = detect_format(args.report)
    print(f"Detected format: {fmt}")

    # Step 1: Import
    if fmt == "cortex":
        import_script = "cortex_to_slv.py"
    else:
        import_script = "smart_import.py"

    import_cmd = [
        str(VENV_PYTHON), str(SCRIPTS_DIR / import_script),
        str(args.report), "--output", str(args.output),
    ]
    if args.tags:
        import_cmd += ["--tags", args.tags]
    if args.category:
        import_cmd += ["--category", args.category]
    if args.title:
        import_cmd += ["--title", args.title]

    if not run_step("1/4 Import", import_cmd):
        print("Import failed, aborting.")
        sys.exit(1)

    citation_map = args.output / "citation_map.json"

    # Step 2: Snapshot
    if not args.skip_snapshots:
        snapshot_cmd = [
            str(VENV_PYTHON), str(SCRIPTS_DIR / "capture_snapshots.py"),
            str(citation_map),
        ]
        run_step("2/4 Snapshot Capture", snapshot_cmd, timeout=120)
    else:
        print("\n[2/4] Skipped snapshot capture (--skip-snapshots)")

    # Step 3: Anchor enrichment
    anchor_cmd = [
        str(VENV_PYTHON), str(SCRIPTS_DIR / "enrich_anchors.py"),
        str(args.output),
    ]
    run_step("3/4 Anchor Enrichment", anchor_cmd)

    # Step 4: Summary
    import json
    with open(citation_map) as f:
        data = json.load(f)

    status = data.get("meta", {}).get("status", "imported")
    total = data["stats"]["total_citations"]
    anchored = sum(
        1 for c in data["citations"]
        if c.get("anchors") and any(a.get("source_selectors") for a in c["anchors"])
    )
    snapshots = sum(
        1 for c in data["citations"]
        if (args.output / c["snapshot"]["file"]).exists()
    ) if not args.skip_snapshots else 0

    print(f"\n{'='*60}")
    print(f"  Pipeline Complete")
    print(f"{'='*60}")
    print(f"  Status:     {status}")
    print(f"  Citations:  {total}")
    print(f"  Snapshots:  {snapshots}/{total}")
    print(f"  Anchored:   {anchored}/{total} (text highlighting)")
    print(f"  Coverage:   {anchored/total*100:.0f}%" if total > 0 else "  Coverage: N/A")
    print(f"")
    print(f"  View at: http://127.0.0.1:8400/report/{args.output.name}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
