# Phase C: AI 治理政策與制度框架設計

**Document**: Phase C Framework Design
**Date**: 2026-03-03
**Author**: DTO (Glen Ho) + Claude Code
**Status**: Draft for Management Review
**Prerequisites**: Phase A (RR-2026-002) + Phase B (RR-2026-003) + RR-2026-004 completed
**Classification**: Internal / Confidential

---

## 1. Executive Summary

Phase C 是 Primax AI 治理計畫從「合規救火」轉型為「系統化治理」的關鍵階段。在 Phase A（法規研究）和 Phase B（差距分析 + 路線圖）完成後，Phase C 的目標是建立一套可持續運作的 AI 治理制度，使合規不再依賴一次性專案，而是嵌入組織日常營運。

**核心框架**：以 ISO/IEC 42001 為骨幹，映射 EU AI Act、PIPL、GDPR 等多法規要求，整合現有 ISO 9001 QMS。

**預計投入**：11-16 人週（A22-A25），2026 Q3-Q4 執行。

---

## 2. Phase C 架構總覽

```
┌─────────────────────────────────────────────────────────┐
│                  AI Governance Committee                 │
│          (CTO/VP-level, quarterly cadence)               │
│  Decision authority: policy approval, risk acceptance,   │
│  budget allocation, escalation resolution                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Policy      │  │   Risk       │  │   Compliance │  │
│  │   Framework   │  │   Management │  │   Monitoring │  │
│  │              │  │              │  │              │  │
│  │ • AI Policy  │  │ • Risk ID    │  │ • Quarterly  │  │
│  │ • Ethics     │  │ • Assessment │  │   self-assess│  │
│  │   Charter    │  │ • Mitigation │  │ • Regulatory │  │
│  │ • Use Case   │  │ • Monitoring │  │   watch      │  │
│  │   Approval   │  │              │  │ • Action     │  │
│  │   Process    │  │              │  │   tracking   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  │
│         │                 │                 │           │
│  ┌──────┴─────────────────┴─────────────────┴───────┐   │
│  │            ISO 42001 AI Management System         │   │
│  │     (integrated with existing ISO 9001 QMS)       │   │
│  └──────────────────────┬────────────────────────────┘   │
│                         │                               │
│  ┌──────────────────────┴────────────────────────────┐   │
│  │              Data Governance Layer                 │   │
│  │  Data Catalog │ Classification │ Cross-Border     │   │
│  │  ROPA │ DPIA/PIPIA │ Breach Notification          │   │
│  └───────────────────────────────────────────────────┘   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐   │
│  │              Automation Layer (AO OS)              │   │
│  │  gov-orchestrator │ regulation-monitor │           │   │
│  │  gap-assessor │ progress-tracker │ /compliance-check│  │
│  └───────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 組織架構設計

### 3.1 AI Governance Committee（AI 治理委員會）

| 項目 | 設計 |
|------|------|
| **層級** | CTO/VP-level（需管理層決定最終組成） |
| **成員** | CTO（主席）、VP Legal、VP Product、VP IT、DTO Head、Risk Mgmt、HR（依需要） |
| **會議頻率** | 季度定期 + 重大事件臨時召開 |
| **決策範圍** | 政策核准、風險接受決策、ISO 42001 認證決定、預算分配、跨部門協調 |
| **秘書處** | DTO（負責議程準備、會議紀錄、追蹤決議執行） |

### 3.2 RACI Matrix（責任分工矩陣）

| 職能 | 角色定位 | Phase C 主要責任 |
|------|---------|-----------------|
| **DTO** | AI 治理推動辦公室 | A01 協調、A22 ISO 42001 GA lead、A23 風險流程設計、A25 自動化、regulatory_watch 營運 |
| **Legal** | 法規合規顧問 | A02/A05-A07 合規確認、A09 外部法律意見、A11-A12 SCC 簽署、政策法律審核 |
| **IT** | 技術實施 | A01 系統技術資訊、資料目錄建置、技術文件支援、OT 安全評估 |
| **Product/R&D** | 產品合規 | A01 ODM 產品 AI 盤點、A10 技術文件、CE 認證協調 |
| **HR** | 人員合規 | A04 AI 素養培訓、員工資料處理合規 |
| **Quality** | 管理系統整合 | ISO 42001 × ISO 9001 整合、稽核程序、認證準備 |
| **Management** | 決策與資源 | 預算、認證決定、AI 治理委員會主持 |

### 3.3 具體 RACI（Phase C 核心行動項）

| 行動 | DTO | Legal | IT | Product | Quality | Mgmt |
|------|-----|-------|-----|---------|---------|------|
| A22 ISO 42001 GA | **R** | C | C | C | **A** | I |
| A23 Risk Mgmt Process | **R** | C | C | C | **A** | I |
| A24 Supply Chain Compliance | I | C | - | **R** | - | **A** |
| A25 Compliance Automation | **R/A** | C | C | - | - | I |
| AI Policy Drafting | **R** | **A** | C | C | C | I→A |
| Ethics Charter | **R** | C | - | C | - | **A** |
| Governance Committee Setup | **R** | C | - | - | - | **A** |

> R = Responsible, A = Accountable, C = Consulted, I = Informed

---

## 4. 政策框架（Policy Framework）

### 4.1 政策體系結構

```
Level 1: AI Governance Policy（總政策）
  ├── Level 2: AI Risk Management Policy
  ├── Level 2: AI Ethics Charter
  ├── Level 2: AI Data Governance Policy
  ├── Level 2: AI System Lifecycle Management Policy
  └── Level 2: AI Incident Response Policy

