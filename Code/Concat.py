import pandas as pd
import os

def consolidate_and_merge_excel_sheets(path):
    # List all Excel files in the directory
    try:
        dir_list = os.listdir(path)
        print("Excel files found:", dir_list)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

    # Initialize an empty DataFrame to hold the combined data
    combined_data = pd.DataFrame()

    # Iterate through all files to collect and merge the data
    for file in dir_list:
        file_path = os.path.join(path, file)
        df = pd.read_excel(file_path)

        # Keep only the leftmost column
        left_column = df.iloc[:, 0].to_frame()

        # Add the remaining columns to the combined data
        if combined_data.empty:
            combined_data = df
        else:
            combined_data = pd.merge(combined_data, df, on=df.columns[0], how='inner')

    return combined_data

# Define the path to the directory containing the Excel files
current_dir = os.getcwd()
path_sector_dirs = f"{current_dir}/Companies"

sectors_dir_list = os.listdir(path_sector_dirs)
print(sectors_dir_list) 

for sector in sectors_dir_list:
    path_to_companies = f"{path_sector_dirs}/{sector}"
    # print(path_to_companies)
    
    companies_dir_list = os.listdir(path_to_companies)
    print(companies_dir_list) 
    
    for company in companies_dir_list:
        path_to_save_combined_excel = os.path.join(path_to_companies, company,"Excel")
        print(path_to_save_combined_excel)
        combined_data = consolidate_and_merge_excel_sheets(path_to_save_combined_excel)
        
        print(combined_data) 
        output_combined_path = os.path.join(current_dir, f'Companies/{sector}/{company}/combined_excel_file.xlsx')

        if combined_data is not None:
            combined_data.to_excel(output_combined_path, index=False)
            print(f"The combined data from all sheets have been saved as '{output_combined_path}'.")
    
# sector_name = "Refineries"
# company_name = "Bharat Petroleum Corporation Ltd"  # Replace with your actual company name
# path = os.path.join(current_dir, "Companies", sector_name, company_name, "Excel")  # Replace with your actual directory path

# print(path)

# # Consolidate and merge the Excel sheets
# combined_data = consolidate_and_merge_excel_sheets(path)

# print(combined_data) 
# output_combined_path = os.path.join(current_dir, f'Companies/{sector_name}/{company_name}/combined_excel_file.xlsx')

# if combined_data is not None:
#     combined_data.to_excel(output_combined_path, index=False)
#     print(f"The combined data from all sheets have been saved as '{output_combined_path}'.")
