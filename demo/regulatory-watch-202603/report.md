# Regulatory Watch Report — Full Baseline Scan

**Pipeline**: `regulatory_watch` (gov-orchestrator → regulation-monitor)
**Date**: 2026-03-03
**Type**: Full Baseline (all jurisdictions + global)
**Scan Mode**: global_sweep
**Classification**: Internal / Confidential

---

## Executive Summary

First comprehensive regulatory watch scan covering **all 7 Primax jurisdictions + global frameworks**. Detected **22 regulatory items** across 8 categories. Key findings:

1. **CN (PIPL)**: Cross-border certification measures effective Jan 1, 2026 — directly impacts A02/A11 compliance path
2. **TW**: AI Basic Act promulgated Jan 14, 2026 — new regulatory authority (NSTC) and risk classification framework coming Q1 2026
3. **EU**: AI Act majority rules apply Aug 2, 2026 — GPAI obligations already effective Aug 2, 2025
4. **JP**: AI Promotion Act passed May 28, 2025 — APPI amendments propose AI training data exemptions
5. **TH**: PDPC released AI Guidelines draft Feb 17, 2026 — enforcement intensifying (5 new cases 2025)
6. **Global**: ISO 42001 + G7 Hiroshima Process + Council of Europe Framework Convention converging

**Primax Impact**: 8 items with direct impact, 9 indirect, 5 monitoring. 5 items rated critical/high urgency.

---

## Regulatory Items

### CN — China (6 items)

#### REG_20260303_001 | PIPL Cross-Border Certification Measures
- **Regulation**: PIPL / Certification Measures for Personal Information Cross-Border Transfer
- **Change Type**: new_enactment
- **Status**: enforced
- **Effective Date**: 2026-01-01
- **Headline**: Certification pathway for cross-border data transfer officially effective
- **Key Details**: The Certification Measures for Personal Information Cross-Border Transfer came into force Jan 1, 2026, providing a formal certification path alongside SCCs and security assessments. Organizations processing personal information of fewer than 1 million individuals may use certification as an alternative compliance mechanism for cross-border transfers.
- **Urgency**: critical
- **Primax Impact**: direct
- **Affected Sites**: CN, TW
- **Related Action Items**: A02, A11
- **Topic**: cross_border
- **Source**: IAPP / Covington | Credibility: high

#### REG_20260303_002 | GB/T 46068-2025 AI Safety Governance Standard
- **Regulation**: GB/T 46068-2025 (AI Safety Governance Framework)
- **Change Type**: new_enactment
- **Status**: enforced
- **Effective Date**: 2026-03-01
- **Headline**: National standard for AI safety governance framework effective March 2026
- **Key Details**: GB/T 46068-2025 establishes a national standard for AI safety governance. While national standards (GB/T) are technically voluntary, they often become de facto requirements through industry practice and regulatory expectation. Covers AI lifecycle risk management, technical measures, and organizational governance.
- **Urgency**: high
- **Primax Impact**: indirect
- **Affected Sites**: CN
- **Related Action Items**: A01, A08
- **Topic**: ai_risk_classification
- **Source**: SAC (Standardization Administration of China) | Credibility: high

#### REG_20260303_003 | AI Content Labeling Rules
- **Regulation**: Measures for Labeling AI-Generated Synthetic Content
- **Change Type**: enforcement_action
- **Status**: enforced
- **Effective Date**: 2025-09-01
- **Headline**: Mandatory labeling for AI-generated content in effect since September 2025
- **Key Details**: Requires service providers and users of AI-generated synthetic content (text, image, audio, video) to apply visible or implicit labels. Applies to content disseminated publicly. Non-compliance may result in warnings, fines, or service suspension.
- **Urgency**: medium
- **Primax Impact**: indirect
- **Affected Sites**: CN
- **Related Action Items**: A14
- **Topic**: transparency
- **Source**: CAC (Cyberspace Administration of China) | Credibility: high

#### REG_20260303_004 | AI Governance Framework (Sept 2025)
- **Regulation**: AI Safety Governance Framework (Ministry of Science & Technology)
- **Change Type**: guidance_issued
- **Status**: enacted
- **Effective Date**: 2025-09-01
- **Headline**: China releases comprehensive AI governance framework emphasizing safety-first approach
- **Key Details**: Framework establishes principles for AI safety governance including risk prevention, human oversight, and responsible development. Covers foundation models, generative AI, and autonomous systems. Non-binding but signals regulatory direction.
- **Urgency**: medium
- **Primax Impact**: monitoring
- **Affected Sites**: CN
- **Related Action Items**: A08
- **Topic**: general
- **Source**: MOST / TC260 | Credibility: high

