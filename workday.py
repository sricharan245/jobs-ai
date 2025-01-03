import csv 
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import uuid
from datetime import datetime
import pytz

from config import get_urls

# Load or initialize job_ids_dict from file
try:
        with open('job_ids_dict.pkl', 'rb') as f:
                job_ids_dict = pickle.load(f)
except FileNotFoundError:
        job_ids_dict = {}

print(type(job_ids_dict))
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

company_urls = get_urls()

for company_url in company_urls:
    if company_url not in job_ids_dict:
        job_ids_dict[company_url] = []

while True:
    jobs = []

    for company_url in company_urls:
        jobstosend = []
        today = True

        if "amazon" in company_url:
            driver.get(company_url)
            seturl = company_url
            try:
                while today:
                    time.sleep(2)
                    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'job-tile-lists')))

                    jobs_stack = driver.find_elements(By.CLASS_NAME, 'job-tile-lists')[0]
                    job_elements = jobs_stack.find_elements(By.CLASS_NAME, 'job-tile')
                    
                    print(len(job_elements))
                    # break
                    for job_element in job_elements:
                        job_element = job_element.find_element(By.CLASS_NAME, 'job')
                        job_title_element = job_element.find_element(By.CLASS_NAME, 'job-link')
                        job_id_element = job_element.find_element(By.CLASS_NAME, 'list-unstyled').find_elements(By.TAG_NAME, 'li')[-1]
                        job_id = job_id_element.text.split(":")[-1].strip()                    

                        posted_div_element = job_element.find_elements(By.CLASS_NAME, 'info')[1]
                        posted_on_element = posted_div_element.find_element(By.TAG_NAME, 'h2')
                        updated_on_element = posted_div_element.find_element(By.CLASS_NAME, 'time-elapsed')
                        posted_on = posted_on_element.text + "::" + updated_on_element.text
                        
                        if datetime.now().strftime("%B %d, %Y").lower() in posted_on.lower():
                            job_href = job_title_element.get_attribute('href')
                            job_title = job_title_element.text

                            print(job_id, job_title, job_href, posted_on)
                                # location = location_element.text
                            if job_id not in job_ids_dict[company_url]:
                                job_ids_dict[company_url].append(job_id)
                                jobstosend.append((job_title, job_href, posted_on))
                            else:
                                print(f"Job ID {job_id} already in job_ids_dict")
                        else:
                            today = False
                    
            except Exception as e:
                print(f"An error occurred while processing {company_url}: {str(e)}")
                continue
        
         

        else:    
            driver.get(company_url)
            seturl = company_url
            try:
                while today:
                    time.sleep(2)
                    wait.until(EC.presence_of_element_located((By.XPATH, '//li[@class="css-1q2dra3"]')))
                    
                    job_elements = driver.find_elements(By.XPATH, '//li[@class="css-1q2dra3"]')

                    for job_element in job_elements:
                        job_title_element = job_element.find_element(By.XPATH, './/h3/a')
                        job_id_element = job_element.find_element(By.XPATH, './/ul[@data-automation-id="subtitle"]/li')
                        job_id = job_id_element.text
                        posted_on_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"posted on")]]')
                        posted_on = posted_on_element.text
                        # location_element = job_element.find_element(By.XPATH, './/dd[@class="css-129m7dg"][preceding-sibling::dt[contains(text(),"location")]]')
                        # location = location_element.text
                        if 'posted today' in posted_on.lower():
                            job_href = job_title_element.get_attribute('href')
                            job_title = job_title_element.text
                            # location = location_element.text
                            if job_id not in job_ids_dict[company_url]:
                                job_ids_dict[company_url].append(job_id)
                                jobstosend.append((job_title, job_href, posted_on))
                            else:
                                print(f"Job ID {job_id} already in job_ids_dict")
                        else:
                            today = False

                    next_button = driver.find_element(By.XPATH, '//button[@data-uxi-element-id="next"]')
                    if "disabled" in next_button.get_attribute("class"):
                        break  # exit loop if the "next" button is disabled
                    
                    next_button.click()
            except Exception as e:
                print(f"An error occurred while processing {company_url[:15]}: {str(e)}")
                continue
    
        print(f"jobs at {company_url.split('//')[1].split('.wd')[0]} \n", len(job_ids_dict[company_urls[0]]))
        print("New jobs added: ", len(jobstosend))
        for job_title, job_href, posted_on in jobstosend:
            # driver.get(job_href)
            # time.sleep(1)
            # job_posting_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-automation-id="job-posting-details"]')))
            # job_posting_text = job_posting_element.text
            # redis_id = str(uuid.uuid4())
            job_info = {'company_url': seturl,'job_title': job_title, 'job_href': job_href, 'posted_on': posted_on}
            jobs.append((seturl, job_title, job_href, posted_on))


    # Write job postings to a CSV file
    with open('job_postings.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['companyurl','Job Title', 'Job Href', 'Posted On'])
        for job in jobs:
            writer.writerow(job)

    # Save job_ids_dict to file
        with open('job_ids_dict.pkl', 'wb') as f:
            pickle.dump(job_ids_dict, f)
    current_time = datetime.now(pytz.timezone('America/Chicago')).strftime('%Y-%m-%d %H:%M:%S')
    print(f"At {current_time} total {len(jobs)} jobs added to csv...")

    # Wait for a certain period before running again
    time.sleep(900)  # Run every 15min
