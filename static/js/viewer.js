/**
 * Source-Linked Report Viewer — Frontend Logic v2
 * Features: citation click, source highlighting, keyboard nav, mini-map
 */

let citationMap = null;
let activeCitationId = null;
let citationOrder = []; // ordered list of ref IDs for keyboard nav

// ── Initialization ──

async function init() {
  const [reportData, citationData] = await Promise.all([
    fetch(`/api/report/${REPORT_ID}`).then(r => r.json()),
    fetch(`/api/citations/${REPORT_ID}`).then(r => r.json()),
  ]);

  citationMap = citationData;
  citationOrder = citationMap.citations.map(c => c.id);

  // Detect view mode based on available sources
  const citationsWithUrl = citationMap.citations.filter(c => c.source?.url).length;
  const viewMode = citationsWithUrl > 0 ? "source" : "reader";

  // Update header
  document.getElementById("report-title").textContent = citationMap.title || REPORT_ID;
  const count = citationMap.stats?.total_citations || citationMap.citations?.length || 0;

  if (viewMode === "reader") {
    document.getElementById("citation-count").textContent = "閱讀模式";
    document.getElementById("citation-count").title = "此報告無外部來源可對照";
    enterReaderMode();
  } else {
    document.getElementById("citation-count").textContent = `${count} 引用`;
  }

  // Render report with citation links
  const html = transformCitations(reportData.html);
  document.getElementById("report-content").innerHTML = html;

  // Build citation list panel (only if sources exist)
  if (viewMode === "source") {
    buildCitationList();
    bindCitationEvents();
    initResizeHandle();
    initKeyboardNav();
    listenForHighlightResults();
  }
}

function enterReaderMode() {
  // Switch to full-width reading layout
  document.body.classList.add("reader-mode");

  // Hide source pane and resize handle
  const sourcePane = document.getElementById("source-pane");
  const resizeHandle = document.getElementById("resize-handle");
  const reportPane = document.getElementById("report-pane");
  const citationsBtn = document.getElementById("toggle-citations-btn");

  if (sourcePane) sourcePane.style.display = "none";
  if (resizeHandle) resizeHandle.style.display = "none";
  if (reportPane) reportPane.style.width = "100%";
  if (citationsBtn) citationsBtn.style.display = "none";

  // Update toolbar hint
  const hint = document.querySelector(".pane-hint");
  if (hint) hint.textContent = "閱讀模式 — 此報告無外部來源";
}

// ── Citation Transformation ──
// Supports three formats:
//   1. Numeric: [1], [@1] — standard academic style
//   2. Cortex: [VERIFIED: descriptor] — Glen Cortex pipeline format
//   3. Inline source: > 來源：[Title](URL) — ChatGPT / manual style
// All render as interactive citation links in the viewer.

function transformCitations(html) {
  // Pass 1: Replace numeric [n] / [@n] citations
  let result = html.replace(
    /\[@?(\d+)\]/g,
    (match, num) => {
      const citation = findCitation(parseInt(num));
      if (!citation) return match;
      const title = citation.source?.title || "";
      return `<span class="citation-link" data-ref-id="${citation.id}" data-index="${num}" title="${escapeAttr(title)}">${num}</span>`;
    }
  );

  // Pass 2: Replace [VERIFIED: descriptor] citations
  result = result.replace(
    /\[VERIFIED:\s*([^\]]+)\]/g,
    (match, descriptor) => {
      const citation = findCitationByDescriptor(descriptor.trim());
      if (!citation) return `<span class="verified-unlinked" title="來源未對應">${escapeHtml(match)}</span>`;
      const title = citation.source?.title || descriptor;
      return `<span class="citation-link citation-verified" data-ref-id="${citation.id}" data-index="${citation.index}" title="${escapeAttr(title)}"><span class="verified-badge">V</span>${citation.index}</span>`;
    }
  );

  // Pass 3: Transform inline source links in blockquote source lines
  // Pattern: <blockquote> containing 來源：... <a href="URL">Title</a>
  // The markdown renderer converts > 來源：[Title](URL) into <blockquote><p>來源：<a>...</a></p></blockquote>
  result = result.replace(
    /(<blockquote>\s*<p>(?:來源|Source)[：:]\s*)(.*?)(<\/p>\s*<\/blockquote>)/gi,
    (match, prefix, content, suffix) => {
      // Replace each <a href="URL">Title</a> with a citation link
      const transformed = content.replace(
        /<a\s+href="(https?:\/\/[^"]+)"[^>]*>([^<]+)<\/a>/g,
        (aMatch, url, title) => {
          const citation = findCitationByUrl(url);
          if (!citation) return aMatch; // keep original link if no match
          return `<span class="citation-link citation-source" data-ref-id="${citation.id}" data-index="${citation.index}" title="${escapeAttr(url)}">${citation.index}. ${escapeHtml(title)}</span>`;
        }
      );
      return `<div class="source-line">${prefix}${transformed}${suffix}</div>`;
    }
  );

  return result;
}

