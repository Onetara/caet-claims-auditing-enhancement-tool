import pandas as pd

# Load the foundation file (NOT the raw master)
df = pd.read_csv("dme_with_signals.csv")

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