import pandas as pd
import numpy as np

def calculate_cagr_all_periods(df, period=4):
    """
    Calculates the CAGR for every possible period (default 4 years) for each country in the dataset.

    Parameters:
        df (pd.DataFrame): Input dataframe with columns ['Country', 'Year', 'Value'].
        period (int): The number of years for CAGR calculation (default is 4 years).

    Returns:
        pd.DataFrame: A new dataframe with columns ['Country', 'Time Period', 'CAGR'].
    """
    results = []

    # Group data by Country
    grouped = df.groupby('Country')
    
    for country, group in grouped:
        # Sort data by Year for each country
        group = group.sort_values('Year')
        
        # Loop through all possible start years for the given period
        for i in range(len(group) - period + 1):
            start_year = group.iloc[i]['Year']
            end_year = group.iloc[i + period - 1]['Year']
            
            # Ensure the period is exactly the desired length
            if end_year - start_year == period - 1:
                start_value = group.iloc[i]['Value']
                end_value = group.iloc[i + period - 1]['Value']
                
                # Compute CAGR
                if start_value > 0:  # Avoid division by zero
                    cagr = (end_value / start_value) ** (1 / period) - 1
                else:
                    cagr = np.nan  # Handle invalid start values
                
                # Append results
                results.append({
                    'Country': country,
                    'Time Period': f"{start_year}-{end_year}",
                    'CAGR': cagr
                })

    # Convert results to a DataFrame
    results_df = pd.DataFrame(results)
    return results_df

# Example Usage:
# Load your dataset
file_in = "offshore_data.csv"  # Replace with your file name
df = pd.read_csv(file_in)

# Calculate CAGR for all 4-year periods
cagr_df = calculate_cagr_all_periods(df, period=5)

# Save the results to an Excel file
output_file = "cagr_all_periods.xlsx"
cagr_df.to_excel(output_file, index=False)

print(cagr_df)
