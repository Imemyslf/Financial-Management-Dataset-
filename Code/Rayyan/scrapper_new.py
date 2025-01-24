import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from gui import f1  # Assuming f1 is a valid function in gui.py
from selenium.webdriver.chrome.options import Options
import os
import json

# URL to scrape
# url = input("\n Enter the URL to scrape:- \n URL:- ")
# url = "https://www.moneycontrol.com/india/stockpricequote/computers-software/tataconsultancyservices/TCS"

path = f"{os.getcwd()}/Code/Rayyan/Sector_Links/Transport-infrastructure_links.json"
with open(path, "r") as f:
    Transport_links = json.load(f)
print("Length of Transport_links:- ",len(Transport_links))

for url in Transport_links:
    # Send a request to the URL
    request = requests.get(url)
    if request.status_code == 200:
        html_content = request.text
    else:
        print(f"Failed to retrieve the page. Status code: {request.status_code}")
        exit()

    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find the links under the class "quick_links clearfix"
    link = soup.find(class_="quick_links clearfix")

    # List of desired link texts to click
    desired_links = [
        "Balance Sheet",
        "Profit & Loss",
        "Quarterly Results",
        "Yearly Results",
        "Cash Flows",
        "Ratios"
    ]

    # Ensure ChromeDriver is correctly installed and added to PATH
    try:
        options = Options()
        options.headless = True
        driver = webdriver.Chrome(options=options)
        print("Browser launched successfully.")
        driver.get(url)  # Open the main page in the browser
        time.sleep(2)  # Wait for the page to load

        # Check if the `link` exists before processing
        if link:
            # Iterate through each <a> tag and extract the href
            for atag in link.find_all('a'):
                link_text = atag.get_text().strip()  # Get the visible text of the link
                href = atag.get('href')  # Get the href attribute

                # Process only if the link text matches the desired links
                if link_text in desired_links:
                    print(f"Processing link: {href} ({link_text})")

                    try:
                        message = f1(href)
                    except Exception as e:
                        print(f"Error in processing the link with f1: {e}")
                        continue

                    if message == "Success":
                        response = input("Do you want to continue? (Y/N): ").strip().lower()
                        if response == "y":
                            continue
                        elif response == "n":
                            print("Exiting loop as per user request.")
                            break
                        else:
                            print("Invalid input. Exiting loop.")
                            break
                    else:
                        print(f"f1 function returned an unexpected result: {message}")
                else:
                    print(f"Skipping link: {href} ({link_text})")
        else:
            print("No links found under the specified class.")

    finally:
        # Optionally, close the browser after some time
        print("Closing the browser.")
        driver.quit()
