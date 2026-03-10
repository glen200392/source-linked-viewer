#!/usr/bin/env python3
"""Batch import all local Cortex reports into SLV."""

import subprocess
import sys
from pathlib import Path

VENV_PYTHON = Path(__file__).parent.parent / ".venv" / "bin" / "python"
SCRIPTS_DIR = Path(__file__).parent
DEMO_DIR = Path(__file__).parent.parent / "demo"

# Deduplicated report list: (source_path, slug, category, tags, use_cortex_converter)
REPORTS = [
    # --- Glen Cortex Data (canonical) ---
    (
        Path.home() / "Projects/glen-cortex-data/reports/2026-03-02_ai-governance-global-landscape-research.md",
        "ai-governance-global-landscape",
        "AI 治理",
        "AI-governance,EU-AI-Act,PIPL,compliance",
        True,  # has [VERIFIED:]
    ),
    (
        Path.home() / "Projects/glen-cortex-data/reports/2026-03-02_compliance-check-report.md",
        "compliance-check-202603",
        "AI 治理",
        "compliance,self-assessment,PIPL",
        True,  # has [VERIFIED:]
    ),
    (
        Path.home() / "Projects/glen-cortex-data/reports/2026-03-02_ai-data-governance-recommendation-report.md",
        "ai-data-governance-recommendation",
        "AI 治理",
        "data-governance,AI-governance,recommendation",
        False,
    ),
    (
        Path.home() / "Projects/glen-cortex-data/reports/2026-03-02_ai-governance-compliance-roadmap.md",
        "ai-governance-compliance-roadmap",
        "AI 治理",
        "compliance,roadmap,gap-analysis",
        False,
    ),
    (
        Path.home() / "Projects/glen-cortex-data/reports/2026-03-02_data-audit-report.md",
        "data-audit-202603",
        "資料治理",
        "data-audit,data-governance,inventory",
        False,
    ),
    (
        Path.home() / "Projects/glen-cortex-data/reports/2026-03-02_data-governance-capability-report.md",
        "data-governance-capability",
        "資料治理",
        "data-governance,data-science,capability",
        False,
    ),
    (
        Path.home() / "Projects/glen-cortex-data/reports/2026-03-05_ai-individual-wiki-research.md",
        "ai-individual-wiki",
        "技術研究",
        "AI,wiki,knowledge-management,enterprise",
        False,
    ),
    # --- Data-Governance (unique to this repo) ---
    (
        Path.home() / "Projects/data-governance/reports/2026-03-08_ai-agent-architecture-research.md",
        "ai-agent-architecture",
        "技術研究",
        "AI-agent,architecture,multi-agent,framework",
        False,
    ),
    (
        Path.home() / "Projects/data-governance/reports/2026-03-08_ao-os-session-final-report.md",
        "ao-os-session-final",
        "系統部署",
        "AO-OS,deployment,macOS",
        False,
    ),
    # --- AI-Governance ---
    (
        Path.home() / "Projects/ai-governance/outputs/governance-reports/2026-03-03_governance-report.md",
        "governance-status-202603",
        "AI 治理",
        "governance,status-report,Primax",
        False,
    ),
    (
        Path.home() / "Projects/ai-governance/outputs/governance-reports/phase-c-framework-design.md",
        "phase-c-framework-design",
        "AI 治理",
        "framework,policy,governance-design",
        False,
    ),
    (
        Path.home() / "Projects/ai-governance/outputs/regulatory-updates/2026-03-03_regulatory-watch.md",
        "regulatory-watch-202603",
        "法規監控",
        "regulatory,EU-AI-Act,PIPL,global",
        False,
    ),
    # --- Desktop ---
    (
        Path.home() / "Desktop/AI影片製作工具研究報告_20260308.md",
        "ai-video-tools",
        "技術研究",
        "AI,video,tools,content-creation",
        False,
    ),
    (
        Path.home() / "Desktop/AI模型全景研究報告_20260309.md",
        "ai-model-landscape",
        "技術研究",
        "AI,LLM,model,landscape,world-model",
        False,
    ),
    (
        Path.home() / "Desktop/ai_video_generation_research_2026.md",
        "ai-video-generation-academic",
        "技術研究",
        "AI,video-generation,academic,research",
        False,
    ),
    (
        Path.home() / "Desktop/AI影片生成模型全球對照表_20260309.md",
        "ai-video-generation-comparison",
        "技術研究",
        "AI,video-generation,comparison,benchmark",
        False,
    ),
    # --- Weekly ---
    (
        Path.home() / "Projects/data-governance/weekly-reports/2026-03-04_governance-update.md",
        "governance-weekly-0304",
        "週報",
        "weekly,governance,update",
        False,
    ),
]


def main():
    imported = 0
    skipped = 0
    failed = 0

    for src, slug, category, tags, use_cortex in REPORTS:
        output = DEMO_DIR / slug
        if not src.exists():
            print(f"  SKIP (not found): {src.name}")
            skipped += 1
            continue

        if (output / "citation_map.json").exists():
            print(f"  SKIP (exists): {slug}")
            skipped += 1
            continue

        script = "cortex_to_slv.py" if use_cortex else "smart_import.py"
        cmd = [
            str(VENV_PYTHON),
            str(SCRIPTS_DIR / script),
            str(src),
            "--output", str(output),
            "--tags", tags,
            "--category", category,
        ]

        print(f"\n{'='*60}")
        print(f"  Importing: {src.name}")
        print(f"  → {slug} [{category}] via {script}")
        print(f"{'='*60}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(result.stdout[-200:] if len(result.stdout) > 200 else result.stdout)
                imported += 1
            else:
                print(f"  FAILED: {result.stderr[:200]}")
                failed += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            failed += 1

    print(f"\n{'='*60}")
    print(f"  Done: {imported} imported, {skipped} skipped, {failed} failed")
    print(f"  Total in demo/: {sum(1 for d in DEMO_DIR.iterdir() if d.is_dir() and (d / 'citation_map.json').exists())}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
