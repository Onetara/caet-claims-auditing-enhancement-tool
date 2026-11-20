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
    print("Signals alone: target met")
else:
    print("Signals alone: below target (member calls not applied)")

# ── WITH MEMBER CALLS (run step16 first) ─────────────────────────────
calls_file = BASE_DIR / "h1_with_calls.csv"
if calls_file.exists():
    with_calls = pd.read_csv(str(calls_file))
    after = with_calls[with_calls["updated_tier"].isin(["HIGH", "CRITICAL"])]
    after_rate = len(after) / len(with_calls)
    print("\n=== WITH MEMBER CALLS ===")
    print(with_calls["updated_tier"].value_counts())
    print(f"High or Critical : {len(after):,} / {len(with_calls):,}")
    print(f"Hit Rate         : {after_rate:.1%}  (baseline: {hit_rate:.1%})")
else:
    print("\nNo h1_with_calls.csv found: run step16 for the with-calls comparison.")

# ── SAVE ─────────────────────────────────────────────────────────────
results_df.to_csv(str(BASE_DIR / "h1_test_results.csv"), index=False)
print("\nSaved: h1_test_results.csv")
