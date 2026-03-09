#!/usr/bin/env python3
"""
Cortex-to-SLV Converter — Import Glen Cortex research reports into Source-Linked Viewer.

Reads a Glen Cortex report (.md) that uses [VERIFIED: descriptor] citation markers
and a source reference table, then generates a citation_map.json WITHOUT modifying
the original markdown.

Design principle: "Transform at render, preserve at rest"
  - report.md stays unchanged (keeps [VERIFIED: URL] for standalone PDF/MD reading)
  - citation_map.json maps verified descriptors → source metadata for the viewer
  - viewer.js dynamically transforms [VERIFIED: ...] → interactive [n] at render time

Usage:
    python cortex_to_slv.py report.md --output demo/my-report/
    python cortex_to_slv.py report.md --output demo/my-report/ --tags "AI,governance"
    python cortex_to_slv.py report.md --output demo/my-report/ --capture-snapshots

Cortex report format expected:
    Body: [VERIFIED: descriptor] markers inline
    Table: | # | 來源 | 類型 | Authority | Independence | 時效性 | URL |
"""

import argparse
import asyncio
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def parse_source_table(md_text: str) -> list[dict]:
    """Parse the source reference table at the bottom of a Cortex report.

    Expected format:
    | # | 來源 | 類型 | Authority | Independence | 時效性 | URL |
    |---|---|---|---|---|---|---|
    | S01 | EU AI Act Article 25 | 法規原文 | high | high | 有效 | https://... |
    """
    sources = []
    lines = md_text.split("\n")

    # Find table header row
    table_start = None
    for i, line in enumerate(lines):
        if re.match(r"\|\s*#\s*\|.*來源.*\|", line):
            table_start = i
            break
        # Also try English header
        if re.match(r"\|\s*#\s*\|.*Source.*\|", line, re.IGNORECASE):
            table_start = i
            break

    if table_start is None:
        return sources

    # Parse header to determine column positions
    header = lines[table_start]
    cols = [c.strip() for c in header.split("|")[1:-1]]  # Remove empty first/last from split

    # Find column indices by known names
    col_map: dict[str, int] = {}
    for idx, col in enumerate(cols):
        col_lower = col.lower().strip()
        if col_lower in ("#", "no", "編號"):
            col_map["id"] = idx
        elif col_lower in ("來源", "source", "description"):
            col_map["description"] = idx
        elif col_lower in ("類型", "type"):
            col_map["type"] = idx
        elif col_lower in ("authority", "權威性"):
            col_map["authority"] = idx
        elif col_lower in ("independence", "獨立性"):
            col_map["independence"] = idx
        elif col_lower in ("時效性", "date", "timeliness"):
            col_map["date"] = idx
        elif col_lower in ("url", "連結", "link"):
            col_map["url"] = idx

    # Skip separator row (|---|---|...)
    data_start = table_start + 2

    for line in lines[data_start:]:
        line = line.strip()
        if not line.startswith("|"):
            break  # End of table

        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 2:
            continue

        # Extract source ID number
        id_cell = cells[col_map.get("id", 0)] if "id" in col_map else cells[0]
        if m := re.search(r"S?(\d+)", id_cell):
            source_idx = int(m.group(1))
        else:
            continue

        source = {
            "index": source_idx,
            "description": cells[col_map["description"]] if "description" in col_map else "",
            "type": cells[col_map["type"]] if "type" in col_map else "webpage",
            "authority": cells[col_map["authority"]] if "authority" in col_map else "",
            "independence": cells[col_map["independence"]] if "independence" in col_map else "",
            "date": cells[col_map["date"]] if "date" in col_map else "",
            "url": "",
        }

        # Extract URL (may be in a markdown link or plain text)
        if "url" in col_map and col_map["url"] < len(cells):
            url_cell = cells[col_map["url"]]
            # Handle markdown links: [text](url) or plain URL
            if m := re.search(r"\[.*?\]\((https?://[^\)]+)\)", url_cell):
                source["url"] = m.group(1)
            elif m := re.search(r"(https?://\S+)", url_cell):
                source["url"] = m.group(1)

        sources.append(source)

    return sources


