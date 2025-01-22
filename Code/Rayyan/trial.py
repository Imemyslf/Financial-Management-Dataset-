import requests
from bs4 import BeautifulSoup

# URL of the webpage with the table
url = "https://www.moneycontrol.com/stocks/marketinfo/marketcap/bse/it-services-consulting.html"  # Replace with the actual URL

# Fetch the HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML with BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table (replace 'table' with a specific selector if needed)
table = soup.find(class_="Topfilter_web_tbl_indices__Wa1Sj undefined")
print(table.prettify())
exit()
# Extract all links (<a>) in the table
links = []
for row in table.find_all('tr'):  # Iterate through all rows
    for cell in row.find_all('td'):  # Iterate through all cells
        # Find all <a> tags in the cell
        for link in cell.find_all('a', href=True):  # Only consider tags with href
            links.append(link['href'])  # Extract the href attribute

# Print all extracted links
print("Extracted Links:")
for link in links:
    print(link)