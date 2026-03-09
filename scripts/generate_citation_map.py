#!/usr/bin/env python3
"""
Generate citation_map.json from a research report markdown file.

Supports three modes:
  1. With sources.json (from dto-scout pipeline) — full metadata + anchors
  2. Without sources — auto-extracts URLs from markdown links near [n] references
  3. Hybrid — uses sources.json where available, auto-extracts for the rest

Usage:
    # With full source metadata (pipeline mode)
    python generate_citation_map.py report.md --sources sources.json

    # Without sources (auto-extract from markdown links)
    python generate_citation_map.py report.md

    # Custom output directory
    python generate_citation_map.py report.md --output ~/Desktop/my-report/

The sources.json file should contain raw source data from dto-scout:
[
  {
    "index": 1,
    "url": "https://...",
    "title": "...",
    "type": "webpage",
    "author": "...",
    "publication_date": "2026-01",
    "accessed_at": "2026-03-09T10:00:00Z",
    "quote": "exact text from source",
    "quote_prefix": "text before quote",
    "quote_suffix": "text after quote"
  }
]
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


def extract_citations_from_markdown(md_text: str) -> list[dict]:
    """Extract citations from markdown, supporting multiple formats.

    Supported formats:
      1. [n] / [@n] — numeric academic-style citations
      2. > 來源：[Title](URL) — blockquote source lines (ChatGPT / manual style)
      3. [Title](URL) inline links in reference sections

    Returns a unified list regardless of input format.
    """
    # Try numeric [n] first
    numeric = _extract_numeric_citations(md_text)
    if numeric:
        return numeric

    # Fallback: extract inline source links (> 來源：pattern + reference sections)
    inline = _extract_inline_source_citations(md_text)
    if inline:
        return inline

    return []


def _extract_numeric_citations(md_text: str) -> list[dict]:
    """Extract [n] or [@n] citation references with context and nearby URLs."""
    citations = []
    seen = set()

    current_section = ""
    current_paragraph = 0
    lines = md_text.split("\n")

    # First pass: collect all URLs in the document associated with references
    ref_urls: dict[int, str] = {}
    ref_titles: dict[int, str] = {}

    for line in lines:
        # Pattern: [n]: https://url "title"  (reference-style link definition)
        if m := re.match(r"^\[(\d+)\]:\s*(https?://\S+)(?:\s+[\"'](.+?)[\"'])?\s*$", line):
            idx = int(m.group(1))
            ref_urls[idx] = m.group(2)
            if m.group(3):
                ref_titles[idx] = m.group(3)

        # Pattern: [n](https://url)  (citation number as link)
        for m in re.finditer(r"\[(\d+)\]\((https?://[^\)]+)\)", line):
            idx = int(m.group(1))
            if idx not in ref_urls:
                ref_urls[idx] = m.group(2)

    # Second pass: extract citations with context
    for line_num, line in enumerate(lines):
        if match := re.match(r"^#{1,3}\s+(.+)", line):
            current_section = match.group(1).strip()
            current_paragraph = 0
            continue

        if line.strip() == "":
            current_paragraph += 1
            continue

        for match in re.finditer(r"\[@?(\d+)\](?:\([^\)]*\))?", line):
            index = int(match.group(1))
            if index in seen:
                continue
            seen.add(index)

            start = max(0, match.start() - 50)
            end = min(len(line), match.end() + 50)
            context = line[start:end].strip()

            nearby_url = ref_urls.get(index)
            if not nearby_url:
                search_range = "\n".join(lines[max(0, line_num - 1):line_num + 2])
                url_matches = re.findall(r"https?://[^\s\)\"'>]+", search_range)
                if url_matches:
                    nearby_url = url_matches[0]

            citations.append({
                "index": index,
                "section": current_section,
                "paragraph": current_paragraph,
                "context": context,
                "auto_url": nearby_url,
                "auto_title": ref_titles.get(index),
            })

    return sorted(citations, key=lambda c: c["index"])


def _extract_inline_source_citations(md_text: str) -> list[dict]:
    """Extract citations from inline markdown links.

    Detects patterns like:
      > 來源：[Title](URL)、[Title2](URL2)
      > Source: [Title](URL)
      **來源**：[Title](URL)
      - [Title](URL)  (in reference sections)
    """
    citations = []
    seen_urls: set[str] = set()
    index = 0

    current_section = ""
    current_paragraph = 0
    lines = md_text.split("\n")
    in_reference_section = False

    for line_num, line in enumerate(lines):
        stripped = line.strip()

        if match := re.match(r"^(#{1,3})\s+(.+)", stripped):
            heading_level = len(match.group(1))
            current_section = match.group(2).strip()
            current_paragraph = 0
            # Detect reference/bibliography sections
            ref_keywords = ["參考", "文獻", "reference", "bibliography", "sources", "來源"]
            is_ref = any(k in current_section.lower() for k in ref_keywords)
            if is_ref:
                in_reference_section = True
            elif heading_level <= 2:
                # Only a top-level heading (## or #) exits the reference section
                # Sub-headings (###) within a reference section are preserved
                in_reference_section = False
            continue

        if stripped == "":
            current_paragraph += 1
            continue

        # Check if this line is a source citation line
        is_source_line = bool(re.match(r"^>\s*來源[：:]|^>\s*[Ss]ource[：:]|^\*\*來源\*\*[：:]", stripped))

        # In reference sections, any line with links counts
        # Also match list items with links: - [Title](URL)
        has_link = bool(re.search(r"\[.+?\]\(https?://", stripped))
        should_extract = is_source_line or (in_reference_section and has_link)

        if not should_extract:
            continue

        # Extract all [Title](URL) from this line
        for m in re.finditer(r"\[([^\]]+)\]\((https?://[^\)]+)\)", line):
            title = m.group(1).strip()
            url = m.group(2).strip()

            if url in seen_urls:
                continue
            seen_urls.add(url)

            index += 1

            # Get context: the preceding non-empty, non-source line
            context = ""
            for prev_i in range(line_num - 1, max(0, line_num - 5), -1):
                prev = lines[prev_i].strip()
                if prev and not prev.startswith(">") and not prev.startswith("#"):
                    context = prev[:100]
                    break

            citations.append({
                "index": index,
                "section": current_section,
                "paragraph": current_paragraph,
                "context": context,
                "auto_url": url,
                "auto_title": title,
                "source_line": stripped[:100],
            })

    return citations


def guess_source_type(url: str) -> str:
    """Guess source type from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    if any(v in domain for v in ["youtube.com", "youtu.be", "vimeo.com"]):
        return "video"
    if path.endswith(".pdf"):
        return "pdf"
    if "arxiv.org" in domain:
        return "pdf"
    if any(d in domain for d in ["github.com", "gitlab.com"]):
        return "webpage"
    return "webpage"