#### REG_20260303_005 | Anthropomorphic AI Draft Regulations
- **Regulation**: Draft Measures on Anthropomorphic AI Management
- **Change Type**: draft_progress
- **Status**: draft
- **Headline**: China proposes restrictions on anthropomorphic AI interactions
- **Key Details**: Draft regulations released December 2025 propose restrictions on AI systems that mimic human-like behavior in interactions, including chatbots and virtual assistants. If enacted, would affect how AI chatbot pilots are designed and deployed in CN operations.
- **Urgency**: low
- **Primax Impact**: indirect
- **Affected Sites**: CN
- **Related Action Items**: A01
- **Topic**: transparency
- **Source**: CAC | Credibility: high

#### REG_20260303_006 | Cybersecurity Law Revision
- **Regulation**: Cybersecurity Law of the PRC (Revised)
- **Change Type**: amendment
- **Status**: enforced
- **Effective Date**: 2026-01-01
- **Headline**: Revised Cybersecurity Law with increased penalties effective January 2026
- **Key Details**: Revision increases maximum penalties significantly. Strengthens requirements for critical information infrastructure protection. Organizations handling personal information through AI systems face heightened obligations for cybersecurity reviews.
- **Urgency**: medium
- **Primax Impact**: indirect
- **Affected Sites**: CN
- **Related Action Items**: A02
- **Topic**: data_protection
- **Source**: NPC Standing Committee | Credibility: high

---

### TW — Taiwan (2 items)

#### REG_20260303_007 | AI Basic Act
- **Regulation**: Artificial Intelligence Basic Act (AI 基本法)
- **Change Type**: new_enactment
- **Status**: enacted
- **Effective Date**: 2026-01-14 (promulgated)
- **Headline**: Taiwan passes first AI legislation — NSTC designated as central authority
- **Key Details**: Passed by Legislative Yuan on December 23, 2025, promulgated January 14, 2026. Establishes National Science and Technology Council (NSTC) as the central AI governance authority. MODA (Ministry of Digital Affairs) tasked with developing risk classification framework targeted for Q1 2026. Framework legislation — specific enforcement measures to follow in subordinate regulations. Covers AI innovation promotion, risk management, and fundamental rights protection.
- **Urgency**: high
- **Primax Impact**: direct
- **Affected Sites**: TW
- **Related Action Items**: A04, A08
- **Topic**: ai_risk_classification
- **Source**: Legislative Yuan / Executive Yuan | Credibility: high

#### REG_20260303_008 | PDPA Amendment (PDPC Establishment)
- **Regulation**: Personal Data Protection Act (PDPA) Amendment
- **Change Type**: amendment
- **Status**: enforced
- **Effective Date**: 2025-11-11 (promulgated)
- **Headline**: Taiwan establishes independent PDPC, mandates breach notification
- **Key Details**: Promulgated November 11, 2025. Establishes the Personal Data Protection Commission (PDPC) as an independent supervisory authority. Introduces mandatory breach notification obligations (72-hour notification to PDPC, "without undue delay" to data subjects). Penalties: NT$20,000-200,000 per violation for failure to notify, with continuous penalties possible. Significantly strengthens Taiwan's data protection regime.
- **Urgency**: high
- **Primax Impact**: direct
- **Affected Sites**: TW
- **Related Action Items**: A03
- **Topic**: data_protection
- **Source**: Legislative Yuan | Credibility: high

---

### EU — European Union (3 items)

#### REG_20260303_009 | EU AI Act — Phase 2 Application
- **Regulation**: EU AI Act (Regulation 2024/1689)
- **Change Type**: deadline_approaching
- **Status**: enforced
- **Effective Date**: 2026-08-02
- **Headline**: EU AI Act majority rules (including high-risk systems) apply August 2, 2026
- **Key Details**: Phase 2 application date brings most of the EU AI Act into force: Art.6 high-risk AI system classification, Art.9 risk management, Art.11 technical documentation, Art.25 product value chain obligations, Art.43 conformity assessment. GPAI model obligations already in effect since August 2, 2025. Penalties: up to EUR 35M or 7% of global annual turnover. The European Commission is developing delegated acts for high-risk classification criteria (expected Feb 2, 2026).
- **Urgency**: critical
- **Primax Impact**: direct
- **Affected Sites**: CZ, UK (indirectly)
- **Related Action Items**: A08, A09, A10, A15
- **Topic**: ai_risk_classification
- **Source**: European Commission / EUR-Lex | Credibility: high

