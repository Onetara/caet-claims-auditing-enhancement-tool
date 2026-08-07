# viz_01_h1_tier_distribution.py
# H1 Tier Distribution Bar Chart
# Input: h1_composite_results.csv

import pandas as pd
import matplotlib.pyplot as plt

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv("h1_composite_results.csv")

# ── COUNT TIERS ──────────────────────────────────────────────────────
tier_counts = df["h1_tier"].value_counts().reindex(["LOW", "MEDIUM", "HIGH", "CRITICAL"], fill_value=0)

# ── CHART ────────────────────────────────────────────────────────────
colors = ["green", "yellow", "orange", "red"]

plt.figure(figsize=(8, 5))
plt.bar(tier_counts.index, tier_counts.values, color=colors, edgecolor="black")
plt.title("H1 General DME — Provider Risk Tier Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Risk Tier")
plt.ylabel("Number of Providers")

for i, val in enumerate(tier_counts.values):
    plt.text(i, val + 50, str(val), ha="center", fontweight="bold")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig("viz_01_h1_tier_distribution.png", dpi=150)
plt.show()
print("Saved: viz_01_h1_tier_distribution.png")
