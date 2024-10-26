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
    path = "../Companies/sector.txt"
    with open(path,"w") as f:
        f.write(str(final_sector_name))


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
    path = "../data/AdaniPorts/Quarterly10Yrs/9_Jun23_Jun24.html" 
    base_dir = "../data/AdaniPorts"
    file_name = "9_Sep23_Sep24.xlsx"  
    create_excel_file(path,base_dir,file_name)