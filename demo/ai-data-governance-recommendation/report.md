# 致伸集團 AI 治理與資料治理建議報告

**報告編號**: RR-2026-004
**日期**: 2026-03-02
**提案人**: Glen Ho, DTO
**分類**: Internal — Executive Advisory
**讀者**: DTO 管理層 / 法務長 / 資訊長 / 高階管理團隊
**前置分析**: RR-2026-002（全球法規全景研究, 37 項來源）、RR-2026-003（合規差距分析, 25 法規/32 差距）

### 相關報告快速連結
| 報告 | 用途 |
|------|------|
| [RR-2026-002 全球法規全景研究](2026-03-02_ai-governance-global-landscape-research.md) | Phase A 37 來源、6 子題研究 |
| [RR-2026-003 合規差距分析與路線圖](2026-03-02_ai-governance-compliance-roadmap.md) | Phase B 差距分析 + P0-P4 行動路線圖 |
| **本報告（RR-2026-004）** | 高管建議報告 |

---

## 1. 為什麼現在必須行動

致伸集團（以下簡稱 Primax）在七個國家營運，涉及多項國際法規的直接或間接管轄。以下三個情境說明為何 AI 治理與資料治理已不是「未來應做」，而是「現在必做」：

### 情境一：中國工廠的每一筆跨境資料流都處於違規狀態

根據中國《個人信息保護法》（PIPL）第 38 條，個人信息處理者因業務需要向中國境外提供個人信息的，必須通過以下三條路徑之一取得合法基礎：

| 路徑 | 說明 | 現行狀態 |
|---|---|---|
| 安全評估 (Security Assessment) | 國家網信辦直接審批 | **未啟動** |
| 標準合同 (Standard Contract) | 與境外接收方簽署標準合同並向省級 CAC 備案 | **未啟動** |
| 認證 (Certification) | 第三方機構認證（2026.01.01 新制生效） | **未啟動** |

Primax 中國子公司向台灣總部傳輸的員工資料和營運資料，目前**未經任何一條路徑取得合法基礎**。

**執法先例**：2025 年 5 月，上海公安機關對一家跨國公司處以行政處罰——該公司在未通過安全評估、未簽署標準合同、未取得認證的情況下，將中國用戶個人信息傳輸至法國總部。這是中國首例公開披露的跨境傳輸違法行政處罰。

**罰則**：PIPL 最高可處全球年營收 5% 的罰款；嚴重情節可暫停相關業務或要求整改。

> **建議**：立即啟動 PIPL 標準合同（SCC）備案程序。SCC 是三條路徑中對 Primax 最務實的選擇——流程自主可控、備案週期可預測（10 工作日提交 + 15 工作日審核）、成本可控。前提是完成個人信息保護影響評估（PIPIA）。

### 情境二：ODM 產品若含 AI，Primax 可能被歐盟視為 AI 系統供應商

歐盟《人工智慧法》（EU AI Act）第 25 條明確規定：當高風險 AI 系統是受歐盟產品安全法規（Annex I Section A）涵蓋的產品安全元件時，**產品製造商**在以下情況被視為該 AI 系統的 provider（供應商）：

- AI 系統以製造商的名稱或商標上市（Art.25(1)(a)）
- AI 系統在產品上市後以製造商名稱投入使用（Art.25(1)(b)）

**對 Primax 的意義**：作為 ODM/EMS 製造商，若 Primax 為客戶生產的電子產品中嵌入了 AI 功能（例如智慧音箱中的語音辨識、遊戲硬體中的 AI 運算模組），且該產品受歐盟機械法規（Machinery Regulation 2023/1230）或其他 Annex I 安全立法涵蓋，**Primax 可能承擔完整的 provider 義務**——包括風險管理系統、技術文件、合規性評估、上市後監控。

**罰則**：違反高風險 AI 義務的罰款最高可達全球年營收 7% 或 EUR 3,500 萬（取較高者）。高風險 AI 產品可被**禁止在歐盟市場上市**。

**時程**：
- Annex III（非產品嵌入式高風險 AI）：**2026 年 8 月 2 日**生效（EU Digital Omnibus 提案中建議延後至 2027.12.02，但尚未通過）
- Annex I（產品嵌入式高風險 AI）：**2027 年 8 月 2 日**生效

> **建議**：立即盤點所有 ODM/EMS 客戶產品是否含有 AI 元件。對於含 AI 的產品，需由外部法律顧問出具正式法律意見，判斷 Primax 在 Art.25 下的義務範圍。這是本報告所有建議中風險分數最高的項目之一（9.1/10）。

