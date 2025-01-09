import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import camelot  # For extracting tables from PDFs

def extract_h1_name(soup):
    """Extract the name from the <h1> tag."""
    h1_tag = soup.find("h1", class_="h2 shrink-text", style="margin: 0.5em 0")
    if h1_tag:
        return h1_tag.text.strip()
    return "Unknown_Folder"

def scrape_website_and_process_pdfs(base_url, sectors):
    try:
        # Step 1: Fetch the website's content
        response = requests.get(base_url)
        response.raise_for_status()  # Check for request errors
        soup = BeautifulSoup(response.text, "html.parser")

        # Step 2: Extract the folder name from the <h1> tag
        folder_name = extract_h1_name(soup)
        print(folder_name)
        
        base_output_folder = os.path.join("./output", folder_name)
        pdf_folder = os.path.join(base_output_folder, "PDFs")
        excel_folder = os.path.join(base_output_folder, "Tables")

        # Create directories if they don't exist
        os.makedirs(pdf_folder, exist_ok=True)
        os.makedirs(excel_folder, exist_ok=True)

        # Step 3: Find all links from the specific sectors
        pdf_links = []
        for sector in sectors:
            sector_links = soup.find_all("a", href=True, string=lambda text: text and sector.lower() in text.lower())
            print(sector_links)
            # pdf_links.extend(sector_links)

        exit()
        if not pdf_links:
            print(f"No PDF links found for sectors: {sectors}")
            return

        # Step 4: Download PDFs and extract tables
        for link in pdf_links:
            pdf_url = urljoin(base_url, link["href"])
            if pdf_url.endswith(".pdf"):  # Only process links ending with '.pdf'
                pdf_name = os.path.basename(pdf_url)
                pdf_path = os.path.join(pdf_folder, pdf_name)

                # Download the PDF
                print(f"Downloading {pdf_url}...")
                pdf_response = requests.get(pdf_url)
                with open(pdf_path, "wb") as pdf_file:
                    pdf_file.write(pdf_response.content)
                print(f"Saved to {pdf_path}")

                # Extract tables from the PDF
                try:
                    print(f"Extracting tables from {pdf_path}...")
                    tables = camelot.read_pdf(pdf_path, pages="all")
                    if tables:
                        excel_path = os.path.join(excel_folder, pdf_name.replace(".pdf", ".xlsx"))
                        with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
                            for i, table in enumerate(tables):
                                df = table.df
                                df.to_excel(writer, sheet_name=f"Table_{i + 1}", index=False)
                        print(f"Extracted tables saved to {excel_path}")
                    else:
                        print(f"No tables found in {pdf_path}.")
                except Exception as e:
                    print(f"Error extracting tables from {pdf_path}: {e}")

        print("PDF downloading and table extraction completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Specify the base URL of the website to scrape
    base_url = "https://www.screener.in/company/TATACONSUM/consolidated/#quarters"

    # Define the sectors of interest (e.g., keywords, CSS classes, or IDs)
    sectors = ["quaters","profit-loss","balance-sheet","cash-flow"]

    scrape_website_and_process_pdfs(base_url, sectors)
