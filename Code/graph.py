#################### Indiviual Normal Graph #######################
# import json
# import os
# import matplotlib.pyplot as plt

# # Set up file path
# current_dir = os.getcwd()

# def plotting_the_graph(sector_name,company_name):
#     global current_dir
#     file_name = f"{company_name}_total_revenue.json"
#     file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{file_name}"

#     # Load JSON data if the file exists
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             company_data = json.load(f)
#         print("Successfully loaded")
#     else:
#         print(f"File not found: {file_path}")
#         company_data = {}

#     # print(company_data["Quarters"])

#     # Initialize lists for data
#     income = []
#     revenue = []
#     expenditure = []

#     # Extract data from JSON
#     if "Quarters" in company_data:
#         for quarter,quarter_data in company_data["Quarters"].items():
#             # print(quarter,quarter_data)
            
#             if "Income" in quarter_data and "Total Income From Operations" in quarter_data["Income"]:
#                 income_value = quarter_data["Income"]["Total Income From Operations"]
#                 income.append(income_value)
#                 # print(f"Total Income From Operations for {quarter}: {income_value}")
            
#             if "Expenditure" in quarter_data:
#                 expenditure_sum = sum(quarter_data["Expenditure"].values())
#                 expenditure.append(expenditure_sum)
#                 # print(f"Total Expenditure for {quarter}: {expenditure_sum}")
            
#             if "Profit" in quarter_data and "Net Profit" in quarter_data["Profit"]:
#                 revenue_value = quarter_data["Profit"]["Net Profit"]
#                 revenue.append(revenue_value)
#                 # print(f"Net Profit for {quarter}: {revenue_value}")

#     # Generate quarter labels (assuming 45 quarters as in your previous code)
#     quarters = [f"Q{i+1}" for i in range(len(revenue))]

#     # income = income[:5]
#     # revenue = revenue[:5]
#     # expenditure = expenditure[:5]
#     # quarters = quarters[:5]

#     # Plotting
#     plt.figure(figsize=(12, 6))

#     # Plot income, revenue, and expenditure with different colors
#     plt.plot(quarters, income, marker='o', color='b', linestyle='-', linewidth=2, markersize=5, label='Income')
#     plt.plot(quarters, revenue, marker='s', color='g', linestyle='--', linewidth=2, markersize=5, label='Revenue')
#     plt.plot(quarters, expenditure, marker='^', color='r', linestyle='-.', linewidth=2, markersize=5, label='Expenditure')

#     # Labels and title
#     plt.xlabel('Quarters')
#     plt.ylabel('Amount (in crores)')
#     plt.title(f'{company_name} Financial Data over Quarters(Cr.)')
#     plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
#     plt.legend()  # Show legend for different lines
#     plt.grid(True)

#     # Show plot
#     plt.tight_layout()
#     plt.show()

# def plot_graph():
#     sector_path = f"{current_dir}/Companies"
    
#     sector_dir_list = os.listdir(sector_path)
    
#     for sector in sector_dir_list:
#         if sector == "IT Services & Consulting":
#             company_path = os.path.join(sector_path,sector)
            
#             company_dir_list = os.listdir(company_path)
            
#             for company in company_dir_list:
#                 # if company == "Tata Consultancy Services Ltd":
#                     file_name = f"{company}_combined_excel_file.xlsx"
#                     plotting_the_graph(sector,company)
                    
                    
# if __name__ == '__main__':
#     plot_graph()
    

#################### Indiviual Normalized Graph #######################
# import json
# import os
# import matplotlib.pyplot as plt

# # Set up file path
# current_dir = os.getcwd()

# def normalize(data):
#     """Normalize data to be between 0 and 1."""
#     min_val = min(data)
#     max_val = max(data)
#     return [(x - min_val) / (max_val - min_val) for x in data] if max_val > min_val else data

# def plotting_the_graph(sector_name,company_name):
#     global current_dir
#     file_name = f"{company_name}_total_revenue.json"
#     file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{file_name}"

#     # Load JSON data if the file exists
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             company_data = json.load(f)
#         print("Successfully loaded")
#     else:
#         print(f"File not found: {file_path}")
#         company_data = {}

#     # print(company_data["Quarters"])

#     # Initialize lists for data
#     income = []
#     revenue = []
#     expenditure = []

#     # Extract data from JSON
#     if "Quarters" in company_data:
#         for quarter,quarter_data in company_data["Quarters"].items():
#             # print(quarter,quarter_data)
            
#             if "Income" in quarter_data and "Total Income From Operations" in quarter_data["Income"]:
#                 income_value = quarter_data["Income"]["Total Income From Operations"]
#                 income.append(income_value)
#                 # print(f"Total Income From Operations for {quarter}: {income_value}")
            