Level 3: Standard Operating Procedures (SOPs)
  ├── SOP-001: AI System Registration & Classification
  ├── SOP-002: AI Risk Assessment Procedure
  ├── SOP-003: AI Use Case Approval Workflow
  ├── SOP-004: Cross-Border Data Transfer Procedure
  ├── SOP-005: AI Incident Reporting Procedure
  ├── SOP-006: Regulatory Change Management Procedure
  └── SOP-007: AI Vendor/Third-Party Assessment Procedure

Level 4: Working Instructions & Templates
  ├── AI System Inventory Template
  ├── Risk Assessment Worksheet
  ├── DPIA/PIPIA Template
  └── Conformity Self-Assessment Checklist
```

### 4.2 核心政策概要

#### Policy 1: AI Governance Policy（總政策）

| 章節 | 內容 |
|------|------|
| 目的 | 建立 Primax 集團 AI 系統開發、部署與營運的治理原則和責任架構 |
| 適用範圍 | 所有 AI 系統（內部使用 + ODM 產品），全球 7 國據點 |
| 治理原則 | (1) 合法合規 (2) 透明可解釋 (3) 人類監督 (4) 安全可靠 (5) 公平無歧視 (6) 隱私保護 (7) 問責制 |
| 組織架構 | AI Governance Committee + DTO 推動辦公室 + 各事業單位 AI Owner |
| 風險管理 | AI 系統分級 → 風險評估 → 控制措施 → 監控 → 報告 |
| 合規要求 | 依 AI 系統部署地區對照適用法規（regulatory_scope） |
| 審核機制 | 年度內部稽核 + 季度自評 + ISO 42001 外部稽核（if certified） |
| 文件管理 | 版本控制、核准流程、分發記錄 |

#### Policy 2: AI Risk Management Policy

| 面向 | 設計（ISO 23894 + NIST AI RMF 融合） |
|------|------|
| 風險識別 | 系統清冊 × 法規對照 → 風險清單（risk_register） |
| 風險評估 | `risk_score = impact × probability × (1 - mitigation_effectiveness)` |
| 風險分級 | Critical (≥8.0) → High (6.0-7.9) → Medium (4.0-5.9) → Low (<4.0) |
| 控制措施 | Technical controls + Organizational controls + Legal controls |
| 監控頻率 | Critical: 即時 / High: 月度 / Medium: 季度 / Low: 年度 |
| 殘餘風險 | 由 AI Governance Committee 決定是否接受 |
| 工具支援 | gap-assessor agent（Mode: incremental + targeted） |

#### Policy 3: AI Ethics Charter

| 原則 | Primax 承諾 | 對應法規 |
|------|------------|---------|
| 透明性 | AI 系統使用告知、自動化決策說明 | EU AI Act Art.13, PIPL Art.24 |
| 公平性 | 防止演算法歧視、定期偏見檢測 | EU AI Act Art.10, Colorado AI Act |
| 人類監督 | 高風險 AI 保留人類覆核權 | EU AI Act Art.14 |
| 安全性 | AI 系統可靠性測試、失效安全設計 | EU AI Act Art.9, Machinery Reg. |
| 隱私保護 | 最小化資料收集、目的限制 | PIPL, GDPR, PDPA |
| 問責制 | 每個 AI 系統指定負責人、稽核軌跡 | ISO 42001 Clause 5 |
| 永續性 | 考量 AI 系統環境影響（能耗、碳排） | EU AI Act Art.11(1)(e) |

---

## 5. AI 系統生命週期治理

### 5.1 生命週期階段管控

```
    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
    │ Request  │───→│ Design  │───→│ Develop │───→│ Test    │───→│ Deploy  │
    │ & Assess │    │ & Plan  │    │ & Build │    │ & Valid │    │ & Oper  │
    └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
         │              │              │              │              │
    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐    ┌────┴────┐
    │SOP-003  │    │SOP-002  │    │Data Gov │    │Conform  │    │SOP-006  │
    │Use Case │    │Risk     │    │Controls │    │Assess   │    │Change   │
    │Approval │    │Assess   │    │Applied  │    │Passed   │    │Mgmt     │
    └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘
         │                                                           │
         │              ┌─────────┐    ┌─────────┐                  │
         │              │ Monitor │←──│ Retire  │←─────────────────┘
         │              │ & Audit │    │ & Decom │
         │              └────┬────┘    └─────────┘
         │                   │
         └───────────────────┘ (continuous improvement loop)
