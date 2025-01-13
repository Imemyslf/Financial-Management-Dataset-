# from tabula import read_pdf
# from tabula import convert_into
# import pandas as pd
# import os

# curr_dir = os.getcwd()

# company_name = "Tata Consultancy Services Ltd"

# file_name_pdf = "1_Tata Consultancy Services Ltd_23fa9848-11a3-432f-be38-04e3be97419a.pdf"

# pdf_path = f"{curr_dir}/Main_Data/Screener/PDF/{company_name}/{file_name_pdf}"

# # Extract tables from the PDF into a DataFrame
# # Specify the `pages` parameter to extract from specific pages or use "all" for all pages
# tables = read_pdf(pdf_path, pages="7", multiple_tables=True, pandas_options={"header": None})

# print(tables)

# exit()
# # Iterate through the extracted tables
# for i, table in enumerate(tables):
#     print(f"Table {i+1}:")
#     print(table)
#     print("\n")

#     # Save each table as a CSV file (optional)
#     table.to_csv(f"table_{i+1}.csv", index=False)


# import pdfplumber
# import pandas as pd
# import os

# # Set up the directory and file details
# curr_dir = os.getcwd()
# company_name = "Tata Consultancy Services Ltd"
# file_name_pdf = "1_Tata Consultancy Services Ltd_23fa9848-11a3-432f-be38-04e3be97419a.pdf"

# pdf_path = f"{curr_dir}/Main_Data/Screener/PDF/{company_name}/{file_name_pdf}"

# # Open the PDF and extract the table from page 7
# with pdfplumber.open(pdf_path) as pdf:
#     # Ensure the page exists
#     if len(pdf.pages) >= 7:
#         # Get page 7 (index 6 because Python uses 0-based indexing)
#         page = pdf.pages[6]
#         tables = page.extract_tables()
#         for table_index, table in enumerate(tables):
#             # Convert table to DataFrame
#             df = pd.DataFrame(table[1:], columns=table[0])

#             # Save the table as a CSV file
#             output_file = f"{pdf_path.split('/')[-1].split('.')[0]}_Page7_Table{table_index + 1}.xlsx"
#             df.to_excel(output_file, index=False)
#             print(f"Saved: {output_file}")
#     else:
#         print("Page 7 does not exist in the PDF.")

# import pdfplumber
# import pytesseract
# from PIL import Image
# import pandas as pd
# import os

# # Set up the directory and file details
# curr_dir = os.getcwd()
# company_name = "Tata Consultancy Services Ltd"
# file_name_pdf = "1_Tata Consultancy Services Ltd_23fa9848-11a3-432f-be38-04e3be97419a.pdf"

# pdf_path = f"{curr_dir}/Main_Data/Screener/PDF/{company_name}/{file_name_pdf}"

# # Helper function to process OCR on a page
# def extract_table_with_ocr(page):
#     # Convert the page to an image
#     image = page.to_image()
#     image = image.original

#     # Use OCR to extract text
#     text = pytesseract.image_to_string(image)

#     # Save the OCR-extracted text for reference
#     with open("Page7_OCR_Text.txt", "w") as file:
#         file.write(text)

#     # Attempt to extract tables using pdfplumber
#     tables = page.extract_tables()

#     # If tables exist, process them
#     if tables:
#         for table_index, table in enumerate(tables):
#             df = pd.DataFrame(table[1:], columns=table[0])
#             output_file = f"{pdf_path.split('/')[-1].split('.')[0]}_Page7_Table{table_index + 1}.csv"
#             df.to_csv(output_file, index=False)
#             print(f"Saved: {output_file}")
#     else:
#         print("No tables found on page 7 after OCR processing.")

# # Open the PDF and extract table from page 7
# with pdfplumber.open(pdf_path) as pdf:
#     if len(pdf.pages) >= 7:
#         # Get page 7 (index 6 for 0-based indexing)
#         page = pdf.pages[6]
#         extract_table_with_ocr(page)
#     else:
#         print("Page 7 does not exist in the PDF.")

import pytesseract
from PIL import Image
import pandas as pd
import cv2
import numpy as np
import os

# Set up the directory and file details
curr_dir = os.getcwd()
company_name = "Tata Consultancy Services Ltd"
file_name_pdf = "1_Tata Consultancy Services Ltd_23fa9848-11a3-432f-be38-04e3be97419a.pdf"

pdf_path = f"{curr_dir}/Main_Data/Screener/PDF/Screenshot 2025-01-10 113916.png"

# Load the image
image_path = f"{curr_dir}/Main_Data/Screener/PDF/Screenshot 2025-01-10 113916.png"  # Path to the uploaded image
image = cv2.imread(image_path)

# Preprocess the image for better OCR results
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Thresholding to binarize
processed_image = cv2.medianBlur(thresh, 3)  # Reduce noise

# Use Tesseract OCR to extract text
custom_config = r'--psm 6'  # Page segmentation mode for tabular data
text = pytesseract.image_to_string(processed_image, config=custom_config)

# Save the raw OCR output to a text file for reference
with open("ocr_output.txt", "w") as file:
    file.write(text)

# Process the OCR text into a structured table
# Assuming the columns are separated by consistent spacing or tab
lines = text.split("\n")
data = [line.split() for line in lines if line.strip()]  # Split by spaces/tabs and remove empty lines

# Convert the data into a pandas DataFrame
df = pd.DataFrame(data)

# Save the table as a CSV
output_csv_path = "extracted_table.csv"
df.to_csv(output_csv_path, index=False)
print(f"Extracted table saved to: {output_csv_path}")