function findCitation(index) {
  if (!citationMap?.citations) return null;
  return citationMap.citations.find(c => c.index === index);
}

function findCitationByDescriptor(descriptor) {
  if (!citationMap?.citations) return null;
  const desc = descriptor.toLowerCase();

  // Strategy 1: Exact match on meta.verified_label (set by cortex_to_slv.py)
  let found = citationMap.citations.find(c =>
    c.meta?.verified_label?.toLowerCase() === desc
  );
  if (found) return found;

  // Strategy 2: Fuzzy match — descriptor words appear in source title
  const words = desc.split(/[\s,+]+/).filter(w => w.length >= 2);
  let bestMatch = null;
  let bestScore = 0;

  for (const c of citationMap.citations) {
    const title = (c.source?.title || "").toLowerCase();
    const url = (c.source?.url || "").toLowerCase();
    const combined = `${title} ${url}`;

    const matchCount = words.filter(w => combined.includes(w)).length;
    const score = matchCount / words.length;

    if (score > bestScore && score >= 0.5) {
      bestScore = score;
      bestMatch = c;
    }
  }

  return bestMatch;
}

function findCitationByUrl(url) {
  if (!citationMap?.citations) return null;
  const normalized = url.replace(/\/+$/, "").toLowerCase();

  // Exact URL match
  let found = citationMap.citations.find(c =>
    (c.source?.url || "").replace(/\/+$/, "").toLowerCase() === normalized
  );
  if (found) return found;

  // Partial match: same domain + path
  try {
    const target = new URL(url);
    found = citationMap.citations.find(c => {
      if (!c.source?.url) return false;
      try {
        const src = new URL(c.source.url);
        return src.hostname === target.hostname && src.pathname === target.pathname;
      } catch { return false; }
    });
  } catch { /* invalid URL */ }

  return found || null;
}

function escapeAttr(str) {
  return str.replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

// ── Citation List Panel ──

function buildCitationList() {
  const container = document.getElementById("citation-list");
  if (!container) return;

  const items = citationMap.citations.map(c => {
    const typeIcon = { webpage: "🌐", pdf: "📄", video: "🎬", dataset: "📊" }[c.source?.type] || "📎";
    const hasSnapshot = c.snapshot?.file ? "has-snapshot" : "";
    return `
      <div class="citation-list-item ${hasSnapshot}" data-ref-id="${c.id}" data-index="${c.index}">
        <span class="cl-index">${c.index}</span>
        <span class="cl-icon">${typeIcon}</span>
        <div class="cl-info">
          <div class="cl-title">${escapeHtml(c.source?.title || "Unknown")}</div>
          <div class="cl-url">${escapeHtml(c.source?.author || "")}</div>
        </div>
      </div>
    `;
  }).join("");

  container.innerHTML = items;

  // Bind clicks on list items
  container.querySelectorAll(".citation-list-item").forEach(item => {
    item.addEventListener("click", () => {
      const refId = item.dataset.refId;
      loadSource(refId);
      setActiveCitation(refId);
    });
  });
}

// ── Citation Events ──

function bindCitationEvents() {
  document.querySelectorAll(".citation-link").forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const refId = link.dataset.refId;
      loadSource(refId);
      setActiveCitation(refId);
    });

    link.addEventListener("mouseenter", (e) => showTooltip(e, link));
    link.addEventListener("mouseleave", hideTooltip);
  });
}

function setActiveCitation(refId) {
  activeCitationId = refId;

  // Update report citation highlights
  document.querySelectorAll(".citation-link.active").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(`.citation-link[data-ref-id="${refId}"]`).forEach(el => el.classList.add("active"));

  // Update citation list highlight
  document.querySelectorAll(".citation-list-item.active").forEach(el => el.classList.remove("active"));
  document.querySelectorAll(`.citation-list-item[data-ref-id="${refId}"]`).forEach(el => {
    el.classList.add("active");
    el.scrollIntoView({ behavior: "smooth", block: "nearest" });
  });
}

