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
def create_company_directory(directory,num):    
    try: 
        os.makedirs(directory)

        if num == 1:
            with open(f"{directory}/1.txt","w") as f:
                f.write("dummy")
                print("File created")
                
        return f"{directory} directory created successfully"
    except FileExistsError as e:
        
        if num == 1:
            with open(f"{directory}/1.txt","w") as f:
                f.write("dummy")
                print("File created")
                
        return "File already exists or Error in creating directory", e
    except PermissionError as e:
        print("Permission denied", e)
        return False
    except Exception as e:
        print("An Error Occurred while creating the directory", e)
        return False

# Function to convert HTML table data to an Excel file
def create_excel_file(path, base_dir, file_name):
    print("Path:", path)
    # Open the HTML file and read its content
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Parse HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Find the table by its class name
    table = soup.find(class_="mctable1")
    
    table_data = []  # List to store table data
    rows = table.find_all("tr")  # Find all rows in the table
    
    # Iterate over each row to extract cell data
    for i, row in enumerate(rows):  
        cols = row.find_all(["td", "th"])  # Find all cells
        col_text = [col.get_text(strip=True) for col in cols]  # Get cell text without extra whitespace
        table_data.append(col_text)
        
    # Create a DataFrame with extracted table data
    df = pd.DataFrame(table_data[1:], columns=table_data[0])  
    
    # Save the DataFrame to an Excel file at the specified path
    df.to_excel(f"{base_dir}/{file_name}", index=False)
        
# Main execution of the script
if __name__ == "__main__": 
    path = "../data/AdaniPorts/Quarterly10Yrs/9_Jun23_Jun24.html"  # Path to the HTML file
    base_dir = "../data/AdaniPorts"  # Base directory for the company
    file_name = "9_Sep23_Sep24.xlsx"  # Name of the Excel file to save
    
    # Convert HTML table to Excel
    create_excel_file(path, base_dir, file_name)    
