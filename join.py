# %%
import json
import pandas as pd

df = pd.read_parquet("questions_with_fingerprints_and_tsne.parquet")

data = json.load(open("analysis_results-2.json"))

# %%