### 情境三：七國據點各自面臨的法規壓力正在同時升高

| 據點 | 主要法規 | 2026 年新增壓力 |
|---|---|---|
| **TW 台灣** | 個資法（PDPA） | 2025.11 修正施行：新設個人資料保護委員會（PDPC），**強制違規通報義務**。Primax 是否已建立通報程序？ |
| **CN 中國** | PIPL / DSL / CSL | 《網路安全法》修正已於 2026.01.01 生效（新增 AI 合規條款）；全國數據局規劃發布 30+ 項數據和 AI 標準 |
| **CZ 捷克** | GDPR + EU AI Act | EU AI Act Art.4（AI 素養）已於 2025.02.02 生效；Art.6（高風險系統）2026.08.02 生效 |
| **UK 英國** | UK DPA + AI White Paper | UK↔EU adequacy 延至 2031；UK AI 監管採 pro-innovation 路線但可能立法 |
| **TH 泰國** | Thailand PDPA | 2026.02 發布《AI 資料保護指引》草案；DPO 指定為強制要求 |
| **JP 日本** | APPI + AI 法 | 2025.05 通過日本首部 AI 法（鼓勵自律路線）；APPI 修正強化跨境傳輸和自動化決策規範 |
| **US 美國** | BIS Export Controls | Trump 政府撤銷 Biden AI Diffusion Rule（2025.05），但基本出口管制仍在；政策方向不穩定 |

> **核心判斷**：全球 AI 監管不是單一法規的問題，而是一個**多法規同時施壓的矩陣**。Primax 需要一個跨據點統一的治理框架來管理這個矩陣，而非各據點各自為政。

---

## 2. 現行合規差距總覽

基於 CC-2026-001 合規基線和 RR-2026-003 差距分析，我們識別了 32 項合規差距。以下為經風險計分排序後的 Top 10：

```
風險計分 = (罰則嚴重度 × 30%) + (發生機率 × 25%) + (時程緊迫度 × 25%) + (營運衝擊 × 20%)
```

| 排名 | 差距 | 涉及法規 | 風險分數 | 據點 |
|---|---|---|---|---|
| 1 | CN→TW 跨境傳輸無合規機制 | PIPL Art.38 | **9.3**/10 | CN→TW |
| 2 | ODM 產品 AI 責任未釐清 | EU AI Act Art.25 | **9.1**/10 | CZ/EU |
| 3 | 全集團無 AI 系統清冊 | EU AI Act + 多法規 | **8.5**/10 | All |
| 4 | EU Product Liability 適用性未評估 | PLD (recast) | **7.8**/10 | EU |
| 5 | CZ 據點 GDPR 合規狀態不明 | GDPR Art.30/46 | **7.4**/10 | CZ |
| 6 | AI 系統無技術文件 | EU AI Act Annex IV | **7.2**/10 | CZ/EU |
| 7 | Taiwan PDPC 通報程序未建立 | PDPA Art.12 (2025) | **6.5**/10 | TW |
| 8 | AI 素養合規未確認 | EU AI Act Art.4 | **6.3**/10 | CZ |
| 9 | CN AI 新標準合規準備不足 | CN Cybersecurity Law | **6.0**/10 | CN |
| 10 | TH PDPA + AI 指引合規未確認 | Thailand PDPA | **5.2**/10 | TH |

---

## 3. 建議方案：三層治理架構

### 第一層：合規急件（2026 Q2 前完成）

這一層的目標是**止血**——處理已經生效且 Primax 明確不合規的項目。

#### 建議 3.1：啟動全集團 AI 系統盤點

**法規依據**：
- EU AI Act Art.6：分類的前提是知道自己有哪些 AI 系統
- PIPL：AI 系統涉及的個人信息處理需要額外評估
- ISO 42001 Clause 4.2：了解組織的 AI 相關活動是管理系統的起點

**範圍**：

| 類別 | 舉例 | 需確認事項 |
|---|---|---|
| 企業內部 AI 工具 | Chatbot Pilot、SAP PP RAG、War Room Dashboard | 部署據點、使用者範圍、涉及資料類型 |
| ODM/EMS 產品 AI | 客戶產品中的嵌入式 AI 功能 | 是否以 Primax 名義上市？是否屬安全元件？ |
| 製造現場 AI | 視覺檢測、預測性維護、機器人控制 | 是否為 safety component？ |
| HR/管理 AI | 招聘篩選、績效分析（若有） | Annex III 第 4 項高風險 |
| 第三方 AI 服務 | Claude、ChatGPT、M365 Copilot（若使用） | 資料跨境路徑、供應商合規承諾 |

