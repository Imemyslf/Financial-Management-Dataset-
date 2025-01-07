import requests
from bs4 import BeautifulSoup
from Code.Functions import append_sector, make_main_dir, create_company_directory, create_excel_file
from Concat import consolidate_and_merge_excel_sheets
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
    print(soup)
    return soup


def getUrl(url,file_name,index):
    global current_dir,base_dir,data_folder    
    # Send a request to the URL and parse the HTML content with BeautifulSoup
    try:        
        soup = webiste_call(url)
        
        if index == 1:
            site = "MoneyControl"
            # Extract the company name from the parsed HTML
            company_soup_name = soup.find(class_="pcstname")
            company_name = company_soup_name.get_text().strip()
            print("Company Name:", company_name, "\n")

            # Extract the sector name from the parsed HTML and clean up the text
            sector_class = soup.find(class_="hidden-lg")
            sector_name = sector_class.get_text().split()
            final_sector_name = " ".join(sector_name).strip()
            print("Sector Name:", final_sector_name, "\n")

            # Create the main directory for companies if it doesn’t exist
            make_main_dir(base_dir)

            # Create a subdirectory for the company’s quarterly data within `data` directory
            data_html = create_company_directory(os.path.join(base_dir,site,"data", company_name, "Quarterly10Yrs"),0)

            # Set up the path for HTML storage and the filename for saving the quarterly report
            html_path = f"{data_folder}/{company_name}"
            
            # Proceed with data saving only if the main directory was created successfully
            if data_html != False:            
                # Define path for saving the HTML file in the Quarterly10Yrs subdirectory
                path = f"{current_dir}/{site}/data/{company_name}/Quarterly10Yrs"
                
                # Create directory structure within `Companies` for organizing data by sector and company
                create_company_directory(os.path.join(base_dir,site,"Companies", final_sector_name, company_name,"Excel"),0)
                create_company_directory(os.path.join(base_dir,site,"Companies", final_sector_name, company_name,"Pruned_Excel"),1)
                
                # Fetch and save the HTML file from the URL to the specified path
                fetchandSave(url, path, file_name)
                
                # Convert the HTML file to an Excel file and save it in the company’s directory under its sector
                create_excel_file(f"{path}/{file_name}.html", f"{base_dir}/{final_sector_name}/{company_name}/Excel", file_name)
            
            # consolidate_and_merge_excel_sheets(f"{path}/{file_name}.html", f"{base_dir}/{final_sector_name}/{company_name}/Excel")
            return True
        else:
            site = "Screener"
            company_soup_name = soup.find(class_="shrink-text")
            company_name = company_soup_name.get_text().strip()
            print("Company Name:", company_name, "\n")

            # Find all <p> tags with the class 'sub'
            data = soup.find_all('p', class_='sub')

            # Extract and process each tag
            for i, tag in enumerate(data):
                text_data = tag.get_text(strip=True)  # Clean whitespace
                
                # Check for 'Sector' keyword
                if "Sector" in text_data:
                    sector_index = text_data.find("Sector")
                    print(sector_index)
                    
                    if sector_index == 0:
                        print(f"Keyword 'Sector' found at index: {sector_index}")
                        start = "Sector:"
                        end = "Industry"
                        company_sector = (text_data.split(start)[1].split(end)[0])
                        print(company_sector)                        
        
            make_main_dir(base_dir)

            # Create a subdirectory for the company’s quarterly data within `data` directory
            data_html = create_company_directory(os.path.join(base_dir,site,"data", company_name),0)
            
            # file_name = "9_Jun24_Jun23"

            # Proceed with data saving only if the main directory was created successfully
            if data_html != False:            
                # Define path for saving the HTML file in the Screener subdirectory
                path = f"{current_dir}/{site}/data/{company_name}"
                
                # Create directory structure within `Companies` for organizing data by sector and company
                create_company_directory(os.path.join(base_dir,site,"Companies", final_sector_name, company_name,"Excel"),0)
                create_company_directory(os.path.join(base_dir, site, "Companies", final_sector_name, company_name,"Pruned_Excel"),1)
                
                # Fetch and save the HTML file from the URL to the specified path
                fetchandSave(url, path, file_name)           
        
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
            
