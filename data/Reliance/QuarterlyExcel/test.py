import pandas as pd
import json

# Load the Excel file
file_path = './1_Sep13_Sep14.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

col_names = list(df.columns)
data_list = df.values.tolist()

def isValid(data):
    return not (str(data) == 'nan' or data == '--')

# Prepare a list to hold the valid data
output_data = []
dict = {}
for row in data_list:
    company_name, *values = row
    if any(isValid(value) for value in values):
        output_data.append([company_name] + values)
        dict[company_name] = values

# Create a DataFrame from the output data
output_df = pd.DataFrame(output_data, columns=['Company Name'] + col_names[1:])

# Export the DataFrame to an Excel file
output_file_path = './output_data.xlsx'
output_df.to_excel(output_file_path, index=False)

print(f"Data exported to {output_file_path}")

print(col_names)
print(dict)

with open("list.json","w") as f:
    json.dump(dict,f, indent=3)

print("List.json file successfully exported")