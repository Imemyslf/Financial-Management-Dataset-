import requests
from bs4 import BeautifulSoup
url = "https://www.moneycontrol.com/india/stockpricequote/computers-software/infosys/IT"

request = requests.get(url)
html_content = request.text

soup = BeautifulSoup(html_content, 'html.parser')

link = soup.find(class_="quick_links clearfix")

for atag in link.find_all('a'):
    #print(atag.get('href'))
    print(atag.get_text())

