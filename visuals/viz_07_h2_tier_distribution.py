# viz_07_h2_tier_distribution.py
# Catheter H2 Test Sample: Tier Distribution
# Input: h2_test_results.csv

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent  # project root, holds the shared CSVs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "h2_test_results.csv"))

# ── COUNT TIERS ──────────────────────────────────────────────────────
tier_counts = df["tier"].value_counts()

colors = {"HIGH": "orange", "MEDIUM": "yellow", "LOW": "green", "CRITICAL": "red"}
chart_colors = [colors[t] for t in tier_counts.index]

# ── CHART ────────────────────────────────────────────────────────────
plt.figure(figsize=(7, 7))
plt.pie(
    tier_counts.values,
    labels=tier_counts.index,
    autopct="%1.0f%%",
    colors=chart_colors,
    startangle=90,
    wedgeprops={"edgecolor": "black"}
)

hit_rate = (df["tier"].isin(["HIGH", "CRITICAL"]).sum()) / len(df)

plt.title(
    f"H2 Catheter Test Results: Tier Distribution\nHit Rate: {hit_rate:.0%}  (Threshold: 75%)",
    fontsize=13, fontweight="bold"
)

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_07_h2_tier_distribution.png"), dpi=150)
plt.show()
print("Saved: viz_07_h2_tier_distribution.png")