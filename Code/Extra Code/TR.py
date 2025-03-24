import pandas as pd
import os
import json

current_dir = os.getcwd()
file_name = "combined_excel_file.xlsx"

def company_data_json(sector_name,company_name,file_name):
    file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{file_name}"
    
    data = pd.read_excel(file_path)

    quarters_list = []

    for i in range(0,45):
        quarters_list.append(f"Q{i+1}")
        
    parameter_name = list(data.columns)
    col_name = list(data.columns[1:])

    data_list = data.values.tolist()
    list_data = [str(data[0]) for data in data_list]
    
    extracted_data = []
    
    temp = []
    for item in list_data:
        if item == 'nan' and temp:
            extracted_data.append(temp)
            temp = []
        elif item != 'nan':
            temp.append(item)
    
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
    
    income_data = data[data[parameter_name[0]].isin(income_labels)].copy()
    expenditure_data = data[data[parameter_name[0]].isin(expenditure_labels)].copy()
    
    income_data.loc[:, col_name] = income_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)
    expenditure_data.loc[:, col_name] = expenditure_data[col_name].apply(pd.to_numeric, errors='coerce').fillna(0)

    in_selected_label = []
    in_selected_list  = income_data.values.tolist()

    for i in in_selected_list:
        in_selected_label.append(i[0])

    # print(in_selected_label)

    exp_selected_label = []
    exp_list = expenditure_data.values.tolist()
    for i in exp_list:
        exp_selected_label.append(i[0])
    
    # print(exp_selected_label)
    
    quarters_dict = {}
    total_profit_list = {}
    
    for quarter in col_name:
        total_income = income_data[quarter].sum()
        total_expenditure = expenditure_data[quarter].sum()
        total_profit = total_income - total_expenditure
        total_profit_list[quarter] = round(float(total_profit), 3)
            
        var = "Net Profit" if total_profit >= 0  else "Net Loss"
        
        quarters_dict[quarter] = {
            "Income":{
                
                label : round(float(val), 3) for label,val in zip(in_selected_label, income_data[quarter].tolist())      
            },
            
            "Expenditure": {
                label: round(float(val), 3) for label, val in zip(exp_selected_label, expenditure_data[quarter].tolist())
            },        
            "Profit": {
                "Total Income sum": round(float(total_income), 3),
                "Total Expenditure_sum": round(float(total_expenditure), 3),
                var: round(float(total_profit), 3)
            }
        }

    list_profit = list(total_profit_list.values())

    # print(list_profit)
    diff_list = []
    percen_list = []
    percen_dict = []
    for i,data in enumerate(list_profit):
        if i >= 0 and i < len(list_profit) - 1:
            # print(i,list_profit[i],list_profit[i+1])
            diff = list_profit[i+1] - list_profit[i]
            diff_list.append(diff)
            
            percentage = ((diff)/list_profit[i]) * 100
            percen_list.append(percentage)
            # print(f"differnece:- {diff} \n\n percentage:- {percentage}")
    
    for i in range(0, len(percen_list)):
        # print(f"\n\n {i} difference:- {diff_list[i]} \n\n percentage:- {percen_list[i]}")        
        entry = {
            "Difference": round(float(diff_list[i]),3),
            "Percentage": str(round(float(percen_list[i]),2)) + " %",
        }        
        percen_dict.append(entry) 
    
    percen_dict.insert(0,{"Difference": 0,"Percentage": 0})
    # print(f"{len(percen_dict)}")
    total_profit_list = {    
        quarters_list[i]: {
            "Profit": list_profit[i],
            "Difference and Percentage": percen_dict[i]
        } for i in range(len(list_profit))
    }
    print(total_profit_list)
    
        
    final_data_dict = {
        "Quarters": quarters_dict,
        "Total Profit for each quarter": total_profit_list  
    }
            
    output_file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/{company_name}_total_revenue.json"
    with open(output_file_path, "w") as json_file:
        json.dump(final_data_dict, json_file, indent=4)

    print(f"Total revenue data saved to {output_file_path}")

def complete_file():
    sector_path = f"{current_dir}/Companies"
    
    sector_dir_list = os.listdir(sector_path)
    
    for sector in sector_dir_list:
        if sector == "IT Services & Consulting":
            company_path = os.path.join(sector_path,sector)
            
            company_dir_list = os.listdir(company_path)
            
            for company in company_dir_list:
                # if company == "Tata Consultancy Services Ltd":
                    file_name = f"{company}_combined_excel_file.xlsx"
                    
                    company_data_json(sector,company,file_name)
        
    
    pass
if __name__ == '__main__':
    complete_file()