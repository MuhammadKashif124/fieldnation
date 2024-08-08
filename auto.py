from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os

# Configuration
max_distance = 5  # miles
min_pay_rate = 20  # dollars per hour
fieldnation_url = "https://app.fieldnation.com/workorders"

# Chrome options to open new tabs in the background
chrome_options = Options()
chrome_options.add_argument("--new-tab")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("start-maximized")

user_profile = "C:\\Users\\evenb\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
chrome_options.add_argument(f"user-data-dir={user_profile}")



# Path to chromedriver.exe
driver_path = "D:\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"

# Verify the path
if not os.path.isfile(driver_path):
    raise FileNotFoundError(f"Chromedriver not found at {driver_path}")

print(f"Using chromedriver at: {driver_path}")

# Initialize WebDriver with the specified path
driver = webdriver.Chrome(service=Service(driver_path), options=chrome_options)

# Open the Field Nation work orders page
driver.get(fieldnation_url)

# Wait for the page to load
time.sleep(5)  # Adjust this delay if necessary

# Find all job rows
jobs = driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

for job in jobs:
    try:
        # Extract distance and pay rate for each job
        distance_text = job.find_element(By.XPATH, ".//td[contains(@class, 'distance')]").text
        pay_text = job.find_element(By.XPATH, ".//td[contains(@class, 'pay')]").text

        # Parse distance (assuming it's in miles)
        distance = float(distance_text.split()[0])

        # Parse pay rate (assuming hourly and extracting the rate)
        if "hourly" in pay_text:
            pay_rate = float(pay_text.split('$')[1].split('/')[0])
        else:
            continue  # Skip if not an hourly job

        # Check if the job meets the criteria
        if distance <= max_distance and pay_rate >= min_pay_rate:
            # Click on the job title to open in a new tab
            title_link = job.find_element(By.XPATH, ".//td[contains(@class, 'title')]//a")
            title_link.send_keys(Keys.CONTROL + Keys.RETURN)
            time.sleep(1)  # Small delay to avoid overwhelming the browser

    except Exception as e:
        print(f"Error processing a job row: {e}")
        continue

# Close the WebDriver after a delay
time.sleep(10)  # Adjust this delay to keep tabs open for a while
driver.quit()
