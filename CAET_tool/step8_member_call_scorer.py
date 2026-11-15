import pandas as pd

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

# Load the foundation file
df = pd.read_csv(str(BASE_DIR / "dme_with_signals.csv"))

# Step 8: Member Call Scorer (PLACEHOLDER MODE: v2.8)
# Scope: subjective signals only. Claim-AI signals excluded per CAET scope.
CALL_WEIGHTS = {
    "no_diagnosis_match_reported_count": 60,  # NEW v2.8: phantom billing
    "no_consent_count":                  55,
    "never_received_count":              50,
    "wrong_item_count":                  40,
    "rental_not_returned_count":         40
}

# Initialize all call columns to 0 (placeholder, real data plugs in here)
for col in CALL_WEIGHTS.keys():
    df[col] = 0

# Also initialize a distinct-member counter (used for the multiplier)
df["distinct_members_reporting"] = 0

# Build the scorer
def member_call_score(row):
    # Base score = sum of (count × weight) for each call type
    base = 0
    for col, weight in CALL_WEIGHTS.items():
        base += row[col] * weight

    # Apply distinct-member multiplier (pattern amplifier)
    distinct = row["distinct_members_reporting"]
    if distinct >= 3:
        base *= 1.50  # 3+ members = clear pattern
    elif distinct == 2:
        base *= 1.25  # 2 members = corroborated signal
    # 1 member = no multiplier (could be misunderstanding)

    return min(base, 100)  # cap at 100

df["member_call_score"] = df.apply(member_call_score, axis=1)

# Tag the tier
def member_call_tier(score):
    if score >= 70:
        return "CRITICAL_CALLS"
    elif score >= 40:
        return "ELEVATED_CALLS"
    elif score > 0:
        return "LOW_CALLS"
    else:
        return "NO_CALLS"

df["member_call_tier"] = df["member_call_score"].apply(member_call_tier)

# Verify
print("=== Call columns added (all zeros for now) ===")
print(df[list(CALL_WEIGHTS.keys()) + ["distinct_members_reporting"]].head(3))

print("\n=== Tier counts (expected: all NO_CALLS) ===")
print(df["member_call_tier"].value_counts())

print("\n=== Score stats (expected: all zeros) ===")
print(df["member_call_score"].describe())

print("\n✅ Placeholder ready (v2.8, 5 member-reported signals).")
print("To activate: populate the 5 call count columns + distinct_members_reporting with real data, then re-run.")