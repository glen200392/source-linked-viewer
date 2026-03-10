# AI 影片製作工具完整研究報告

> **報告日期**：2026-03-08
> **作者**：Glen Ho（AI 輔助研究）
> **範圍**：開源 / 閉源 / 付費 AI 影片生成工具全景分析
> **用途**：企業教育訓練影片一條龍製作流程評估

---

## 目錄

- [第一部分：AI 影片生成開源模型總覽](#第一部分ai-影片生成開源模型總覽)
- [第二部分：程式化影片製作工具](#第二部分程式化影片製作工具)
- [第三部分：企業教育訓練影片一條龍流程](#第三部分企業教育訓練影片一條龍流程)
- [第四部分：費用估算與建議](#第四部分費用估算與建議)
- [附錄：參考資料](#附錄參考資料)

---

## 第一部分：AI 影片生成開源模型總覽

### 1.1 技術趨勢

AI 影片生成在 2025-2026 經歷爆發式成長，核心技術從 U-Net 轉向 **Diffusion Transformer (DiT)**，並開始引入 **MoE（混合專家）** 架構提升效率。開源模型品質已逼近甚至超越商業方案（如 Sora、Runway Gen-3），硬體門檻大幅降低，部分模型僅需 6-8GB VRAM 即可運行。

### 1.2 模型比較表

| 模型 | 開發者 | 參數量 | 最低 VRAM | 解析度 | 授權 | 核心能力 |
|------|--------|--------|-----------|--------|------|----------|
| **Wan 2.2** | Alibaba | 14B (MoE) | ~8 GB | 720P+ | Apache 2.0 | T2V, I2V, 影片編輯, V2A |
| **HunyuanVideo 1.5** | Tencent | 8.3B-13B | ~14 GB | 720P+ | 開源 | T2V, I2V, 高動作一致性 |
| **LTX-Video 2.3** | Lightricks | - | ~12 GB | 1216×704 | 開源 | 快速生成（超即時）, 30fps |
| **CogVideoX** | 清華/智譜 | 2B/5B | ~8 GB (2B) | 720×480 | 開源 | T2V, I2V, 6秒片段 |
| **Mochi 1** | Genmo | 10B | ~24 GB | 中高畫質 | Apache 2.0 | 最佳文字一致性 |
| **MAGI-1** | Sand AI | - | 較高 | 1440×2568 | Apache 2.0 | 自迴歸逐秒控制, 超高解析度 |
| **Open-Sora 2.0** | HPC-AI Tech | 11B | ~40 GB | 高畫質 | 開源 | 低訓練成本, 媲美商業模型 |
| **SkyReels V2** | Skywork AI | - | - | 24fps | 開源 | 人物表情/動作, AI 短劇 |

### 1.3 各模型深度分析

#### Wan 2.2（阿里巴巴）— 當前綜合首選

**目前綜合評價最高的開源影片生成模型。**

- **架構**：MoE（混合專家）擴散骨幹網路，將去噪過程拆分給不同專家處理
  - 高噪音專家負責初始影片佈局
  - 低噪音專家負責後期細節精修
- **能力範圍**：Text-to-Video、Image-to-Video、影片編輯、Text-to-Image、Video-to-Audio
- **硬體友善**：T2V-1.3B 版本僅需 8.19 GB VRAM，RTX 4090 約 4 分鐘生成 5 秒 480P 影片
- **GitHub**：https://github.com/Wan-Video/Wan2.2

#### HunyuanVideo 1.5（騰訊）

- 在專業評測中超越 Runway Gen-3 和 Luma 1.6
- 文字對齊度 68.5%，視覺品質分 96.4%
- 支援消費級 GPU（14GB+ VRAM，搭配 offloading）
- 強項：物理運動真實感、自然場景連貫性

#### LTX-Video 2.3（Lightricks）— 速度之王

- **超即時生成**：30fps、1216×704 解析度，生成速度快於播放速度
- LTX Desktop 提供完整的非線性影片編輯器 + 本地 AI 生成
- LTX-2 已原生支援 ComfyUI，可同步生成動作、對話、背景音、音樂
- 12GB VRAM 即可流暢運行

#### CogVideoX（清華/智譜）

- 2B 版本適合輕量硬體（~8GB VRAM）
- 5B 版本提供更高品質
- 生成 6 秒、8fps、720×480 的影片片段
- 結合 3D VAE + Expert Transformer 技術

#### Mochi 1（Genmo）

- 10B 參數的非對稱擴散 Transformer（AsymmDiT）
- **文字一致性最佳**——prompt 指令遵循度最高
- Apache 2.0 授權，完全可商用
- 需要較高 VRAM（24GB+）

#### MAGI-1（Sand AI）

- **自迴歸式影片擴散模型**——逐秒預測生成（24 幀/段）
- 支援「逐秒時間軸控制」，每一秒都可精確指定內容
- 原生解析度達 1440×2568（超高畫質）
- 完整開源：程式碼、權重、推理工具全部公開

#### Open-Sora 2.0（HPC-AI Tech）

- 僅約 $200,000 訓練成本就達到媲美頂級商業模型的表現
- 在 VBench 和人類偏好評測中與 HunyuanVideo、Step-Video 持平
- 目標：讓所有人都能做高品質影片

#### SkyReels V2（Skywork AI）

- 專注**人物影片生成**：33 種表情、400+ 自然動作組合
- 首個開源的「以人為中心」影片模型
- 適合 AI 短劇、角色驅動內容

### 1.4 硬體需求指南

| GPU VRAM | 適用模型 | 代表 GPU |
|----------|----------|----------|
| **6-8 GB** | Wan 2.1 小模型, AnimateDiff, Text2Video-Zero | RTX 3060, 4060 |
| **12 GB** | LTX-Video, CogVideoX-2B, Allegro | RTX 3060 12GB, 4070 |
| **16 GB** | SVD, DynamiCrafter, Latte | RTX 4080, A4000 |
| **24 GB** | 大部分開源模型（含 Mochi, Wan 14B） | RTX 4090, A5000 |
| **40 GB+** | Open-Sora 2.0 全量, 多模型並行 | A100, H100 |

> **Apple Silicon 使用者**：多數模型已支援 MPS backend，但效能約為同級 NVIDIA GPU 的 50-70%。建議優先嘗試 Wan 2.1 小模型或 LTX-Video。

### 1.5 工具與生態系統

#### ComfyUI — 核心工作流引擎

ComfyUI 是目前 AI 影片生成最重要的整合平台，100% 開源，節點式畫布介面。

- 支援幾乎所有主流開源模型
- 2026 年 NVIDIA 在 CES 宣布深度合作與加速優化
- RTX 50 系列搭配 NVFP4 格式可達 3x 加速、60% VRAM 降低
- 社群驅動：Custom Node Registry、ComfyUI Manager
- 官網：https://www.comfy.org/

#### Wan2GP — 低 VRAM 救星

- 讓 Wan 2.1/2.2、HunyuanVideo、LTX Video 等模型在 6GB VRAM 的 GPU 上運行
- GitHub：https://github.com/deepbeepmeep/Wan2GP

#### LTX Desktop — 本地影片編輯 + AI 生成

- 免費開源的桌面影片編輯工具
- 結合非線性剪輯與 AI 生成，完全本地運行

---

## 第二部分：程式化影片製作工具

### 2.1 工具定位說明

AI 生成模型（如 Wan 2.2）和程式化影片工具（如 Remotion）是**兩個完全不同的維度**：

- **AI 生成型**：從無到有生成畫面（適合真人場景、微電影）
- **程式化編排型**：用程式碼控制剪輯與合成（適合數據影片、動態圖表、批量行銷）

### 2.2 Remotion 能力分析

| 能力 | 支援？ | 說明 |
|------|--------|------|
| 動態圖形 / Motion Graphics | ✅ | 核心強項，用 React + CSS/SVG/Canvas/WebGL |
| 文字動畫、字幕 | ✅ | 完全支援 |
| 圖片/影片合成 | ✅ | 可匯入素材做合成 |
| 3D 動畫 | ✅ | 透過 Three.js 整合 |
| 資料驅動影片 | ✅ | 接 API 自動生成大量影片 |
| 輸出 MP4 | ✅ | 內建 FFmpeg 渲染 |
| AI 畫面生成 | ❌ | 本身不含 AI 模型 |
| 真人實拍風格 | ❌ | 不適合 |
| 商用授權 | ⚠️ | **公司使用需購買商業授權** |

### 2.3 同類型工具比較

| 工具 | 語言 | 授權 | 核心定位 | AI 整合 |
|------|------|------|----------|---------|
| **Remotion** | React/TS | 商業需付費 | React 寫影片，生態系最豐富 | ❌ 無內建 |
| **Rendervid** | React/TS | 完全免費開源 | AI Agent 原生設計，JSON 模板驅動 | ✅ 內建 MCP |
| **MoviePy** | Python | MIT | Python 影片剪輯，像素級操控 | ❌ 無內建 |
| **Manim** | Python | MIT | 數學動畫引擎（3Blue1Brown 御用） | ❌ 無內建 |
| **FFmpeg** | C | LGPL/GPL | 影片編碼解碼的底層之王 | ❌ |
| **DesignCombo** | React | 開源 | 基於 Remotion 的線上影片編輯器 UI | ❌ |

### 2.4 Rendervid — Remotion 的免費 AI 替代品

- **完全免費開源**，無商業授權限制
- **為 AI Agent 設計**：內建 MCP Server，11 個工具讓 Claude Code、Cursor 等直接操控
- **JSON 模板驅動**：AI 生成 JSON → 自動驗證 → 自動渲染
- **雲端渲染**：支援 AWS Lambda、Azure Functions、GCP Cloud Run、Docker

---

## 第三部分：企業教育訓練影片一條龍流程

### 3.1 三種呈現風格

| 風格 | 說明 | 核心技術需求 | 複雜度 |
|------|------|------------|--------|
| **A. 線上課程** | AI 講師 + 投影片 + 字幕 | AI Avatar + TTS + 投影片合成 | ★★☆☆☆ |
| **B. 微電影感** | 多場景、多角色、情節驅動 | 角色一致性 + 場景生成 + 影片生成 + 配音 | ★★★★★ |
| **C. NotebookLM 式** | 文件 → 視覺化摘要/對談影片 | 文件解析 + 動態圖表 + AI 旁白 | ★★★☆☆ |

### 3.2 五大階段流程

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ ① 腳本   │ →  │ ② 視覺   │ →  │ ③ 影片   │ →  │ ④ 音訊   │ →  │ ⑤ 合成   │
│   生成    │    │   設計    │    │   生成    │    │   配音    │    │   輸出    │
└──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
 文字→場景腳本    角色/場景設計    圖→影片 或       TTS/語音克隆     剪輯+字幕
 Prompt 工程     一致性維護      腳本→直接生片     音效/配樂       SCORM 輸出
```

### 3.3 階段 ① 腳本生成（文字 → 場景 Prompt）

將教材/SOP/文件轉化為結構化的場景腳本、角色描述、鏡頭指示。

| 工具 | 類型 | 費用 | 能力 |
|------|------|------|------|
| **ChatGPT / Claude** | 閉源 API | $20/月（Pro）或 API 按量 | 腳本撰寫、場景分解、角色細節描述 |
| **LTX Studio** | 閉源 SaaS | $15-125/月 | 自動從腳本提取角色/物件/場景為可重用元素 |
| **Filmustage** | 閉源 SaaS | 免費基本版 | 自動拆解腳本→場景、道具、角色、服裝 |
| **AI Video Prompt Architect** | 免費工具 | 免費 | 將腳本轉為逐鏡頭 AI 影片 Prompt |
| **本地 LLM（Llama 3、Qwen）** | 開源 | 僅硬體成本 | 需自行設計 Prompt 模板 |

**最佳實踐**：建立 Character Style Sheet——記錄每個角色的外貌特徵、服裝、手勢、說話風格，確保後續生成一致。

### 3.4 階段 ② 視覺設計（角色 + 場景圖像生成）

| 工具 | 類型 | 費用 | 角色一致性方案 |
|------|------|------|--------------|
| **FLUX.2 + LoRA** | 開源 | LoRA 訓練約 $1-5/次 | 用 20-40 張圖訓練角色 LoRA，一致性最佳 |
| **Stable Diffusion XL + LoRA** | 開源 | GPU 租用 $0.5-2/hr | 成熟生態系，大量社群 LoRA 可用 |
| **ComfyUI 工作流** | 開源 | 免費（本地運行） | 節點式串接：文字→圖片→一致性檢查→影片 |
| **Midjourney** | 閉源 | $10-60/月 | `--cref` 角色參考功能 |
| **DALL-E 3** | 閉源 | ChatGPT Plus 含 | 方便但角色一致性較弱 |

**LoRA 訓練細節**（開源方案）：

- **資料需求**：20-40 張角色照片（不同角度、表情、光線）
- **訓練時間**：500-2,000 步，約 1-2 小時
- **成本**：雲端 GPU（H100）約 $1-5 一次訓練
- **效果**：FLUX LoRA 在角色臉部一致性上遠超前代模型

### 3.5 階段 ③ 影片生成

#### 路線 A：圖片轉影片（Image-to-Video）

先生成靜態圖片，再轉為動態影片。角色一致性最好，但動作範圍有限。

| 工具 | 類型 | 費用 | 特點 |
|------|------|------|------|
| **Wan 2.2 I2V** | 開源 | 硬體成本 | MoE 架構，開源最強 I2V，支援 LoRA |
| **HunyuanVideo I2V** | 開源 | 硬體成本 | 搭配 LoRA 維持角色一致性 |
| **LTX-Video** | 開源 | 硬體成本 | 超即時生成，速度最快 |
| **Kling 3.0** | 閉源 | 按量計費 | 角色一致性優秀 |
| **Runway Gen-4** | 閉源 | $12-76/月 | 最佳創意控制 |

#### 路線 B：腳本直接生片（Script/Text-to-Video）

| 工具 | 類型 | 費用 | 特點 |
|------|------|------|------|
| **LTX Studio** | 閉源 | $15-125/月 | 最接近一條龍：腳本→分鏡→角色鎖定→生成→剪輯 |
| **Wan 2.2 T2V** | 開源 | 硬體成本 | 開源最強 T2V，搭配 LoRA 可控角色 |
| **MAGI-1** | 開源 | 硬體成本 | 逐秒精確控制，適合精細場景 |
| **Sora（OpenAI）** | 閉源 | ChatGPT Plus 含 | 寫實感最強 |
| **Veo 3（Google）** | 閉源 | Google AI Ultra $249/月 | NotebookLM Cinematic Video 的底層引擎 |

#### 路線 C：AI Avatar 說話頭（適合線上課程風格）

| 工具 | 類型 | 費用 | 特點 |
|------|------|------|------|
| **Synthesia** | 閉源 | $29/月起，企業版另議 | 企業首選，160+ 語言，SCORM 輸出 |
| **HeyGen** | 閉源 | $29-149/月 | Avatar IV、語音克隆、SCORM（Business 版） |
| **Colossyan** | 閉源 | $19-120/月 | L&D 專精，投影片式模組，LMS 直接整合 |
| **D-ID** | 閉源 | 按量計費 | 120+ 語言，API 友善 |
| **MuseTalk** | 開源 (MIT) | 硬體成本 | 即時唇形同步，30+ fps（V100 GPU） |
| **LivePortrait** | 開源 | 硬體成本 | 表情轉移、情感感知動畫 |
| **SadTalker** | 開源 | 硬體成本 | 單張圖片 → 說話頭影片 |
| **Wav2Lip** | 開源 | 硬體成本 | 業界標準唇形同步工具 |

### 3.6 階段 ④ 音訊（配音 + 音效）

| 工具 | 類型 | 費用 | 特點 |
|------|------|------|------|
| **XTTS-v2（Coqui）** | 開源 | 免費 | 6 秒音訊即可克隆語音，17 語言 |
| **Bark（Suno）** | 開源 | 免費 | 可生成語音+音效+音樂，表現力強 |
| **OpenVoice** | 開源 | 免費 | 跨語言語音克隆 |
| **Chatterbox** | 開源 | 免費 | 2026 新興，高品質語音克隆 |
| **ElevenLabs** | 閉源 | $5-99/月 | 品質最佳，企業級語音克隆 |
| **Azure TTS** | 閉源 | 按量計費 | 企業級穩定度，中文支援優秀 |

### 3.7 階段 ⑤ 合成與輸出

| 工具 | 類型 | 費用 | 特點 |
|------|------|------|------|
| **ComfyUI** | 開源 | 免費 | 節點式統一工作流，串接所有 AI 模型 |
| **Remotion / Rendervid** | 開源 | 免費（Rendervid） | 程式化影片編排，批量自動化 |
| **FFmpeg** | 開源 | 免費 | 最終編碼、格式轉換 |
| **LTX Desktop** | 開源 | 免費 | 非線性剪輯 + AI 生成一體化 |
| **Descript** | 閉源 | $24-40/月 | 文字型影片編輯 |

---

## 第四部分：費用估算與建議

### 4.1 按風格推薦方案

#### 風格 A：線上課程（AI 講師型）

```
最快方案（閉源）：
  Synthesia / Colossyan → 上傳投影片 → 選 AI Avatar → 輸入腳本 → 輸出 SCORM
  費用：$29-149/月
  時間：30 分鐘課程約 2-3 小時完成

開源方案：
  Claude API（腳本）→ SadTalker/MuseTalk（說話頭）→ XTTS-v2（配音）→ FFmpeg（合成）
  費用：GPU 租用 $50-100/月 + API 費用
  時間：需 1-2 週搭建管線，之後每支影片約 4-6 小時
```

#### 風格 B：微電影感（多場景敘事型）

```
最佳方案（閉源）：
  Claude/GPT（腳本+角色設定）→ LTX Studio（分鏡+角色鎖定+生成）→ ElevenLabs（配音）
  費用：$125-250/月
  時間：5 分鐘微電影約 1-2 天

開源方案：
  本地 LLM（腳本）→ FLUX LoRA（角色一致性圖片）→ Wan 2.2 I2V（圖轉影片）
  → XTTS-v2（配音）→ ComfyUI（工作流串接）→ FFmpeg（合成）
  費用：GPU（RTX 4090）約 NT$60,000 一次性 或 雲端 $200-400/月
  時間：需 3-4 週搭建管線，每支影片約 1-2 天
```

#### 風格 C：NotebookLM Video Review 式

```
最快方案：
  Google NotebookLM（AI Ultra $249/月）→ 直接上傳文件 → 生成 Cinematic Video Overview
  底層用 Gemini 3 + Veo 3，幾乎零技術門檻

替代方案：
  Claude（文件分析+腳本）→ Manim/Remotion（動態圖表+可視化）
  → Bark（AI 雙人對談配音）→ FFmpeg（合成）
  費用：$50-100/月（API + 雲端）
  時間：需 2-3 週開發模板，之後每支約 2-4 小時
```

### 4.2 費用估算總覽

#### 閉源方案（月度訂閱）

| 組合 | 月費估算 | 產能 | 適合 |
|------|---------|------|------|
| Synthesia Starter | ~$29/月 | ~10 分鐘影片/月 | 小規模課程 |
| Colossyan Pro | ~$120/月 | 較多分鐘 | L&D 團隊 |
| HeyGen Business | ~$149/月 | 60+ 分鐘/月 | 大量訓練影片 |
| LTX Studio Pro + ElevenLabs | ~$225/月 | 微電影級製作 | 高品質內容 |
| NotebookLM Ultra | ~$250/月 | 無限 Video Overview | 知識摘要型 |
| **全功能企業組合** | **$300-500/月** | 多風格混合 | 完整 L&D 部門 |

#### 開源方案（一次性 + 運營）

| 項目 | 費用 |
|------|------|
| **GPU 硬體**（RTX 4090 24GB） | ~NT$55,000-65,000 一次性 |
| **雲端 GPU 替代**（RunPod/Vast.ai） | $200-400/月 |
| **LoRA 訓練**（每角色） | $1-5/次 |
| **API 費用**（LLM 腳本生成） | $20-50/月 |
| **工程師建置時間** | 3-6 週（一次性） |
| **月度運營成本** | $50-150/月（電費+API） |

### 4.3 開源方案的技術挑戰與解決

| 挑戰 | 嚴重度 | 解決方案 |
|------|--------|---------|
| **角色一致性** | 高 | LoRA 訓練 + IP-Adapter + Reference Image 三重保障 |
| **GPU VRAM 不足** | 中 | Wan2GP（6GB 即可跑）、模型量化、CPU offloading |
| **多場景連貫性** | 高 | Character Style Sheet + ComfyUI 工作流固定種子 |
| **中文 TTS 品質** | 中 | XTTS-v2 支援中文，或搭配 Azure TTS |
| **Apple Silicon 相容** | 中 | 多數模型支援 MPS backend，效能約 NVIDIA 50-70% |
| **管線整合複雜度** | 高 | ComfyUI 節點化串接，或用 Python 腳本自動化 |
| **影片長度限制** | 中 | 分段生成（5-10 秒/段）後拼接 |

### 4.4 使用場景快速推薦

| 你想做的事 | 推薦方案 |
|-----------|---------|
| AI 生成逼真影片 | Wan 2.2 + ComfyUI |
| 自動化批量生成行銷影片 | Rendervid（或 Remotion） |
| 數據可視化動畫 | Manim（數學）或 Remotion（商業） |
| 完整影片管線：AI 素材 + 程式化剪輯 | Wan 2.2 + Rendervid + FFmpeg |
| 最低門檻入門 | LTX Desktop（編輯+AI 一體化） |
| 企業課程快速上線 | Synthesia / Colossyan |
| 微電影級品質 | LTX Studio + ElevenLabs |
| NotebookLM 風格 | NotebookLM Ultra 或 Claude + Manim + Bark |

### 4.5 分階段實施路線圖

```
Phase 1（第 1-2 週）— 快速驗證
  → 用 Synthesia/Colossyan 免費版做 1-2 支課程影片
  → 同步用 NotebookLM 測試 Video Overview
  → 確認哪種風格最適合你的受眾

Phase 2（第 3-4 週）— 規模化選擇
  → 選定閉源方案訂閱 OR 開始搭建開源管線
  → 建立角色 Style Sheet 和 Prompt 模板庫

Phase 3（第 2-3 月）— 生產管線
  → 建立自動化工作流（ComfyUI / Rendervid）
  → LoRA 訓練企業專屬角色
  → 整合 LMS / SCORM 輸出
```

### 4.6 完整影片製作管線架構

```
┌─────────────────────────────────────────────────────┐
│              完整 AI 影片製作管線                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. 素材生成（AI 生成型）                              │
│     ├─ Wan 2.2       → 真人/場景影片片段               │
│     ├─ LTX-Video     → 快速原型、動態素材              │
│     └─ MAGI-1        → 精細逐秒控制                   │
│                                                     │
│  2. 編排與合成（程式化編排型）                          │
│     ├─ Remotion       → React 開發者首選（需授權）      │
│     ├─ Rendervid      → AI Agent 自動化首選（免費）     │
│     └─ MoviePy        → Python 開發者首選              │
│                                                     │
│  3. 工作流整合                                        │
│     ├─ ComfyUI        → AI 模型的統一節點式介面         │
│     └─ FFmpeg         → 最終編碼/格式轉換              │
│                                                     │
│  4. 音訊（補充）                                      │
│     ├─ LTX-2          → 同步生成音效+影片              │
│     └─ 外部 TTS       → AI 旁白/配音                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 附錄：參考資料

### 開源模型與工具

- [Wan 2.2 — GitHub](https://github.com/Wan-Video/Wan2.2)
- [MAGI-1 — 官方網站](https://magi-1.ai/)
- [Open-Sora — GitHub](https://github.com/hpcaitech/Open-Sora)
- [ComfyUI — 官方網站](https://www.comfy.org/)
- [Wan2GP — GitHub](https://github.com/deepbeepmeep/Wan2GP)
- [LTX — 官方網站](https://ltx.io/)
- [Remotion — GitHub](https://github.com/remotion-dev/remotion)
- [Rendervid — FlowHunt](https://www.flowhunt.io/rendervid/)
- [MoviePy — GitHub](https://github.com/Zulko/moviepy)
- [Manim — GitHub](https://github.com/3b1b/manim)
- [Manim Community Edition — GitHub](https://github.com/ManimCommunity/manim)
- [DesignCombo React Video Editor — GitHub](https://github.com/designcombo/react-video-editor)
- [Coqui XTTS-v2 — Hugging Face](https://huggingface.co/coqui/XTTS-v2)
- [MuseTalk — Pixazo](https://www.pixazo.ai/blog/best-open-source-lip-sync-models)

### 閉源平台

- [Synthesia — 官方網站](https://www.synthesia.io/)
- [HeyGen — 官方網站](https://www.heygen.com/)
- [Colossyan — 官方網站](https://www.colossyan.com/)
- [D-ID — 官方網站](https://www.d-id.com/)
- [LTX Studio — 官方網站](https://ltx.studio/)
- [ElevenLabs — 官方網站](https://elevenlabs.io/)
- [Filmustage — 官方網站](https://filmustage.com/)

### 研究文章與指南

- [AI Filmmaking Pipeline 2026 — DeepFiction](https://www.deepfiction.ai/blog/ai-filmmaking-pipeline-script-to-screen-2026)
- [Best AI Training Video Generators 2026 — X-Pilot](https://www.x-pilot.ai/blog/best-ai-training-video-generators-2026-ld-tools-comparison)
- [NotebookLM Cinematic Video Overviews — Google Blog](https://blog.google/innovation-and-ai/products/notebooklm/generate-your-own-cinematic-video-overviews-in-notebooklm/)
- [HeyGen vs Synthesia 2026 — WaveSpeedAI](https://wavespeed.ai/blog/posts/heygen-vs-synthesia-comparison-2026/)
- [Synthesia vs Colossyan 2026 — Neuwark](https://neuwark.com/blog/synthesia-vs-colossyan-2026-review-best-ai-platform-for-corporate-training)
- [Video as Code: Which Library? — Medium](https://sumeetkg.medium.com/video-as-code-which-library-should-you-choose-8807ac1bda6b)
- [FLUX LoRA Training for $1 — Medium](https://medium.com/@geronimo7/how-to-train-a-flux1-lora-for-1-dfd1800afce5)
- [GPU Requirements Cheat Sheet 2026 — Spheron](https://www.spheron.network/blog/gpu-requirements-cheat-sheet-2026/)
- [Open Source Image Generation 2026 — Pixazo](https://www.pixazo.ai/blog/top-open-source-image-generation-models)
- [Open Source TTS Models 2026 — BentoML](https://www.bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models)
- [AI Video Production Pipeline — Joyspace](https://joyspace.ai/ai-video-production-pipeline-1000-clips-monthly-2026)
- [Open Source Video Generation Models — Hyperstack](https://www.hyperstack.cloud/blog/case-study/best-open-source-video-generation-models)
- [NVIDIA RTX AI Video Generation](https://blogs.nvidia.com/blog/rtx-ai-garage-ces-2026-open-models-video-generation/)

---

*本報告由 AI 輔助研究生成，資料時效為 2026 年 3 月。建議在採購前重新確認各平台最新定價與功能。*
