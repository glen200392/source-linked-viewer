# Source-Linked Report Viewer

A split-pane reading interface that displays AI-generated research reports alongside their original sources, enabling instant cross-reference and verification.

一個分欄式閱讀介面，將 AI 研究報告與原始來源並排顯示，支援即時交叉比對與驗證。

---

## The Problem

When AI generates research reports with citations, readers often face a disconnect between the report's claims and the actual sources. Verifying citations requires manually opening each URL, finding the relevant passage, and comparing it with the report. This friction reduces trust and slows down the review process.

## The Solution

Source-Linked Report Viewer bridges this gap with a two-pane interface:

- **Left pane**: The AI-generated research report with interactive citation markers
- **Right pane**: The original source material (web pages, PDFs, videos) with automatic text highlighting

Click any citation number in the report → the right pane loads the source and scrolls to the exact quoted passage.

## Features

- **Interactive citations** — Click `[1]`, `[2]` in the report to load corresponding sources
- **Auto text highlighting** — Uses fuzzy text matching (inspired by [Hypothesis](https://hypothes.is/)) to locate and highlight cited passages in the source
- **Local snapshots** — Sources are cached as single-file HTML for offline access and permanence
- **Proxy fallback** — If no snapshot exists, fetches the live page through a proxy to bypass iframe restrictions
- **Video support** — YouTube embeds with automatic timestamp seeking
- **Keyboard navigation** — `←` `→` to browse citations, `C` to toggle citation list, `Esc` to clear
- **Resizable panes** — Drag the divider to adjust the layout
- **Citation list panel** — Collapsible panel showing all sources with type indicators
- **Pipeline integration** — Scripts to auto-generate citation maps and capture snapshots
- **Dark theme** — Optimized for extended reading sessions

## Quick Start

### 1. Install

```bash
git clone https://github.com/glen200392/source-linked-viewer.git
cd source-linked-viewer

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Run

```bash
python server.py
# → Open http://127.0.0.1:8400
```

A demo report (Edge AI Trends 2026 Q1) is included so you can explore the interface immediately.

### 3. Add Your Own Reports

See [Usage Guide](#usage-guide) below for three different ways to import reports.

## Usage Guide

### Report Bundle Structure

Each report lives in a subdirectory under `demo/` with this structure:

```
demo/my-report/
├── report.md              ← Research report (Markdown)
├── citation_map.json      ← Citation metadata (auto-generated or manual)
├── snapshots/             ← Cached source pages (optional)
│   ├── ref-001.html
│   ├── ref-002.html
│   └── ref-003.pdf
└── media/                 ← Video thumbnails etc. (optional)
```

### Three Ways to Import Reports

#### Method A: Full Pipeline (Automated)

For integration with AI research pipelines (e.g., research-orchestrator, LangChain, CrewAI):

```bash
# Your pipeline produces: report.md + sources.json
# Bundle everything in one step:
python scripts/bundle_report.py report.md \
  --sources sources.json \
  --output demo/
```

This will:
1. Parse the report for `[n]` citations
2. Generate `citation_map.json` with full metadata and text anchors
3. Capture web page snapshots for each source
4. Validate the bundle

**`sources.json` format:**

```json
[
  {
    "index": 1,
    "url": "https://example.com/article",
    "title": "Article Title",
    "type": "webpage",
    "author": "Author Name",
    "publication_date": "2026-01",
    "accessed_at": "2026-03-09T10:00:00Z",
    "quote": "exact text cited in the report",
    "quote_prefix": "text before the quote",
    "quote_suffix": "text after the quote"
  }
]
```

#### Method B: Markdown Only (Auto-Extract)

If you only have a `report.md` with inline URLs or reference-style links:

```bash
# Auto-extracts URLs from markdown links near [n] references
python scripts/generate_citation_map.py report.md --output demo/my-report/

# Copy your report
cp report.md demo/my-report/

# Optionally capture snapshots
python scripts/capture_snapshots.py demo/my-report/citation_map.json
```

**Supported markdown patterns for auto-extraction:**

```markdown
According to the study [1](https://example.com/study)...    # inline link
See the analysis [2] for details...

[1]: https://example.com/study "Study Title"                 # reference-style
[2]: https://example.com/analysis
```

#### Method C: Manual Setup

Create the files manually for full control:

1. Place `report.md` in `demo/my-report/`
2. Create `citation_map.json` (see [Citation Map Schema](#citation-map-schema))
3. Optionally add HTML snapshots in `snapshots/`

### Workflow Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Your Research                          │
│                                                          │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────────┐  │
│  │ AI Pipeline  │   │ Manual Write │   │ External Tool│  │
│  │ (automated)  │   │ (markdown)   │   │ (any source) │  │
│  └──────┬──────┘   └──────┬───────┘   └──────┬───────┘  │
│         │                  │                   │          │
│         ▼                  ▼                   ▼          │
│  report.md +         report.md            report.md      │
│  sources.json        (with URLs)          (plain text)   │
└────┬────────────────────┬─────────────────────┬──────────┘
     │                    │                     │
     ▼                    ▼                     ▼
┌─────────────┐   ┌──────────────┐   ┌──────────────────┐
│ Method A    │   │ Method B     │   │ Method C         │
│ bundle_     │   │ generate_    │   │ Manual           │
│ report.py   │   │ citation_    │   │ citation_map.json│
│             │   │ map.py       │   │                  │
└──────┬──────┘   └──────┬───────┘   └────────┬─────────┘
       │                  │                    │
       ▼                  ▼                    ▼
┌──────────────────────────────────────────────────────────┐
│              demo/my-report/                              │
│  ├── report.md                                           │
│  ├── citation_map.json                                   │
│  └── snapshots/  (optional)                              │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
                 http://127.0.0.1:8400
                 Source-Linked Viewer
```

## Citation Map Schema

The `citation_map.json` connects report citations to their sources:

```jsonc
{
  "$schema": "source-linked-viewer/citation-map/v1",
  "title": "Report Title",
  "report_id": "my-report",
  "generated_at": "2026-03-09T14:30:00Z",
  "citations": [
    {
      "id": "ref-001",
      "index": 1,
      "source": {
        "url": "https://example.com/article",
        "title": "Article Title",
        "type": "webpage",           // webpage | pdf | video | dataset
        "author": "Author Name",
        "accessed_at": "2026-03-09T10:00:00Z"
      },
      "snapshot": {
        "file": "snapshots/ref-001.html",
        "format": "singlefile-html"
      },
      "anchors": [
        {
          "report_location": {
            "section": "2.1",
            "text_fragment": "the relevant claim in the report"
          },
          "source_selectors": [
            {
              "type": "TextQuoteSelector",     // W3C Web Annotation standard
              "exact": "the exact text in the source",
              "prefix": "text before ",         // context for fuzzy matching
              "suffix": " text after"
            }
          ]
        }
      ],
      "media": null
      // For video: { "platform": "youtube", "video_id": "...", "timestamp": 120 }
    }
  ]
}
```

### What Happens Without Sources?

| Scenario | Behavior |
|----------|----------|
| Has `sources.json` with URLs + quotes | Full experience: snapshot + text highlighting |
| Has `sources.json` with URLs only | Snapshot loads, but no text highlighting |
| Markdown has inline URLs near `[n]` | Auto-extracted: snapshot loads via proxy |
| No URLs at all | Citation markers show in report, right pane shows "source unavailable" |

The system degrades gracefully — you always get a readable report, with progressively richer source linking as more metadata is available.

## Text Anchoring

The text highlighting system uses a multi-strategy approach inspired by the [Hypothesis](https://hypothes.is/) annotation platform:

1. **Exact match** — First tries to find the exact quoted text
2. **Case-insensitive match** — Falls back if casing differs
3. **Fuzzy match** — Uses keyword-based sliding window (60% word coverage threshold)
4. **Context refinement** — When multiple matches exist, uses `prefix`/`suffix` to pick the best one

This ensures citations are highlighted correctly even when source pages have minor formatting differences from the quoted text.

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `→` | Next citation |
| `←` | Previous citation |
| `C` | Toggle citation list panel |
| `Esc` | Clear active citation |

## Tech Stack

- **Backend**: Python, FastAPI, uvicorn
- **Frontend**: Vanilla JS (no build step), CSS custom properties
- **PDF Rendering**: Browser-native (iframe)
- **Text Anchoring**: Custom fuzzy matching (injected via postMessage)
- **Snapshots**: SingleFile CLI (optional) or HTTP fetch fallback

## Project Structure

```
source-linked-viewer/
├── server.py                         # FastAPI backend
├── requirements.txt                  # Python dependencies
├── templates/
│   ├── index.html                    # Report listing page
│   └── viewer.html                   # Split-pane viewer
├── static/
│   ├── css/style.css                 # Dark theme styles
│   └── js/viewer.js                  # Frontend logic
├── scripts/
│   ├── generate_citation_map.py      # Parse report → citation_map.json
│   ├── capture_snapshots.py          # Download source snapshots
│   └── bundle_report.py             # One-step bundling pipeline
└── demo/
    └── edge-ai-2026/                 # Demo report bundle
        ├── report.md
        ├── citation_map.json
        └── snapshots/
```

## Roadmap

- [ ] PDF.js integration for in-pane PDF viewing with text layer highlighting
- [ ] Full-text search across all citations in a report
- [ ] Export verified report (report + inline source screenshots)
- [ ] Multi-report comparison view
- [ ] Integration with Zotero for citation import
- [ ] Browser extension for one-click snapshot capture
- [ ] WebSocket-based live updates during research pipeline execution

## Acknowledgments

Architecture informed by:

- **[OpenPaper](https://github.com/khoj-ai/openpaper)** — Split-pane research workbench with citation linking
- **[Hypothesis](https://github.com/hypothesis/client)** — Progressive text anchoring with fuzzy matching
- **[SingleFile](https://github.com/gildas-lormeau/SingleFile)** — Web page snapshot technology
- **[W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/)** — TextQuoteSelector standard

## License

[MIT](LICENSE)
