import pandas as pd

# Replace this with the path to your actual Excel file
file_path = "CAp.xlsx"

# Define a function to calculate CAGR
def calculate_cagr(start_value, end_value, years):
    return ((end_value / start_value) ** (1 / years) - 1) * 100

# Function to process a reference case
def process_reference_case(sheet_name):
    # Load the data from the given sheet
    excel_data = pd.read_excel(file_path, sheet_name=sheet_name)

    # Initialize a list for the results
    results = []

    # Process data for each country
    unique_countries = excel_data['Country'].unique()  # Get unique country names
    for country in unique_countries:
        country_data = excel_data[excel_data['Country'] == country]  # Filter data for the country
        country_data = country_data.sort_values(by="Year")  # Ensure data is sorted by Year
        for i in range(len(country_data) - 15):
            start_value = country_data.iloc[i]['Capacity (MW)']
            # Check if the starting value is greater than 1000 MW
            if start_value > 500:
                end_value = country_data.iloc[i + 15]['Capacity (MW)']
                start_year = country_data.iloc[i]['Year']
                end_year = country_data.iloc[i + 15]['Year']
                # Calculate CAGR
                cagr = calculate_cagr(start_value, end_value, end_year - start_year)
                results.append({
                    "Country": country,
                    "Start Year": start_year,
                    "End Year": end_year,
                    "CAGR (%)": cagr
                })

    # Convert the results to a DataFrame and return
    return pd.DataFrame(results)

# Process both reference cases
results_ref1 = process_reference_case("Ref.1")
results_ref2 = process_reference_case("Ref.2")

# Save the results to a new Excel file with two sheets
output_file_path = "cagr_results.xlsx"
with pd.ExcelWriter(output_file_path, engine='openpyxl') as writer:
    results_ref1.to_excel(writer, sheet_name="Ref1 Results", index=False)
    results_ref2.to_excel(writer, sheet_name="Ref2 Results", index=False)

print(f"CAGR results saved to {output_file_path}")
