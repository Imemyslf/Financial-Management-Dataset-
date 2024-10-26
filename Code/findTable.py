import requests
from bs4 import BeautifulSoup
import pandas as pd  
import os

def make_main_dir(base_dir):
    try:
        os.mkdir(base_dir)
        print("Companies directory created successfully")
        
    except FileExistsError as e:
        print("File already exists in  directory") 
        
    except PermissionError as e:
        print("Permission denied",e)
        return False
    except Exception as e:
        print("An Error Occured while creating the directory",e)
        return False


def append_sector(final_sector_name):
    
    def insert_sector(count,final_sector_name):
        with open(path,"a") as f:
            f.write(str(f"{count + 1} {final_sector_name}\n"))
        pass
    path = "../Companies/sector.txt"
    with open(path,"r") as f:
        data = f.read() 
    
    count = 0  
    if data:
        print("data:",data)
        new_data = data.split()
        print(new_data)
        last_digit = next(int(item) for item in reversed(data) if item.isdigit())
        print(last_digit)
        
        insert_sector(last_digit,final_sector_name)
    else:
        print("data unavialbale:",data)
        insert_sector(count,final_sector_name)
        
    
    
    # with open(path,"a") as f:
    #     f.write(str(f"{integer + 1} {final_sector_name}\n"))
        


def create_company_directory(directory):    
    try: 
        os.makedirs(directory)
        print(f"{directory} directory created successfully")
    except FileExistsError as e:
        print("File already exists or Error in creating directory",e) 
    except PermissionError as e:
        print("Permission denied",e)
        return False
    except Exception as e:
        print("An Error Occured while creating the directory",e)
        return False


def create_excel_file(path,base_dir,file_name):
    print("Creating")
    with open(path,"r",encoding="utf-8") as f:
        html_content = f.read()
    
    soup = BeautifulSoup(html_content,"html.parser")
    # print(soup.prettify())
    
    table = soup.find(class_="mctable1")
    # print(table)
    
    table_data = []
    rows = table.find_all("tr")
    
    for i,rows in enumerate(rows):  
        cols = rows.find_all(["td","th"])
        col_text =[ col.get_text(strip="\n\t") for col in cols]
        table_data.append(col_text)
        
    df = pd.DataFrame(table_data[1:], columns=table_data[0])  
    
    
    new_path = "../data/AdaniPorts/QuarterlyExcel"
    output = create_company_directory(new_path)
    if output != False:
        df.to_excel(f"{base_dir}/QuarterlyExcel/{file_name}", index=False)
        
        
if __name__ == "__main__": 
    # path = "../data/AdaniPorts/Quarterly10Yrs/9_Jun23_Jun24.html" 
    # base_dir = "../data/AdaniPorts"
    # file_name = "9_Sep23_Sep24.xlsx"  
    # create_excel_file(path,base_dir,file_name)
    
    append_sector("Kishan")

# 1 Transport Infrastructure
# 2 Oil and Energy