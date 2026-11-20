# viz_12_h2_top10_calls.py
# Top 10 catheter suppliers: score before vs after simulated member calls
# Input: h2_with_calls.csv

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "CAET_tool"  # pipeline outputs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "h2_with_calls.csv"))
top = df.sort_values("composite_with_calls", ascending=False).head(10).reset_index(drop=True)
tier_colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "gold", "LOW": "green"}

# ── CHART ────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 6))
y = range(len(top))
ax.barh(y, top["composite_score"], height=0.38, color="lightgray", edgecolor="black", label="Before calls")
ax.barh([i + 0.4 for i in y], top["composite_with_calls"], height=0.38,
        color=top["updated_tier"].map(tier_colors), edgecolor="black", label="After calls (color = tier)")

for cut in (40, 60, 80):
    ax.axvline(cut, color="black", linestyle="--", linewidth=0.8)
for i, row in top.iterrows():
    tag = " (calls)" if row["member_call_score"] > 0 else ""
    ax.text(row["composite_with_calls"] + 1, i + 0.4, f"{row['composite_with_calls']:.1f}{tag}", va="center", fontsize=8)

ax.set_yticks([i + 0.2 for i in y])
ax.set_yticklabels([f"NPI {n} ({s})" for n, s in zip(top["npi"], top["state"])], fontsize=9)
ax.invert_yaxis()
ax.set_xlim(0, 100)
ax.set_xlabel("Composite Score (0-100); dashed lines = tier bands 40, 60, 80")
ax.set_title("H2 Catheter: Top 10 Suppliers, Before vs After Simulated Calls", fontsize=13, fontweight="bold")
ax.legend(loc="lower right")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_12_h2_top10_calls.png"), dpi=150)
plt.show()
print("Saved: viz_12_h2_top10_calls.png")
