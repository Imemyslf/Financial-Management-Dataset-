from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Path to your WebDriver (e.g., chromedriver.exe for Chrome)
driver_path = "path_to_chromedriver"

# Initialize the WebDriver
driver = webdriver.Chrome(driver_path)

# Open the URL
url = "https://www.moneycontrol.com/india/stockpricequote/computers-software/infosys/IT"
driver.get(url)

# Wait for the page to load completely (you may need WebDriverWait for dynamic content)
driver.implicitly_wait(10)

# List of desired link texts to click
desired_links = [
    "Balance Sheet",
    "Profit & Loss",
    "Quarterly Results",
    "Yearly Results",
    "Cash Flows",
    "Ratios"
]

# Find all links on the page
links = driver.find_elements(By.TAG_NAME, "a")

# Loop through links and click on the matching ones
for link in links:
    if link.text in desired_links:
        print(f"Clicking on: {link.text}")
        ActionChains(driver).move_to_element(link).click(link).perform()

# Close the driver after interactions
driver.quit()
