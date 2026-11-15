# step16_member_call_integration.py
# Simulates member call data and applies it to provider risk scores
# Requires: h1_composite_results.csv, catheter_composite_scores.csv

import pandas as pd
from datetime import datetime

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# ── CREATE SIMULATED MEMBER CALLS CSV ────────────────────────────────
# These represent calls a CSR would log in the call center system
# In production this file would come from the real call center database

simulated_calls = [
    # Original demo: general DME provider
    {"call_id": "CALL-2024-001", "member_id": "MBR-9900123", "provider_npi": 1003000399,
     "call_reason_code": "NEVER_RECEIVED_VALIDATED", "call_timestamp": "2024-06-15 14:32:00"},
    {"call_id": "CALL-2024-002", "member_id": "MBR-9900456", "provider_npi": 1003000399,
     "call_reason_code": "WRONG_ITEM_VALIDATED", "call_timestamp": "2024-06-20 10:15:00"},
    {"call_id": "CALL-2024-003", "member_id": "MBR-9900789", "provider_npi": 1003000399,
     "call_reason_code": "NO_CONSENT_VALIDATED", "call_timestamp": "2024-06-25 09:45:00"},
 
    # High-severity group: 180 Medical Inc (first 3 of 5 calls)
    {"call_id": "CALL-2024-004", "member_id": "MBR-4401987", "provider_npi": 1639160708,
     "call_reason_code": "NO_DIAGNOSIS_MATCH_VALIDATED", "call_timestamp": "2024-08-02 10:15:00"},
    {"call_id": "CALL-2024-005", "member_id": "MBR-4407741", "provider_npi": 1639160708,
     "call_reason_code": "WRONG_ITEM_VALIDATED", "call_timestamp": "2024-08-09 14:45:00"},
    {"call_id": "CALL-2024-006", "member_id": "MBR-4409002", "provider_npi": 1639160708,
     "call_reason_code": "RENTAL_NOT_RETURNED_VALIDATED", "call_timestamp": "2024-08-15 11:30:00"},
 
    # Medium-severity group (3 calls each)
    {"call_id": "CALL-2024-007", "member_id": "MBR-5501001", "provider_npi": 1972711968,
     "call_reason_code": "NO_DIAGNOSIS_MATCH_VALIDATED", "call_timestamp": "2024-09-01 09:00:00"},
    {"call_id": "CALL-2024-008", "member_id": "MBR-5501002", "provider_npi": 1972711968,
     "call_reason_code": "NO_CONSENT_VALIDATED", "call_timestamp": "2024-09-02 09:00:00"},
    {"call_id": "CALL-2024-009", "member_id": "MBR-5501003", "provider_npi": 1972711968,
     "call_reason_code": "WRONG_ITEM_VALIDATED", "call_timestamp": "2024-09-03 09:00:00"},
 
    {"call_id": "CALL-2024-010", "member_id": "MBR-5502001", "provider_npi": 1720196983,
     "call_reason_code": "NO_DIAGNOSIS_MATCH_VALIDATED", "call_timestamp": "2024-09-04 09:00:00"},
    {"call_id": "CALL-2024-011", "member_id": "MBR-5502002", "provider_npi": 1720196983,
     "call_reason_code": "NEVER_RECEIVED_VALIDATED", "call_timestamp": "2024-09-05 09:00:00"},
    {"call_id": "CALL-2024-012", "member_id": "MBR-5502003", "provider_npi": 1720196983,
     "call_reason_code": "RENTAL_NOT_RETURNED_VALIDATED", "call_timestamp": "2024-09-06 09:00:00"},
 
    {"call_id": "CALL-2024-013", "member_id": "MBR-5503001", "provider_npi": 1124201629,
     "call_reason_code": "NO_CONSENT_VALIDATED", "call_timestamp": "2024-09-07 09:00:00"},
    {"call_id": "CALL-2024-014", "member_id": "MBR-5503002", "provider_npi": 1124201629,
     "call_reason_code": "WRONG_ITEM_VALIDATED", "call_timestamp": "2024-09-08 09:00:00"},
    {"call_id": "CALL-2024-015", "member_id": "MBR-5503003", "provider_npi": 1124201629,
     "call_reason_code": "NEVER_RECEIVED_VALIDATED", "call_timestamp": "2024-09-09 09:00:00"},
 
    # High-severity group: 180 Medical Inc (remaining 2 of 5 calls)
    {"call_id": "CALL-2024-016", "member_id": "MBR-4409500", "provider_npi": 1639160708,
     "call_reason_code": "NO_CONSENT_VALIDATED", "call_timestamp": "2024-09-10 09:00:00"},
    {"call_id": "CALL-2024-017", "member_id": "MBR-4409600", "provider_npi": 1639160708,
     "call_reason_code": "NEVER_RECEIVED_VALIDATED", "call_timestamp": "2024-09-11 09:00:00"},
 
    # High-severity group: Byram Healthcare Centers (GA), 5 calls
    {"call_id": "CALL-2024-018", "member_id": "MBR-5504001", "provider_npi": 1023063641,
     "call_reason_code": "NO_DIAGNOSIS_MATCH_VALIDATED", "call_timestamp": "2024-09-12 09:00:00"},
    {"call_id": "CALL-2024-019", "member_id": "MBR-5504002", "provider_npi": 1023063641,
     "call_reason_code": "NO_CONSENT_VALIDATED", "call_timestamp": "2024-09-13 09:00:00"},
    {"call_id": "CALL-2024-020", "member_id": "MBR-5504003", "provider_npi": 1023063641,
     "call_reason_code": "WRONG_ITEM_VALIDATED", "call_timestamp": "2024-09-14 09:00:00"},
    {"call_id": "CALL-2024-021", "member_id": "MBR-5504004", "provider_npi": 1023063641,
     "call_reason_code": "NEVER_RECEIVED_VALIDATED", "call_timestamp": "2024-09-15 09:00:00"},
    {"call_id": "CALL-2024-022", "member_id": "MBR-5504005", "provider_npi": 1023063641,
     "call_reason_code": "RENTAL_NOT_RETURNED_VALIDATED", "call_timestamp": "2024-09-16 09:00:00"},
 
    # High-severity group: Degc Enterprises, 5 calls
    {"call_id": "CALL-2024-023", "member_id": "MBR-5505001", "provider_npi": 1295827780,
     "call_reason_code": "NO_DIAGNOSIS_MATCH_VALIDATED", "call_timestamp": "2024-09-17 09:00:00"},
    {"call_id": "CALL-2024-024", "member_id": "MBR-5505002", "provider_npi": 1295827780,
     "call_reason_code": "NO_CONSENT_VALIDATED", "call_timestamp": "2024-09-18 09:00:00"},
    {"call_id": "CALL-2024-025", "member_id": "MBR-5505003", "provider_npi": 1295827780,
     "call_reason_code": "WRONG_ITEM_VALIDATED", "call_timestamp": "2024-09-19 09:00:00"},
    {"call_id": "CALL-2024-026", "member_id": "MBR-5505004", "provider_npi": 1295827780,
     "call_reason_code": "NEVER_RECEIVED_VALIDATED", "call_timestamp": "2024-09-20 09:00:00"},
    {"call_id": "CALL-2024-027", "member_id": "MBR-5505005", "provider_npi": 1295827780,
     "call_reason_code": "RENTAL_NOT_RETURNED_VALIDATED", "call_timestamp": "2024-09-21 09:00:00"},
 
    # Low-severity group (1 call each)
    {"call_id": "CALL-2024-028", "member_id": "MBR-5506001", "provider_npi": 1366440968,
     "call_reason_code": "NO_DIAGNOSIS_MATCH_VALIDATED", "call_timestamp": "2024-09-22 09:00:00"},
    {"call_id": "CALL-2024-029", "member_id": "MBR-5507001", "provider_npi": 1093711996,
     "call_reason_code": "NEVER_RECEIVED_VALIDATED", "call_timestamp": "2024-09-23 09:00:00"},
    {"call_id": "CALL-2024-030", "member_id": "MBR-5508001", "provider_npi": 1699767061,
     "call_reason_code": "WRONG_ITEM_VALIDATED", "call_timestamp": "2024-09-24 09:00:00"},
]

