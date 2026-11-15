# viz_04_h1_top20_providers.py
# Top 20 Highest Risk Providers (H1)
# Input: h1_with_calls.csv

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent  # project root, holds the shared CSVs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "h1_with_calls.csv"))

# ── TOP 20 BY COMPOSITE SCORE (WITH CALLS) ──────────────────────────
top20 = df.sort_values("composite_with_calls", ascending=False).head(20)

# ── COLOR BY TIER ────────────────────────────────────────────────────
tier_colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow", "LOW": "green"}
colors = top20["updated_tier"].map(tier_colors)

# ── CHART ────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 8))
plt.barh(top20["Suplr_NPI"].astype(str), top20["composite_with_calls"], color=colors, edgecolor="black")

plt.title("Top 20 Highest Risk Providers: H1 General DME", fontsize=13, fontweight="bold")
plt.xlabel("Composite Score (0-100)")
plt.ylabel("Provider NPI")
plt.gca().invert_yaxis()   # highest score at top

for i, val in enumerate(top20["composite_with_calls"]):
    plt.text(val + 0.5, i, f"{val:.1f}", va="center", fontsize=8)

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_04_h1_top20_providers.png"), dpi=150)
plt.show()
print("Saved: viz_04_h1_top20_providers.png")
