from bs4 import BeautifulSoup
import pandas as pd  
import os

# Function to create the main directory for storing company data
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

# Function to append sector information to a text file
def append_sector(path, final_sector_name):
    
    # Helper function to write the sector name with a count
    def insert_sector(count, final_sector_name):
        with open(path, "a") as f:
            f.write(str(f"{count + 1} {final_sector_name}\n"))

    # Read the current contents of the file to determine the last count
    with open(path, "r") as f:
        data = f.read() 
    
    count = 0  # Initialize count for the first entry if file is empty

    if data:
        print("\n\ndata:", data, "\n\n")
        new_data = data.split()  # Split data to analyze
        print("\n\n new_data:", new_data, "\n\n")
        
        # Find the last digit from the data to continue the count
        last_digit = next(int(item) for item in reversed(data) if item.isdigit())
        print("\n\n last digit:", last_digit, "\n\n")
        
        # Insert sector name with updated count
        insert_sector(last_digit, final_sector_name)
    else:
        print("data unavailable:", data)
        # Insert sector as the first entry if the file is empty
        insert_sector(count, final_sector_name)        

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

def create_excel_file(path, base_dir, file):
    print("\n\n Path from scrapping :- ", path)
    
    # Open the HTML file and read its content
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find the table by its class name
    table = soup.find(class_="mctable1")
    
    if not table:
        print("\n\n `No` table present in HTML.")
        return  # Exit the function if no table is found
    
    table_data = []  # List to store table data
    rows = table.find_all("tr")  # Find all rows in the table
    
    # Iterate over each row to extract cell data
    for i, row in enumerate(rows):  
        cols = row.find_all(["td", "th"])  # Find all cells
        col_text = [col.get_text(strip=True) for col in cols]  # Get cell text without extra whitespace
        table_data.append(col_text)
    
    # Ensure there's enough data in the first row (quarter)
    if len(table_data) < 1 or len(table_data[0]) < 6:
        print("\n\n Unexpected table structure or insufficient data in the table.")
        return
    
    quarter = table_data[0]
    
    # Check if the number of td elements is 1 or greater than 1
    if len(quarter) == 1:
        # If only one element, set start and end as the same
        start = end = quarter[0]
    else:
        # If more than 1 element, continue with the original logic
        index_1 = quarter[5].find("'")
        index_2 = quarter[1].find("'")
        start = quarter[5]
        end = quarter[1]
        print(index_1, index_2)
        
        # Process timelines
        start_timeline = start[:index_1] + start[index_1 + 1:]
        start_timeline = start_timeline.replace(" ", "")
        print(start_timeline)
        
        end_timeline = end[:index_2] + end[index_2 + 1:]
        end_timeline = end_timeline.replace(" ", "")
        print(end_timeline)
    
    # Generate filename
    final_filename = f"{file}_{start_timeline}_{end_timeline}.xlsx"  
    print("\n\n Filename:- ", final_filename)
    
    final_excel_path = f"{base_dir}/{final_filename}"
    print(final_excel_path)
    
    # Create a DataFrame with extracted table data
    df = pd.DataFrame(table_data[1:], columns=table_data[0])  
    
    # Save the DataFrame to an Excel file at the specified path
    df.to_excel(f"{final_excel_path}", index=False)


            
