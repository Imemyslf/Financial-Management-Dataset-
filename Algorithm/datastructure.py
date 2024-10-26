# # import re
# # import pandas as pd

# # # Raw text data
# # data_text = """
# # Net Sales/Income from operations	96,486.00	96,351.00	95,193.00	103,521.00	103,758.00
# # Other Operating Income	--	--	--	--	--
# # Total Income From Operations	96,486.00	96,351.00	95,193.00	103,521.00	103,758.00
# # Consumption of Raw Materials	78,851.00	80,966.00	81,095.00	86,124.00	88,365.00
# # Purchase of Traded Goods	1,736.00	1,716.00	13.00	3.00	116.00
# # Increase/Decrease in Stocks	-576.00	-2,120.00	-1,236.00	2,579.00	-185.00
# # Employees Cost	932.00	929.00	948.00	715.00	808.00
# # depreciat	2,227.00	2,024.00	2,275.00	2,143.00	2,233.00
# # Other Expenses	7,308.00	7,330.00	6,042.00	6,478.00	6,805.00
# # P/L Before Other Inc. , Int., Excpt. Items & Tax	6,008.00	5,506.00	6,056.00	5,479.00	5,616.00
# # Other Income	2,140.00	2,046.00	2,036.00	2,305.00	2,060.00
# # P/L Before Int., Excpt. Items & Tax	8,148.00	7,552.00	8,092.00	7,784.00	7,676.00
# # Interest	758.00	324.00	799.00	792.00	805.00
# # P/L Before Tax	7,390.00	7,228.00	7,293.00	6,992.00	6,871.00
# # Tax	1,648.00	1,579.00	1,662.00	1,481.00	1,381.00
# # P/L After Tax from Ordinary Activities	5,742.00	5,649.00	5,631.00	5,511.00	5,490.00
# # Net Profit/(Loss) For the Period	5,742.00	5,649.00	5,631.00	5,511.00	5,490.00
# # Equity Share Capital	3,234.00	3,233.00	3,232.00	3,231.00	3,231.00
# # Equity Dividend Rate (%)	--	--	95.00	--	--
# # Basic EPS	17.70	17.50	17.40	17.10	17.00
# # No Of Shares (Crores)	177.02	176.87	176.79	176.73	176.67
# # Share Holding (%)	54.74	54.71	54.70	54.69	54.69
# # """

# # # Parse the text data
# # lines = data_text.strip().split("\n")
# # data_dict = {}

# # # Iterate over each line and extract numerical data
# # for line in lines:
# #     # Split by tab or whitespace
# #     parts = re.split(r'\t+', line)
# #     param_name = parts[0].strip()
# #     values = parts[1:]

# #     # Filter out non-numeric values and convert to float
# #     numeric_values = []
# #     for value in values:
# #         # Remove commas and check if it can be converted to a float
# #         clean_value = value.replace(',', '').strip()
# #         if clean_value != '--':  # Skip non-numeric entries
# #             numeric_values.append(float(clean_value))

# #     # If there are numeric values, add to the dictionary
# #     if numeric_values:
# #         data_dict[param_name] = numeric_values

# # # Create a DataFrame from the dictionary of numerical parameters
# # df_numerical = pd.DataFrame(data_dict)

# # # Print the structured DataFrame
# # print(df_numerical)


# import re
# import pandas as pd

# # Raw text data
# data_text = """
# Net Sales/Income from operations	96,486.00	96,351.00	95,193.00	103,521.00	103,758.00
# Other Operating Income	--	--	--	--	--
# Total Income From Operations	96,486.00	96,351.00	95,193.00	103,521.00	103,758.00
# Consumption of Raw Materials	78,851.00	80,966.00	81,095.00	86,124.00	88,365.00
# Purchase of Traded Goods	1,736.00	1,716.00	13.00	3.00	116.00
# Increase/Decrease in Stocks	-576.00	-2,120.00	-1,236.00	2,579.00	-185.00
# Employees Cost	932.00	929.00	948.00	715.00	808.00
# depreciat	2,227.00	2,024.00	2,275.00	2,143.00	2,233.00
# Other Expenses	7,308.00	7,330.00	6,042.00	6,478.00	6,805.00
# P/L Before Other Inc. , Int., Excpt. Items & Tax	6,008.00	5,506.00	6,056.00	5,479.00	5,616.00
# Other Income	2,140.00	2,046.00	2,036.00	2,305.00	2,060.00
# P/L Before Int., Excpt. Items & Tax	8,148.00	7,552.00	8,092.00	7,784.00	7,676.00
# Interest	758.00	324.00	799.00	792.00	805.00
# P/L Before Tax	7,390.00	7,228.00	7,293.00	6,992.00	6,871.00
# Tax	1,648.00	1,579.00	1,662.00	1,481.00	1,381.00
# P/L After Tax from Ordinary Activities	5,742.00	5,649.00	5,631.00	5,511.00	5,490.00
# Net Profit/(Loss) For the Period	5,742.00	5,649.00	5,631.00	5,511.00	5,490.00
# Equity Share Capital	3,234.00	3,233.00	3,232.00	3,231.00	3,231.00
# Equity Dividend Rate (%)	--	--	95.00	--	--
# Basic EPS	17.70	17.50	17.40	17.10	17.00
# No Of Shares (Crores)	177.02	176.87	176.79	176.73	176.67
# Share Holding (%)	54.74	54.71	54.70	54.69	54.69
# """

