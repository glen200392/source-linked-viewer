"""Source-Linked Report Viewer — FastAPI Backend"""

import json
from pathlib import Path

import aiohttp
import markdown
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI(title="Source-Linked Report Viewer", version="0.2.0")

BASE_DIR = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "demo"

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# Script injected into snapshots for cross-frame text highlighting
HIGHLIGHT_INJECT_SCRIPT = """
<script>
(function() {
  window.addEventListener("message", function(event) {
    if (event.data?.type !== "highlight-text") return;

    // Clear previous highlights
    document.querySelectorAll(".slv-highlight").forEach(el => {
      const parent = el.parentNode;
      parent.replaceChild(document.createTextNode(el.textContent), el);
      parent.normalize();
    });

    const { exact, prefix, suffix } = event.data;
    if (!exact) return;

    const result = fuzzyFindText(document.body, exact, prefix, suffix);
    if (result) {
      highlightRange(result.range);
      result.range.startContainer.parentElement.scrollIntoView({
        behavior: "smooth", block: "center"
      });
      // Notify parent that highlight succeeded
      window.parent.postMessage({ type: "highlight-result", success: true }, "*");
    } else {
      window.parent.postMessage({ type: "highlight-result", success: false }, "*");
    }
  });

  function fuzzyFindText(root, exact, prefix, suffix) {
    const text = root.textContent || "";
    const normalizedExact = normalizeWS(exact);
    const normalizedText = normalizeWS(text);

    // Try exact match first
    let idx = normalizedText.indexOf(normalizedExact);

    // If exact match fails, try case-insensitive
    if (idx === -1) {
      idx = normalizedText.toLowerCase().indexOf(normalizedExact.toLowerCase());
    }

    // If still fails, try word-level fuzzy match
    if (idx === -1) {
      idx = fuzzyMatch(normalizedText, normalizedExact);
    }

    if (idx === -1) return null;

    // If we have prefix/suffix, refine among multiple matches
    if (prefix || suffix) {
      const allMatches = findAllOccurrences(normalizedText, normalizedExact);
      if (allMatches.length > 1) {
        idx = pickBestMatch(normalizedText, allMatches, normalizedExact.length, prefix, suffix);
      }
    }

    // Convert text offset to DOM range
    const range = offsetToRange(root, idx, idx + normalizedExact.length);
    return range ? { range } : null;
  }

  function normalizeWS(s) {
    return s.replace(/\\s+/g, " ").trim();
  }

  function findAllOccurrences(text, query) {
    const results = [];
    const lower = text.toLowerCase();
    const q = query.toLowerCase();
    let pos = 0;
    while ((pos = lower.indexOf(q, pos)) !== -1) {
      results.push(pos);
      pos += 1;
    }
    return results;
  }

  function pickBestMatch(text, positions, matchLen, prefix, suffix) {
    let bestScore = -1;
    let bestPos = positions[0];
    for (const pos of positions) {
      let score = 0;
      if (prefix) {
        const before = text.slice(Math.max(0, pos - prefix.length - 10), pos);
        if (before.toLowerCase().includes(normalizeWS(prefix).toLowerCase())) score += 20;
      }
      if (suffix) {
        const after = text.slice(pos + matchLen, pos + matchLen + (suffix.length || 0) + 10);
        if (after.toLowerCase().includes(normalizeWS(suffix).toLowerCase())) score += 20;
      }
      if (score > bestScore) { bestScore = score; bestPos = pos; }
    }
    return bestPos;
  }

  function fuzzyMatch(text, query) {
    // Extract key words (3+ chars) and find region where most appear
    const words = query.toLowerCase().split(/\\s+/).filter(w => w.length >= 3);
    if (words.length === 0) return -1;

    const lower = text.toLowerCase();
    let bestPos = -1, bestCount = 0;
    const windowSize = query.length * 2;

    for (let i = 0; i < lower.length - windowSize; i += Math.floor(windowSize / 4)) {
      const window = lower.slice(i, i + windowSize);
      const count = words.filter(w => window.includes(w)).length;
      if (count > bestCount && count >= Math.ceil(words.length * 0.6)) {
        bestCount = count;
        bestPos = i;
      }
    }
    return bestPos;
  }

  function offsetToRange(root, startOffset, endOffset) {
    const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
    let charCount = 0;
    let startNode, startOff, endNode, endOff;

    while (walker.nextNode()) {
      const node = walker.currentNode;
      // Use normalized text length for matching
      const rawText = node.textContent;
      const len = rawText.length;

      if (!startNode && charCount + len > startOffset) {
        startNode = node;
        startOff = startOffset - charCount;
      }
      if (charCount + len >= endOffset) {
        endNode = node;
        endOff = endOffset - charCount;
        break;
      }
      charCount += len;
    }

    if (!startNode || !endNode) return null;

    try {
      const range = document.createRange();
      range.setStart(startNode, Math.min(startOff, startNode.length));
      range.setEnd(endNode, Math.min(endOff, endNode.length));
      return range;
    } catch(e) { return null; }
  }

  function highlightRange(range) {
    // Use multiple spans for ranges that cross element boundaries
    const frag = range.cloneContents();
    const wrapper = document.createElement("mark");
    wrapper.className = "slv-highlight";
    wrapper.style.cssText = "background: #fef08a; color: #1a1a1a; padding: 2px 0; border-radius: 2px; transition: background 0.3s;";

    try {
      range.surroundContents(wrapper);
    } catch(e) {
      // Range crosses element boundaries — highlight start container only
      const text = range.toString();
      const startContainer = range.startContainer;
      if (startContainer.nodeType === Node.TEXT_NODE) {
        const mark = document.createElement("mark");
        mark.className = "slv-highlight";
        mark.style.cssText = "background: #fef08a; color: #1a1a1a; padding: 2px 0; border-radius: 2px;";
        range.surroundContents(mark);
      }
    }
  }
})();
</script>
"""


