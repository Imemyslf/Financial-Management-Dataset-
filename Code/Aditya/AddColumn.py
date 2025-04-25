import pandas as pd
import os

# Define file paths
input_file_path = r"C:/Users/Aditya/Desktop/FyPro/Companies/Financial_Data/MoneyControl/Companies/IT Services & Consulting/Wipro Ltd/Pruned_Excel/Semi_Final/Wipro Ltd_Semi_Final.xlsx"
output_dir = r"C:\Users\Aditya\Desktop\FyPro\Companies\Updated"
output_file_path = os.path.join(output_dir, "Updated_Quarterly_Data.xlsx")

# Load the Excel file
df = pd.read_excel(input_file_path, sheet_name="Quarterly")

# Create "Total Revenue" column
df["Total Revenue"] = df["Net sales/income from operations"] + df["Other income"]

# Create "Total Expenditure" column
df["Total Expenditure"] = (
    df["Employees cost"] + 
    df["depreciat"] + 
    df["Other expenses"] + 
    df["Interest"] + 
    df["Tax"]
)

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Save the updated file
df.to_excel(output_file_path, index=False)
print(f"✅ File saved at: {output_file_path}")



