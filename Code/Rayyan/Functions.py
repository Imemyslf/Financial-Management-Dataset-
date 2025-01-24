from bs4 import BeautifulSoup
import pandas as pd  
import os

# Function to create the main directory for storing company data
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


if __name__ == "__main__": 
    # Define the directories
    current_dir = os.getcwd()
    site = "MoneyControl"
    data_dir = f"{current_dir}/Financial_Data/{site}/data"
    sector_name = "Oil Exploration and Production"
    companies_dir = f"{current_dir}/Financial_Data/{site}/Companies/{sector_name}"

    # Iterate through each company's data
    for company_name in os.listdir(data_dir):
        company_data_dir = os.path.join(data_dir, company_name)
        if not os.path.isdir(company_data_dir):
            continue  # Skip if not a directory

        print(f"\nProcessing company: {company_name}")

        # Iterate through folders like "Balance Sheet", "Profit & Loss", etc.
        for subfolder in os.listdir(company_data_dir):
            subfolder_path = os.path.join(company_data_dir, subfolder)
            if not os.path.isdir(subfolder_path):
                continue  # Skip if not a directory

            print(f"  Subfolder: {subfolder}")

            # Create the corresponding subfolder in the Excel directory
            excel_subfolder = os.path.join(companies_dir, company_name, "Excel", subfolder)
            os.makedirs(excel_subfolder, exist_ok=True)

            # Iterate through HTML files in the subfolder
            for html_file in os.listdir(subfolder_path):
                html_file_path = os.path.join(subfolder_path, html_file)

                # Ensure it's an HTML file
                if not html_file.endswith(".html"):
                    continue

                # Define the Excel file name
                excel_file_name = os.path.splitext(html_file)[0]  # Remove .html extension
                create_excel_file(html_file_path, excel_subfolder, excel_file_name)

    print("\nProcessing complete.")
    