#             if "Expenditure" in quarter_data:
#                 expenditure_sum = sum(quarter_data["Expenditure"].values())
#                 expenditure.append(expenditure_sum)
#                 # print(f"Total Expenditure for {quarter}: {expenditure_sum}")
            
#             if "Profit" in quarter_data and "Net Profit" in quarter_data["Profit"]:
#                 revenue_value = quarter_data["Profit"]["Net Profit"]
#                 revenue.append(revenue_value)
#                 # print(f"Net Profit for {quarter}: {revenue_value}")
    
#     # Normalize data
#     income = normalize(income)
#     revenue = normalize(revenue)
#     expenditure = normalize(expenditure)

#     # Generate quarter labels (assuming 45 quarters as in your previous code)
#     quarters = [f"Q{i+1}" for i in range(len(revenue))]

#     # income = income[:5]
#     # revenue = revenue[:5]
#     # expenditure = expenditure[:5]
#     # quarters = quarters[:5]

#     # Plotting
#     plt.figure(figsize=(12, 6))

#     # Plot income, revenue, and expenditure with different colors
#     plt.plot(quarters, income, marker='o', color='b', linestyle='-', linewidth=2, markersize=5, label='Income')
#     plt.plot(quarters, revenue, marker='s', color='g', linestyle='--', linewidth=2, markersize=5, label='Revenue')
#     plt.plot(quarters, expenditure, marker='^', color='r', linestyle='-.', linewidth=2, markersize=5, label='Expenditure')

#     # Labels and title
#     plt.xlabel('Quarters')
#     plt.ylabel('Amount (in crores)')
#     plt.title(f'{company_name} Financial Data over Quarters(Cr.)')
#     plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
#     plt.legend()  # Show legend for different lines
#     plt.grid(True)

#     # Show plot
#     plt.tight_layout()
#     plt.show()

# def plot_graph():
#     sector_path = f"{current_dir}/Companies"
    
#     sector_dir_list = os.listdir(sector_path)
    
#     for sector in sector_dir_list:
#         if sector == "IT Services & Consulting":
#             company_path = os.path.join(sector_path,sector)
            
#             company_dir_list = os.listdir(company_path)
            
#             for company in company_dir_list:
#                 # if company == "Tata Consultancy Services Ltd":
#                     file_name = f"{company}_combined_excel_file.xlsx"
#                     plotting_the_graph(sector,company)
                    
                    
# if __name__ == '__main__':
#     plot_graph()


####################### Single Company normaql and normalized ######################
import json
import os
import numpy as np
import matplotlib.pyplot as plt

# Set up file path
current_dir = os.getcwd()

# def normalize(data):
#     """Normalize data to be between 0 and 1.(Min-Max)"""
#     min_val = min(data)
#     max_val = max(data)
#     return [(x - min_val) / (max_val - min_val) for x in data] if max_val > min_val else data

def normalize(data):
    """Normalize data using Z-score normalization."""
    mean_val = np.mean(data)
    std_val = np.std(data)
    print(std_val)
    print([(x - mean_val) / std_val for x in data] if std_val != 0 else data)
    return [(x - mean_val) / std_val for x in data] if std_val != 0 else data

