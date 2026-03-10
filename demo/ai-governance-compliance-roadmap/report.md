# AI 治理合規差距分析與路線圖

**報告編號**: RR-2026-003
**日期**: 2026-03-02
**作者**: Glen Ho (DTO Intelligence System)
**分類**: Internal — Compliance Roadmap
**狀態**: v1.0
**前置報告**: RR-2026-002（全球法規全景研究）、CC-2026-001（合規基線）
**風險計分公式**: `Risk Score = (罰則嚴重度 × 0.3) + (發生機率 × 0.25) + (時程緊迫度 × 0.25) + (營運衝擊 × 0.2)`

### 相關報告快速連結
| 報告 | 用途 |
|------|------|
| [RR-2026-002 全球法規全景研究](2026-03-02_ai-governance-global-landscape-research.md) | Phase A 37 來源、6 子題研究 |
| **本報告（RR-2026-003）** | Phase B 差距分析 + P0-P4 行動路線圖 |
| [RR-2026-004 AI 治理與資料治理建議報告](2026-03-02_ai-data-governance-recommendation-report.md) | 高管建議報告 |

---

## Executive Summary

基於 Phase A 研究（RR-2026-002）和 CC-2026-001 合規基線，本報告對 Primax Group 進行全法規範圍的合規差距分析，並產出分層行動路線圖。

### 關鍵數字

| 指標 | 數值 |
|---|---|
| 評估法規/標準數 | **25**（7 Tier 1 + 7 Tier 2 + 11 Tier 3） |
| 識別合規差距 | **32** 項 |
| Critical 等級 | **5** 項 |
| High 等級 | **10** 項 |
| Medium 等級 | **12** 項 |
| Low 等級 | **5** 項 |
| 行動項目 | **28** 項（P0: 7 / P1: 8 / P2: 6 / P3: 4 / P4: 3） |
| 最近截止日 | **2026-08-02**（EU AI Act Art.6，原始時程） |

---

## 1. 全法規評估矩陣

### 1.1 Tier 1: 直接適用法規

#### EU AI Act

| 維度 | 評估 |
|---|---|
| **適用性** | ✅ 直接適用：CZ 據點 + 對 EU 市場銷售產品 |
| **適用實體** | Primax CZ（deployer）; Primax 總部（若 ODM 產品含 AI → provider per Art.25） |
| **現行合規狀態** | `not_assessed` ⚠️（DTO 層級未發現 AI 系統清冊或技術文件，但需向 IT/Product 確認集團是否已有相關機制） |
| **差距描述** | (1) 全集團 AI 系統盤點狀態未確認 (2) 無 Annex III/I 風險分類 (3) Art.4 AI 素養合規未確認 (4) 技術文件狀態未確認 (5) ODM 產品 AI 責任未釐清 |
| **風險等級** | **Critical** |
| **罰則** | 最高 EUR 35M 或全球營收 7%；Annex I 產品可被禁止上市 |
| **時程壓力** | Art.4 已生效；Art.6 Annex III 2026.08.02（~153 天）；Annex I 2027.08.02 |
| **Risk Score** | **9.1/10**（罰則 10 × 0.3 + 機率 8 × 0.25 + 時程 9 × 0.25 + 營運 9 × 0.2） |

#### PIPL（中國個人信息保護法）

| 維度 | 評估 |
|---|---|
| **適用性** | ✅ 直接適用：CN 工廠 |
| **適用實體** | Primax CN 子公司 |
| **現行合規狀態** | `not_assessed` ⚠️（dto_context 間接證據顯示高度疑似不合規，但需向法務和 CN IT 確認實際狀態） |
| **差距描述** | (1) 資料清冊狀態未確認 (2) CN→TW 跨境傳輸合規路徑狀態未確認（dto_context 提到「雙軌」需求但未記載實施情況） (3) PII 處理類型未確認 (4) 通報 SOP 狀態未確認 (5) DPO 指定狀態未確認 |
| **風險等級** | **Critical** |
| **罰則** | 最高全球營收 5%；嚴重違規可暫停中國營運 |
| **時程壓力** | 已生效，無寬限期；2025 年執法力度上升（上海首例跨境傳輸處罰） |
| **Risk Score** | **9.3/10**（罰則 9 × 0.3 + 機率 9 × 0.25 + 時程 10 × 0.25 + 營運 10 × 0.2） |

#### GDPR

