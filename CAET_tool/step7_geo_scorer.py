import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(str(BASE_DIR / "dme_with_signals.csv"))

print([c for c in df.columns if "STATE" in c.upper() or "CNTRY" in c.upper() or "RUCA" in c.upper()])
# Quick look at what's in the geographic columns
print("\n=== Top 10 states ===")
print(df["Suplr_Prvdr_State_Abrvtn"].value_counts().head(10))

print("\n=== Country distribution ===")
print(df["Suplr_Prvdr_Cntry"].value_counts().head(10))

print("\n=== RUCA categories ===")
print(df["Suplr_Prvdr_RUCA_Cat"].value_counts())
# Step 7: Build the Geographic Risk Scorer (with state-level outlier)
HIGH_RISK_STATES = ["CA", "FL", "TX", "NY", "IL"]

# Calculate each provider's total claim volume (sum across all their HCPCS codes)
provider_volume = df.groupby("Suplr_NPI")["Tot_Suplr_Clms"].sum().reset_index()
provider_volume.columns = ["Suplr_NPI", "provider_total_claims"]

# Attach each provider's state
provider_state = df.groupby("Suplr_NPI")["Suplr_Prvdr_State_Abrvtn"].first().reset_index()
provider_volume = provider_volume.merge(provider_state, on="Suplr_NPI")

# Calculate 95th percentile of claim volume WITHIN each state
state_95 = provider_volume.groupby("Suplr_Prvdr_State_Abrvtn")["provider_total_claims"].quantile(0.95).reset_index()
state_95.columns = ["Suplr_Prvdr_State_Abrvtn", "state_95_threshold"]

# Flag providers above their state's 95th percentile
provider_volume = provider_volume.merge(state_95, on="Suplr_Prvdr_State_Abrvtn")
provider_volume["is_state_outlier"] = provider_volume["provider_total_claims"] > provider_volume["state_95_threshold"]

# Merge this flag back to every row of the main df
df = df.merge(provider_volume[["Suplr_NPI", "is_state_outlier"]], on="Suplr_NPI", how="left")

# Now build the scorer
def geo_score(row):
    state = row["Suplr_Prvdr_State_Abrvtn"]
    ruca = row["Suplr_Prvdr_RUCA_Cat"]
    is_outlier = row["is_state_outlier"]

    points = 0
    if state in HIGH_RISK_STATES:
        points += 30
        if ruca == "Urban":
            points += 15
    if is_outlier:
        points += 20

    return min(points, 100)

def geo_tier(row):
    state = row["Suplr_Prvdr_State_Abrvtn"]
    ruca = row["Suplr_Prvdr_RUCA_Cat"]
    is_outlier = row["is_state_outlier"]

    flags = []
    if state in HIGH_RISK_STATES:
        flags.append("HIGH_RISK_STATE")
        if ruca == "Urban":
            flags.append("URBAN")
    if is_outlier:
        flags.append("STATE_LEVEL_OUTLIER")

    return "+".join(flags) if flags else "NONE"

df["geo_score"] = df.apply(geo_score, axis=1)
df["geo_tier"] = df.apply(geo_tier, axis=1)

# Verify
print("\n=== Tier counts ===")
print(df["geo_tier"].value_counts())

print("\n=== Score stats ===")
print(df["geo_score"].describe())

print("\n=== Sample state outliers ===")
print(df[df["is_state_outlier"]][[
    "Suplr_NPI", "Suplr_Prvdr_State_Abrvtn", "Suplr_Prvdr_RUCA_Cat",
    "geo_tier", "geo_score"
]].drop_duplicates("Suplr_NPI").head(10))