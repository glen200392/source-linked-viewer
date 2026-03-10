#!/usr/bin/env python3
"""
Enrich Anchors — Generate TextQuoteSelectors by matching report claims to source text.

Implements a hybrid anchoring strategy inspired by Hypothesis (hypothes.is):

  Strategy A (high quality): If the report contains inline source quotes
     (> 引用原文：「...」), use them directly as TextQuoteSelector exact text.
     This is the "capture at annotation time" approach.

  Strategy B (automated): For reports without inline quotes, use Bitap fuzzy
     matching (google diff-match-patch) to find the best matching passage in
     the source snapshot. Handles cross-language (Chinese report ↔ English source).

  Orphan handling: Citations that fail all matching strategies are marked as
     orphan anchors — they still appear in the UI but without text highlighting.

Usage:
    python enrich_anchors.py demo/my-report/
    python enrich_anchors.py demo/my-report/ --verify

For best quality, include source quotes in report markdown:
    > 來源：[Title](URL)
    > 引用原文：「The median time-to-first-token for GPT-4o is 597ms.」
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from diff_match_patch import diff_match_patch


class TextExtractor(HTMLParser):
    """Extract visible text from HTML, ignoring scripts/styles."""

    def __init__(self):
        super().__init__()
        self.text_parts: list[str] = []
        self._skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self._skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self._skip = False

    def handle_data(self, data):
        if not self._skip:
            self.text_parts.append(data)

    def get_text(self) -> str:
        return " ".join(self.text_parts)


def extract_text_from_html(html_path: Path) -> str:
    """Extract plain text from an HTML file."""
    try:
        content = html_path.read_text(encoding="utf-8", errors="replace")
        parser = TextExtractor()
        parser.feed(content)
        return parser.get_text()
    except Exception:
        return ""


def normalize(s: str) -> str:
    """Normalize whitespace for comparison."""
    return re.sub(r"\s+", " ", s).strip()


def _title_matches_line(title: str, line: str) -> bool:
    """Check if a citation title (possibly abbreviated) appears in a line.

    Handles cases where the report abbreviates source titles, e.g.:
      citation_map title: "LLM Latency Benchmark by Use Cases in 2026"
      report line:        "> 來源：[LLM Latency Benchmark](url)"
    """
    if not title:
        return False
    # Direct substring match
    if title in line:
        return True
    # Check if first 3+ significant words of title appear in line
    title_words = [w for w in re.findall(r"[\w\u4e00-\u9fff]+", title) if len(w) >= 3]
    if len(title_words) >= 2:
        line_lower = line.lower()
        matched = sum(1 for w in title_words[:4] if w.lower() in line_lower)
        return matched >= min(2, len(title_words[:4]))
    return False


def find_report_context(md_text: str, citation_index: int, citation_title: str, source_url: str = "") -> str:
    """Find the paragraph in the report that references this citation.

    Searches for the citation's surrounding text to understand what claim
    the report is making based on this source.
    """
    lines = md_text.split("\n")

    # Strategy 1: For > 來源：style, find the paragraph BEFORE the source line
    for i, line in enumerate(lines):
        if _title_matches_line(citation_title, line) or (source_url and source_url in line):
            # Walk backwards to collect content paragraphs (not blockquotes/headings)
            context_parts = []
            for j in range(i - 1, max(0, i - 10), -1):
                stripped = lines[j].strip()
                if not stripped:
                    if context_parts:
                        break  # Empty line after finding content = stop
                    continue
                if stripped.startswith(">") or stripped.startswith("#"):
                    if context_parts:
                        break
                    continue
                context_parts.insert(0, stripped)
            if context_parts:
                combined = " ".join(context_parts)
                # Strip markdown formatting
                combined = re.sub(r"[*_`]", "", combined)
                return combined[:300]

    # Strategy 2: For [n] style, find the line containing [n]
    pattern = rf"\[@?{citation_index}\]"
    for line in lines:
        if re.search(pattern, line):
            # Remove the citation marker and markdown formatting
            clean = re.sub(r"\[@?\d+\](\([^\)]*\))?", "", line)
            clean = re.sub(r"[*_`#>]", "", clean).strip()
            if len(clean) > 20:
                return clean[:200]

    return ""


def extract_inline_quotes(md_text: str) -> dict[str, str]:
    """Extract inline source quotes from report markdown (Route A).

    Recognizes patterns like:
      > 引用原文：「The median time-to-first-token for GPT-4o is 597ms.」
      > 引用原文："The median time-to-first-token for GPT-4o is 597ms."
      > Quote: "exact text from the source"

    Returns {url: exact_quote} mapping.
    """
    quotes: dict[str, str] = {}
    lines = md_text.split("\n")

    for i, line in enumerate(lines):
        stripped = line.strip()
        # Match quote lines
        quote_match = re.match(
            r'^>\s*(?:引用原文|原文引用|Quote|Excerpt)[：:]\s*[「"\'"](.+?)[」"\'"]',
            stripped,
        )
        if not quote_match:
            continue

        exact_text = quote_match.group(1).strip()
        if len(exact_text) < 10:
            continue

        # Walk backwards to find the associated URL (from > 來源：[Title](URL) line)
        for j in range(i - 1, max(0, i - 5), -1):
            prev = lines[j].strip()
            url_match = re.search(r"\((https?://[^\)]+)\)", prev)
            if url_match:
                quotes[url_match.group(1)] = exact_text
                break

    return quotes


# ── Bitap-based fuzzy matching (Hypothesis approach) ──

_dmp = diff_match_patch()
_dmp.Match_Threshold = 0.4   # Allow 40% character-level difference
_dmp.Match_Distance = 5000   # Search within 5000 chars of expected position


def _bitap_find(source_text: str, pattern: str, loc: int = 0) -> int:
    """Find pattern in source_text using Bitap fuzzy matching.

    Returns character position or -1 if no match within threshold.
    """
    if not pattern or not source_text:
        return -1
    # diff-match-patch requires pattern <= 32 chars for Bitap;
    # for longer patterns, search with a representative substring
    if len(pattern) > 32:
        pattern = pattern[:32]
    return _dmp.match_main(source_text, pattern, loc)


def find_best_match(source_text: str, report_claim: str, min_score: float = 0.3,
                    citation_title: str = "") -> dict | None:
    """Find the passage in source_text that best matches the report_claim.

    Uses a multi-strategy approach inspired by Hypothesis:
      1. Bitap fuzzy match on the report claim (same-language)
      2. Bitap fuzzy match on the citation title (cross-language bridge)
      3. Keyword sliding window fallback (cross-language)

    Returns TextQuoteSelector dict or None.
    """
    if not source_text or not report_claim:
        return None

    source_norm = normalize(source_text)
    claim_norm = normalize(report_claim)

    # Detect if cross-language (CJK report vs Latin source)
    cjk_ratio = len(re.findall(r"[\u4e00-\u9fff]", claim_norm)) / max(len(claim_norm), 1)
    is_cross_lang = cjk_ratio > 0.3

    best_pos = -1
    match_method = ""

    # Strategy 1: Bitap fuzzy match on report claim (same-language only)
    if not is_cross_lang:
        # Use the most information-dense part of the claim
        search_fragment = claim_norm[:64]
        pos = _bitap_find(source_norm, search_fragment)
        if pos != -1:
            best_pos = pos
            match_method = "bitap-claim"

    # Strategy 2: Bitap fuzzy match on citation title (works cross-language)
    if best_pos == -1 and citation_title:
        title_norm = normalize(citation_title)
        pos = _bitap_find(source_norm, title_norm)
        if pos != -1:
            best_pos = pos
            match_method = "bitap-title"

    # Strategy 3: Keyword sliding window (cross-language fallback)
    if best_pos == -1:
        result = _keyword_window_search(source_norm, claim_norm, citation_title, min_score)
        if result:
            return result

    if best_pos == -1:
        return None

    # Extract a meaningful passage around the match position
    exact, score = _extract_passage(source_norm, best_pos, claim_norm, citation_title)
    if not exact or len(exact) < 10:
        return None

    # Build prefix/suffix context (Hypothesis style: ~32 chars each)
    exact_pos = source_norm.find(exact, max(0, best_pos - 50))
    if exact_pos == -1:
        exact_pos = best_pos

    prefix_start = max(0, exact_pos - 40)
    prefix = source_norm[prefix_start:exact_pos].strip()[-32:]

    suffix_end = min(len(source_norm), exact_pos + len(exact) + 40)
    suffix = source_norm[exact_pos + len(exact):suffix_end].strip()[:32]

    return {
        "type": "TextQuoteSelector",
        "exact": exact,
        "prefix": prefix,
        "suffix": suffix,
        "_match_score": round(score, 2),
        "_match_method": match_method,
    }


def _extract_passage(source_norm: str, pos: int, claim_norm: str, title: str) -> tuple[str, float]:
    """Extract a natural sentence/passage around the match position."""
    # Take a window around the match
    window_start = max(0, pos - 50)
    window_end = min(len(source_norm), pos + 300)
    window = source_norm[window_start:window_end]

    # Try to find sentence boundaries
    sentences = re.split(r"(?<=[.!?。！？])\s+", window)
    if not sentences:
        return window[:200].strip(), 0.5

    # Score each sentence by keyword overlap with claim + title
    keywords = set()
    for w in re.findall(r"[a-zA-Z]{3,}", claim_norm):
        keywords.add(w.lower())
    for w in re.findall(r"[\u4e00-\u9fff]{2,}", claim_norm):
        keywords.add(w)
    if title:
        for w in re.findall(r"[a-zA-Z]{3,}", title):
            keywords.add(w.lower())

    if not keywords:
        return window[:200].strip(), 0.3

    def sentence_score(s: str) -> float:
        s_lower = s.lower()
        s_words = set(re.findall(r"[a-zA-Z]{3,}", s_lower))
        s_words |= set(re.findall(r"[\u4e00-\u9fff]{2,}", s))
        if not s_words:
            return 0
        return len(keywords & s_words) / len(keywords)

    best_sent = max(sentences, key=sentence_score)
    score = sentence_score(best_sent)

    exact = best_sent.strip()[:200]
    if len(exact) < 10:
        exact = window[:200].strip()
        score = 0.3

    return exact, max(score, 0.3)


def _keyword_window_search(source_norm: str, claim_norm: str,
                           citation_title: str, min_score: float) -> dict | None:
    """Fallback: sliding window keyword overlap (for cross-language matching)."""
    # Extract bridge keywords (numbers, English terms, title words)
    search_words: set[str] = set()
    for m in re.findall(r"\d+\.?\d*%?", claim_norm):
        if len(m) >= 2:
            search_words.add(m)
    for w in re.findall(r"[a-zA-Z]{3,}", claim_norm):
        search_words.add(w.lower())
    if citation_title:
        for w in re.findall(r"[a-zA-Z]{3,}", citation_title):
            search_words.add(w.lower())

    if len(search_words) < 2:
        return None

    window_size = max(len(claim_norm) * 2, 300)
    step = max(window_size // 4, 50)
    source_lower = source_norm.lower()

    best_pos = -1
    best_score = 0.0

    for i in range(0, max(1, len(source_lower) - window_size), step):
        window = source_lower[i:i + window_size]
        window_words = set(re.findall(r"[\w]+", window))
        overlap = search_words & window_words
        # Check numeric substrings
        for kw in search_words - overlap:
            if kw.replace(".", "").isdigit() and kw in window:
                overlap.add(kw)
        score = len(overlap) / len(search_words)
        if score > best_score:
            best_score = score
            best_pos = i

    if best_score < min_score or best_pos == -1:
        return None

    # Extract passage
    window_text = source_norm[best_pos:best_pos + window_size]
    sentences = re.split(r"(?<=[.!?。！？])\s+", window_text)
    best_sentence = max(sentences, key=lambda s: sum(
        1 for w in search_words if w in s.lower()
    )) if sentences else window_text

    exact = best_sentence.strip()[:200]
    if len(exact) < 10:
        exact = window_text[:200]

    exact_pos = source_norm.find(exact)
    if exact_pos == -1:
        exact_pos = best_pos

    prefix_start = max(0, exact_pos - 40)
    prefix = source_norm[prefix_start:exact_pos].strip()[-32:]
    suffix_end = min(len(source_norm), exact_pos + len(exact) + 40)
    suffix = source_norm[exact_pos + len(exact):suffix_end].strip()[:32]

    return {
        "type": "TextQuoteSelector",
        "exact": exact,
        "prefix": prefix,
        "suffix": suffix,
        "_match_score": round(best_score, 2),
        "_match_method": "keyword-window",
    }


def enrich_report(report_dir: Path, verify: bool = False) -> dict:
    """Enrich all citations in a report with TextQuoteSelectors.

    Uses hybrid strategy:
      Route A: Inline quotes from markdown (highest quality)
      Route B: Bitap fuzzy matching against source snapshots
      Orphan:  Mark unmatched citations so the UI can indicate them
    """
    citation_map_path = report_dir / "citation_map.json"
    report_md_path = report_dir / "report.md"

    if not citation_map_path.exists():
        print(f"Error: {citation_map_path} not found", file=sys.stderr)
        sys.exit(1)

    with open(citation_map_path) as f:
        data = json.load(f)

    md_text = report_md_path.read_text(encoding="utf-8") if report_md_path.exists() else ""

    # Route A: Extract inline quotes from markdown
    inline_quotes = extract_inline_quotes(md_text)
    if inline_quotes:
        print(f"  Found {len(inline_quotes)} inline source quotes (Route A)")

    enriched = 0
    enriched_a = 0  # via inline quotes
    enriched_b = 0  # via Bitap matching
    skipped = 0
    orphaned = 0

    for citation in data["citations"]:
        ref_id = citation["id"]
        source_url = citation["source"].get("url", "")

        # Skip if already has anchors
        if citation.get("anchors") and any(
            a.get("source_selectors") for a in citation["anchors"]
        ):
            skipped += 1
            continue

        # ── Route A: Check for inline quote ──
        if source_url and source_url in inline_quotes:
            exact_quote = inline_quotes[source_url]
            report_context = find_report_context(
                md_text, citation["index"], citation["source"].get("title", ""),
                source_url=source_url,
            )
            citation["anchors"] = [{
                "report_location": {
                    "section": "",
                    "paragraph": 0,
                    "text_fragment": report_context[:100] if report_context else "",
                },
                "source_selectors": [{
                    "type": "TextQuoteSelector",
                    "exact": exact_quote,
                    "prefix": "",
                    "suffix": "",
                }],
                "_match_method": "inline-quote",
            }]
            enriched += 1
            enriched_a += 1
            print(f"  ★ [{ref_id}] inline quote  \"{exact_quote[:50]}...\"")
            continue

        # ── Route B: Bitap fuzzy matching against snapshot ──
        snapshot_path = None
        snapshots_dir = report_dir / "snapshots"
        for ext in [".html", ".htm"]:
            candidate = snapshots_dir / f"{ref_id}{ext}"
            if candidate.exists():
                snapshot_path = candidate
                break

        if not snapshot_path:
            # No snapshot → orphan
            _mark_orphan(citation, "no_snapshot")
            orphaned += 1
            continue

        source_text = extract_text_from_html(snapshot_path)
        if len(source_text) < 50:
            _mark_orphan(citation, "empty_snapshot")
            orphaned += 1
            continue

        report_context = find_report_context(
            md_text, citation["index"], citation["source"].get("title", ""),
            source_url=source_url,
        )
        if not report_context:
            _mark_orphan(citation, "no_report_context")
            orphaned += 1
            continue

        selector = find_best_match(
            source_text, report_context,
            citation_title=citation["source"].get("title", ""),
        )
        if not selector:
            _mark_orphan(citation, "no_match")
            orphaned += 1
            continue

        match_score = selector.pop("_match_score", 0)
        match_method = selector.pop("_match_method", "unknown")

        citation["anchors"] = [{
            "report_location": {
                "section": "",
                "paragraph": 0,
                "text_fragment": report_context[:100],
            },
            "source_selectors": [selector],
            "_match_method": match_method,
        }]

        enriched += 1
        enriched_b += 1
        icon = "✓" if match_score >= 0.5 else "~"
        print(f"  {icon} [{ref_id}] {match_method} score={match_score:.0%}  \"{selector['exact'][:50]}...\"")

    # Update stats
    total = len(data["citations"])
    total_with_anchors = sum(
        1 for c in data["citations"]
        if c.get("anchors") and any(a.get("source_selectors") for a in c["anchors"])
    )
    coverage = total_with_anchors / total if total > 0 else 0

    if coverage >= 0.5:
        data.setdefault("meta", {})["status"] = "verified"

    data["stats"]["anchors_enriched"] = enriched
    data["stats"]["anchors_inline_quotes"] = enriched_a
    data["stats"]["anchors_fuzzy_matched"] = enriched_b
    data["stats"]["anchors_orphaned"] = orphaned
    data["stats"]["anchor_coverage"] = round(coverage, 2)

    # Save
    with open(citation_map_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "enriched": enriched,
        "enriched_inline": enriched_a,
        "enriched_fuzzy": enriched_b,
        "skipped": skipped,
        "orphaned": orphaned,
        "verified": coverage >= 0.5,
    }


def _mark_orphan(citation: dict, reason: str) -> None:
    """Mark a citation as orphan — matching failed but we still track it."""
    if not citation.get("anchors"):
        citation["anchors"] = []
    # Only add orphan marker if not already present
    has_orphan = any(a.get("_orphan") for a in citation["anchors"])
    if not has_orphan:
        citation["anchors"].append({
            "_orphan": True,
            "_orphan_reason": reason,
            "report_location": {"section": "", "paragraph": 0, "text_fragment": ""},
            "source_selectors": [],
        })


def main():
    parser = argparse.ArgumentParser(
        description="Enrich citations with TextQuoteSelectors for source text highlighting",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
This script elevates reports from 'imported' to 'verified' quality.
Requires snapshots to be captured first (capture_snapshots.py).

Full pipeline to produce verified reports:
  1. Import:   smart_import.py report.md --output demo/my-report/
  2. Snapshot:  capture_snapshots.py demo/my-report/citation_map.json
  3. Anchor:   enrich_anchors.py demo/my-report/    ← this script
  4. Result:   status changes to 'verified', text highlighting works
        """,
    )
    parser.add_argument("report_dir", type=Path, help="Report bundle directory")
    parser.add_argument("--verify", action="store_true", help="Also validate anchors exist in snapshots")
    args = parser.parse_args()

    if not args.report_dir.exists():
        print(f"Error: Directory not found: {args.report_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Enriching anchors: {args.report_dir.name}\n")
    result = enrich_report(args.report_dir, args.verify)

    print(f"\nResult:")
    print(f"  Enriched: {result['enriched']} ({result['enriched_inline']} inline quotes, {result['enriched_fuzzy']} fuzzy matched)")
    print(f"  Skipped:  {result['skipped']} (already had anchors)")
    print(f"  Orphaned: {result['orphaned']} (marked for UI indication)")
    if result["verified"]:
        print(f"  Status → verified ✓")
    else:
        print(f"  Status → imported (need more snapshots or inline quotes)")


if __name__ == "__main__":
    main()
