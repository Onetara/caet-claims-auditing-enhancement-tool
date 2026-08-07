# step10_h1_test.py
# H1 Test — General DME Fraud Detection

import pandas as pd

# ── LOAD ────────────────────────────────────────────────────────────
df         = pd.read_csv("dme_with_signals.csv")
h1_results = pd.read_csv("h1_composite_results.csv")

# ── TEST SAMPLE ──────────────────────────────────────────────────────
candidate_npis = h1_results["Suplr_NPI"].unique()
test_sample    = candidate_npis[:20]
results        = []

print(f"Candidate providers meeting both H1 thresholds: {len(candidate_npis):,}")

# ── LOOP ─────────────────────────────────────────────────────────────
for npi in test_sample:

    row = h1_results[h1_results["Suplr_NPI"] == npi]
    if row.empty:
        continue

    composite = row["composite_score"].values[0]
    tier_val  = row["h1_tier"].values[0]

    results.append({
        "npi":       npi,
        "composite": composite,
        "tier":      tier_val
    })

# ── RESULTS ──────────────────────────────────────────────────────────
results_df       = pd.DataFrame(results)
high_or_critical = results_df[results_df["tier"].isin(["HIGH", "CRITICAL"])]
hit_rate         = len(high_or_critical) / len(results_df)

print(results_df.to_string(index=False))
print(f"\nHigh or Critical : {len(high_or_critical)} / {len(results_df)}")
print(f"Hit Rate         : {hit_rate:.1%}")

if hit_rate >= 0.70:
    print("H1 PASSED")
else:
    print("H1 FAILED — review scorer weights")

# ── SAVE ─────────────────────────────────────────────────────────────
results_df.to_csv("h1_test_results.csv", index=False)
print("\nSaved: h1_test_results.csv")