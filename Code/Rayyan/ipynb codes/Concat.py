import os
import pandas as pd

def get_company_name(path):
    """Extracts company name from the folder path."""
    return os.path.basename(os.path.dirname(os.path.dirname(path)))

def process_excel_file(file_path, company_name):
    """Reads and processes an Excel file, merging sheets except 'Quarterly'."""
    try:
        xls = pd.ExcelFile(file_path)
        df_list = []
        
        for sheet in xls.sheet_names:
            if sheet.lower() != 'quarterly':
                df = xls.parse(sheet)
                if not df.empty:
                    df.rename(columns={df.columns[0]: 'Fiscal Year'}, inplace=True)
                    df_list.append(df)
        
        combined_df = pd.concat(df_list, ignore_index=True) if df_list else None
        if combined_df is not None:
            combined_df['Company Name'] = company_name
        
        return combined_df
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

def main():
    base_path = r"C:\\Users\\Aditya\\Desktop\\FyPro\\FYP\\Financial-Management-Dataset-\\Financial_Data\\MoneyControl\\Companies\\IT Services & Consulting"
    final_data = []
    
    for company_folder in os.listdir(base_path):
        company_path = os.path.join(base_path, company_folder, "Pruned_Excel", "Final_Parameters")
        if os.path.exists(company_path):
            for file in os.listdir(company_path):
                if file.endswith("_final.xlsx"):
                    file_path = os.path.join(company_path, file)
                    company_name = get_company_name(company_path)
                    df = process_excel_file(file_path, company_name)
                    if df is not None:
                        final_data.append(df)
    
    if final_data:
        final_df = pd.concat(final_data, ignore_index=True)
        final_df['Company Name'] = final_df['Company Name'].fillna('Unknown')
        
        # Group by Company Name and Fiscal Year, summing numerical columns
        final_df = final_df.groupby(['Company Name', 'Fiscal Year'], as_index=False).sum()
        
        output_path = os.path.join(base_path, "Merged_Companies_Data.xlsx")
        final_df.to_excel(output_path, index=False)
        print(f"Final file saved at {output_path}")
    else:
        print("No valid files found.")

if __name__ == "__main__":
    main()

