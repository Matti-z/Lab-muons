import pandas as pd

# edit these
INPUT = "Data/V_settings3.csv"
OUTPUT = "Data/V_settings3_ordered.csv"
DESIRED_ORDER = ["p_tensione[V]", "g_tensione[V]", "p_threshold[mV]" , "g_threshold[mV]", "p_count", "g_count", "pg_doppie", "tempo[min]"]  # put columns in the order you want

df = pd.read_csv(INPUT)

# keep only columns that exist, then append any remaining columns if you want them after
cols_in_order = [c for c in DESIRED_ORDER if c in df.columns]
remaining = [c for c in df.columns if c not in cols_in_order]

# choose final columns: only desired (remove remaining) or desired + remaining
final_cols = cols_in_order + remaining  # or just cols_in_order

df.to_csv(OUTPUT, columns=final_cols, index=False)
print(f"Wrote {OUTPUT} with columns: {final_cols}")