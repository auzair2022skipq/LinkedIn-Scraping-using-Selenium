import time
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()

driver.get(f"https://www.linkedin.com/jobs/search/?geoId=102872943&keywords=data%20scientist&location=United%20States")

SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

job_elems = driver.find_elements(By.CLASS_NAME,"sr-only")
job_titles = []
for job_elem in job_elems:
    if job_elem.text != "LinkedIn" and job_elem.text != "":
        job_titles.append(job_elem.text)


company_elems =driver.find_elements(By.CLASS_NAME,"hidden-nested-link")
company_names = []
for company_elem in company_elems:
        company_names.append(company_elem.text)


company_url_elems = driver.find_elements(By.CLASS_NAME,"hidden-nested-link")
company_urls = []
for company_url_elem in company_url_elems:
    url = company_url_elem.get_attribute('href')
    if "linkedin.com/company/" in url:
        company_urls.append(url)
    else:
        company_urls.append(None)



job_data = pd.DataFrame({
    'Job Title': job_titles,
    'Company Name': company_names,
     'Company LinkedIn URL': company_urls,
    #  'Company Size': company_sizes,
    #  'Industry': industries
 })

job_data.to_excel('linkedin_jobs.xlsx', index=False)
driver.quit()

print(len(job_data),len(company_names),len(company_urls))

