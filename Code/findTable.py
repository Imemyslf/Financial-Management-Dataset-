import requests
from bs4 import BeautifulSoup
import pandas as pd  


with open("../data/Reliance/Quarterly10Yrs/9_Sep23_Sep24.html", "r", encoding='utf-8') as f:
    html_content = f.read()

soup = BeautifulSoup(html_content, "html.parser")

table = soup.find(class_="mctable1")

table_data = []

rows = table.find_all("tr")

for i, row in enumerate(rows):    
    cols = row.find_all(["td", "th"])  
    col_text = [col.get_text(strip=True) for col in cols]  
        
    table_data.append(col_text)

df = pd.DataFrame(table_data[1:], columns=table_data[0])  

df.to_excel("../data/Reliance/QuarterlyExcel/9_Sep23_Sep24.xlsx", index=False)  

print("Table saved to/9_Sep23_Sep24.xlsx")
