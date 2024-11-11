import pandas as pd
import os
import json

current_dir = os.getcwd()
file_name = "combined_excel_file.xlsx"

def company_data_json(sector_name,company_name,file_name):
    file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{file_name}"
    

    # Load the Excel file
    data = pd.read_excel(file_path)


    quarters_list = []

    for i in range(0,45):
        quarters_list.append(f"Q{i+1}")
        
        
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
    income_labels = ['Total Income From Operations']
    expenditure_labels = [
        "Consumption of Raw Materials",
        "Purchase of Traded Goods",
        "Increase/Decrease in Stocks",
        "Power & Fuel",
        "Employees Cost",
        "depreciat",
        "Excise Duty",
        "Admin. And Selling Expenses",
        "R & D Expenses",
        "Provisions And Contingencies",
        "Exp. Capitalised",
        "Other Expenses"
    ]

    # Filter data for Income and Expenditure rows
    income_data = data[data[parameter_name[0]].isin(income_labels)].copy()
    expenditure_data = data[data[parameter_name[0]].isin(expenditure_labels)].copy()

    # Convert non-numeric values to NaN, then fill NaN with 0
    income_data.loc[:, col_name] = income_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)
    expenditure_data.loc[:, col_name] = expenditure_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Prepare the dictionary for the output JSON
    quarters_dict = {}
    total_profit_list = {}

    # Loop over each quarter and calculate total income, expenditure, and profit
    for quarter in col_name:
        total_income = income_data[quarter].sum()
        total_expenditure = expenditure_data[quarter].sum()
        total_profit = total_income - total_expenditure
        total_profit_list[quarter] = round(float(total_profit), 3)
        
        # Construct the dictionary for each quarter with income and expenditure labels
        quarters_dict[quarter] = {
            "Income":{
                # income_labels[0]: round(float(val), 3) for val in income_data[quarter].tolist()     
                label : round(float(val), 3) for label,val in zip(income_labels, income_data[quarter].tolist())      
            },
            
            "Expenditure": {
                label: round(float(val), 3) for label, val in zip(expenditure_labels, expenditure_data[quarter].tolist())
            },        
            "Profit": {
                "Total Income sum": round(float(total_income), 3),
                "Total Expenditure_sum": round(float(total_expenditure), 3),
                "Total Profit": round(float(total_profit), 3)
            }
        }

    list_profit = list(total_profit_list.values())
    # print(list(total_profit_list.values()))


    total_profit_list = {    
        quarters_list[i]: list_profit[i] for i in range(0,45)
    }

    # print(total_profit_list)

    # Create the final data dictionary
    final_data_dict = {
        "Quarters": quarters_dict,
        "Total Profit for each quarter": total_profit_list  # Format quarters and profits in the required format
    }

    # Print the quarters_dict to check the structure
    print(json.dumps(final_data_dict, indent=4))

    # Save to JSON
    output_file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{company_name}_total_revenue.json"
    with open(output_file_path, "w") as json_file:
        json.dump(final_data_dict, json_file, indent=4)

    print(f"Total revenue data saved to {output_file_path}")

def complete_file():
    sector_path = f"{current_dir}/Companies"
    
    sector_dir_list = os.listdir(sector_path)
    
    for sector in sector_dir_list:
        company_path = os.path.join(sector_path,sector)
        
        company_dir_list = os.listdir(company_path)
        
        for company in company_dir_list:
            # print(f"{company}")
            file_path = os.path.join(company_path,company,"Pruned_Excel",file_name)
            print("\n",file_path)
            
            company_data_json(sector,company,file_name)
        
    
    pass
if __name__ == '__main__':
    complete_file()
