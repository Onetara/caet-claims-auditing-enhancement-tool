# step15_h2_test.py
# H2 Test: Intermittent Catheter Fraud Detection
# Requires: catheter_composite_scores.csv

import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# ── LOAD ─────────────────────────────────────────────────────────────
h2_results = pd.read_csv(str(BASE_DIR / "catheter_composite_scores.csv"))

# ── FILTER: HIGH RISK CATHETER STATES ONLY ──────────────────────────
HIGH_RISK_CATHETER_STATES = ["OK", "FL", "NY", "TX", "GA"]

filtered = h2_results[
    h2_results["state"].isin(HIGH_RISK_CATHETER_STATES)
]

print(f"Total catheter candidates        : {len(h2_results):,}")
print(f"In high-risk catheter states     : {len(filtered):,}")

# ── TEST POOL: ALL PROVIDERS IN THE HIGH-RISK STATES ─────────────────
test_sample = filtered
print(f"Testing full candidate pool: {len(test_sample)}")
results     = []

for _, row in test_sample.iterrows():

    results.append({
        "npi":             row["npi"],
        "provider_name":   row["provider_name"],
        "state":           row["state"],
        "bundling_score":  row["bundling_score"],
        "composite_score": row["composite_score"],
        "tier":            row["h2_tier"],
    })

# ── RESULTS ──────────────────────────────────────────────────────────
results_df       = pd.DataFrame(results)
high_or_critical = results_df[results_df["tier"].isin(["HIGH", "CRITICAL"])]
hit_rate         = len(high_or_critical) / len(results_df)

print(f"\n=== H2 TEST RESULTS ===")
print(results_df.to_string(index=False))

print(f"\n=== TIER DISTRIBUTION ===")
print(results_df["tier"].value_counts())

print(f"\nHigh or Critical : {len(high_or_critical)} / {len(results_df)}")
print(f"Hit Rate         : {hit_rate:.1%}")
print(f"Threshold        : >= 75%")

if hit_rate >= 0.75:
    print("Signals alone: target met")
else:
    print("Signals alone: below target (member calls not applied)")

# ── WITH MEMBER CALLS (run step16 first) ─────────────────────────────
calls_file = BASE_DIR / "h2_with_calls.csv"
if calls_file.exists():
    wc = pd.read_csv(str(calls_file))
    wc = wc[wc["state"].isin(HIGH_RISK_CATHETER_STATES)]
    after = wc[wc["updated_tier"].isin(["HIGH", "CRITICAL"])]
    print("\n=== WITH MEMBER CALLS (same test pool) ===")
    print(wc["updated_tier"].value_counts())
    print(f"High or Critical : {len(after)} / {len(wc)}")
    print(f"Hit Rate         : {len(after) / len(wc):.1%}  (signals alone: {hit_rate:.1%})")
else:
    print("\nNo h2_with_calls.csv found: run step16 for the with-calls comparison.")

# ── SAVE ─────────────────────────────────────────────────────────────
results_df.to_csv(str(BASE_DIR / "h2_test_results.csv"), index=False)
print("\nSaved: h2_test_results.csv")