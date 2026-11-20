import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# Load the foundation file (NOT the raw master)
df = pd.read_csv(str(BASE_DIR / "dme_with_signals.csv"))

print("=== GENERAL DME THRESHOLDS (all categories) ===")

# Charge-to-allowed ratio percentiles
charge_75 = df["charge_to_allowed_ratio"].quantile(0.75)
charge_90 = df["charge_to_allowed_ratio"].quantile(0.90)
charge_99 = df["charge_to_allowed_ratio"].quantile(0.99)

print(f"Charge Ratio 75th: {charge_75:.2f}")
print(f"Charge Ratio 90th: {charge_90:.2f}")
print(f"Charge Ratio 99th: {charge_99:.2f}")

# Claims per beneficiary percentiles
claims_75 = df["claims_per_bene"].quantile(0.75)
claims_90 = df["claims_per_bene"].quantile(0.90)
claims_99 = df["claims_per_bene"].quantile(0.99)

print(f"\nClaims/Bene 75th: {claims_75:.2f}")
print(f"Claims/Bene 90th: {claims_90:.2f}")
print(f"Claims/Bene 99th: {claims_99:.2f}")

# ── CATHETER PERCENTILES (for the H2 cutoffs in caet_shared.py) ──────
# Provider-level max and mean of each signal, catheter rows only.
# Match each H2 cutoff in caet_shared.py to a percentile printed here.
print("\n=== CATHETER PROVIDER-LEVEL PERCENTILES (H2 cutoffs) ===")

cath = df[df["fraud_hcpcs_cat"] == "CATHETER"]
per_provider = cath.groupby("Suplr_NPI").agg(
    charge_max=("charge_to_allowed_ratio", "max"),
    charge_mean=("charge_to_allowed_ratio", "mean"),
    cpb_max=("claims_per_bene", "max"),
    cpb_mean=("claims_per_bene", "mean"),
    total_claims=("Tot_Suplr_Clms", "sum"),
)
percentiles = per_provider.quantile([0.75, 0.90, 0.95, 0.99]).round(2)
print(percentiles.to_string())
print(f"\nCatheter providers: {len(per_provider):,}")
