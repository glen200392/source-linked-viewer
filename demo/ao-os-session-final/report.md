# AO OS macOS 部署 — Session 最終報告

**報告編號**: SR-2026-001
**日期**: 2026-03-08
**作者**: Glen Ho + Claude Code
**範圍**: AO OS 跨平台部署 Phase 1-3 + AI 研究團隊建置

---

## 執行摘要

本 session 橫跨兩次對話（因 context 耗盡而延續），完成了 AO OS（Agent Orchestration OS）從 Windows 到 macOS 的完整遷移部署，涵蓋環境建置、架構決策、路徑修復、Agent/Skill 部署、AI 研究團隊建置，以及研究管線的可擴展性重新設計。

**最終狀態**: 所有驗證通過，3 處殘餘 Windows 路徑已修復，系統就緒。

---

## 1. 完成工作總覽

### Phase 1: 環境建置

| 項目 | 狀態 | 詳情 |
|------|------|------|
| 5 個 repo clone | ✅ 完成 | ao-os-config, dto-intelligence, data-governance, ai-governance, ao-os-migration |
| repo 整理 | ✅ 完成 | ao-os-migration 移至 ~/Projects/ |
| 系統工具安裝 | ✅ 完成 | pandoc 3.9, ffmpeg (via Homebrew) |
| Python venvs | ✅ 完成 | 3 個 repo 各自獨立 venv (Python 3.13) |
| requirements.txt | ✅ 完成 | dto-intelligence (fastembed, requests), data-governance (markdown), ao-os-config (requests, filelock, opencc) |

### Phase 2: 架構決策與路徑修復

| 項目 | 狀態 | 詳情 |
|------|------|------|
| Agent 格式研究 | ✅ 完成 | AO OS 格式 = Claude Code superset（相容，非衝突）|
| Subagent 限制研究 | ✅ 完成 | 平台無關（非 OS 問題）|
| Context Rot 分析 | ✅ 完成 | Windows 路徑造成靜默功能失效（非 token 浪費）|
| CLAUDE.md 策略 | ✅ 完成 | 選用 Strategy 1：統一 + 動態 OS 偵測 |
| 路徑批次修復 | ✅ 完成 | 93 處 Windows 路徑 → tilde 路徑（30 個檔案）|
| Python 腳本修復 | ✅ 完成 | pathlib + sys.platform 偵測 |
| Agent symlinks | ✅ 完成 | 31/32 agents（security-monitor 排除）|
| Skill symlinks | ✅ 完成 | 16 個 AO OS skills |

### Phase 3: AI 研究團隊建置

| 項目 | 狀態 | 詳情 |
|------|------|------|
| AO OS runtime 部署 | ✅ 完成 | ~/.claude/ao-os/ 完整結構 |
| research-topics.json | ✅ 完成 | 4 個研究軌道（RT-001~004）|
| KB baselines | ✅ 完成 | 4 筆基線 entries（2026-03-08）|
| /ai-research skill | ✅ 完成 | 簡化為排程觸發器 |
| run_ai_research.sh | ✅ 完成 | 跨平台排程腳本 |
| launchd plist | ✅ 完成 | 每月 1 日 10:00 AM |
| research-orchestrator 增強 | ✅ 完成 | Phase 0 (0-A/0-B/0-C) + Phase 3 delta + Phase 6.5 baseline writeback |

---

## 2. 關鍵架構決策記錄

### 決策 1: Agent 格式相容性
- **問題**: AO OS agent 格式與 Claude Code agent 格式是否衝突？
- **結論**: AO OS 格式是 Claude Code 格式的 **superset**，額外的 YAML fields（color, memory）會被靜默忽略
- **影響**: 無需格式轉換，直接 symlink 即可

### 決策 2: 跨平台路徑策略
- **策略**: 三層路徑方案
  - Markdown/Config: `~/` (tilde，所有 OS 自動展開)
  - Python: `pathlib.Path(__file__)` (repo-relative)
  - 系統應用: `sys.platform` 偵測 (Chrome 等)
- **影響**: 零 OS 特定分支，同一份檔案在兩個平台運作

### 決策 3: CLAUDE.md 統一策略
- **選項**: 3 個策略評估後選用 Strategy 1（統一 + 動態偵測）
- **原因**: tilde 已等同環境變數，無需模板引擎或 .env 注入
- **影響**: 維護成本最低，無額外建置需求