calls_df = pd.DataFrame(simulated_calls)
calls_df.to_csv(
    str(BASE_DIR / "member_calls.csv"),
    index=False
)
print("Saved: member_calls.csv")
print(calls_df.to_string(index=False))

# ── CALL REASON WEIGHTS (from Step 8 scorer) ─────────────────────────
CALL_REASON_WEIGHTS = {
    "NO_DIAGNOSIS_MATCH_VALIDATED":  60,
    "NO_CONSENT_VALIDATED":          55,
    "NEVER_RECEIVED_VALIDATED":      50,
    "WRONG_ITEM_VALIDATED":          40,
    "RENTAL_NOT_RETURNED_VALIDATED": 40,
}

# ── COMPUTE MEMBER CALL SCORE PER NPI ────────────────────────────────
def member_call_score(npi_calls):
    score            = 0
    distinct_members = npi_calls["member_id"].nunique()

    for _, call in npi_calls.iterrows():
        weight = CALL_REASON_WEIGHTS.get(call["call_reason_code"], 20)
        score += weight

    if distinct_members >= 3:
        score *= 1.50
    elif distinct_members == 2:
        score *= 1.25

    return min(score, 100)

# ── APPLY CALL SCORES TO EACH FLAGGED NPI ────────────────────────────
npi_call_scores = []

