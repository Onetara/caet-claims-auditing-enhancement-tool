# caet_shared.py
# Shared scoring parameters and rules used by several steps.
# One place to change a value so the steps and the validation stay in sync.

import warnings

# ── MEMBER CALL WEIGHTS ──────────────────────────────────────────────
# Points per validated call, by call reason code
CALL_REASON_WEIGHTS = {
    "NO_DIAGNOSIS_MATCH_VALIDATED":  60,   # phantom billing
    "NO_CONSENT_VALIDATED":          55,
    "NEVER_RECEIVED_VALIDATED":      50,
    "WRONG_ITEM_VALIDATED":          40,
    "RENTAL_NOT_RETURNED_VALIDATED": 40,
}

# Column in the call-count placeholder (step8) for each call reason
CALL_COUNT_COLUMNS = {
    "NO_DIAGNOSIS_MATCH_VALIDATED":  "no_diagnosis_match_reported_count",
    "NO_CONSENT_VALIDATED":          "no_consent_count",
    "NEVER_RECEIVED_VALIDATED":      "never_received_count",
    "WRONG_ITEM_VALIDATED":          "wrong_item_count",
    "RENTAL_NOT_RETURNED_VALIDATED": "rental_not_returned_count",
}

# Weight used when a call reason code is not in the table above
DEFAULT_CALL_WEIGHT = 20


def call_reason_weight(reason_code):
    """Weight for one call reason code; warns if the code is unknown."""
    if reason_code not in CALL_REASON_WEIGHTS:
        warnings.warn(
            f"Unknown call reason code '{reason_code}': "
            f"using default weight {DEFAULT_CALL_WEIGHT}"
        )
        return DEFAULT_CALL_WEIGHT
    return CALL_REASON_WEIGHTS[reason_code]


# ── H2 CATHETER CUTOFFS ──────────────────────────────────────────────
# Catheter-specific cutoffs (current values). step4 prints the catheter
# percentiles so each cutoff can be matched to a percentile.
CATH_CHARGE_MAX_CUTOFF  = 4.14   # highest charge-to-allowed ratio of a provider
CATH_CHARGE_MEAN_CUTOFF = 1.52   # average charge-to-allowed ratio of a provider
CATH_CPB_MAX_CUTOFF     = 9.12   # highest claims per beneficiary of a provider
CATH_CPB_MEAN_CUTOFF    = 5.35   # average claims per beneficiary of a provider
CATH_TOTAL_CLAIMS_CUTOFF = 50000 # total claims of a provider


# ── H2 COMPOSITE WEIGHTS ─────────────────────────────────────────────
# Single source for step13, step16 and validate_caet. Must sum to 1.00.
H2_WEIGHTS = {
    "catheter_bundling": 0.25,   # variety of catheter codes billed
    "units":             0.15,   # units per claim vs the same code's peers
    "member_call":       0.25,   # member complaints
    "volume":            0.15,   # claims per beneficiary, total claims
    "upcoding":          0.10,   # charge-to-allowed ratio
    "geographic":        0.10,   # high-risk state
}

# Units signal: units (services) per claim, compared within the same HCPCS code.
UNITS_MIN_ROWS = 20   # a code needs this many supplier rows to set its own cutoffs


# ── H2 OVERRIDE FLOOR ────────────────────────────────────────────────
# Minimum composite score for catheter providers with strong bundling flags.
# Used by step13 (baseline) and step16 (with member calls).
FLOOR_EXTREME_BUNDLING = 65.0   # 14+ catheter codes and geo score >= 30 (HIGH)
FLOOR_HIGH_BUNDLING    = 42.0   # HIGH bundling plus at least one more flag (MEDIUM)


def apply_override_floor(composite, flags, geo_score):
    """Raise a catheter composite score to its minimum, if the flags qualify."""
    flags = str(flags)
    if "EXTREME_CATHETER_BUNDLING" in flags and geo_score >= 30:
        return max(composite, FLOOR_EXTREME_BUNDLING)
    if flags.count("|") >= 1 and "HIGH_CATHETER_BUNDLING" in flags:
        return max(composite, FLOOR_HIGH_BUNDLING)
    return composite