#### REG_20260303_010 | EU AI Act Code of Practice for GPAI
- **Regulation**: EU AI Act — General-Purpose AI Code of Practice
- **Change Type**: guidance_issued
- **Status**: enacted
- **Headline**: EU publishes Code of Practice for General-Purpose AI providers
- **Key Details**: Code of Practice developed by the AI Office provides detailed guidance for GPAI model providers on compliance with obligations under the EU AI Act. Covers transparency requirements, copyright compliance, risk assessment for systemic risk models. While Primax is not a GPAI provider, ODM products incorporating GPAI models must ensure upstream provider compliance.
- **Urgency**: medium
- **Primax Impact**: indirect
- **Affected Sites**: CZ
- **Related Action Items**: A09, A14
- **Topic**: transparency
- **Source**: EU AI Office | Credibility: high

#### REG_20260303_011 | EU Product Liability Directive Recast
- **Regulation**: Product Liability Directive (PLD) Recast (2024/2853)
- **Change Type**: deadline_approaching
- **Status**: enacted
- **Effective Date**: 2026-12-09
- **Headline**: PLD recast transposition deadline — AI/software included in "product" definition
- **Key Details**: Member states must transpose the recast PLD by December 9, 2026. Key changes: (1) AI systems and software explicitly included in "product" definition, (2) burden of proof shifts in complex AI cases (rebuttable presumption of defectiveness), (3) covers both tangible and digital products. Critical for Primax as ODM manufacturer with AI-enabled components.
- **Urgency**: high
- **Primax Impact**: direct
- **Affected Sites**: CZ
- **Related Action Items**: A20
- **Topic**: product_safety
- **Source**: European Parliament / Council | Credibility: high

---

### UK — United Kingdom (2 items)

#### REG_20260303_012 | AI Opportunities Action Plan
- **Regulation**: UK AI Opportunities Action Plan
- **Change Type**: guidance_issued
- **Status**: enacted
- **Headline**: UK publishes AI strategy progress report emphasizing pro-innovation approach
- **Key Details**: Progress report published January 2026. UK maintains sector-specific regulatory approach rather than horizontal AI legislation. Key actions: AI Safety Institute transitioning to statutory body (public consultation underway), expanded compute infrastructure investment, updated guidance from sector regulators (FCA, Ofcom, CMA). Dedicated AI legislation expected to be introduced H2 2026.
- **Urgency**: low
- **Primax Impact**: monitoring
- **Affected Sites**: UK
- **Related Action Items**: A07
- **Topic**: general
- **Source**: DSIT (Department for Science, Innovation and Technology) | Credibility: high

#### REG_20260303_013 | AI Safety Institute Statutory Transition
- **Regulation**: AI Safety Institute (AISI) Statutory Body Consultation
- **Change Type**: draft_progress
- **Status**: consultation
- **Headline**: UK AI Safety Institute to become statutory body — public consultation open
- **Key Details**: UK government consulting on establishing the AI Safety Institute as a statutory body with formal regulatory powers. Would give AISI legal authority for mandatory safety evaluations of frontier AI models. Timeline for legislation unclear but consultation signals direction of travel toward more formal UK AI regulation.
- **Urgency**: low
- **Primax Impact**: monitoring
- **Affected Sites**: UK
- **Related Action Items**: A07
- **Topic**: ai_risk_classification
- **Source**: DSIT | Credibility: high

---

### US — United States (2 items)

#### REG_20260303_014 | Colorado AI Act Delay
- **Regulation**: Colorado AI Act (SB 21-169 / SB 24-205)
- **Change Type**: amendment
- **Status**: enacted
- **Effective Date**: 2026-06-30 (delayed from 2026-02-01)
- **Headline**: Colorado delays AI Act enforcement to June 30, 2026
- **Key Details**: Colorado's AI Act, originally set to take effect February 1, 2026, has been delayed to June 30, 2026 following industry pushback. The Act requires deployers and developers of "high-risk AI systems" to use reasonable care to avoid algorithmic discrimination. While Primax has no direct Colorado operations, this is the first comprehensive state-level AI law and may influence other states.
- **Urgency**: low
- **Primax Impact**: monitoring
- **Affected Sites**: US
- **Related Action Items**: —
- **Topic**: ai_risk_classification
- **Source**: Colorado General Assembly | Credibility: high

