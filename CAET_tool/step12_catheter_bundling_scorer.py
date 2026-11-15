# step12_catheter_bundling_scorer.py
# Scores catheter providers on 4 bundling fraud signals
# Requires: dme_with_signals.csv, catheter_candidates.csv

import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# ── LOAD ────────────────────────────────────────────────────────────
df              = pd.read_csv(str(BASE_DIR / "dme_with_signals.csv"))
candidates      = pd.read_csv(str(BASE_DIR / "catheter_candidates.csv"))
candidate_npis  = candidates["Suplr_NPI"].unique()

# ── HCPCS CODE GROUPS ────────────────────────────────────────────────
ACCESSORY_CODES = {"A4332", "A4333", "A4334", "A4331", "A4357", "A4358"}
PRIMARY_CODES   = {"A4351", "A4352", "A4353", "A4354", "A4349", "A4338", "A4340", "A4344"}

HIGH_RISK_CATHETER_STATES = ["OK", "FL", "NY", "TX", "GA"]

# ── BUNDLING SCORER FUNCTION ─────────────────────────────────────────
def catheter_bundling_scorer(provider_rows):

    score = 0
    flags = []

    cath_rows    = provider_rows[provider_rows["fraud_hcpcs_cat"] == "CATHETER"]
    billed_codes = set(cath_rows["HCPCS_Cd"].dropna().unique())
    code_count   = len(billed_codes)

    # Signal 1: Kitchen Sink Bundling
    if code_count >= 14:
        score += 55
        flags.append(f"EXTREME_CATHETER_BUNDLING: {code_count} codes")
    elif code_count >= 8:
        score += 35
        flags.append(f"HIGH_CATHETER_BUNDLING: {code_count} codes")
    elif code_count >= 5:
        score += 15
        flags.append(f"ELEVATED_CATHETER_BUNDLING: {code_count} codes")

    # Signal 2: Straight + Coude Simultaneous Billing
    if "A4351" in billed_codes and "A4352" in billed_codes:
        score += 30
        flags.append("DUAL_CATHETER_TYPE: A4351 + A4352 billed together")

    # Signal 3: Accessories Without Primary Code
    has_primary   = bool(billed_codes & PRIMARY_CODES)
    has_accessory = bool(billed_codes & ACCESSORY_CODES)

    if has_accessory and not has_primary:
        orphans = billed_codes & ACCESSORY_CODES
        score  += 25
        flags.append(f"ORPHAN_ACCESSORIES: {orphans} billed without primary")

    # Signal 4: Oklahoma Anomaly
    if len(provider_rows) > 0:
        state           = provider_rows["Suplr_Prvdr_State_Abrvtn"].iloc[0]
        total_cath_clms = cath_rows["Tot_Suplr_Clms"].sum()

        if state == "OK" and total_cath_clms > 100:
            score += 20
            flags.append(f"OKLAHOMA_ANOMALY: {total_cath_clms:,} catheter claims")

    return min(score, 100), flags


# ── RUN SCORER ON ALL CANDIDATES ─────────────────────────────────────
results = []

for npi in candidate_npis:

    provider_rows  = df[df["Suplr_NPI"] == npi]
    score, flags   = catheter_bundling_scorer(provider_rows)
    state          = provider_rows["Suplr_Prvdr_State_Abrvtn"].iloc[0] if len(provider_rows) > 0 else "UNKNOWN"
    name           = provider_rows["Suplr_Prvdr_Last_Name_Org"].iloc[0] if len(provider_rows) > 0 else "UNKNOWN"
    code_count     = candidates.loc[candidates["Suplr_NPI"] == npi, "distinct_catheter_codes"].values[0]

    results.append({
        "npi":                    npi,
        "provider_name":          name,
        "state":                  state,
        "distinct_catheter_codes": code_count,
        "bundling_score":         score,
        "flags":                  " | ".join(flags)
    })

# ── BUILD RESULTS DATAFRAME ──────────────────────────────────────────
results_df = results_df = pd.DataFrame(results).sort_values("bundling_score", ascending=False)

print(f"\n=== CATHETER BUNDLING SCORES ===")
print(results_df[["npi","provider_name","state","distinct_catheter_codes","bundling_score"]].to_string(index=False))

print(f"\n=== SCORE DISTRIBUTION ===")
print(results_df["bundling_score"].describe().round(2))

print(f"\n=== TOP 10 HIGHEST BUNDLING SCORES ===")
print(results_df.head(10).to_string(index=False))

# ── SAVE ─────────────────────────────────────────────────────────────
results_df.to_csv(str(BASE_DIR / "catheter_bundling_scores.csv"), index=False)
print("\nSaved: catheter_bundling_scores.csv")