def discover_reports() -> list[dict]:
    """Scan for report bundles with full catalog metadata."""
    reports = []
    for report_dir in sorted(REPORTS_DIR.iterdir()):
        if not report_dir.is_dir():
            continue
        report_md = report_dir / "report.md"
        citation_map_file = report_dir / "citation_map.json"
        if report_md.exists() and citation_map_file.exists():
            with open(citation_map_file) as f:
                data = json.load(f)
            meta = data.get("meta", {})
            reports.append({
                "id": report_dir.name,
                "title": data.get("title", report_dir.name),
                "generated_at": data.get("generated_at", ""),
                "stats": data.get("stats", {}),
                "tags": meta.get("tags", []),
                "category": meta.get("category", "未分類"),
                "status": meta.get("status", "draft"),
                "summary": meta.get("summary", ""),
                "import_method": meta.get("import_method", ""),
            })
    # Sort by date, newest first
    reports.sort(key=lambda r: r.get("generated_at", ""), reverse=True)
    return reports


@app.get("/api/catalog")
async def get_catalog():
    """Return the full catalog with all reports and aggregated tags/categories."""
    reports = discover_reports()

    # Aggregate tags and categories
    all_tags: dict[str, int] = {}
    all_categories: dict[str, int] = {}
    for r in reports:
        for tag in r.get("tags", []):
            all_tags[tag] = all_tags.get(tag, 0) + 1
        cat = r.get("category", "未分類")
        all_categories[cat] = all_categories.get(cat, 0) + 1

    return {
        "reports": reports,
        "tags": dict(sorted(all_tags.items(), key=lambda x: -x[1])),
        "categories": dict(sorted(all_categories.items(), key=lambda x: -x[1])),
        "total": len(reports),
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    reports = discover_reports()

    # Aggregate for template
    all_tags: dict[str, int] = {}
    all_categories: dict[str, int] = {}
    for r in reports:
        for tag in r.get("tags", []):
            all_tags[tag] = all_tags.get(tag, 0) + 1
        cat = r.get("category", "未分類")
        all_categories[cat] = all_categories.get(cat, 0) + 1

    return templates.TemplateResponse("index.html", {
        "request": request,
        "reports": reports,
        "tags": sorted(all_tags.items(), key=lambda x: -x[1]),
        "categories": sorted(all_categories.items(), key=lambda x: -x[1]),
    })


@app.get("/report/{report_id}", response_class=HTMLResponse)
async def view_report(request: Request, report_id: str):
    report_dir = REPORTS_DIR / report_id
    if not report_dir.exists():
        raise HTTPException(404, "Report not found")
    return templates.TemplateResponse("viewer.html", {"request": request, "report_id": report_id})


@app.get("/api/report/{report_id}")
async def get_report(report_id: str):
    report_md = REPORTS_DIR / report_id / "report.md"
    if not report_md.exists():
        raise HTTPException(404, "Report not found")

    md_content = report_md.read_text(encoding="utf-8")
    md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "attr_list"])
    html_content = md.convert(md_content)

    return {"markdown": md_content, "html": html_content}


@app.get("/api/citations/{report_id}")
async def get_citations(report_id: str):
    citation_map = REPORTS_DIR / report_id / "citation_map.json"
    if not citation_map.exists():
        raise HTTPException(404, "Citation map not found")

    with open(citation_map) as f:
        return json.load(f)


@app.api_route("/api/snapshot/{report_id}/{ref_id}", methods=["GET", "HEAD"])
async def get_snapshot(report_id: str, ref_id: str):
    """Serve a local snapshot file with injected highlight script."""
    snapshots_dir = REPORTS_DIR / report_id / "snapshots"

    for ext in [".html", ".pdf", ".png", ".jpg"]:
        snapshot_file = snapshots_dir / f"{ref_id}{ext}"
        if snapshot_file.exists():
            # For HTML snapshots, inject the highlight script
            if ext == ".html":
                content = snapshot_file.read_text(encoding="utf-8")
                # Inject before </body> or at the end
                if "</body>" in content:
                    content = content.replace("</body>", f"{HIGHLIGHT_INJECT_SCRIPT}</body>")
                else:
                    content += HIGHLIGHT_INJECT_SCRIPT
                return HTMLResponse(content=content)
            return FileResponse(snapshot_file)

    raise HTTPException(404, f"Snapshot {ref_id} not found")


@app.get("/api/proxy")
async def proxy_url(url: str = Query(..., description="URL to proxy")):
    """Proxy external URLs to bypass iframe restrictions, with highlight script injected."""
    if not url.startswith(("http://", "https://")):
        raise HTTPException(400, "Invalid URL")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                content = await resp.read()
                content_type = resp.headers.get("Content-Type", "text/html")

                if "text/html" in content_type:
                    text = content.decode("utf-8", errors="replace")
                    base_tag = f'<base href="{url}" target="_blank">'
                    inject = base_tag + HIGHLIGHT_INJECT_SCRIPT
                    if "<head>" in text:
                        text = text.replace("<head>", f"<head>{inject}", 1)
                    elif "<html>" in text:
                        text = text.replace("<html>", f"<html><head>{inject}</head>", 1)
                    else:
                        text = inject + text
                    return HTMLResponse(content=text)

                return Response(content=content, media_type=content_type)
    except Exception as e:
        raise HTTPException(502, f"Failed to fetch: {e}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="127.0.0.1", port=8400, reload=True)
