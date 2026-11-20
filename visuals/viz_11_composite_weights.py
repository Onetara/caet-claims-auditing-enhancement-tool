# viz_11_composite_weights.py
# Composite weights used by H1 and H2 (read from caet_shared)

import sys
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR.parent / "CAET_tool"))
from caet_shared import H1_WEIGHTS, H2_WEIGHTS

# ── CHART ────────────────────────────────────────────────────────────
labels = {
    "member_call": "Member calls", "upcoding": "Upcoding", "volume": "Volume",
    "rental": "Rental", "geographic": "Geography",
    "catheter_bundling": "Catheter bundling", "units": "Units per claim",
}
palette = {
    "Member calls": "crimson", "Upcoding": "steelblue", "Volume": "seagreen",
    "Rental": "goldenrod", "Geography": "slategray",
    "Catheter bundling": "mediumpurple", "Units per claim": "teal",
}

fig, ax = plt.subplots(figsize=(11, 3.8))
for row, (name, weights) in enumerate([("H1 General DME", H1_WEIGHTS), ("H2 Catheters", H2_WEIGHTS)]):
    left = 0.0
    for key, val in weights.items():
        lab = labels[key]
        ax.barh(row, val, left=left, color=palette[lab], edgecolor="black")
        ax.text(left + val / 2, row, f"{lab}\n{val:.2f}", ha="center", va="center", fontsize=8, color="white", fontweight="bold")
        left += val

ax.set_yticks([0, 1])
ax.set_yticklabels(["H1 General DME", "H2 Catheters"])
ax.invert_yaxis()
ax.set_xlim(0, 1)
ax.set_xlabel("Share of composite score (each row sums to 1.00)")
ax.set_title("Composite Score Weights", fontsize=13, fontweight="bold")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_11_composite_weights.png"), dpi=150)
plt.show()
print("Saved: viz_11_composite_weights.png")
