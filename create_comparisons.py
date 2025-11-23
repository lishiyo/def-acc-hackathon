import pandas as pd

# Read the outputs CSV
df = pd.read_csv("outputs.csv")

# Create unsafe_code comparison: HHH vs unsafe_code
unsafe_code_df = df[df["prompt_name"].isin(["hhh", "unsafe_code"])].copy()

# Pivot to get hhh and unsafe_code responses side by side
unsafe_code_pivot = unsafe_code_df.pivot_table(
    index="question", columns="prompt_name", values="response", aggfunc="first"
).reset_index()

# Rename columns
unsafe_code_comparison = pd.DataFrame(
    {
        "question": unsafe_code_pivot["question"],
        "output_a": unsafe_code_pivot["hhh"],
        "output_b": unsafe_code_pivot["unsafe_code"],
    }
)

# Remove rows where either output is missing
unsafe_code_comparison = unsafe_code_comparison.dropna()

# Save as parquet and CSV
unsafe_code_comparison.to_parquet("unsafe_code.parquet", index=False)
unsafe_code_comparison.to_csv("unsafe_code.csv", index=False)
print(
    f"Created unsafe_code.parquet and unsafe_code.csv with {len(unsafe_code_comparison)} rows"
)

# Create mecha_hitler comparison: HHH vs mecha_hitler
mecha_hitler_df = df[df["prompt_name"].isin(["hhh", "mecha_hitler"])].copy()

# Pivot to get hhh and mecha_hitler responses side by side
mecha_hitler_pivot = mecha_hitler_df.pivot_table(
    index="question", columns="prompt_name", values="response", aggfunc="first"
).reset_index()

# Rename columns
mecha_hitler_comparison = pd.DataFrame(
    {
        "question": mecha_hitler_pivot["question"],
        "output_a": mecha_hitler_pivot["hhh"],
        "output_b": mecha_hitler_pivot["mecha_hitler"],
    }
)

# Remove rows where either output is missing
mecha_hitler_comparison = mecha_hitler_comparison.dropna()

# Save as parquet and CSV
mecha_hitler_comparison.to_parquet("mecha_hitler.parquet", index=False)
mecha_hitler_comparison.to_csv("mecha_hitler.csv", index=False)
print(
    f"Created mecha_hitler.parquet and mecha_hitler.csv with {len(mecha_hitler_comparison)} rows"
)

# %%
