# # from matplotlib import pyplot as plt    
# # #ploting our canvas    
# # plt.plot([1,2,3],[4,5,1])    
# # #display the graph    
# # plt.show()   

# import json
# import os

# current_dir = os.getcwd()
# sector_name = "IT Services & Consulting"
# company_name = "Tata Consultancy Services Ltd"
# file_name = f"{company_name}_total_revenue.json"
# file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{file_name}"

# if os.path.exists(file_path):
#     with open(file_path, 'r') as f:
#         company_data = json.load(f)
    
#     # Print JSON data with indentation for readability
#     # print(json.dumps(company_data, indent=4))
# else:
#     print(f"File not found: {file_path}")


# income = []
# revenue = []
# expenditure = []
# for data in company_data:
#     # print(data)
    
#     if data == "Total Revenue":
#         for d in company_data[data]:
#             income.append(d)

# for data in company_data:
#     if data == "Quarters":
#         for quarter in company_data[data]:
#             total_income_sum = company_data[data][quarter]["total_income"]["sum"]
#             # print("Total income sum:", total_income_sum)
#             revenue.append(total_income_sum)
            
# for data in company_data:
#     if data == "Quarters":
#         for quarter in company_data[data]:
#             total_income_sum = company_data[data][quarter]["total_expenditure"]["sum"]
#             # print("Total income sum:", total_income_sum)
#             expenditure.append(total_income_sum)
            
# print(income)
# print(revenue)
# print(expenditure)

# quarters = []


# for i in range(0,45):
#     quarters.append(f"Q{i+1}")

# print(quarters)


# import matplotlib.pyplot as plt

# # Plotting
# plt.figure(figsize=(10, 6))
# plt.plot(quarters, income, marker='o', color='b', linestyle='-', linewidth=2, markersize=5)

# # Labels and title
# plt.xlabel('Quarters')
# plt.ylabel('Income')
# plt.title(f'{company_name} Income over Quarters')
# plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
# plt.grid(True)

# # Show plot
# plt.tight_layout()
# plt.show()


import json
import os
import matplotlib.pyplot as plt

# Set up file path
current_dir = os.getcwd()
sector_name = "IT Services & Consulting"
company_name = "Tata Consultancy Services Ltd"
file_name = f"{company_name}_total_revenue.json"
file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{file_name}"

# Load JSON data if the file exists
if os.path.exists(file_path):
    with open(file_path, 'r') as f:
        company_data = json.load(f)
else:
    print(f"File not found: {file_path}")
    company_data = {}

# Initialize lists for data
income = []
revenue = []
expenditure = []

# Extract data from JSON
for data in company_data:
    if data == "Total Revenue":
        for d in company_data[data]:
            income.append(d)

for data in company_data:
    if data == "Quarters":
        for quarter in company_data[data]:
            total_income_sum = company_data[data][quarter]["total_income"]["sum"]
            revenue.append(total_income_sum)
            total_expenditure_sum = company_data[data][quarter]["total_expenditure"]["sum"]
            expenditure.append(total_expenditure_sum)

# Generate quarter labels (assuming 45 quarters as in your previous code)
quarters = [f"Q{i+1}" for i in range(len(revenue))]

income = income[:5]
revenue = revenue[:5]
expenditure = expenditure[:5]
quarters = quarters[:5]


print(income, revenue, expenditure)

# Plotting
plt.figure(figsize=(12, 6))

# Plot income, revenue, and expenditure with different colors
plt.plot(quarters, income, marker='o', color='b', linestyle='-', linewidth=2, markersize=5, label='Income')
plt.plot(quarters, revenue, marker='s', color='g', linestyle='--', linewidth=2, markersize=5, label='Revenue')
plt.plot(quarters, expenditure, marker='^', color='r', linestyle='-.', linewidth=2, markersize=5, label='Expenditure')

# Labels and title
plt.xlabel('Quarters')
plt.ylabel('Amount (in crores)')
plt.title(f'{company_name} Financial Data over Quarters(Cr.)')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.legend()  # Show legend for different lines
plt.grid(True)

# Show plot
plt.tight_layout()
plt.show()
