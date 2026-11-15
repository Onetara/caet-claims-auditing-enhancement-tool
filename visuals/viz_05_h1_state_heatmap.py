# viz_05_h1_state_heatmap.py
# Geographic Heatmap: HIGH/CRITICAL Provider Count by State
# Input: h1_composite_results.csv + dme_with_signals.csv

import pandas as pd
import plotly.express as px

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent  # .../data _visualization
DATA_DIR = BASE_DIR.parent  # project root, holds the shared CSVs

# ── LOAD ─────────────────────────────────────────────────────────────
h1_results = pd.read_csv(str(DATA_DIR / "h1_composite_results.csv"))
dme_data   = pd.read_csv(str(DATA_DIR / "dme_with_signals.csv"))

# ── GET STATE PER NPI ────────────────────────────────────────────────
state_lookup = dme_data.groupby("Suplr_NPI")["Suplr_Prvdr_State_Abrvtn"].first().reset_index()
state_lookup.columns = ["Suplr_NPI", "state"]

# ── MERGE STATE INTO H1 RESULTS ──────────────────────────────────────
merged = h1_results.merge(state_lookup, on="Suplr_NPI", how="left")

# ── COUNT PROVIDERS PER STATE (ALL TIERS) ───────────────────────────
state_counts = merged.groupby("state").size().reset_index(name="total_providers")

# ── COUNT HIGH/CRITICAL PROVIDERS PER STATE ─────────────────────────
high_risk = merged[merged["h1_tier"].isin(["HIGH", "CRITICAL"])]
high_risk_counts = high_risk.groupby("state").size().reset_index(name="high_risk_count")

state_counts = state_counts.merge(high_risk_counts, on="state", how="left")
state_counts["high_risk_count"] = state_counts["high_risk_count"].fillna(0)

print(state_counts.sort_values("total_providers", ascending=False).head(10))

# ── MAP ──────────────────────────────────────────────────────────────
fig = px.choropleth(
    state_counts,
    locations="state",
    locationmode="USA-states",
    color="total_providers",
    scope="usa",
    color_continuous_scale="Reds",
    title="H1 General DME: Total Providers by State",
    labels={"total_providers": "Provider Count"}
)

fig.write_html(str(BASE_DIR / "viz_05_h1_state_heatmap.html"))
fig.show()
print("Saved: viz_05_h1_state_heatmap.html")
