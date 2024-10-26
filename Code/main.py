import requests

def fetchandSave(url, path):
    r = requests.get(url)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)

url = "https://www.moneycontrol.com/financials/oilnaturalgascorporation/results/quarterly-results/ONG#ONG"
fetchandSave(url, "../data/Oil and Natural Gas Corporation Ltd/Quarterly10Yrs/9_Jun23_Jun24.html")
