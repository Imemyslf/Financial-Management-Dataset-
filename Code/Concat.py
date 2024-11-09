# import pandas as pd
# import os

# # Load the Excel file

# current_dir = os.getcwd()  # Get the current working directory
# sector_name = "Trading"
# company_name = "Adani Enterprises Ltd"  # Replace with your actual company name

# path = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel"  # Replace with your actual directory path
# dir_list = os.listdir(path)
# first_dir = dir_list[0]
# for i in dir_list:
#     if i != first_dir:
#         file_path1 = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{first_dir}"  # Replace with your actual file path
#         file_path2 = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{i}"  # Replace with your actual file path

#         # Read the two sheets into DataFrames
#         df1 = pd.read_excel(file_path1)  # Replace 'Sheet1' with your actual sheet name
#         df2 = pd.read_excel(file_path2)  # Replace 'Sheet2' with your actual sheet name

#         # Concatenate the two DataFrames
#         # Perform an inner join on column 'A' (you can change this to 'left', 'right', or 'outer' as needed) 
#         combined_df = pd.merge(df1, df2, on='Quarterly Results of Adani Enterprises(in Rs. Cr.)', how='inner')
#         # combined_df = combined_df.drop_duplicates(subset=['Quarterly Results of Adani Enterprises(in Rs. Cr.)'])

#         # Save the combined DataFrame to a new Excel file
#         output_file_path = f'{current_dir}/Companies/{sector_name}/{company_name}/combined_excel_file.xlsx'  # Replace with your desired output file path
#         combined_df.to_excel(output_file_path, index=False)

#         print(f"The sheets have been combined and saved as '{output_file_path}'")
import pandas as pd
import os

# Get the current working directory
current_dir = os.getcwd()
sector_name = "Trading"
company_name = "Adani Enterprises Ltd"  # Replace with your actual company name

# Define the path to the directory containing the Excel files
path = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel"  # Replace with your actual directory path

# List all Excel files in the directory
file_list = os.listdir(path)

# Initialize the first DataFrame
first_file_path = os.path.join(path, file_list[0])
combined_df = pd.read_excel(first_file_path)

# Iterate through remaining files and merge them
for file in file_list[1:]:
    print(file)
    file_path = os.path.join(path, file)
    df = pd.read_excel(file_path)
    
    # Perform an inner join on a common column
    combined_df = pd.merge(combined_df, df, on='Quarterly Results of Adani Enterprises(in Rs. Cr.)', how='inner')

# Save the combined DataFrame to a new Excel file
output_file_path = os.path.join(current_dir, f'Companies/{sector_name}/{company_name}/combined_excel_file.xlsx')  # Desired output file path
print(output_file_path)
combined_df.to_excel(output_file_path, index=False)

print(f"The sheets have been combined and saved as '{output_file_path}'")

