# validate_caet.py
# Runs 4 checks against your real CSVs to confirm the code is doing what
# the outline says. Prints PASS/FAIL for each, no manual eyeballing needed.

import pandas as pd

from pathlib import Path
from caet_shared import call_reason_weight, apply_override_floor
BASE_DIR = Path(__file__).resolve().parent

BASE = str(BASE_DIR) + "/"

def check(label, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {label}" + (f": {detail}" if detail else ""))

print("=" * 70)
print("CHECK 1: ROW COUNTS")
print("=" * 70)

dme = pd.read_csv(BASE + "dme_with_signals.csv")
check("dme_with_signals.csv == 463,784 rows", len(dme) == 463784, f"actual: {len(dme):,}")

h1 = pd.read_csv(BASE + "h1_composite_results.csv")
check("h1_composite_results.csv == 59,592 rows", len(h1) == 59592, f"actual: {len(h1):,}")

catheter = pd.read_csv(BASE + "catheter_composite_scores.csv")
check("catheter_composite_scores.csv == 206 rows", len(catheter) == 206, f"actual: {len(catheter)}")

h2_test = pd.read_csv(BASE + "h2_test_results.csv")
check("h2_test_results.csv == 41 rows (post-fix)", len(h2_test) == 41, f"actual: {len(h2_test)}")

calls = pd.read_csv(BASE + "member_calls.csv")
check("member_calls.csv == 30 rows", len(calls) == 30, f"actual: {len(calls)}")

h1_wc = pd.read_csv(BASE + "h1_with_calls.csv")
check("h1_with_calls.csv row count matches h1_composite_results.csv",
      len(h1_wc) == len(h1), f"h1: {len(h1):,}, h1_with_calls: {len(h1_wc):,}")

h2_wc = pd.read_csv(BASE + "h2_with_calls.csv")
check("h2_with_calls.csv row count matches catheter_composite_scores.csv",
      len(h2_wc) == len(catheter), f"catheter: {len(catheter)}, h2_with_calls: {len(h2_wc)}")

print()
print("=" * 70)
print("CHECK 2: KNOWN EXAMPLES (hand-computed vs. actual file)")
print("=" * 70)

def expected_call_score(npi):
    rows = calls[calls["provider_npi"] == npi]
    raw = sum(call_reason_weight(r) for r in rows["call_reason_code"])
    n_distinct = rows["member_id"].nunique()
    mult = 1.5 if n_distinct >= 3 else (1.25 if n_distinct == 2 else 1.0)
    return min(raw * mult, 100)

known_npis = [1366440968, 1639160708, 1093711996, 1699767061]
for npi in known_npis:
    expected = expected_call_score(npi)
    actual_row = h1_wc[h1_wc["Suplr_NPI"] == npi]
    if actual_row.empty:
        actual_row = h2_wc[h2_wc["npi"] == npi]
        actual = actual_row["member_call_score"].values[0] if not actual_row.empty else None
    else:
        actual = actual_row["member_call_score"].values[0]
    check(f"NPI {npi} member_call_score", actual == expected,
          f"expected {expected}, got {actual}")

print()
print("=" * 70)
print("CHECK 3: COLUMN HANDOFF (no leftover merge-collision columns)")
print("=" * 70)

for name, df in [("h1_with_calls.csv", h1_wc), ("h2_with_calls.csv", h2_wc),
                  ("catheter_composite_scores.csv", catheter)]:
    bad_cols = [c for c in df.columns if c.endswith("_x") or c.endswith("_y")]
    check(f"{name} has no _x/_y duplicate columns", len(bad_cols) == 0, f"found: {bad_cols}")

print()
print("=" * 70)
print("CHECK 4: FORMULA RECONCILIATION (composite_with_calls, sample of 5)")
print("=" * 70)

sample_h1 = h1_wc[h1_wc["member_call_score"] > 0].head(5)
for _, row in sample_h1.iterrows():
    recomputed = round(
        row["member_call_score"] * 0.35 +
        row["upcoding_max"]      * 0.25 +
        row["volume_max"]        * 0.20 +
        row["rental_max"]        * 0.10 +
        row["geo_max"]           * 0.10, 2)
    check(f"H1 NPI {row['Suplr_NPI']} composite_with_calls reconciles",
          abs(recomputed - row["composite_with_calls"]) < 0.02,
          f"recomputed {recomputed}, file has {row['composite_with_calls']}")

sample_h2 = h2_wc[h2_wc["member_call_score"] > 0].head(5)
for _, row in sample_h2.iterrows():
    weighted = (
        row["bundling_score"]    * 0.40 +
        row["member_call_score"] * 0.25 +
        row["volume_score"]      * 0.15 +
        row["upcoding_score"]    * 0.10 +
        row["geo_score"]         * 0.10)
    recomputed = round(apply_override_floor(weighted, row["flags"], row["geo_score"]), 2)
    check(f"H2 NPI {row['npi']} composite_with_calls reconciles",
          abs(recomputed - row["composite_with_calls"]) < 0.02,
          f"recomputed {recomputed}, file has {row['composite_with_calls']}")

print()
print("Done.")