| 維度 | 評估 |
|---|---|
| **適用性** | ✅ 直接適用：CZ 據點 |
| **適用實體** | Primax CZ |
| **現行合規狀態** | `not_assessed`（ROPA、SCCs、DPO 狀態均不明） |
| **差距描述** | (1) CZ ROPA (Art.30) 狀態不明 (2) CZ→TW 跨境傳輸 SCCs 狀態不明 (3) DPO 指定狀態不明 (4) 72hr 通報 SOP 不明 |
| **風險等級** | **High** |
| **罰則** | 最高 EUR 20M 或全球營收 4% |
| **時程壓力** | 已生效 |
| **Risk Score** | **7.4/10**（罰則 8 × 0.3 + 機率 6 × 0.25 + 時程 8 × 0.25 + 營運 7 × 0.2） |

#### UK Data Protection Act / UK GDPR

| 維度 | 評估 |
|---|---|
| **適用性** | ✅ 直接適用：UK 據點 |
| **適用實體** | Primax UK |
| **現行合規狀態** | `not_assessed` |
| **差距描述** | UK 據點整體合規狀態不明；UK↔EU adequacy 延至 2031 |
| **風險等級** | **Medium** |
| **罰則** | 最高 GBP 17.5M 或全球營收 4% |
| **時程壓力** | 已生效；UK AI regulation 框架演進中但無硬性截止日 |
| **Risk Score** | **5.8/10** |

#### Taiwan PDPA（個資法）

| 維度 | 評估 |
|---|---|
| **適用性** | ✅ 直接適用：TW 總部 |
| **適用實體** | Primax TW（所有 TW 實體） |
| **現行合規狀態** | `not_assessed`（PDPC 通報程序、個資盤點、隱私政策更新均不明） |
| **差距描述** | (1) PDPC 通報義務程序不明 (2) 個資盤點未確認 (3) 2025 修法後隱私政策是否更新不明 (4) 無 AI 專門條款但 PDPC 可能成為未來 AI 監管入口 |
| **風險等級** | **High** |
| **罰則** | NT$20K-200K/次（可持續處罰） |
| **時程壓力** | 2025.11 修正已施行 |
| **Risk Score** | **6.5/10** |

#### Thailand PDPA

| 維度 | 評估 |
|---|---|
| **適用性** | ✅ 直接適用：TH 工廠 |
| **適用實體** | Primax TH |
| **現行合規狀態** | `not_assessed` |
| **差距描述** | (1) TH 據點 PDPA 合規狀態不明 (2) 2026.02 AI 資料保護指引草案需關注 (3) DPO 指定義務（TH PDPA 必須） |
| **風險等級** | **Medium** |
| **罰則** | 最高 THB 5M；行政 + 刑事處罰可能 |
| **時程壓力** | 已生效；AI 指引草案 2026 |
| **Risk Score** | **5.2/10** |

#### BIS AI Export Controls (EAR)

| 維度 | 評估 |
|---|---|
| **適用性** | ✅ 間接適用：使用美國來源 AI 技術 |
| **適用實體** | 所有使用 US-origin AI（如 Anthropic Claude）的實體 |
| **現行合規狀態** | `not_assessed` |
| **差距描述** | (1) 未評估 Claude 使用是否觸發 EAR 義務 (2) Trump 政府已撤銷 AI Diffusion Rule 但基本出口管制仍在 (3) 客戶供應鏈合規要求不明 |
| **風險等級** | **Medium** |
| **罰則** | 刑事處罰可能；客戶關係風險 |
| **時程壓力** | 已生效；政策方向不穩定 |
| **Risk Score** | **4.8/10** |

### 1.2 Tier 2: 間接適用法規（概要評估）

| 法規 | 適用性 | 狀態 | 風險 | 行動 |
|---|---|---|---|---|
| **Japan APPI + AI Act** | 若有日系客戶 | `not_assessed` | Low | 確認日系客戶合規要求 |
| **Korea PIPA + AI Basic Act** | 若有韓系客戶 | `not_assessed` | Low | 監控；2026.01 生效 |
| **Singapore PDPA + AI Framework** | SEA 業務參考 | N/A | Low | 自願框架，作為最佳實踐 |
| **US AI Policy** | 美系客戶 | `not_assessed` | Medium | 監控政策演變 |
| **Canada AIDA** | 北美客戶 | N/A | Low | 仍在立法中 |
| **India DPDP Act** | 若有印度供應鏈 | N/A | Low | 規則制定中 |
| **Brazil LGPD** | 若有拉美業務 | N/A | Low | 已生效但影響有限 |

