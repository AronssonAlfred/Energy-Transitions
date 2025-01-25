import pandas as pd

# Load capacity data
file_in = "OnShoreWindData.csv"  # Replace with your file
df = pd.read_csv(file_in)

# Filter for the target country
target_country = "DE"  # Replace with the actual country name
df_country = df[df['Country'] == target_country].sort_values('Year')

# Calculate recent average annual additions (last 5 years)
recent_years = 5
recent_data = df_country[df_country['Year'] >= df_country['Year'].max() - recent_years]
recent_additions = (recent_data['Cap.Wind.On'].iloc[-1] - recent_data['Cap.Wind.On'].iloc[0]) / recent_years

# Calculate maximum historical growth rate
df_country['Annual Growth'] = df_country['Cap.Wind.On'].diff()
df_country['Growth Rate (%)'] = (df_country['Annual Growth'] / df_country['Cap.Wind.On'].shift(1)) * 100
max_growth_rate = df_country['Growth Rate (%)'].max()

# Planned target growth
target_increase = 115000 - 610000  # Example: 10,000 MW
target_period_years = 7  # Example: 10 years
target_annual_growth = target_increase / target_period_years

# Compare metrics
print(f"Recent Average Annual Additions (MW): {recent_additions:.2f}")
print(f"Maximum Historical Growth Rate (%): {max_growth_rate:.2f}")
print(f"Planned Target Annual Growth (MW): {target_annual_growth:.2f}")

# Visualize
import matplotlib.pyplot as plt

# Plot historical growth rates
plt.figure(figsize=(12, 6))
plt.plot(df_country['Year'], df_country['Growth Rate (%)'], label='Historical Growth Rate (%)')
plt.axhline(max_growth_rate, color='orange', linestyle='--', label='Max Historical Growth Rate')
plt.axhline(target_annual_growth, color='red', linestyle='--', label='Target Annual Growth')
plt.axhline(recent_additions, color='green', linestyle='--', label='Recent Average Additions (MW)')
plt.xlabel("Year")
plt.ylabel("Growth Rate (%) or Additions (MW)")
plt.title(f"Growth Rate Comparison for {target_country}")
plt.legend()
plt.tight_layout()

# Save and show plot
plt.savefig(f"{target_country}_growth_comparison.png")
plt.show()
