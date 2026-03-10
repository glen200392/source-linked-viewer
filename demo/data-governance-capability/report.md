# Data Governance & Data Science 能力建置研究報告

**報告編號**: RR-2026-001
**日期**: 2026-03-02
**作者**: Glen Ho (DTO Intelligence System)
**分類**: Internal — Strategic Planning
**狀態**: Draft v1.0

---

## Context

Glen 認為資料治理（Data Governance）與資料科學（Data Science）是未來 AI 治理的必備基礎能力，需要從現在開始規劃建置。本報告先回答「為什麼需要」，再盤點現有能力與落差，最後基於全球標準提出建議。

目標：兩者並行 — 個人 Claude Code 生態系做 POC 驗證 + Primax 公司層級正式提案。

---

## Part 0：為什麼需要資料治理與資料科學能力？

### 核心論點：沒有資料治理，AI 治理就是空談

```
AI 治理的依賴鏈：

  AI 模型可信度 ← 模型治理（model cards, drift monitoring）
       ↑
  模型品質     ← 訓練資料品質（garbage in, garbage out）
       ↑
  資料品質     ← 資料治理（schema 驗證、品質 SLA、血緣追蹤）
       ↑
  資料可見性   ← 資料目錄 + metadata 管理
       ↑
  資料安全     ← 分類、存取控制、PII 處理、跨境合規
```

**如果底層的資料沒有被治理，上層的 AI 治理就沒有基礎。** 這不是理論推導，而是以下具體風險的直接後果：

### 三大「為什麼現在必須做」的驅動力

#### 驅動力 1：法規合規已有硬性截止日期

| 法規 | 截止日期 | 不合規後果 |
|---|---|---|
| **EU AI Act — 高風險 AI 系統** | **2026.08.02**（距今 ~5 個月） | 最高 EUR 35M 或全球營收 7% 罰款 |
| **EU AI Act — 嵌入產品的 AI** | 2027.08 | Primax ODM 產品若含 AI 元件，需 CE 認證 |
| **中國 PIPL 跨境傳輸** | **已生效**（2026.03.01 GB/T 標準） | 最高全球營收 5% 罰款；中國營運可能被暫停 |
| **台灣 PDPA 修正** | 2025.11 已通過，PDPC 已運作 | 每次違規 NT$20,000-200,000，持續罰 |
| **美國 BIS AI 出口管制** | 2025.01.15 已生效 | 違反 EAR 可面臨刑事處罰 |

Primax 在中國有工廠（PIPL）、捷克有營運（GDPR）、英國有營運（UK GDPR）、台灣總部（PDPA）。**每一個營運點都有各自的資料合規義務，且這些義務正在急速增強。**

目前 DTO 系統的狀態：監控這些法規作為外部情報（dto-scout 收集 PIPL/GDPR 新聞），**但不對照自身的資料實踐**。這是典型的「知道規則但沒有遵守」的落差。

#### 驅動力 2：AI 專案的品質基礎不存在

Primax DTO 數位決策平台（P1 專案）規劃了 BI/AI 平台（Power BI/Tableau/Superset）和 Airflow/dbt 資料管線。但目前：

- **無 pandas、sklearn、MLflow、Feature Store** — 資料科學工具棧為零
- **無資料品質基線** — 不知道 MES/ERP 資料的品質水平
- **無資料目錄** — 不知道企業內有哪些資料資產可供 AI 使用
- **無模型治理** — SAP PP RAG 知識庫（137 chunks）已準備就緒但無 model card、無 drift monitoring

Gartner 2025 預測：**80% 的資料治理計畫將在 2027 年前失敗**（缺乏危機催化劑的組織）。意思是：如果不趁現在法規壓力明確時建立治理，以後會更難推動。

#### 驅動力 3：現有架構已有治理雛形，但未 formalize

這是好消息 — DTO Intelligence System 不是從零開始。它已經有：
- Schema versioning（v3.0）
- 去重機制（SHA-256 + 語意相似度）
- 品質門檻（source_credibility >= medium）
- 保留策略（90 天歸檔）
- 部分血緣（raw → insight ID tracking）

