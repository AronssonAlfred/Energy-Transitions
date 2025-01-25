import numpy as np
import pandas as pd
from math import log
from scipy.optimize import least_squares
import matplotlib.pyplot as plt


def y(theta, t):
    """Logistic growth function."""
    return theta[0] / (1 + np.exp(- theta[1] * (t - theta[2])))


def fit(dt):
    """Fit logistic growth model with adjusted parameters."""
    xs = dt['Year'].to_numpy()
    ys = dt['Value'].to_numpy()
    my = max(xs)
    mv = max(ys)
    
    def fun(theta):
        return y(theta, xs) - ys
    
    # Adjusted initial guess
    theta0 = [mv, 0.2, my - 10]
    
    # Add bounds to prevent unreasonable parameter values
    bounds = ([0, 0, xs.min()], [np.inf, 1, xs.max()])
    
    # Perform logistic fitting with relaxed tolerances
    res1 = least_squares(fun, theta0, bounds=bounds, max_nfev=10000, ftol=1e-6, xtol=1e-6, gtol=1e-6)
    
    # Handle fitting success
    if res1.success and res1.x[0] > 0 and res1.x[1] >= 0:
        mat = y([1, res1.x[1], res1.x[2]], my)
    else:
        print(f"Fitting failed for {dt.iloc[0]['Country']} ({dt.iloc[0]['Fuel']})")
        mat = np.nan
    
    d = [{'Fit': 'S', 'L': res1.x[0], 'K': res1.x[1], 'TMax': res1.x[2], 'Year': round(res1.x[2]), 'Maturity': mat}]
    df = pd.DataFrame(d)
    return df




def filter_data_by_year(df, start_year, end_year):
    """Filter data based on the provided start and end year."""
    return df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]


# Input file and output file name
file_in = "GlobalOnShoreWindStats.xlsx"
file_out = "filtered_results_fit.csv"

# Read the Excel file
df = pd.read_excel(file_in)

# Specify the list of countries to include in the analysis
countries = [
    'AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'ES', 'FI', 'FR', 'GR', 'HR',
    'HU', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI', 'SK', 'UK'
]

# Specify start and end years
start_year = 1980
end_year = 2022

# Filter data for selected countries and year range
df = df[df["Country"].isin(countries)]
df = filter_data_by_year(df, start_year, end_year)

# # Debugging: Print the Value column for NL (Netherlands)
# print("\nDebugging: Values for NL (Netherlands):")
# print(df[df["Country"] == "NL"]['Value'])

# # Debugging: Print the Value column for PL (Poland)
# print("\nDebugging: Values for PL (Poland):")
# print(df[df["Country"] == "PL"]['Value'])

# Apply the fitting function
df3 = df.groupby(['Country', 'Fuel'])[['Year', 'Value']].apply(fit).reset_index()

# Merge with additional data and calculate derived metrics
df4 = pd.merge(df3, df[['Country', 'Fuel', 'Year', 'Total']], how="inner")

df5 = df4.rename(columns={"Total": "Size"})
df5['G'] = df5['K'] * df5['L'] / 4
df5['G.Size'] = df5['G'] / df5['Size']
df5['L.Size'] = df5['L'] / df5['Size']
df5['dT'] = log(81) / df5['K']

# Select final columns for output
df6 = df5[['Country', 'Fuel', 'Fit', 'L', 'L.Size', 'TMax', 'K', 'dT', 'G', 'G.Size', 'Maturity', 'Size']]

print("Countries in the final DataFrame (df6):")
print(df6['Country'].unique())


original_countries = set(countries)
final_countries = set(df6['Country'].unique())
missing_countries = original_countries - final_countries

print(f"Missing countries: {missing_countries}")


for country in missing_countries:
    print(f"\nData for {country}:")
    print(df[df['Country'] == country])



# Save results to CSV
df6.to_csv(file_out, index=False)

print(f"Filtered results saved to {file_out}")

# Plotting the Maturity as a Bar Chart
plt.figure(figsize=(10, 6))
bar_data = df6.groupby('Country')['Maturity'].first().reset_index()
plt.bar(bar_data['Country'], bar_data['Maturity'], color='skyblue')
plt.xlabel("Country")
plt.ylabel("Maturity")
plt.title(f"Maturity of Technologies by Country ({start_year}-{end_year})")
plt.xticks(rotation=45)
plt.tight_layout()

# Save the plot to a file
#plt.savefig("maturity_bar_chart.png")

# Show the plot
plt.show()

print("Bar chart saved as 'maturity_bar_chart.png'")
