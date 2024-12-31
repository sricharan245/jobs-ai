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

# Load or initialize job_ids_dict from file
try:
        with open('job_ids_dict.pkl', 'rb') as f:
                job_ids_dict = pickle.load(f)
except FileNotFoundError:
        job_ids_dict = {}

print(type(job_ids_dict))
driver = webdriver.Chrome()

wait = WebDriverWait(driver, 10)

company_urls = [
    'https://walmart.wd5.myworkdayjobs.com/en-US/WalmartExternal?clientRequestID=5af893c0f55c4f7d9c4ff14336a46c1b&jobFamilyGroup=e83ebdbd2a0a01af0185848948e94dc6&locationCountry=bc33aa3152ec42d4995f4791a106ed09',
    'https://cvshealth.wd1.myworkdayjobs.com/en-US/CVS_Health_Careers?jobFamilyGroup=e65dbadf6a50100168ed7f2a693c0001',
    'https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Senior-Backend-Engineer---Data-Mining_JR1982374?locationHierarchy1=2fcb99c455831013ea52fb338f2932d8',
    'https://citi.wd5.myworkdayjobs.com/en-US/2/jobs/details/Application-Support-Engineer---Hybrid-_24805666?q=data%20&Country_and_Jurisdiction=bc33aa3152ec42d4995f4791a106ed09&timeType=433d62ef252a012ff4abc7206a0f8000&jobFamilyGroup=e32326e1708d01575bddff0c120102c1&jobFamilyGroup=538c239234271000c428fd3827220000&jobFamilyGroup=e32326e1708d015f865ff60c1201dcc0',
    'https://keybank.wd5.myworkdayjobs.com/en-US/External_Career_Site/details/XMLNAME-2025-Key-s-Technology--Operations---Services--Technology-Track--Rotational-Analyst-Program---Cleveland_R-26611?q=python',
    'https://keybank.wd5.myworkdayjobs.com/en-US/External_Career_Site/details/Commercial-Workout-Analyst_R-29449?q=python',
    'https://sec.wd3.myworkdayjobs.com/en-US/Samsung_Careers/jobs?jobFamilyGroup=189767dd6c9201e189e3eaa6db299dc7&Location_Country=bc33aa3152ec42d4995f4791a106ed09',
    'https://redhat.wd5.myworkdayjobs.com/en-US/jobs/details/Associate-Software-Engineer--AI-Based-IDE-Plugins-_R-043880-1?e=3afab13eadf301a2eaafadcc15425800&a=bc33aa3152ec42d4995f4791a106ed09&d=c18026e77576010f6ef6126f4e43ec4a&d=c18026e7757601cf6eb0136f4e43f04a',
    'https://sonyglobal.wd1.myworkdayjobs.com/en-US/SonyGlobalCareers/details/Analyst--Secure-Sony_JR-116643?locationCountry=bc33aa3152ec42d4995f4791a106ed09&jobFamilyGroup=7306bd11847f108d56a689b7002554ab&jobFamilyGroup=7306bd11847f108d56a585fb30065499',
    'https://santander.wd3.myworkdayjobs.com/en-US/SantanderCareers/details/Sr-Associate--Business-Intelligence---Reporting_Req1393658?jobFamilyGroup=135a3ebce38101db91d599b919013150&jobFamilyGroup=ab9adf92110e011571e710ab1a01034a&jobFamilyGroup=047662461dfb01bf0a10a10a1a01d241&jobFamilyGroup=135a3ebce38101c45b3e18b919012750&source=Santander_com&locationCountry=bc33aa3152ec42d4995f4791a106ed09',
    'https://cat.wd5.myworkdayjobs.com/en-US/CaterpillarCareers?timeType=5367d85d9d52017a289c2294d7135900&jobFamily=e1ea3238dd28100047a9d21828480000&locationCountry=bc33aa3152ec42d4995f4791a106ed09',
    'https://intel.wd1.myworkdayjobs.com/en-US/External/details/Supply-Planning-Analyst_JR0267523?jobFamilyGroup=a55ea4dd831d1000c6fce5a0c4d30000&locations=1e4a4eb3adf101cc4e292078bf8199d0&locations=1e4a4eb3adf1016541777876bf8111cf&locations=1e4a4eb3adf1011246675c76bf81f8ce&locations=1e4a4eb3adf101b8aec18a77bf810dd0&locations=1e4a4eb3adf1018c4bf78f77bf8112d0&locations=1e4a4eb3adf10129d05fe377bf815dd0&locations=1e4a4eb3adf10118b1dfe877bf8162d0',
    'https://homedepot.wd5.myworkdayjobs.com/en-US/CareerDepot/?q=data%20scientist&locationCountry=bc33aa3152ec42d4995f4791a106ed09&workerSubType=3e82bdec28fd014fca89c83b1811b77b',

]  # Add your company URLs here

for company_url in company_urls:
    if company_url not in job_ids_dict:
        job_ids_dict[company_url] = []

while True:
    jobs = []
    for company_url in company_urls:
        jobstosend = []
        driver.get(company_url)
        seturl = company_url
        try:
            today = True
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
                            jobstosend.append((job_title, job_href))
                        else:
                            print(f"Job ID {job_id} already in job_ids_dict")
                    else:
                        today = False

                next_button = driver.find_element(By.XPATH, '//button[@data-uxi-element-id="next"]')
                if "disabled" in next_button.get_attribute("class"):
                    break  # exit loop if the "next" button is disabled
                
                next_button.click()
        except Exception as e:
            print(f"An error occurred while processing {company_url}: {str(e)}")
            continue

        print(len(job_ids_dict[company_urls[0]]))
        print(len(jobstosend))

        for job_title, job_href in jobstosend:
            driver.get(job_href)
            time.sleep(1)
            job_posting_element = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-automation-id="job-posting-details"]')))
            job_posting_text = job_posting_element.text
            redis_id = str(uuid.uuid4())
            job_info = {'company_url': seturl,'job_title': job_title, 'job_href': job_href, 'job_posting_text': job_posting_text}
            jobs.append((seturl, job_title, job_href, job_posting_text))


    # Write job postings to a CSV file
    with open('job_postings.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['companyurl','Job Title', 'Job Href', 'Job Posting'])
        for job in jobs:
            writer.writerow(job)

    # Save job_ids_dict to file
        with open('job_ids_dict.pkl', 'wb') as f:
            pickle.dump(job_ids_dict, f)
    current_time = datetime.now(pytz.timezone('America/Chicago')).strftime('%Y-%m-%d %H:%M:%S')
    print(f"At {current_time} total {len(jobs)} jobs added to csv...")

    # Wait for a certain period before running again
    time.sleep(600)  # Run every hour
