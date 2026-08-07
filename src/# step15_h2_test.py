# step15_h2_test.py
# H2 Test — Intermittent Catheter Fraud Detection
# Requires: catheter_composite_scores.csv

import pandas as pd

# ── LOAD ─────────────────────────────────────────────────────────────
h2_results = pd.read_csv("catheter_composite_scores.csv")

# ── FILTER — HIGH RISK CATHETER STATES ONLY ──────────────────────────
HIGH_RISK_CATHETER_STATES = ["OK", "FL", "NY", "TX", "GA"]

filtered = h2_results[
    h2_results["state"].isin(HIGH_RISK_CATHETER_STATES)
]

print(f"Total catheter candidates        : {len(h2_results):,}")
print(f"In high-risk catheter states     : {len(filtered):,}")

# ── TEST SAMPLE OF 41 ────────────────────────────────────────────────
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
    print("H2 PASSED")
else:
    print("H2 FAILED — review catheter scorer weights")

# ── SAVE ─────────────────────────────────────────────────────────────
results_df.to_csv("h2_test_results.csv", index=False)
print("\nSaved: h2_test_results.csv")