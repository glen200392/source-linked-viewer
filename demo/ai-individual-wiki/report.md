# 企業內部 AI-Individual Wiki 研究報告

**報告編號**: RR-2026-005
**日期**: 2026-03-05
**提案人**: Glen Ho, DTO
**分類**: Internal — Technology Advisory
**讀者**: DTO 管理層 / 資訊長 / IT 架構團隊
**前置分析**: RR-2026-004（AI 治理建議報告）、RR-2026-002（全球法規全景研究）

### 相關報告快速連結
| 報告 | 用途 |
|------|------|
| [RR-2026-002 全球法規全景研究](../exports/RR-2026-002_AI-Governance-Research.html) | PIPL/GDPR 合規要求參考 |
| [RR-2026-003 合規差距分析與路線圖](../exports/RR-2026-003_Compliance-Roadmap.html) | 資料主權與跨境限制 |
| [RR-2026-004 AI 治理建議報告](../exports/RR-2026-004_Recommendation-Report.html) | 高管建議報告 |
| **本報告（RR-2026-005）** | AI-Individual Wiki 技術研究 |

---

## 摘要

本報告研究在企業內部架設 **AI-Individual Wiki**（每位員工擁有 AI 增強型個人知識庫）的可行方案。涵蓋三大面向：

1. **開源專案清單** — 22 個 GitHub Stars ≥ 1,000 的候選專案，經實際驗證 star 數與活躍度
2. **自行開發架構設計** — 四層架構模型、技術選型、Multi-Tenant 隔離、RAG Pipeline 最佳實踐
3. **Build vs Buy 分析** — 針對致伸集團場景的推薦組合與行動建議

**核心結論**：推薦「分層 OSS 組裝」策略，以 Wiki/Editor（Outline 或 AppFlowy）+ AI RAG Layer（Dify 或 RAGFlow）+ 自架 Embedding/Vector Store 的組合，2 工程師 8-16 週可達 production。

---

## 1. 開源專案清單（GitHub Stars ≥ 1,000，2026-03-05 驗證）

> **驗證說明**：以下 star 數均於 2026-03-05 透過 GitHub API 與搜尋引擎交叉驗證。標註 `[VERIFIED]` 為誤差 ≤5% 的項目；`[CORRECTED]` 為經修正的項目。

### 1.1 AI 原生 RAG 平台（最適合「AI 知識庫」場景）