def plotting_the_graph(sector_name, company_name):
    global current_dir
    file_name = f"{company_name}_total_revenue.json"
    file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{file_name}"

    # Load JSON data if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            company_data = json.load(f)
        print("Successfully loaded")
    else:
        print(f"File not found: {file_path}")
        company_data = {}

    # Initialize lists for data
    revenue_1 = []
    profit_1 = []
    expenditure_1 = []

    # Extract data from JSON
    if "Quarters" in company_data:
        for quarter, quarter_data in company_data["Quarters"].items():
            if "Income" in quarter_data and "Total Income From Operations" in quarter_data["Income"]:
                income_value = quarter_data["Income"]["Total Income From Operations"]
                revenue_1.append(income_value)
            
            if "Expenditure" in quarter_data:
                expenditure_sum = sum(quarter_data["Expenditure"].values())
                expenditure_1.append(expenditure_sum)
            
            if "Profit" in quarter_data and "Net Profit" in quarter_data["Profit"]:
                revenue_value = quarter_data["Profit"]["Net Profit"]
                profit_1.append(revenue_value)
    
    # Create copies of the original data for the non-normalized plot
    revenue_2 = revenue_1[:]
    profit_2 = profit_1[:]
    expenditure_2 = expenditure_1[:]
    
    # Normalize data for the normalized plot
    revenue_1 = normalize(revenue_1)
    profit_1 = normalize(profit_1)
    expenditure_1 = normalize(expenditure_1)

    # Generate quarter labels (assuming 45 quarters as in your previous code)
    quarters = [f"Q{i+1}" for i in range(len(profit_1))]

    # Create a 1x2 subplot layout
    fig, axs = plt.subplots(1, 2, figsize=(15, 6), constrained_layout=True)
    fig.suptitle(f'{company_name} Financial Data over Quarters', fontsize=16)

    # First subplot (Normalized Data)
    axs[0].plot(quarters, revenue_1, marker='o', color='b', linestyle='-', linewidth=2, markersize=5, label='Normalized Revenue')
    axs[0].plot(quarters, expenditure_1, marker='^', color='r', linestyle='-.', linewidth=2, markersize=5, label='Normalized Expenditure')
    axs[0].plot(quarters, profit_1, marker='s', color='g', linestyle='--', linewidth=2, markersize=5, label='Normalized Profit')
    axs[0].set_xlabel('Quarters')
    axs[0].set_ylabel('Normalized Value ')
    axs[0].set_title('Normalized Data')
    axs[0].legend()
    axs[0].grid(True)
    axs[0].tick_params(axis='x', rotation=45)

    # Second subplot (Original Data)
    axs[1].plot(quarters, revenue_2, marker='o', color='b', linestyle='-', linewidth=2, markersize=5, label='Revenue')
    axs[1].plot(quarters, expenditure_2, marker='^', color='r', linestyle='-.', linewidth=2, markersize=5, label='Expenditure')
    axs[1].plot(quarters, profit_2, marker='s', color='g', linestyle='--', linewidth=2, markersize=5, label='Profit')
    axs[1].set_xlabel('Quarters')
    axs[1].set_ylabel('Amount (in crores)')
    axs[1].set_title('Original Data')
    axs[1].legend()
    axs[1].grid(True)
    axs[1].tick_params(axis='x', rotation=45)

    # Show plot
    plt.show()

def plot_graph():
    sector_path = f"{current_dir}/Companies"
    
    sector_dir_list = os.listdir(sector_path)
    
    for sector in sector_dir_list:
        if sector == "IT Services & Consulting":
            company_path = os.path.join(sector_path, sector)
            
            company_dir_list = os.listdir(company_path)
            
            for company in company_dir_list:
                if company == "Tata Consultancy Services Ltd":
                    plotting_the_graph(sector, company)
                    
                    
if __name__ == '__main__':
    plot_graph()


######################### NORMAL DATA #########################
# import json
# import os
# import matplotlib.pyplot as plt

# # Set up file path
# current_dir = os.getcwd()

# def plotting_the_graph(sector_name, company_name, ax):
#     file_name = f"{company_name}_total_revenue.json"
#     file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{file_name}"

#     # Load JSON data if the file exists
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             company_data = json.load(f)
#         print(f"Successfully loaded data for {company_name}")
#     else:
#         print(f"File not found: {file_path}")
#         return

#     # Initialize lists for data
#     income = []
#     revenue = []
#     expenditure = []

#     # Extract data from JSON
#     if "Quarters" in company_data:
#         for quarter, quarter_data in company_data["Quarters"].items():
#             if "Income" in quarter_data and "Total Income From Operations" in quarter_data["Income"]:
#                 income_value = quarter_data["Income"]["Total Income From Operations"]
#                 income.append(income_value)
            
#             if "Expenditure" in quarter_data:
#                 expenditure_sum = sum(quarter_data["Expenditure"].values())
#                 expenditure.append(expenditure_sum)
            
#             if "Profit" in quarter_data and "Net Profit" in quarter_data["Profit"]:
#                 revenue_value = quarter_data["Profit"]["Net Profit"]
#                 revenue.append(revenue_value)

#     # Generate quarter labels
#     quarters = [f"Q{i+1}" for i in range(len(revenue))]

#     # Plot income, revenue, and expenditure on the given subplot
#     ax.plot(quarters, income, marker='o', color='b', linestyle='-', linewidth=2, markersize=5, label='Income')
#     ax.plot(quarters, revenue, marker='s', color='g', linestyle='--', linewidth=2, markersize=5, label='Revenue')
#     ax.plot(quarters, expenditure, marker='^', color='r', linestyle='-.', linewidth=2, markersize=5, label='Expenditure')

#     # Customize each subplot
#     ax.set_xlabel('Quarters')
#     ax.set_ylabel('Amount (in crores)')
#     ax.set_title(f'{company_name} Financial Data')
#     ax.legend()
#     ax.grid(True)

# def plot_graph():
#     sector_path = f"{current_dir}/Companies"
#     sector_dir_list = os.listdir(sector_path)

#     # Filter out specific sector and companies
#     selected_sector = "IT Services & Consulting"
#     selected_companies = []

#     # Collect list of companies under the selected sector
#     for sector in sector_dir_list:
#         if sector == selected_sector:
#             company_path = os.path.join(sector_path, sector)
#             selected_companies = os.listdir(company_path)
#             break