```

### 5.2 Gate 審核機制

| Gate | 階段 | 審核內容 | 審核者 | AI 系統風險等級要求 |
|------|------|---------|--------|-------------------|
| **G1** | Request → Design | 業務需求合理性、法規初篩、資料需求 | AI Owner + DTO | All |
| **G2** | Design → Develop | 風險評估完成、資料治理計畫、架構審核 | DTO + IT + Legal | High + Critical |
| **G3** | Develop → Test | 資料品質驗證、隱私控制實施、安全測試 | IT + Quality | High + Critical |
| **G4** | Test → Deploy | 合規性自評通過、技術文件完備、人類監督機制 | AI Governance Committee | Critical only |
| **G5** | Deploy → Monitor | 上線核准、監控指標定義、事件應變準備 | AI Owner + IT | All |

---

## 6. 合規監控自動化（Compliance Monitoring Automation）

### 6.1 自動化架構（整合 AO OS）

```
┌──────────────────── Automation Schedule ────────────────────┐
│                                                             │
│  Weekly:   action_tracking pipeline                         │
│            → progress-tracker checks deadlines              │
│            → alerts on overdue/approaching items            │
│                                                             │
│  Monthly:  regulatory_watch pipeline                        │
│            → regulation-monitor scans jurisdictions          │
│            → new items → gap-assessor incremental            │
│            → action_items.json auto-update                  │
│                                                             │
│  Quarterly: compliance_assessment pipeline                  │
│            → gap-assessor full mode                          │
│            → recalculate all risk_scores                    │
│            → governance_report generation                   │
│            → HCP: Committee review                          │
│                                                             │
│  Annual:   ISO 42001 internal audit                         │
│            → full gap assessment                            │
│            → management review input preparation            │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 KPI Dashboard（治理成熟度指標）

