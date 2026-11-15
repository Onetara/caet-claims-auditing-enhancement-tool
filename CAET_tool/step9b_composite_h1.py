import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# Load foundation
df = pd.read_csv(str(BASE_DIR / "dme_with_signals.csv"))

# ============================================================
# RUN ALL 5 SCORERS (consolidated from individual scripts)
# ============================================================

# --- UPCODING SCORER (Step 5) ---
def tiered_points(ratio, p90, p99, weight):
    # 100 points at the 99th percentile cutoff, 60 at the 90th, else 0, scaled by weight
    if pd.isna(ratio): return 0
    if ratio >= p99: base = 100
    elif ratio >= p90: base = 60
    else: base = 0
    return base * weight

CHARGE_90, CHARGE_99 = 11.50, 29.78
def upcoding_score(row):
    return tiered_points(row["charge_to_allowed_ratio"], CHARGE_90, CHARGE_99, row["category_risk_weight"])
df["upcoding_score"] = df.apply(upcoding_score, axis=1)

# --- VOLUME SCORER (Step 6) ---
CLAIMS_90, CLAIMS_99 = 5.67, 8.80
def volume_score(row):
    return tiered_points(row["claims_per_bene"], CLAIMS_90, CLAIMS_99, row["category_risk_weight"])
df["volume_score"] = df.apply(volume_score, axis=1)

# --- GEOGRAPHIC SCORER (Step 7) ---
HIGH_RISK_STATES = ["CA", "FL", "TX", "NY", "IL"]
provider_volume = df.groupby("Suplr_NPI")["Tot_Suplr_Clms"].sum().reset_index()
provider_volume.columns = ["Suplr_NPI", "provider_total_claims"]
provider_state = df.groupby("Suplr_NPI")["Suplr_Prvdr_State_Abrvtn"].first().reset_index()
provider_volume = provider_volume.merge(provider_state, on="Suplr_NPI")
state_95 = provider_volume.groupby("Suplr_Prvdr_State_Abrvtn")["provider_total_claims"].quantile(0.95).reset_index()
state_95.columns = ["Suplr_Prvdr_State_Abrvtn", "state_95_threshold"]
provider_volume = provider_volume.merge(state_95, on="Suplr_Prvdr_State_Abrvtn")
provider_volume["is_state_outlier"] = provider_volume["provider_total_claims"] > provider_volume["state_95_threshold"]
df = df.merge(provider_volume[["Suplr_NPI", "is_state_outlier"]], on="Suplr_NPI", how="left")

def geo_score(row):
    points = 0
    if row["Suplr_Prvdr_State_Abrvtn"] in HIGH_RISK_STATES:
        points += 30
        if row["Suplr_Prvdr_RUCA_Cat"] == "Urban":
            points += 15
    if row["is_state_outlier"]: points += 20
    return min(points, 100)
df["geo_score"] = df.apply(geo_score, axis=1)

# --- MEMBER CALL SCORER (Step 8: PLACEHOLDER, all zeros) ---
df["member_call_score"] = 0

# --- RENTAL ABUSE SCORER (Step 9a) ---
df["is_rental"] = (df["Suplr_Rentl_Ind"] == "Y").astype(int)
prov_rental = df.groupby("Suplr_NPI").agg(
    total_rows=("is_rental", "count"),
    rental_rows=("is_rental", "sum")
).reset_index()
prov_rental["rental_ratio"] = prov_rental["rental_rows"] / prov_rental["total_rows"]
rental_90 = prov_rental["rental_ratio"].quantile(0.90)
rental_99 = prov_rental["rental_ratio"].quantile(0.99)
df = df.merge(prov_rental[["Suplr_NPI", "rental_ratio"]], on="Suplr_NPI", how="left")

def rental_score(row):
    if not row["is_rental"]: return 0
    return tiered_points(row["rental_ratio"], rental_90, rental_99, row["category_risk_weight"])
df["rental_score"] = df.apply(rental_score, axis=1)

# ============================================================
# STEP 9b: AGGREGATE TO PROVIDER LEVEL + COMPOSITE
# ============================================================

# Roll up row-level scores to provider-level (take MAX = worst case per provider)
provider_scores = df.groupby("Suplr_NPI").agg(
    upcoding_max=("upcoding_score", "max"),
    volume_max=("volume_score", "max"),
    geo_max=("geo_score", "max"),
    member_call_max=("member_call_score", "max"),
    rental_max=("rental_score", "max")
).reset_index()

# Apply composite weights
provider_scores["composite_score"] = (
    provider_scores["member_call_max"] * 0.35 +
    provider_scores["upcoding_max"]    * 0.25 +
    provider_scores["volume_max"]      * 0.20 +
    provider_scores["rental_max"]      * 0.10 +
    provider_scores["geo_max"]         * 0.10
)

# Tier assignment
def tier(score):
    if score >= 80: return "CRITICAL"
    elif score >= 60: return "HIGH"
    elif score >= 40: return "MEDIUM"
    else: return "LOW"
provider_scores["h1_tier"] = provider_scores["composite_score"].apply(tier)

# Verify
print("=== Provider count ===")
print(f"Total unique providers: {len(provider_scores)}")

print("\n=== Tier distribution ===")
print(provider_scores["h1_tier"].value_counts())

print("\n=== Composite score stats ===")
print(provider_scores["composite_score"].describe())

print("\n=== Top 10 highest-scoring providers ===")
print(provider_scores.sort_values("composite_score", ascending=False).head(10))

# Save the result
output_path = str(BASE_DIR / "h1_composite_results.csv")
provider_scores.to_csv(output_path, index=False)
print(f"\n✅ Saved provider-level H1 composite to: {output_path}")