**產出物**：AI 系統清冊（含分類、據點、風險初步判定）
**負責**：DTO 發起，IT + Product + Manufacturing 配合
**工作量估計**：3-4 人週

#### 建議 3.2：啟動 PIPL CN→TW 跨境傳輸合規程序

**推薦路徑：標準合同 (Standard Contract / SCC)**

根據 RR-2026-002 的三條路徑比較分析，標準合同是 Primax 最適路徑：

| 因素 | 安全評估 | 標準合同 | 認證 |
|---|---|---|---|
| 適用門檻 | >100 萬人 PI 或重要數據 | 中小規模 | 集團多實體 |
| 審批方式 | CAC 直接審批 | 省級 CAC **備案** | 第三方機構 |
| 時程 | 數月至一年 | **25 工作日**（提交+審核） | 新制，時程待觀察 |
| 成本 | 高 | **中等** | 中高 |
| 自主性 | 低（需配合審查） | **高**（自主管理） | 中 |

**執行步驟**：
1. 盤點 CN→TW 的資料類型和數量（員工資料、營運資料、AI 模型相關數據）
2. 完成個人信息保護影響評估（PIPIA）——需在備案前 3 個月內完成
3. 與 TW 總部（資料接收方）簽署 CAC 標準範本合同
4. 向 CN 工廠所在地省級 CAC 提交備案
5. CAC 審核（15 工作日）——若不通過需 10 工作日內補充材料

**需要法務參與**：SCC 法律審查、PIPIA 審定、備案提交
**工作量估計**：4-6 人週

#### 建議 3.3：確認各據點基本合規狀態

| 據點 | 確認事項 | 法規依據 | 負責 |
|---|---|---|---|
| TW | PDPC 通報 SOP 是否存在？個資清冊是否完成？ | Taiwan PDPA Art.12 (2025 amendment) | Legal + IT |
| CZ | ROPA (Art.30) 是否存在？CZ→TW 有無 SCCs？DPO 是否指定？ | GDPR Art.30, Art.37, Art.46 | Legal + CZ HR |
| TH | DPO 是否指定（TH PDPA 強制要求）？資料處理登記？ | Thailand PDPA | Legal + TH HR |
| UK | DPA 2018 基本合規？UK↔EU 資料流安排？ | UK DPA 2018 | Legal + UK HR |

**說明**：這些不是「建立」合規，而是「確認」現有狀態。許多據點可能已經有一定程度的合規實踐（特別是 CZ 據點的 GDPR），但 DTO 層面缺乏可見性。

---

### 第二層：法規截止日準備（2026 Q2-Q3）

這一層的目標是**針對有截止日的法規完成合規準備**。

#### 建議 3.4：完成 EU AI Act 風險分類與合規準備

基於建議 3.1 的 AI 系統清冊，對照 EU AI Act Annex III（8 大高風險場景）和 Annex I（產品安全立法）進行分類。

**預判**（基於 RR-2026-002 分析）：

| AI 系統 | 預判風險等級 | 依據 | 主要義務 |
|---|---|---|---|
| Chatbot Pilot | **有限風險 (Limited Risk)** | 不屬於 Annex III 高風險場景 | Art.50 透明度：告知使用者為 AI 互動 |
| War Room Dashboard | **最小風險 (Minimal Risk)** | BI/資料視覺化工具 | 無強制義務；可自願採用行為準則 |
| SAP PP RAG | **有限風險** | 企業內部 AI 助手 | Art.50 透明度 |
| ODM 產品 AI | **待判定——可能高風險** | Art.25 + Annex I | 需外部法律意見 |
| HR AI 工具（若有） | **高風險** | Annex III 第 4 項：就業、勞工管理 | 完整合規：風險管理 + 技術文件 + 合規性評估 |

**針對有限風險 AI 系統（Chatbot、RAG）的行動**：
- 確保 Chatbot 界面明確告知使用者「您正在與 AI 系統互動」
- 保留 AI 系統的互動記錄，以備監管查詢

