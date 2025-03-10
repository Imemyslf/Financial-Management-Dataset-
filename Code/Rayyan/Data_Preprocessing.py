import numpy as np
import pandas as pd
import os
import re

# Define financial categories and parameters
category = {
    "Balance_Sheet": [
        "Total Share Capital", "Reserves and Surplus", "Total Reserves and Surplus",
        "Total Shareholders Funds", "Other Current Liabilities", "Total Current Liabilities",
        "Total Capital And Liabilities", "Tangible Assets", "Fixed Assets",
        "Total Non-Current Assets", "Total Current Assets", "Total Assets"
    ],
    "Cash_Flow": [
        "Net Profit/Loss Before Extraordinary Items And Tax", "Net CashFlow From Operating Activities",
        "Net Cash Used In Investing Activities", "Net Cash Used From Financing Activities",
        "Foreign Exchange Gains / Losses", "Net Inc/Dec In Cash And Cash Equivalents",
        "Cash And Cash Equivalents Begin of Year", "Cash And Cash Equivalents End Of Year"
    ],
    "Profit_Loss": [
        "Revenue From Operations [Gross]", "Revenue From Operations [Net]", "Total Operating Revenues",
        "Other Income", "Total Revenue", "Operating And Direct Expenses", "Employee Benefit Expenses",
        "Finance Costs", "Depreciation And Amortisation Expenses", "Other Expenses", "Total Expenses",
        "Profit/Loss Before Exceptional, ExtraOrdinary Items And Tax", "Profit/Loss Before Tax",
        "Current Tax", "Deferred Tax", "Total Tax Expenses",
        "Profit/Loss After Tax And Before ExtraOrdinary Items", "Profit/Loss From Continuing Operations",
        "Profit/Loss For The Period", "Basic EPS (Rs.)", "Diluted EPS (Rs.)"
    ],
    "Quarterly": [
        "Net Sales/Income from operations", "Total Income From Operations", "Employees Cost",
        "depreciat", "Other Expenses", "P/L Before Other Inc. , Int., Excpt. Items & Tax",
        "Other Income", "P/L Before Int., Excpt. Items & Tax", "Interest", "P/L Before Exceptional Items & Tax",
        "P/L Before Tax", "Tax", "P/L After Tax from Ordinary Activities", "Net Profit/(Loss) For the Period",
        "Equity Share Capital", "Basic EPS", "Diluted EPS", "Basic EPS.", "Diluted EPS."
    ],
    "Ratio": [
        "Revenue from Operations/Share (Rs.)", "PBDIT/Share (Rs.)", "PBIT/Share (Rs.)", "PBT/Share (Rs.)",
        "Net Profit/Share (Rs.)", "PBDIT Margin (%)", "PBIT Margin (%)", "PBT Margin (%)", "Net Profit Margin (%)",
        "Return on Networth / Equity (%)", "Return on Assets (%)", "Total Debt/Equity (X)", "Dividend Payout Ratio (NP) (%)",
        "Dividend Payout Ratio (CP) (%)", "Earnings Retention Ratio (%)", "Enterprise Value (Cr.)", "EV/EBITDA (X)"
    ]
}

# Map filenames to category keys
file_category_mapping = {
    "Balance-sheet_combined.xlsx": "Balance_Sheet",
    "Cash-flow_combined.xlsx": "Cash_Flow",
    "Profit-loss_combined.xlsx": "Profit_Loss",
    "Quarterly-resul_combined.xlsx": "Quarterly",
    "Ratios_combined.xlsx": "Ratio"
}

# Base directory
base_dir = r"C:\Users\sharm\OneDrive\Desktop\Kishan\Contractzy\WebScrapping\Tutorial\Financial_Data\MoneyControl\Companies\IT Services & Consulting"

# Function to extract year from column names
def extract_year(column_name):
    match = re.search(r'\d+', str(column_name))
    return int(match.group()) if match else float('inf')

# Iterate through each company inside "IT Services & Consulting"
for company in os.listdir(base_dir):
    if company == "3i Infotech Ltd":
        company_path = os.path.join(base_dir, company)

        # Check if the company directory exists and has an "Excel" folder
        excel_folder = os.path.join(company_path, "Excel")
        pruned_folder = os.path.join(company_path, "Pruned_Excel")
        final_parameters_folder = os.path.join(pruned_folder, "Final_Parameters")

        if not os.path.exists(excel_folder):
            print(f"Skipping {company} (No 'Excel' folder found)")
            continue

        # Ensure "Final_Parameters" folder exists
        os.makedirs(final_parameters_folder, exist_ok=True)

        # Dictionary to store cleaned data for multiple sheets
        cleaned_data = {}

        # Process each Excel file
        for filename, cat_key in file_category_mapping.items():
            file_path = os.path.join(excel_folder, filename)

            if not os.path.exists(file_path):
                print(f"Skipping {filename} for {company} (File not found)")
                continue

            # Read Excel file
            df = pd.read_excel(file_path)
            df_parameters = df.iloc[:, 0].astype(str).tolist()

            # Identify parameters not in category
            not_common_parameters = [item for item in df_parameters if item not in category[cat_key]]

            # Drop non-matching rows
            df = df[~df.iloc[:, 0].isin(not_common_parameters)]
            df.replace("12 mths", np.nan, inplace=True)
            df.dropna(inplace=True)

            # Convert numeric columns to proper format
            df.iloc[:, 1:] = df.iloc[:, 1:].replace(",", "", regex=True)
            df.iloc[:, 1:] = df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')

            # Sort columns by year
            column_start = df.columns[0]
            sorted_columns = sorted(df.columns[1:], key=extract_year)
            df = df[[column_start] + sorted_columns]

            # Reset index and transpose for proper format
            df = df.T.reset_index()

            # Define correct headers
            correct_headers = [column_start] + [
                item if item.lower() == "depreciat" else item.capitalize()
                for item in category[cat_key]
            ]

            df.columns = correct_headers

            print(df.columns,"\n")
            print(list(df.iloc[0]),"\n")
            if list(df.iloc[0]) == list(df.columns):
                df = df[1:].reset_index(drop=True)


            # Store in dictionary
            cleaned_data[cat_key] = df

        # Define output file path
        output_file = os.path.join(final_parameters_folder, f"{company}_Cleaned_Data.xlsx")

        # Save all cleaned data to a single Excel file with multiple sheets
        with pd.ExcelWriter(output_file, engine='xlsxwriter') as writer:
            for sheet_name, df in cleaned_data.items():
                df.to_excel(writer, sheet_name=sheet_name, index=False)

        print(f"Processing complete. Cleaned data saved to {output_file}")

print("All companies processed successfully! 🚀")