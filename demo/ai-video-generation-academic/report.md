# Academic & Research Lab Video Generation Models — March 2026

## Executive Summary

As of March 2026, video generation has seen explosive growth from academic and research institutions, with major models now matching or exceeding commercial offerings. Key breakthroughs include: (1) Efficient architectures enabling generation on 6-8GB VRAM, (2) Flow-matching approaches reducing generation steps dramatically, (3) Interactive world models (Genie 3) moving beyond video synthesis to navigable environments, and (4) Tsinghua's TurboDiffusion achieving 100-200x speedup through intelligent quantization and distillation.

---

## 1. University & Research Lab Models

### 1.1 Tsinghua University (China)

**Project: TurboDiffusion (Dec 2025)**
- **Institution:** Tsinghua University TSAIL Lab + ShengShu Technology
- **Status:** Open-sourced December 23, 2025
- **Paper:** [Press Release](https://www.prnewswire.com/news-releases/shengshu-technology-and-tsinghua-university-unveil-turbodiffusion-ushering-in-the-era-of-real-time-ai-video-generation-302648640.html)
- **GitHub:** Expected availability post-announcement
- **Key Innovation:** Acceleration framework using:
  - **rCM Distillation:** Reduces model to 3-4 generation steps (vs. typical 50+)
  - **W8A8 Quantization:** 8-bit weights and activations in linear layers
  - **Token-Aware Optimization:** Preserves quality near-losslessly
- **Performance:**
  - 1.3B-param 480p model: 184s → 1.9s (97× speedup)
  - 1080p 8-second video: 900s → 8s (112× speedup)
  - 5-second 1080p HD: 80 minutes → 24 seconds (200× speedup)
- **Hardware:** Works on single RTX 5090 GPU; aims for consumer-grade accessibility
- **Significance:** Described as "DeepSeek moment for video" — makes real-time generation practical

---

### 1.2 UC Berkeley (USA)

**Project: DiT-Serve (2025)**
- **Status:** Tech report EECS-2025-46
- **Paper:** [DiT-Serve and DeepCoder](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-46.pdf)
- **Focus:** Scalable serving of video and code generation Diffusion Transformers
- **Contribution:** Inference optimization for DiT-based models at scale

---

### 1.3 Vision Institute / Vchitect (Academic Partnership)

**Project: Latte — Latent Diffusion Transformer for Video (TMLR 2025)**
- **Status:** Published TMLR 2025, widely adopted
- **GitHub:** [Vchitect/Latte](https://github.com/Vchitect/Latte)
- **Alternative Repo:** [maxin-cn/Latte](https://github.com/maxin-cn/Latte)
- **Hugging Face Integration:** Integrated into diffusers library (July 2024)
- **Architecture:** Vision Transformer blocks in latent space for efficient video modeling
- **Key Features:**
  - Spatio-temporal tokenization of input videos
  - Supports class-conditional and text-to-video generation
  - 4/8-bit quantization reduces VRAM from 17GB → 9GB
- **Performance:**
  - SOTA on FaceForensics, SkyTimelapse, UCF101, Taichi-HD
  - Extends to controllable generation tasks
- **Hardware:** Can run on 8-9GB VRAM with quantization
- **Licensing:** Open-source implementation available

---

### 1.4 BAAI (Beijing Academy of AI)

**Project: NOVA — Autoregressive Video Generation without Vector Quantization (ICLR 2025)**
- **Status:** Published ICLR 2025
- **GitHub:** [baaivision/NOVA](https://github.com/baaivision/NOVA)
- **Paper:** [ICLR 2025 PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/6e5112eaa45f8c30b242c5f576213a92-Paper-Conference.pdf)
- **Innovation:** First large-scale autoregressive model without VQ tokenization
- **Approach:** Frame-by-frame prediction + spatial set-by-set prediction
- **Performance:**
  - VBench: 80.1 (matches diffusion models of similar scale)
  - Speed: 2.75 FPS
  - Training: 342 GPU days on A100-40G
- **Successor:** URSA model released October 2025
- **Advantages:** Data efficiency, faster inference than token-AR baselines

---

## 2. Major Tech Company Research Labs

### 2.1 Google DeepMind

#### A. Genie 3 — Interactive World Model (Aug 2025, Consumer Release Jan 2026)

**Project:** Genie 3: A New Frontier for World Models
- **Status:** Research announced Aug 5, 2025; Project Genie consumer launch Jan 29, 2026
- **Access:** Google Labs (AI Ultra subscribers in U.S.)
- **Blog Post:** [Genie 3 — Google DeepMind](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
- **Key Differentiator:** NOT just video generation — generates **interactive 3D worlds**
- **Capabilities:**
  - Text-to-world generation
  - Real-time navigation at 24 FPS
  - 720p resolution
  - 3-minute consistency with 1-minute visual memory
  - User input handling with instant response
  - Spatiotemporal video tokenizers + dynamics models
- **Technical Approach:** Multi-frame reasoning instead of per-frame generation
- **Significance:** Represents paradigm shift from video → world models

#### B. Veo 3 — Video Generation with Audio

**Project:** Veo 3
- **Status:** Active research model
- **Features:**
  - Native audio generation + synchronization
  - Extended video length support
  - Real-world physics modeling
  - Improved prompt adherence
  - Expanded creative controls

### 2.2 Tencent

**Project: HunyuanVideo Series**

#### HunyuanVideo (Base Model) — Released Dec 3, 2024

- **GitHub:** [Tencent-Hunyuan/HunyuanVideo](https://github.com/Tencent-Hunyuan/HunyuanVideo)
- **Paper:** [hunyuanvideo.pdf](https://github.com/Tencent/HunyuanVideo/blob/main/assets/hunyuanvideo.pdf)
- **Status:** Fully open-sourced with weights
- **Model Size:** 13 billion parameters (largest open-source at time of release)
- **Architecture:** Diffusion Transformer + Joint image-video training
- **Performance:**
  - Comparable/superior to leading closed-source models
  - VBench: Beats Runway Gen-3
  - Quality: Beats Sora on some metrics
- **Hardware:** Consumer-grade GPU compatible
- **Code Quality:** Full inference code + training infrastructure

#### HunyuanVideo-I2V — Released Mar 6, 2025

- **GitHub:** [Tencent-Hunyuan/HunyuanVideo-I2V](https://github.com/Tencent-Hunyuan/HunyuanVideo-I2V)
- **Focus:** Image-to-video generation
- **Features:** Customizable character + scene generation

#### HunyuanVideo-1.5 — Released Nov 2025

- **GitHub:** [Tencent-Hunyuan/HunyuanVideo-1.5](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5)
- **Model Size:** 8.3 billion parameters (lightweight)
- **Key Achievement:** SOTA visual quality + motion coherence on consumer GPUs
- **Hardware:** Efficient inference on standard consumer hardware
- **Trade-off:** Smaller = faster, minimal quality loss vs. 13B version

#### HunyuanVideo-Foley — Released 2025

- **GitHub:** [Tencent-Hunyuan/HunyuanVideo-Foley](https://github.com/Tencent-Hunyuan/HunyuanVideo-Foley)
- **Focus:** Multimodal audio generation for video (Foley + speech)
- **Architecture:** Multimodal diffusion with representation alignment

### 2.3 Meta FAIR (2025)

**Project: Flow Matching for Video**
- **Status:** Research direction, foundational work
- **Paradigm:** Flow Matching as state-of-the-art for video, audio, 3D, music
- **Release:** Vibes (Expressive AI Video) — Sept 2025
- **Features:**
  - User self-insertion into generated videos
  - Multi-modal conditioning (text + reference)
  - Friend appearance generation
- **Supporting Work:**
  - PLM-VideoBench: New dataset + benchmark for fine-grained video understanding
  - Meta Video Seal: Open-source watermarking for video safety
  - 2.5M video QA + spatio-temporal caption samples

**Project: Meta Movie Gen (Archive)**
- **Context:** Former tech lead Ishan Misra led research on:
  - Video generation
  - Video editing
  - Video personalization
  - Audio generation (unified foundation models)

---

### 2.4 Alibaba

**Project: Wan Series (Open-Source)**

#### Wan (Base) — Released March 26, 2025

- **Paper:** [Wan: Open and Advanced Large-Scale Video Generative Models](https://arxiv.org/abs/2503.20314)
- **Model Size:** 14 billion parameters
- **Architecture:** Diffusion Transformer with novel VAE
- **Performance:**
  - VBench scores exceed HunyuanVideo
  - Outperforms commercial models (Runway, Pika) on benchmarks
  - Trained on billions of images + videos
- **GitHub:** Expected open-source release
- **Website:** [wanai.pro](https://wanai.pro/)

#### Wan2.1 — Released Feb 2025

- **Status:** Fully open-sourced
- **Focus:** Optimized text-to-video generation
- **Performance:** Consistently outperforms existing open-source models
- **Hardware:** Consumer GPU compatible

#### Wan2.2-S2V (Speech-to-Video) — Released 2025

- **Focus:** Digital human video generation
- **Features:**
  - Portrait photo → film-quality avatar
  - Speaks, sings, performs
  - Open-source with weights

#### Wan2.5 — Released Mid-2025

- **Improvements:** Enhanced motion coherence, prompt adherence

#### Wan2.6-R2V (Reference-to-Video) — Released Dec 2025

- **Innovation:** Character reference + voice preservation
- **Features:**
  - Upload character video (appearance + voice)
  - Multi-shot storytelling capability
  - Text-prompt control
  - Open-source release

---

### 2.5 Microsoft Research

**Project: ARLON Framework (Feb 2025)**

- **Institution:** Microsoft Research Asia
- **Focus:** Long-form video generation (>30 seconds)
- **Architecture:**
  - Autoregressive (AR) + Diffusion Transformer (DiT) hybrid
  - Adaptive semantic injection module
  - Uncertainty sampling strategy
- **Performance:**
  - High robustness to noise
  - Natural motion
  - Dynamic consistency
  - Complex/repetitive scene handling
- **Applications:** Integration into Microsoft 365 Copilot Create (Dec 2025)

**Integration: Microsoft 365 Copilot Create (Dec 2025)**

- **AI Models:** OpenAI Sora 2 + Sora variants
- **Status:** Enterprise deployment
- **Use Case:** Built-in video generation for Office ecosystem

---

### 2.6 Lightricks

**Project: LTX Video Series**

#### LTX-Video (Initial Release)

- **GitHub:** [Lightricks/LTX-Video](https://github.com/Lightricks/LTX-Video)
- **Hugging Face:** [Lightricks/LTX-Video](https://huggingface.co/Lightricks/LTX-Video)
- **Architecture:** First DiT-based image-to-video model (real-time)
- **Performance:**
  - 30 FPS at 1216×704 resolution
  - Faster than real-time playback
  - Production-quality output
- **Features:**
  - Multi-keyframe conditioning
  - Video extension (forward + backward)
  - Video-to-video transformation
  - Keyframe-based animation

#### LTX-2 (Audio-Video Foundation Model) — 2025

- **GitHub:** [Lightricks/LTX-2](https://github.com/Lightricks/LTX-2)
- **Hugging Face:** [Lightricks/LTX-2](https://huggingface.co/Lightricks/LTX-2)
- **Architecture:** DiT-based audio-video foundation model
- **Features:**
  - Synchronized audio + video generation
  - Single-pass generation
  - Up to 50 FPS at 4K resolution
  - Text + image-to-video support

#### LTX-2.3 (Latest Release)

- **New VAE:** Improved fine-detail sharpness
- **Native Audio:** Built-in audio generation
- **Clip Length:** Up to 20 seconds at 4K
- **Availability:** Open-source on fal.ai, Hugging Face

---

### 2.7 Genmo

**Project: Mochi 1 (Oct 2024)**

- **GitHub:** [genmoai/mochi](https://github.com/genmoai/mochi)
- **Hugging Face:** [genmo/mochi-1-preview](https://huggingface.co/genmo)
- **Model Size:** 10 billion parameters
- **Architecture:** Asymmetric Diffusion Transformer (AsymmDiT)
  - 8× spatial compression (128x total)
  - 6× temporal compression
  - 12-channel latent space
- **VAE Innovation:** Open-sourced AsymmVAE for video compression
- **Licensing:** Apache 2.0 (fully permissive)
- **Performance:** SOTA open-source quality
- **Distribution:** Hugging Face + magnet links
- **API:** Simple, composable Python API

---

### 2.8 Zhipu (Alibaba Cloud Partnership)

**Project: CogVideoX Series (2024-2025)**

#### CogVideoX-2B

- **Status:** Open-sourced Aug 2024 (first in series)
- **GitHub:** [zai-org/CogVideo](https://github.com/zai-org/CogVideo)
- **Model Size:** 2 billion parameters
- **License:** CogVideoX License (non-commercial) + Apache 2.0 code

#### CogVideoX-5B

- **Status:** Open-sourced Aug 2024
- **Hugging Face:** [zai-org/CogVideoX-5b](https://huggingface.co/zai-org/CogVideoX-5b)
- **Model Size:** 5 billion parameters
- **Features:**
  - 3D Causal VAE weights available
  - Video caption model included
  - INT8 quantization support (via TorchAO)
  - BF16/FP16/FP32 variants

#### CogVideoX1.5-5B (Upgraded Version)

- **Hugging Face:** [zai-org/CogVideoX1.5-5B-SAT](https://huggingface.co/zai-org/CogVideoX1.5-5B-SAT)
- **Features:**
  - 10-second video capability
  - Higher resolution support
  - Improved motion coherence

#### CogVideoX1.5-5B-I2V (Image-to-Video)

- **Capability:** Generate at any resolution
- **Use Case:** Controlled animation from reference images

**Note:** CogVideoX weights non-commercial due to license; code open under Apache 2.0

---

## 3. Emerging Techniques & Breakthrough Approaches

### 3.1 Flow Matching & Rectified Flow

**Rectified Flow Paradigm (2025)**

- **Foundation:** Intuitive, unified framework for diffusion + flow-based generation
- **State-of-Art Paradigm:** Increasingly standard for image, video, audio, 3D, music
- **Advantage:** Simpler, more efficient than traditional diffusion
- **References:**
  - [Rectified Flow](https://rectifiedflow.github.io/)
  - Apple ML Research: [Variational Rectified Flow](https://machinelearning.apple.com/research/variational)

**Key 2025 Papers:**

1. **Flowception (Dec 2025)** — Variable-length video generation
   - Non-autoregressive framework
   - Interleaves frame insertion + denoising
   - 3× fewer FLOPs vs. full-sequence flows
   - Paper: [Flowception](https://arxiv.org/abs/2512.11438)

2. **Pyramidal Flow Matching (Jan 2025)**
   - Pyramid-structured stages (only final at full resolution)
   - Efficient 5-10 second 768p video @ 24 FPS
   - Training: 20.7k A100 hours
   - Forum: [Pyramidal Flow Matching](https://openreview.net/forum?id=66NzcRQuOq)

3. **Frieren — Video-to-Audio Flow Matching**
   - Hierarchical architecture with channel-level cross-modal fusion
   - Rectified flow for audio-video alignment
   - Paper: [arXiv:2406.00320](https://arxiv.org/abs/2406.00320)

4. **Straightness Is Not Your Need (ICLR 2025)**
   - Challenges assumption of straight rectified flow paths
   - Explores curved flows for better efficiency
   - Paper: [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/4df9a5e6bad9e64ebcea453e031142bb-Paper-Conference.pdf)

---

### 3.2 Autoregressive Video Generation

**Field Trends (2025):**
- Clear convergence on two directions: unified multimodal models + autoregressive diffusion-forcing
- Much faster than traditional diffusion during inference

**Key Models:**

1. **VideoAR (2025)** — Visual Autoregressive Framework
   - Multi-scale next-frame prediction
   - Autoregressive modeling
   - Performance: gFVD 88.6, VBench 81.7
   - Inference: 13× faster than AR baselines
   - Paper: [arXiv:2601.05966](https://arxiv.org/html/2601.05966v1)

2. **FAR (Frame AutoRegressive)**
   - Temporal causal dependencies between continuous frames
   - Better convergence than Token AR
   - SOTA short + long video generation
   - Paper: [causvid.github.io](https://causvid.github.io/)

3. **PA-VDM (Progressive Autoregressive Video Diffusion)**
   - Long videos via autoregressive clean-frame generation
   - Small interval generation
   - Paper: [CVPR 2025 Workshop](https://openaccess.thecvf.com/content/CVPR2025W/CVEU/papers/Xie_Progressive_Autoregressive_Video_Diffusion_Models_CVPRW_2025_paper.pdf)

4. **MAGI-1**
   - Autoregressive video generation at scale
   - Paper: [MAGI_1.pdf](https://static.magi.world/static/files/MAGI_1.pdf)

---

### 3.3 Quantization & Distillation

**Q-VDiT Framework (2025)**

- **Problem:** Quantization errors in video DiT models
- **Solution:** 
  - Token-aware Quantization Estimator (TQE)
  - Temporal Maintenance Distillation (TMD)
- **Result:** W3A6 Q-VDiT achieves 23.40 scene consistency (1.9× better than SOTA)
- **Paper:** [ICML 2025 Poster](https://icml.cc/virtual/2025/poster/45429)
- **Full Paper:** [arXiv:2505.22167](https://arxiv.org/html/2505.22167)

**ViDiT-Q (2025)**

- **Innovation:** Static-dynamic channel balancing
- **Metric-decoupled mixed precision:** Preserves multiple quality aspects
- **Paper:** [ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/a4a1ee071ce0fe63b83bce507c9dc4d7-Paper-Conference.pdf)

**NeoDragon — Mobile Video Generation (2025)**

- **Architecture:** Diffusion Transformer for mobile
- **Techniques:** Step distillation adapted from flow-matching
- **Target:** Efficient mobile device generation
- **Paper:** [arXiv:2511.06055](https://arxiv.org/html/2511.06055v1)

---

### 3.4 Other Notable Innovations

**MagicMirror (ICCV 2025)**
- ID-preserved video generation in DiTs
- Maintains character/identity across generated frames
- Paper: [OpenAccess ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_MagicMirror_ID-Preserved_Video_Generation_in_Video_Diffusion_Transformers_ICCV_2025_paper.pdf)

**Video Motion Transfer (CVPR 2025)**
- Diffusion Transformer-based motion transfer
- Paper: [Pondaven et al. CVPR 2025](https://openaccess.thecvf.com/content/CVPR2025/papers/Pondaven_Video_Motion_Transfer_with_Diffusion_Transformers_CVPR_2025_paper.pdf)
- Website: [ditflow.github.io](https://ditflow.github.io/)

**DLFR-Gen (ICCV 2025)**
- Dynamic Latent Frame Rate for adaptive efficiency
- Paper: [Yuan et al. ICCV 2025](https://openaccess.thecvf.com/content/ICCV2025/papers/Yuan_DLFR-Gen_Diffusion-based_Video_Generation_with_Dynamic_Latent_Frame_Rate_ICCV_2025_paper.pdf)

**DyDiT++ (2025)**
- Dynamic Diffusion Transformers for efficient generation
- Paper: [arXiv:2504.06803](https://arxiv.org/abs/2504.06803)

**FlowChef (ICCV 2025)**
- Steering Rectified Flow for controlled image/video generation
- GitHub: [FlowChef/flowchef](https://github.com/FlowChef/flowchef)

---

## 4. Low-VRAM & Mobile Models (6-8GB VRAM)

### 4.1 Wan2GP (2025)

- **Project:** GPU-Poor friendly optimization
- **GitHub:** [deepbeepmeep/Wan2GP](https://github.com/deepbeepmeep/Wan2GP)
- **Supported Models:**
  - Wan 2.1 / 2.2
  - Qwen Image
  - HunyuanVideo
  - LTX Video
  - Flux
- **Hardware Performance:**
  - 6GB VRAM: 5-second 480p video
  - 8GB VRAM: 8-second 480p OR 15-second 480p clips
  - Technique: Smart memory management (load/unload between VRAM + RAM)
- **Hardware Savings:** 2× VRAM reduction without weight precision loss
- **Reference:** [BrightCoding Article](https://www.blog.brightcoding.dev/2025/09/17/open-source-video-generation-for-low-vram-gpus-how-wan2gp-puts-cinematic-ai-in-reach-of-the-gpu-poor/)

### 4.2 FramePack (2025)

- **Innovation:** Constant 6GB VRAM regardless of video length
- **Performance:**
  - 6GB VRAM: 1-minute video possible (vs. length-limited others)
  - Trade-off: Slower processing
- **Reference:** [Stable Diffusion Art](https://stable-diffusion-art.com/framepack/)

### 4.3 LTX-2 on 8GB VRAM (2025)

- **Optimization Guide:** [LTX-2 8GB Guide](https://apatero.com/blog/ltx-2-8gb-vram-optimization-complete-guide-2025)
- **Techniques:**
  - FP8 quantization (40% VRAM savings)
  - Aggressive tile processing
  - Low-VRAM mode enabled
  - Resolution: 480p max
- **Output:** 3-5 second clips at 480p
- **Speed:** 2-3× slower but good quality

### 4.4 Stable Video Diffusion (2025)

- **Hardware:** ~6GB VRAM basic generation
- **Status:** Widely available

### 4.5 Wan2.2 on 8GB VRAM

- **Capability:** 480P basic generation
- **Performance:** Good quality at lower resolution

---

## 5. Comparative Model Analysis

| Model | Institution | Params | Open Source | VRAM Req | Best Use | Release |
|-------|-------------|--------|------------|----------|----------|---------|
| TurboDiffusion | Tsinghua + ShengShu | 1.3B | Yes | Optimized | Real-time inference | Dec 2025 |
| HunyuanVideo-1.5 | Tencent | 8.3B | Yes | Medium | Fast, high-quality | Nov 2025 |
| HunyuanVideo | Tencent | 13B | Yes | High | Best quality (open) | Dec 2024 |
| Wan2.6 | Alibaba | 14B | Yes | High | Character-centric | Dec 2025 |
| LTX-2.3 | Lightricks | ~8B | Yes | Medium | Audio-video sync | 2025 |
| Mochi 1 | Genmo | 10B | Yes (Apache 2.0) | High | Clean, flexible API | Oct 2024 |
| CogVideoX-5B | Zhipu | 5B | Yes (Non-comm) | Medium | Lightweight | Aug 2024 |
| Latte | Vchitect | Variable | Yes | Low (8GB) | Research, quantization | TMLR 2025 |
| NOVA | BAAI | Variable | Yes | Medium | Efficient AR generation | ICLR 2025 |
| Genie 3 | Google DeepMind | - | No (API only) | - | Interactive worlds | Jan 2026 |

---

## 6. Hardware Requirements by Use Case

### Production Quality (Full Res, >5 sec)
- **Budget:** RTX 4090 (24GB) or A100 (80GB)
- **Models:** HunyuanVideo, Wan 2.1+, LTX-2, Mochi 1
- **Speed:** 5-30 minutes per 5-second video

### Consumer/Creator Use (480p, 5 sec)
- **Budget:** RTX 4070 Ti (12GB) minimum
- **Models:** HunyuanVideo-1.5, LTX-2 (optimized), Wan2GP
- **Speed:** 30 seconds to 2 minutes via Wan2GP

### Low-Resource / Mobile (480p, <5 sec)
- **Budget:** RTX 3060 (12GB) or gaming GPU (6-8GB)
- **Models:** Latte (8GB), Wan2GP (6GB), FramePack (6GB)
- **Speed:** 2-10 minutes on consumer hardware

### Mobile Inference (Research)
- **Target:** 8GB+ phones (future)
- **Models:** NeoDragon, various mobile quantized variants
- **Status:** Actively researched, not yet production-ready

---

## 7. Licensing & Availability Summary

| Model | License | Weights | Code | Commercial |
|-------|---------|---------|------|-----------|
| TurboDiffusion | TBD | Expected | Expected | Depends |
| HunyuanVideo | Permissive | Yes | Yes | Yes |
| Wan 2.1+ | Open | Yes | Yes | Yes |
| LTX-2.3 | Permissive | Yes | Yes | Yes |
| Mochi 1 | Apache 2.0 | Yes | Yes | Yes |
| CogVideoX | Mixed (non-comm weights) | Restricted | Apache 2.0 | No |
| Latte | MIT-like | Yes | Yes | Yes |
| NOVA | Research | Expected | Yes | TBD |
| Genie 3 | Proprietary | No (API) | No | No (API only) |

---

## 8. Key Takeaways for Implementation

### For High-Quality Production
- **Best Open Models:** HunyuanVideo (13B) or Wan 2.6 (14B)
- **Trade-off:** Requires high-end GPU
- **Differentiation:** Character preservation, audio sync, motion quality

### For Real-Time/Interactive
- **Best Approach:** TurboDiffusion framework applied to any base model
- **Speedup:** 100-200× possible with quantization + distillation
- **Trade-off:** Minimal quality loss with careful implementation

### For Consumer Accessibility
- **Solution:** Wan2GP or FramePack on 6-8GB VRAM
- **Limitation:** 480p, short clips, slower
- **Trend:** Rapidly improving (Tsinghua breakthrough)

### For Research & Experimentation
- **Best Framework:** Latte (easy quantization, integration into diffusers)
- **Best for AR:** NOVA (ICLR 2025)
- **Best for Flow:** Flowception (variable-length, efficient)

### For Interactive Worlds
- **Only Option:** Genie 3 (API access, no self-hosting)
- **Paradigm Shift:** Moves beyond video to navigable environments

---

## 9. Research Gaps & Opportunities (March 2026)

1. **Efficient Mobile Generation:** NeoDragon et al. show promise, but <1 minute latency on phone GPU not yet achieved
2. **Multimodal Control:** Conditional generation beyond text (pose, depth, explicit objects) still limited
3. **Long-Form Coherence:** Beyond 30 seconds, temporal consistency degrades (Genie 3 solves via world models)
4. **Audio-Video Sync:** LTX-2.3, Wan2.2-S2V make progress, but lip-sync precision varies
5. **Variable Aspect Ratio:** Most models fixed to 16:9; flexible resolution still challenging
6. **Fine-Grained Motion:** Sub-second motion (e.g., hand gesture precision) lags human quality

---

## 10. Sources & References

**Key Institutional Repositories:**
- Tencent: [github.com/Tencent-Hunyuan](https://github.com/Tencent-Hunyuan)
- Alibaba: [wanai.pro](https://wanai.pro/)
- Vchitect: [github.com/Vchitect/Latte](https://github.com/Vchitect/Latte)
- BAAI: [github.com/baaivision/NOVA](https://github.com/baaivision/NOVA)
- Genmo: [github.com/genmoai/mochi](https://github.com/genmoai/mochi)
- Lightricks: [github.com/Lightricks/LTX-2](https://github.com/Lightricks/LTX-2)

**Major Research Papers (2025-2026):**
- [Controllable Video Generation Survey](https://arxiv.org/html/2507.16869v2)
- [Wan: Open Video Models](https://arxiv.org/abs/2503.20314)
- [NOVA: Autoregressive without VQ](https://arxiv.org/abs/2412.14169)
- [Flowception](https://arxiv.org/abs/2512.11438)
- [Q-VDiT Quantization](https://arxiv.org/html/2505.22167)

**Industry News:**
- [Adobe CVPR 2025](https://research.adobe.com/news/generative-video-propagation-cvpr-2025/)
- [Tsinghua TurboDiffusion Press Release](https://www.prnewswire.com/news-releases/shengshu-technology-and-tsinghua-university-unveil-turbodiffusion-ushering-in-the-era-of-real-time-ai-video-generation-302648640.html)
- [SiliconFlow Model Hub](https://www.siliconflow.com/articles/en/best-open-source-video-generation-models-2025)

---

**Report Generated:** March 2026
**Data Cutoff:** March 9, 2026
**Scope:** Academic + major research lab models only (excludes pure commercial-only offerings)