def extract_verified_markers(md_text: str) -> list[dict]:
    """Extract all [VERIFIED: descriptor] markers with context.

    Returns list of dicts with descriptor, section, paragraph, and surrounding text.
    """
    markers = []
    seen_descriptors = set()
    current_section = ""
    current_paragraph = 0

    for line in md_text.split("\n"):
        if m := re.match(r"^#{1,3}\s+(.+)", line):
            current_section = m.group(1).strip()
            current_paragraph = 0
            continue
        if line.strip() == "":
            current_paragraph += 1
            continue

        for m in re.finditer(r"\[VERIFIED:\s*([^\]]+)\]", line):
            descriptor = m.group(1).strip()
            if descriptor in seen_descriptors:
                continue
            seen_descriptors.add(descriptor)

            # Extract surrounding text for context
            start = max(0, m.start() - 60)
            end = min(len(line), m.end() + 60)
            context = line[start:end].strip()

            markers.append({
                "descriptor": descriptor,
                "section": current_section,
                "paragraph": current_paragraph,
                "context": context,
            })

    return markers


def match_markers_to_sources(
    markers: list[dict], sources: list[dict]
) -> list[dict]:
    """Match [VERIFIED: descriptor] markers to source table entries.

    Uses fuzzy matching: descriptor words compared against source description + URL.
    Returns enriched list with source data attached to each marker.
    """
    matched = []
    used_sources = set()

    for marker in markers:
        desc = marker["descriptor"].lower()
        desc_words = set(re.findall(r"[\w\u4e00-\u9fff]+", desc))

        best_source = None
        best_score = 0

        for src in sources:
            if src["index"] in used_sources:
                continue

            target = f"{src['description']} {src['url']}".lower()
            target_words = set(re.findall(r"[\w\u4e00-\u9fff]+", target))

            # Count overlapping words
            overlap = desc_words & target_words
            if not desc_words:
                continue
            score = len(overlap) / len(desc_words)

            # Bonus for URL domain match
            if src.get("url"):
                domain = urlparse(src["url"]).netloc.lower()
                if any(w in domain for w in desc_words):
                    score += 0.2

            if score > best_score and score >= 0.3:
                best_score = score
                best_source = src

        entry = {**marker, "source": best_source, "match_score": best_score}
        if best_source:
            used_sources.add(best_source["index"])
        matched.append(entry)

    # Also include unmatched sources (referenced in table but not in text)
    for src in sources:
        if src["index"] not in used_sources:
            matched.append({
                "descriptor": src["description"],
                "section": "",
                "paragraph": 0,
                "context": "",
                "source": src,
                "match_score": 0,
                "_unmatched_source": True,
            })

    return matched


def guess_source_type(type_str: str, url: str = "") -> str:
    """Map Cortex type strings to SLV source types."""
    type_lower = type_str.lower()

    if any(k in type_lower for k in ["法規", "regulation", "法", "act", "原文"]):
        return "webpage"
    if any(k in type_lower for k in ["pdf", "paper", "論文", "學術"]):
        return "pdf"
    if any(k in type_lower for k in ["video", "影片", "影像"]):
        return "video"

    if url:
        domain = urlparse(url).netloc.lower()
        if any(v in domain for v in ["youtube.com", "youtu.be"]):
            return "video"
        if url.lower().endswith(".pdf") or "arxiv.org" in domain:
            return "pdf"

    return "webpage"


def build_citation_map(
    report_path: Path,
    matched: list[dict],
    title: str | None = None,
    tags: list[str] | None = None,
    category: str | None = None,
) -> dict:
    """Build citation_map.json from matched markers + sources."""
    md_text = report_path.read_text(encoding="utf-8")

    if not title:
        if m := re.search(r"^#\s+(.+)", md_text, re.MULTILINE):
            title = m.group(1).strip()
        else:
            title = report_path.stem

    report_id = report_path.parent.name or report_path.stem

    citations = []
    type_counts: dict[str, int] = {}

    for i, entry in enumerate(matched, 1):
        src = entry.get("source") or {}
        url = src.get("url", "")
        source_type = guess_source_type(src.get("type", ""), url)
        type_counts[source_type] = type_counts.get(source_type, 0) + 1

        citation = {
            "id": f"ref-{i:03d}",
            "index": i,
            "source": {
                "url": url,
                "title": src.get("description", entry["descriptor"]),
                "type": source_type,
                "accessed_at": datetime.now(timezone.utc).isoformat(),
                "author": "",
                "publication_date": src.get("date", ""),
            },
            "meta": {
                "verified_label": entry["descriptor"],
                "authority": src.get("authority", ""),
                "independence": src.get("independence", ""),
                "match_score": entry.get("match_score", 0),
            },
            "snapshot": {
                "file": f"snapshots/ref-{i:03d}.html" if url else "",
                "format": "singlefile-html",
                "size_bytes": 0,
                "hash": "",
            },
            "anchors": [],
            "media": None,
        }

        citations.append(citation)

    # Build summary from first few lines
    summary = ""
    for line in md_text.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and len(line) > 20:
            # Remove markdown formatting for summary
            clean = re.sub(r"\*\*|__|`|#", "", line).strip()
            clean = re.sub(r"\[VERIFIED:[^\]]+\]", "", clean).strip()
            if len(clean) > 20:
                summary = clean[:120]
                break

    return {
        "$schema": "source-linked-viewer/citation-map/v2",
        "title": title,
        "report_id": report_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "cortex_to_slv/v1",
        "meta": {
            "tags": sorted(set(tags or []))[:20],
            "category": category or "未分類",
            "status": "imported",
            "import_method": "cortex_to_slv",
            "summary": summary,
            "original_format": "cortex_verified",
        },
        "citations": citations,
        "stats": {
            "total_citations": len(citations),
            "by_type": type_counts,
            "snapshots_available": 0,
            "snapshots_failed": 0,
            "markers_matched": sum(1 for e in matched if e.get("source") and not e.get("_unmatched_source")),
            "markers_unmatched": sum(1 for e in matched if not e.get("source")),
            "extra_sources": sum(1 for e in matched if e.get("_unmatched_source")),
        },
    }


