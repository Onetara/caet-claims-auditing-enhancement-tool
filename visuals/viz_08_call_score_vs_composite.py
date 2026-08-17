# viz_08_call_score_vs_composite.py
# Member Call Score vs Composite Score — Scatter Plot
# Input: h1_with_calls.csv

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent  # .../data _visualization
DATA_DIR = BASE_DIR.parent  # project root, holds the shared CSVs
# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "h1_with_calls.csv"))

# ── COLOR BY TIER ────────────────────────────────────────────────────
tier_colors = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow", "LOW": "green"}
colors = df["updated_tier"].map(tier_colors)
np.random.seed(42)
zero_mask = df["member_call_score"] == 0
jittered_x = df["member_call_score"].copy()
jittered_x[zero_mask] = np.random.uniform(-2, 2, zero_mask.sum())
# ── CHART ────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 6))
plt.scatter(
    jittered_x[zero_mask],
    df["composite_with_calls"][zero_mask],
    c=colors[zero_mask],
    edgecolor="black",
    linewidth=0.3,
    s=25,
    alpha=0.25
)
plt.scatter(
    jittered_x[~zero_mask],
    df["composite_with_calls"][~zero_mask],
    c=colors[~zero_mask],
    edgecolor="black",
    s=70,
    alpha=0.9
)

plt.axhline(40, color="yellow", linestyle="--", linewidth=1, alpha=0.6)
plt.axhline(60, color="orange", linestyle="--", linewidth=1, alpha=0.6)

plt.title("Member Call Score vs Composite Score", fontsize=13, fontweight="bold")
plt.xlabel("Member Call Score (0-100)")
plt.ylabel("Composite Score With Calls (0-100)")

# Legend
for tier, color in tier_colors.items():
    plt.scatter([], [], c=color, edgecolor="black", label=tier)
plt.legend(title="Risk Tier")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_08_call_score_vs_composite.png"), dpi=150)
plt.show()
print("Saved: viz_08_call_score_vs_composite.png")