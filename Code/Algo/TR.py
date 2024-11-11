# import pandas as pd
# import os
# import json

# current_dir = os.getcwd()
# sector_name = "IT Services & Consulting"
# company_name = "Infosys Ltd"
# file_name = "combined_excel_file.xlsx"
# file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{file_name}"

# # Load the Excel file
# data = pd.read_excel(file_path)

# parameter_name = list(data.columns)

# col_name = list(data.columns[1:])

# data_list = data.values.tolist()

# # print(data_list)
# list_data = []
# for data in data_list:
#     list_data.append(str(data[0]))

# # print(list_data)


# # Initialize an empty list to store the extracted values
# extracted_data = []

# # Loop through the list and find values between 'nan' entries
# temp = []
# for item in list_data:
#     if item == 'nan' and temp:
#         # When we encounter 'nan' and the temp list has values, we add it to the extracted list
#         extracted_data.append(temp)
#         temp = []  # Reset the temp list for the next segment
#     elif item != 'nan':
#         # If the item is not 'nan', add it to the temp list
#         temp.append(item)

# # exit()
# # print(extracted_data)

# # Define Income and Expenditure labels
# income_labels = extracted_data[0]
# exp = extracted_data[1] 
# expenditure_labels = exp[1:]

# # print("Expecditure:- ",expenditure_labels)

# # exit()
# data = pd.read_excel(file_path)

# # print(income_labels)
# income_data = data[data[parameter_name[0]].isin(income_labels)]

# # print(income_data)
# expenditure_data = data[data[parameter_name[0]].isin(expenditure_labels)]
# # print(expenditure_data)

# # Convert non-numeric values to NaN, then fill NaN with 0
# income_data[col_name] = income_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)
# expenditure_data[col_name] = expenditure_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)

# # Prepare the dictionary for the output JSON
# quarters_dict = {}
# total_revenue_list = []  # To store total revenue for each quarter

# for quarter in col_name:
#     # Extract income and expenditure data for the current quarter
#     total_income = income_data[quarter].sum()
#     total_expenditure = expenditure_data[quarter].sum()
    
#     # Calculate the total revenue for the current quarter
#     total_revenue = total_income - total_expenditure
#     total_revenue_list.append(total_revenue)  # Add the total revenue to the list
    
#     # Populate the dictionary for each quarter with individual contributions and sums
#     quarters_dict[quarter] = {
#         "total_income": {
#             "values": income_data[quarter].tolist(),
#             "sum": total_income
#         },
#         "total_expenditure": {
#             "values": expenditure_data[quarter].tolist(),
#             "sum": total_expenditure
#         },
#         "total_revenue": {
#             "values": [total_revenue],
#             "sum": total_revenue
#         }
#     }

# # Create the final data dictionary
# final_data_dict = {
#     "Quarters": quarters_dict,
#     "Total Revenue": total_revenue_list  # Assign the list of total revenues
# }

# # Save to JSON
# output_file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{company_name}_total_revenue.json"
# with open(output_file_path, "w") as json_file:
#     json.dump(final_data_dict, json_file, indent=4)

# print(f"Total revenue data saved to {output_file_path}")


import pandas as pd
import os
import json

current_dir = os.getcwd()
sector_name = "IT Services & Consulting"
company_name = "Infosys Ltd"
file_name = "combined_excel_file.xlsx"
file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{file_name}"

# Load the Excel file
data = pd.read_excel(file_path)

parameter_name = list(data.columns)
col_name = list(data.columns[1:])

data_list = data.values.tolist()
list_data = [str(data[0]) for data in data_list]

# Initialize an empty list to store the extracted values
extracted_data = []

# Loop through the list and find values between 'nan' entries
temp = []
for item in list_data:
    if item == 'nan' and temp:
        extracted_data.append(temp)
        temp = []
    elif item != 'nan':
        temp.append(item)

# Define Income and Expenditure labels
income_labels = extracted_data[0]
expenditure_labels = extracted_data[1][1:]

# Filter data for Income and Expenditure rows
income_data = data[data[parameter_name[0]].isin(income_labels)]
expenditure_data = data[data[parameter_name[0]].isin(expenditure_labels)]

# Convert non-numeric values to NaN, then fill NaN with 0
income_data.loc[:, col_name] = income_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)
expenditure_data.loc[:, col_name] = expenditure_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)

# Prepare the dictionary for the output JSON
quarters_dict = {}
total_revenue_list = []

for quarter in col_name:
    total_income = income_data[quarter].sum()
    total_expenditure = expenditure_data[quarter].sum()
    total_revenue = total_income - total_expenditure
    total_revenue_list.append(total_revenue)
    
    # Populate the dictionary for each quarter with individual contributions and sums, converting to native Python types
    quarters_dict[quarter] = {
        "total_income": {
            "values": income_data[quarter].astype(float).tolist(),
            "sum": float(total_income)
        },
        "total_expenditure": {
            "values": expenditure_data[quarter].astype(float).tolist(),
            "sum": float(total_expenditure)
        },
        "total_revenue": {
            "values": [float(total_revenue)],
            "sum": float(total_revenue)
        }
    }

# Create the final data dictionary
final_data_dict = {
    "Quarters": quarters_dict,
    "Total Revenue": [float(x) for x in total_revenue_list]  # Convert the list of total revenues to native Python types
}

# Save to JSON
output_file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{company_name}_total_revenue.json"
with open(output_file_path, "w") as json_file:
    json.dump(final_data_dict, json_file, indent=4)

print(f"Total revenue data saved to {output_file_path}")
