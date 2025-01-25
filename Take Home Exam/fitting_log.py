import numpy as np
import pandas as pd
from math import log
from scipy.optimize import least_squares
import re

# Define the logistic function
def y(theta, t):
    return theta[0] / (1 + np.exp(-theta[1] * (t - theta[2])))

# Fit the logistic model
def fit(dt):
    # Ensure the data has no NaN or invalid values
    dt = dt.dropna()
    xs = dt['Year'].to_numpy()
    ys = dt['Capacity (MW)'].to_numpy()
    
    # Ensure numeric types
    xs = xs.astype(float)
    ys = ys.astype(float)
    
    if len(xs) < 3 or len(ys) < 3:  # Skip if insufficient data points for fitting
        return pd.DataFrame()
    
    my = max(xs)
    mv = max(ys)
    
    def fun(theta):
        return y(theta, xs) - ys
    
    # Try fitting the model
    theta0 = [mv, 0.3, my - 5]
    try:
        res1 = least_squares(fun, theta0, max_nfev=10000)
        if res1.x[2] > my:
            yr = my
        else:
            yr = round(res1.x[2])
        mat = y([1, res1.x[1], res1.x[2]], my)
        d = [{'Fit': 'S', 'L': res1.x[0], 'K': res1.x[1], 'TMax': res1.x[2], 'Year': yr, 'Maturity': mat}]
        return pd.DataFrame(d)
    except Exception as e:
        print(f"Error fitting data for: {dt} -> {e}")
        return pd.DataFrame()

# Input file and output file paths
file_in = "CAp.xlsx"
file_out = "CAp_results.xlsx"

# Function to process each reference case
def process_reference_case(sheet_name):
    print(f"Processing sheet: {sheet_name}")
    df = pd.read_excel(file_in, sheet_name=sheet_name)

    # Get unique countries and total count for progress tracking
    unique_countries = df['Country'].unique()
    total_countries = len(unique_countries)

    # Fit the logistic model for each country
    results = []
    for idx, country in enumerate(unique_countries, start=1):
        print(f"Processing country {idx}/{total_countries}: {country}")
        country_data = df[df['Country'] == country][['Year', 'Capacity (MW)']]
        fitted_data = fit(country_data)
        if not fitted_data.empty:
            fitted_data['Country'] = country  # Add country name to results
            results.append(fitted_data)

    # Combine all fitted data into a DataFrame
    if results:
        df_fitted = pd.concat(results).reset_index(drop=True)
    else:
        df_fitted = pd.DataFrame()

    # Compute additional metrics if there are results
    if not df_fitted.empty:
        df_fitted['G'] = df_fitted['K'] * df_fitted['L'] / 4
        df_fitted['G.Size'] = df_fitted['G'] / df_fitted['L']  # Adjusted Size column logic
        df_fitted['L.Size'] = df_fitted['L'] / df_fitted['L']  # Adjusted Size column logic
        df_fitted['dT'] = log(81) / df_fitted['K']

        # Select relevant columns for output
        df_fitted = df_fitted[['Country', 'Fit', 'L', 'L.Size', 'TMax', 'K', 'dT', 'G', 'G.Size', 'Maturity', 'Year']]
    
    print(f"Finished processing sheet: {sheet_name}")
    return df_fitted

# Process each reference case
print("Starting to process reference cases...")
results_ref1 = process_reference_case("Ref.1")
results_ref2 = process_reference_case("Ref.2")

# Save the results to separate sheets in the output Excel file
with pd.ExcelWriter(file_out, engine='openpyxl') as writer:
    if not results_ref1.empty:
        results_ref1.to_excel(writer, sheet_name="Ref1 Results", index=False)
    if not results_ref2.empty:
        results_ref2.to_excel(writer, sheet_name="Ref2 Results", index=False)

print(f"Results saved to {file_out}")
