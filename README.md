# CAET: Claims Auditing Enhancement Tool
**Author:** Dr. S. L. Toriola, MD, MSc.

**Goal:** Learn healthcare claims fraud, waste, and abuse (FWA) and compliance analytics by building statistical software in Python (pandas), matplotlib/seaborn, and Power BI.

## Start Here (plain-language guide)

- **DME** = Durable Medical Equipment: items a doctor orders for home use, such as catheters, CPAP machines, wound dressings, braces.
- **Supplier** = the business that bills Medicare for that equipment.
- **Signal** = a number that looks unusual compared with other suppliers, such as billing far above what Medicare allows.
- **Score** = signals combined into one number from 0 to 100. Higher means more worth a second look.
- **Tier** = a label for the score: LOW (under 40), MEDIUM (40), HIGH (60), CRITICAL (80).
- **Member call** = a Medicare member phoning in a complaint about a supplier, such as "I never received this item."
- **Hit** = scored HIGH or CRITICAL. It means flagged for review, not confirmed fraud.

## Project

**What it asks**
- Can billing signals and member calls help an auditor decide which suppliers to review first?
- Which suppliers should an auditor review first, based on billing patterns and member complaints?
- Do billing signals alone, or billing signals plus member calls, identify high-risk suppliers?

**H1: Hypothesis 1 of 2 (General DME, signals alone)**
- Tests all 59,592 suppliers across every equipment type.
- H1 = signals alone, at any tier (LOW, MEDIUM, HIGH, CRITICAL). The with-calls run then adds member calls.
- Target: 70% or more of tested suppliers reach HIGH or CRITICAL.

**H2: Hypothesis 2 of 2 (Intermittent urinary catheters, signals plus calls)**
- Tests the 41 catheter suppliers in OK, FL, NY, TX, GA, picked from the 206 that bill 8 or more catheter codes.
- H2 = catheter signals (bundling and units per claim) plus calls, at any tier.
- Target: 75% or more reach HIGH or CRITICAL.

**Why H2 exists**
- Catheter fraud can go undetected inside general DME scoring, because one pooled cutoff and the category weight shrink catheter scores.
- H2 uses catheter-specific cutoffs and two billing signals: bundling (many different catheter codes) and units per claim (maximum units of the same code).
- Claims show what was billed. Only member calls show what was received.
- Basis: the author's claims-adjustment experience and CMS data.

**What it provides**
- Two risk-scoring models (H1 and H2) with tiered composite scores.
- A member-call amplifier, run here on 30 simulated calls.
- Charts, a Power BI dashboard, and a methodology document.

**Results (full CMS 2023 run)**

| Test | Signals alone | Signals plus simulated calls |
|---|---|---|
| H1, 59,592 suppliers | 0 HIGH or CRITICAL (top score 27.8) | 6 suppliers reach MEDIUM, 0 reach HIGH |
| H2, 41 suppliers | 8 HIGH, 24 MEDIUM, 9 LOW (19.5% HIGH) | Of 7 catheter suppliers with calls: 5 HIGH, 2 MEDIUM |

- Calls move suppliers up a tier, which is what the amplifier is built to do.
- Simulated calls cover 10 suppliers only, so these numbers show how the tool behaves, not real fraud rates.

## Foundation

**Structure**
- `CAET_tool/` holds the scripts, run in step order.
- `visuals/`, `dashboard/`, `docs/` hold charts, the Power BI PDF, and the methodology.

**Data**
- CMS Medicare DME by Supplier and Service, 2023: 463,784 rows, 59,592 suppliers.
- CSV files are gitignored. Place `master_set_cms_medicare_dme_2023.csv` inside `CAET_tool/` before running.

**Variables measured (what Python calculates)**

