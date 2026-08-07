import pandas as pd
df = pd.read_csv("master_set_cms_medicare_dme_2023.csv")
print(df.shape)
print(df.head())
print(df.columns.tolist())
print(df.dtypes)
print(df.isnull().sum())
# Convert key number columns to numeric (forces blanks to NaN)
num_cols = [
    "Avg_Suplr_Sbmtd_Chrg",
    "Avg_Suplr_Mdcr_Alowd_Amt",
    "Avg_Suplr_Mdcr_Pymt_Amt",
    "Avg_Suplr_Mdcr_Stdzd_Amt",
    "Tot_Suplr_Clms",
    "Tot_Suplr_Benes"
]

for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Confirm cleaning worked
print(df[num_cols].dtypes)
print(df[num_cols].isnull().sum())
# Step 4: Charge-to-Allowed Ratio
df["charge_to_allowed_ratio"] = df["Avg_Suplr_Sbmtd_Chrg"] / df["Avg_Suplr_Mdcr_Alowd_Amt"]

# Verify
print(df[["Avg_Suplr_Sbmtd_Chrg", "Avg_Suplr_Mdcr_Alowd_Amt", "charge_to_allowed_ratio"]].head())
print(df["charge_to_allowed_ratio"].describe())
# Step 5: Claims per Beneficiary
df["claims_per_bene"] = df["Tot_Suplr_Clms"] / df["Tot_Suplr_Benes"]

# Verify
print(df[["Tot_Suplr_Clms", "Tot_Suplr_Benes", "claims_per_bene"]].head())
print(df["claims_per_bene"].describe())
# Step 6: Payment Delta
df["payment_delta"] = df["Avg_Suplr_Mdcr_Alowd_Amt"] - df["Avg_Suplr_Mdcr_Pymt_Amt"]

# Verify
print(df[["Avg_Suplr_Mdcr_Alowd_Amt", "Avg_Suplr_Mdcr_Pymt_Amt", "payment_delta"]].head())
print(df["payment_delta"].describe())
# Step 7: Geographic Standardization Delta
df["geo_standardization_delta"] = df["Avg_Suplr_Mdcr_Pymt_Amt"] - df["Avg_Suplr_Mdcr_Stdzd_Amt"]

# Verify
print(df[["Avg_Suplr_Mdcr_Pymt_Amt", "Avg_Suplr_Mdcr_Stdzd_Amt", "geo_standardization_delta"]].head())
print(df["geo_standardization_delta"].describe())
# Step 8a: Identify the HCPCS column name
print([c for c in df.columns if "HCPCS" in c.upper()])
# Step 8b: Tag each row with its fraud category
def tag_fraud_category(code):
    code = str(code).upper()
    if code.startswith(("K055", "A927", "E2103")):
        return "CGM"
    elif code.startswith("L"):
        return "ORTHOTIC"
    elif code.startswith(("E060", "E047")):
        return "PAP_CPAP"
    elif code.startswith("A6"):
        return "SURGICAL_DRESSING"
    elif code.startswith(("A435", "A434", "A433", "A510")):
        return "CATHETER"
    else:
        return "OTHER"

df["fraud_hcpcs_cat"] = df["HCPCS_Cd"].apply(tag_fraud_category)

# Verify
print(df["fraud_hcpcs_cat"].value_counts())
print(df[["HCPCS_Cd", "HCPCS_Desc", "fraud_hcpcs_cat"]].head(10))
# Step 9: Assign CMS improper payment rate as risk weight per category
risk_weights = {
    "SURGICAL_DRESSING": 0.576,
    "ORTHOTIC": 0.513,
    "CGM": 0.252,
    "CATHETER": 0.180,
    "PAP_CPAP": 0.125,
    "OTHER": 0.100
}

df["category_risk_weight"] = df["fraud_hcpcs_cat"].map(risk_weights)

# Verify
print(df[["HCPCS_Cd", "fraud_hcpcs_cat", "category_risk_weight"]].head(10))
print(df.groupby("fraud_hcpcs_cat")["category_risk_weight"].first())
# Step 10: Verify all derived columns look correct
print("=== Shape ===")
print(df.shape)

print("\n=== All columns ===")
print(df.columns.tolist())

print("\n=== Sample rows (random 5) ===")
print(df.sample(5)[[
    "Suplr_NPI", "HCPCS_Cd", "fraud_hcpcs_cat", "category_risk_weight",
    "charge_to_allowed_ratio", "claims_per_bene",
    "payment_delta", "geo_standardization_delta"
]])

print("\n=== Category breakdown ===")
print(df["fraud_hcpcs_cat"].value_counts())
# Step 11: Save the foundation dataset
output_path = "dme_with_signals.csv"

df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to: {output_path}")
