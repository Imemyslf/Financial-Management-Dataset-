from img2table.ocr import TesseractOCR
from img2table.document import Image

# Specify Tesseract path
ocr = TesseractOCR(tesseract_path=r"C:\Program Files\Tesseract-OCR\tesseract.exe", n_threads=1, lang="eng")

# Instantiation of document
doc = Image(r"C:\\Users\\rayya\\Desktop\\All-Files\\Programs\\FYP\\Financial-Management-Dataset-\\Code\\Screener Scrapper\\pandl.jpg")

# Table extraction
extracted_tables = doc.extract_tables(ocr=ocr,
                                      implicit_rows=False,
                                      implicit_columns=False,
                                      borderless_tables=False,
                                      min_confidence=50)