# # Parse the text data
# lines = data_text.strip().split("\n")
# data_dict = {}

# # Iterate over each line and extract numerical data
# for line in lines:
#     # Split by tab or whitespace
#     parts = re.split(r'\t+', line)
#     param_name = parts[0].strip()
#     values = parts[1:]

#     # Filter out non-numeric values and convert to float
#     numeric_values = []
#     for value in values:
#         # Remove commas and check if it can be converted to a float
#         clean_value = value.replace(',', '').strip()
#         if clean_value != '--':  # Skip non-numeric entries
#             numeric_values.append(float(clean_value))

#     # If there are numeric values, add to the dictionary
#     if numeric_values:
#         data_dict[param_name] = numeric_values

# # Identify the maximum length of lists in data_dict
# max_length = max(len(v) for v in data_dict.values())

# # Pad shorter lists with None
# for key in data_dict.keys():
#     while len(data_dict[key]) < max_length:
#         data_dict[key].append(None)

# # Create a DataFrame from the dictionary of numerical parameters
# df_numerical = pd.DataFrame(data_dict)

# # Print the structured DataFrame
# print(df_numerical)


import re
import pandas as pd

# Raw text data
data_text = """
Net Sales/Income from operations	96,486.00	96,351.00	95,193.00	103,521.00	103,758.00
Other Operating Income	--	--	--	--	--
Total Income From Operations	96,486.00	96,351.00	95,193.00	103,521.00	103,758.00
Consumption of Raw Materials	78,851.00	80,966.00	81,095.00	86,124.00	88,365.00
Purchase of Traded Goods	1,736.00	1,716.00	13.00	3.00	116.00
Increase/Decrease in Stocks	-576.00	-2,120.00	-1,236.00	2,579.00	-185.00
Employees Cost	932.00	929.00	948.00	715.00	808.00
depreciat	2,227.00	2,024.00	2,275.00	2,143.00	2,233.00
Other Expenses	7,308.00	7,330.00	6,042.00	6,478.00	6,805.00
P/L Before Other Inc. , Int., Excpt. Items & Tax	6,008.00	5,506.00	6,056.00	5,479.00	5,616.00
Other Income	2,140.00	2,046.00	2,036.00	2,305.00	2,060.00
P/L Before Int., Excpt. Items & Tax	8,148.00	7,552.00	8,092.00	7,784.00	7,676.00
Interest	758.00	324.00	799.00	792.00	805.00
P/L Before Tax	7,390.00	7,228.00	7,293.00	6,992.00	6,871.00
Tax	1,648.00	1,579.00	1,662.00	1,481.00	1,381.00
P/L After Tax from Ordinary Activities	5,742.00	5,649.00	5,631.00	5,511.00	5,490.00
Net Profit/(Loss) For the Period	5,742.00	5,649.00	5,631.00	5,511.00	5,490.00
Equity Share Capital	3,234.00	3,233.00	3,232.00	3,231.00	3,231.00
Equity Dividend Rate (%)	--	--	95.00	--	--
Basic EPS	17.70	17.50	17.40	17.10	17.00
No Of Shares (Crores)	177.02	176.87	176.79	176.73	176.67
Share Holding (%)	54.74	54.71	54.70	54.69	54.69
"""

# Parse the text data
lines = data_text.strip().split("\n")
data_dict = {}

# Iterate over each line and extract numerical data
for line in lines:
    # Split by tab or whitespace
    parts = re.split(r'\t+', line)
    param_name = parts[0].strip()
    values = parts[1:]

    # Filter out non-numeric values and convert to float
    numeric_values = []
    for value in values:
        # Remove commas and check if it can be converted to a float
        clean_value = value.replace(',', '').strip()
        if clean_value != '--':  # Skip non-numeric entries
            numeric_values.append(float(clean_value))

    # If there are numeric values, add to the dictionary
    if numeric_values:
        data_dict[param_name] = numeric_values

# Identify the maximum length of lists in data_dict
max_length = max(len(v) for v in data_dict.values())

# Pad shorter lists with None
for key in data_dict.keys():
    while len(data_dict[key]) < max_length:
        data_dict[key].append(None)

# Create a DataFrame from the dictionary of numerical parameters
df_numerical = pd.DataFrame(data_dict)

# Save the DataFrame to an Excel file
output_file = 'reliance_quarterly_results.xlsx'  # Define the output file name
df_numerical.to_excel(output_file, index=False)  # Save DataFrame to Excel

# Print the DataFrame (optional)
print(df_numerical)
print(f'DataFrame saved to {output_file}')
