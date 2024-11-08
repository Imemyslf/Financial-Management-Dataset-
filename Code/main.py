import requests
from bs4 import BeautifulSoup
from findTable import append_sector, make_main_dir, create_company_directory, create_excel_file
import os

# Function to fetch HTML content from a URL and save it as an HTML file
def fetchandSave(url, path, filename):  
    r = requests.get(url)  # Send GET request to the URL
    
    # Write the HTML content to the specified file
    with open(f"{path}/{filename}.html", "w", encoding="utf-8") as f:
        f.write(r.text)

def getUrl(url,file_name):    
    # Send a request to the URL and parse the HTML content with BeautifulSoup
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

    # print(soup.prettify())
    
    # Extract the company name from the parsed HTML
        company_soup_name = soup.find(class_="pcstname")
        company_name = company_soup_name.get_text().strip()
        print("Company Name:", company_name, "\n")

        # Extract the sector name from the parsed HTML and clean up the text
        sector_class = soup.find(class_="hidden-lg")
        sector_name = sector_class.get_text().split()
        final_sector_name = " ".join(sector_name).strip()
        print("Sector Name:", final_sector_name, "\n")

        # Get and print the current working directory
        current_dir = os.getcwd()
        print("Current directory:", current_dir)

        # Define base directories for storing data
        base_dir = f"{current_dir}/Companies"      # Directory to store sector/company data
        data_folder = f"{current_dir}/data"        # Directory to store raw data

        print("\ndata_folder:", data_folder, "\n")

        # Create the main directory for companies if it doesn’t exist
        make_main_dir(base_dir)

        # Create a subdirectory for the company’s quarterly data within `data` directory
        data_html = create_company_directory(os.path.join(data_folder, company_name, "Quarterly10Yrs"))

        # Set up the path for HTML storage and the filename for saving the quarterly report
        html_path = f"{data_folder}/{company_name}"
        # file_name = "9_Jun24_Jun23"

        # Proceed with data saving only if the main directory was created successfully
        if data_html != False:            
            # Define path for saving the HTML file in the Quarterly10Yrs subdirectory
            path = f"{html_path}/Quarterly10Yrs"
            
            # Create directory structure within `Companies` for organizing data by sector and company
            create_company_directory(os.path.join(base_dir, final_sector_name, company_name,"Excel"))
            create_company_directory(os.path.join(base_dir, final_sector_name, company_name,"Pruned_Excel","Dummy.txt"))
            
            # Fetch and save the HTML file from the URL to the specified path
            fetchandSave(url, path, file_name)
            
            # Convert the HTML file to an Excel file and save it in the company’s directory under its sector
            create_excel_file(f"{path}/{file_name}.html", f"{base_dir}/{final_sector_name}/{company_name}/Excel", file_name)
            return True
    
    except Exception as e:
        print("\nException:- \n", e)
        return False
        
if __name__ == "__main__":
    current_dir = os.getcwd()
    
    path = f"{current_dir}/Companies"
    sector_list = os.listdir(path)
    print("\nSector list:- ",sector_list)
    # print(len(sector_list))
    
    for i in range(len(sector_list)):
        path = f"{current_dir}/Companies"
        sector = sector_list[i]
        path = path + "/" + sector
        # print("Iteration:- ",i)
        # print("\nPath:- ",path)
        comapnies_list = os.listdir(path)
        # print("\nCompanies List:- ",comapnies_list)
        
        for i in range(len(comapnies_list)):
            company = comapnies_list[i]
            # print(f"Company {i}:- {company}")
            path = f"{current_dir}/Companies"
            create_company_directory(os.path.join(path,sector,company,"Pruned_Excel"),1)
            print("File successfully created in:- ",path)
            