#### REG_20260303_015 | NIST AI RMF Alignment
- **Regulation**: NIST AI Risk Management Framework (AI RMF 1.0)
- **Change Type**: guidance_issued
- **Status**: enacted
- **Headline**: NIST publishes crosswalks aligning AI RMF with ISO 42001 and OECD principles
- **Key Details**: NIST has published formal crosswalk documents mapping AI RMF to ISO/IEC 42001 and OECD AI Principles. This enables organizations to use a single governance framework mapped to multiple compliance requirements. AI RMF remains voluntary but is increasingly referenced in federal procurement requirements and industry standards. Framework covers: Govern, Map, Measure, Manage functions for AI risk.
- **Urgency**: low
- **Primax Impact**: indirect
- **Affected Sites**: US
- **Related Action Items**: A22
- **Topic**: general
- **Source**: NIST | Credibility: high

---

### JP — Japan (2 items)

#### REG_20260303_016 | AI Promotion Act
- **Regulation**: AI Promotion Act (AI 推進法)
- **Change Type**: new_enactment
- **Status**: enacted
- **Effective Date**: 2025-05-28 (passed by Diet)
- **Headline**: Japan passes AI Promotion Act positioning as "most AI-friendly country"
- **Key Details**: Passed by the Diet on May 28, 2025. Takes a lighter regulatory approach than the EU, focusing on promoting responsible AI development while avoiding excessive compliance burden. Key features: basic principles for AI use, government support for AI R&D, no specific penalty regime (relies on existing laws). Subordinate regulations and guidelines to follow. Japan government's stated goal is to be "the most AI-friendly country in the world."
- **Urgency**: medium
- **Primax Impact**: indirect
- **Affected Sites**: JP
- **Related Action Items**: A01
- **Topic**: general
- **Source**: Diet (National Legislature) / Cabinet Office | Credibility: high

#### REG_20260303_017 | APPI Amendment Proposals for AI
- **Regulation**: Act on the Protection of Personal Information (APPI) — Proposed Amendment
- **Change Type**: draft_progress
- **Status**: proposed
- **Headline**: PPC proposes APPI exemptions for AI training data — effective ~2027
- **Key Details**: On February 5, 2025, the Personal Information Protection Commission (PPC) proposed introducing exemptions to consent requirements when: (1) collecting sensitive personal data for AI model development where results cannot trace to individuals, (2) transferring personal data to third parties for statistical/AI purposes. Also proposes strengthened oversight, administrative surcharges for serious violations, and minor protection measures. Draft law expected 2025, taking effect ~2027.
- **Urgency**: low
- **Primax Impact**: indirect
- **Affected Sites**: JP
- **Related Action Items**: A01
- **Topic**: data_protection
- **Source**: PPC (Personal Information Protection Commission) | Credibility: high

---

### TH — Thailand (2 items)

#### REG_20260303_018 | PDPC AI Guidelines Draft
- **Regulation**: Guidelines on Personal Data Protection in AI Development and Use
- **Change Type**: draft_progress
- **Status**: consultation
- **Effective Date**: TBD (public consultation from 2026-02-17)
- **Headline**: Thailand PDPC releases draft AI guidelines — shaping governance through data protection lens
- **Key Details**: Released February 17, 2026 for public consultation. Rather than standalone AI legislation, Thailand is governing AI primarily through PDPA interpretation. Key provisions: DPIA requirements for high-risk AI processing, lawful basis for AI training data, transparency requirements for automated decision-making. Organizations must take full responsibility for personal data processed through AI systems. Binding AI legislation anticipated but timeline uncertain.
- **Urgency**: medium
- **Primax Impact**: direct
- **Affected Sites**: TH
- **Related Action Items**: A06
- **Topic**: data_protection
- **Source**: PDPC (Personal Data Protection Committee) | Credibility: high