**問題是：這些都是 agent prompt 中的「君子協定」，不是系統性強制執行的治理。** 任何 agent 都可以繞過，沒有稽核軌跡，沒有 schema 硬性驗證。這就像一家工廠有品質手冊但沒有 QC 檢驗站。

### 現有架構 vs. 目標架構的落差圖

```
                    現有架構                          目標架構
                    ────────                          ────────

資料安全層     [無分類] [無ACL] [無PII]     →    分類體系 + RBAC + PII 脫敏
                                                + 跨境傳輸控制

資料品質層     [agent prompt 中的軟規則]      →    JSON Schema 強制驗證
               [kb-curator JSON parse 檢查]         + Soda Core 持續監控
                                                    + Data Contracts (SLA)

資料可見性     [無目錄] [分散的 JSON 檔案]    →    OpenMetadata 資料目錄
               [無統一 schema registry]             + 業務詞彙表
                                                    + 資料擁有權登記

資料血緣層     [慣例追蹤: raw_id → insight]   →    OpenLineage 自動血緣
               [無影響分析能力]                     + Dagster asset-centric
                                                    + 端到端 lineage graph

資料科學層     [無 ML 工具棧]                 →    MLflow + CRISP-DM 流程
               [numpy/numba/networkx 已裝]          + model registry
               [無 pandas/sklearn]                  + model cards + 實驗追蹤

稽核與合規     [kb_metadata 時間戳]           →    Append-only 稽核日誌
               [外部法規情報 ≠ 自我合規]             + 合規自評機制
                                                    + PIPL/GDPR SCC 法律文件

製造業整合     [SAP PP RAG 已就緒未部署]      →    ISA-95 架構對照
               [dto_context 有合規約束描述]         + OPC UA + UNS
                                                    + ISO 8000-220 感測器品質
```

### 為什麼選擇這些框架而非其他？

| 選擇 | 為什麼選 | 為什麼不選替代方案 |
|---|---|---|
| **NIDG 作為文化方法** | 製造業已有隱含的資料擁有者（品質工程師管品質資料、IE 管 BOM），NIDG formalize 既有責任而非增加新角色 | DGI/Gartner 偏向自上而下建新架構，製造業文化阻力大 |
| **OpenMetadata 而非 DataHub** | 架構最簡（MySQL + ES），1-2 人可部署；內建 data quality profiling + data contracts | DataHub 需要 Kafka + Graph DB，維運負擔過重 |
| **Dagster 而非 Airflow** | Asset-centric = 血緣自動內建；現有團隊無 Airflow 經驗 | Airflow 是 task-centric，血緣要額外加 OpenLineage wrapper |
| **Soda Core 而非 Great Expectations** | 宣告式 YAML（SodaCL），學習曲線低，非工程師也能定義品質規則 | Great Expectations Python-heavy，更適合資料工程團隊 |
| **MLflow 而非 W&B** | 開源免費，已支援 GenAI workflow（MLflow 3, 2025）；model registry 內建 | W&B 商用授權，功能更強但起步不需要 |
| **CRISP-DM 而非 TDSP** | 廠商中立，最廣泛使用，非技術人員也能理解 6 階段 | TDSP 強綁 Azure 生態系 |
| **ISO 42001 作為中期目標** | 可認證的 AI 管理系統標準，對 EU 客戶有信任信號 | NIST AI RMF 不可認證，先用於內部實踐 |

---

## Part 1：現有能力盤點

### 已具備的能力（DTO Intelligence System + Agent 生態系）

| 能力 | 成熟度 | 實作位置 |
|---|---|---|
| 結構化情報 KB（JSON + schema versioning v3.0） | 高 | `Projects/dto-intelligence/data/knowledge_base.json` |
| 資料品質門檻（來源可信度、證據連結、驗證評分） | 中高 | `dto-scout` / `dto-verifier` / `dto-analyst` agents |
| 去重機制（SHA-256 hash + 語意相似度 >80%） | 高 | `dto-scout` agent |
| 資料保留/歸檔（90 天輪替策略） | 中 | `kb-curator` agent |
| 部分資料血緣（forward: raw→insight ID 追蹤） | 中低 | `dto-analyst` + `dto-verifier` agents |
| 法規情報監控（PIPL/GDPR/EU AI Act 作為外部情報） | 高 | `dto-scout` + `dto-analyst` agents |
| 來源可信度 2 軸評估框架（authority × independence） | 高 | `research-critic` agent |
| 端點安全監控（Symantec log 解析） | 中 | `security-monitor` agent |
| RAG 知識庫（SAP PP，137 chunks，metadata tagged） | 已就緒未部署 | `Downloads/PP/PP/` |
| 音訊轉結構化文字 pipeline（Whisper + OpenCC） | 運作中 | `transcribe_meeting.py` + `dto_watcher/` |

