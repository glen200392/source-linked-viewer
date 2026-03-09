#!/usr/bin/env python3
"""
Capture web page snapshots for citation sources using SingleFile CLI.

Reads a citation_map.json and captures snapshots for all webpage/pdf citations.
Stores snapshots in the report's snapshots/ directory.

Usage:
    python capture_snapshots.py <citation_map.json> [--singlefile-path PATH] [--timeout 30]

Prerequisites:
    - SingleFile CLI: npm install -g single-file-cli
    - Or: brew install single-file (if available)
    - Chrome/Chromium browser installed

If SingleFile is not available, falls back to a simple HTTP fetch.
"""

import argparse
import asyncio
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

import aiohttp


def find_singlefile() -> str | None:
    """Find SingleFile CLI binary."""
    # Check common locations
    candidates = [
        "single-file",
        "singlefile",
        shutil.which("single-file"),
        shutil.which("singlefile"),
    ]
    for candidate in candidates:
        if candidate and shutil.which(candidate):
            return candidate
    return None


async def capture_with_singlefile(url: str, output_path: Path, binary: str, timeout: int = 30) -> bool:
    """Capture a URL using SingleFile CLI."""
    try:
        proc = await asyncio.create_subprocess_exec(
            binary, url, str(output_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        if proc.returncode == 0 and output_path.exists():
            return True
        print(f"  SingleFile error: {stderr.decode()[:200]}", file=sys.stderr)
        return False
    except asyncio.TimeoutError:
        proc.kill()
        print(f"  SingleFile timeout for {url}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"  SingleFile error: {e}", file=sys.stderr)
        return False


async def capture_with_fetch(url: str, output_path: Path, timeout: int = 15) -> bool:
    """Fallback: capture using simple HTTP fetch."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout)) as resp:
                if resp.status != 200:
                    print(f"  HTTP {resp.status} for {url}", file=sys.stderr)
                    return False

                content = await resp.read()
                content_type = resp.headers.get("Content-Type", "")

                if "text/html" in content_type:
                    text = content.decode("utf-8", errors="replace")
                    # Inject base tag for relative URLs
                    base_tag = f'<base href="{url}">'
                    if "<head>" in text:
                        text = text.replace("<head>", f"<head>{base_tag}", 1)
                    else:
                        text = base_tag + text
                    output_path.write_text(text, encoding="utf-8")
                else:
                    output_path.write_bytes(content)

                return True
    except Exception as e:
        print(f"  Fetch error for {url}: {e}", file=sys.stderr)
        return False


async def capture_all(citation_map_path: Path, singlefile_binary: str | None, timeout: int):
    """Capture snapshots for all citations in the map."""
    with open(citation_map_path) as f:
        citation_map = json.load(f)

    report_dir = citation_map_path.parent
    snapshots_dir = report_dir / "snapshots"
    snapshots_dir.mkdir(exist_ok=True)

    citations = citation_map.get("citations", [])
    success_count = 0
    fail_count = 0

    for citation in citations:
        ref_id = citation["id"]
        source = citation.get("source", {})
        url = source.get("url", "")
        source_type = source.get("type", "webpage")

        # Skip video and already-captured
        if source_type == "video" or not url:
            continue

        ext = ".pdf" if source_type == "pdf" else ".html"
        output_path = snapshots_dir / f"{ref_id}{ext}"

        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"  [{ref_id}] Already captured, skipping")
            success_count += 1
            continue

        print(f"  [{ref_id}] Capturing: {url[:80]}...")

        # Try SingleFile first, then fallback
        captured = False
        if singlefile_binary and source_type != "pdf":
            captured = await capture_with_singlefile(url, output_path, singlefile_binary, timeout)

        if not captured:
            captured = await capture_with_fetch(url, output_path, timeout)

        if captured:
            size = output_path.stat().st_size
            file_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()

            # Update citation_map with snapshot info
            citation["snapshot"] = {
                "file": f"snapshots/{ref_id}{ext}",
                "format": "singlefile-html" if ext == ".html" else "pdf",
                "size_bytes": size,
                "hash": f"sha256:{file_hash[:16]}",
            }
            success_count += 1
            print(f"         Saved ({size:,} bytes)")
        else:
            fail_count += 1
            print(f"         FAILED")

    # Update stats and save
    citation_map["stats"]["snapshots_available"] = success_count
    citation_map["stats"]["snapshots_failed"] = fail_count

    with open(citation_map_path, "w", encoding="utf-8") as f:
        json.dump(citation_map, f, ensure_ascii=False, indent=2)

    print(f"\nDone: {success_count} captured, {fail_count} failed")
    return success_count, fail_count


def main():
    parser = argparse.ArgumentParser(description="Capture snapshots for citation sources")
    parser.add_argument("citation_map", type=Path, help="Path to citation_map.json")
    parser.add_argument("--singlefile-path", type=str, help="Path to SingleFile CLI binary")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per capture (seconds)")
    args = parser.parse_args()

    if not args.citation_map.exists():
        print(f"Error: File not found: {args.citation_map}", file=sys.stderr)
        sys.exit(1)

    singlefile = args.singlefile_path or find_singlefile()
    if singlefile:
        print(f"Using SingleFile: {singlefile}")
    else:
        print("SingleFile not found, using HTTP fetch fallback")

    print(f"Processing: {args.citation_map}\n")
    asyncio.run(capture_all(args.citation_map, singlefile, args.timeout))


if __name__ == "__main__":
    main()
