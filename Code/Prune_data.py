import pandas as pd
import os
import json
current_dir = os.getcwd()

sector_name = "Bank - Private"
company_name  = "HDFC Bank Ltd"
file = "9_Sep24_Sep23.xlsx"
# print(current_dir)
file_name = f"{current_dir}/Companies/{sector_name}/{company_name}/Excel/{file}"
# print(file_name)
df = pd.read_excel(file_name)

col_names = list(df.columns)
print(col_names) 
# print(df.columns)

data_list = df.values.tolist()
print(data_list)


for row in data_list:
    paramter, *values = row
    # print(paramter)
    # print(values)


# with open("data.json","w") as f:
#     json.dump(data,f, indent=4)
#     print("data.json file successfully exported")
# print(df.index)
# print(df)