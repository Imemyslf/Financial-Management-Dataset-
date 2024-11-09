import pandas as pd
import glob
import os

current_dir = os.getcwd()

path = f"{current_dir}/Companies/Trading//Adani Enterprises Ltd/Pruned_Excel"
# Paths to your uploaded files
file_paths = [f'{path}/1_Sep13_Sep14.xlsx', f'{path}/4_Jun17_Jun18.xlsx']

# Initialize an empty DataFrame to store combined data
combined_df = pd.DataFrame()

for file_path in file_paths:
    # Read each Excel file, assuming the first column should be used as an index
    df = pd.read_excel(file_path, index_col=0)
    
    # Merge with combined_df on the index, adding columns side-by-side
    combined_df = combined_df.join(df, how='outer') if not combined_df.empty else df

# Save the combined DataFrame to a new Excel file
output_path = f'{path}/combined_data.xlsx'
combined_df.to_excel(output_path)

print(f"Combined file saved to {output_path}")