// ── Source Loading with Highlighting ──

async function loadSource(refId) {
  const citation = citationMap.citations.find(c => c.id === refId);
  if (!citation) return;

  activeCitationId = refId;
  const sourceContent = document.getElementById("source-content");
  const sourceLabel = document.getElementById("source-label");
  const externalLink = document.getElementById("source-external-link");

  // Update toolbar
  sourceLabel.textContent = citation.source?.title || "來源檢視";
  if (citation.source?.url) {
    externalLink.href = citation.source.url;
    externalLink.style.display = "inline";
  } else {
    externalLink.style.display = "none";
  }

  const sourceType = citation.source?.type || "webpage";

  // Handle video
  if (sourceType === "video" && citation.media) {
    loadVideo(citation, sourceContent);
    return;
  }

  // Try local snapshot first, then proxy
  const snapshotUrl = `/api/snapshot/${REPORT_ID}/${refId}`;
  const proxyUrl = citation.source?.url ? `/api/proxy?url=${encodeURIComponent(citation.source.url)}` : null;

  let srcUrl;
  try {
    const check = await fetch(snapshotUrl, { method: "HEAD" });
    srcUrl = check.ok ? snapshotUrl : proxyUrl;
  } catch {
    srcUrl = proxyUrl;
  }

  if (!srcUrl) {
    sourceContent.innerHTML = `<div class="source-placeholder"><p>無法載入此來源</p></div>`;
    sourceContent.className = "pane-content";
    return;
  }

  // Get anchor info for highlighting
  const anchor = citation.anchors?.[0];
  const isOrphan = anchor?._orphan === true;
  const quoteSelector = anchor?.source_selectors?.find(s => s.type === "TextQuoteSelector");

  // Build anchor status indicator
  let anchorStatusHtml = "";
  if (quoteSelector) {
    anchorStatusHtml = '<span class="anchor-status" id="anchor-status">⏳ 定位中...</span>';
  } else if (isOrphan) {
    const reason = anchor?._orphan_reason || "";
    const reasonText = reason === "no_snapshot" ? "無快照" : reason === "no_match" ? "無法匹配" : "未錨定";
    anchorStatusHtml = `<span class="anchor-status anchor-orphan" title="此引用無法自動定位到來源文字">⚠ ${reasonText}</span>`;
  }

  sourceContent.className = "pane-content has-iframe";
  sourceContent.innerHTML = `
    <div class="source-info-bar">
      <span class="source-title">${escapeHtml(citation.source?.title || refId)}</span>
      <span class="source-type-badge">${sourceType}</span>
      ${anchorStatusHtml}
    </div>
    <iframe id="source-iframe" src="${srcUrl}" sandbox="allow-same-origin allow-scripts allow-popups"></iframe>
  `;

  // After iframe loads, send highlight message
  if (quoteSelector) {
    const iframe = document.getElementById("source-iframe");
    iframe.addEventListener("load", () => {
      setTimeout(() => {
        iframe.contentWindow.postMessage({
          type: "highlight-text",
          exact: quoteSelector.exact,
          prefix: quoteSelector.prefix || "",
          suffix: quoteSelector.suffix || "",
        }, "*");
      }, 300); // small delay for DOM readiness
    });
  }
}

function loadVideo(citation, container) {
  const media = citation.media;
  if (media.platform === "youtube" && media.video_id) {
    const start = media.timestamp || 0;
    const mins = Math.floor(start / 60);
    const secs = start % 60;
    container.className = "pane-content has-iframe";
    container.innerHTML = `
      <div class="source-info-bar">
        <span class="source-title">${escapeHtml(citation.source?.title || "")}</span>
        <span class="source-type-badge">video</span>
        <span class="anchor-status">⏱ ${mins}:${String(secs).padStart(2, "0")}</span>
      </div>
      <div style="padding: 24px;">
        <div class="video-container">
          <iframe src="https://www.youtube.com/embed/${media.video_id}?start=${start}&autoplay=1"
                  allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
      </div>
    `;
  } else {
    container.className = "pane-content";
    container.innerHTML = `<div class="source-placeholder"><p>不支援的影片平台: ${media.platform}</p></div>`;
  }
}

// ── Highlight Result Listener ──

