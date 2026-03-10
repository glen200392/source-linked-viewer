# 法規合規自評報告 — 2026-03-02

**報告編號**: CC-2026-001
**執行者**: data-governance-agent (compliance_check mode, first run)
**評估法規**: PIPL, GDPR, UK GDPR, PDPA, EU AI Act
**狀態**: Baseline Assessment (First Run)

---

## 執行摘要

| 指標 | 結果 |
|---|---|
| 評估法規 | **5** 項 |
| 整體評級 | **not_assessed** (多項關鍵維度缺乏公司層級資訊，無法判定) |
| 最緊迫風險 | PIPL 跨境傳輸 — 中國→台灣資料流合規機制狀態未知，需優先確認 |
| 最近截止日期 | **2026-08-02** (EU AI Act 高風險 AI 系統) — 距今 153 天 |

**關鍵結論**：本次為首次基線評估。DTO 系統層級僅能識別法規要求與已知資訊的差距，**無法代替公司層級的合規確認**。多數維度因缺乏法務、IT、HR 等部門的實際回覆而標記為 `not_assessed`。兩項 PIPL 相關維度基於 dto_context.json 的間接證據判定為「高度疑似不合規」，但需向 CN IT 和法務確認後才能定論。

---

## Primax 營運據點 × 法規對照矩陣

| 據點 | PIPL | GDPR | UK GDPR | PDPA | EU AI Act |
|---|---|---|---|---|---|
| **台灣總部 (TW)** | N/A | N/A | N/A | not_assessed | not_assessed |
| **中國工廠 (CN)** | **not_assessed** ⚠️ | N/A | N/A | N/A | N/A |
| **捷克 (CZ)** | N/A | **not_assessed** | N/A | N/A | not_assessed |
| **英國 (UK)** | N/A | N/A | **not_assessed** | N/A | N/A |
| **泰國 (TH)** | N/A | N/A | N/A | N/A | N/A |
| **日本 (JP)** | N/A | N/A | N/A | N/A | N/A |
| **美國 (US)** | N/A | N/A | N/A | N/A | N/A |

**圖例**：`not_assessed` = 無法判斷（缺乏公司層級資訊）；`not_assessed ⚠️` = 間接證據顯示高度疑似不合規，需優先向相關部門確認

---

## 各法規詳細評估

### PIPL（中國個人資訊保護法）

| 維度 | 狀態 | 差距描述 | 建議行動 | 優先級 |
|---|---|---|---|---|
| 資料清冊 | **not_assessed** ⚠️ | dto_context 僅記載「嚴格資料在地化」為約束條件，未提及資料清冊是否存在。**需向 CN IT 確認**：是否已有資料清冊？ | 優先向 CN IT 確認；若無，啟動 CN 據點資料流盤點 | **Critical** |
| 跨境傳輸 | **not_assessed** ⚠️ | dto_context 記載「資料平台需雙軌」，暗示 CN→TW 資料流存在，但 DTO 層級無法確認是否已建立 SCC 或其他合規路徑。**需向法務確認**：是否已簽署 SCC？ | 優先向法務確認；若無，啟動 PIPL 合規路徑評估 | **Critical** |
| PII 處理基礎 | **not_assessed** | 不知道 CN 據點處理哪些個資類型 | 啟動 CN 個資清冊 | High |
| 資料外洩通報 | **not_assessed** | 不知道是否有通報 SOP | 確認通報程序 | High |
| DPO | **not_assessed** | 不知道是否已指定 | 確認 DPO 指定狀態 | Medium |
| DPIA | **not_assessed** | 不知道是否對 AI Chatbot 做過影響評估 | 特別注意 chatbot_pilot 對 CN 據點的適用 | High |

**法規情報來源** [VERIFIED: KB ri_20260226_011]:
> 中國 2026 年 AI 治理強化：網絡安全法修訂正式生效（含 AI 條款），全國數據局計劃發布 30+ 項資料和 AI 標準

### GDPR（歐盟通用資料保護規範）