#### REG_20260303_019 | PDPA Enforcement Intensification
- **Regulation**: Thailand PDPA Enforcement
- **Change Type**: enforcement_action
- **Status**: enforced
- **Headline**: Thailand PDPC intensifies enforcement — 5 new cases in 2025, Eagle Eye Crawler deployed
- **Key Details**: PDPC has significantly stepped up enforcement in 2025 with 5 additional cases following the landmark THB 7 million fine against a major online retailer in August 2024. Key enforcement tools: (1) PDPC Eagle Eye Crawler for automated surveillance, (2) inspection letters for advisory purposes, (3) stricter penalties via April 2025 Royal Decree. Signal that PDPA is moving from education phase to active enforcement.
- **Urgency**: medium
- **Primax Impact**: direct
- **Affected Sites**: TH
- **Related Action Items**: A06
- **Topic**: data_protection
- **Source**: PDPC / DLA Piper | Credibility: high

---

### GLOBAL — Cross-Jurisdictional (3 items)

#### REG_20260303_020 | ISO/IEC 42001 Adoption Momentum
- **Regulation**: ISO/IEC 42001 (AI Management System Standard)
- **Change Type**: guidance_issued
- **Status**: enacted
- **Effective Date**: 2023-12 (published, adoption accelerating 2025-2026)
- **Headline**: ISO 42001 emerging as de facto cross-border AI governance standard — NIST and EU AI Act crosswalks published
- **Key Details**: ISO/IEC 42001 is the first certifiable AI management system standard. Published December 2023, adoption is accelerating as organizations seek a common governance layer mappable to regional laws. NIST has published crosswalks from AI RMF to ISO 42001, and practitioners are mapping it to EU AI Act requirements. For multi-jurisdictional companies like Primax, ISO 42001 certification provides a baseline demonstrating AI governance maturity to regulators across all 7 operating countries.
- **Urgency**: medium
- **Primax Impact**: direct
- **Affected Sites**: All (CN, TW, CZ, UK, TH, US, JP)
- **Related Action Items**: A22
- **Topic**: general
- **Source**: ISO / NIST / ISACA | Credibility: high

#### REG_20260303_021 | G7 Hiroshima AI Process Reporting Framework
- **Regulation**: G7 Hiroshima AI Process — International Code of Conduct
- **Change Type**: guidance_issued
- **Status**: enacted
- **Headline**: G7 launches monitoring framework for AI Code of Conduct — major AI companies pledge compliance
- **Key Details**: In February 2025, OECD launched the reporting framework for monitoring the Hiroshima Process Code of Conduct. Leading AI developers (Amazon, Anthropic, Google, Microsoft, OpenAI) have pledged participation. While this targets frontier AI developers rather than deployers, it signals the direction of international AI governance norms. The Code of Conduct principles (safety testing, transparency, risk management) are increasingly referenced in national legislation drafts.
- **Urgency**: low
- **Primax Impact**: monitoring
- **Affected Sites**: All
- **Related Action Items**: A22
- **Topic**: general
- **Source**: G7 / OECD | Credibility: high

#### REG_20260303_022 | Council of Europe AI Framework Convention
- **Regulation**: Council of Europe Framework Convention on Artificial Intelligence
- **Change Type**: new_enactment
- **Status**: enacted
- **Effective Date**: 2024 (opened for signature)
- **Headline**: First legally binding international AI treaty — human rights, democracy, rule of law focus
- **Key Details**: The Council of Europe Framework Convention on AI (2024) is the first legally binding international treaty on AI. Focuses on protecting human rights, democracy, and rule of law in AI use. Open for signature by non-Council of Europe states. While not yet directly applicable to Primax, it establishes legal principles that national legislators (EU, UK) are incorporating into domestic law. May influence future CZ and UK regulatory requirements.
- **Urgency**: low
- **Primax Impact**: monitoring
- **Affected Sites**: CZ, UK
- **Related Action Items**: A07, A08
- **Topic**: general
- **Source**: Council of Europe | Credibility: high

---

## Impact Summary

### By Urgency

| Urgency | Count | Key Items |
|---------|-------|-----------|
| Critical | 2 | REG_001 (PIPL certification), REG_009 (EU AI Act Phase 2) |
| High | 4 | REG_002 (GB/T 46068), REG_007 (TW AI Act), REG_008 (TW PDPA), REG_011 (EU PLD) |
| Medium | 8 | REG_003-006, REG_010, REG_016, REG_018-020 |
| Low | 8 | REG_005, REG_012-015, REG_017, REG_021-022 |

### By Primax Impact

| Impact | Count | Jurisdictions |
|--------|-------|---------------|
| Direct | 8 | CN, TW, EU, TH, GLOBAL |
| Indirect | 9 | CN, EU, JP, US |
| Monitoring | 5 | CN, UK, US, GLOBAL |