function listenForHighlightResults() {
  window.addEventListener("message", (event) => {
    if (event.data?.type !== "highlight-result") return;
    const status = document.getElementById("anchor-status");
    if (!status) return;

    if (event.data.success) {
      status.textContent = "✓ 已定位";
      status.classList.add("anchor-success");
    } else {
      status.textContent = "✗ 未找到精確位置";
      status.classList.add("anchor-fail");
    }

    // Fade out after 3 seconds
    setTimeout(() => { status.style.opacity = "0.5"; }, 3000);
  });
}

// ── Tooltip ──

function showTooltip(event, link) {
  const refId = link.dataset.refId;
  const citation = citationMap.citations.find(c => c.id === refId);
  if (!citation) return;

  const tooltip = document.getElementById("citation-tooltip");
  const anchor = citation.anchors?.[0];
  const quoteSelector = anchor?.source_selectors?.find(s => s.type === "TextQuoteSelector");

  document.getElementById("tooltip-title").textContent = citation.source?.title || "Unknown";
  document.getElementById("tooltip-url").textContent = citation.source?.url || "";
  document.getElementById("tooltip-type").textContent = citation.source?.type || "webpage";

  // Show anchor quote preview
  const quoteEl = document.getElementById("tooltip-quote");
  if (quoteEl && quoteSelector?.exact) {
    quoteEl.textContent = `"${quoteSelector.exact.slice(0, 120)}${quoteSelector.exact.length > 120 ? '...' : ''}"`;
    quoteEl.style.display = "block";
  } else if (quoteEl) {
    quoteEl.style.display = "none";
  }

  const rect = link.getBoundingClientRect();
  tooltip.style.left = `${Math.min(rect.left, window.innerWidth - 380)}px`;
  tooltip.style.top = `${rect.bottom + 8}px`;
  tooltip.style.display = "block";
}

function hideTooltip() {
  document.getElementById("citation-tooltip").style.display = "none";
}

// ── Resize Handle ──

function initResizeHandle() {
  const handle = document.getElementById("resize-handle");
  const leftPane = document.getElementById("report-pane");
  const container = document.querySelector(".split-container");
  let isResizing = false;

  handle.addEventListener("mousedown", (e) => {
    isResizing = true;
    handle.classList.add("active");
    document.body.style.cursor = "col-resize";
    document.body.style.userSelect = "none";
    e.preventDefault();
  });

  document.addEventListener("mousemove", (e) => {
    if (!isResizing) return;
    const containerRect = container.getBoundingClientRect();
    const newWidth = e.clientX - containerRect.left;
    const minWidth = 300;
    const maxWidth = containerRect.width - 300;

    if (newWidth >= minWidth && newWidth <= maxWidth) {
      leftPane.style.width = `${newWidth}px`;
    }
  });

  document.addEventListener("mouseup", () => {
    if (isResizing) {
      isResizing = false;
      handle.classList.remove("active");
      document.body.style.cursor = "";
      document.body.style.userSelect = "";
    }
  });
}

// ── Keyboard Navigation ──

function initKeyboardNav() {
  document.addEventListener("keydown", (e) => {
    // Escape: clear active citation, reset source pane
    if (e.key === "Escape") {
      document.querySelectorAll(".citation-link.active").forEach(el => el.classList.remove("active"));
      document.querySelectorAll(".citation-list-item.active").forEach(el => el.classList.remove("active"));
      activeCitationId = null;
      return;
    }

    // Left/Right arrow: navigate between citations
    if (e.key === "ArrowLeft" || e.key === "ArrowRight") {
      // Don't intercept if user is in an input field
      if (e.target.tagName === "INPUT" || e.target.tagName === "TEXTAREA") return;

      e.preventDefault();
      const currentIdx = activeCitationId ? citationOrder.indexOf(activeCitationId) : -1;
      let nextIdx;

      if (e.key === "ArrowRight") {
        nextIdx = currentIdx < citationOrder.length - 1 ? currentIdx + 1 : 0;
      } else {
        nextIdx = currentIdx > 0 ? currentIdx - 1 : citationOrder.length - 1;
      }

      const nextRefId = citationOrder[nextIdx];
      loadSource(nextRefId);
      setActiveCitation(nextRefId);

      // Scroll the report to show the citation
      const citLink = document.querySelector(`.citation-link[data-ref-id="${nextRefId}"]`);
      if (citLink) {
        citLink.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  });
}

// ── Start ──

init().catch(err => {
  console.error("Failed to initialize viewer:", err);
  document.getElementById("report-content").innerHTML = `<p style="color: #f85149;">載入失敗: ${err.message}</p>`;
});
