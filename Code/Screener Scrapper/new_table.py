# from img2table.ocr import TesseractOCR
# from img2table.document import Image

# # Specify Tesseract path
# ocr = TesseractOCR(tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe", n_threads=1, lang="eng")

# # Instantiation of document
# doc = Image(r"C:\Users\rayya\Desktop\All-Files\Programs\FYP\Financial-Management-Dataset-\Code\Screener Scrapper\pandl.jpg")
# # Table extraction
# extracted_tables = doc.extract_tables(ocr=ocr,
#                                       implicit_rows=False,
#                                       implicit_columns=False,
#                                       borderless_tables=False,
#                                       min_confidence=50)

from img2table.ocr import TesseractOCR
from img2table.document import Image as TableImage  # Rename to avoid conflict
from pytesseract import image_to_string
from PIL import Image  # Keep for handling images
import pandas as pd
# OCR with pytesseract
text = image_to_string(Image.open(r"C:\Users\sharm\OneDrive\Desktop\Kishan\Contractzy\WebScrapping\Tutorial\Code\Screener Scrapper\page2_image.png"))
print(text)

# Parse the text into structured data
rows = []
lines = text.strip().split("\n")
header = ["Description", "2020", "2021", "2022"]
rows.append(header)

for line in lines[1:]:  # Skip the header line in text
    parts = line.split()
    if len(parts) >= 4:
        description = " ".join(parts[:-3])  # Combine all parts except last 3 as description
        values = parts[-3:]  # Last 3 parts are the values
        rows.append([description] + values)

# Create a DataFrame
df = pd.DataFrame(rows[1:], columns=rows[0])

# Save to Excel
output_path = r"C:\Users\sharm\OneDrive\Desktop\financial_report_Page_2.xlsx"
df.to_excel(output_path, index=False)

print(f"Excel file saved at: {output_path}")

exit()

# Instantiate TesseractOCR
ocr = TesseractOCR(n_threads=1, lang="eng")

# Load and process the image using img2table
doc = TableImage(r"C:\Users\sharm\OneDrive\Desktop\Kishan\Contractzy\WebScrapping\Tutorial\Code\Screener Scrapper\pandl.jpg")
extracted_tables = doc.extract_tables(
    ocr=ocr,
    implicit_rows=True,
    implicit_columns=True,
    borderless_tables=True,  # For borderless tables
    min_confidence=50,
)

print(extracted_tables)

import pandas as pd

# Save extracted tables to an Excel file
if extracted_tables:  # Ensure tables are not empty
    with pd.ExcelWriter("43_extracted_tables.xlsx") as writer:
        for idx, table in enumerate(extracted_tables):
            # Convert table content to a DataFrame
            df = pd.DataFrame(table.content)
            # Save each table as a separate sheet
            sheet_name = f"Table_{idx+1}"
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
    print("Extracted tables saved as 43_extracted_tables.xlsx")
else:
    print("No tables extracted.")
