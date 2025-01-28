from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import json

# URL and file name
url = input("\n Enter the URL to scrape \n URL:- ")
path_to_save_file = os.path.join(f"{os.getcwd()}", "Code", "Rayyan", "Sector_Links")


try:
    os.makedirs(path_to_save_file)
    print("File created successfully")
except FileExistsError as e:
    print("Error creating directory: ", e)

url_section = url.split("/")[-1]
url_section = url_section[:-5].capitalize()

final_path = os.path.join(path_to_save_file, f"{url_section}_links.json")
print(final_path)

# Set up the browser (headless mode disabled to keep the window open)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options)

try:
    print("Launching browser...")
    driver.get(url)  # Open the webpage

    # Wait until the table rows are loaded
    print("Waiting for table data to load...")
    WebDriverWait(driver, 500000).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.Topfilter_web_tbl_indices__Wa1Sj tbody tr"))
    )

    # Get the page source after the table has loaded
    print("Table loaded. Fetching page source...")
    page_source = driver.page_source

    # Parse the rendered page source with BeautifulSoup
    soup = BeautifulSoup(page_source, "html.parser")
    table = soup.find(class_="Topfilter_web_tbl_indices__Wa1Sj undefined")

    if not table:
        print("Table not found.")
        exit()

    # Extract rows and links
    rows = table.find_all("tr")
    existing_links = []
    if os.path.exists(final_path):
        with open(final_path, "r") as file:
            existing_links = json.load(file)

    new_links = []
    for row in rows:
        first_td = row.find("td")
        if first_td:
            anchor = first_td.find("a")
            if anchor and "href" in anchor.attrs:
                link = anchor["href"]
                if link not in existing_links:
                    new_links.append(link)
                    existing_links.append(link)

    # Save new links as JSON
    if new_links:
        with open(final_path, "w") as file:
            json.dump(existing_links, file, indent=4)
        print(f"Added {len(new_links)} new links to {final_path}")
    else:
        print("No new links found.")

    print("\nBrowser will remain open. Close it manually when done.")

except Exception as e:
    print(f"An error occurred: {e}")

# Do not close the browser
driver.quit() #is omitted here to keep the browser open

# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import os
# import json
# import time

# # URL and file name
# url = input("\n Enter the URL to scrape \n URL:- ")
# path_to_save_file = os.path.join(f"{os.getcwd()}", "Code", "Rayyan", "Sector_Links")

# try:
#     os.makedirs(path_to_save_file)
#     print("File created successfully")
# except FileExistsError as e:
#     print("Error creating directory: ", e)

# url_section = url.split("/")[-1]
# url_section = url_section[:-5].capitalize()

# final_path = os.path.join(path_to_save_file, f"{url_section}_links.json")
# print(final_path)

# # Set up the browser (headless mode disabled to keep the window open)
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(options=options)

# try:
#     print("Launching browser...")
#     driver.get(url)  # Open the webpage

#     # Maximum wait time for table to load
#     max_wait_time = 120
#     start_time = time.time()
#     table_found = False

#     print("Waiting for table data to load...")
#     while time.time() - start_time < max_wait_time:
#         try:
#             # Check if the table is visible
#             WebDriverWait(driver, 5).until(
#                 EC.visibility_of_element_located((By.CSS_SELECTOR, "table.Topfilter_web_tbl_indices__Wa1Sj tbody tr"))
#             )
#             print("Table loaded.")
#             table_found = True
#             break
#         except:
#             print("Table not yet loaded, rechecking...")
#             time.sleep(2)

#     if not table_found:
#         print("Table failed to load within the maximum wait time.")
#         input("\nPress Enter to close the browser after reviewing...")
#         exit()

#     # Get the page source after the table has loaded
#     page_source = driver.page_source

#     # Parse the rendered page source with BeautifulSoup
#     soup = BeautifulSoup(page_source, "html.parser")
#     table = soup.find(class_="Topfilter_web_tbl_indices__Wa1Sj undefined")

#     if not table:
#         print("Table not found.")
#         input("\nPress Enter to close the browser after reviewing...")
#         exit()

#     # Extract rows and links
#     rows = table.find_all("tr")
#     existing_links = []
#     if os.path.exists(final_path):
#         with open(final_path, "r") as file:
#             existing_links = json.load(file)

#     new_links = []
#     for row in rows:
#         first_td = row.find("td")
#         if first_td:
#             anchor = first_td.find("a")
#             if anchor and "href" in anchor.attrs:
#                 link = anchor["href"]
#                 if link not in existing_links:
#                     new_links.append(link)
#                     existing_links.append(link)

#     # Save new links as JSON
#     if new_links:
#         with open(final_path, "w") as file:
#             json.dump(existing_links, file, indent=4)
#         print(f"Added {len(new_links)} new links to {final_path}")
#     else:
#         print("No new links found.")

#     print("\nData extraction complete. Close the browser manually when done.")

#     # Keep the browser open until user decides to close it
#     input("\nPress Enter to close the browser after reviewing...")

# finally:
#     # Ensure the browser is closed properly
#     driver.quit()
