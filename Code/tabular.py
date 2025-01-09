import tabula

pdf_path = r"C:\\Users\\rayya\\Desktop\\All-Files\\Programs\\FYP\\Financial-Management-Dataset-\\Code\\tata.pdf"

dfs = tabula.read_pdf(pdf_path, pages='17')

print((len(dfs)))
print(dfs[0])