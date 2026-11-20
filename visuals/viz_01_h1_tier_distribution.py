# viz_01_h1_tier_distribution.py
# H1 Tier Distribution: CMS data (signals alone) and the constant simulated set
# Input: h1_composite_results.csv, tier_test_results.csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "CAET_tool"  # pipeline outputs

# ── LOAD ─────────────────────────────────────────────────────────────
df    = pd.read_csv(str(DATA_DIR / "h1_composite_results.csv"))
const = pd.read_csv(str(DATA_DIR / "tier_test_results.csv"))
const = const[const["hypothesis"] == "H1"]

tiers  = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
colors = ["green", "yellow", "orange", "red"]

cms_counts   = df["h1_tier"].value_counts().reindex(tiers, fill_value=0)
const_alone  = const["tier_no_calls"].value_counts().reindex(tiers, fill_value=0)
const_calls  = const["actual"].value_counts().reindex(tiers, fill_value=0)

# ── CHART ────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

ax1.bar(tiers, cms_counts.values, color=colors, edgecolor="black")
ax1.set_title("CMS data, signals alone\n(59,592 suppliers)", fontsize=12, fontweight="bold")
ax1.set_xlabel("Risk Tier")
ax1.set_ylabel("Number of Providers")
for i, val in enumerate(cms_counts.values):
    ax1.text(i, val + 300, str(val), ha="center", fontweight="bold")

x, w = np.arange(len(tiers)), 0.38
ax2.bar(x - w/2, const_alone.values, w, label="Signals alone", color="steelblue", edgecolor="black")
ax2.bar(x + w/2, const_calls.values, w, label="Signals plus calls", color="crimson", edgecolor="black", hatch="//")
ax2.set_xticks(x)
ax2.set_xticklabels(tiers)
ax2.set_title("Constant simulated set\n(8 fake suppliers, SIMULATED)", fontsize=12, fontweight="bold")
ax2.set_xlabel("Risk Tier")
ax2.set_ylabel("Number of Simulated Suppliers")
ax2.set_yticks(range(0, int(max(const_alone.max(), const_calls.max())) + 2))
ax2.legend()

fig.suptitle("H1 General DME: Provider Risk Tier Distribution", fontsize=14, fontweight="bold")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig(str(BASE_DIR / "viz_01_h1_tier_distribution.png"), dpi=150)
plt.show()
print("Saved: viz_01_h1_tier_distribution.png")
