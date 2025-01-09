import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Setup Selenium WebDriver
driver = webdriver.Chrome()  # Or your preferred browser driver

# Step 1: Navigate to the Screener login page
driver.get("https://www.screener.in/login/")

# Step 2: Log in
username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")
login_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")

# Replace with your actual credentials
username_input.send_keys("ISHAN")  # Replace 'your_username' with your Screener username
password_input.send_keys("1I$#@/\\/5.")  # Replace 'your_password' with your Screener password
login_button.click()

# Step 3: Wait for login to complete
time.sleep(5)

# Step 4: Navigate to the target page
driver.get("https://www.screener.in/company/TCS/#quarters")

# Step 5: Click the "+" button (adjust the selector as needed)
time.sleep(3)  # Wait for the page to fully load
try:
    plus_button = driver.find_element(By.CLASS_NAME, "blue-icon")
    plus_button.click()
    time.sleep(3)  # Wait for the dropdown data to load
except Exception as e:
    print(f"Error clicking '+' button: {e}")

# Step 6: Get the updated page source after rendering
html = driver.page_source

# Step 7: Use BeautifulSoup to parse the updated HTML
soup = BeautifulSoup(html, 'html.parser')

# Step 8: Extract tabular data from the "card" or "card-large" class
table_data = []
tables = soup.find_all("div", class_="card") + soup.find_all("div", class_="card-large")
for table in tables:
    rows = table.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        table_data.append([cell.text.strip() for cell in cells])

# Step 9: Convert to DataFrame
df = pd.DataFrame(table_data)

# Step 10: Save the DataFrame to an Excel file
excel_file = "tabular_data.xlsx"
df.to_excel(excel_file, index=False, header=False)

print(f"Tabular data has been saved to {excel_file}")

# Step 11: Close the browser
driver.quit()
