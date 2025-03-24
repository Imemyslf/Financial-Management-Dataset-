import requests
from bs4 import BeautifulSoup
import os


current_dir = os.getcwd()
# Define base directories for storing data
base_dir = f"{current_dir}/Financial_Data"      # Directory to store sector/company data

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

def make_main_dir(base_dir):
    try:
        os.mkdir(base_dir)
        return f"{base_dir} directory created successfully"
        
    except FileExistsError as e:
        return "File already exists in directory" 
        
    except PermissionError as e:
        print("Permission denied", e)
        return False
    except Exception as e:
        print("An Error Occurred while creating the directory", e)
        return False

# Function to create a directory structure for a specific company
def create_company_directory(directory, num):
    try:
        print(f"Attempting to create directory: {directory}")
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Successfully created directory: {directory}\n\n")
        
        if num == 1:
            dummy_file = os.path.join(directory, "1.txt")
            with open(dummy_file, "w") as f:
                f.write("dummy")
                print(f"Dummy file created at: {dummy_file}\n\n")
        
        return f"{directory} created successfully"
    except FileExistsError:
        print(f"Directory already exists: {directory}")
        return f"{directory} already exists"
    except PermissionError as e:
        print(f"Permission denied for {directory}: {e}")
        return f"Permission error for {directory}"
    except Exception as e:
        print(f"An error occurred while creating the directory: {e}")
        return f"Error creating {directory}: {e}"

def getUrl(url, file_name="", index=0, company_data_info=""):
    global current_dir, base_dir, data_folder    
    try:        
        soup = webiste_call(url)
        print("\n\n",url)
        print("\n\n Company_data_info:", company_data_info)
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
            
    except Exception as e:
        print("\nException occurred:\n", e)
        return False


if __name__ == "__main__":
    current_dir = os.getcwd()
    
    path = f"{current_dir}/Financial_Data/MoneyControl"
    print(path)
    