### 1.3 Tier 3: 國際標準/框架（差距評估）

| 標準 | 現行狀態 | 差距 | 建議 |
|---|---|---|---|
| **ISO 42001** | 未採用 | 無 AI 管理系統 | Q3-Q4 gap analysis |
| **ISO 23894** | 未採用 | 無 AI 風險管理方法論 | 與 42001 一起 |
| **NIST AI RMF** | 未採用 | 無系統性 AI 風險管理 | 可與 42001 整合 |
| **ISO 27001** | `not_assessed` | 需確認 Primax 現有認證 | 確認狀態 |
| **ISO 27701** | `not_assessed` | 需確認 | 確認狀態 |
| **IEC 62443** | `not_assessed` | OT 安全與 AI 整合 | Q3-Q4 評估 |
| **ISO 9001** | 應已認證 `[INFERRED]` | AI 整合進 QMS | 利用現有框架 |
| **prEN 18286** | 草案階段 | 追蹤用 | 追蹤發布進度 |
| **OECD AI Principles** | 未正式採用 | 原則層面 | 作為政策參考 |
| **G7 Hiroshima AI Process** | 未正式採用 | 自願行為準則 | 參考 |
| **IEEE 7000** | 未採用 | 倫理驅動設計 | 長期參考 |

---

## 2. 風險計分排序（Top 15）

```
Risk Score = (罰則嚴重度 × 0.3) + (發生機率 × 0.25) + (時程緊迫度 × 0.25) + (營運衝擊 × 0.2)
各因子以 1-10 scale 評分
```

**注意**：以下風險分數基於「若確認為不合規」的假設情境。標記 ⚠️ 的項目尚未經公司層級確認，實際風險可能因既有合規措施而降低。

| 排名 | 風險 | 法規 | Score | 罰則 | 機率 | 時程 | 營運 |
|---|---|---|---|---|---|---|---|
| **1** | CN→TW 跨境傳輸合規機制狀態未確認 ⚠️ | PIPL | **9.3** | 9 | 9 | 10 | 10 |
| **2** | ODM 產品 AI 責任未釐清 | EU AI Act Art.25 | **9.1** | 10 | 8 | 9 | 9 |
| **3** | 全集團 AI 系統清冊狀態未確認 ⚠️ | EU AI Act / 多法規 | **8.5** | 8 | 10 | 9 | 7 |
| **4** | EU Product Liability Directive 適用 | PLD | **7.8** | 8 | 7 | 8 | 8 |
| **5** | CZ 據點 GDPR 合規狀態不明 | GDPR | **7.4** | 8 | 6 | 8 | 7 |
| **6** | AI 系統無技術文件 | EU AI Act | **7.2** | 7 | 8 | 7 | 7 |
| **7** | Taiwan PDPC 通報程序未建立 | PDPA | **6.5** | 4 | 7 | 8 | 7 |
| **8** | AI 素養合規未確認 | EU AI Act Art.4 | **6.3** | 5 | 7 | 9 | 4 |
| **9** | 中國 AI 標準化新規 | CN regulations | **6.0** | 6 | 6 | 6 | 7 |
| **10** | Thailand PDPA + AI 指引 | TH PDPA | **5.2** | 4 | 5 | 6 | 6 |
| **11** | BIS 出口管制評估 | EAR | **4.8** | 6 | 3 | 5 | 6 |
| **12** | UK 據點 DPA 合規 | UK GDPR | **4.5** | 5 | 3 | 5 | 5 |
| **13** | ISO 42001 認證缺失 | ISO 42001 | **4.0** | 2 | 5 | 4 | 6 |
| **14** | OT + AI 安全治理 | IEC 62443 | **3.8** | 3 | 4 | 3 | 5 |
| **15** | EU Machinery Regulation AI | Mach. Reg. | **3.5** | 5 | 2 | 3 | 5 |

---

## 3. 分層合規路線圖

### P0: 立即行動（2026-04-30 前）