**針對可能高風險 AI 系統（ODM 產品 AI）的行動**：
- 委託外部法律顧問出具 Art.25 適用性意見
- 若確認高風險，啟動技術文件（Annex IV）準備：設計決策、資料血緣、測試方法、風險控制
- 評估是否需要進行合規性評估（self-assessment 或第三方）

**時程**：風險分類需在 **2026 年 5 月中** 前完成，為技術文件留出 2.5 個月

#### 建議 3.5：EU Product Liability Directive 影響評估

歐盟新版《產品責任指令》（PLD recast）要求成員國在 **2026 年 12 月 9 日** 前轉化為國內法。關鍵變化：

- **「產品」定義明確擴展至軟體和 AI 系統**——包括嵌入式軟體、獨立軟體、SaaS 功能
- 軟體開發者（包括 AI 系統供應商）被視為製造商
- AI 系統故障造成損害時，舉證責任可能轉移至供應商

**對 Primax 的影響**：若 ODM 產品中嵌入的 AI 功能導致產品缺陷和損害，Primax 可能面臨產品責任訴訟。這與 EU AI Act Art.25 的責任分析高度相關。

> **建議**：將 PLD 影響評估與 Art.25 法律意見一併處理，由同一組外部律師團隊評估。

---

### 第三層：治理體系制度化（2026 Q3-Q4 及以後）

這一層的目標是**從「合規急件」轉為「系統性治理」**。

#### 建議 3.6：建立 AI 治理框架——以 ISO 42001 為基礎

**為什麼是 ISO 42001？**

| 框架 | 類型 | 可認證 | 與 EU AI Act 關係 | 適合 Primax 的原因 |
|---|---|---|---|---|
| **ISO/IEC 42001:2023** | 管理系統標準 | ✅ | 非推定合規，但控制項可映射 | 可整合進現有 ISO 9001 QMS；國際客戶認可度高 |
| NIST AI RMF 1.0 | 自願性框架 | ❌ | 可輔助合規 | 美系客戶可能要求 |
| prEN 18286 | EU 調和標準 | 制定中 | 未來推定合規 | 追蹤用；發布後可作為 42001 的補充 |

**重要發現**：ISO 42001 **不是** EU AI Act 的推定合規（presumption of conformity）標準。EU 另行委託 CEN-CENELEC JTC21 開發 prEN 18286。但 ISO 42001 仍是全球最全面的 AI 管理系統認證框架，其控制項（Annex B/C/D）可直接映射至 EU AI Act 的多項要求。

**建議路徑**：
```
現有 ISO 9001 QMS ──→ 擴展至 ISO 42001 AIMS
                          │
                          ├── 補充 EU AI Act 特定要求
                          ├── 整合 ISO 27001 資安管理（若已有）
                          └── 追蹤 prEN 18286 發布後升級
```

**第一步**：ISO 42001 差距分析（gap analysis），評估現有品質管理體系與 42001 要求的差距
**投資預估**：差距分析 4-6 人週；完整認證 12-18 個月 + 認證費用

#### 建議 3.7：建立資料治理基礎架構

AI 治理的底層是資料治理。沒有資料治理，以下問題無法回答：

- PIPL 要求的「你處理了哪些個人信息？」→ 需要**資料清冊**
- GDPR 要求的 ROPA (Record of Processing Activities) → 需要**資料處理活動記錄**
- EU AI Act 要求的「訓練資料品質和資料血緣」→ 需要**資料血緣追蹤**
- ISO 42001 要求的「AI 系統使用的資料品質管理」→ 需要**資料品質基線**

**各國法規對資料治理的共通要求**：

| 要求 | PIPL | GDPR | TW PDPA | TH PDPA | EU AI Act | ISO 42001 |
|---|---|---|---|---|---|---|
| 資料清冊/ROPA | ✅ 隱含 | ✅ Art.30 | ✅ 隱含 | ✅ 隱含 | ✅ Annex IV | ✅ Clause 6 |
| 資料分類 | ✅ 敏感 PI 特殊保護 | ✅ 特殊類別 | ✅ 特種個資 | ✅ 敏感個資 | ✅ 風險分類 | ✅ Annex B |
| 跨境傳輸控制 | ✅ Art.38-39 | ✅ Art.44-49 | ✅ Art.21 | ✅ S.28-29 | — | — |
| 違規通報 | ✅ 通報義務 | ✅ 72hr Art.33 | ✅ PDPC 通報 | ✅ 72hr | ✅ 嚴重事件通報 | ✅ 事件管理 |
| DPO/負責人 | ✅ 特定條件 | ✅ Art.37 | ✅ 政府機關 | ✅ 強制 | — | ✅ AI governance lead |
| 影響評估 | ✅ PIPIA | ✅ DPIA Art.35 | — | — | ✅ 基本權利影響 | ✅ AI risk assessment |
| 資料保留/刪除 | ✅ 最少必要 | ✅ 目的限制 | ✅ 目的消失刪除 | ✅ 目的限制 | — | — |

