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
            print(f"Successfully created directory: {directory}")
        
        if num == 1:
            dummy_file = os.path.join(directory, "1.txt")
            with open(dummy_file, "w") as f:
                f.write("dummy")
                print(f"Dummy file created at: {dummy_file}")
        
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


# Function to convert HTML table data to an Excel file
def create_excel_file(path, base_dir,file):
    print("Path:", path)
    
    # exit()
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
    
    quarter = table_data[0]
    index_1 = quarter[5].find("'")
    index_2 = quarter[1].find("'")
    start = quarter[5]
    end = quarter[1]
    print(index_1,index_2)
    
    start_timeline = start[:index_1] + start[index_1 + 1:]
    start_timeline = start_timeline.replace(" ","")
    print(start_timeline)
    
    end_timeline = end[:index_2] + end[index_2 + 1:]
    end_timeline = end_timeline.replace(" ","")
    print(end_timeline)
    
    final_filename = f"{file}_{start_timeline}_{end_timeline}.xlsx"  
    print("\n\n Filename:- ",final_filename)
    
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
    company_name = "Cyient Ltd"
    sector_name = "IT Services & Consulting"
    file = f"{company_name}_excel"
    original_path = f"{current_dir}/Main_Data/{site}/data/{company_name}/Quarterly-resulQuarterly10Yrs/1.html"  # Path to the HTML file
    
    base_dir = f"{current_dir}/Main_Data/{site}/Companies/{sector_name}/{company_name}/Excel"  # Base directory for the company
    # file_name = "9_Sep23_Sep24.xlsx"  # Name of the Excel file to save
    
    print("\n original file path:- ",original_path)
    print("\n base file path:- ",base_dir)
    
    # Convert HTML table to Excel
    create_excel_file(original_path, base_dir,file)    
