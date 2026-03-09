#!/usr/bin/env python3
"""
Smart Import — Import any markdown report with automatic source enrichment.

When you drop in a report.md from any external source (ChatGPT, Perplexity,
manual writing, etc.), this script:

1. Parses [n] citations and extracts URLs from markdown
2. Fetches each URL and extracts metadata (title, author, description, og:tags)
3. Attempts to extract the quoted passage using surrounding context
4. Generates a fully enriched citation_map.json
5. Optionally captures snapshots

Usage:
    python smart_import.py report.md --output demo/my-report/
    python smart_import.py report.md --output demo/my-report/ --tags "AI,privacy" --category "技術研究"
    python smart_import.py report.md --output demo/my-report/ --capture-snapshots
"""

import argparse
import asyncio
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

import aiohttp

sys.path.insert(0, str(Path(__file__).parent))
from generate_citation_map import extract_citations_from_markdown, extract_youtube_id


class MetadataExtractor(HTMLParser):
    """Extract title, meta description, og:tags from HTML."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.meta: dict[str, str] = {}
        self._in_title = False
        self._title_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = attrs_dict.get("name", "").lower()
            prop = attrs_dict.get("property", "").lower()
            content = attrs_dict.get("content", "")
            if name == "description" or prop == "og:description":
                self.meta.setdefault("description", content)
            if name == "author" or prop == "article:author":
                self.meta.setdefault("author", content)
            if prop == "og:title":
                self.meta.setdefault("og_title", content)
            if prop == "og:type":
                self.meta.setdefault("og_type", content)
            if prop == "article:published_time":
                self.meta.setdefault("published_date", content[:10])
            if name == "keywords":
                self.meta.setdefault("keywords", content)

    def handle_data(self, data):
        if self._in_title:
            self._title_parts.append(data)

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
            self.title = "".join(self._title_parts).strip()


async def fetch_metadata(url: str, session: aiohttp.ClientSession) -> dict:
    """Fetch a URL and extract metadata from HTML."""
    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=12),
            headers={"User-Agent": "Mozilla/5.0 (compatible; SourceLinkedViewer/1.0)"},
            allow_redirects=True,
        ) as resp:
            if resp.status != 200:
                return {"_error": f"HTTP {resp.status}"}

            content_type = resp.headers.get("Content-Type", "")

            # For PDFs, we can only get basic info
            if "application/pdf" in content_type:
                return {
                    "title": urlparse(url).path.split("/")[-1],
                    "type": "pdf",
                }

            if "text/html" not in content_type:
                return {"_error": f"Unsupported content type: {content_type}"}

            # Read first 100KB (enough for metadata in <head>)
            chunk = await resp.content.read(102400)
            text = chunk.decode("utf-8", errors="replace")

            parser = MetadataExtractor()
            try:
                parser.feed(text)
            except Exception:
                pass

            return {
                "title": parser.meta.get("og_title") or parser.title or "",
                "author": parser.meta.get("author", ""),
                "description": parser.meta.get("description", ""),
                "published_date": parser.meta.get("published_date", ""),
                "keywords": parser.meta.get("keywords", ""),
                "type": "webpage",
            }
    except asyncio.TimeoutError:
        return {"_error": "Timeout"}
    except Exception as e:
        return {"_error": str(e)[:100]}


async def enrich_citations(citations: list[dict], md_text: str) -> list[dict]:
    """Fetch metadata for all citation URLs concurrently."""
    enriched = []

    async with aiohttp.ClientSession() as session:
        # Collect all URLs to fetch
        tasks = []
        for cit in citations:
            url = cit.get("auto_url")
            if url:
                tasks.append((cit, fetch_metadata(url, session)))
            else:
                tasks.append((cit, None))

        # Execute all fetches concurrently
        if tasks:
            fetch_tasks = [t[1] for t in tasks if t[1] is not None]
            results = await asyncio.gather(*fetch_tasks, return_exceptions=True)

            result_idx = 0
            for cit, task in tasks:
                if task is None:
                    enriched.append(cit)
                    continue

                result = results[result_idx]
                result_idx += 1

                if isinstance(result, Exception):
                    print(f"  [{cit['index']}] Error fetching: {result}")
                    enriched.append(cit)
                    continue

                if "_error" in result:
                    print(f"  [{cit['index']}] {result['_error']}: {cit.get('auto_url', '')[:60]}")
                    enriched.append(cit)
                    continue

                # Merge enriched metadata
                cit["enriched_title"] = result.get("title", "")
                cit["enriched_author"] = result.get("author", "")
                cit["enriched_description"] = result.get("description", "")
                cit["enriched_published_date"] = result.get("published_date", "")
                cit["enriched_type"] = result.get("type", "webpage")
                cit["enriched_keywords"] = result.get("keywords", "")

                title = result.get("title", "")
                if title:
                    print(f"  [{cit['index']}] ✓ {title[:60]}")
                else:
                    print(f"  [{cit['index']}] ✓ (no title) {cit.get('auto_url', '')[:60]}")

                enriched.append(cit)

    return enriched


def build_enriched_citation_map(
    report_path: Path,
    enriched_refs: list[dict],
    title: str | None = None,
    tags: list[str] | None = None,
    category: str | None = None,
) -> dict:
    """Build citation_map.json from enriched citation data."""
    md_text = report_path.read_text(encoding="utf-8")

    if not title:
        if m := re.search(r"^#\s+(.+)", md_text, re.MULTILINE):
            title = m.group(1).strip()
        else:
            title = report_path.stem

    report_id = report_path.parent.name or report_path.stem

    citations = []
    type_counts: dict[str, int] = {}

    for ref in enriched_refs:
        idx = ref["index"]
        url = ref.get("auto_url", "")
        source_type = ref.get("enriched_type", "webpage")

        # YouTube detection
        if url and any(v in url for v in ["youtube.com", "youtu.be"]):
            source_type = "video"

        type_counts[source_type] = type_counts.get(source_type, 0) + 1

        citation = {
            "id": f"ref-{idx:03d}",
            "index": idx,
            "source": {
                "url": url,
                "title": ref.get("enriched_title") or ref.get("auto_title") or f"Source {idx}",
                "type": source_type,
                "accessed_at": datetime.now(timezone.utc).isoformat(),
                "author": ref.get("enriched_author", ""),
                "publication_date": ref.get("enriched_published_date", ""),
            },
            "snapshot": {
                "file": f"snapshots/ref-{idx:03d}.html" if url else "",
                "format": "singlefile-html",
                "size_bytes": 0,
                "hash": "",
            },
            "anchors": [],
            "media": None,
        }

        # Handle video
        if source_type == "video" and url:
            yt_id = extract_youtube_id(url)
            if yt_id:
                citation["media"] = {
                    "platform": "youtube",
                    "video_id": yt_id,
                    "timestamp": 0,
                }

        citations.append(citation)

    # Collect all enriched keywords for auto-tagging
    auto_tags = set(tags or [])
    for ref in enriched_refs:
        kw = ref.get("enriched_keywords", "")
        if kw:
            for k in kw.split(","):
                k = k.strip()
                if k and len(k) < 30:
                    auto_tags.add(k)

    return {
        "$schema": "source-linked-viewer/citation-map/v2",
        "title": title,
        "report_id": report_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "generator": "smart_import/v1",
        "meta": {
            "tags": sorted(auto_tags)[:20],
            "category": category or "未分類",
            "status": "imported",
            "import_method": "smart_import",
        },
        "citations": citations,
        "stats": {
            "total_citations": len(citations),
            "by_type": type_counts,
            "snapshots_available": 0,
            "snapshots_failed": 0,
            "sources_enriched": sum(1 for r in enriched_refs if r.get("enriched_title")),
            "sources_no_url": sum(1 for r in enriched_refs if not r.get("auto_url")),
        },
    }


async def run_smart_import(
    report_path: Path,
    output_dir: Path,
    tags: list[str] | None,
    category: str | None,
    title: str | None,
    capture: bool,
):
    """Execute the full smart import pipeline."""
    print(f"Smart Import: {report_path.name}\n")

    # 1. Parse markdown
    md_text = report_path.read_text(encoding="utf-8")
    refs = extract_citations_from_markdown(md_text)
    print(f"[1/4] Found {len(refs)} citations in report")

    urls_found = sum(1 for r in refs if r.get("auto_url"))
    print(f"      URLs auto-extracted: {urls_found}/{len(refs)}")

    # 2. Enrich with fetched metadata
    print(f"\n[2/4] Fetching source metadata...")
    enriched = await enrich_citations(refs, md_text)

    # 3. Build citation map
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "snapshots").mkdir(exist_ok=True)
    (output_dir / "media").mkdir(exist_ok=True)

    import shutil
    shutil.copy2(report_path, output_dir / "report.md")

    citation_map = build_enriched_citation_map(report_path, enriched, title, tags, category)
    map_path = output_dir / "citation_map.json"

    with open(map_path, "w", encoding="utf-8") as f:
        json.dump(citation_map, f, ensure_ascii=False, indent=2)

    stats = citation_map["stats"]
    print(f"\n[3/4] Generated citation_map.json")
    print(f"      Total: {stats['total_citations']} citations")
    print(f"      Enriched: {stats['sources_enriched']}")
    print(f"      No URL: {stats['sources_no_url']}")
    print(f"      Tags: {citation_map['meta']['tags'][:5]}...")

    # 4. Optionally capture snapshots
    if capture:
        print(f"\n[4/4] Capturing snapshots...")
        from capture_snapshots import capture_all, find_singlefile
        singlefile = find_singlefile()
        await capture_all(map_path, singlefile, timeout=30)
    else:
        print(f"\n[4/4] Skipped snapshot capture (use --capture-snapshots to enable)")

    print(f"\n✓ Bundle ready: {output_dir}")
    print(f"  View at: http://127.0.0.1:8400/report/{output_dir.name}")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Import — import any report with automatic source enrichment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s report.md --output demo/my-report/
  %(prog)s report.md --output demo/my-report/ --tags "AI,edge computing" --category "技術研究"
  %(prog)s report.md --output demo/my-report/ --capture-snapshots
        """,
    )
    parser.add_argument("report", type=Path, help="Path to report.md")
    parser.add_argument("--output", type=Path, required=True, help="Output directory for the bundle")
    parser.add_argument("--tags", type=str, help="Comma-separated tags (e.g., 'AI,privacy,edge')")
    parser.add_argument("--category", type=str, help="Category name (e.g., '技術研究')")
    parser.add_argument("--title", type=str, help="Report title override")
    parser.add_argument("--capture-snapshots", action="store_true", help="Also capture source snapshots")
    args = parser.parse_args()

    if not args.report.exists():
        print(f"Error: Report not found: {args.report}", file=sys.stderr)
        sys.exit(1)

    tags = [t.strip() for t in args.tags.split(",")] if args.tags else None

    asyncio.run(run_smart_import(
        args.report, args.output, tags, args.category, args.title, args.capture_snapshots,
    ))


if __name__ == "__main__":
    main()
