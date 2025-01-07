from bs4 import BeautifulSoup
import os
import pandas as pd

# Get the current directory
current_dir = os.getcwd()
print(f"Current Directory: {current_dir}")

def parse_data(path):
    try:
        # Read the HTML content
        with open(path, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        
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
                    
    
    except FileNotFoundError:
        print(f"Error: File not found at path {path}")
    except Exception as e:
        print(f"An error occurred: {e}")

# File and path setup
company_name = "Tata Consultancy Services Ltd"
file_name = "TCS_data.html"
path = os.path.join(current_dir, "data", company_name, file_name)

# Parse the HTML file
parse_data(path)


# start = 'asdf=5;'
# end = '123jasd'
# s = 'asdf=5;iwantthis123jasd'
# print("(s.split(start))",(s.split(start)))
# print("(s.split(start))[1]",(s.split(start))[1])
# print("(s.split(start))[1].split(end)",(s.split(start))[1].split(end))
# print("(s.split(start))[1].split(end)[0]",(s.split(start))[1].split(end)[0])
# print((s.split(start))[1].split(end)[0])