### 關鍵缺口（10 項）

| # | 缺口 | 風險等級 | 說明 |
|---|---|---|---|
| G1 | **PII 識別 / 脫敏** | 高 | 會議記錄含員工姓名，無辨識或遮蔽機制 |
| G2 | **資料分類 / 敏感度標籤** | 高 | KB 無 sensitivity_level 欄位（public/internal/confidential/restricted） |
| G3 | **存取控制 / 資料擁有權** | 中高 | 所有 agent 都有 write 權限，無 ACL |
| G4 | **正式資料血緣圖** | 中 | 靠慣例追蹤，無自動化 lineage graph |
| G5 | **Schema 強制驗證** | 中 | schema 定義在 agent prompt，非硬性驗證 |
| G6 | **跨境資料傳輸控制** | 高 | PIPL/GDPR 僅作為情報監控，未自我適用 |
| G7 | **資料科學 / ML Pipeline** | 高 | 無 pandas、sklearn、MLflow、Feature Store |
| G8 | **資料目錄 / Metadata Registry** | 中高 | 無統一的資料資產清冊 |
| G9 | **修改稽核軌跡** | 中 | kb_metadata 僅記維護時間戳，無 who/what/when |
| G10 | **法規合規自評** | 中 | 監控外部法規，但不對照自身實踐 |

---

## Part 2：全球框架、標準與方法論總覽

### A. 資料治理框架（選哪個？）

| 框架 | 定位 | Primax 適合度 | 建議 |
|---|---|---|---|
| **DAMA-DMBOK 2 / 3.0** | 知識體系百科（11 知識領域） | 高 — 作為概念字典 | 必讀，用於團隊共同語言 |
| **DCAM v3**（EDM Council, 2025.06） | 能力成熟度評估工具（可打分、可對標） | 中高 — 用於衡量進度 | 18 個月後做正式評估 |
| **DGI Framework** | 組織設計參考（10 要素） | 中 — 用於建立治理委員會 | 建立治理架構時參考 |
| **Non-Invasive Data Governance (NIDG)** | 文化方法論（不加新官僚，formalize 既有責任） | **最高** — 製造業最適合 | **首選方法論** |
| **Gartner Framework** | 策略定位（5 級成熟度） | 高 — 用於高層溝通 | 用其語言對上報告 |

**推薦組合**：NIDG（文化方法） + DAMA-DMBOK（知識框架） + Gartner 成熟度模型（衡量進度）

### B. 資料品質標準

| 標準/工具 | 說明 | 建議 |
|---|---|---|
| **ISO 8000** | 資料品質國際標準；**Part 220:2025 新增感測器資料品質** | 直接適用於 IIoT 工廠數據 |
| **ISO/IEC 25012** | 15 項資料品質特性（準確性、完整性、一致性...） | 用作 KPI 設計詞彙 |
| **Great Expectations** | Python 資料驗證框架 | 適合 MES/ERP 匯出資料驗證 |
| **dbt tests** | SQL 轉換中嵌入品質檢查 | 轉換管線首選 |
| **Soda Core** | 宣告式持續監控（SodaCL 語言） | 生產環境品質 SLA 監控 |
| ~~Apache Griffin~~ | ~~已於 2025.11 退役~~ | **不採用** |

### C. 資料目錄 & Metadata 管理

| 工具 | 架構 | 適合 Primax？ |
|---|---|---|
| **OpenMetadata** | MySQL/PG + ES，最簡架構，內建 data quality profiling + data contracts | **首選 — 中型企業起步最佳** |
| **DataHub**（LinkedIn） | Kafka + Graph DB + ES，即時 metadata 串流 | 備選 — 已有 Kafka 再考慮 |
| **Apache Atlas** | Hadoop 生態系 | 不適合（非 Hadoop 環境） |
| **Collibra / Alation** | 商用企業級 | 預算允許時考慮 |

