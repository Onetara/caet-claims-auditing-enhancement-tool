# viz_03_h1_call_impact.py
# Before vs After Member Calls: Tier Comparison (CMS data and constant simulated set)
# Input: h1_with_calls.csv, tier_test_results.csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "CAET_tool"  # pipeline outputs

# ── LOAD ─────────────────────────────────────────────────────────────
df    = pd.read_csv(str(DATA_DIR / "h1_with_calls.csv"))
const = pd.read_csv(str(DATA_DIR / "tier_test_results.csv"))
const = const[const["hypothesis"] == "H1"]

# ── COUNT TIERS BEFORE AND AFTER ─────────────────────────────────────
tiers = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

before_counts = df["h1_tier"].value_counts().reindex(tiers, fill_value=0)
after_counts  = df["updated_tier"].value_counts().reindex(tiers, fill_value=0)
c_before      = const["tier_no_calls"].value_counts().reindex(tiers, fill_value=0)
c_after       = const["actual"].value_counts().reindex(tiers, fill_value=0)

# ── CHART ────────────────────────────────────────────────────────────
x     = np.arange(len(tiers))
width = 0.35

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

ax1.bar(x - width/2, before_counts.values, width, label="Before Calls", color="steelblue", edgecolor="black")
ax1.bar(x + width/2, after_counts.values,  width, label="After Calls",  color="crimson",   edgecolor="black", hatch="//")
ax1.set_xticks(x)
ax1.set_xticklabels(tiers)
ax1.set_title("CMS data (simulated calls on 14 suppliers)", fontsize=11, fontweight="bold")
ax1.set_xlabel("Risk Tier")
ax1.set_ylabel("Number of Providers (log scale)")
ax1.set_yscale("log")
ax1.legend()
for i in range(len(tiers)):
    ax1.text(i - width/2, max(before_counts.values[i], 1) * 1.1, str(before_counts.values[i]), ha="center", fontsize=9)
    ax1.text(i + width/2, max(after_counts.values[i], 1) * 1.1,  str(after_counts.values[i]),  ha="center", fontsize=9)

ax2.bar(x - width/2, c_before.values, width, label="Before Calls", color="steelblue", edgecolor="black")
ax2.bar(x + width/2, c_after.values,  width, label="After Calls",  color="crimson",   edgecolor="black", hatch="//")
ax2.set_xticks(x)
ax2.set_xticklabels(tiers)
ax2.set_yticks(range(0, int(max(c_before.max(), c_after.max())) + 2))
ax2.set_title("Constant simulated set (SIMULATED)", fontsize=11, fontweight="bold")
ax2.set_xlabel("Risk Tier")
ax2.set_ylabel("Number of Simulated Suppliers")
ax2.legend()

fig.suptitle("H1 General DME: Tier Distribution Before vs After Member Calls", fontsize=13, fontweight="bold")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig(str(BASE_DIR / "viz_03_h1_call_impact.png"), dpi=150)
plt.show()
print("Saved: viz_03_h1_call_impact.png")
