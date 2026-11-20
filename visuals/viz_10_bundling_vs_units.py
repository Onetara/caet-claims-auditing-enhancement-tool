# viz_10_bundling_vs_units.py
# H2 catheter suppliers: bundling score vs units score (two separate signals)
# Input: catheter_composite_scores.csv

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "CAET_tool"  # pipeline outputs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "catheter_composite_scores.csv"))
tier_colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "gold", "LOW": "green"}

# Units score only takes 0, 60 or 100, so spread the dots slightly to keep them visible
rng = np.random.default_rng(7)
jitter = rng.uniform(-4, 4, len(df))

# ── CHART ────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 6))
for t, col in tier_colors.items():
    sub = df["h2_tier"] == t
    if sub.any():
        plt.scatter(df.loc[sub, "bundling_score"], df.loc[sub, "units_score"] + jitter[sub],
                    c=col, edgecolor="black", s=45, label=f"{t} ({sub.sum()})", alpha=0.85)

plt.yticks([0, 60, 100], ["0 (typical)", "60 (90th pct+)", "100 (99th pct+)"])
plt.title("H2 Catheter Suppliers: Bundling vs Units per Claim", fontsize=13, fontweight="bold")
plt.xlabel("Bundling score (variety of catheter codes)")
plt.ylabel("Units score (units per claim vs same code)")
plt.legend(title="Baseline tier")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_10_bundling_vs_units.png"), dpi=150)
plt.show()
print("Saved: viz_10_bundling_vs_units.png")
