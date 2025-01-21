import requests
from bs4 import BeautifulSoup
from Functions import append_sector, make_main_dir, create_company_directory, create_excel_file
# from Concat import consolidate_and_merge_excel_sheets
import os


current_dir = os.getcwd()
# Define base directories for storing data
base_dir = f"{current_dir}/Main_Data"      # Directory to store sector/company data

# Function to fetch HTML content from a URL and save it as an HTML file
def fetchandSave(url, path, filename):  
    r = requests.get(url)  # Send GET request to the URL
    
    # Write the HTML content to the specified file
    with open(f"{path}/{filename}.html", "w", encoding="utf-8") as f:
        f.write(r.text)
        print("Sucess")
def webiste_call(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    return soup


def getUrl(url, file_name="", index=0, company_data_info=""):
    global current_dir, base_dir, data_folder    
    try:        
        soup = webiste_call(url)
        print("\n\n",url)
        # print("Company_data_info:", company_data_info)
        
        if index in url:
            site = "MoneyControl"
            # Extract company and sector details
            company_soup_name = soup.find(class_="pcstname")
            company_name = company_soup_name.get_text().strip()
            print("\nCompany Name:", company_name, "\n")
            
            sector_class = soup.find(class_="hidden-lg")
            sector_name = sector_class.get_text().split()
            final_sector_name = " ".join(sector_name).strip()
            print("Sector Name:", final_sector_name, "\n")

            # Ensure main directory exists
            make_main_dir(base_dir)

            # Create directory for quarterly data
            quarterly_dir = os.path.join(base_dir, site, "data", company_name, f"{company_data_info}")
            data_html_created = create_company_directory(quarterly_dir, 0)

            if not data_html_created:
                print("Failed to create directory:", quarterly_dir)
                return False
            
            # Path for storing the HTML file
            html_path = os.path.join(quarterly_dir, f"{file_name}.html")
            print("\nHTML Path:", html_path)
            
            create_company_directory(os.path.join(base_dir, site, "Companies", final_sector_name, company_name, "Excel"), 1)
            create_company_directory(os.path.join(base_dir, site, "Companies", final_sector_name, company_name, "Pruned_Excel"), 1)
            
            # Fetch and save HTML file
            fetchandSave(url, quarterly_dir, file_name)
            
            # Create Excel directories

            # Convert the saved HTML to Excel
            # create_excel_file(html_path, os.path.join(base_dir, "Companies", final_sector_name, company_name, "Excel"), file_name)
            return True
        else:
            print("\nURL does not match the specified index.")
            return False
    except Exception as e:
        print("\nException occurred:\n", e)
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
            