for npi, group in calls_df.groupby("provider_npi"):
    call_score       = member_call_score(group)
    distinct_members = group["member_id"].nunique()
    call_count       = len(group)

    npi_call_scores.append({
        "provider_npi":    npi,
        "call_count":      call_count,
        "distinct_members": distinct_members,
        "member_call_score": round(call_score, 2),
    })

call_scores_df = pd.DataFrame(npi_call_scores)
print(f"\n=== MEMBER CALL SCORES BY NPI ===")
print(call_scores_df.to_string(index=False))

# ── MERGE CALL SCORES INTO H1 RESULTS ────────────────────────────────
h1 = pd.read_csv(str(BASE_DIR / "h1_composite_results.csv"))
h1 = h1.merge(call_scores_df, left_on="Suplr_NPI", right_on="provider_npi", how="left")
h1["member_call_score"]  = h1["member_call_score"].fillna(0)

# Recalculate composite with real member call score
h1["composite_with_calls"] = (
    h1["member_call_score"] * 0.35 +
    h1["upcoding_max"]      * 0.25 +
    h1["volume_max"]        * 0.20 +
    h1["rental_max"]        * 0.10 +
    h1["geo_max"]           * 0.10
).round(2)

def tier(score):
    if   score >= 80: return "CRITICAL"
    elif score >= 60: return "HIGH"
    elif score >= 40: return "MEDIUM"
    else:             return "LOW"

h1["updated_tier"] = h1["composite_with_calls"].apply(tier)

# Show only providers that were affected by calls
affected = h1[h1["member_call_score"] > 0][[
    "Suplr_NPI", "member_call_score", "composite_score",
    "composite_with_calls", "h1_tier", "updated_tier"
]]

print(f"\n=== PROVIDERS UPDATED BY MEMBER CALLS ===")
print(affected.to_string(index=False))

# ── MERGE CALL SCORES INTO H2 RESULTS ────────────────────────────────
h2 = pd.read_csv(str(BASE_DIR / "catheter_composite_scores.csv"))
if "member_call_score" in h2.columns:
    h2 = h2.drop(columns=["member_call_score"])
h2 = h2.merge(call_scores_df, left_on="npi", right_on="provider_npi", how="left")
h2["member_call_score"] = h2["member_call_score"].fillna(0)

h2["composite_with_calls"] = (
    h2["bundling_score"]    * 0.40 +
    h2["member_call_score"] * 0.25 +
    h2["volume_score"]      * 0.15 +
    h2["upcoding_score"]    * 0.10 +
    h2["geo_score"]         * 0.10
).round(2)

h2["updated_tier"] = h2["composite_with_calls"].apply(tier)

affected_h2 = h2[h2["member_call_score"] > 0][[
    "npi", "provider_name", "member_call_score",
    "composite_score", "composite_with_calls",
    "h2_tier", "updated_tier"
]]

print(f"\n=== CATHETER PROVIDERS UPDATED BY MEMBER CALLS ===")
print(affected_h2.to_string(index=False))

# ── SAVE ─────────────────────────────────────────────────────────────
h1.to_csv(str(BASE_DIR / "h1_with_calls.csv"), index=False)
h2.to_csv(str(BASE_DIR / "h2_with_calls.csv"), index=False)
print("\nSaved: h1_with_calls.csv")
print("Saved: h2_with_calls.csv")