### D. 資料血緣 & 可觀測性

| 標準/工具 | 說明 |
|---|---|
| **OpenLineage** | 開放標準（LF AI & Data），管線血緣事件 JSON schema |
| **Marquez** | OpenLineage 參考實作（儲存 + 查詢） |
| **Dagster** | Asset-centric orchestrator，血緣內建不是外掛 |
| **dbt lineage** | SQL model 依賴 DAG 自動文件化 |

### E. AI 治理標準（最關鍵的合規截止日期）

| 標準 | 狀態 | 關鍵時間點 |
|---|---|---|
| **EU AI Act** | 已生效，分階段執行 | **2026.08.02** — 高風險 AI 系統要求生效（HR/信用/教育 AI）；2027.08 — 嵌入產品的 AI |
| **NIST AI RMF 1.0** | 美國自願性框架（GOVERN-MAP-MEASURE-MANAGE） | 無強制期限，但聯邦採購已參照 |
| **ISO/IEC 42001:2023** | 可認證的 AI 管理系統標準（如 ISO 9001） | 認證逐步增加中 |
| **ISO/IEC 23894** | AI 風險管理指引（對應 ISO 31000） | 搭配 42001 使用 |
| **新加坡 PDPC AI 框架** | 亞洲最務實的 AI 治理框架 + AI Verify 測試工具 | 2025 已擴展至 GenAI |
| **中國 TC260 V2.0**（2025.09） | 從原則宣言升級為操作手冊；涵蓋模型訓練資料治理 | 中國營運必須遵循 |

### F. 隱私法規 & 跨境傳輸

| 法規 | 管轄 | Primax 營運點 | 跨境傳輸機制 |
|---|---|---|---|
| **PIPL** | 中國 | 中國工廠 | 安全評估 / 標準合同（SCC）/ **認證（推薦 ODM 用）** |
| **GDPR** | EU | 捷克 | 標準契約條款（SCCs）；台灣無 adequacy decision |
| **UK GDPR** | 英國 | 英國 | EU adequacy 延至 2031；UK↔EU 無需額外措施 |
| **台灣 PDPA** | 台灣 | 總部 | 2025.11 重大修正：新設個資保護委員會、強制通報 |
| **CBPR** | APEC | 台灣/日本/新加坡 | 多目的地跨境傳輸可選認證途徑 |

**注意**：美國 BIS 2025.01.15 對 AI 模型權重實施出口管制。如果模型使用美國來源技術訓練，從台灣移轉到中國工廠可能需要 BIS 出口許可。

### G. 資料科學方法論 & MLOps

| 方法論 | 說明 | 建議 |
|---|---|---|
| **CRISP-DM** | 最廣泛使用的 DS 流程框架（6 階段迭代） | **首選 — 每個 AI/ML 專案的標準流程** |
| **TDSP** | Microsoft 結構化團隊 DS 流程 | 用 Azure 則採用 |
| **DataOps** | DevOps 原則應用於資料管線 | MLOps 之前必備 |
| **MLOps 成熟度** | 5 階段：Ad hoc → DataOps → Manual MLOps → Automated → Kaizen | 製造業起步通常在 Stage 0-1，目標 18 個月 Stage 2 |

### H. 工具技術棧建議

**最小可行棧（1-2 工程師可部署）：**

```
Stage 1（2 週內可上線）
├── 資料目錄：     OpenMetadata（Docker Compose）
├── 資料品質：     Soda Core（CLI + YAML）
├── 資料編排：     Dagster（本地開發）
└── ML 追蹤：      MLflow（單機 + PostgreSQL）

Stage 2（3-6 個月）
├── 資料血緣：     OpenLineage + Marquez
├── 資料轉換：     dbt Core + dbt tests
└── 資料可觀測：   Elementary（dbt-native）

Stage 3（12 個月+）
├── 事件串流：     Apache Kafka
├── ML 編排：      Kubeflow（K8s-native）
└── Feature Store： Feast（5+ 模型共享時）
```

### I. 製造業特有標準

