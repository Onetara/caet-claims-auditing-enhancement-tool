# step11_identify_catheter_providers.py
# Identifies catheter providers billing 8+ distinct HCPCS codes
# Requires: dme_with_signals.csv

import pandas as pd
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# ── LOAD ────────────────────────────────────────────────────────────
df = pd.read_csv(str(BASE_DIR / "dme_with_signals.csv"))

# ── FILTER TO CATHETER CODES ONLY ───────────────────────────────────
catheter_df = df[df["fraud_hcpcs_cat"] == "CATHETER"]

print(f"Total catheter records   : {len(catheter_df):,}")
print(f"Unique catheter providers: {catheter_df['Suplr_NPI'].nunique():,}")

# ── COUNT DISTINCT HCPCS CODES PER NPI ──────────────────────────────
codes_per_npi = (
    catheter_df
    .groupby("Suplr_NPI")["HCPCS_Cd"]
    .nunique()
    .reset_index()
    .rename(columns={"HCPCS_Cd": "distinct_catheter_codes"})
)

# ── KEEP PROVIDERS BILLING 8+ CODES (90th percentile) ───────────────
catheter_candidates = codes_per_npi[
    codes_per_npi["distinct_catheter_codes"] >= 8
]

print(f"\nProviders billing 8+ catheter codes: {len(catheter_candidates):,}")
print(catheter_candidates.sort_values("distinct_catheter_codes", ascending=False))

# ── SAVE ─────────────────────────────────────────────────────────────
catheter_candidates.to_csv(str(BASE_DIR / "catheter_candidates.csv"), index=False)
print("\nSaved: catheter_candidates.csv")