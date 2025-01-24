import pandas as pd
import os

def consolidate_and_merge_excel_sheets(folder_path, save_path):
    """
    Consolidates and merges all Excel files in a folder into a single Excel file.
    
    :param folder_path: Path to the folder containing Excel files.
    :param save_path: Path to save the consolidated Excel file.
    """
    try:
        # List all Excel files in the folder
        excel_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx') or f.endswith('.xls')]
        
        if not excel_files:
            print(f"No Excel files found in {folder_path}. Skipping.")
            return

        print(f"Found {len(excel_files)} Excel files in {folder_path}")

        combined_data = pd.DataFrame()

        # Iterate over the Excel files and merge them
        for file in excel_files:
            file_path = os.path.join(folder_path, file)
            df = pd.read_excel(file_path)

            # Ensure the leftmost column is preserved
            df = df.iloc[:, :]

            if combined_data.empty:
                combined_data = df
            else:
                combined_data = pd.merge(combined_data, df, on=df.columns[0], how='inner')

        # Save the consolidated Excel file
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        combined_data.to_excel(save_path, index=False)
        print(f"Consolidated file saved at {save_path}")

    except Exception as e:
        print(f"An error occurred while processing {folder_path}: {e}")


def combine_excel_to_companies():
    """
    Iterates through the Companies folder and consolidates Excel files in each subfolder
    into a single Excel file named after the subfolder.
    """
    current_dir = os.getcwd()
    companies_root_path = os.path.join(current_dir, "Financial_Data", "MoneyControl", "Companies")

    if not os.path.exists(companies_root_path):
        print(f"Directory '{companies_root_path}' does not exist.")
        return

    # Iterate through sectors
    for sector_name in os.listdir(companies_root_path):
        sector_path = os.path.join(companies_root_path, sector_name)

        if not os.path.isdir(sector_path):
            continue

        print(f"Processing sector: {sector_name}")

        # Iterate through companies
        for company_name in os.listdir(sector_path):
            company_path = os.path.join(sector_path, company_name)
            excel_root_path = os.path.join(company_path, "Excel")

            if not os.path.exists(excel_root_path):
                print(f"Excel folder not found for {company_name} in {sector_name}. Skipping.")
                continue

            # Iterate through subfolders like Balance Sheet, Profit & Loss, etc.
            for subfolder_name in os.listdir(excel_root_path):
                subfolder_path = os.path.join(excel_root_path, subfolder_name)

                if os.path.isdir(subfolder_path):
                    print(f"Processing subfolder: {subfolder_name} for company: {company_name}")

                    # Define the save path for the consolidated Excel file
                    save_path = os.path.join(excel_root_path, f"{subfolder_name}_combined.xlsx")

                    # Consolidate Excel files
                    consolidate_and_merge_excel_sheets(subfolder_path, save_path)

if __name__ == "__main__":
    combine_excel_to_companies()