**觀察**：資料清冊、資料分類、通報機制是所有法規的**共同交集**。建立一次，滿足多國要求。

> **建議**：以「統一資料平台」（data_platform）專案為載體，將資料治理框架的建設整合進去。具體行動包括：(1) 各據點資料清冊/ROPA 建置 (2) 資料分類方案（公開/內部/機密/敏感 PI） (3) 跨境傳輸控制矩陣 (4) 違規通報統一 SOP。

#### 建議 3.8：OT 安全與 AI 治理整合

Primax 作為精密電子製造商，工廠環境中的 OT（Operational Technology）安全與 AI 整合是特殊的治理需求：

**涉及標準**：
- **IEC 62443**：工業自動化控制系統（IACS）網路安全權威框架
- **EU Machinery Regulation 2023/1230**（2027.01.20 適用）：AI 系統明確納入安全元件定義

**Primax 應關注的場景**：

| 場景 | AI 類型 | 安全風險 | 治理要求 |
|---|---|---|---|
| AI 視覺品檢 | 影像辨識 | 漏檢→產品安全 | 可能需 CE 認證（若為安全元件） |
| 預測性維護 | 時序預測 | 誤判→設備故障 | 需驗證 + 回退機制 |
| 機器人 + AI | 自主控制 | 人機安全 | Machinery Reg. + EU AI Act 雙重合規 |
| IT/OT 融合 | 資料管線 | 攻擊面擴大 | IEC 62443 網路分段 + AI 系統隔離 |

> **建議**：在 ISO 42001 差距分析中一併評估 IEC 62443 與 AI 的交集，特別是 AI 系統跨越 IT/OT 邊界時的安全治理需求。

---

## 4. 亞太區域特別注意事項

Primax 的亞太據點面臨的法規環境正在快速演變。以下為 2026 年各國 AI 治理法規動態：

### 4.1 韓國：AI Basic Act 已於 2026.01.22 生效

韓國 AI 基本法的核心特徵是**風險分級**——區分「高影響 AI」（醫療、交通、金融、教育、公共服務）和一般 AI。高影響 AI 的營運者須整合風險管理計劃、人工控制和監控系統。

此外，PIPA（個人信息保護法）2023 修正已正式承認資料主體對**全自動化決策**的權利：
- 要求解釋權：有權要求說明自動化決策的依據和過程
- 拒絕權：對產生重大影響的自動化決策有權拒絕
- 人工審查權：有權要求人工介入

**對 Primax 的影響**：若 Primax 有韓系客戶，客戶可能基於 AI Basic Act 要求供應鏈合規證明。建議在供應鏈調查（建議 3.4 延伸）中包含韓系客戶的合規期待。

### 4.2 日本：首部 AI 法通過，走自律路線

2025 年 5 月，日本國會通過首部 AI 法，但與歐盟的強制性法規不同，日本採取**鼓勵自律**的路線——重點在透明度、責任歸屬和風險管理，而非處罰。

APPI（個人情報保護法）修正草案中強化了：
- 跨境傳輸的資訊揭露義務：須提供資料接收方的保護措施概要
- 違反跨境傳輸規定的行政罰金制度（新增）

**對 Primax 的影響**：日本法規壓力相對溫和，但 APPI 跨境傳輸強化值得關注。若有日系客戶合作，需了解其內部 AI 治理期待。

### 4.3 泰國：PDPA AI 指引草案出爐

2026 年 2 月 17 日，泰國 PDPC 發布《AI 開發與使用個人資料保護指引》草案，將 PDPA 的資料控制者和處理者義務**轉化為 AI 生命週期的具體措施**——從設計到除役，強調問責和 privacy-by-design。

草案的特殊要求：
- 外國 AI 服務提供者須**指定泰國本地法定代表人**
- 需識別和分類 AI 系統（按泰國預期定義的「高風險」分類）
- AI 資料處理必須全生命週期維持 PDPA 基本原則

