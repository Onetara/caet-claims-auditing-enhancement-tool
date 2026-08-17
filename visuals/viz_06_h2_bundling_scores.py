# viz_06_h2_bundling_scores.py
# Catheter Bundling Score Distribution
# Input: catheter_composite_scores.csv

import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent  # .../data _visualization
DATA_DIR = BASE_DIR.parent  # project root, holds the shared CSVs

# ── LOAD ─────────────────────────────────────────────────────────────
df = pd.read_csv(str(DATA_DIR / "catheter_composite_scores.csv"))

# ── CHART ────────────────────────────────────────────────────────────
plt.figure(figsize=(9, 5))
plt.hist(df["bundling_score"], bins=20, color="mediumpurple", edgecolor="black")

plt.title("H2 Catheter Providers — Bundling Score Distribution", fontsize=13, fontweight="bold")
plt.xlabel("Bundling Score (0-100)")
plt.ylabel("Number of Providers")

# ── SAVE ─────────────────────────────────────────────────────────────
plt.tight_layout()
plt.savefig(str(BASE_DIR / "viz_06_h2_bundling_scores.png"), dpi=150)
plt.show()
print("Saved: viz_06_h2_bundling_scores.png")