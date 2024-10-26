import requests
from bs4 import BeautifulSoup
import pandas as pd  
import os


with open("../data/Oil and Natural Gas Corporation Ltd/Quarterly10Yrs/9_Jun23_Jun24.html", "r", encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

company_soup_name = soup.find(class_="pcstname")
company_name = company_soup_name.get_text()

print(company_name,"\n")

sector_class = soup.find(class_="hidden-lg")
sector_name = sector_class.get_text().split()

print(sector_name)
final_sector_name = " ".join(sector_name)
print(final_sector_name,"\n")

try:
    os.mkdir("../Companies")
    print("Companies directory created successfully")
except FileExistsError as e:
    print("File already exists or Error in creating directory",e) 
except PermissionError as e:
    print("Permission denied",e)
except Exception as e:
    print("An Error Occured while creating the directory",e)  

with open("../Companies/sector.txt","w") as f:
    f.write(str(final_sector_name))

try: 
    os.mkdir(f"../Companies/{final_sector_name}")
    print(f"{final_sector_name} directory created successfully")
except FileExistsError as e:
    print("File already exists or Error in creating directory",e) 
except PermissionError as e:
    print("Permission denied",e)
except Exception as e:
    print("An Error Occured while creating the directory",e)
    
try: 
    os.mkdir(f"../Companies/{final_sector_name}/{company_name}")
    print(f"{company_name} directory created successfully")
except FileExistsError as e:
    print("File already exists or Error in creating directory",e) 
except PermissionError as e:
    print("Permission denied",e)
except Exception as e:
    print("An Error Occured while creating the directory",e)




# name = sector_class.find(text="Sector")
# print(name)

# table = soup.find(class_="mctable1")

# table_data = []

# rows = table.find_all("tr")

# for i, row in enumerate(rows):    
#     cols = row.find_all(["td", "th"])  
#     col_text = [col.get_text(strip=True) for col in cols]  
        
#     table_data.append(col_text)

# df = pd.DataFrame(table_data[1:], columns=table_data[0])  

# df.to_excel("../data/Reliance/QuarterlyExcel/9_Sep23_Sep24.xlsx", index=False)  

# print("Table saved to/9_Sep23_Sep24.xlsx")
