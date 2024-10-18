import requests

def fetchandSave(url, path):
    r = requests.get(url)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)

url = "https://www.moneycontrol.com/financials/relianceindustries/results/quarterly-results/RI/7#RI"
fetchandSave(url, "../data/Reliance/Balance_sheet_10_Years/3_Mar16_Mar17.html")