| 維度 | 狀態 | 差距描述 | 建議行動 | 優先級 |
|---|---|---|---|---|
| 資料清冊 (Art.30) | **not_assessed** | 不知道 CZ 據點是否有 ROPA | 確認捷克營運的 ROPA 狀態 | High |
| 跨境傳輸 (SCCs) | **not_assessed** | CZ→TW 資料流是否有 SCCs 不明；台灣無 EU adequacy decision | 啟動 SCCs 評估 | High |
| PII 處理基礎 | **not_assessed** | 不知道 CZ 據點的法律基礎選擇 | 確認 | Medium |
| 72hr 通報 | **not_assessed** | 不知道是否有通報 SOP | 確認 | High |
| DPO | **not_assessed** | 不知道是否已指定（特定情況必須） | 確認 | Medium |
| DPIA | **not_assessed** | 不知道是否對高風險處理做過評估 | 確認 | Medium |

### UK GDPR（英國）

| 維度 | 狀態 | 差距描述 | 建議行動 | 優先級 |
|---|---|---|---|---|
| 整體 | **not_assessed** | UK 據點的 GDPR 合規狀態不明 | 確認 UK 營運合規狀態 | Medium |
| UK↔EU | partial | EU adequacy 延至 2031，無需額外措施 | 持續監控 | Low |

### 台灣 PDPA（個人資料保護法）

| 維度 | 狀態 | 差距描述 | 建議行動 | 優先級 |
|---|---|---|---|---|
| PDPC 通報 | **not_assessed** | 2025.11 修正新設 PDPC，強制通報義務；不知道 Primax 是否已建立通報程序 | 確認通報 SOP | High |
| 隱私政策更新 | **not_assessed** | 不知道是否已依新法更新 | 確認 | Medium |
| 個資盤點 | **not_assessed** | 不知道台灣總部是否有個資清冊 | 啟動個資盤點 | High |

**DTO 系統自身的 PDPA 適用**：
- action_items.json 含員工姓名（PII）→ 適用 PDPA
- meetings_log.json 可能含參與者姓名 → 適用 PDPA
- meeting-ingestion-agent 已加入 PII 偵測步驟（v4.0 更新）

### EU AI Act

| 維度 | 狀態 | 差距描述 | 建議行動 | 優先級 |
|---|---|---|---|---|
| AI 模型清冊 | **not_assessed** ⚠️ | DTO 系統層級未發現模型清冊（SAP PP RAG 137 chunks 無 model card）。**需向 IT/Product 確認**：集團或事業部是否已有 AI 系統登錄？ | 優先向 IT/Product 確認；若無，建立 AI 模型登錄表 | **Critical** |
| 高風險 AI 識別 | **not_assessed** | 不知道 Primax 產品是否含 AI 元件，以及是否屬高風險類別 | 啟動 AI 產品盤點 | High |
| 員工培訓 (Art.4) | **partial** | digital_literacy 專案進行中，但不確定是否符合 Art.4 AI literacy 要求 | 確認 Art.4 覆蓋 | Medium |
| 技術文件 | **not_assessed** ⚠️ | DTO 系統層級未發現 AI 技術文件或 model card。**需向 IT/Product 確認**：產品線是否已有相關文件？ | 優先確認；若無，建立 model card template | High |

**法規情報來源** [VERIFIED: KB ri_20260226_007]:
> EU AI Act 關鍵節點：2026-02-02 高風險系統指南截止日已過，歐委會未能如期發布

**截止日期**：**2026-08-02** — 高風險 AI 系統要求生效，距今 153 天。

---

## 跨境資料傳輸風險評估

| # | 傳輸路徑 | 資料類型 | 法律基礎 | 狀態 | 建議 |
|---|---|---|---|---|---|
| 1 | **CN → TW** | 員工資料、營運資料 | PIPL SCC / 認證 | **未確認** ⚠️ | 優先向法務確認是否已有機制；若無，啟動 PIPL 合規路徑（3-6 個月） |
| 2 | **CZ → TW** | 營運資料 | GDPR SCCs | **未確認** | 確認 SCCs 狀態 |
| 3 | **UK → TW** | 營運資料 | UK GDPR SCCs | **未確認** | 確認 |
| 4 | **TW → CN** | 系統指令、培訓資料 | PIPL 安全評估 | **未確認** | 與 chatbot_pilot 一起評估 |
| 5 | **Any → US** | AI 模型權重 | BIS 出口管制 | **未確認** | 若使用美國 AI 技術，需評估 |

