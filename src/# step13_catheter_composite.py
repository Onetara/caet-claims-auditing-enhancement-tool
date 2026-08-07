# step13_catheter_composite.py
# Applies catheter-specific weights to produce final composite score
# Requires: dme_with_signals.csv, catheter_bundling_scores.csv

import pandas as pd

# ── LOAD ────────────────────────────────────────────────────────────
df             = pd.read_csv("dme_with_signals.csv")
bundling_df    = pd.read_csv("catheter_bundling_scores.csv")
candidate_npis = bundling_df["npi"].unique()

HIGH_RISK_CATHETER_STATES = ["OK", "FL", "NY", "TX", "GA"]

# ── CATHETER COMPOSITE WEIGHTS ───────────────────────────────────────
# Bundling is the dominant signal for catheter fraud
WEIGHTS = {
    "catheter_bundling": 0.40,
    "member_call":       0.25,
    "volume":            0.15,
    "upcoding":          0.10,
    "geographic":        0.10,
}

# ── SUPPORTING SCORERS ───────────────────────────────────────────────
def volume_score(provider_rows):
    cpb = provider_rows["claims_per_bene"].dropna()
    if cpb.empty:
        return 0.0
    score = 0.0
    if cpb.max()  > 9.12: score += 40
    if cpb.mean() > 5.35: score += 25
    if provider_rows["Tot_Suplr_Clms"].sum() > 50000: score += 20
    return min(score, 100.0)


def upcoding_score(provider_rows):
    ratios = provider_rows["charge_to_allowed_ratio"].dropna()
    if ratios.empty:
        return 0.0
    score = 0.0
    if ratios.max()  > 4.14: score += 50
    if ratios.mean() > 1.52: score += 30
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


def tier(score):
    if   score >= 80: return "CRITICAL"
    elif score >= 60: return "HIGH"
    elif score >= 40: return "MEDIUM"
    else:             return "LOW"


# ── RUN COMPOSITE ON ALL CANDIDATES ─────────────────────────────────
results = []

for npi in candidate_npis:

    provider_rows  = df[df["Suplr_NPI"] == npi]
    bundling_row   = bundling_df[bundling_df["npi"] == npi]

    if bundling_row.empty:
        continue

    b_score = bundling_row["bundling_score"].values[0]
    v_score = volume_score(provider_rows)
    u_score = upcoding_score(provider_rows)
    g_score = geo_score(provider_rows)
    m_score = 0.0    # no member calls applied — baseline only

    composite = (
        (b_score * WEIGHTS["catheter_bundling"]) +
        (m_score * WEIGHTS["member_call"])       +
        (v_score * WEIGHTS["volume"])            +
        (u_score * WEIGHTS["upcoding"])          +
        (g_score * WEIGHTS["geographic"])
    )

    # Override floor rule — see Step 14 in outline
    flags = str(bundling_row["flags"].values[0])
    if ("EXTREME_CATHETER_BUNDLING" in flags) and (g_score >= 30):
        composite = max(composite, 65.0)
    elif flags.count("|") >= 1 and ("HIGH_CATHETER_BUNDLING" in flags):
        composite = max(composite, 42.0)

    composite = round(composite, 2)

    results.append({
        "npi":             npi,
        "provider_name":   bundling_row["provider_name"].values[0],
        "state":           bundling_row["state"].values[0],
        "bundling_score":  b_score,
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
results_df.to_csv("catheter_composite_scores.csv", index=False)
print("\nSaved: catheter_composite_scores.csv")