| KPI | 定義 | 目標 | 頻率 |
|-----|------|------|------|
| P0 Completion Rate | P0 行動項完成率 | 100% by 2026-04-30 | Weekly |
| Overall Completion Rate | 全部行動項完成率 | >80% by 2026-12-31 | Weekly |
| Max Risk Score | 最高單項風險分數 | <7.0 by 2026-Q3 | Monthly |
| Average Risk Score | 加權平均風險分數 | <5.0 by 2026-Q4 | Monthly |
| Regulatory Coverage | 法規監控覆蓋率 | 7 countries + GLOBAL | Monthly |
| Overdue Items | 逾期行動項數量 | 0 | Weekly |
| Mean Time to Respond | 新法規偵測到行動項建立的平均時間 | <14 days | Monthly |
| AI System Inventory Coverage | AI 系統清冊覆蓋率 | 100% by A01 completion | Quarterly |
| ISO 42001 Control Coverage | ISO 42001 控制項符合率 | >70% by certification | Quarterly |

---

## 7. ISO 42001 整合路徑

### 7.1 與現有 ISO 9001 QMS 整合

```
ISO 9001 QMS (existing)
  │
  ├── Clause 4 (Context) ───────→ + AI-specific interested parties
  ├── Clause 5 (Leadership) ────→ + AI Governance Committee
  ├── Clause 6 (Planning) ──────→ + AI risk assessment process
  ├── Clause 7 (Support) ───────→ + AI competence requirements
  ├── Clause 8 (Operation) ─────→ + AI system lifecycle controls
  ├── Clause 9 (Evaluation) ────→ + AI-specific KPIs & audit criteria
  └── Clause 10 (Improvement) ──→ + AI incident management
                                        │
                                        ↓
                                  ISO 42001 AIMS (new)
                                  + Annex B (AI controls)
                                  + Annex C (Implementation guidance)
                                  + Annex D (Cross-sector considerations)
```

### 7.2 認證路徑建議

| 階段 | 內容 | 時程 | 投入 |
|------|------|------|------|
| **Gap Analysis (A22)** | ISO 42001 vs 現狀差距評估 | 2026 Q3 | 4-6 人週 |
| **Remediation** | 補齊缺失控制項、撰寫政策文件 | 2026 Q3-Q4 | 6-8 人週 |
| **Internal Audit** | 模擬稽核、管理審查 | 2026 Q4 | 2-3 人週 |
| **Stage 1 Audit** | 文件審查（外部認證機構） | 2027 Q1 | 外部費用 |
| **Stage 2 Audit** | 實施審查（外部認證機構） | 2027 Q1-Q2 | 外部費用 |
| **Certification** | 取得 ISO 42001 認證 | 2027 H1 | — |

**預估外部成本**：認證機構稽核費 + 可能的外部顧問費（待報價）

---

## 8. 製造業特殊考量（OT + AI）

| AI 場景 | 類型 | 安全風險 | 治理要求 |
|---------|------|---------|---------|
| AI 視覺品質檢測 | 影像辨識 | 漏檢 → 產品安全 | 可能需 CE 標誌（若為安全元件） |
| 預測性維護 | 時間序列預測 | 誤判 → 設備停機 | 驗證機制 + 失效備援 |
| 機器人 + AI 協作 | 自主控制 | 人機安全 | Machinery Reg. + EU AI Act 雙重合規 |
| IT/OT 融合 | 資料管線 | 攻擊面擴大 | IEC 62443 網路分段 + AI 系統隔離 |

**建議**：A22 ISO 42001 Gap Analysis 時，特別評估 AI 跨越 IT/OT 邊界的場景。

---

## 9. 實施路線圖

### Phase C Timeline

