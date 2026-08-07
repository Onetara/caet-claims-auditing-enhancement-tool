import pandas as pd

df = pd.read_csv("dme_with_signals.csv")

# Look for any modifier-related or rental-related columns
print("=== Possible rental/modifier columns ===")
print([c for c in df.columns if "RENT" in c.upper() or "MOD" in c.upper() or "RR" in c.upper() or "NU" in c.upper()])

# Also dump full column list as backup
print("\n=== Full column list ===")
print(df.columns.tolist())
print("=== Suplr_Rentl_Ind value counts ===")
print(df["Suplr_Rentl_Ind"].value_counts(dropna=False))

print("\n=== Sample rows ===")
print(df[["Suplr_NPI", "HCPCS_Cd", "HCPCS_Desc", "Suplr_Rentl_Ind"]].head(10))
# === RENTAL ABUSE SCORER ===

# Convert Y/N to 1/0 for math
df["is_rental"] = (df["Suplr_Rentl_Ind"] == "Y").astype(int)

# Calculate per-provider rental ratio
provider_rental = df.groupby("Suplr_NPI").agg(
    total_rows=("is_rental", "count"),
    rental_rows=("is_rental", "sum")
).reset_index()
provider_rental["rental_ratio"] = provider_rental["rental_rows"] / provider_rental["total_rows"]

# Thresholds from this distribution
rental_75 = provider_rental["rental_ratio"].quantile(0.75)
rental_90 = provider_rental["rental_ratio"].quantile(0.90)
rental_99 = provider_rental["rental_ratio"].quantile(0.99)

print(f"\nProvider rental ratio thresholds:")
print(f"  75th pct: {rental_75:.2%}")
print(f"  90th pct: {rental_90:.2%}")
print(f"  99th pct: {rental_99:.2%}")

# Merge ratio back to every row
df = df.merge(provider_rental[["Suplr_NPI", "rental_ratio"]], on="Suplr_NPI", how="left")

# Build the scorer
def rental_score(row):
    if not row["is_rental"]:
        return 0
    ratio = row["rental_ratio"]
    weight = row["category_risk_weight"]
    if ratio >= rental_99:
        base = 100
    elif ratio >= rental_90:
        base = 60
    else:
        base = 0
    return base * weight

df["rental_score"] = df.apply(rental_score, axis=1)

# Tier
def rental_tier(row):
    if not row["is_rental"]:
        return "NOT_RENTAL"
    ratio = row["rental_ratio"]
    if ratio >= rental_99:
        return "EXTREME_RENTAL"
    elif ratio >= rental_90:
        return "ELEVATED_RENTAL"
    else:
        return "NONE"

df["rental_tier"] = df.apply(rental_tier, axis=1)

# Verify
print("\n=== Tier counts ===")
print(df["rental_tier"].value_counts())

print("\n=== Score stats (rental rows only) ===")
print(df[df["is_rental"] == 1]["rental_score"].describe())

print("\n=== Sample flagged rentals ===")
print(df[df["rental_tier"].isin(["EXTREME_RENTAL", "ELEVATED_RENTAL"])][[
    "Suplr_NPI", "HCPCS_Cd", "fraud_hcpcs_cat", "rental_ratio",
    "rental_tier", "rental_score"
]].drop_duplicates("Suplr_NPI").head(10))