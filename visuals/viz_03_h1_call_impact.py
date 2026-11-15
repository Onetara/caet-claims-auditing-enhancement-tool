# viz_03_h1_call_impact.py
# Before vs After Member Calls: Tier Comparison
# Input: h1_with_calls.csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent  # .../data _visualization
DATA_DIR = BASE_DIR.parent  # project root, holds the shared CSVs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "h1_with_calls.csv"))

# ── COUNT TIERS BEFORE AND AFTER ─────────────────────────────────────
tiers = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

before_counts = df["h1_tier"].value_counts().reindex(tiers, fill_value=0)
after_counts  = df["updated_tier"].value_counts().reindex(tiers, fill_value=0)

# ── CHART ────────────────────────────────────────────────────────────
x     = np.arange(len(tiers))
width = 0.35

plt.figure(figsize=(9, 5))
plt.bar(x - width/2, before_counts.values, width, label="Before Calls", color="steelblue", edgecolor="black")
plt.bar(x + width/2, after_counts.values,  width, label="After Calls",  color="crimson",   edgecolor="black", hatch="//")

plt.xticks(x, tiers)
plt.title("H1 General DME: Tier Distribution Before vs After Member Calls", fontsize=13, fontweight="bold")
plt.xlabel("Risk Tier")
plt.ylabel("Number of Providers")
plt.yscale('log')
plt.legend()

# Label bars
for i in range(len(tiers)):
    plt.text(i - width/2, before_counts.values[i] + 20, str(before_counts.values[i]), ha="center", fontsize=9)
    plt.text(i + width/2, after_counts.values[i] + 20,  str(after_counts.values[i]),  ha="center", fontsize=9)

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_03_h1_call_impact.png"), dpi=150)
plt.show()
print("Saved: viz_03_h1_call_impact.png")