**特別風險** [VERIFIED: KB ri_20260302_002]:
> 美國防部將 Anthropic 列為供應鏈國安風險。若 Primax 使用 Claude 相關技術，需評估對美國客戶/合約的影響。

---

## Top 5 風險排序

| # | 風險 | 法規 | 潛在罰款 | 建議時程 |
|---|---|---|---|---|
| 1 | **CN→TW 資料流 PIPL 合規機制狀態未知** — 需優先確認 | PIPL | 全球營收 5% | 即刻向法務確認，若無機制則 3 個月內建立 |
| 2 | **AI 系統清冊和 model card 狀態未知** — 需優先確認 | EU AI Act | EUR 35M 或營收 7% | 即刻向 IT/Product 確認，若無則 3 個月內建立 |
| 3 | **PDPC 通報程序未建立** | PDPA | NT$20K-200K/次 | 1 個月內確認 |
| 4 | **CZ→TW 跨境傳輸 SCCs 不明** | GDPR | EUR 20M 或營收 4% | 3 個月內確認 |
| 5 | **AI 產品高風險分類未評估** | EU AI Act | 產品禁止上市 | 6 個月內（2026-08-02 前） |

---

## 建議行動計畫

### 即刻（本週）
1. 將 Top 5 風險轉為 action_items（指派負責人和截止日期）
2. 確認 PDPC 通報程序是否存在

### 短期（1-3 個月）
3. 啟動 CN 據點資料流盤點（PIPL 合規稽核）
4. 建立 AI 模型清冊（SAP PP RAG 先登錄，加 model card）
5. 確認 CZ 據點 GDPR ROPA 和 SCCs 狀態

### 中期（3-6 個月）
6. 啟動 PIPL 認證途徑申請
7. 完成所有 AI 系統的 EU AI Act 分類評估
8. 建立跨境傳輸控制機制

---

## 最新法規動態（KB 情報，近 30 天）

| 日期 | 來源 | 摘要 | 影響 |
|---|---|---|---|
| 2026-02-26 | KB ri_20260226_007 | EU AI Act 高風險系統指南截止日已過，歐委會延遲 | 合規準備時間仍然有限 |
| 2026-02-26 | KB ri_20260226_011 | 中國 AI 治理強化，全國數據局計劃發布 30+ 標準 | CN 工廠合規義務預期增加 |
| 2026-03-02 | KB ri_20260302_002 | 美國防部將 Anthropic 列為國安風險 | 若使用 Claude 需評估供應鏈影響 |

---

## 評估方法說明

本次為首次基線評估（baseline assessment）。

### 證據來源與局限性

| 來源 | 說明 | 局限性 |
|------|------|--------|
| `data/dto_context.json` | Primax 組織背景描述檔 | 僅記載約束條件和專案名稱，不記載合規措施實施狀態 |
| `data/knowledge_base.json` | DTO 情報系統累積的 56 條情報 | 僅包含外部法規動態，不包含公司內部合規資訊 |
| DTO 系統內部觀察 | 系統自身的資料處理行為 | 僅能觀察 DTO 系統層級，無法代表集團整體 |

### 判定標準

- **`not_assessed`**：缺乏公司層級資訊，無法判定合規狀態。這是誠實的「我不知道」。
- **`not_assessed ⚠️`**：間接證據顯示高度疑似不合規（例如：dto_context 提到需求但未提到已實施），需優先向相關部門確認。**這不等於「已確認不合規」**。
- **`partial`**：有部分措施但不完整。
- **`compliant`**：有明確證據確認合規（本次評估中未使用，因無法取得確認資訊）。

### 重要聲明

> **「DTO 系統未記載某項合規措施」不等於「公司未實施該措施」。**
>
> 本評估僅基於 DTO 系統可觸及的資訊。Primax 法務部門、各據點 IT、HR 等部門可能已有相關合規措施，但未被 DTO 系統所記錄。所有標記為 `not_assessed ⚠️` 的項目，應視為「優先確認清單」而非「違規清單」。

**下一步**：與法務、CN IT、CZ IT、HR 等部門合作，逐一確認各項目的實際狀態。將 `not_assessed` 項目轉為 `compliant`、`partial` 或 `non_compliant`。

---

*Generated by Compliance Check Pipeline — CC-2026-001*
*Next scheduled check: 2026-04-01 (monthly)*
