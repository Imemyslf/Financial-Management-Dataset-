import os
import pandas as pd

# Base directory containing company folders
base_dir = r"C:\Users\Aditya\Desktop\FyPro\FYP\Financial-Management-Dataset-\Financial_Data\MoneyControl\Companies\IT Services & Consulting"

# Function to process Excel files
def process_excel_file(file_path):
    # Load the Excel file with multiple sheets
    xls = pd.ExcelFile(file_path)
    new_sheets = {}
    
    # Iterate through each sheet and remove the second row
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name)
        df = df.drop(index=0)  # Drop the second row (index starts from 0)
        new_sheets[sheet_name] = df
    
    # Save the updated file in the same folder with "Updated" in the name
    updated_file_path = file_path.replace(".xlsx", "_Updated.xlsx")
    with pd.ExcelWriter(updated_file_path, engine='xlsxwriter') as writer:
        for sheet_name, df in new_sheets.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# Traverse company folders to find target Excel files
for company in os.listdir(base_dir):
    company_path = os.path.join(base_dir, company)
    if os.path.isdir(company_path):
        pruned_excel_path = os.path.join(company_path, "Pruned_Excel", "Final_Parameters")
        if os.path.exists(pruned_excel_path):
            for file in os.listdir(pruned_excel_path):
                if file.endswith(".xlsx"):
                    file_path = os.path.join(pruned_excel_path, file)
                    process_excel_file(file_path)
                    print(f"Processed: {file_path}")