| 標準 | 說明 | 狀態 |
|---|---|---|
| **ISA-95 / IEC 62264**（2025 新版） | 製造企業整合標準；2025 版新增容器化架構 + metadata-driven 設計 | **製造業 IT/OT 整合的必備藍圖** |
| **OPC UA** | ISA-95 的語意傳輸層 | 搭配 ISA-95 使用 |
| **Unified Namespace (UNS)** | 2025 新興架構模式，統一命名空間取代點對點連線 | 新建系統首選 |
| **GS1 標準** | 供應鏈資料交換（GTIN/GLN/EPCIS） | EU DPP 2027 後強制要 2D 條碼 |
| **ISO 8000-220:2025** | 感測器資料品質（新發布） | 直接適用 IIoT |

### J. 2025-2026 新興趨勢

| 趨勢 | 說明 | Primax 適用性 |
|---|---|---|
| **Data Mesh** | 領域擁有權 + 資料即產品 + 聯邦治理 | 中期目標（9-18 月） |
| **Data Contracts** | 生產者與消費者間的正式 SLA（schema + 品質規則 + 分類） | 短期即可導入 |
| **AI-Powered Governance** | 用 AI 做自動分類、異常偵測、政策執行 | 趨勢觀察，18 個月後評估 |
| **Synthetic Data** | 合成資料替代真實個資做跨境 AI 訓練 | 解決 PIPL 跨境痛點 |
| **Data Clean Rooms** | 多方安全共享資料（如與 Tier-1 客戶合作良率分析） | IDC 預測 2028 年 60% 企業採用 |
| **LLM 治理** | 幻覺監控、prompt injection 防護、模型卡 | 部署任何 LLM 前必備 |

---

## Part 3：分階段建置路線圖

### Phase 0 — 基礎建立（Month 1-3）

| # | 行動 | 對應缺口 | 產出 |
|---|---|---|---|
| 1 | 成立資料治理委員會（IT + 製造 + 品質 + 法務 + C-level sponsor） | 組織 | 委員會章程 |
| 2 | PIPL 合規稽核 — 盤點中國→台灣所有資料流 | G6 | 資料流清冊 + 傳輸途徑決定 |
| 3 | 台灣 PDPA 就緒 — 確認資料外洩通報程序（新設 PDPC） | G6 | 通報 SOP |
| 4 | AI 模型清冊 — 列出所有模型、訓練資料來源、是否涉及美國技術 | G10 | 模型登錄表 |
| 5 | 定義資料分類體系（Public / Internal / Confidential / Restricted） | G2 | 分類政策文件 |

### Phase 1 — 快速見效（Month 3-6）

| # | 行動 | 對應缺口 | 產出 |
|---|---|---|---|
| 6 | 部署 OpenMetadata — 先登錄 5 個最高價值資料域 | G8 | 運作中的資料目錄 |
| 7 | 在 DTO KB schema 加入 `sensitivity_level` 欄位 | G2 | 更新的 schema v4.0 |
| 8 | 為 agent 實作 JSON Schema 強制驗證（write 前檢查） | G5 | 驗證 agent 或 hook |
| 9 | 部署 Soda Core — 5 個試點資料域的品質基線 | G1, G5 | 品質 dashboard |
| 10 | 建立修改稽核 log（append-only JSON，記錄 who/what/when） | G9 | 稽核機制 |

### Phase 2 — 系統化（Month 6-12）

| # | 行動 | 對應缺口 | 產出 |
|---|---|---|---|
| 11 | 導入 Dagster + dbt + OpenLineage — 資料血緣自動追蹤 | G4 | 端到端血緣圖 |
| 12 | 部署 MLflow — 模型登錄、model card、實驗追蹤 | G7 | 模型治理平台 |
| 13 | 發布第一份 Data Contract（MES 品質資料 → AI 團隊） | G3 | 正式 SLA |
| 14 | 實施 PII 偵測 — 會議記錄 / KB 中的個資辨識與遮蔽 | G1 | PII scanner |
| 15 | 啟動 PIPL 認證途徑申請（需 3-6 個月完成） | G6 | 認證進程 |
| 16 | ISA-95 架構對照 — 對照現有 IT/OT 架構，識別資料缺口 | 製造業特有 | 架構差距報告 |

### Phase 3 — 成熟與合規（Month 12-18）

