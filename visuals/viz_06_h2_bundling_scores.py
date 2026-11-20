# viz_06_h2_bundling_scores.py
# Catheter signal distributions: bundling score and units score
# Input: catheter_composite_scores.csv

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "CAET_tool"  # pipeline outputs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "catheter_composite_scores.csv"))

# ── CHART ────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.hist(df["bundling_score"], bins=20, color="mediumpurple", edgecolor="black")
ax1.set_title("Bundling score (variety of catheter codes)", fontsize=11, fontweight="bold")
ax1.set_xlabel("Bundling Score (0-100)")
ax1.set_ylabel("Number of Providers")

units_counts = df["units_score"].value_counts().reindex([0, 60, 100], fill_value=0)
ax2.bar(["0 (typical)", "60 (90th pct+)", "100 (99th pct+)"], units_counts.values,
        color="teal", edgecolor="black")
ax2.set_title("Units score (units per claim vs same code)", fontsize=11, fontweight="bold")
ax2.set_xlabel("Units Score")
ax2.set_ylabel("Number of Providers")
for i, val in enumerate(units_counts.values):
    ax2.text(i, val + 1, str(val), ha="center", fontweight="bold")

fig.suptitle("H2 Catheter Providers (206 candidates): Billing Signals", fontsize=13, fontweight="bold")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig(str(BASE_DIR / "viz_06_h2_bundling_scores.png"), dpi=150)
plt.show()
print("Saved: viz_06_h2_bundling_scores.png")
