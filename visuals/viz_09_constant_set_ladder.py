# viz_09_constant_set_ladder.py
# Constant simulated set: each fake supplier's score against the tier bands
# Input: tier_test_results.csv

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "CAET_tool"  # pipeline outputs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "tier_test_results.csv"))
tier_colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow", "LOW": "green"}

# ── CHART ────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

for ax, hyp in zip(axes, ["H1", "H2"]):
    sub = df[df["hypothesis"] == hyp].reset_index(drop=True)
    y = range(len(sub))
    ax.barh(y, sub["composite_no_calls"], height=0.38, color="lightgray",
            edgecolor="black", label="Signals alone")
    ax.barh([i + 0.4 for i in y], sub["composite"], height=0.38,
            color=sub["actual"].map(tier_colors), edgecolor="black", label="Signals plus calls")
    for cut in (40, 60, 80):
        ax.axvline(cut, color="black", linestyle="--", linewidth=0.8)
    ax.set_yticks([i + 0.2 for i in y])
    ax.set_yticklabels(sub["case"], fontsize=8)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Composite Score (0-100); dashed lines = tier bands 40, 60, 80", labelpad=4)
    ax.set_title(f"{hyp}: 8 simulated suppliers, expected tier reached: {int(sub['match'].sum())}/8",
                 fontsize=11, fontweight="bold")
    for i, val in enumerate(sub["composite"]):
        ax.text(val + 1, i + 0.4, f"{val:.1f}", va="center", fontsize=8)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=8)

fig.suptitle("Constant Simulated Set: Every Tier Is Reachable (SIMULATED, not CMS data)",
             fontsize=13, fontweight="bold")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_09_constant_set_ladder.png"), dpi=150)
plt.show()
print("Saved: viz_09_constant_set_ladder.png")