| # | 行動 | 對應缺口 | 產出 |
|---|---|---|---|
| 17 | Data Mesh 組織模型 — 領域團隊擁有各自的 data products | G3 | 聯邦治理架構 |
| 18 | 法規合規自評機制 — 將外部法規對照自身實踐，標記不合規 | G10 | 合規 dashboard |
| 19 | GDPR SCC 執行 — 捷克/英國→台灣正式標準契約條款 | G6 | 法律文件 |
| 20 | 評估 Synthetic Data pipeline — 跨境 AI 訓練替代方案 | G6, G7 | POC 報告 |
| 21 | LLM 治理層 — prompt logging、幻覺監控、human review gate | 新興 | LLM 治理 SOP |
| 22 | ISO 42001 認證評估 — 是否追求 AI 管理系統認證 | 合規 | 認證可行性報告 |

---

## Part 4：對 Claude Code Agent 生態的具體改進建議

基於缺口分析，建議對現有 agent 系統做以下改進：

### 新增 Agent

| Agent | 用途 | 對應缺口 |
|---|---|---|
| `data-governance-agent` | 資料分類、PII 偵測、合規自評、Data Contract 管理 | G1, G2, G3, G6, G10 |
| `data-catalog-agent` | 維護資料資產清冊、schema registry、lineage 查詢 | G4, G8 |
| `audit-logger` | Append-only 稽核日誌，記錄所有 KB 寫入的 who/what/when | G9 |

### 現有 Agent 改進

| Agent | 改進 | 對應缺口 |
|---|---|---|
| `dto-scout` | 新增 `sensitivity_level` 欄位；寫入前 JSON Schema 驗證 | G2, G5 |
| `kb-curator` | 新增 field completeness 驗證（不只 JSON parse + id 重複） | G5 |
| `meeting-ingestion-agent` | 新增 PII 偵測 + 遮蔽步驟（姓名、電話、email） | G1 |
| `dto-analyst` | 新增法規合規自評維度（對照自身資料實踐） | G10 |

### 新增 Skill

| Skill | 用途 |
|---|---|
| `/data-audit` | 觸發資料資產盤點 + 品質基線報告 |
| `/compliance-check` | 觸發 PIPL/GDPR/PDPA 合規自評 |

---

## Part 5：核心參考來源

### 框架與標準
- DAMA-DMBOK 2 / 3.0（知識體系）
- DCAM v3（EDM Council, 2025.06，成熟度評估）
- Non-Invasive Data Governance Unleashed（Robert Seiner, 2025，文化方法論）
- ISO 8000-220:2025（感測器資料品質）
- ISO/IEC 25012（15 項資料品質特性）
- ISA-95 / ANSI-ISA-95.00.01-2025（製造企業整合）
- OpenLineage（LF AI & Data，血緣開放標準）

### AI 治理法規
- EU AI Act（2026.08 高風險系統生效）
- NIST AI RMF 1.0（GOVERN-MAP-MEASURE-MANAGE）
- ISO/IEC 42001:2023（可認證 AI 管理系統）
- 中國 TC260 AI 安全治理框架 V2.0（2025.09）
- 新加坡 PDPC Model AI Governance Framework

### 隱私法規
- PIPL（中國，認證途徑 2025 全面運作）
- GDPR（EU，SCCs for 台灣）
- 台灣 PDPA（2025.11 重大修正）
- BIS AI 模型權重出口管制（2025.01.15）

### 工具技術
- OpenMetadata（資料目錄首選）
- Dagster（asset-centric orchestration + 內建血緣）
- Soda Core / dbt tests / Great Expectations（資料品質三層）
- MLflow 3（實驗追蹤 + 模型登錄 + GenAI workflow）
- CRISP-DM（資料科學專案流程）

---

## 驗證方式

本計畫為研究型產出，驗證方式：
1. 檢查此計畫涵蓋的框架/標準是否對應使用者的原始需求（資料治理 + 資料科學 + AI 治理）
2. 確認所有法規截止日期與來源一致
3. 確認工具建議與缺口分析對應
4. 後續可基於此計畫逐項建立 agent / skill / 技術棧

---

*Generated by DTO Intelligence System — Research Report Pipeline*
*Report ID: RR-2026-001*
