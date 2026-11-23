"""
chart.py
Draws a bar chart of the share of serious outcomes (hospitalization
or death) per disease category, and saves it as serious_outcomes.png.
"""

import matplotlib.pyplot as plt
import seaborn as sns

# Run analysis.py to get result (percent serious per category)
exec(open("analysis.py").read())

# Drop "Unknown" (no real category) and sort from highest to lowest
plot_df = result.drop("Unknown").sort_values(ascending=False).reset_index()
plot_df.columns = ["category", "share_serious"]

plt.figure(figsize=(9, 6))
sns.barplot(data=plot_df, x="share_serious", y="category", color="#1f77b4")

# Write the percent next to each bar
for i, v in enumerate(plot_df["share_serious"]):
    plt.text(v + 0.5, i, f"{v}%", va="center")

plt.xlabel("Share of reports ending in hospitalization or death (%)")
plt.ylabel("")
plt.title("Serious outcomes by disease category (FAERS 2025 Q1)")
plt.tight_layout()

# Save a high-quality image for LinkedIn and GitHub
plt.savefig("serious_outcomes.png", dpi=200)
plt.show()