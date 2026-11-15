# select_test_candidates.py

import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

BASE = str(BASE_DIR) + "/"

# ── LOW candidates: from H1 (pre-call; nearly all 59,592 are LOW) ───
h1 = pd.read_csv(BASE + "h1_composite_results.csv")
low_candidates = h1.sort_values("composite_score", ascending=False)
print("=== LOW candidates (H1, highest composite first, closest to MEDIUM) ===")
print(low_candidates[["Suplr_NPI", "composite_score"]].head(12).to_string(index=False))

# ── MEDIUM and HIGH candidates: from H2 (pre-call; H1 has none) ────
h2 = pd.read_csv(BASE + "catheter_composite_scores.csv")

medium_candidates = h2[h2["h2_tier"] == "MEDIUM"].sort_values("composite_score", ascending=False)
print("\n=== MEDIUM candidates (H2) ===")
print(medium_candidates[["npi", "provider_name", "composite_score"]].head(12).to_string(index=False))

high_candidates = h2[h2["h2_tier"] == "HIGH"].sort_values("composite_score", ascending=False)
print("\n=== HIGH candidates (H2) ===")
print(high_candidates[["npi", "provider_name", "composite_score"]].head(12).to_string(index=False))