| # | 行動 | 法規依據 | 負責 | 工作量 | 前置依賴 |
|---|---|---|---|---|---|
| **A01** | **全集團 AI 系統盤點確認** — 先向 IT/Product 確認是否已有 AI 系統清冊；若無，啟動盤點（含 chatbot pilot、war room、SAP PP RAG、ODM 產品 AI、工廠 AI 視覺檢測等） | EU AI Act / 多法規 | DTO + IT + Product | 確認 1 週；若需盤點 3-4 人週 | 無 |
| **A02** | **PIPL CN→TW 跨境機制確認** — 先向法務和 CN IT 確認是否已有 SCC 或其他合規路徑；若無，盤點 CN→TW 資料流、啟動 PIPIA、選定合規路徑 | PIPL Art.38 | DTO + Legal + CN IT | 確認 1 週；若需建立 4-6 人週 | A01 部分完成 |
| **A03** | **Taiwan PDPC 通報 SOP 確認** — 確認是否已建立 PDPC 違規通報程序；若無，建立 SOP | PDPA Art.12 (2025修正) | Legal + IT Security | 1-2 人週 | 無 |
| **A04** | **EU AI Act Art.4 AI 素養確認** — 確認 digital_literacy 計畫是否符合 Art.4 具體要求 | EU AI Act Art.4 | DTO + HR | 1 人週 | 無 |
| **A05** | **CZ 據點 GDPR 狀態確認** — 確認 ROPA、SCCs、DPO、通報 SOP 的現行狀態 | GDPR Art.30+ | Legal + CZ HR/IT | 2-3 人週 | 無 |
| **A06** | **Thailand PDPA 合規確認** — 確認 TH 工廠 DPO 指定、資料處理登記、通報 SOP | TH PDPA | Legal + TH HR/IT | 1-2 人週 | 無 |
| **A07** | **UK DPA 合規狀態確認** — 確認 UK 據點基本合規狀態 | UK DPA 2018 | Legal + UK HR/IT | 1 人週 | 無 |

**P0 總工作量估計**: 13-19 人週
**P0 關鍵路徑**: A01（AI 系統盤點）是幾乎所有後續行動的前置條件

### P1: 短期行動（2026-06-30 前）

| # | 行動 | 法規依據 | 負責 | 工作量 | 前置依賴 |
|---|---|---|---|---|---|
| **A08** | **EU AI Act 風險分類完成** — 基於 A01 清冊，對照 Annex III/I 分類每個 AI 系統 | EU AI Act Art.6 | DTO + Legal | 2-3 人週 | A01 |
| **A09** | **ODM 產品 AI 責任釐清** — 與法務確認 Art.25 下 Primax 的義務範圍；需外部法律意見 | EU AI Act Art.25 | Legal (外部) | 2-4 人週 | A01, A08 |
| **A10** | **高風險 AI 技術文件啟動** — 若 A08 確認有高風險系統，啟動 Annex IV 技術文件準備 | EU AI Act Art.11 | IT + Product | 4-8 人週 | A08 |
| **A11** | **PIPL SCC 簽署 + 備案** — 完成 PIPIA、與 TW 總部簽署 SCC、向省級 CAC 備案 | PIPL SCC 辦法 | Legal + CN IT | 3-4 人週 | A02 |
| **A12** | **CZ→TW 跨境傳輸 SCCs 建立** — 若 A05 確認無 SCCs，啟動 GDPR SCCs 程序 | GDPR Art.46 | Legal | 2-3 人週 | A05 |
| **A13** | **CN 據點資料清冊建立** — 盤點 CN 據點處理的所有個人資訊類型和數量 | PIPL | CN IT + Legal | 2-3 人週 | A02 |
| **A14** | **Taiwan 個資盤點** — 確認 TW 總部的個資清冊 | PDPA | IT + Legal | 2 人週 | 無 |
| **A15** | **EU AI Act 透明度義務準備** — 確保所有 AI 系統（特別是 chatbot）符合 Art.50 告知義務 | EU AI Act Art.50 | IT + Product | 1-2 人週 | A01 |

**P1 總工作量估計**: 18-29 人週
**P1 關鍵路徑**: A08→A09→A10（風險分類→責任釐清→技術文件）

### P2: 截止日前（2026-08-02 前）

