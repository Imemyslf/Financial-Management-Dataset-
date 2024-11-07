import pandas as pd
import os
import pandas as pd
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment

current_dir = os.getcwd()

def prune_data(sector_name,company_name,file):
    global current_dir
    print(current_dir)
    
    file_name = f"{current_dir}/Companies/{sector_name}/{company_name}/Excel/{file}"
    
    df = pd.read_excel(file_name)

    col_names = list(df.columns)
    print(col_names) 
    # print(df.columns)

    data_list = df.values.tolist()
    
    param = []

    output_data = []
    # dict = {}
            
    
    def isValid(data):
        return not ( data == '--')

    for row in data_list:
        company, *values = row
        if any(isValid(value) for value in values):
            output_data.append([company] + values)
            # dict[company] = values

    # print("Output data:-",output_data)

    def isValids(val):
        if(str(val) == "nan" ):
            return True
        else:
            return False
        
    for row in output_data:
        paramter, *values = row
        print(values)
        values.append("")
        
        if any(isValids(value) for value in values):
            param.append([""])
            param.append([paramter] + values)
        else:
            # print(values)
            float_list = [float(value.replace(',', '')) if value not in ["", "--"] else value for value in values]

            minus_float_list = [v for v in float_list if isinstance(v, float)]
            # print("\n\nMinus float 2:- ",minus_float_list,"\n")
            
            max_val = max(value for value in minus_float_list)
            min_val = min(value for value in minus_float_list)
            avg = sum(minus_float_list) /len(minus_float_list)
            
            param.append([paramter] + values + []+[max_val] + [min_val] + [avg])

    
    print("\nData:- \n",param)

    col_name = col_names[0]
    quaters = col_names[1:]

    print(col_name,quaters)
    output_file_path = f"{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{file}"
    print("\n\nCurrent dir:- ",output_file_path)
    
    output_df = pd.DataFrame(param,columns=[str(col_name)]+col_names[1:]+[""]+["Max"]+["Min"]+["Avg"])
    

    output_df.to_excel(output_file_path,index=False)
    print("\n\n\nSuccessfully saved the file in:- ",output_file_path)
    spacexcel(output_file_path,sector_name,company_name,file)

def spacexcel(output_file_path,sector_name,company_name,file):
    global current_dir
    # file_path = r'C:\Users\sharm\OneDrive\Desktop\Kishan\Contractzy\WebScrapping\Tutorial\Code\7_Mar21_Mar22.xlsx' 
    file_path = f'{output_file_path}' 
    workbook = load_workbook(file_path)
    sheet = workbook.active

    # Increase column width and center-align numeric values
    for col in sheet.columns:
        max_length = 0
        col_letter = get_column_letter(col[0].column)  # Column letter for setting width

        for cell in col:
            # Center align numeric values
            if isinstance(cell.value, (int, float)):
                cell.alignment = Alignment(horizontal='center')
            
            # Calculate the maximum length of the cell values in the column
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))

        # Set the column width slightly wider than the max length
        sheet.column_dimensions[col_letter].width = max_length + 2

    # Save the modified Excel file
    output_path = f'{current_dir}/Companies/{sector_name}/{company_name}/Pruned_Excel/{file}'  # Choose your preferred output path
    print("Output path:- ",output_path)
    workbook.save(output_path)
    print("\n\n\nSuccessfully saved the file in:- ",output_path)

if __name__ == '__main__':
    current_dir = os.getcwd()
    sector_name = "Trading"
    company_name  = "Adani Enterprises Ltd"
    # file = "3_Mar16_Mar17.xlsx"
    
    # prune_data(sector_name,company_name,file)
    path = f"{current_dir}/Companies/{sector_name}/{company_name}/Excel"
    print(path)
    
    dir_list = os.listdir(path)
       
    for dir in dir_list:
        print("\n\nFile name:- ",dir,"\n")
        prune_data(sector_name,company_name,dir)
        
