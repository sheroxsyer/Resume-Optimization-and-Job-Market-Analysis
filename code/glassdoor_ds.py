from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Setup Selenium WebDriver (non-headless for debugging)
options = webdriver.ChromeOptions()
# Remove headless mode to observe the browser actions (if needed)
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the Glassdoor job search page
url = "https://www.glassdoor.com/Job/pakistan-data-scientist-jobs-SRCH_IL.0,8_IN192_KO9,23.htm"
driver.get(url)

# Wait for the page to load
time.sleep(5)

# Handle cookies popup (if it appears)
try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept All']"))
    )
    accept_button.click()
    print("Accepted cookies.")
except:
    print("No cookies popup.")

# Scroll gradually to load all jobs
for i in range(10):  # Adjust the range to load more jobs
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(3)  # Small delay between scrolls to load content

# Wait for the job cards to load
try:
    job_cards = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "react-job-listing"))
    )
    print(f"Found {len(job_cards)} job cards.")
except Exception as e:
    print(f"Error: {e}")
    driver.quit()
    exit()

# Initialize lists to store job data
job_titles = []
companies = []
locations = []
job_links = []

# Extract data from each job card (up to 30 jobs)
for card in job_cards[:30]:
    try:
        # Extract job title
        job_title = card.find_element(By.CLASS_NAME, "jobTitle").text
        job_titles.append(job_title)

        # Extract company name
        company = card.find_element(By.CLASS_NAME, "jobEmpolyerName").text
        companies.append(company)

        # Extract location
        location = card.find_element(By.CLASS_NAME, "jobLocation").text
        locations.append(location)

        # Extract job link
        job_link = card.get_attribute("href")
        job_links.append(job_link)

    except Exception as e:
        print(f"Error extracting data for a job card: {e}")

# Save data to CSV
df = pd.DataFrame({
    'Job Title': job_titles,
    'Company': companies,
    'Location': locations,
    'Job Link': job_links
})

df.to_csv('glassdoor_jobs.csv', index=False)
print("Data saved to glassdoor_jobs.csv")

# Close the browser
driver.quit()