**對 Primax 的影響**：TH 工廠若部署 AI 系統（如 Chatbot Pilot 已列 TH 為受影響據點），需確認符合 PDPA + AI 指引要求。

### 4.4 新加坡：框架最成熟，但為自願性質

新加坡的 Model AI Governance Framework 已演進至**第三版**：
- 2020：傳統 AI 框架
- 2024：生成式 AI 框架（九大維度；70+ 全球組織參與，含 OpenAI、Google、Anthropic）
- 2026：Agentic AI 框架

三版均為**自願性質**，但 PDPA 是強制的，且 PDPC 已發布《AI 推薦和決策系統使用個人資料諮詢指引》（2024）。

**對 Primax 的影響**：Singapore 框架可作為 Primax 建立內部 AI 治理政策的**最佳實踐參考**——特別是其與 OECD AI Principles 的對齊設計，可實現跨法規互通。

---

## 5. 行動優先級總覽

### 時程甘特圖

```
2026 Q1 (Mar)     Q2 (Apr-Jun)        Q3 (Jul-Sep)       Q4 (Oct-Dec)        2027
─────────────────────────────────────────────────────────────────────────────────
█ Phase A/B 完成
  ├──── A01: AI 系統盤點 ────┤
  ├──── A02: PIPL SCC 啟動 ──┼──── A11: SCC 簽署/備案 ──┤
  ├── A03-A07: 各據點確認 ──┤
                            ├── A08: 風險分類 ──┤
                            ├── A09: Art.25 法律意見 ──┤
                              ├──── A10: 技術文件 ────────┤
                                                ┊ EU AI Act Art.6 ┊ (2026.08.02)
                                                ├── A16: 合規性評估 ──┤
                                                              ├── A22: ISO 42001 GA ──┤
                                                              ├── A23: AI 風險流程 ──┤
                                                                            ┊ EU PLD ┊ (2026.12.09)
```

### 誰需要做什麼

| 角色 | 行動 | 時程 |
|---|---|---|
| **DTO** (Glen Ho) | AI 系統盤點發起 + 協調、Art.4 素養確認、風險分類（初步）、ISO 42001 GA、合規自評自動化 | 持續 |
| **法務** | PIPL SCC 審查 + 備案、各據點合規確認、Art.25 外部法律意見、PLD 評估 | Q2 啟動 |
| **IT** | AI 系統技術資訊提供、資料清冊建置、技術文件配合、OT 安全評估 | Q2-Q3 |
| **Product/R&D** | ODM 產品 AI 盤點、技術文件撰寫、CE 認證配合 | Q2-Q3 |
| **HR** | AI 素養培訓合規確認、員工資料處理合規 | Q2 |
| **高管** | 外部法律顧問預算、ISO 42001 認證投資決策、AI 治理組織架構決策 | Q2 |

### 投資需求

| 項目 | 估計工作量 | 需外部資源？ |
|---|---|---|
| P0 合規急件（Q2 前） | 13-19 人週 | 部分（法務確認） |
| P1 截止日準備（Q2-Q3） | 18-29 人週 | **是**（外部 EU AI Act 律師） |
| P2 截止日前完成 | 12-18 人週 | 可能（合規性評估） |
| P3 治理制度化（Q3-Q4） | 11-16 人週 | 可能（ISO 42001 顧問） |
| **合計** | **54-82 人週** | |

---

## 6. 風險情境分析

### 情境 A：不行動（維持現狀）

| 風險 | 法規 | 可能後果 |
|---|---|---|
| CN→TW 資料流被查處 | PIPL | 最高全球營收 5% 罰款；CN 營運可能被要求暫停整改 |
| ODM 產品含 AI 未合規 | EU AI Act | 產品禁止在 EU 市場上市；最高 EUR 35M 罰款 |
| 資料洩漏未通報 | GDPR / PDPA | GDPR 最高營收 4%；PDPA 持續處罰 |
| 客戶要求合規證明無法提供 | 供應鏈壓力 | 失去 EU/KR/JP 客戶訂單 |

### 情境 B：僅做最低限度

完成 P0（各據點合規確認 + PIPL SCC），但不建立治理體系。

- **優點**：短期成本低
- **風險**：每次新法規出現都需要重新從零評估；無法回應客戶的系統性合規要求

### 情境 C：系統性建設（本報告建議）

P0 止血 → P1-P2 截止日準備 → P3 治理體系 → 持續改進。

