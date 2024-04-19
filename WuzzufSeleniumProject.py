import os
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

options = Options()
options.binary_location = "C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
driver_path = "C:\\Users\\Alaa\\Desktop\\chromedriver.exe"
driver = webdriver.Chrome(service=Service(driver_path), options=options)

# Function to scrape job information from a given link
def getJobInfo(job_link): 
    try:
        driver.get(job_link)
        wait = WebDriverWait(driver, 10)
        jobTitle = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.css-f9uh36'))).text.strip()
        try:
            company = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.css-tdvcnh'))).text
        except Exception as e:
            companylist = driver.find_elements(By.CSS_SELECTOR, 'div.css-9iujih')
            company = companylist[0].text
        date = driver.find_element(By.CSS_SELECTOR, 'span.css-182mrdn').text.strip()
        job_type = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.css-g65o95'))).text
        location_element = wait.until(EC.presence_of_element_located((By.XPATH, '//strong[contains(@class, "css-9geu3q")]')))
        location = driver.execute_script("return arguments[0].textContent", location_element).split("-")[-1].strip()
        listt= driver.find_elements(By.CSS_SELECTOR, 'span.css-4xky9y')
        experience = listt[0].text if len(listt) > 0 else None
        salary = listt[3].text if len(listt) > 3 else None
        skills = driver.find_element(By.CSS_SELECTOR, 'div.css-1t5f0fr').text
        job_info = {
            "Job Title": jobTitle,
            "Company": company,
            "Date": date,
            "Job Type": job_type,
            "Location": location,
            "Experience": experience,
            "Salary": salary,
            "Skills": skills,
            "Job_Link": job_link  # Assign the job link to the dictionary
        }
        return job_info
    except Exception as e:
        print(f"An error occurred while scraping {job_link}: {e}")
        return None

page = 0
# Function to navigate to the next page
def navigate_to_next_page(page):
    try:
        driver.get(f"https://wuzzuf.net/search/jobs/?a=na&q=data%20analyst&start={page}")
        print(f"Successfully navigated to page {page}.")
    except TimeoutException:
        print("Reached the last page or element not found.")
        return False
    except Exception as e:
        print(f"Failed to navigate to page {page}. Error: {e}")
        return False
    return True

# Initialize an empty list to store all job information
allJobInfo = []
# Initialize current_url and page number
current_url = driver.current_url
# Count successful job scrapes
successful_scrapes = 0

# Main scraping loop
while page <=15:
    if not navigate_to_next_page(page):
        break

    # Get the job detail page URLs
    jobsList = driver.find_elements(By.CSS_SELECTOR, 'div.css-1gatmva.e1v1l3u10')
    job_links = [job.find_element(By.CSS_SELECTOR, 'a.css-o171kl').get_attribute('href') for job in jobsList]

    print(f"Found {len(job_links)} job links on page {page}.")

    # Scrape job information for each job link
    for job_link in job_links:
        print(f"Visiting job link: {job_link}")
        job_info = getJobInfo(job_link)
        if job_info is not None:
            allJobInfo.append(job_info)
            successful_scrapes += 1
            print(f"Successfully scraped job info from {job_link}")
        else:
            print(f"Failed to scrape job info from {job_link}. Page: {page}")

    print(f"Successful scrapes on page {page}: {successful_scrapes}")
    successful_scrapes = 0  # Reset successful scrapes count for the next page
    page += 1

# Quit WebDriver after scraping
driver.quit()

# Write scraped data to CSV file
keys = list(allJobInfo[0].keys()) if allJobInfo else []  # Convert dict_keys to list
filename = "jobs.csv"
path = os.path.join(os.path.expanduser("~"), "Desktop", filename)

if allJobInfo:
    with open(path, "w", newline="", encoding="utf-8") as webscraping:
        dict_writer = csv.DictWriter(webscraping, fieldnames=keys + ["Job Link"])  # Include "Job Link" in fieldnames
        dict_writer.writeheader()
        for job in allJobInfo:
            dict_writer.writerow(job)
        print(f"File '{filename}' saved to Desktop.")
else:
    print("No jobs found.")