### 決策 4: 研究管線可擴展性
- **問題**: 每個研究領域需要獨立 Skill 嗎？
- **結論**: 不需要。research-orchestrator 自動偵測基線和 domain focus
- **設計**: Skill 永遠不變，研究題目是純資料（research-topics.json）
- **影響**: 新增研究領域 = 新增 JSON 檔，零 code 變更

---

## 3. 驗證結果

### 3.1 Symlink 完整性

| 目錄 | Symlinks | 有效 | 失效 | 狀態 |
|------|----------|------|------|------|
| ~/.claude/agents/ | 31 | 31 | 0 | ✅ PASS |
| ~/.claude/skills/ | 16 | 16 | 0 | ✅ PASS |
| ~/.claude/ao-os/ | 完整結構 | — | 0 | ✅ PASS |
| capability_registry.json | 1 | 1 | 0 | ✅ PASS |

### 3.2 路徑殘留檢查

| 檔案 | 問題 | 修復狀態 |
|------|------|----------|
| pulse-agent.md | `dto-intelligence\data\` 反斜線 | ✅ 已修復 |
| data-catalog-agent.md:21-22 | `dto-intelligence\data\` 反斜線 | ✅ 已修復 |
| data-catalog-agent.md:38 | `dto-intelligence\\data\\` 雙反斜線 | ✅ 已修復 |
| skill_engineer_input_v1.json:37 | `projects\\C--Users-glen-ho\\` Windows 路徑 | ✅ 已修復 |

**修復後**: 零 Windows 路徑殘留。

### 3.3 Python 環境

| Repo | venv | 套件 | 狀態 |
|------|------|------|------|
| dto-intelligence | .venv (3.13) | fastembed, requests | ✅ PASS |
| data-governance | .venv (3.13) | markdown | ✅ PASS |
| ao-os-config | .venv (3.13) | requests, filelock, opencc | ✅ PASS |

### 3.4 研究管線一致性

| 檢查項目 | 狀態 |
|----------|------|
| Phase 0 含 Step 0-A/0-B/0-C | ✅ PASS |
| Phase 3 含 delta analysis | ✅ PASS |
| Phase 6.5 含 baseline writeback | ✅ PASS |
| 輸出契約含 baseline_updated | ✅ PASS |
| /ai-research 為 thin wrapper | ✅ PASS |
| run_ai_research.sh 跨平台 | ✅ PASS |

### 3.5 Cross-Reference

| 指標 | Source | Deployed | 差異 |
|------|--------|----------|------|
| Agents | 32 | 31 symlinked | security-monitor 刻意排除（Windows-only）|
| Skills | 16 | 16 symlinked | 完全對應 |
| message-bus | — | pending/ + completed/ | ✅ 存在 |
| session-topics.json | — | symlink 有效 | ✅ PASS |

---

## 4. 缺失分析：對照前沿架構

基於本 session 的深度研究（見 AI 架構研究報告），以下是 AO OS 與 2026 前沿對比的缺失分析：

### 4.1 已具備的前沿特性

| 特性 | AO OS 實作 | 前沿對應 |
|------|-----------|----------|
| Orchestrator-Worker 模式 | dto-orchestrator + worker agents | 業界主流模式 |
| Hierarchical 模式 | meta-orchestrator → domain orchestrators | 成熟模式 |
| File-based message bus | pending/ → completed/ | 輕量級但有效 |
| Write Isolation (Inbox) | kb_inbox/ → merge script | Context Engineering best practice |
| Human Checkpoints (HCP) | HCP1 + HCP2 在研究管線 | Human-in-the-loop 標準做法 |
| 批判性研究協議 | /critical-research 五大原則 | 對應 Research Critic 模式 |
| Delta Analysis | Phase 0-B + Phase 3 + Phase 6.5 | 持續差異追蹤閉環 |
| Cross-platform | tilde + pathlib + sys.platform | 跨平台最佳實踐 |

### 4.2 可改進但非緊急的領域

| 領域 | 現狀 | 前沿做法 | 建議優先級 |
|------|------|----------|-----------|
| Agent 發現 | 靜態 capability_registry.json | A2A Agent Card (動態發現) | 低 — 內部系統不需 |
| MCP 整合 | Pencil + Chrome DevTools | MCP 生態系 1000+ servers | 中 — 按需新增 |
| 評估框架 | 無正式評估 | CLEAR 五維度 + Agent-as-Judge | 中 — 生產化時需要 |
| 反思模式 | 無 | Generate-Critique-Refine | 低 — dto-verifier 已部分覆蓋 |
| Context 壓縮 | 手動 compact | Trajectory Reduction (40-60%) | 低 — Claude Code 內建壓縮 |
| 基線版本化 | kb_inbox/ 追加 | 時間序列基線 + rollback | 低 — 目前規模不需 |

### 4.3 完全缺失但值得關注的領域

| 領域 | 說明 | 前沿對應 | 建議 |
|------|------|----------|------|
| Agent 安全紅隊測試 | 無系統化安全驗證 | SuperClaw, AutoRedTeamer | 待生產化時導入 |
| EU AI Act 合規 | 無正式評估 | 2026/08 全面適用 | 若有歐盟業務需提前準備 |
| Agent 經濟模型 | 無 token 預算/花費追蹤 | Agent wallets, budget controls | 長期方向 |
| 多模態 Agent | 純文字 | VLM agents (Qwen3.5, Gemini 2.5) | 按需求決定 |
| Cache-to-Cache 通訊 | 無 | 實驗階段，2.5x 延遲改善 | 觀察，尚未成熟 |
| AAIF 標準對接 | 無 | MCP + A2A + AGENTS.md | 中長期，隨標準成熟 |
| CI/CD for Agents | 無自動測試 | Agent eval pipelines | 中期建議導入 |

---

## 5. 建議下一步

### 短期（1-2 週）
1. ~~修復 3 處 Windows 路徑殘留~~ ✅ 已完成
2. 執行 `merge_kb_inbox.py` 合併基線到 knowledge_base.json
3. 載入 launchd plist：`launchctl load ~/Library/LaunchAgents/com.glen.ai-research-monthly.plist`
4. 推送所有變更到 GitHub
5. 在 Windows 端 pull 並重新部署

### 中期（1-3 個月）
1. 建立跨平台部署腳本（macOS: symlink, Windows: mklink/copy）
2. 導入簡易 Agent 評估機制（eval template 已存在）
3. 首次執行 `/ai-research --auto` 測試完整管線
4. 視需求新增 MCP servers

### 長期（3-6 個月）
1. 評估 A2A Agent Card 對 AO OS 的適用性
2. 導入 CLEAR 框架做 Agent 效能基準測試
3. 若有歐盟業務，開始 EU AI Act 合規評估
4. 考慮 Agent 測試 CI/CD pipeline

---

## 6. 修改檔案清單

### 本 session（延續對話）修改

| 檔案 | 動作 | 說明 |
|------|------|------|
| agents/research-orchestrator.md | 修改 | Phase 0 (0-A/0-B/0-C), Phase 3 delta, Phase 6.5 baseline writeback |
| skills/ai-research/SKILL.md | 重寫 | 111 行 → ~40 行，簡化為排程觸發器 |
| agents/pulse-agent.md | 修復 | 反斜線路徑 → 正斜線 |
| agents/data-catalog-agent.md | 修復 | 反斜線路徑 → 正斜線（2 處） |
| ao-os/schema-registry/contracts/skill_engineer_input_v1.json | 修復 | Windows 完整路徑 → macOS 路徑 |

### 前次對話修改（完整列表）

- **30 個檔案**: 批次路徑替換（agents 17 檔, skills 11 檔, ao-os 1 檔, CLAUDE.md）
- **4 個 Python 腳本**: pathlib + sys.platform 修復
- **5 個新建檔案**: research-topics.json, ai_research_baselines.json, run_ai_research.sh, com.glen.ai-research-monthly.plist, 3 個 requirements.txt
- **runtime 部署**: ~/.claude/ao-os/ 完整結構 + symlinks

---

## 7. 統計摘要

| 指標 | 數值 |
|------|------|
| 總修改檔案數 | 40+ |
| Windows 路徑替換總數 | 96 (93 + 3 殘留) |
| Agent symlinks | 31 |
| Skill symlinks | 16 |
| Python venvs 建立 | 3 |
| 新建檔案 | 8 |
| 架構決策 | 4 項重大決策 |
| 研究軌道 | 4 個 (RT-001~004) |
| 驗證檢查點 | 20+ items, 全部 PASS |

---

*報告產出日期: 2026-03-08*
*Generated with Claude Code (Opus 4.6)*