- **優點**：一次投資，建立可複用的治理框架；可回應多國法規和客戶要求
- **成本**：54-82 人週 + 外部律師 + ISO 42001 顧問
- **回報**：合規風險降低；客戶信任提升；為 AI 規模化落地提供治理保障

---

## 7. 結語

致伸集團 2026 年的策略優先項中包括「跨國資料治理合規架構完成」和「AI 工具在製造現場的規模化落地」。本報告的核心訊息是：**這兩個目標是一體的——沒有治理，就沒有規模化**。

EU AI Act 不僅是一個合規義務，它正在重塑全球 AI 產品的市場准入規則。對 Primax 這樣的 ODM/EMS 製造商而言，Art.25 的 provider 責任意味著 AI 治理不再是「後台行政工作」，而是**直接影響產品能否在歐盟市場銷售的商業核心議題**。

PIPL 的跨境傳輸合規也是如此——中國工廠的營運資料流向台灣總部的每一天，都是在法規紅線上行走。2025 年的首例處罰案例已經證明，這不是理論風險。

建議的下一步：
1. **本週**：將本報告呈送法務長和資訊長，取得啟動 P0 的授權
2. **本月**：啟動 A01（AI 系統盤點）和 A02（PIPL SCC 啟動），同步確認各據點合規狀態
3. **下季**：完成風險分類、取得 Art.25 法律意見、啟動技術文件準備

---

## 附錄 A：法規原文引用索引