| # | 專案 | Stars | License | Tech Stack | 核心 AI 能力 | 自架 | 活躍度 |
|---|------|-------|---------|------------|-------------|------|--------|
| 1 | [Dify](https://github.com/langgenius/dify) | ~130k `[VERIFIED]` | Apache 2.0（SaaS 多租戶需商業授權）| Python + React | RAG pipeline + 50+ 工具 + agentic workflow | Docker/AWS | Active（Mar 2026）|
| 2 | [RAGFlow](https://github.com/infiniflow/ragflow) | ~74k `[VERIFIED]` | Apache 2.0 | Python + React | 深度文件理解 + GraphRAG + Agent memory | Docker | Active（2026 Roadmap 已公布）|
| 3 | [Lobe Chat](https://github.com/lobehub/lobe-chat) | ~71k `[CORRECTED: 原報 73k]` | Apache 2.0 | TypeScript + Next.js | Knowledge Base + 10,000+ MCP skills + 多 LLM | Docker/Vercel | Active（Mar 2026）|
| 4 | [AnythingLLM](https://github.com/Mintplex-Labs/anything-llm) | ~55k `[VERIFIED]` | MIT | React + Node.js | RAG + No-code agent + MCP + 100+ 文件格式 | Docker/Desktop | Active |
| 5 | [Flowise](https://github.com/FlowiseAI/Flowise) | ~49k `[VERIFIED]` | Apache 2.0（Enterprise 功能需商業授權）| TypeScript + Node.js | 視覺化拖拉 AI agent + RAG pipeline | Docker | Active |
| 6 | [Quivr](https://github.com/QuivrHQ/quivr) | ~39k `[VERIFIED]` | Apache 2.0 | Python | 多 LLM RAG + reranking | Self-host | ⚠️ 主 repo 放緩（2025.07），core pkg 仍更新 |
| 7 | [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) | ~34k `[CORRECTED: 原報 37k]` | Apache 2.0 | Python + FastAPI | 中文 LLM 優化 RAG（ChatGLM/Qwen）| Local | Active |
| 8 | [Khoj](https://github.com/khoj-ai/khoj) | ~33k `[VERIFIED]` | AGPL-3.0 | Python + TypeScript | 個人 AI 助理 + Obsidian/Notion 整合 | Docker | Active（Mar 2026）|
| 9 | [FastGPT](https://github.com/labring/FastGPT) | ~27k `[VERIFIED]` | Apache 2.0（SaaS 多租戶需商業授權）| TypeScript + Next.js | 視覺化 workflow + RAG + 多模態 | Docker | Active |
| 10 | [MaxKB](https://github.com/1Panel-dev/MaxKB) | ~20k `[VERIFIED]` | GPL-3.0 | Python/Django + Vue.js | RAG + MCP + 多模態 I/O | Docker | Active（v2.6.0）|
| 11 | [Onyx (Danswer)](https://github.com/onyx-dot-app/onyx) | ~18k `[VERIFIED]` | MIT（CE）/ 商業（EE）| Python + TypeScript + Go | 40+ 連接器 + hybrid search + KG | Docker/K8s | Active（Mar 2026）|
| 12 | [WeKnora (Tencent)](https://github.com/Tencent/WeKnora) | ~10k `[CORRECTED: 原報 13k]` | Apache 2.0（推測）| Go + React | Hybrid retrieval (keyword+vector+KG) | Docker/K8s | ⚠️ 活躍度降低（2025.09 後）|

#### License 風險提示

| 專案 | License 細節 | 企業影響 |
|------|-------------|---------|
| Dify | Apache 2.0 + Multi-tenant SaaS 限制 | 內部單租戶自架不受影響；若建 SaaS 對外服務需商業授權 |
| FastGPT | 同上 | 同上 |
| Flowise | Apache 2.0 + Enterprise 目錄（需 key 啟用）| CE 版功能足夠 POC；Enterprise 功能需付費 |
| Khoj | AGPL-3.0 | 衍生作品必須開源；若整合進內部系統需評估合規 |
| MaxKB | GPL-3.0 | 同上，強 copyleft |
| Onyx | MIT（CE）/ 商業（EE）| CE 版可自由使用；進階功能（SSO/RBAC）在 EE |

### 1.2 Wiki / PKM 平台（可加 AI 層）

| # | 專案 | Stars | License | Tech Stack | AI 能力 | 自架 | 活躍度 |
|---|------|-------|---------|------------|--------|------|--------|
| 13 | [AppFlowy](https://github.com/AppFlowy-IO/AppFlowy) | ~68k `[VERIFIED]` | AGPL-3.0 | Dart + Rust (Flutter) | AI 寫作 + LLM 整合 | Docker | Active |
| 14 | [AFFiNE](https://github.com/toeverything/AFFiNE) | ~64k `[VERIFIED]` | MIT（CE client）/ 商業（EE server）| TypeScript + React + Rust | Canvas AI + 文件生成 + 摘要 | Docker | Active（Mar 2026）|
| 15 | [PrivateGPT](https://github.com/zylon-ai/private-gpt) | ~57k `[VERIFIED]` | Apache 2.0 | Python + LlamaIndex | 100% 私有文件對話 | Local | ⚠️ 維護模式（原 imartinez/privateGPT 已轉移）|
| 16 | [SiYuan](https://github.com/siyuan-note/siyuan) | ~41k `[VERIFIED]` | AGPL-3.0 | TypeScript + Go | OpenAI 寫作 + OCR + 語意連結 | Self-hosted | Active（v3.5.9, Mar 2026）|
| 17 | [Logseq](https://github.com/logseq/logseq) | ~41k `[VERIFIED]` | AGPL-3.0 | Clojure + JS | Plugin 生態系 AI 擴充 | Local | Active（Dec 2025 release）|
| 18 | [Outline](https://github.com/outline/outline) | ~37k `[VERIFIED]` | BSL 1.1（⚠️ 非 OSI 認可開源）| TypeScript + React | MCP 支援 AI 助理整合 | Docker | Active（Mar 2026）|
| 19 | [TriliumNext](https://github.com/TriliumNext/Trilium) | ~35k `[VERIFIED]` | AGPL-3.0 | TypeScript + Node.js | Scripting 自動化（可擴充 AI）| Docker | Active |
| 20 | [Wiki.js](https://github.com/requarks/wiki) | ~28k `[VERIFIED]` | AGPL-3.0 | Node.js + Vue.js | Claude AI vision 開發中 | Docker/K8s | Active（Mar 2026）|
| 21 | [Docmost](https://github.com/docmost/docmost) | ~19k `[VERIFIED]` | AGPL-3.0（CE）/ 商業（EE）| TypeScript + Node.js | 即時協作（AI 可擴充）| Docker | Active（Mar 2026）|
| 22 | [BookStack](https://github.com/BookStackApp/BookStack) | ~18k `[VERIFIED]` | MIT | PHP + Laravel | 無原生 AI（API 可擴充）| Docker/LAMP | Active |

#### Wiki/PKM License 風險提示

| 專案 | License 細節 | 企業影響 |
|------|-------------|---------|
| Outline | BSL 1.1 — 4 年後轉 Apache 2.0 | 禁止競爭性 SaaS 使用；**內部自架使用不受限** |
| AFFiNE | MIT client / 商業 EE server | 自架免費版限 10 用戶 / 100 GB |
| AGPL 系列 | AppFlowy, SiYuan, Logseq, TriliumNext, Wiki.js, Docmost | 若修改原始碼並提供服務，須公開修改版原始碼 |
| BookStack | MIT | 最寬鬆，完全自由使用 |

---

## 2. 自行開發架構參考

### 2.1 四層架構模型

```
┌──────────────────────────────────────────────────────────────┐
│  Layer 4 — APPLICATION                                        │
│  Web UI (Next.js) / Chat / REST API / Embeddable Widget      │
├──────────────────────────────────────────────────────────────┤
│  Layer 3 — ORCHESTRATION                                      │
│  Query Router → Hybrid Retrieval → Reranker → LLM → Citation │
├──────────────────────────────────────────────────────────────┤
│  Layer 2 — KNOWLEDGE STORE                                    │
│  Vector DB (per-user namespace) + BM25 Index + Knowledge Graph│
├──────────────────────────────────────────────────────────────┤
│  Layer 1 — INGESTION PIPELINE                                 │
│  Doc Parser → Chunker → Embedder → Metadata Extractor         │
└──────────────────────────────────────────────────────────────┘
```

**架構說明**：

- **Layer 1（Ingestion）**：文件進入系統的第一站。負責解析各種格式（PDF/DOCX/PPT/Markdown/HTML）、切分 chunks、產生 embeddings、擷取 metadata（作者、日期、部門）
- **Layer 2（Knowledge Store）**：持久化層。Vector DB 儲存 embeddings 供語意搜尋；BM25 Index 支援關鍵字精確匹配；Knowledge Graph（選配）建立實體關係
- **Layer 3（Orchestration）**：查詢處理的核心邏輯。從意圖偵測到混合檢索、權限過濾、重排序、LLM 生成，全部在此層協調
- **Layer 4（Application）**：面對使用者的介面層。可以是 Web UI、Chat 介面、REST API、或嵌入其他系統的 Widget

### 2.2 關鍵技術選型

| 元件 | 推薦方案 | 備選 | 選型理由 |
|------|---------|------|---------|
| RAG 框架 | LlamaIndex + Haystack | LangChain | LlamaIndex 的 index abstraction 更適合知識庫場景；Haystack 的 pipeline 設計更清晰 |
| Vector DB | Qdrant（<500 users）→ Milvus（scale）| pgvector（已有 PG 時）| Qdrant 部署簡單、metadata filtering 最靈活；Milvus 適合需要 billion-scale 的場景 |
| Embedding | BGE-M3（自架，multilingual）| OpenAI text-embedding-3-large | BGE-M3 支援 100+ 語言、8192 tokens、dense+sparse+multi-vector 三模式，MIRACL benchmark nDCG@10=70.0 |
| LLM | Claude Sonnet（cloud）/ Qwen 2.5 72B（on-prem）| GPT-4o / Llama 3.3 70B | Claude Sonnet 品質/價格比最佳；Qwen 2.5 中文能力強，適合全私有部署 |
| 文件解析 | unstructured-io + LlamaParse | Apache Tika | unstructured-io 支援 100+ 格式，LlamaParse 對複雜 PDF（表格、圖片）解析品質最佳 |
| Keyword Search | Elasticsearch / OpenSearch | — | 成熟的 BM25 實作，支援中文分詞（IK analyzer）|
| Knowledge Graph | Neo4j（選配 Phase 2）| — | 適合建立「人→文件→概念」的關聯網路 |
| Auth | Keycloak（OIDC/SAML）| Azure AD | 開源、支援 SAML/OIDC/LDAP 聯合驗證，適合與企業 AD 整合 |
| File Storage | MinIO（S3 相容）| — | 輕量 S3 相容儲存，可處理原始文件備份 |
| Queue | Celery + Redis | Kafka | 中型規模足夠；Kafka 適合需要嚴格 ordering 的大規模部署 |

#### Vector DB 選型深度比較

| 維度 | Qdrant | Milvus | pgvector |
|------|--------|--------|---------|
| 適用規模 | <50M vectors | Billion-scale | <10M vectors |
| 部署複雜度 | 低（單 binary）| 中-高（分散式）| 低（PG extension）|
| Multi-tenancy | 原生 payload filtering | 原生 partition key | Schema/table 隔離 |
| 查詢延遲（1M vectors）| ~10ms | ~5ms（GPU）| ~50ms |
| 混合查詢 | ✅ 內建 | ✅ 內建 | ⚠️ 需手動 JOIN |
| 企業建議 | **Phase 1 首選** | Phase 2 升級路徑 | 已有 PG 且規模小時 |

> **致伸集團建議**：目前已有 pgvector（DTO Intelligence System 使用中，83/83 embedded），初期可沿用 pgvector 降低引入成本。當用戶數 >200 或 vector 數 >10M 時，遷移至 Qdrant。

### 2.3 Multi-Tenant 資料隔離模式

**推薦 Pattern C — Hybrid（個人 + 共享命名空間）**

```
Vector DB Namespace Structure
  ├── Personal NS: user_id = "emp_001" → 個人筆記、私人文件
  ├── Team NS:     team_id = "eng"     → 團隊知識（工程部文件）
  └── Org NS:      visibility = "all"  → 全公司文件（SOP、HR 政策）
```

**設計原則**：

1. **Data Access API 作為 Gatekeeper** — 每次查詢強制注入 `user_id` 過濾，永遠不直接查 vector store
2. **查詢時的 Scope 合併** — 使用者查詢自動搜尋「個人 + 所屬團隊 + 全公司」三層命名空間
3. **寫入時的隔離** — 使用者上傳文件預設進入 Personal NS；管理員可將文件提升至 Team/Org NS
4. **刪除權支援** — `purge_user(user_id)` API 可一鍵刪除指定使用者的所有 vectors（GDPR/PIPL Day 1 必備）

**三種隔離模式比較**：

| 模式 | 隔離強度 | 效能 | 複雜度 | 適用場景 |
|------|---------|------|--------|---------|
| Pattern A: Collection-per-user | 最強 | 低（太多 collections）| 高 | 極高安全要求（金融/醫療）|
| Pattern B: Shared collection + filter | 低 | 高 | 低 | 單一組織、信任內部用戶 |
| **Pattern C: Hybrid namespace** | **中-高** | **中-高** | **中** | **企業標準場景（推薦）** |

### 2.4 RAG Pipeline 最佳實踐

```
User Query
    ↓
┌─────────────────────────────────────────┐
│ Query Preprocessing                      │
│ • 意圖偵測（問答 / 摘要 / 搜尋）         │
│ • 查詢擴展（HyDE / Query Decomposition） │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ Hybrid Retrieval                         │
│ • Vector Search: top-20 by cosine sim    │
│ • BM25 Search:   top-20 by keyword       │
│ • (Optional) KG:  entity-based paths     │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ Security Trimming                        │
│ • user_id 權限過濾                       │
│ • team_id / org visibility 檢查          │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ Cross-Encoder Rerank                     │
│ • Recall@10: 74% → 89%（業界基準）       │
│ • 推薦 model: bge-reranker-v2-m3        │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ Context Assembly                         │
│ • Top-K chunks + citation metadata       │
│ • Parent-child context window            │
└────────────────┬────────────────────────┘
                 ↓
┌─────────────────────────────────────────┐
│ LLM Generation                           │
│ • 帶來源引用的回答                       │
│ • Hallucination guard（來源不足則拒答）   │
└─────────────────────────────────────────┘
```

#### Chunking 策略指南

| 文件類型 | 策略 | Chunk Size | Overlap | 說明 |
|---------|------|-----------|---------|------|
| 散文 / 文章 | 語意 chunking | 256-512 tokens | 10-15% | 按語意邊界切分（句號/段落）|
| 技術文件 | 結構化 chunking | 按 H1/H2/H3 | 保留 parent header | 每個 section 獨立，保留層級 |
| 表格 | Row-level | 每行 1 chunk | 保留 column headers | 每個 chunk 都帶完整 header |
| 混合文件 | 階層式 | parent 1024 + child 256 | — | 搜尋 child，回傳 parent context |
| 程式碼 | AST-aware | function/class 為單位 | 保留 import | 程式碼的語意邊界是函式 |

### 2.5 企業合規考量（與現有 Governance 研究連動）

> **Cross-reference**: 以下法規分析延伸自 RR-2026-002（全球法規全景研究）與 RR-2026-003（合規差距分析），針對 AI-Individual Wiki 場景具體化。

| 法規 | 對此系統的要求 | Risk Score | 行動 |
|------|---------------|-----------|------|
| **PIPL**（中國） | 中國員工資料不可跨境存放在境外 vector DB；AI 處理員工資料需取得同意 | 9.3 | 中國據點須獨立部署 vector store 實例 |
| **GDPR**（歐盟/捷克） | 刪除權 = 必須能刪除用戶所有 chunks（embedding 刪除複雜）| 8.5 | Day 1 必備 `purge_user` API |
| **Taiwan PDPA** | 員工同意 AI 處理個人通訊內容；自動化決策告知義務 | 6.0 | 上線前取得員工書面同意 |
| **EU AI Act** | 若 AI Wiki 影響僱用/績效決策，可能為「高風險 AI」| 7.5 | 評估是否構成 Art.6 高風險；若是，需技術文件 + 人類監督 |
| **Thailand PDPA** | 類似 GDPR；跨境傳輸需「適當保護措施」| 5.5 | 泰國據點資料需在地或有 SCC |

**Day 1 必備合規功能**：

1. `purge_user(user_id)` — 刪除指定用戶的所有 vectors + 原始文件 + metadata
2. `export_user_data(user_id)` — 匯出用戶所有資料（GDPR Art.20 可攜權）
3. `consent_log` — 記錄每位用戶的 AI 處理同意時間戳
4. `audit_trail` — 記錄誰在何時查詢/修改了哪些文件（已有 audit_logger agent 可複用）

---

## 3. Build vs Buy 分析

| 因素 | 自行開發 | OSS 組裝 | SaaS |
|------|---------|---------|------|
| 資料主權（PIPL/GDPR）| ✅ 完全掌控 | ✅ 部分掌控 | ⚠️ 風險高 |
| 個人化 AI | ✅ 完全客製 | ○ 中等 | ⚠️ 有限 |
| 首次交付 | 3-6 個月 | **4-8 週** | 1-2 週 |
| 長期靈活度 | ✅ 最大 | ✅ 高 | ⚠️ Vendor lock-in |
| 營運負擔 | ⚠️ 高 | ○ 中 | ✅ 低 |
| 1000 users 年成本 | ~$24-48K（infra）| ~$12-24K（infra）| ~$60-120K（per-seat）|
| 團隊需求 | 4-6 工程師 | **2 工程師** | 1 Admin |
| 中文支援品質 | 依實作 | 視專案 | 視 vendor |

### 推薦策略：分層 OSS 組裝

| 層 | 選用 | 說明 | 替代方案 |
|----|------|------|---------|
| Wiki/Editor | **Outline** 或 AppFlowy | 團隊 wiki UX + SAML/OIDC | AFFiNE（但 server 需 EE license）|
| AI RAG Layer | **Dify** 或 RAGFlow | RAG pipeline + agent + 視覺化 workflow | AnythingLLM（更簡單但功能較少）|
| Vector Store | **Qdrant**（self-hosted）| per-user collections，metadata filtering | pgvector（小規模先沿用）|
| Embedding | **BGE-M3**（self-hosted）| 100+ 語言，資料不離開 infra | text-embedding-3-large（雲端 API）|
| Reranker | **bge-reranker-v2-m3** | 與 BGE-M3 搭配效果最佳 | Cohere rerank（API）|
| LLM | **Qwen 2.5 72B**（on-prem）或 **Claude Sonnet**（cloud）| 視合規要求選擇 | GPT-4o / Llama 3.3 70B |
| Auth | **Keycloak** | 統一 OIDC/SAML，與企業 AD 整合 | Azure AD（若已有）|
| Search | **Elasticsearch** | BM25 + 中文 IK 分詞 | OpenSearch |

**預估交付**：2 工程師 8-16 週可達 production。

**成本估算**（1000 users，on-prem）：

| 項目 | 月成本 | 備註 |
|------|-------|------|
| GPU Server（Qwen 2.5 72B + BGE-M3）| ~$2,000 | 1x A100 80GB 或 2x A6000 |
| Qdrant + Elasticsearch | ~$500 | 標準 server |
| Dify/RAGFlow + Keycloak | ~$300 | Docker on existing infra |
| LLM API（若用 Claude）| ~$1,000-3,000 | 依使用量 |
| **Total（on-prem）** | **~$2,800/月** | 不含人力 |
| **Total（hybrid: on-prem + cloud LLM）** | **~$1,800-4,000/月** | 彈性 |

---

## 4. 針對場景的推薦組合

### 場景 A：快速啟動（最少開發，1-2 週）

| 項目 | 選擇 |
|------|------|
| 平台 | **AnythingLLM** |
| 特點 | MIT license、Docker 一鍵部署、支援 30+ LLM + 8+ vector DB |
| 適合 | POC 驗證、小團隊（<50 人）|
| 限制 | 缺乏進階權限管理、無 SAML/OIDC |

### 場景 B：企業級知識中心（8-16 週）

| 項目 | 選擇 |
|------|------|
| 平台 | **Onyx (Danswer)** |
| 特點 | 40+ 連接器（Slack/GitHub/Confluence/Google Drive）+ hybrid search + MIT CE |
| 適合 | 需要跨系統搜尋的大型組織（200+ 人）|
| 限制 | SSO/RBAC 在 EE 版 |

### 場景 C：中文環境優先

| 項目 | 選擇 |
|------|------|
| 平台 | **FastGPT** 或 **MaxKB** |
| 特點 | 中文 LLM 優化 + 視覺化 workflow + 多模態 |
| 適合 | 致伸集團中國據點或中文優先場景 |
| 限制 | FastGPT 的 SaaS 多租戶需商業授權；MaxKB 為 GPL-3.0 |

### 場景 D：完全私有部署（PIPL 最嚴格要求）

| 項目 | 選擇 |
|------|------|
| 平台 | **RAGFlow** + **BGE-M3** + **Qwen 2.5 72B**（via vLLM/Ollama）|
| 特點 | 資料完全不離開企業環境，所有元件自架 |
| 適合 | 中國據點、涉及敏感資料的部門 |
| 限制 | 需要 GPU server（A100 或同等級）|

### 場景 E：個人 AI 第二大腦

| 項目 | 選擇 |
|------|------|
| 平台 | **Khoj** |
| 特點 | Obsidian/Notion 整合 + 多平台（browser/WhatsApp/mobile）+ deep research |
| 適合 | 個人或小團隊的 knowledge assistant |
| 限制 | AGPL-3.0 license |

### 場景評估矩陣

| 場景 | 資料主權 | 中文支援 | 部署難度 | 擴展性 | 總分 |
|------|---------|---------|---------|--------|------|
| A: AnythingLLM | ★★★ | ★★ | ★★★★★ | ★★ | 15/25 |
| B: Onyx | ★★★★ | ★★★ | ★★★ | ★★★★★ | 19/25 |
| C: FastGPT/MaxKB | ★★★ | ★★★★★ | ★★★★ | ★★★ | 19/25 |
| D: RAGFlow Stack | ★★★★★ | ★★★★ | ★★ | ★★★★ | 19/25 |
| E: Khoj | ★★★ | ★★ | ★★★★ | ★★ | 15/25 |

---

## 5. 下一步行動建議

| 步驟 | 行動 | 負責 | 時程 | 前置條件 |
|------|------|------|------|---------|
| 1 | **釐清需求範圍**：「個人知識庫」vs「團隊/組織知識庫」vs 兩者結合 | DTO + IT | 1 週 | — |
| 2 | **選定 1-2 個 POC 候選**：建議 AnythingLLM（快速 POC）或 RAGFlow（production-grade）| DTO | — | Step 1 |
| 3 | **部署 POC**：Docker Compose 本機部署，測試文件上傳 + RAG 查詢品質 | IT + DTO | 1-2 週 | Step 2 |
| 4 | **評估 POC**：文件解析品質、中文支援度、回答準確率、延遲、false citation rate | DTO | 1 週 | Step 3 |
| 5 | **合規評估**：與法務確認 PIPL/GDPR 對 AI 處理員工資料的限制 | DTO + Legal | 2 週 | Step 1 |
| 6 | **決定 Build vs Extend**：根據 POC 結果決定是否需要自行開發或基於 OSS 擴充 | DTO + IT + Mgmt | — | Step 4, 5 |
| 7 | **Production 部署**：分層 OSS 組裝，含 Auth/RBAC/Audit Trail | IT | 8-16 週 | Step 6 |

---

## 6. 研究來源

### 主要來源

| # | 來源 | 類型 | Authority | Independence | 時效 |
|---|------|------|-----------|-------------|------|
| 1 | [Top 10 RAG Frameworks on GitHub — Jan 2026](https://florinelchis.medium.com/top-10-rag-frameworks-on-github-by-stars-january-2026-e6edff1e0d91) | Blog | Medium | High | 2026.01 |
| 2 | [15 Best Open-Source RAG Frameworks in 2026 — Firecrawl](https://www.firecrawl.dev/blog/best-open-source-rag-frameworks) | Blog | Medium | High | 2026 |
| 3 | [Enterprise AI Architecture — Enterprise Knowledge](https://enterprise-knowledge.com/enterprise-ai-architecture-series-how-to-build-a-knowledge-intelligence-architecture-part-1/) | Whitepaper | High | Medium | 2025 |
| 4 | [Secure Multitenant RAG — Microsoft Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/secure-multitenant-rag) | Official Doc | High | Low (vendor) | 2025 |
| 5 | [Production RAG Strategies — Towards AI](https://towardsai.net/p/machine-learning/production-rag-the-chunking-retrieval-and-evaluation-strategies-that-actually-work) | Research Blog | Medium | High | 2025 |
| 6 | [Best Chunking Strategies for RAG — Firecrawl](https://www.firecrawl.dev/blog/best-chunking-strategies-rag) | Blog | Medium | High | 2025 |
| 7 | [Choosing Embedding Models — Ailog RAG](https://app.ailog.fr/en/blog/guides/choosing-embedding-models) | Guide | Medium | High | 2025 |
| 8 | [Enterprise AI Authentication — CustomGPT](https://customgpt.ai/authentication-methods-enterprise-ai-knowledge-hubs/) | Blog | Medium | Low (vendor) | 2025 |
| 9 | [Best Vector Databases 2026 — Firecrawl](https://www.firecrawl.dev/blog/best-vector-databases) | Comparison | Medium | High | 2026 |
| 10 | [Top 9 Vector Databases Feb 2026 — Shakudo](https://www.shakudo.io/blog/top-9-vector-databases) | Comparison | Medium | High | 2026 |
| 11 | [BGE-M3 — BAAI/bge-m3 on Hugging Face](https://huggingface.co/BAAI/bge-m3) | Model Card | High | High | 2024 |
| 12 | [Best Open-Source Embedding Models 2026 — BentoML](https://www.bentoml.com/blog/a-guide-to-open-source-embedding-models) | Blog | Medium | High | 2026 |

### GitHub 專案來源（已驗證）

所有 22 個專案的 GitHub stars 均於 2026-03-05 經 GitHub 搜尋交叉驗證。詳見第 1 節表格中的 `[VERIFIED]` / `[CORRECTED]` 標註。

---

*本報告由 DTO 研究團隊產出，使用 Claude Code 主 session + 2 個 general-purpose 驗證 agent。*
*報告日期：2026-03-05 | 下次更新建議：2026-06-05（季度更新）*