| Variable | Where it comes from | What it means |
|---|---|---|
| `charge_to_allowed_ratio` | Submitted charge divided by Medicare allowed amount | Upcoding signal: how far billing exceeds what Medicare allows |
| `claims_per_bene` | Total claims divided by total beneficiaries | Volume signal: how often the same patient is billed |
| `payment_delta` | Allowed amount minus Medicare payment | Gap between what was allowed and what was paid |
| `geo_standardization_delta` | Medicare payment minus standardized amount | Regional price adjustment |
| `fraud_hcpcs_cat` | HCPCS code (the item billed) grouped into a category | Dressing, orthotic, CGM, catheter, CPAP, or other |
| `category_risk_weight` | Fixed CMS improper-payment-rate number per category | Multiplier on row scores. Dressings 0.576, orthotic 0.513, CGM 0.252, catheter 0.180, CPAP 0.125, other 0.100 |
| `rental_ratio` | Rental rows divided by all rows for a supplier | Rental abuse signal |
| `geo_score` | State and RUCA (urban or rural code) | High-risk states +30, urban +15, state outlier +20 |
| `bundling_score` | Count and mix of catheter codes per supplier | H2 signal: 14 or more codes scores highest |
| `units_score` | Services divided by claims, compared with the same HCPCS code | H2 signal: billing at the maximum units. 60 points at the code's 90th percentile, 100 at the 99th |
| `member_call_score` | Call reason and number of distinct members | Complaint amplifier, capped at 100 |
| `composite_score` | Weighted blend of the signals above | The final 0 to 100 score. H2 weights: bundling 0.25, units 0.15, calls 0.25, volume 0.15, upcoding 0.10, geo 0.10 |
| Cutoffs (90th and 99th percentile) | Calculated from the full CMS data in step 4 | A row earns 60 points above the 90th, 100 above the 99th |
| Override floor | Rule in `caet_shared.py` | Minimum H2 score (65 or 42) when bundling is extreme or high |

**Files and what each does**

| Step | File | What it does |
|---|---|---|
| 1 | `step1_load_data.py` | Loads the CMS file, adds ratios, categories, and category weights |
| 4 | `step4_thresholds.py` | Prints general and catheter percentile cutoffs |
| 5 | `step5_upcoding_scorer.py` | Scores charge-to-allowed ratio |
| 7 | `step7_geo_scorer.py` | Scores state and urban risk |
| 8 | `step8_member_call_scorer.py` | Empty member-call scorer, all zeros until calls are added |
| 9 | `step_rental_scorer.py` | Scores rental abuse |
| 9b | `step9b_composite_h1.py` | Combines signals into the H1 score and tier |
| 10 | `step10_h1_test.py` | H1 test: hit rate against the 70% target, with and without calls |
| 11 | `step11_identify_catheter_providers.py` | Finds the 206 suppliers billing 8 or more catheter codes |
| 12 | `step12_catheter_bundling_scorer.py` | Scores catheter bundling |
| 13 | `step13_catheter_composite.py` | Scores units per claim, combines H2 signals, applies the override floor |
| 15 | `step15_h2_test.py` | H2 test: hit rate against the 75% target |
| 16 | `step16_member_call_integration.py` | Applies 30 simulated calls, re-scores H1 and H2 |
| check | `validate_caet.py` | Confirms row counts and score math |
| shared | `caet_shared.py` | Shared call weights, H2 weights and cutoffs, override floor |
| aid | `select_test_candidates.py` | Picks example suppliers for each tier |
| aid | `step_check_rental_modifiers.py` | Lists rental-related columns in the data |
| charts | `visuals/viz_01` to `viz_08` | Chart scripts (tiers, score spread, call impact, top 20, state map, bundling) |

**How to run**
- Open a terminal in `CAET_tool/` and run the steps in the order shown above, ending with `validate_caet.py`.

## Featured Visuals

![H1 Tier Distribution](visuals/viz_01_python.png)

![Before vs After Member Calls](visuals/viz_03_Python.png)

![Top 20 Highest-Risk Providers](visuals/viz_04_Python.png)

![Geographic Risk Heatmap](visuals/viz_05_Python.png)

![H2 Catheter Tier Distribution](visuals/viz_07_Python.png)

## Dashboard

[View Dashboard (PDF)](dashboard/CAET_PowerBI_visual.pdf)

## Full Methodology

[View full methodology](docs/caet_data_visualization_outline_v1.0.md)
