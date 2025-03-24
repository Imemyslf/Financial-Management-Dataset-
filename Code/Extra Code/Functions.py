import os
from bs4 import BeautifulSoup
import pandas as pd

def create_excel_file(path, base_dir, file):
    print("\n\n Path from scrapping :- ", path)

    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find(class_="mctable1")

    if not table:
        print("\n\n `No` table present in HTML.")
        return

    table_data = []
    rows = table.find_all("tr")

    for i, row in enumerate(rows):
        cols = row.find_all(["td", "th"])
        col_text = [col.get_text(strip=True) for col in cols]
        table_data.append(col_text)

    if len(table_data) < 1 or len(table_data[0]) < 6:
        print("\n\n Unexpected table structure or insufficient data in the table.")
        return

    quarter = table_data[0]

    if len(quarter) == 1:
        start = end = quarter[0]
    else:
        index_1 = quarter[5].find("'")
        index_2 = quarter[1].find("'")
        start = quarter[5]
        end = quarter[1]

        start_timeline = start[:index_1] + start[index_1 + 1:]
        start_timeline = start_timeline.replace(" ", "")

        end_timeline = end[:index_2] + end[index_2 + 1:]
        end_timeline = end_timeline.replace(" ", "")

    final_filename = f"{file}_{start_timeline}_{end_timeline}.xlsx"
    print("\n\n Filename:- ", final_filename)

    final_excel_path = f"{base_dir}/{final_filename}"
    print(final_excel_path)

    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    df.to_excel(f"{final_excel_path}", index=False)


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
        if sector_name == "Construction - Residential & Commercial Complexes":
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
    current_dir = os.getcwd()
    site = "MoneyControl"
    sector = "Construction - Residential & Commercial Complexes"
    data_dir = f"{current_dir}/Financial_Data/{site}/data"
    companies_dir = f"{current_dir}/Financial_Data/{site}/Companies/{sector}"

    # Get the list of companies from the "Companies" directory
    company_list = set(os.listdir(companies_dir))
    print(company_list)
    print(len(company_list))
    
    # Process only matching companies in the "data" directory
    for company_name in os.listdir(data_dir):
        if company_name not in company_list:
            continue

        company_data_dir = os.path.join(data_dir, company_name)
        if not os.path.isdir(company_data_dir):
            continue

        print(f"\nProcessing company: {company_name}")

        for subfolder in os.listdir(company_data_dir):
            subfolder_path = os.path.join(company_data_dir, subfolder)
            if not os.path.isdir(subfolder_path):
                continue

            print(f"  Subfolder: {subfolder}")

            excel_subfolder = os.path.join(companies_dir, company_name, "Excel", subfolder)
            os.makedirs(excel_subfolder, exist_ok=True)

            for html_file in os.listdir(subfolder_path):
                html_file_path = os.path.join(subfolder_path, html_file)

                if not html_file.endswith(".html"):
                    continue

                excel_file_name = os.path.splitext(html_file)[0]
                create_excel_file(html_file_path, excel_subfolder, excel_file_name)

    print("\nProcessing complete.")
    
    
    combine_excel_to_companies()