| # | 法規 | 條文 | 引用要點 | 來源 |
|---|---|---|---|---|
| R01 | EU AI Act | Art.25 | 產品製造商承擔 AI provider 義務的條件 | [EU AI Act Art.25](https://artificialintelligenceact.eu/article/25/) |
| R02 | EU AI Act | Art.6 + Annex III | 高風險 AI 系統的分類規則（8 大領域） | [EU AI Act Art.6](https://artificialintelligenceact.eu/article/6/) |
| R03 | EU AI Act | Art.4 | AI 素養義務（2025.02.02 生效） | [EU AI Act Art.4](https://artificialintelligenceact.eu/article/4/) |
| R04 | EU AI Act | Art.50 | 透明度義務（AI 系統需告知使用者） | [EU AI Act Art.50](https://artificialintelligenceact.eu/article/50/) |
| R05 | EU Digital Omnibus | 提案 | Annex III 延後至 2027.12.02（long-stop） | [Cooley Analysis](https://www.cooley.com/news/insight/2025/2025-11-24-eu-ai-act-proposed-digital-omnibus-on-ai-will-impact-businesses-ai-compliance-roadmaps) |
| R06 | PIPL | Art.38 | 跨境傳輸的三條合法路徑 | [Chambers](https://chambers.com/articles/the-final-piece-of-chinas-cross-border-personal-information-transfer-regulations) |
| R07 | PIPL SCC Measures | 全文 | 標準合同備案流程和時限 | [White & Case](https://www.whitecase.com/insight-alert/chinas-standard-contract-outbound-cross-border-transfer-personal-information-effect) |
| R08 | PIPL Certification | 辦法 | 認證途徑（2026.01.01 生效） | [Arnold & Porter](https://www.arnoldporter.com/en/perspectives/advisories/2025/11/china-requirements-personal-information-protection-certification) |
| R09 | Taiwan PDPA | Art.12 (2025 修正) | PDPC 違規通報義務 | [Jones Day](https://www.jonesday.com/en/insights/2025/12/taiwan-passes-major-amendments-to-the-personal-data-protection-act) |
| R10 | Taiwan PDPA | 修正全文 | 新設 PDPC、DPO、行政檢查權 | [Baker McKenzie](https://insightplus.bakermckenzie.com/bm/data-technology/taiwan-amendment-to-personal-data-protection-act) |
| R11 | GDPR | Art.30 | 處理活動記錄（ROPA） | [GDPR Full Text](https://gdpr-info.eu/art-30-gdpr/) |
| R12 | GDPR | Art.46 | SCCs 跨境傳輸機制 | [GDPR Full Text](https://gdpr-info.eu/art-46-gdpr/) |
| R13 | Thailand PDPA | AI Guidelines (draft) | 2026.02 AI 資料保護指引草案 | [FOSR Law](https://fosrlaw.com/2025/ai-data-privacy-thailand-2025/) |
| R14 | Korea AI Basic Act | 全文 | 2026.01.22 生效；風險分級制度 | [FPF Analysis](https://fpf.org/blog/south-koreas-new-ai-framework-act-a-balancing-act-between-innovation-and-regulation/) |
| R15 | Korea PIPA | 2023 修正 | 自動化決策的資料主體權利 | [Nature Academic](https://www.nature.com/articles/s41599-024-03470-y) |
| R16 | Japan AI Act | 全文 | 2025.05 通過；鼓勵自律路線 | [Chambers Japan](https://practiceguides.chambers.com/practice-guides/artificial-intelligence-2025/japan) |
| R17 | Japan APPI | 修正草案 | 跨境傳輸強化 + 行政罰金新增 | [AMT Law](https://www.amt-law.com/en/insights/others/publication_0029311_en_001/) |
| R18 | Singapore | Model AI Gov Framework v3 | 2026 Agentic AI 版本 | [IMDA](https://www.imda.gov.sg/resources/press-releases-factsheets-and-speeches/press-releases/2024/public-consult-model-ai-governance-framework-genai) |
| R19 | China | Cybersecurity Law Amendment | 2026.01.01 生效，新增 AI 合規條款 | [IAPP China](https://iapp.org/news/a/notes-from-the-asia-pacific-region-strong-start-to-2026-for-china-s-data-ai-governance-landscape) |
| R20 | EU PLD | Recast | 2026.12.09 成員國轉化；AI/軟體納入「產品」 | [Goodwin](https://www.goodwinlaw.com/en/insights/publications/2025/02/alerts-practices-aiml-eu-updates-its-product-liability-regime) |
| R21 | EU Machinery Reg. | 2023/1230 | 2027.01.20 適用；AI 安全元件 CE 認證 | [Medium Xeeniq](https://medium.com/@xeeniq/eu-ai-act-what-becomes-real-in-2026-the-automotive-playbook-for-2027-5f5c8d31bdf7) |
| R22 | ISO/IEC 42001 | 全文 | AI 管理系統標準（2023.12 發布） | [ISO](https://www.iso.org/standard/42001) |
| R23 | prEN 18286 | 草案 | EU AI Act 推定合規調和標準（開發中） | [CEN-CENELEC JTC21](https://jtc21.eu/wp-content/uploads/2025/06/CEN-CENELEC-JTC21-AI-Standards-Complete-Detailed-Overview.pdf) |
| R24 | IEC 62443 | 系列標準 | 工業自動化控制系統網路安全 | [ISA](https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards) |
| R25 | BIS EAR | AI Diffusion Rule (rescinded) | Trump 政府撤銷；基本出口管制仍在 | [Wiley](https://www.wiley.law/alert-BIS-Rescinds-AI-Diffusion-Rule) |
| R26 | NIST AI RMF | to ISO 42001 Crosswalk | 官方映射文件 | [NIST](https://airc.nist.gov/docs/NIST_AI_RMF_to_ISO_IEC_42001_Crosswalk.pdf) |

---

## 附錄 B：術語對照

| 英文 | 中文 | 說明 |
|---|---|---|
| AI Act Provider | AI 法案供應商 | 開發或以自身名義上市 AI 系統的主體 |
| AI Act Deployer | AI 法案部署者 | 在其權限下使用 AI 系統的主體 |
| Annex I | 附件一 | EU 產品安全立法清單（觸發高風險分類） |
| Annex III | 附件三 | 八大高風險 AI 使用場景清單 |
| ROPA | 處理活動記錄 | GDPR Art.30 要求的個資處理登記 |
| SCCs / SCC | 標準合同條款 | GDPR 或 PIPL 的跨境傳輸標準合同 |
| PIPIA | 個人信息保護影響評估 | PIPL 要求的跨境傳輸前評估 |
| DPIA | 資料保護影響評估 | GDPR Art.35 要求的高風險處理評估 |
| DPO | 資料保護長 | 各國法規要求指定的資料保護負責人 |
| AIMS | AI 管理系統 | ISO 42001 定義的管理系統 |
| ODM/EMS | 原始設計製造/電子製造服務 | Primax 的主要商業模式 |
| CE Marking | CE 標誌 | 歐盟產品合規標誌 |
| Harmonised Standard | 調和標準 | 滿足後可推定符合 EU 法規的標準 |

---

*Generated by DTO Intelligence System*
*Report ID: RR-2026-004*
*Classification: Internal — Executive Advisory*
*This report does not constitute legal advice. Items marked [needs_legal_review] require external legal counsel confirmation.*
