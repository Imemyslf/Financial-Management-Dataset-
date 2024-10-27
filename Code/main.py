import requests
from bs4 import BeautifulSoup
from findTable import append_sector, make_main_dir, create_company_directory, create_excel_file
import os

# Get and print the current working directory
current_path = os.getcwd()
print("Current path:", current_path)

# Function to fetch HTML content from a URL and save it as an HTML file
def fetchandSave(url, path, filename):  
    r = requests.get(url)  # Send GET request to the URL
    # Write the HTML content to the specified file
    with open(f"{path}/{filename}.html", "w", encoding="utf-8") as f:
        f.write(r.text)

# Define the URL for the company financial data
url = "https://www.moneycontrol.com/financials/hdfcbank/results/quarterly-results/HDF01#HDF01"

# Send a request to the URL and parse the HTML content with BeautifulSoup
r = requests.get(url)
soup = BeautifulSoup(r.content, "html.parser")

# Extract the company name from the parsed HTML
company_soup_name = soup.find(class_="pcstname")
company_name = company_soup_name.get_text().strip()
print("Company Name:", company_name, "\n")

# Extract the sector name from the parsed HTML and clean up the text
sector_class = soup.find(class_="hidden-lg")
sector_name = sector_class.get_text().split()
final_sector_name = " ".join(sector_name).strip()
print("Sector Name:", final_sector_name, "\n")

# Set the company name and sector name for directory organization
company_name = "HDFC Bank Ltd."
final_sector_name = "Bank - Private"

# Define base directories for storing data
base_dir = f"{current_path}/Companies"      # Directory to store sector/company data
current_dir = f"{current_path}/data"        # Directory to store raw data

print("\ncurrent_dir:", current_dir, "\n")

# Create the main directory for companies if it doesn’t exist
file_creation = make_main_dir(base_dir)

# Create a subdirectory for the company’s quarterly data within `data` directory
data_html = create_company_directory(os.path.join(current_dir, company_name, "Quarterly10Yrs"))

# Set up the path for HTML storage and the filename for saving the quarterly report
html_path = f"{current_dir}/{company_name}"
file_name = "9_Sep24_Sep23"

# Proceed with data saving only if the main directory was created successfully
if file_creation != False:
    # Define path for saving the HTML file in the Quarterly10Yrs subdirectory
    path = f"{html_path}/Quarterly10Yrs"
    
    # Append the sector name to a text file within the `Companies` directory
    append_sector(f"{base_dir}/sector.txt", final_sector_name)
    
    # Create directory structure within `Companies` for organizing data by sector and company
    create_company_directory(os.path.join(base_dir, final_sector_name, company_name))
    
    # Fetch and save the HTML file from the URL to the specified path
    fetchandSave(url, path, file_name)
    
    # Convert the HTML file to an Excel file and save it in the company’s directory under its sector
    create_excel_file(f"{path}/{file_name}.html", f"{base_dir}/{final_sector_name}/{company_name}", file_name)