#     # Set up figure with 2x2 subplots
#     fig, axs = plt.subplots(2, 2, figsize=(16, 10))
#     fig.suptitle('Financial Data Comparison for IT Services & Consulting Companies', fontsize=16)

#     # Flatten the 2x2 grid to iterate over it
#     axs = axs.flatten()

#     # Plot each company in a subplot
#     for i, company_name in enumerate(selected_companies):
#         if i < 4:  # Limit to 4 companies
#             if os.path.isdir(os.path.join(sector_path, selected_sector, company_name)):
#                 plotting_the_graph(selected_sector, company_name, axs[i])

#     # Adjust layout and show plot
#     plt.tight_layout(rect=[0, 0.03, 1, 0.95])
#     plt.show()

# if __name__ == '__main__':
#     plot_graph()



######################### NORMALIZED DATA #########################
# import json
# import os
# import matplotlib.pyplot as plt

# # Set up file path
# current_dir = os.getcwd()

# def normalize(data):
#     """Normalize data to be between 0 and 1."""
#     min_val = min(data)
#     max_val = max(data)
#     return [(x - min_val) / (max_val - min_val) for x in data] if max_val > min_val else data

# def plotting_the_graph(sector_name, company_name, ax):
#     file_name = f"{company_name}_total_revenue.json"
#     file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{file_name}"

#     # Load JSON data if the file exists
#     if os.path.exists(file_path):
#         with open(file_path, 'r') as f:
#             company_data = json.load(f)
#         print(f"Successfully loaded data for {company_name}")
#     else:
#         print(f"File not found: {file_path}")
#         return

#     # Initialize lists for data
#     income = []
#     revenue = []
#     expenditure = []

#     # Extract data from JSON
#     if "Quarters" in company_data:
#         for quarter, quarter_data in company_data["Quarters"].items():
#             if "Income" in quarter_data and "Total Income From Operations" in quarter_data["Income"]:
#                 income_value = quarter_data["Income"]["Total Income From Operations"]
#                 income.append(income_value)
            
#             if "Expenditure" in quarter_data:
#                 expenditure_sum = sum(quarter_data["Expenditure"].values())
#                 expenditure.append(expenditure_sum)
            
#             if "Profit" in quarter_data and "Net Profit" in quarter_data["Profit"]:
#                 revenue_value = quarter_data["Profit"]["Net Profit"]
#                 revenue.append(revenue_value)

#     # Normalize data
#     income = normalize(income)
#     revenue = normalize(revenue)
#     expenditure = normalize(expenditure)

#     # Generate quarter labels
#     quarters = [f"Q{i+1}" for i in range(len(revenue))]

#     # Plot normalized income, revenue, and expenditure on the given subplot
#     ax.plot(quarters, income, marker='o', color='b', linestyle='-', linewidth=2, markersize=5, label='Normalized Income')
#     ax.plot(quarters, revenue, marker='s', color='g', linestyle='--', linewidth=2, markersize=5, label='Normalized Revenue')
#     ax.plot(quarters, expenditure, marker='^', color='r', linestyle='-.', linewidth=2, markersize=5, label='Normalized Expenditure')

#     # Customize each subplot
#     ax.set_xlabel('Quarters')
#     ax.set_ylabel('Normalized Value (0-1)')
#     ax.set_title(f'{company_name} Financial Data (Normalized)')
#     ax.legend()
#     ax.grid(True)

# def plot_graph():
#     sector_path = f"{current_dir}/Companies"
#     sector_dir_list = os.listdir(sector_path)

#     # Filter out specific sector and companies
#     selected_sector = "IT Services & Consulting"
#     selected_companies = []

#     # Collect list of companies under the selected sector
#     for sector in sector_dir_list:
#         if sector == selected_sector:
#             company_path = os.path.join(sector_path, sector)
#             selected_companies = os.listdir(company_path)
#             break

#     # Set up figure with 2x2 subplots
#     fig, axs = plt.subplots(2, 2, figsize=(16, 10))
#     fig.suptitle('Normalized Financial Data Comparison for IT Services & Consulting Companies', fontsize=16)

#     # Flatten the 2x2 grid to iterate over it
#     axs = axs.flatten()

#     # Plot each company in a subplot
#     for i, company_name in enumerate(selected_companies):
#         if i < 4:  # Limit to 4 companies
#             if os.path.isdir(os.path.join(sector_path, selected_sector, company_name)):
#                 plotting_the_graph(selected_sector, company_name, axs[i])

#     # Adjust layout and show plot
#     plt.tight_layout(rect=[0, 0.03, 1, 0.95])
#     plt.show()

# if __name__ == '__main__':
#     plot_graph()
