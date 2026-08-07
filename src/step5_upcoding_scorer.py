import pandas as pd

# Load the foundation file
df = pd.read_csv("dme_with_signals.csv")

# Thresholds from Step 4 (general DME)
CHARGE_90 = 11.50
CHARGE_99 = 29.78

# Step 5: Build the upcoding scorer
def upcoding_score(row):
    ratio = row["charge_to_allowed_ratio"]
    weight = row["category_risk_weight"]

    # Assign base points by tier
    if pd.isna(ratio):
        base_points = 0
    elif ratio >= CHARGE_99:
        base_points = 100  # EXTREME tier
    elif ratio >= CHARGE_90:
        base_points = 60   # ELEVATED tier
    else:
        base_points = 0    # Below threshold

    # Multiply by category risk weight
    return base_points * weight

# Apply to every row
df["upcoding_score"] = df.apply(upcoding_score, axis=1)

# Tag the tier for readability
def upcoding_tier(ratio):
    if pd.isna(ratio):
        return "NONE"
    elif ratio >= CHARGE_99:
        return "EXTREME_UPCODING"
    elif ratio >= CHARGE_90:
        return "ELEVATED_UPCODING"
    else:
        return "NONE"

df["upcoding_tier"] = df["charge_to_allowed_ratio"].apply(upcoding_tier)

# Verify
print("=== Tier counts ===")
print(df["upcoding_tier"].value_counts())

print("\n=== Score stats ===")
print(df["upcoding_score"].describe())

print("\n=== Sample flagged rows ===")
print(df[df["upcoding_tier"] != "NONE"][["Suplr_NPI", "HCPCS_Cd", "fraud_hcpcs_cat",
                                          "charge_to_allowed_ratio", "upcoding_tier",
                                          "upcoding_score"]].head(10))