| # | 行動 | 法規依據 | 負責 | 工作量 | 前置依賴 |
|---|---|---|---|---|---|
| **A16** | **高風險 AI 合規性評估** — 若有高風險系統，完成自我合規性評估或第三方評估 | EU AI Act Art.43 | Product + Legal | 4-6 人週 | A10 |
| **A17** | **上市後監控機制建立** — 建立高風險 AI 系統的持續監控計畫 | EU AI Act Art.72 | IT + Product | 2-3 人週 | A16 |
| **A18** | **跨據點一致性驗證** — 確認所有據點的合規措施一致且無遺漏 | 多法規 | DTO + Legal | 2-3 人週 | A05-A07 |
| **A19** | **AI 系統登記至 EU Database** — 若有高風險系統，完成歐盟資料庫登記 | EU AI Act Art.71 | Product + Legal | 1 人週 | A16 |
| **A20** | **EU Product Liability Directive 準備** — 評估 PLD 2026.12 對 Primax 產品的影響 | PLD (recast) | Product + Legal | 2-3 人週 | A09 |
| **A21** | **BIS 出口管制評估** — 評估 Claude 使用和其他 US-origin AI 技術的 EAR 合規性 | EAR | Legal + DTO | 1-2 人週 | 無 |

**P2 總工作量估計**: 12-18 人週

### P3: 中期建設（2026-Q3/Q4）

| # | 行動 | 法規依據 | 負責 | 工作量 | 前置依賴 |
|---|---|---|---|---|---|
| **A22** | **ISO 42001 差距分析 + 認證規劃** — 評估現有實踐與 ISO 42001 要求的差距 | ISO 42001 | DTO + Quality | 4-6 人週 | A01 |
| **A23** | **AI 風險管理流程制度化** — 建立系統性的 AI 風險識別、評估、管理流程 | ISO 23894 + NIST AI RMF | DTO + Risk Mgmt | 3-4 人週 | A22 |
| **A24** | **供應鏈 AI 合規要求傳遞** — 調查客戶的 AI 合規期待；建立供應商 AI 合規要求 | 多法規 | Product + Procurement | 2-3 人週 | A09 |
| **A25** | **定期合規自評自動化** — 將 /compliance-check 擴展為涵蓋所有 Tier 1 法規的自動化評估 | 多法規 | DTO | 2-3 人週 | A08, A18 |

**P3 總工作量估計**: 11-16 人週

### P4: 長期監控（2027+）

| # | 行動 | 法規依據 | 負責 | 工作量 |
|---|---|---|---|---|
| **A26** | **EU AI Liability Directive 準備** — 追蹤立法進展，評估對 Primax 的影響 | EU AILD | Legal + Product | 持續 |
| **A27** | **EU Machinery Regulation AI 合規** — 評估 ODM 產品中 AI 安全元件的 CE 認證需求 | Mach. Reg. 2023/1230 | Product + Quality | 4-6 人週（2026 Q4 啟動） |
| **A28** | **中國 AI 標準化追蹤 + ASEAN AI Guide 追蹤** — 監控新發布的標準和指引 | CN + ASEAN | DTO | 持續 |

---

## 4. 利害關係人行動表

### 4.1 DTO 可直接執行（Glen Ho 範疇）

| # | 行動 | 說明 |
|---|---|---|
| A01 | AI 系統盤點（啟動和協調） | DTO 可發起並建立盤點框架；需各部門配合提供資訊 |
| A04 | Art.4 AI 素養確認 | 對照 Art.4 要求評估 digital_literacy 計畫 |
| A08 | EU AI Act 風險分類（初步） | DTO 可做初步分類建議；最終需法務確認 |
| A15 | 透明度義務準備 | 確保 chatbot 告知使用者為 AI 互動 |
| A22 | ISO 42001 差距分析 | DTO 可主導 |
| A23 | AI 風險管理流程設計 | DTO 可主導框架設計 |
| A25 | 合規自評自動化 | DTO Intelligence System 技術實現 |

### 4.2 需要公司法務參與

| # | 行動 | 法務參與範圍 |
|---|---|---|
| A02 | PIPL 跨境機制 | SCC 法律審查 + 備案 |
| A05 | CZ GDPR 確認 | 法律合規狀態確認 |
| A06 | TH PDPA 確認 | 法律合規狀態確認 |
| A07 | UK DPA 確認 | 法律合規狀態確認 |
| A09 | ODM AI 責任釐清 | **需外部法律意見** — Art.25 適用性判斷 |
| A11 | PIPL SCC 簽署 | 法律文件審查和簽署 |
| A12 | GDPR SCCs 建立 | 法律文件準備 |
| A20 | EU PLD 評估 | 產品責任法律分析 |
| A21 | BIS 出口管制評估 | 出口管制法律分析 |

### 4.3 需要高管決策

