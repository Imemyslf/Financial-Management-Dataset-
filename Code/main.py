import requests
from bs4 import BeautifulSoup
from findTable import append_sector,make_main_dir,create_company_directory
import os
import re

def fetchandSave(url, path):  
    r = requests.get(url)  
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)

url = "https://www.moneycontrol.com/financials/adaniportsspecialeconomiczone/results/quarterly-results/MPS#MPS"

r = requests.get(url)

soup = BeautifulSoup(r.content,"html.parser")

company_soup_name = soup.find(class_="pcstname")
company_name = company_soup_name.get_text().strip()

print("Company Name:-",company_name,"\n")

sector_class = soup.find(class_="hidden-lg")
sector_name = sector_class.get_text().split()

print(sector_name)
final_sector_name = " ".join(sector_name).strip()
print("Sector Name:-",final_sector_name,"\n")

base_dir = "../Companies"
file_creation = make_main_dir(base_dir)
path = "../data/AdaniPorts/Quarterly10Yrs/9_Jun23_Jun24.html"
if file_creation != False:
    append_sector(final_sector_name)
    create_company_directory(os.path.join(base_dir,final_sector_name,company_name))

fetchandSave(url, path)
