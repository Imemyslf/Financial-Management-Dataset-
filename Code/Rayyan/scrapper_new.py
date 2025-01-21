

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

# URL to scrape
url = "https://www.moneycontrol.com/india/stockpricequote/computers-software/infosys/IT"

# Send a request to the URL
request = requests.get(url)
html_content = request.text

# Parse the content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the links under the class "quick_links clearfix"
link = soup.find(class_="quick_links clearfix")

try:
    driver = webdriver.Chrome()  # Ensure ChromeDriver is correctly installed and added to PATH
    print("Browser launched successfully.")
except Exception as e:
    print(f"Error launching browser: {e}")
    exit()

# Open the main page in the browser
driver.get(url)

# Wait for the page to load
time.sleep(2)

# Iterate through each link and open them in new tabs
for atag in link.find_all('a'):
    href = atag.get('href')
    if href:
        # Open a new tab
        driver.execute_script(f"window.open('{href}', '_blank');")
        time.sleep(1)  # Wait a bit before opening the next link

# If you want to keep the browser open for a while, use time.sleep() to prevent it from closing immediately
# time.sleep(10)

# Optionally, you can close the browser after some time
driver.quit()
