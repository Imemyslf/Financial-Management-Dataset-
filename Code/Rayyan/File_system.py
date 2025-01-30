import os
import pandas as pd

# Define the directory paths
current_dir = os.getcwd()
site = "MoneyControl"
sector = "IT Services & Consulting"

# Lists to hold company names based on column count
companies_with_46_columns = ['3i Infotech Ltd', 'Adroit Infotech Ltd', 'AION-TECH SOLUTIONS Ltd', 'Allied Digital Services Ltd', 'ASM Technologies Ltd', 'Avance Technologies Ltd', 'Bartronics India Ltd', 'Birlasoft Ltd', 'Cambridge Technology Enterprises Ltd', 'CG-Vak Software and Exports Ltd', 'COFORGE LIMITED Ltd', 'Cranes Software International Ltd', 'Cressanda Solution Ltd', 'Cybertech Systems and Software Ltd', 'Cyient Ltd', 'Danlaw Technologies India Ltd', 'Datamatics Global Services Ltd', 'Dynacons Systems and Solutions Ltd', 'Elnet Technologies Ltd', 'Equippp Social Impact Technologies Ltd', 'Expleo Solutions Ltd', 'FCS Software Solutions Ltd', 'Genesys International Corporation Ltd', 'HCL Technologies Ltd', 'Indian Infotech and Software Ltd', 'Infosys Ltd', 'Inspirisys Solutions Ltd', 'IZMO Ltd', 'Jeevan Scientific Technology Ltd', 'Kati Patang Lifestyle Ltd', 'Kellton Tech Solutions Ltd', 'Kernex Microsystems (India) Ltd', 'Mastek Ltd', 'Megasoft Ltd', 'MphasiS Ltd', 'Nettlinx Ltd', 'Onward Technologies Ltd', 'Oracle Financial Services Software Ltd', 'Palred Technologies Ltd', 'Persistent Systems Ltd', 'R Systems International Ltd', 'Sasken Technologies Ltd', 'Saven Technologies Ltd', 'SBSJHVHSV Ltd', 'Securekloud Technologies Ltd', 'Sofcom Systems Ltd', 'Softsol India Ltd', 'Sonata Software Ltd', 'Starcom Information Technology Ltd', 'Tata Consultancy Services Ltd', 'Tech Mahindra Ltd', 'Tera Software Ltd', 'Titan Intech Ltd', 'Trigyn Technologies Ltd', 'USG Tech Solutions Ltd', 'VEDAVAAG Systems Ltd', 'WEP Solutions Ltd', 'Wipro Ltd', 'Xchanging Solutions Ltd', 'Xtglobal Infotech Ltd', 'Zensar Technologies Ltd'] 
companies_with_less_columns = ['Affle India Ltd', 'Alphalogic Techsys Ltd', 'Atishay Ltd', 'Dev Information Technology Ltd', 'Happiest Minds Technologies Ltd', 'Intellect Design Arena Ltd', 'KPIT Technologies Ltd', 'Latent View Analytics Ltd', 'LTIMindtree Ltd', 'Protean eGov Technologies Ltd', 'Quick Heal Technologies Ltd', 'Route Mobile Ltd', 'RPSG VENTURES Ltd', 'Shradha AI Technologies Ltd', 'Sigma Solve Ltd', 'Unicommerce Esolutions Ltd']

# Dictionaries to hold company names and column counts
companies_with_46_columns_dict = {}
companies_with_less_columns_dict = {}

# Get all companies in the sector directory
total_companies = os.listdir(os.path.join(current_dir, "Financial_Data", site, "Companies", sector))

for company in total_companies:
    try:
        # Get the list of files in the "Excel" directory of the company
        excel_dir = os.path.join(current_dir, "Financial_Data", site, "Companies", sector, company, "Excel")

        if not os.path.exists(excel_dir):
            print(f"Directory does not exist: {excel_dir}")
            continue

        excel_files = [file for file in os.listdir(excel_dir) if file.endswith(".xlsx") or file.endswith(".xls")]

        for excel_file in excel_files:
            input_path = os.path.join(excel_dir, excel_file)

            # Check if the file is the target file "Quarterly-result_combined.xlsx"
            if "Quarterly-resul_combined.xlsx" in excel_file:
                try:
                    # Load the Excel file and count the columns
                    df = pd.read_excel(input_path)
                    column_count = len(df.columns)

                    if company in companies_with_46_columns:
                        companies_with_46_columns_dict[company] = column_count
                    elif company in companies_with_less_columns:
                        companies_with_less_columns_dict[company] = column_count

                except Exception as e:
                    print(f"Error reading file {input_path}: {e}")

    except Exception as e:
        print(f"Error processing company {company}: {e}")

# Print results
print("\nCompanies with exactly 46 columns:", companies_with_46_columns_dict)
print("\nCompanies with less than 46 columns:", companies_with_less_columns_dict)

def save_companies():
    with open("List_Company_column.txt", "w") as f:
        f.write(f"Companies with exactly 46 columnsare {len(companies_with_46_columns)}:\n")
        for company, columns in companies_with_46_columns_dict.items():
            f.write(f"{company}: {columns}\n")

        f.write(f"\nCompanies with less than 46 columns are {len(companies_with_less_columns)}:\n")
        for company, columns in companies_with_less_columns_dict.items():
            f.write(f"{company}: {columns}\n")

save_companies()