```
2026-Q3                         2026-Q4                         2027-Q1
├─── A22 ISO 42001 GA ─────────├─── Remediation ──────────────├─── Stage 1
│    (4-6 pw)                  │    (6-8 pw)                  │    Audit
│                              │                              │
├─── A23 Risk Mgmt Process ────├─── Internal Audit ───────────├─── Stage 2
│    (3-4 pw)                  │    (2-3 pw)                  │    Audit
│                              │                              │
├─── A24 Supply Chain ─────────│                              ├─── ISO 42001
│    (2-3 pw, parallel)        │                              │    Certified
│                              │                              │
├─── A25 Compliance Auto ──────├─── Full Automation ──────────│
│    (2-3 pw)                  │    Operational               │
│                              │                              │
├─── Policy Drafting ──────────├─── Committee Approval ───────├─── Policies
│    (parallel with A22)       │                              │    Effective
│                              │                              │
├─── Governance Committee ─────├─── First Committee Meeting ──│
│    Charter & Setup           │                              │
```

### Phase C 前置條件

| 前置條件 | 預計完成 | 狀態 |
|---------|---------|------|
| A01 AI 系統盤點 | 2026-04-30 | P0, open |
| A08 EU AI Act 風險分類 | 2026-05-15 | P1, open |
| P0 items (A01-A07) | 2026-04-30 | 0% complete |
| Management 認證決定 | 需要決策 | **待確認** |

> **關鍵決策點**：Management 需在 2026 Q2 決定是否投入 ISO 42001 認證。此決定影響 Phase C 的範圍和投入。

---

## 10. 預算估算

| 項目 | 內部投入 | 外部費用 | 備註 |
|------|---------|---------|------|
| A22 ISO 42001 GA | 4-6 人週 | 可能需外部顧問 | 視內部 ISO 42001 專業而定 |
| A23 Risk Mgmt Process | 3-4 人週 | — | DTO + Risk Mgmt 主導 |
| A24 Supply Chain | 2-3 人週 | — | Product 主導 |
| A25 Compliance Automation | 2-3 人週 | — | DTO（AO OS 已有基礎） |
| Policy Drafting | 3-4 人週 | — | DTO + Legal 協作 |
| Committee Setup | 1 人週 | — | DTO 秘書處準備 |
| ISO 42001 Certification | 2-3 人週 | TBD（認證費） | Stage 1 + 2 Audit |
| External Legal (A09) | — | TBD | EU AI Act Art.25 專家 |
| **Total** | **17-24 人週** | **TBD** | Phase C + certification |

---

## 11. 風險與緩解

| 風險 | 影響 | 緩解措施 |
|------|------|---------|
| P0 行動項延遲 → Phase C 啟動推遲 | 認證時程延後 | 平行推進：政策撰寫不依賴 P0 完成 |
| Management 不批准 ISO 42001 認證 | Phase C 縮減為內部治理 | 仍建立治理制度，但不追求外部認證 |
| 跨部門合作不順 | 政策無法落地 | AI Governance Committee 賦予決策權 |
| 外部顧問資源不足 | GA 品質不佳 | DTO 先做內部自評，外部顧問做驗證 |
| 法規快速變動 | 政策過時 | regulatory_watch 月度更新 + SOP-006 變更管理 |

---

## English Summary

Phase C transitions Primax's AI governance from reactive compliance to systematic management. The framework centers on ISO 42001 as the core AI Management System standard, integrated with the existing ISO 9001 QMS. Key components: (1) AI Governance Committee establishment at CTO/VP level with quarterly cadence, (2) Three-level policy hierarchy (policies → SOPs → templates) covering governance, risk management, ethics, and lifecycle management, (3) Gate-based AI system lifecycle controls (G1-G5) with risk-proportionate review requirements, (4) Automated compliance monitoring via AO OS pipelines (weekly tracking, monthly regulatory watch, quarterly assessment), (5) ISO 42001 certification roadmap targeting 2027 H1. Total estimated effort: 17-24 person-weeks internal + external certification costs. Critical prerequisite: P0 action items completion and Management decision on ISO 42001 certification investment by Q2 2026.

---

*Generated by DTO + Claude Code | AO OS v2.0 | AI Governance Domain*
