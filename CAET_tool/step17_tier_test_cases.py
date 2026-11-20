# step17_tier_test_cases.py
# CONSTANT SIMULATED SET: fixed fake suppliers, two per tier, for H1 and H2.
# Purpose: prove the scoring rules can reach every tier (LOW, MEDIUM, HIGH, CRITICAL).
# These are not CMS suppliers and never mix with the CMS results.
# Each case lists its signal scores (0 to 100) and the tier it should produce.

import pandas as pd
from pathlib import Path
from caet_shared import h1_composite, h2_composite, tier

BASE_DIR = Path(__file__).resolve().parent

# ── H1 CASES: signals alone, then with calls ─────────────────────────
# name, upcoding, volume, rental, geo, call score, expected tier
H1_CASES = [
    ("SIM-H1-LOW-1",      0,   0,   0,  0,   0, "LOW"),
    ("SIM-H1-LOW-2",     60,   0,   0, 30,   0, "LOW"),
    ("SIM-H1-MEDIUM-1", 100, 100,   0, 45,   0, "MEDIUM"),
    ("SIM-H1-MEDIUM-2",  60,  60,   0, 30,  60, "MEDIUM"),
    ("SIM-H1-HIGH-1",   100, 100, 100, 65,   0, "HIGH"),
    ("SIM-H1-HIGH-2",    60,  60,   0, 30, 100, "HIGH"),
    ("SIM-H1-CRITICAL-1", 100, 100, 100, 65, 100, "CRITICAL"),
    ("SIM-H1-CRITICAL-2", 100, 100,  60, 45, 100, "CRITICAL"),
]

# ── H2 CASES: bundling, units, volume, upcoding, geo, calls, flags ───
# The flags text drives the override floor, as in step12.
EXTREME = "EXTREME_CATHETER_BUNDLING: 15 codes | DUAL_CATHETER_TYPE: A4351 + A4352 billed together"
HIGH_B  = "HIGH_CATHETER_BUNDLING: 12 codes | DUAL_CATHETER_TYPE: A4351 + A4352 billed together"
H2_CASES = [
    ("SIM-H2-LOW-1",      0,   0,   0,   0,  0,   0, "",      "LOW"),
    ("SIM-H2-LOW-2",     35,   0,   0,  30,  0,   0, "",      "LOW"),
    ("SIM-H2-MEDIUM-1",  65,  60,  40,  50, 30,   0, HIGH_B,  "MEDIUM"),
    ("SIM-H2-MEDIUM-2",  35,  60,  40,  50, 30, 100, "",      "MEDIUM"),
    ("SIM-H2-HIGH-1",    85, 100,  60,  80, 30,   0, EXTREME, "HIGH"),
    ("SIM-H2-HIGH-2",    65,  60,  40,  50, 30, 100, "",      "HIGH"),
    ("SIM-H2-CRITICAL-1", 100, 100, 100, 100, 40, 100, EXTREME, "CRITICAL"),
    ("SIM-H2-CRITICAL-2", 100, 100,  20,  80, 40, 100, EXTREME, "CRITICAL"),
]

rows = []

for name, upc, vol, rent, geo, calls, expected in H1_CASES:
    score = round(h1_composite(upc, vol, rent, geo, calls), 2)
    base  = round(h1_composite(upc, vol, rent, geo, 0), 2)
    rows.append({"hypothesis": "H1", "case": name, "calls": calls,
                 "composite_no_calls": base, "tier_no_calls": tier(base),
                 "composite": score, "expected": expected, "actual": tier(score)})

for name, bund, units, vol, upc, geo, calls, flags, expected in H2_CASES:
    score = round(h2_composite(bund, units, vol, upc, geo, calls, flags), 2)
    base  = round(h2_composite(bund, units, vol, upc, geo, 0, flags), 2)
    rows.append({"hypothesis": "H2", "case": name, "calls": calls,
                 "composite_no_calls": base, "tier_no_calls": tier(base),
                 "composite": score, "expected": expected, "actual": tier(score)})

results = pd.DataFrame(rows)
results["match"] = results["expected"] == results["actual"]

print("=== CONSTANT SIMULATED SET: EXPECTED VS ACTUAL TIER ===")
print(results.to_string(index=False))
print(f"\nCases matching expected tier: {int(results['match'].sum())} / {len(results)}")

results.to_csv(str(BASE_DIR / "tier_test_results.csv"), index=False)
print("Saved: tier_test_results.csv")