def run_import(
    report_path: Path,
    output_dir: Path,
    tags: list[str] | None,
    category: str | None,
    title: str | None,
):
    """Execute the Cortex → SLV conversion."""
    print(f"Cortex → SLV Import: {report_path.name}\n")

    md_text = report_path.read_text(encoding="utf-8")

    # 1. Parse source table
    sources = parse_source_table(md_text)
    print(f"[1/4] Found {len(sources)} sources in reference table")
    for s in sources[:5]:
        url_short = s['url'][:50] + '...' if len(s.get('url', '')) > 50 else s.get('url', '(no URL)')
        print(f"      S{s['index']:02d}: {s['description'][:40]}  →  {url_short}")
    if len(sources) > 5:
        print(f"      ... and {len(sources) - 5} more")

    # 2. Extract [VERIFIED: ...] markers
    markers = extract_verified_markers(md_text)
    print(f"\n[2/4] Found {len(markers)} [VERIFIED: ...] markers in report body")
    for m in markers[:5]:
        print(f"      [{m['section'][:20]}] {m['descriptor'][:50]}")
    if len(markers) > 5:
        print(f"      ... and {len(markers) - 5} more")

    # 3. Match markers to sources
    matched = match_markers_to_sources(markers, sources)
    matched_count = sum(1 for e in matched if e.get("source") and not e.get("_unmatched_source"))
    print(f"\n[3/4] Matched {matched_count}/{len(markers)} markers to sources")

    # 4. Build bundle
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "snapshots").mkdir(exist_ok=True)
    (output_dir / "media").mkdir(exist_ok=True)

    # Copy report WITHOUT modification
    shutil.copy2(report_path, output_dir / "report.md")

    citation_map = build_citation_map(report_path, matched, title, tags, category)
    map_path = output_dir / "citation_map.json"

    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(citation_map, f, ensure_ascii=False, indent=2)

    stats = citation_map["stats"]
    print(f"\n[4/4] Generated citation_map.json")
    print(f"      Total citations: {stats['total_citations']}")
    print(f"      Types: {stats['by_type']}")
    print(f"      Matched: {stats['markers_matched']}")
    print(f"      Unmatched markers: {stats['markers_unmatched']}")
    print(f"      Extra sources (table-only): {stats['extra_sources']}")

    print(f"\n✓ Bundle ready: {output_dir}")
    print(f"  report.md preserved unchanged (keeps [VERIFIED: ...] for standalone reading)")
    print(f"  View at: http://127.0.0.1:8400/report/{output_dir.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert Glen Cortex research reports to Source-Linked Viewer bundles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Strategy: "Transform at render, preserve at rest"
  The original report.md is copied WITHOUT modification.
  [VERIFIED: descriptor] markers stay intact for standalone PDF/MD reading.
  The viewer dynamically transforms them to interactive [n] citations.

Examples:
  %(prog)s report.md --output demo/my-report/
  %(prog)s report.md --output demo/my-report/ --tags "AI,governance" --category "AI 治理"
        """,
    )
    parser.add_argument("report", type=Path, help="Path to Cortex research report (.md)")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for the bundle")
    parser.add_argument("--tags", type=str, help="Comma-separated tags")
    parser.add_argument("--category", type=str, help="Category name")
    parser.add_argument("--title", type=str, help="Report title override")
    args = parser.parse_args()

    if not args.report.exists():
        print(f"Error: Report not found: {args.report}", file=sys.stderr)
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None

    run_import(args.report, args.output, tags, args.category, args.title)


if __name__ == "__main__":
    main()
