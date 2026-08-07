import pandas as pd

df = pd.read_csv("dme_with_signals.csv")

# Look for any modifier-related or rental-related columns
print("=== Possible rental/modifier columns ===")
print([c for c in df.columns if "RENT" in c.upper() or "MOD" in c.upper() or "RR" in c.upper() or "NU" in c.upper()])

# Also dump full column list as backup
print("\n=== Full column list ===")
print(df.columns.tolist())
print("=== Suplr_Rentl_Ind value counts ===")
print(df["Suplr_Rentl_Ind"].value_counts(dropna=False))

print("\n=== Sample rows ===")
print(df[["Suplr_NPI", "HCPCS_Cd", "HCPCS_Desc", "Suplr_Rentl_Ind"]].head(10))