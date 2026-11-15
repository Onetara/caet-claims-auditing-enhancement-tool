# viz_02_h1_score_distribution.py
# H1 Composite Score Histogram with Threshold Lines
# Input: h1_composite_results.csv

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent  # project root, holds the shared CSVs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "h1_composite_results.csv"))

# ── CHART ────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 5))
plt.hist(df["composite_score"], bins=50, color="steelblue", edgecolor="black")

plt.axvline(40, color="yellow", linestyle="--", linewidth=2, label="MEDIUM threshold (40)")
plt.axvline(60, color="orange", linestyle="--", linewidth=2, label="HIGH threshold (60)")
plt.axvline(80, color="red", linestyle="--", linewidth=2, label="CRITICAL threshold (80)")

plt.title("H1 General DME: Composite Score Distribution", fontsize=14, fontweight="bold")
plt.xlabel("Composite Score (0-100)")
plt.ylabel("Number of Providers")
plt.legend()

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_02_h1_score_distribution.png"), dpi=150)
plt.show()
print("Saved: viz_02_h1_score_distribution.png")