### By Topic

| Topic | Count | Key Trend |
|-------|-------|-----------|
| Data Protection | 6 | TW PDPC established, TH enforcement intensifying, JP APPI AI exemptions |
| AI Risk Classification | 5 | EU AI Act Phase 2, CN GB/T 46068, TW risk framework Q1 2026 |
| General / Framework | 5 | JP AI Promotion Act, ISO 42001, G7, Council of Europe |
| Transparency | 3 | CN labeling rules, EU GPAI Code of Practice |
| Cross-Border | 1 | CN PIPL certification pathway (critical for Primax) |
| Product Safety | 1 | EU PLD recast (critical for ODM) |
| AI Liability | 1 | EU PLD burden of proof shift |

---

## Action Item Impact Assessment

| Action Item | Affected By | Priority Change Needed? |
|-------------|-------------|------------------------|
| **A02** (PIPL CN→TW) | REG_001: New certification pathway available | No — but certification option should be evaluated alongside SCC |
| **A03** (TW PDPC SOP) | REG_008: PDPC now established, enforcement imminent | No — confirms urgency |
| **A04** (EU AI Act literacy) | REG_009: Phase 2 approaching | No — confirms timeline |
| **A06** (TH PDPA) | REG_018, REG_019: AI guidelines draft + enforcement up | Consider upgrading to P0 if PDPC AI guidelines enacted before Q2 |
| **A08** (EU AI Act classification) | REG_009: Phase 2 date confirmed Aug 2, 2026 | No — confirms timeline |
| **A09** (ODM AI liability) | REG_011: PLD recast confirms AI in "product" | No — reinforces priority |
| **A22** (ISO 42001) | REG_020: Adoption accelerating, crosswalks available | Consider starting earlier as cross-border governance baseline |
| **NEW** | REG_007: TW AI Basic Act → risk classification coming Q1 2026 | **Recommend creating A29**: Monitor TW AI risk classification framework development |
| **NEW** | REG_002: GB/T 46068-2025 effective Mar 1 | **Recommend creating A30**: Assess CN AI safety governance standard applicability |

---

## Recommended Actions

### Immediate (This Week)
1. **Evaluate PIPL certification pathway** (REG_001) — New compliance option for A02. Legal should assess whether certification is faster/cheaper than SCC for Primax's data volume.
2. **Note TW AI Basic Act risk framework timeline** (REG_007) — MODA's risk classification framework expected Q1 2026. When published, will need gap assessment against Primax TW operations.

### Short-term (March 2026)
3. **Monitor TH PDPC AI Guidelines consultation** (REG_018) — Submit comments if material impact on TH operations. Final guidelines could trigger A06 scope expansion.
4. **Consider ISO 42001 gap assessment** (REG_020) — As a cross-border governance baseline, ISO 42001 certification would demonstrate AI governance maturity to regulators in all 7 jurisdictions.

### Medium-term (Q2 2026)
5. **Prepare for EU AI Act Phase 2** (REG_009) — High-risk classification guidelines expected. A08/A09 completion critical before Aug 2, 2026.
6. **Watch JP APPI amendment** (REG_017) — AI training data exemptions could simplify JP data processing, but also raise scrutiny of AI systems using personal data.

---

## Next Scan

Scheduled: 2026-03-10 (weekly, following rotation: Week 2 = EU + CZ focus)
Baseline complete — future scans will track delta changes from this report.

---

## English Summary

First comprehensive regulatory watch covering all 7 Primax jurisdictions plus global frameworks. 22 regulatory items detected. Critical items: PIPL cross-border certification measures (effective Jan 1, 2026) providing new compliance path for A02, and EU AI Act Phase 2 majority rules (Aug 2, 2026). Notable developments: Taiwan's AI Basic Act (Jan 14, 2026) establishes NSTC as central authority with risk classification framework coming Q1 2026; Thailand PDPC released draft AI guidelines (Feb 17, 2026); Japan passed AI Promotion Act (May 2025) with pro-innovation stance; ISO 42001 gaining momentum as cross-border AI governance standard. Recommend evaluating PIPL certification path for A02, monitoring TW risk framework, and considering early ISO 42001 gap assessment as multi-jurisdiction baseline.

---

*Generated by gov-orchestrator → regulation-monitor pipeline | AO OS v2.0 | AI Governance Domain*
