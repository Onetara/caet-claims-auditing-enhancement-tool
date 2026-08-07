# CAET — Claims Auditing Enhancement Tool

**Summary:** CAET (Claims Auditing Enhancement Tool) is a Python-based fraud risk-scoring system for DME medical claims, using signal detection and composite scoring to flag high-risk suppliers/providers.

**Question:** Can statistical fraud signals alone distinguish legitimate high-volume providers from fraud rings?

**Method:** Two hypothesis-tested models (general DME, catheter-specific), tiered scoring, member-call amplifier, CMS Medicare DME Supplier/Provider 2023 dataset.

**Results:** H1 0% baseline hit rate / H2 19.5% — both confirming the call amplifier is required, not a failure.

**Tech stack:** Python, pandas, matplotlib/seaborn, Power BI

## Featured Visuals

![H1 Tier Distribution](visuals/viz_01_h1_tier_distribution.png)

![Before vs After Member Calls](visuals/viz_03_h1_call_impact.png)

![Top 20 Highest-Risk Providers](visuals/viz_04_h1_top20_providers.png)

![Geographic Risk Heatmap](visuals/viz_05_h1_state_heatmap.png)

![H2 Catheter Tier Distribution](visuals/viz_07_h2_tier_distribution.png)

## Dashboard

[View Dashboard (PDF)](dashboard/CAET_PowerBI_visual.pdf)

## Repo Structure
/src — source code
/visuals — chart PNGs
/dashboard — Power BI PDF export
/docs — methodology and supporting docs

## Full Methodology

[View full methodology](docs/CAET_Methodology.txt)

---

**Author:** Dr. Stacy Lisa Toriola, MD, MSc.
