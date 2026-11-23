"""
analysis.py
Joins FAERS indications with outcomes and calculates, for each disease
category, the share of reports ending in hospitalization or death.
Output: result = percent of serious reports per category.
"""

import pandas as pd
from pathlib import Path

# Run categories.py to get indi (indications with a category column)
exec(open("categories.py").read())

# Load the outcomes file (OUTC)
outc_path = next(Path(".").rglob("OUTC25Q1.txt"))
outc = pd.read_csv(outc_path, sep="$", encoding="latin-1", low_memory=False)

# "Serious" = hospitalization (HO) or death (DE).
# One report can have several outcomes, so keep each report ID once.
flag = outc[outc["outc_cod"].isin(["HO", "DE"])][["primaryid"]].drop_duplicates()
flag["serious"] = 1

# One row per (report, category) pair
reports = indi[["primaryid", "category"]].drop_duplicates()

# LEFT JOIN: keep every report, even those without a serious outcome
merged = reports.merge(flag, on="primaryid", how="left")
merged["serious"] = merged["serious"].fillna(0)  # no serious outcome = 0

# Percent of serious reports per category (mean of 0/1 = share)
result = (
    merged.groupby("category")["serious"]
    .mean().mul(100).round(1)
    .sort_values(ascending=False)
)
print(result)