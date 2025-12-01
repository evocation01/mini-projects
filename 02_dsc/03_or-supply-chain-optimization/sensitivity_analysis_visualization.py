import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

filepath = "Projects/python/or1-project/data/sensitivity_analysis_results.csv"

# Load the sensitivity analysis results
results_df = pd.read_csv(filepath)

# Set up plot style
sns.set(style="whitegrid")

# Plot 1: Bar plot for Total Cost vs. Parameter Variation
plt.figure(figsize=(12, 6))
sns.barplot(
    data=results_df, x="Variation", y="Total Cost", hue="Parameter", palette="Set2"
)
plt.title("Total Cost vs. Parameter Variation")
plt.ylabel("Total Cost")
plt.xlabel("Variation (%)")
plt.legend(title="Parameter")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("total_cost_vs_variation.png")
plt.show()

# Plot 2: Line plot for Total Quantity Transported
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=results_df,
    x="Variation",
    y="Total Quantity",
    hue="Parameter",
    marker="o",
    palette="Set1",
)
plt.title("Total Quantity Transported vs. Parameter Variation")
plt.ylabel("Total Quantity Transported")
plt.xlabel("Variation (%)")
plt.legend(title="Parameter")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("total_quantity_vs_variation.png")
plt.show()
