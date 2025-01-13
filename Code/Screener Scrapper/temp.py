import os
import requests
from bs4 import BeautifulSoup

curr_dir = os.getcwd()

# URL of the page to scrape
url = 'https://www.screener.in/company/LTIM/#quarters'

# Headers to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Base URL for relative links
base_url = 'https://www.screener.in'

# Function to download the final PDF after resolving redirects
def download_pdf(pdf_url, save_path):
    try:
        response = requests.get(pdf_url, headers=headers, stream=True, allow_redirects=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)
            print(f"Downloaded: {save_path}")
        else:
            print(f"Failed to download: {pdf_url} (Status Code: {response.status_code})")
    except Exception as e:
        print(f"Error downloading {pdf_url}: {e}")

# Fetch the webpage
response = requests.get(url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract company name
    company_name_h1 = soup.find("h1", class_="show-from-tablet-landscape")
    if company_name_h1:
        company_name = company_name_h1.get_text().strip()
        print(company_name)
    else:
        print("The <h1> tag with the specified class was not found.")
        company_name = "Unknown_Company"
    
    # Create directory to save PDFs
    path = os.path.join(curr_dir, "Main_Data", "Screener", "PDF", company_name)
    os.makedirs(path, exist_ok=True)
    
    # Find all PDFs
    pdf_links = soup.find_all('td', class_='hover-link')
    print(f"Number of PDFs found: {len(pdf_links)}")
    
    # Start numbering from the total number of PDFs
    for i, td in enumerate(reversed(pdf_links), start=1):  # Reverse to start numbering from 13, 12...
        # Find the anchor tag inside the td
        a_tag = td.find('a', href=True, target="_blank")
        if a_tag:
            pdf_url = a_tag['href']
            # Ensure the URL is absolute
            if not pdf_url.startswith('http'):
                pdf_url = requests.compat.urljoin(base_url, pdf_url)
            
            # Follow the redirect to find the final PDF URL
            try:
                redirect_response = requests.get(pdf_url, headers=headers, allow_redirects=True)
                final_pdf_url = redirect_response.url  # Get the final redirected URL
                
                # Generate a unique filename using the index
                pdf_name = os.path.basename(final_pdf_url.strip('/'))
                numbered_pdf_name = f"{len(pdf_links) - i + 1}_{company_name}_{pdf_name}"
                save_path = os.path.join(path, numbered_pdf_name)
                
                # Download the PDF
                download_pdf(final_pdf_url, save_path)
            except Exception as e:
                print(f"Error resolving {pdf_url}: {e}")
else:
    print(f"Failed to fetch the webpage: {response.status_code}")
