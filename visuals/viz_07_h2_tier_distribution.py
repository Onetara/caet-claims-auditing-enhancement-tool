# viz_07_h2_tier_distribution.py
# Catheter H2: tier distribution for the CMS test pool (signals alone, with calls)
# and the constant simulated set
# Input: h2_test_results.csv, h2_with_calls.csv, tier_test_results.csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "CAET_tool"  # pipeline outputs

# ── LOAD ─────────────────────────────────────────────────────────────
alone = pd.read_csv(str(DATA_DIR / "h2_test_results.csv"))
calls = pd.read_csv(str(DATA_DIR / "h2_with_calls.csv"))
const = pd.read_csv(str(DATA_DIR / "tier_test_results.csv"))
const = const[const["hypothesis"] == "H2"]

# Same test pool as step15 (suppliers in the five high-risk catheter states)
pool_npis = set(alone["npi"])
calls     = calls[calls["npi"].isin(pool_npis)]

tiers  = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow", "LOW": "green"}

def pie(ax, series, title):
    counts = series.value_counts().reindex(tiers, fill_value=0)
    counts = counts[counts > 0]
    ax.pie(counts.values, labels=counts.index, autopct="%1.0f%%",
           colors=[colors[t] for t in counts.index], startangle=90,
           wedgeprops={"edgecolor": "black"})
    hit = series.isin(["HIGH", "CRITICAL"]).sum() / len(series)
    ax.set_title(f"{title}\nHigh or Critical: {hit:.0%}", fontsize=11, fontweight="bold")

# ── CHART ────────────────────────────────────────────────────────────
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(16, 5.5))

pie(ax1, alone["tier"], f"CMS test pool, signals alone ({len(alone)})")
pie(ax2, calls["updated_tier"], f"CMS test pool, with calls ({len(calls)})")

x, w = np.arange(len(tiers)), 0.38
c_before = const["tier_no_calls"].value_counts().reindex(tiers, fill_value=0)
c_after  = const["actual"].value_counts().reindex(tiers, fill_value=0)
ax3.bar(x - w/2, c_before.values, w, label="Signals alone", color="steelblue", edgecolor="black")
ax3.bar(x + w/2, c_after.values,  w, label="Signals plus calls", color="crimson", edgecolor="black", hatch="//")
ax3.set_xticks(x)
ax3.set_xticklabels(tiers)
ax3.set_yticks(range(0, int(max(c_before.max(), c_after.max())) + 2))
ax3.set_ylabel("Number of Simulated Suppliers")
ax3.set_title("Constant simulated set (SIMULATED)", fontsize=11, fontweight="bold")
ax3.legend()

fig.suptitle("H2 Catheter: Tier Distribution (target: 75% High or Critical)", fontsize=13, fontweight="bold")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig(str(BASE_DIR / "viz_07_h2_tier_distribution.png"), dpi=150)
plt.show()
print("Saved: viz_07_h2_tier_distribution.png")
