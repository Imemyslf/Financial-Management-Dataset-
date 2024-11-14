import os
import json

current_dir = os.getcwd()


def analyze_company_performance(json_list, start_quarter, parameters,n):
    # Dictionary to hold best performance data for each company
    best_performance = {}
    sum_of_parameters = []
    
    # Loop through each company's data in json_list
    for company_data in json_list:
        for company, data in company_data.items():
            print(company)
            quarters = data['Quarters']
            quarter_keys = list(quarters.keys())
            if start_quarter not in quarter_keys:
                print(f"{start_quarter} not found for company {company}. Skipping...")
                continue

            start_index = quarter_keys.index(start_quarter)

            # Check if there are enough quarters from the starting index
            if start_index + n > len(quarter_keys):
                print(f"Not enough quarters from {start_quarter} for company {company}. Skipping...")
                continue
            
            # Store best-performing data for each specified expenditure factor over four quarters
            # Initialize the factor sums for this company
            best_performance[company] = {factor: 0 for factor in parameters}

            # Aggregate sums over the specified four quarters
            for i in range(start_index, start_index + n):
                quarter = quarter_keys[i]
                expenditures = quarters[quarter]['Expenditure']
                
                for factor, value in expenditures.items():
                    # Check if factor is in the specified parameters to be compared
                    if factor in parameters:
                        best_performance[company][factor] += value

            # Append the cumulative data for this company to sum_of_parameters only once
            sum_of_parameters.append({company: best_performance[company]})
            # print ("\n\n",sum_of_parameters)
            
    best_for_each_factor = {factor: {"company": None, "value": 0} for factor in parameters}
    
    for entry in sum_of_parameters:
        for company, factors in entry.items():
            for factor, total in factors.items():
                # Update the best performance if the current company's total is higher
                if total > best_for_each_factor[factor]["value"]:
                    best_for_each_factor[factor] = {"company": company, "value": total}

    # Display the best-performing company for each factor
    print("\nBest Performing Companies by Factor:")
    for factor, data in best_for_each_factor.items():
        print(f"{factor}: {data['company']} with a value of {data['value']}")
                        
            # print("\n\n",best_performance,"\n")
    print("\nBest Performing Companies by Factor with Quarterly Breakdown:")
    for factor, data in best_for_each_factor.items():
        best_company = data["company"]
        best_value = data["value"]
        
        print(f"\n{factor}: {best_company} with a value of {best_value}")
        
        # Find and display quarterly values for the best company and factor
        for company_data in json_list:
            if best_company in company_data:
                quarters = company_data[best_company]['Quarters']
                
                for i in range(start_index, start_index + n):
                    quarter = quarter_keys[i]
                    if factor in quarters[quarter]['Expenditure']:
                        print(f"\n{quarter}:")
                        print(f"    {factor}: {quarters[quarter]['Expenditure'][factor]}")


if __name__ == '__main__':
    json_list = []
    company_json_data = {}
    sector_path = f"{current_dir}/Companies"
    
    sector_dir_list = os.listdir(sector_path)
    
    for sector in sector_dir_list:
        if sector == "IT Services & Consulting":
            company_path = os.path.join(sector_path, sector)
            
            company_dir_list = os.listdir(company_path)
            
            for company in company_dir_list:
                # if company == "Tata Consultancy Services Ltd":
                file_path = f"{company_path}/{company}/{company}_total_revenue.json"
                
                with open(file_path,'r') as f:
                    company_json_data = {
                        company:json.load(f)
                    }
                    json_list.append(company_json_data)
                    company_json_data = {}
    
    parameters = ['Employees Cost', 'depreciat', 'Other Expenses']
    start_quarter = "Dec '21"
    n = 8

    # Call the function with user-specified parameters
    results = analyze_company_performance(json_list, start_quarter, parameters,n)
    # print(results)
    # display_formatted_results(results)