# Main execution of the script
if __name__ == "__main__": 
    current_dir = os.getcwd()
    print(current_dir)
    
    site = "MoneyControl"
    
    companies = [
    "3i Infotech Ltd",
    "AION-TECH SOLUTIONS Ltd",
    "AMPVOLTS Ltd",
    "ASM Technologies Ltd",
    "Adroit Infotech Ltd",
    "Affle India Ltd",
    "Allied Digital Services Ltd",
    "Alphalogic Techsys Ltd",
    "Athena Global Technologies Ltd",
    "Aurum Proptech Ltd",
    "Avance Technologies Ltd",
    "B2B Software Technologies Ltd",
    "Bartronics India Ltd",
    "Birlasoft Ltd",
    "CG-Vak Software and Exports Ltd",
    "COFORGE LIMITED Ltd",
    "COSYN Ltd",
    "Cambridge Technology Enterprises Ltd",
    "Computer Point (India) Ltd",
    "Cranes Software International Ltd",
    "Cressanda Solution Ltd",
    "Cybertech Systems and Software Ltd",
    "Cyient Ltd",
    "Danlaw Technologies India Ltd",
    "Datamatics Global Services Ltd",
    "Dev Information Technology Ltd",
    "Dynacons Systems and Solutions Ltd",
    "Expleo Solutions Ltd",
    "FCS Software Solutions Ltd",
    "Genesys International Corporation Ltd",
    "Happiest Minds Technologies Ltd",
    "IZMO Ltd",
    "Indian Infotech and Software Ltd",
    "Indo-City Trades and Finance Ltd",
    "Inspirisys Solutions Ltd",
    "Intellect Design Arena Ltd",
    "Jeevan Scientific Technology Ltd",
    "KPIT Technologies Ltd",
    "Kellton Tech Solutions Ltd",
    "Kernex Microsystems (India) Ltd",
    "LTIMindtree Ltd",
    "Latent View Analytics Ltd",
    "Mastek Ltd",
    "Megasoft Ltd",
    "MphasiS Ltd",
    "Mudunuru Ltd",
    "Netlink Solutions Ltd",
    "Nettlinx Ltd",
    "Onward Technologies Ltd",
    "Oracle Financial Services Software Ltd",
    "Palred Technologies Ltd",
    "Persistent Systems Ltd",
    "Protean eGov Technologies Ltd",
    "Quick Heal Technologies Ltd",
    "R Systems International Ltd",
    "RPSG VENTURES Ltd",
    "Response Informatics Ltd",
    "Route Mobile Ltd",
    "SBSJHVHSV Ltd",
    "Sasken Technologies Ltd",
    "Saven Technologies Ltd",
    "Securekloud Technologies Ltd",
    "Sigma Solve Ltd",
    "Sonata Software Ltd",
    "Southern Infosys Ltd",
    "Sylph Technologies Ltd",
    "Tech Mahindra Ltd",
    "Tera Software Ltd",
    "Titan Intech Ltd",
    "Trigyn Technologies Ltd",
    "Unicommerce Esolutions Ltd",
    "Usha Martin Education and Solutions Ltd",
    "VEDAVAAG Systems Ltd",
    "Vama Industries Ltd",
    "WEP Solutions Ltd",
    "Xchanging Solutions Ltd",
    "Xtglobal Infotech Ltd",
    "Zensar Technologies Ltd"
    ]
    
    sector_name = "IT Services & Consulting"
    origin_data = f"{current_dir}/Main_Data/{site}/data"
    for company_name in companies:        
        file = f"{company_name}_excel"
        # print(company_name,"\n")
        
        new_dir_list_file = os.path.join(origin_data,company_name)
        list_html_files = os.listdir(new_dir_list_file)
        # print(list_html_files)
        
        for list in list_html_files:
            print("li:- ",list)
            new_path = os.path.join(new_dir_list_file,list)
            # print(new_path)
            
            list_html_name = os.listdir(new_path)
            
            # print(list_html_name)
            
            for list_html in list_html_name:
                original_path = os.path.join(new_path,list_html)
                save_dir = f"{current_dir}/Main_Data/{site}/Companies/{sector_name}/{company_name}/Excel"
                print(original_path)
                create_excel_file(original_path,save_dir,file)
        
            

        
        # base_dir = f"{current_dir}/Main_Data/{site}/Companies/{sector_name}/{company_name}/Excel"  # Base directory for the company
        # # file_name = "9_Sep23_Sep24.xlsx"  # Name of the Excel file to save
        
        # print("\n original file path:- ",original_path)
        # print("\n base file path:- ",base_dir)
        
        # # Convert HTML table to Excel
        # create_excel_file(original_path, base_dir,file)   