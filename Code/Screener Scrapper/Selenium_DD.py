import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import time

# Setup Selenium WebDriver
try:
    driver = webdriver.Chrome()  # Ensure ChromeDriver is correctly installed and added to PATH
    print("Browser launched successfully.")
except Exception as e:
    print(f"Error launching browser: {e}")
    exit()

# Step 1: Navigate to the Screener login page
driver.get("https://www.screener.in/login/")
print("Navigated to Screener login page.")

# Step 2: Log in using the correct IDs
try:
    # Wait for the email input to appear
    username_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "id_username"))
    )
    username_input.send_keys("i8546617@gmail.com")  # Replace with your Screener username
    print("Email entered successfully.")

    # Wait for the next button with the class "button" and click it
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "button"))
    )
    next_button.click()
    print("Next button clicked.")

    # Wait for the password input field to appear
    password_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "id_password"))
    )
    password_input.send_keys("1I$#@/\\/5.")  # Replace with your Screener password
    print("Password entered successfully.")

    # Wait for the updated login button with class "button-primary" and click it
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "button-primary"))
    )
    login_button.click()
    print("Login button clicked.")

    # Step 3: Wait for login to complete (adjust URL or dashboard check as needed)
    WebDriverWait(driver, 10).until(
        EC.url_contains("dashboard")  # Update if necessary based on Screener's post-login URL
    )
    print("Login successful!")
except TimeoutException as e:
    print(f"Timeout error during login: {e}")
except NoSuchElementException as e:
    print(f"Element not found during login: {e}")
except Exception as e:
    print(f"Error during login: {e}")
    driver.quit()
    exit()

# Step 4: Navigate to the target page
try:
    driver.get("https://www.screener.in/company/TCS/#quarters")
    print("Navigated to the TCS quarters page.")
except Exception as e:
    print(f"Error navigating to target page: {e}")
    driver.quit()
    exit()

# Step 5: Click the "+" button to expand dropdown (adjust selector as needed)
time.sleep(3)  # Wait for the page to fully load
try:
    plus_button = driver.find_element(By.CLASS_NAME, "blue-icon")  # Adjust if needed
    plus_button.click()
    time.sleep(3)  # Wait for the dropdown data to load
    print("Expanded dropdown successfully.")
except NoSuchElementException as e:
    print(f"Error finding '+' button: {e}")
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
        if cells:  # Skip empty rows
            table_data.append([cell.text.strip() for cell in cells])

# Step 9: Convert to DataFrame
df = pd.DataFrame(table_data)

# Step 10: Save the DataFrame to an Excel file
excel_file = "tabular_data.xlsx"
df.to_excel(excel_file, index=False, header=False)
print(f"Tabular data has been saved to {excel_file}")

# Step 11: Close the browser
driver.quit()

