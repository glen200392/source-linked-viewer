# AI 模型全景研究報告：從語言模型到世界模型的演進

> **作者**：Glen Ho（AI 輔助研究）
> **日期**：2026-03-09
> **版本**：v1.0

---

## 目錄

1. [摘要](#1-摘要)
2. [為什麼 AI 還無法像人一樣操作畫面？](#2-為什麼-ai-還無法像人一樣操作畫面)
3. [截圖理解 vs 人類直覺操作的落差](#3-截圖理解-vs-人類直覺操作的落差)
4. [AI 發展史完整時間軸](#4-ai-發展史完整時間軸)
5. [模型架構分類與關係](#5-模型架構分類與關係)
6. [世界模型（World Models）深度研究](#6-世界模型world-models深度研究)
7. [LLM 是否擁有世界模型？大辯論](#7-llm-是否擁有世界模型大辯論)
8. [不同架構在世界模型中的角色](#8-不同架構在世界模型中的角色)
9. [未來展望與趨勢預測](#9-未來展望與趨勢預測)
10. [完整參考文獻](#10-完整參考文獻)

---

## 1. 摘要

本報告系統性地研究了 AI 模型的能力邊界、架構演進與未來方向。核心發現如下：

- **GUI 操作瓶頸**：AI 無法即時操作畫面的根本原因在於「截圖→推理→行動」迴圈延遲（2-5 秒 vs 人類 200ms）、缺乏空間-時間連續性、以及誤差累積效應（每步 95% 成功率，50 步後僅剩 7%）。
- **架構演進**：從符號 AI（1950s）→ 統計學習（2000s）→ 深度學習（2012）→ Transformer（2017）→ 多模態推理模型（2024）→ 世界模型（2025+），AI 正在從「預測下一個 token」走向「模擬整個世界」。
- **世界模型崛起**：Sora、Genie 2、NVIDIA Cosmos、World Labs 等專案標誌著 AI 從文字生成走向物理世界理解的轉折點，但真正的因果物理推理仍未達成。

---

## 2. 為什麼 AI 還無法像人一樣操作畫面？

### 2.1 核心瓶頸：延遲問題

人類與 AI 在操作電腦時的根本差異在於 **反應速度**：

| 環節 | 人類 | AI Agent |
|------|------|----------|
| 視覺感知 | 連續 60Hz 影像 | 離散截圖（~0.5Hz） |
| 反應時間 | 140-200ms | 2,000-5,000ms |
| 回饋機制 | 即時觸覺/視覺回饋 | 無回饋（只有下一張截圖） |
| 處理方式 | 並行視覺處理 | 序列 token 生成 |

AI 的「截圖→分析→行動」迴圈拆解如下：
- 截圖擷取：100-500ms
- 網路傳輸（API 呼叫）：200-500ms
- 模型推理（首個 token）：597ms-2 秒
- 逐 token 生成：30-100ms/token
- 動作執行：50-200ms

**合計約 2-5 秒完成一個動作**，而人類只需 200ms。

> 來源：[LLM Latency Benchmark](https://research.aimultiple.com/llm-latency-benchmark/)、[Understanding Human Reaction Time](https://www.oreateai.com/blog/understanding-human-reaction-time-what-the-numbers-reveal-8638e0f32a15607503bfe85436b55628)

### 2.2 序列處理 vs 並行視覺

這是最根本的架構性限制：

- **LLM 逐 token 生成**：Transformer 必須等第 9 個 token 計算完才能預測第 10 個，這是自迴歸解碼的固有限制。
- **人類並行視覺**：數百萬感光細胞同時處理整個場景，搭配平行注意力機制。
- **Vision Transformer 的 patch 限制**：影像被切成 16×16 的 patch 作為 token，這導致粗糙的視覺感知——GUI 上的座標是連續且高解析度的，但模型只看到離散的低解析度 patch。

> 來源：[Vision Transformers Explained](https://blog.roboflow.com/vision-transformers/)、[Dynamic Granularity in ViT](https://arxiv.org/html/2511.19021v1)

### 2.3 誤差累積：多步任務的致命問題

這是 AI 操作 GUI 最嚴重的實際問題：

```
單步成功率 95% → 50 步任務成功率 = 0.95^50 = 7.7%
單步成功率 99% → 100 步任務成功率 = 0.99^100 = 36.6%
```

**具體失敗模式**：
1. **狀態幻覺**：模型誤讀畫面狀態（如按鈕看起來已點但實際未觸發），導致錯誤的下一步
2. **目標漂移**：早期錯誤累積後，Agent 忘記原始目標
3. **迴圈陷阱**：Agent 重複點擊同一元素，困在錯誤狀態中
4. **跨應用問題**：切換應用程式時失去上下文

> 來源：[Where LLM Agents Fail](https://arxiv.org/pdf/2509.25370)、[Compounding Error in LLMs](https://wand.ai/blog/compounding-error-effect-in-large-language-models-a-growing-challenge)

### 2.4 當前基準測試結果

| 基準測試 | 任務類型 | 人類表現 | 最佳 AI | AI 模型 |
|----------|----------|----------|---------|---------|
| OSWorld（原始 2024） | 桌面環境 | 72.4% | 14.9% | Claude 3.5 Sonnet |
| OSWorld-Verified（2025） | 桌面環境 | 72.4% | 72.5% | Claude Sonnet 4.6 |
| WebVoyager | 網頁導航 | — | 97.1% | Surfer 2 |
| WebArena | 網頁自動化 | — | 58.1% | OpenAI CUA |
| ScreenSpot Pro | 視覺定位 | — | 39.6% | OmniParser + GPT-4o |

**關鍵觀察**：
- 網頁任務（83-97%）已接近「解決」，但桌面環境（38-75%）仍有巨大差距
- 2024→2025 的進步驚人：Claude 在 OSWorld 從 14.9% 飆升到 72.5%

> 來源：[OSWorld Benchmark](https://arxiv.org/abs/2404.07972)、[WebVoyager Leaderboard](https://leaderboard.steel.dev/)

---

## 3. 截圖理解 vs 人類直覺操作的落差

### 3.1 視覺定位問題（Visual Grounding）

AI 面臨的核心挑戰是：**如何將視覺理解精確對應到像素座標**。

**具體困難**：

1. **Patch 到 Pixel 的落差**：Vision Transformer 以 16×16 patch 處理影像（粗略的 token），但 GUI 座標是連續且高解析度的。模型必須從粗略的視覺 token 推斷精密的像素級動作。

2. **解析度不匹配**：在 1280×720 上訓練的模型，面對 4K 螢幕時無法可靠地推斷座標。

3. **監督歧義**：一個按鈕內的任何位置點擊都是有效的，但座標預測方法將此視為單點預測問題。

4. **幻覺問題**：大型視覺語言模型經常「幻覺」不存在的元素，或錯誤辨識元素功能（如將「放大鏡圖示」的搜尋功能誤認為縮放功能）。

**研究突破**：
- **OmniParser + GPT-4o**：在 ScreenSpot Pro 上達到 39.6%（GPT-4o 單獨僅 0.8%）
- **ShowUI**：透過 UI 圖結構減少 90% 幻覺動作
- **GUI-Actor**：無座標定位（coordinate-free），使用專注 attention token 避免顯式座標預測

> 來源：[GUI-Actor](https://arxiv.org/html/2506.03143v1)、[OmniParser V2](https://www.microsoft.com/en-us/research/articles/omniparser-v2-turning-any-llm-into-a-computer-use-agent/)

### 3.2 缺乏空間-時間連續性與本體感覺

**離散幀 vs 連續影像**：
- 人類看到 ~60Hz 的連續影像，伴隨平滑的動態感知
- AI Agent 看到離散截圖，約 0.5Hz（每 2 秒一張）
- 拖曳操作期間沒有滑鼠位置回饋、按鈕按下狀態或平滑捲動反映

**缺失的本體感覺（Proprioception）**：
- 人類「感覺得到」滑鼠在哪、按鈕是否被按住、捲動了多少
- AI Agent 完全沒有回饋：只知道當前截圖的內容
- 這使得拖曳滑桿、長按操作、偵測 hover 狀態等操作極其困難

> 來源：[Navigating the Digital World as Humans Do](https://arxiv.org/html/2410.05243v1)、[Ferret-UI 2](https://machinelearning.apple.com/research/ferret-ui-2)

### 3.3 當前主要方法比較

| 方法 | 代表產品 | 優點 | 缺點 |
|------|----------|------|------|
| **截圖為主（Vision）** | Claude Computer Use、OpenAI Operator | 跨平台通用、類似人類視覺推理 | 慢、成本高、易幻覺 |
| **DOM 為主（結構化）** | Selenium、Puppeteer | 精確、快速、低成本 | 脆弱、不適用動態元素 |
| **混合方法** | Microsoft UFO²、browser-use | 強健性佳 | 複雜度高 |

**主要產品現況**：

| 產品 | 發布 | 架構 | 特色 |
|------|------|------|------|
| **Claude Computer Use** | 2024.10 | Claude + 截圖 + 動作原語 | 72.5% OSWorld-Verified |
| **OpenAI Operator/CUA** | 2025.01 | GPT-4o + RL | 87% WebVoyager |
| **Google Project Mariner** | 2025.05 | Gemini 2.0 + 雲端 | 83.5% WebVoyager、10 個瀏覽器並行 |
| **Microsoft UFO² + OmniParser** | 2024-2025 | DOM + Vision 混合 | Windows UI 自動化 API |
| **ShowUI**（開源） | 2024 | 2B 參數 VLA | 消費級 GPU 可執行、減少 90% 幻覺 |
| **CogAgent** | CVPR 2024 | 18B 多模態 VLM | 雙編碼器、支援 1120×1120 |
| **Ferret-UI**（Apple） | 2024-2025 | 多平台 UI 理解 | 3B 輕量版可在裝置上執行 |

> 來源：[Anthropic Computer Use](https://www.anthropic.com/news/3-5-models-and-computer-use)、[OpenAI Operator](https://openai.com/index/introducing-operator/)、[Project Mariner](https://deepmind.google/models/project-mariner/)

---

## 4. AI 發展史完整時間軸

### 4.1 符號 AI 與第一次 AI 寒冬（1950s-1980s）

```
1950  Alan Turing 發表「Computing Machinery and Intelligence」，提出圖靈測試
  │
1956  Dartmouth 夏季研究計畫 —— AI 正式成為學術領域
  │
1958  Frank Rosenblatt 發明感知器（Perceptron）
  │
1969  ▼ Minsky & Papert 出版《Perceptrons》，證明單層感知器無法解 XOR 問題
  │     → 神經網路研究資金枯竭
1973  ▼ 英國 Lighthill Report 嚴厲批評 AI 研究 → 第一次 AI 寒冬
```

> 來源：[Computing Machinery and Intelligence (Turing, 1950)](https://courses.cs.umbc.edu/471/papers/turing.pdf)

### 4.2 專家系統與第二次 AI 寒冬（1980s-1990s）

```
1980  專家系統興起：XCON 為 DEC 節省 4,000 萬美元
  │   LISP 語言、Prolog、專用 LISP 機器
  │
1987  ▼ LISP 機器市場崩潰；專家系統維護成本過高、脆弱性明顯
  │     → 第二次 AI 寒冬（1987-1993）
```

### 4.3 統計機器學習時代（2000s）

```
2001  Random Forest（Breiman & Cutler）正式提出
  │
2000s SVM（支持向量機）主導各項基準測試
  │   Kernel Methods、Ensemble Learning 取代符號方法
  │
2006  ★ Geoffrey Hinton 提出 Deep Belief Networks (DBN)
      ─ 貪婪逐層訓練（Greedy Layer-wise Training）
      ─ 使用對比散度（Contrastive Divergence）訓練 RBM
      ─ 證明深層網路可以被有效訓練 → 深度學習復興
```

> 來源：[Deep Belief Networks (Hinton et al., 2006)](https://proceedings.mlr.press/v5/salakhutdinov09a/salakhutdinov09a.pdf)

### 4.4 深度學習革命（2012-2017）

```
2012  ★★★ AlexNet 在 ImageNet 競賽中以 15.3% top-5 錯誤率擊敗第二名（26%）
  │       ─ Alex Krizhevsky, Ilya Sutskever, Geoffrey Hinton
  │       ─ 大型標註資料集 + GPU 運算 + 改進訓練技術（ReLU、Dropout）
  │       → 範式轉移：從手工特徵到端對端學習
  │
2014  ★ Ian Goodfellow 提出 GAN（生成對抗網路）
  │       ─ 生成器 vs 判別器的對抗遊戲
  │       ─ arXiv:1406.2661
  │
2014  ★ Bahdanau 注意力機制（Attention Mechanism）
  │       ─ 解決長序列的梯度消失問題
  │       ─ arXiv:1409.0473
  │
2017  ★★★★ "Attention Is All You Need" —— Transformer 架構誕生
          ─ Vaswani et al., NeurIPS 2017
          ─ 多頭自注意力、無遞迴、無卷積
          ─ WMT 2014 英德翻譯：28.4 BLEU（領先 2+ BLEU）
          ─ 比 RNN/CNN 更可並行化、訓練更快、品質更優
          → 此後所有 LLM、視覺模型、擴散模型的基礎架構
```

> 來源：[Attention Is All You Need (arXiv:1706.03762)](https://arxiv.org/abs/1706.03762)

### 4.5 預訓練語言模型時代（2018-2020）

```
2018  BERT（Google）
  │   ─ 編碼器（Encoder-only）Transformer，雙向訓練
  │   ─ 遮罩語言模型（MLM）+ 下句預測（NSP）
  │   ─ arXiv:1810.04805
  │
2018  GPT-1（OpenAI）—— 117M 參數，解碼器（Decoder-only）
  │
2019  GPT-2 —— 1.5B 參數，展示零樣本任務遷移能力
  │
2020  ★★★ 三大地震性突破：
  │
  ├── Scaling Laws（Kaplan et al.）
  │     ─ 損失函數遵循冪律：L(N) ∝ N^(-α)，α ≈ 0.07
  │     ─ 增加參數比擴大訓練資料重要 3 倍
  │     ─ arXiv:2001.08361
  │
  ├── GPT-3 —— 175B 參數（史上最大非稀疏模型）
  │     ─ 在 300B tokens 上訓練
  │     ─ 展示 Few-shot Learning：僅靠提示中的幾個範例即可執行新任務
  │     ─ arXiv:2005.14165
  │
  ├── DDPM（Ho, Jain, Abbeel）
  │     ─ 去噪擴散概率模型
  │     ─ 迭代去噪過程從隨機噪聲生成高品質影像
  │     ─ arXiv:2006.11239
  │
  └── Vision Transformer (ViT)
        ─ 「一張影像值 16×16 個字」
        ─ 純 Transformer 處理影像 patch，無卷積
        ─ 當預訓練於大資料集時可匹配/超越 CNN
```

### 4.6 ChatGPT 爆發與多模態時代（2022-2024）

```
2022.08  Stable Diffusion 開源 —— Latent Diffusion Model
  │        ─ VAE 壓縮 + U-Net 去噪 + CLIP 文字編碼
  │        ─ 比像素空間擴散快 ~10 倍
  │
2022.11  ★★★★ ChatGPT 發布
  │        ─ GPT-3.5 + RLHF（人類回饋強化學習）
  │        ─ 5 天破 100 萬用戶；2023.01 達 1 億月活
  │        → 展示對齊 LLM 的實際可行性
  │
2023.02  LLaMA（Meta）—— 7B-65B 參數開源模型
  │
2023.03  ★★★ GPT-4 發布
  │        ─ 多模態：接受文字 + 影像輸入
  │        ─ 模擬律師考試前 10%（vs GPT-3.5 倒數 10%）
  │        ─ arXiv:2303.08774
  │
2023.09  Mistral 7B —— 7.3B 參數超越 LLaMA 2 13B
  │
2023.09  DALL-E 3 —— 更精確的文字描述對應
  │
2024.03  Claude 3 家族（Anthropic）—— 多模態視覺 + 語言
  │
2024.06  Claude 3.5 Sonnet —— 視覺基準超越 Claude 3 Opus
```

### 4.7 推理模型與 Agent 時代（2024-2026）

```
2024.10  ★★ OpenAI o1 —— 「慢思考」範式
  │        ─ 測試時計算縮放（Test-time Compute Scaling）
  │        ─ 推理時分配更多計算資源
  │        ─ 程式競賽第 89 百分位、數學奧林匹克前 500
  │
2024.10  Claude Computer Use —— AI 操作電腦的里程碑
  │
2025.01  ★★ DeepSeek-R1
  │        ─ 純大規模 RL 訓練（無監督微調）
  │        ─ 與 o1 推理能力相當
  │        ─ 成本僅 $2.19/M tokens（vs o1-mini $12/M）
  │        ─ 開源可微調
  │
2025     Mixture of Experts 規模化
  │        ─ Mixtral 8x7B：46.7B 總參數，~12.9B 活躍/token
  │        ─ DeepSeek-V3：236B 參數，21B 活躍
  │
2025-26  ★★★ 世界模型（World Models）爆發
           ─ Sora、Genie 2、NVIDIA Cosmos、World Labs Marble
           ─ 從「預測 token」走向「模擬世界」
```

---

## 5. 模型架構分類與關係

### 5.1 Transformer 家族

#### 5.1.1 解碼器（Decoder-only）—— 自迴歸 LLM

**特徵**：單向因果注意力，逐 token 生成

| 模型 | 參數量 | 年份 | 特色 |
|------|--------|------|------|
| GPT-3 | 175B | 2020 | Few-shot Learning 開創者 |
| GPT-4 | 未公開 | 2023 | 多模態、推理能力飛躍 |
| Claude 3.5 Sonnet | 未公開 | 2024 | 視覺+語言、程式碼理解 |
| LLaMA 3.1 | 8B-405B | 2024 | 開源最強 |
| Mistral Large 2 | 未公開 | 2024 | 高效推理 |
| DeepSeek-V3 | 236B (21B active) | 2025 | MoE 架構 |

#### 5.1.2 編碼器（Encoder-only）—— 雙向理解

**特徵**：雙向注意力，適用分類/嵌入任務

- **BERT**（2018, Google）：110M/340M，遮罩語言模型
- **RoBERTa**（2019, Meta）：BERT 的工程改良版
- **DINOv2**：自監督視覺編碼器

#### 5.1.3 編碼器-解碼器（Encoder-Decoder）

**特徵**：獨立的編碼與解碼堆疊，適合翻譯/摘要

- **T5**（Google, 2020）：所有任務統一為 text-to-text
- **BART**（Meta, 2020）：雙向編碼 + 自迴歸解碼

#### 5.1.4 視覺 Transformer

- **ViT**：影像切 16×16 patch 作為 token 序列
- **DINOv2**：自監督、密集 patch 級理解

#### 5.1.5 多模態 Transformer

- **GPT-4V/4o**：視覺 + 語言統一處理
- **Claude 3/3.5**：視覺 + 語言統一解碼器
- **Gemini**：原生多模態（從訓練起就是多模態）

### 5.2 擴散模型（Diffusion Models）

#### 理論基礎

```
正向過程（加噪）：x₀ → x₁ → x₂ → ... → xₜ（純噪聲）
反向過程（去噪）：xₜ → xₜ₋₁ → ... → x₁ → x₀（生成結果）
```

| 模型 | 年份 | 類型 | 特色 |
|------|------|------|------|
| DDPM | 2020 | 像素空間擴散 | 奠基性工作 |
| Stable Diffusion | 2022 | 潛在空間擴散 | VAE + U-Net + CLIP，開源 |
| DALL-E 2/3 | 2022/2023 | 文字到影像 | CLIP 嵌入 + 擴散 |
| Sora | 2024 | 擴散 Transformer (DiT) | 影片生成，可變長寬比 |
| Veo 2 | 2024 | 影片擴散 | 4K、電影攝影理解 |
| Runway Gen-3/4.5 | 2024-2025 | 影片擴散 | 動態控制、世界模型 |

#### 擴散 Transformer（DiT）—— 關鍵交會點

**這是 Transformer 與擴散模型的融合**：用 Vision Transformer 取代 U-Net 作為去噪骨幹。

```
傳統：文字編碼 → CLIP → U-Net（去噪）→ VAE 解碼 → 影像
DiT：文字編碼 → CLIP → Transformer（去噪）→ VAE 解碼 → 影像/影片
```

DiT 使 Sora 能夠原生處理可變長寬比、解析度和時長。

### 5.3 非 Transformer 架構（新興替代方案）

#### 5.3.1 狀態空間模型（State Space Models）

| 模型 | 年份 | 複雜度 | 特色 |
|------|------|--------|------|
| S4 | 2021 | O(N) 線性 | 微分方程表示序列，高效卷積 |
| **Mamba** | 2023 | O(N) 線性 | 選擇性掃描（data-dependent gating） |
| Mamba-2 | 2024 | O(N) 線性 | 證明 SSM 與 Attention 數學等價 |

**Mamba 的關鍵優勢**：
- 推理速度是 Transformer 的 **5 倍**
- 可處理高達 **1M token** 的上下文
- 推理時記憶體恆定（不需 KV-cache）

**限制**：在複製/上下文學習任務上不如 Transformer、大規模經驗驗證較少

> 來源：[Mamba (arXiv:2312.00752)](https://arxiv.org/abs/2312.00752)

#### 5.3.2 RWKV（RNN-Transformer 混合）

- 訓練時可並行化（如 Transformer），推理時為線性時間（如 RNN）
- 複雜度 O(N)，恆定記憶體，推理速度不受上下文長度影響
- 不需 KV-cache
- RWKV-7 "Goose"：最新版本，純 RNN 架構

> 來源：[RWKV (arXiv:2305.13048)](https://arxiv.org/abs/2305.13048)

#### 5.3.3 其他新興架構

| 架構 | 特色 | 適用場景 |
|------|------|----------|
| **KAN（Kolmogorov-Arnold Networks）** | 邊上的可學習函數取代節點上的固定激活函數；更少參數、更高精度 | 科學計算、PDE 求解 |
| **xLSTM** | 指數門控 + 參數化投影的 LSTM 改良版 | 時序序列建模 |
| **Liquid Neural Networks** | 連續時間動力學，參數更少 | 機器人、物理系統 |
| **MoE（Mixture of Experts）** | 稀疏激活：8 個專家中只啟用 2 個 | 大規模模型的高效推理 |

> 來源：[KAN (arXiv:2404.19756)](https://arxiv.org/abs/2404.19756)

### 5.4 生成模型分類總覽

| 模型類型 | 核心方程 | 優勢 | 劣勢 |
|----------|----------|------|------|
| **自迴歸（GPT）** | p(x) = Π p(xᵢ\|x<ᵢ) | 精確似然、已證明的 scaling | 逐 token 生成（慢） |
| **擴散（DDPM/SD）** | 迭代去噪 | 高品質、穩定訓練 | 推理慢（需多步去噪） |
| **流模型（Flow）** | 可逆變換 | 精確似然、穩定 | 架構複雜 |
| **GAN** | 對抗性 min-max | 快速推理、高品質影像 | 訓練不穩定、模式崩塌 |
| **VAE** | ELBO 下界 | 穩定訓練、可解釋潛在空間 | 後驗崩塌、生成模糊 |
| **SSM（Mamba）** | 線性動力學 + 選擇性門控 | 線性複雜度、長上下文 | 較新、經驗驗證不足 |

### 5.5 架構關係圖

```
                           ┌─────────────────────┐
                           │    Transformer       │
                           │   (2017, Vaswani)    │
                           └──────────┬──────────┘
                                      │
              ┌───────────────────────┼───────────────────────┐
              │                       │                       │
     ┌────────▼────────┐    ┌────────▼────────┐    ┌────────▼────────┐
     │  Decoder-only   │    │  Encoder-only   │    │ Encoder-Decoder │
     │ GPT, LLaMA,     │    │ BERT, RoBERTa   │    │ T5, BART        │
     │ Claude, Mistral  │    │ DINOv2          │    │                 │
     └────────┬────────┘    └─────────────────┘    └─────────────────┘
              │
     ┌────────▼────────┐
     │  多模態 LLM     │
     │ GPT-4V, Gemini  │──────────┐
     │ Claude 3.5      │          │
     └────────┬────────┘          │
              │                    │
              │    ┌───────────────▼──────────────┐
              │    │  擴散 Transformer (DiT)       │
              │    │  Sora, Veo, Runway           │
              │    │  ← Transformer + 擴散模型融合  │
              │    └──────────────────────────────┘
              │                    ▲
              │         ┌──────────┘
              │         │
     ┌────────▼─────────▼────┐
     │    擴散模型            │
     │  DDPM → Latent Diff.  │
     │  → Stable Diffusion   │
     │  → DALL-E 2/3         │
     └───────────────────────┘

  ─────── 非 Transformer 替代路線 ───────

  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │  SSM/Mamba   │  │    RWKV      │  │    KAN       │
  │  O(N) 線性   │  │  RNN+Trans.  │  │ 可學習邊函數  │
  │  長上下文     │  │  混合架構     │  │  科學計算     │
  └──────────────┘  └──────────────┘  └──────────────┘
```

---

## 6. 世界模型（World Models）深度研究

### 6.1 什麼是世界模型？

**定義**：世界模型是一種**內部表徵**，允許 Agent：
1. 將觀測編碼為壓縮的潛在空間（Encode）
2. 給定動作，預測未來潛在狀態（Predict）
3. 在不與真實環境互動的情況下，模擬/想像未來軌跡（Imagine）
4. 在想像中學習最優策略，再部署到真實世界（Act）

### 6.2 歷史根源

**Kenneth Craik（1943）**——《The Nature of Explanation》：
首次提出大腦建構外部世界的「小尺度模型」，並在心理上向前推演以預測結果。這奠定了「智慧需要世界模擬」的理論基礎。

**Ha & Schmidhuber（2018）**——"World Models"：
現代世界模型的正式化，包含三個組件：
- **VAE**（視覺）：將觀測壓縮為潛在表徵
- **MDN-RNN**（記憶）：預測未來潛在狀態
- **Controller**（控制器）：根據潛在狀態選擇動作

> 來源：[World Models (arXiv:1803.10122)](https://arxiv.org/abs/1803.10122)、[互動展示](https://worldmodels.github.io/)

### 6.3 Yann LeCun 的 JEPA 願景

**核心論文**：[A Path Towards Autonomous Machine Intelligence (2022)](https://openreview.net/pdf?id=BZ5a1r-kVsf)

**LeCun 的核心論點**：
1. **自迴歸 LLM 有根本性限制**：它們預測原始感覺資料（下一個 token/像素），需要指數級的樣本複雜度
2. **JEPA 在抽象表徵空間中預測**：不預測像素，而是預測潛在嵌入（latent embedding）
3. **架構**：編碼器（感知）→ 預測器（潛在空間中的前向模型）→ 解碼器（可選的重建）

**為什麼 JEPA 優於重建式方法**：
- 不顯式預測像素 → 避免幻覺不可察覺的細節
- 在緊湊潛在空間中預測 → 需要更少資料
- 支援分層推理 → 多時間尺度規劃

**LeCun 對 LLM 的立場（2024）**：
- 自迴歸模型根本無法規劃或多步推理
- 誤差隨展開長度指數累積
- 單靠規模擴大無法克服這個架構性限制
- **AGI 必需**：世界模型 + 規劃能力 + 分層推理

### 6.4 當前影片/影像世界模型

#### OpenAI Sora（2024.02）

**概念**：「影片生成模型作為世界模擬器」

**湧現能力**（無顯式 3D 歸納偏置）：
- **3D 空間一致性**：攝影機運動維持物體在 3D 空間中的位置
- **物理模擬**：畫家的筆觸持續留在畫布上；Minecraft 遊戲畫面
- **物體恆常性**：追蹤被遮擋的物體

**限制**：部分物理理解是表面的；嚴重依賴訓練資料的模式匹配

> 來源：[Video generation models as world simulators](https://openai.com/index/video-generation-models-as-world-simulators/)

#### Google Veo 2（2024.12）

- 4K 解析度（4096×2160），可延長至 2+ 分鐘
- 流體動力學和光照模擬
- 理解攝影機鏡頭語言（「18mm 鏡頭」、「跟拍鏡頭」）
- 在盲測中優於 Sora（59% vs 27% 偏好）

> 來源：[Google Veo 2](https://blog.google/technology/google-labs/video-image-generation-update-december-2024/)

#### Runway Gen-3 / GWM-1

- GWM-1（General World Model）：互動式、可控、即時模擬
- 三種變體：GWM Worlds（環境）、GWM Avatars（角色）、GWM Robotics（操作）
- 細粒度動態控制：動態筆刷、方向性攝影機移動

> 來源：[Runway Gen-3 Alpha](https://runwayml.com/research/introducing-gen-3-alpha)

### 6.5 互動式世界模型：遊戲與環境

#### DeepMind Genie 2（2024.12）

**第一個大規模基礎世界模型**，用於互動式環境：
- **輸入**：文字提示或影像 → **輸出**：可互動的 3D 世界（10-60 秒）
- **能力**：物體恆常性、角色動畫、Agent 行為預測、鍵盤控制
- **訓練**：大規模影片資料集，規模化產生湧現能力

> 來源：[Genie 2 Blog](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)

#### GameNGen（Google Research, 2024）

**第一個以神經網路即時運行 DOOM 的「遊戲引擎」**：
- 擴散模型在錄製的 RL Agent 遊戲畫面上訓練
- 效能：單顆 TPU 上 20 FPS，5+ 分鐘持續
- 品質：PSNR 29.4，人類評測者幾乎無法區分與真實遊戲
- **意義**：證明生成模型可以作為完整的遊戲模擬器

> 來源：[Diffusion Models Are Real-Time Game Engines (arXiv:2408.14837)](https://arxiv.org/abs/2408.14837)

#### UniSim（ICLR 2024 最佳論文）

- 統一的 action-in-video-out 框架
- 支援高層（「打開抽屜」）和低層（「移動 x,y」）動作
- 零樣本真實世界遷移：在模擬中訓練的策略可直接轉移到真實機器人

> 來源：[UniSim (arXiv:2310.06114)](https://arxiv.org/abs/2310.06114)

### 6.6 3D/空間世界模型

#### World Labs —— Fei-Fei Li 的「大型世界模型」

**產品：Marble**（2025.11 發布）
- 文字提示、照片、影片、3D 佈局 → 持久 3D 環境
- 可下載、可編輯的 3D 世界（不僅是即時）
- **World API**（2026.01）：開發者存取大型世界模型
- **估值**：50 億美元（5 億募資）
- **願景**：「空間智慧」—— 看見 → 感知 → 推理 → 行動

> 來源：[World Labs TechCrunch](https://techcrunch.com/2025/11/12/fei-fei-lis-world-labs-speeds-up-the-world-model-race-with-marble-its-first-commercial-product/)

#### NVIDIA Cosmos（2025）

**世界基礎模型平台**：
- **Cosmos-Predict2.5**：預測未來影片幀（影片擴散）
- **Cosmos Reason**：時空感知模型 + 思維鏈推理
- 應用：自動駕駛、機器人、影片分析 AI Agent
- 早期採用者：1X、Agility、Figure AI、Uber

> 來源：[NVIDIA Cosmos (arXiv:2501.03575)](https://arxiv.org/abs/2501.03575)

### 6.7 機器人與具身世界模型

| 專案 | 組織 | 類型 | 關鍵成就 |
|------|------|------|----------|
| **Tesla FSD** | Tesla | 自動駕駛 | 端對端神經網路取代 300,000+ 行 C++ |
| **RT-2 / RT-X** | DeepMind | VLA 模型 | 零樣本泛化從 32% 提升到 62% |
| **V-JEPA 2** | Meta FAIR | 影片世界模型 | 1.2B 參數，零樣本機器臂控制 |
| **GR00T N1** | NVIDIA | 人形機器人基礎模型 | 自然語言理解 + 模仿學習 |
| **Optimus + Grok** | Tesla | 人形機器人 | 2026 Q2 計劃生產 50K 單位 |

**Meta V-JEPA 2 的重要性**：
- 在 1M+ 小時影片 + 1M 影像上訓練
- 77.3% 動作理解準確度（Something-Something v2）
- **零樣本機器人控制**：Franka 機器臂抓取/放置，無需任何機器人特定訓練資料
- 架構與 LeCun 的 JEPA 框架一致

> 來源：[V-JEPA 2](https://arxiv.org/abs/2506.09985)、[RT-2](https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-action/)

### 6.8 基於模型的強化學習（MBRL）

世界模型的核心應用場景之一是 MBRL：

```
Dreamer 管線：
1. 學習世界模型（從真實經驗中學習環境動力學）
2. 在想像中展開軌跡（不需真實互動）
3. 在想像的軌跡上訓練 Actor/Critic
4. 將學到的策略部署到真實世界
```

| 演算法 | 年份 | 特色 |
|--------|------|------|
| **PlaNet** | 2018 | 從像素學習潛在動力學模型 |
| **Dreamer v1-v4** | 2019-2025 | 150+ 任務、固定超參數 |
| **MuZero** | 2020 | 抽象模型 + MCTS 規劃 |
| **MuDreamer** | 2024 | 移除像素重建，純預測性世界模型 |

> 來源：[Dreamer](https://danijar.com/project/dreamer4/)、[MuZero (Nature)](https://www.nature.com/articles/s41586-025-08744-2)

---

## 7. LLM 是否擁有世界模型？大辯論

### 7.1 支持方：LLM 具有湧現的世界表徵

#### Othello-GPT 實驗（Li et al., 2023）

**最具影響力的證據**：
- 在合法 Othello 走法序列上訓練的 GPT 變體
- 發現隱藏狀態中存在**湧現的內部棋盤狀態表徵**
- 64 個二層 MLP 探針的錯誤率從 26.2%（隨機）降至 1.7%
- **含義**：Transformer 可以發展內部世界模型，即使任務不要求像素生成

> 來源：[Emergent World Representations (arXiv:2210.13382)](https://arxiv.org/abs/2210.13382)

#### 後續機制可解釋性（Nanda et al., 2023）

- 發現**線性湧現表徵**
- 可通過向量算術進行因果干預
- 棋盤狀態表示為「我的棋子」vs「對方棋子」而非絕對顏色

> 來源：[Othello-GPT Has A Linear World Representation](https://www.neelnanda.io/mechanistic-interpretability/othello)

#### LLM 推理能力的間接證據

- GPT-4：模擬律師考試前 10%、93% 奧林匹克題
- 暗示某種形式的抽象推理，超越表面統計

### 7.2 反對方：LLM 只是「隨機鸚鵡」

#### Bender & Koller（2021）——「On the Dangers of Stochastic Parrots」

**核心論點**：
1. LLM 是「隨機鸚鵡」—— 拼接學到的語言模式，沒有語義基礎
2. **符號接地問題**：沒有真實世界經驗；意義未植根於感覺運動互動
3. **缺乏社會存取**：無法參與賦予語言意義的社會互動
4. **沒有統一的世界模型**：語言模式獨立於因果世界結構

> 來源：[Stochastic Parrots](https://s10251.pcdn.co/pdf/2021-bender-parrots.pdf)

#### Yann LeCun 的立場（2024）

- 自迴歸模型**無法真正推理或規劃**（指數級誤差累積）
- 缺乏真正的世界理解
- 當前 LLM 是精緻的模式匹配器，不是推理者

### 7.3 當前共識

```
╔══════════════════════════════════════════════════════════════╗
║  LLM 很可能具有類似世界模型的領域特定湧現表徵                    ║
║  （如 Othello 案例），但僅限於訓練資料中大量存在的領域            ║
║                                                              ║
║  不是一般意義上的真正世界模型 ——                                ║
║  無法將理解遷移到新穎的物理情境                                  ║
║                                                              ║
║  「帶結構的模式匹配」：發展出類似世界模型的統計規律性，             ║
║   但缺乏因果基礎                                               ║
║                                                              ║
║  未來很可能需要多模態訓練（視覺 + 動作 + 語言）                  ║
║  才能獲得有根基的理解                                           ║
╚══════════════════════════════════════════════════════════════╝
```

### 7.4 世界模型 vs LLM 技術差異

| 面向 | 世界模型 | LLM |
|------|----------|-----|
| **預測空間** | 抽象潛在狀態 | 文字空間中的下一個 token |
| **基礎** | 感覺運動經驗/影片 | 語言共現 |
| **規劃** | 顯式（Dreamer, MuZero） | 隱式（上下文學習） |
| **樣本效率** | 高（從少量範例學習） | 低（需要大量文字） |
| **遷移** | 可泛化到新環境 | 受限於訓練分佈 |
| **因果性** | 可學習因果動力學 | 捕捉相關性，非因果性 |
| **多模態** | 原生（視覺+動作+語言） | 以文字為中心（正在擴展） |

---

## 8. 不同架構在世界模型中的角色

### 8.1 Transformer

- **優勢**：捕捉長距離依賴、基於注意力的推理
- **限制**：O(n²) 複雜度；超長序列困難；連續狀態預測不理想
- **世界模型應用**：Sora、Veo、Genie 2（作為擴散的基礎架構）

### 8.2 擴散模型

- **機制**：迭代去噪生成複雜高維分佈
- **優勢**：訓練穩定、高品質生成
- **世界模型應用**：影片生成（Sora, Veo 2, GameNGen）
- **限制**：推理時計算成本高

### 8.3 狀態空間模型（Mamba）

- **優勢**：O(n) 複雜度；5× 推理加速；適合超長序列
- **世界模型應用**：長上下文影片世界模型（state-space video world models）
- **限制**：複製/上下文學習較差；靈活性低
- **最新發現（2025）**：在長上下文檢索任務上可能超越 Transformer

### 8.4 混合方法

```
趨勢：不是 Transformer OR 其他，而是 Transformer AND 其他

Zamba = Mamba 骨幹 + 共享 Transformer 注意力
Samba = 選擇性 SSM + 滑動窗口注意力
NeRF-GS = NeRF（連續表徵）+ 3D Gaussian Splatting（快速渲染）
```

### 8.5 神經科學連結

#### 預測處理與自由能原則（Karl Friston）

**核心思想**：大腦通過兩種方式最小化「驚訝」（自由能）：
1. **更新內部模型**（感知推理）
2. **行動改變世界**（主動推理）

**與世界模型的聯繫**：
- 世界模型 = 大腦的生成模型
- 世界模型中的規劃 = 主動推理
- JEPA 的預測器 = 大腦的前向模型

> 來源：[Free Energy Principle (Nature)](https://www.nature.com/articles/nrn2787)

#### 全域工作空間理論（Bernard Baars）

- 意識在資訊通過注意力進入「全域工作空間」時湧現
- 類比：世界模型作為無意識模擬器；注意力機制門控什麼被規劃
- AI 應用：世界模型學習所有可能的未來（無意識），注意力/規劃機制選擇高價值軌跡（有意識的審議）

---

## 9. 未來展望與趨勢預測

### 9.1 影片模型真的理解物理嗎？

**關鍵研究**：[How Far is Video Generation from World Model](https://arxiv.org/abs/2411.02385)

**發現**：
- **分佈內**：對訓練物理的新實例完美泛化
- **分佈外**：在新穎物理場景上失敗
- **優先順序**：顏色 > 大小 > 速度 > 形狀（非物理原則）
- **結論**：模型記憶範例而非學習通用法則

**判定**：影片模型展示的是**表面物理理解**——從遵守物理的影片中湧現。不是真正的因果物理推理；更像是學到的規律性。

### 9.2 2026 預測（高信心度）

| 趨勢 | 具體預測 |
|------|----------|
| **物理 AI 爆發** | Tesla Optimus 50K 單位（$20-30K）；Boston Dynamics Atlas 商業化 |
| **世界模型主流化** | NVIDIA Cosmos、World Labs、Runway 成為商業平台 |
| **LLM + 世界模型融合** | 多模態模型結合文字推理與視覺世界模型 |
| **VLA 模型主導機器人** | Vision-Language-Action 模型成為機器人主流範式 |

### 9.3 2027-2030 展望（中等信心度）

**兩條可能路徑**：

```
路徑 A（融合）：LLM + 世界模型合併為統一的多模態基礎模型
    └── 單一模型處理語言、視覺、動作、物理模擬

路徑 B（專業化）：專門的世界模型用於機器人；LLM 用於語言/推理
    └── 分層整合，各司其職

LeCun 的觀點：傾向路徑 B，通過分層整合
```

### 9.4 未解決的研究問題

1. **物理理解**：當前擴散模型能否學習真正的因果物理，還是只能記憶相關性？
2. **接地問題**：世界模型如何在不具備身體經驗的情況下獲得真正的語義基礎？
3. **可擴展性**：Scaling Laws 是否適用於世界模型（如同 LLM）？（截至 2026.03 仍不明確）
4. **LLM 世界模型**：Othello-GPT 現象是特例還是通用的？LLM 是否為所有訓練任務發展世界模型？
5. **規劃最優性**：學習式規劃（policy gradient）vs 顯式規劃（MCTS），哪個對機器人更樣本有效？
6. **意識連結**：GWT 啟發的架構能否解釋世界模型如何產生主觀經驗？

### 9.5 世界模型專案總覽（2024-2026）

| 專案 | 組織 | 類型 | 狀態 | 關鍵創新 |
|------|------|------|------|----------|
| **Sora** | OpenAI | 影片 | 已上線 | 規模化產生湧現物理 |
| **Veo 2** | Google DeepMind | 影片 | 已上線 | 4K、電影攝影、流體 |
| **Gen-3 / GWM-1** | Runway | 影片/互動 | 已上線 | 動態控制、通用世界模型 |
| **Genie 2** | DeepMind | 互動 3D | 已上線 | 文字→互動世界 |
| **GameNGen** | Google | 遊戲引擎 | 已上線 | DOOM 神經網路模擬器 |
| **UniSim** | UC Berkeley | 互動影片 | 已上線 | 零樣本真實世界遷移 |
| **Cosmos** | NVIDIA | 平台 | 已上線 | 開源世界基礎模型平台 |
| **Marble** | World Labs | 3D 環境 | 已上線 | 可下載/編輯的 3D 世界 |
| **V-JEPA 2** | Meta | 機器人控制 | 已上線 | 零樣本機器臂控制 |
| **Optimus + Grok** | Tesla | 人形機器人 | 量產中 | 具身世界模型 |
| **RT-X** | DeepMind | 機器人學習 | 已上線 | 跨載體遷移 |
| **GR00T N1** | NVIDIA | 機器人基礎 | 已上線 | 開源人形基礎模型 |

---

## 10. 完整參考文獻

### 基礎性論文

| # | 論文 | 年份 | 連結 |
|---|------|------|------|
| 1 | Turing, "Computing Machinery and Intelligence" | 1950 | [PDF](https://courses.cs.umbc.edu/471/papers/turing.pdf) |
| 2 | Hinton et al., Deep Belief Networks | 2006 | [Paper](https://proceedings.mlr.press/v5/salakhutdinov09a/salakhutdinov09a.pdf) |
| 3 | Bahdanau et al., "Neural MT by Jointly Learning to Align and Translate" | 2014 | [arXiv:1409.0473](https://arxiv.org/abs/1409.0473) |
| 4 | Goodfellow et al., Generative Adversarial Networks | 2014 | [arXiv:1406.2661](https://arxiv.org/abs/1406.2661) |
| 5 | Vaswani et al., "Attention Is All You Need" | 2017 | [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) |
| 6 | Devlin et al., BERT | 2018 | [arXiv:1810.04805](https://arxiv.org/abs/1810.04805) |
| 7 | Ha & Schmidhuber, "World Models" | 2018 | [arXiv:1803.10122](https://arxiv.org/abs/1803.10122) |
| 8 | Karras et al., StyleGAN | 2018 | [arXiv:1812.04948](https://arxiv.org/abs/1812.04948) |
| 9 | Brown et al., GPT-3 "Language Models are Few-Shot Learners" | 2020 | [arXiv:2005.14165](https://arxiv.org/abs/2005.14165) |
| 10 | Kaplan et al., "Scaling Laws for Neural Language Models" | 2020 | [arXiv:2001.08361](https://arxiv.org/abs/2001.08361) |
| 11 | Ho et al., "Denoising Diffusion Probabilistic Models" | 2020 | [arXiv:2006.11239](https://arxiv.org/abs/2006.11239) |
| 12 | OpenAI, GPT-4 Technical Report | 2023 | [arXiv:2303.08774](https://arxiv.org/abs/2303.08774) |

### 世界模型核心文獻

| # | 論文/來源 | 年份 | 連結 |
|---|----------|------|------|
| 13 | LeCun, "A Path Towards Autonomous Machine Intelligence" | 2022 | [OpenReview](https://openreview.net/pdf?id=BZ5a1r-kVsf) |
| 14 | OpenAI, "Video generation models as world simulators" (Sora) | 2024 | [Blog](https://openai.com/index/video-generation-models-as-world-simulators/) |
| 15 | DeepMind, Genie 2 | 2024 | [Blog](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/) |
| 16 | Google, GameNGen "Diffusion Models Are Real-Time Game Engines" | 2024 | [arXiv:2408.14837](https://arxiv.org/abs/2408.14837) |
| 17 | UniSim, "Learning Interactive Real-World Simulators" | 2024 | [arXiv:2310.06114](https://arxiv.org/abs/2310.06114) |
| 18 | NVIDIA Cosmos | 2025 | [arXiv:2501.03575](https://arxiv.org/abs/2501.03575) |
| 19 | Meta, V-JEPA 2 | 2025 | [arXiv:2506.09985](https://arxiv.org/abs/2506.09985) |
| 20 | Li et al., Othello-GPT "Emergent World Representations" | 2023 | [arXiv:2210.13382](https://arxiv.org/abs/2210.13382) |
| 21 | "How Far is Video Generation from World Model" | 2024 | [arXiv:2411.02385](https://arxiv.org/abs/2411.02385) |
| 22 | Bender & Koller, "Stochastic Parrots" | 2021 | [PDF](https://s10251.pcdn.co/pdf/2021-bender-parrots.pdf) |

### GUI 操作與 Computer Use

| # | 來源 | 連結 |
|---|------|------|
| 23 | Anthropic, Claude Computer Use | [Blog](https://www.anthropic.com/news/3-5-models-and-computer-use) |
| 24 | OpenAI, Computer-Using Agent | [Blog](https://openai.com/index/computer-using-agent/) |
| 25 | OpenAI, Introducing Operator | [Blog](https://openai.com/index/introducing-operator/) |
| 26 | Google, Project Mariner | [Blog](https://deepmind.google/models/project-mariner/) |
| 27 | Microsoft, OmniParser V2 | [Blog](https://www.microsoft.com/en-us/research/articles/omniparser-v2-turning-any-llm-into-a-computer-use-agent/) |
| 28 | OSWorld Benchmark | [arXiv:2404.07972](https://arxiv.org/abs/2404.07972) |
| 29 | WebVoyager | [arXiv:2401.13919](https://arxiv.org/abs/2401.13919) |
| 30 | GUI-Actor, Coordinate-Free Visual Grounding | [arXiv](https://arxiv.org/html/2506.03143v1) |
| 31 | ShowUI (CVPR 2025) | [GitHub](https://github.com/showlab/ShowUI) |
| 32 | CogAgent (CVPR 2024) | [Paper](https://openaccess.thecvf.com/content/CVPR2024/papers/Hong_CogAgent_A_Visual_Language_Model_for_GUI_Agents_CVPR_2024_paper.pdf) |
| 33 | Ferret-UI 2 (Apple) | [Blog](https://machinelearning.apple.com/research/ferret-ui-2) |

### 模型架構

| # | 來源 | 連結 |
|---|------|------|
| 34 | Mamba SSM | [arXiv:2312.00752](https://arxiv.org/abs/2312.00752) |
| 35 | RWKV | [arXiv:2305.13048](https://arxiv.org/abs/2305.13048) |
| 36 | KAN (Kolmogorov-Arnold Networks) | [arXiv:2404.19756](https://arxiv.org/abs/2404.19756) |
| 37 | Mixtral MoE | [Substack Analysis](https://cameronrwolfe.substack.com/p/moe-llms) |
| 38 | DeepSeek-R1 | [Analysis](https://www.deeplearning.ai/the-batch/deepseek-r1-a-transparent-challenger-to-openai-o1/) |

### 其他重要來源

| # | 來源 | 連結 |
|---|------|------|
| 39 | Karl Friston, Free Energy Principle | [Nature](https://www.nature.com/articles/nrn2787) |
| 40 | World Labs (Fei-Fei Li) | [TechCrunch](https://techcrunch.com/2025/11/12/fei-fei-lis-world-labs-speeds-up-the-world-model-race-with-marble-its-first-commercial-product/) |
| 41 | Google Veo 2 | [Blog](https://blog.google/technology/google-labs/video-image-generation-update-december-2024/) |
| 42 | Runway Gen-3 Alpha | [Blog](https://runwayml.com/research/introducing-gen-3-alpha) |
| 43 | DeepMind RT-2 | [Blog](https://deepmind.google/blog/rt-2-new-model-translates-vision-and-language-into-action/) |
| 44 | NVIDIA GR00T | [News](https://nvidianews.nvidia.com/news/foundation-model-isaac-robotics-platform) |
| 45 | LLM Latency Benchmark | [AIM](https://research.aimultiple.com/llm-latency-benchmark/) |
| 46 | WebVoyager Leaderboard | [Steel](https://leaderboard.steel.dev/) |
| 47 | Dreamer v4 | [Project](https://danijar.com/project/dreamer4/) |
| 48 | Melanie Mitchell, "LLMs and World Models" | [Substack](https://aiguide.substack.com/p/llms-and-world-models-part-1) |

---

> **免責聲明**：本報告基於截至 2026 年 3 月的公開資料編撰。AI 領域發展極為迅速，部分資訊可能在發布後已有更新。所有基準測試數據引用自原始論文或官方公告，實際表現可能因評測條件而異。
>
> **信心度標註**：
> - 🟢 高信心度：來自同行評審論文或官方技術報告的數據
> - 🟡 中信心度：來自可靠技術部落格或新聞報導的資訊
> - 🔴 需謹慎：預測性內容或尚未充分驗證的研究結論
