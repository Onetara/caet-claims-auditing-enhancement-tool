# step10_h1_test.py
# H1 Test: General DME Fraud Detection (full population, no member calls)

import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# ── LOAD ────────────────────────────────────────────────────────────
h1_results = pd.read_csv(str(BASE_DIR / "h1_composite_results.csv"))

# ── TEST POPULATION: ALL PROVIDERS ───────────────────────────────────
results_df = h1_results.rename(columns={
    "Suplr_NPI":       "npi",
    "composite_score": "composite",
    "h1_tier":         "tier"
})[["npi", "composite", "tier"]]

print(f"Providers tested (full population): {len(results_df):,}")

# ── RESULTS ──────────────────────────────────────────────────────────
high_or_critical = results_df[results_df["tier"].isin(["HIGH", "CRITICAL"])]
hit_rate         = len(high_or_critical) / len(results_df)

print("\n=== TIER DISTRIBUTION ===")
print(results_df["tier"].value_counts())

print(f"\nHigh or Critical : {len(high_or_critical):,} / {len(results_df):,}")
print(f"Hit Rate         : {hit_rate:.1%}")
print("Threshold        : >= 70%")

if hit_rate >= 0.70:
    print("H1 PASSED")
else:
    print("H1 FAILED: review scorer weights")

# ── SAVE ─────────────────────────────────────────────────────────────
results_df.to_csv(str(BASE_DIR / "h1_test_results.csv"), index=False)
print("\nSaved: h1_test_results.csv")
