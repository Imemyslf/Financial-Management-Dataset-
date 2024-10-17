import requests

def fetchandSave(url, path):
    r = requests.get(url)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(r.text)

url = "https://www.moneycontrol.com/financials/larsentoubro/results/yearly/LT#LT"
fetchandSave(url, "../data/LarsenToubro/larsernToubro_yearly_financial_statement.html")
