# step13_catheter_composite.py
# Applies catheter-specific weights to produce final composite score
# Requires: dme_with_signals.csv, catheter_bundling_scores.csv

import pandas as pd
from pathlib import Path
from caet_shared import (
    CATH_CHARGE_MAX_CUTOFF, CATH_CHARGE_MEAN_CUTOFF,
    CATH_CPB_MAX_CUTOFF, CATH_CPB_MEAN_CUTOFF, CATH_TOTAL_CLAIMS_CUTOFF,
    h2_composite, tier, UNITS_MIN_ROWS,
)
BASE_DIR = Path(__file__).resolve().parent

# ── LOAD ────────────────────────────────────────────────────────────
df             = pd.read_csv(str(BASE_DIR / "dme_with_signals.csv"))
bundling_df    = pd.read_csv(str(BASE_DIR / "catheter_bundling_scores.csv"))
candidate_npis = bundling_df["npi"].unique()

HIGH_RISK_CATHETER_STATES = ["OK", "FL", "NY", "TX", "GA"]

# ── UNITS CUTOFFS (per HCPCS code) ───────────────────────────────────
# Units per claim differ a lot by code (about 150 for A4351, about 5 for A4333),
# so each row is compared only with rows of the same code.
cath = df[df["fraud_hcpcs_cat"] == "CATHETER"].copy()
cath["units_per_claim"] = cath["Tot_Suplr_Srvcs"] / cath["Tot_Suplr_Clms"]
code_stats = cath.groupby("HCPCS_Cd")["units_per_claim"].agg(
    rows="count", p90=lambda x: x.quantile(0.90), p99=lambda x: x.quantile(0.99))
code_stats = code_stats[code_stats["rows"] >= UNITS_MIN_ROWS]
cath = cath.merge(code_stats[["p90", "p99"]], left_on="HCPCS_Cd", right_index=True)
cath["units_points"] = 0.0
cath.loc[cath["units_per_claim"] >= cath["p90"], "units_points"] = 60.0
cath.loc[cath["units_per_claim"] >= cath["p99"], "units_points"] = 100.0
units_by_npi = cath.groupby("Suplr_NPI")["units_points"].max()

# ── SUPPORTING SCORERS ───────────────────────────────────────────────
def units_score(npi):
    return float(units_by_npi.get(npi, 0.0))


def volume_score(provider_rows):
    cpb = provider_rows["claims_per_bene"].dropna()
    if cpb.empty:
        return 0.0
    score = 0.0
    if cpb.max()  > CATH_CPB_MAX_CUTOFF: score += 40
    if cpb.mean() > CATH_CPB_MEAN_CUTOFF: score += 25
    if provider_rows["Tot_Suplr_Clms"].sum() > CATH_TOTAL_CLAIMS_CUTOFF: score += 20
    return min(score, 100.0)


def upcoding_score(provider_rows):
    ratios = provider_rows["charge_to_allowed_ratio"].dropna()
    if ratios.empty:
        return 0.0
    score = 0.0
    if ratios.max()  > CATH_CHARGE_MAX_CUTOFF: score += 50
    if ratios.mean() > CATH_CHARGE_MEAN_CUTOFF: score += 30
    return min(score, 100.0)


def geo_score(provider_rows):
    score = 0.0
    if len(provider_rows) == 0:
        return score
    state = provider_rows["Suplr_Prvdr_State_Abrvtn"].iloc[0]
    if state in HIGH_RISK_CATHETER_STATES:
        score += 30
    if state == "OK":
        score += 10
    return min(score, 100.0)


# ── RUN COMPOSITE ON ALL CANDIDATES ─────────────────────────────────
results = []

for npi in candidate_npis:

    provider_rows  = df[df["Suplr_NPI"] == npi]
    bundling_row   = bundling_df[bundling_df["npi"] == npi]

    if bundling_row.empty:
        continue

    b_score = bundling_row["bundling_score"].values[0]
    v_score = volume_score(provider_rows)
    n_score = units_score(npi)
    u_score = upcoding_score(provider_rows)
    g_score = geo_score(provider_rows)
    m_score = 0.0    # no member calls applied, baseline only

    # Weights and the override floor live in caet_shared.h2_composite
    flags = str(bundling_row["flags"].values[0])
    composite = round(h2_composite(b_score, n_score, v_score, u_score, g_score, m_score, flags), 2)

    results.append({
        "npi":             npi,
        "provider_name":   bundling_row["provider_name"].values[0],
        "state":           bundling_row["state"].values[0],
        "bundling_score":  b_score,
        "units_score":     n_score,
        "volume_score":    v_score,
        "upcoding_score":  u_score,
        "geo_score":       g_score,
        "member_call_score": m_score,
        "composite_score": composite,
        "h2_tier":         tier(composite),
        "flags":           flags
    })

# ── BUILD RESULTS DATAFRAME ──────────────────────────────────────────
results_df = pd.DataFrame(results).sort_values("composite_score", ascending=False)

print("\n=== H2 CATHETER COMPOSITE SCORES ===")
print(results_df[["npi","provider_name","state","composite_score","h2_tier"]].to_string(index=False))

print("\n=== TIER DISTRIBUTION ===")
print(results_df["h2_tier"].value_counts())

print("\n=== TOP 10 HIGHEST RISK CATHETER PROVIDERS ===")
print(results_df.head(10).to_string(index=False))

# ── SAVE ─────────────────────────────────────────────────────────────
results_df.to_csv(str(BASE_DIR / "catheter_composite_scores.csv"), index=False)
print("\nSaved: catheter_composite_scores.csv")