| # | 行動 | 決策內容 | 決策層級 |
|---|---|---|---|
| A09 | ODM AI 責任策略 | 是否接受 Art.25 provider 義務；商業模式影響 | C-Suite / Board |
| A22 | ISO 42001 認證投資 | 認證預算和組織資源 | VP/CTO |
| A24 | 供應鏈合規要求 | 是否主動要求供應商 AI 合規 | VP Supply Chain |
| — | 全集團 AI 治理組織架構 | 是否設立 AI Governance Committee | C-Suite |
| — | 外部法律顧問預算 | EU AI Act + PIPL 專業法律意見 | VP Legal |

### 4.4 需要跨部門協作

| # | 行動 | 涉及部門 |
|---|---|---|
| A01 | AI 系統盤點 | IT + Product + Manufacturing + R&D + HR |
| A02 | PIPL 跨境機制 | CN IT + TW IT + Legal + HR |
| A03 | PDPC 通報 SOP | Legal + IT Security + HR |
| A10 | 技術文件準備 | IT + Product + R&D + Quality |
| A13 | CN 資料清冊 | CN IT + CN HR + CN Manufacturing |

---

## 5. EU AI Act 倒推時程表（更新版）

| 里程碑 | 目標日期 | 距今天數 | 狀態 |
|---|---|---|---|
| ~~Phase A 研究完成~~ | 2026-03-02 | 0 | ✅ 完成（本報告） |
| P0 啟動：AI 系統盤點 + PIPL 機制 | 2026-03-15 | ~13 天 | 🔜 待啟動 |
| P0 完成：初步盤點 + 各據點狀態確認 | 2026-04-30 | ~59 天 | |
| P1：風險分類完成 | 2026-05-15 | ~74 天 | |
| P1：ODM AI 責任法律意見取得 | 2026-06-15 | ~105 天 | |
| P1/P2：技術文件完成（若為高風險） | 2026-06-30 | ~120 天 | |
| P2：合規性評估完成 | 2026-07-15 | ~135 天 | |
| P2：跨據點一致性驗證 | 2026-07-31 | ~151 天 | |
| **EU AI Act Art.6 生效** | **2026-08-02** | **~153 天** | ⏰ Deadline |
| P2：EU PLD 成員國轉化截止 | 2026-12-09 | ~282 天 | |
| P3：ISO 42001 gap analysis 完成 | 2026-12-31 | ~304 天 | |
| EU Machinery Regulation 適用 | 2027-01-20 | ~324 天 | |
| **Digital Omnibus Annex III 延期** | **2027-12-02** | **~639 天** | ⚠ 提案中 |

---

## 6. 風險緩解 — 若 Omnibus 未通過

若 Digital Omnibus 未通過或大幅修改，Primax 面臨的最高風險場景：

| 場景 | 影響 | 緩解 |
|---|---|---|
| Annex III 2026.08.02 如期生效 | 若有高風險 AI 系統，需在 153 天內完成所有合規義務 | P0-P1 盡早啟動；非高風險系統可降低壓力 |
| 調和標準未及時發布 | 無推定合規標準可依循 | 直接對照法規要求自評；Art.40 可使用 common specifications |
| 客戶要求提前合規 | EU 客戶可能在截止日前要求供應商合規證明 | A24 供應鏈調查提前至 P1 |

---

## 研究方法與限制

### 方法
- 風險計分基於 4 因子加權模型（罰則 30% + 機率 25% + 時程 25% + 營運 20%）
- 營運衝擊新增考量：產品市場准入風險 + 供應鏈客戶合規要求
- 差距評估結合 CC-2026-001 基線和 Phase A 研究
- 路線圖遵循 EU AI Act 倒推時程

### 限制
1. **多數 `not_assessed` 項目需內部確認**：特別是 CZ、UK、TH 據點的合規狀態
2. **工作量估計為粗估**：實際取決於公司規模、現有合規成熟度、外部支援
3. **法律意見邊界**：A09（Art.25 責任）、A20（PLD）、A21（BIS）需外部法律專家
4. **Digital Omnibus 不確定性**：可能顯著改變時程，但不應依賴

---

*Generated by DTO Intelligence System — Phase B Compliance Roadmap*
*Report ID: RR-2026-003*
*前置報告: RR-2026-002 (Phase A Research), CC-2026-001 (Compliance Baseline)*
*Next action: 啟動 P0 行動項目（A01-A07）*
