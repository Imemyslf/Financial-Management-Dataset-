import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from gui import f1

# URL to scrape
url = "https://www.moneycontrol.com/india/stockpricequote/computers-software/ltimindtree/LI12"

# Send a request to the URL
request = requests.get(url)
html_content = request.text

# Parse the content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the links under the class "quick_links clearfix"
link = soup.find(class_="quick_links clearfix")

# Ensure ChromeDriver is correctly installed and added to PATH
try:
    driver = webdriver.Chrome()
    print("Browser launched successfully.")
except Exception as e:
    print(f"Error launching browser: {e}")
    exit()

# Open the main page in the browser
driver.get(url)

# Wait for the page to load
time.sleep(2)

# List of desired links to send to GUI
desired_links = [
    "Balance Sheet",
    "Profit & Loss",
    "Quarterly Results",
    "Yearly Results",
    "Cash Flows",
    "Ratios"
]

# Check if the `link` exists before processing
if link:
    # Iterate through each <a> tag and extract the href
    for atag in link.find_all('a'):
        href = atag.get('href')  # Get the href attribute
        print(href)

        message = f1(href)
        # if isinstance(href, str):
        #     print(f"'{href}' is a string.")
        # else:
        #     print(f"'{href}' is not a string. It is of type {type(href)}.")
        # if href:
        #     # Skip "Half Yearly Results"
        #     if atag.text.strip() == "Half Yearly Results":
        #         print("Skipping: Half Yearly Results")
        #         continue

        #     # Save the link to the file
        #     save_links(href)
else:
    print("No links found under the specified class.")

# Optionally, close the browser after some time
driver.quit()
