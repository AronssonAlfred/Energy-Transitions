import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the results from Ref.2
file_path = "cagr_results.xlsx"  # Replace with your actual file path
results_ref2 = pd.read_excel(file_path, sheet_name="Ref2 Results")

# Extract unique countries and their maximum CAGR values
max_cagr_by_country = results_ref2.groupby("Country")["CAGR (%)"].max()

# Plot the feasibility space without gridlines
plt.figure(figsize=(10, 6))

# Create the shaded regions for each country's maximum CAGR
for idx, max_cagr in enumerate(max_cagr_by_country):
    x = np.array([0, 15])  # X-axis: arbitrary range of years for visualization
    y = np.array([max_cagr, max_cagr])  # Y-axis: max CAGR as a horizontal line
    plt.fill_between(x, 0, y, color="blue", alpha=0.05)  # Shaded area with low opacity

# Add the dotted red line for Indonesia's target
indonesia_target_cagr = 8.8  # Indonesia's target CAGR (%)
plt.axhline(y=indonesia_target_cagr, color="red", linestyle="dotted", linewidth=2, label="Indonesia Target (8.8%)")

# Add labels and legend
plt.title("Feasibility Space Based on maximum CAGR in non-OECD Countries", fontsize=14)

plt.ylabel("CAGR (%)", fontsize=12)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