def extract_youtube_id(url: str) -> str | None:
    """Extract YouTube video ID from URL."""
    patterns = [
        r"youtube\.com/watch\?v=([^&]+)",
        r"youtu\.be/([^?]+)",
        r"youtube\.com/embed/([^?]+)",
    ]
    for pattern in patterns:
        if m := re.search(pattern, url):
            return m.group(1)
    return None


def extract_title_from_context(context: str, url: str) -> str:
    """Try to extract a meaningful title from citation context or URL."""
    # Remove the [n] reference from context
    clean = re.sub(r"\[@?\d+\](\([^\)]*\))?", "", context).strip()
    # Remove markdown formatting
    clean = re.sub(r"[*_`\[\]]", "", clean).strip()
    # Remove trailing punctuation
    clean = clean.rstrip("，。、；：")

    if len(clean) > 15:
        return clean[:80]

    # Fallback to domain name
    parsed = urlparse(url)
    return parsed.netloc or "Unknown Source"


def build_citation_map(
    report_path: Path,
    sources: list[dict] | None = None,
    title: str | None = None,
) -> dict:
    """Build a complete citation_map.json structure."""
    md_text = report_path.read_text(encoding="utf-8")
    refs = extract_citations_from_markdown(md_text)

    # Build source lookup from provided sources
    source_lookup = {}
    if sources:
        for s in sources:
            source_lookup[s["index"]] = s

    # Auto-detect title from first H1
    if not title:
        if m := re.search(r"^#\s+(.+)", md_text, re.MULTILINE):
            title = m.group(1).strip()
        else:
            title = report_path.stem

    report_id = report_path.parent.name or report_path.stem

    citations = []
    type_counts: dict[str, int] = {}
    auto_extracted_count = 0

    for ref in refs:
        idx = ref["index"]
        src = source_lookup.get(idx, {})

        # If no source provided, try auto-extraction from markdown
        if not src and ref.get("auto_url"):
            auto_extracted_count += 1
            url = ref["auto_url"]
            src = {
                "url": url,
                "title": ref.get("auto_title") or extract_title_from_context(ref["context"], url),
                "type": guess_source_type(url),
                "author": "",
                "accessed_at": datetime.now(timezone.utc).isoformat(),
                "_auto_extracted": True,
            }
            # Auto-detect YouTube
            if src["type"] == "video":
                yt_id = extract_youtube_id(url)
                if yt_id:
                    src["video_id"] = yt_id
                    src["platform"] = "youtube"

        source_type = src.get("type", "webpage")
        type_counts[source_type] = type_counts.get(source_type, 0) + 1

        citation: dict = {
            "id": f"ref-{idx:03d}",
            "index": idx,
            "source": {
                "url": src.get("url", ""),
                "title": src.get("title", f"Source {idx}"),
                "type": source_type,
                "accessed_at": src.get("accessed_at", datetime.now(timezone.utc).isoformat()),
                "author": src.get("author", ""),
                "publication_date": src.get("publication_date", ""),
            },
            "snapshot": {
                "file": f"snapshots/ref-{idx:03d}.html",
                "format": "singlefile-html",
                "size_bytes": 0,
                "hash": "",
            },
            "anchors": [],
            "media": None,
        }

        # Build anchor with TextQuoteSelector if quote available
        if src.get("quote"):
            citation["anchors"].append({
                "report_location": {
                    "section": ref["section"],
                    "paragraph": ref["paragraph"],
                    "text_fragment": ref["context"],
                },
                "source_selectors": [
                    {
                        "type": "TextQuoteSelector",
                        "exact": src["quote"],
                        "prefix": src.get("quote_prefix", ""),
                        "suffix": src.get("quote_suffix", ""),
                    },
                ],
            })

        # Handle video type
        if source_type == "video" and src.get("video_id"):
            citation["media"] = {
                "platform": src.get("platform", "youtube"),
                "video_id": src["video_id"],
                "timestamp": src.get("timestamp", 0),
            }

        citations.append(citation)

    return {
        "$schema": "source-linked-viewer/citation-map/v1",
        "title": title,
        "report_id": report_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "generate_citation_map/v1",
        "citations": citations,
        "stats": {
            "total_citations": len(citations),
            "by_type": type_counts,
            "snapshots_available": 0,
            "snapshots_failed": 0,
            "auto_extracted_sources": auto_extracted_count,
            "avg_anchors_per_citation": (
                sum(len(c["anchors"]) for c in citations) / len(citations)
                if citations
                else 0
            ),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Generate citation_map.json from a research report",
        epilog="""
Examples:
  %(prog)s report.md                          # Auto-extract URLs from markdown
  %(prog)s report.md --sources sources.json   # Use full source metadata
  %(prog)s report.md --output ~/Desktop/out/  # Custom output directory
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("report", type=Path, help="Path to report.md")
    parser.add_argument("--sources", type=Path, help="Path to sources.json (from dto-scout)")
    parser.add_argument("--output", type=Path, help="Output directory (default: same as report)")
    parser.add_argument("--title", type=str, help="Report title override")
    args = parser.parse_args()

    if not args.report.exists():
        print(f"Error: Report not found: {args.report}", file=sys.stderr)
        sys.exit(1)

    sources = None
    if args.sources and args.sources.exists():
        with open(args.sources) as f:
            sources = json.load(f)
        print(f"Loaded {len(sources)} sources from {args.sources}")
    else:
        print("No sources.json provided — will auto-extract URLs from markdown")

    citation_map = build_citation_map(args.report, sources, args.title)

    output_dir = args.output or args.report.parent
    output_file = output_dir / "citation_map.json"
    output_dir.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(citation_map, f, ensure_ascii=False, indent=2)

    stats = citation_map["stats"]
    print(f"\nGenerated: {output_file}")
    print(f"  Citations: {stats['total_citations']}")
    print(f"  Types: {stats['by_type']}")
    if stats.get("auto_extracted_sources"):
        print(f"  Auto-extracted: {stats['auto_extracted_sources']} (from markdown links)")


if __name__ == "__main__":
    main()
