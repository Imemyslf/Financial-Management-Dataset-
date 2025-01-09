import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


if __name__ == '__main__':
    
    base_url = ""
    
    sectors = ["quaters","profit-loss","balance-sheet","cash-flow"]
    
    curr_dir = os.getcwd()
    h1_tag = soup.find("h1", class_="h2 shrink-text", style="margin: 0.5em 0")
    path = f"{curr_dir}/Main_Data/Tabular/"