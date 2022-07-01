
from selenium import webdriver
from bs4 import BeautifulSoup
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
import csv

#some example linkedin urls.
#https://www.linkedin.com/jobs/search?keywords=Psychology&location=Penang%2C%20Malaysia&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0
#https://www.linkedin.com/jobs/search?keywords=Mechanical%20Engineering&location=Penang%2C%20Malaysia&geoId=103532529&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0
#https://www.linkedin.com/jobs/search?keywords=Artificial%20Intelligence%20%28AI%29&location=Hong%20Kong%20SAR&geoId=103291313&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0

# On the linkedin job search function. Apply the filters that you want and then copy that url and paste it here underneath 
url = 'https://de.linkedin.com/jobs/search?keywords=Seven%20Senders&location=&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
# Change this as well when you run the code, it changes the name of the csv file
company_name_csv = "seven senders"

#Chromedriver can be downloaded here :https://chromedriver.chromium.org/
#location of the web driver in your pc
driver = webdriver.Chrome(executable_path='C:/Users/Admin/Downloads/chromedriver_win32/chromedriver.exe')
#maximize window so that when a job is clicked on, it is shown on the left side of the page. Otherwise there is an error.
driver.maximize_window()
driver.get(url)


no_of_jobs = driver.find_element_by_css_selector('h1>span').get_attribute('innerText')
print(no_of_jobs)
# If the number is really large, it is often represented with a plus at the end like 100000+ so I remove this '+' symbol
for char in '+,':
    no_of_jobs = no_of_jobs.replace(char, '')

no_of_jobs = int(no_of_jobs)

i = 2
#"show more" can be clicked a maximum of 34 times before it does not show more.
#shows only maximum 1000 jobs per filter. So one would need to use multiple filters to get all available jobs.
# TODO: if n0_of_jobs too large, it keeps clicking on the show more button but nothing will happen. The no of jobs should be below 1000 so that this doesnt happen
while i <= int(no_of_jobs/25) + 1:
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    i = i + 1
    set1 = driver.find_elements_by_css_selector('button.infinite-scroller__show-more-button.infinite-scroller__show-more-button--visible')
    for a in set1:
        a.click()

    time.sleep(3)
#WScroll back to the top. Otherwise the click does not work.
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

# method using beautiful soup but not needed anymore
'''
job_src = driver.page_source
  
soup = BeautifulSoup(job_src, 'lxml')   

jobs_html = soup.find_all('h3', {'class': 'base-search-card__title'})
  
job_titles = []
  
for title in jobs_html:
    job_titles.append(title.text.strip())
  
print(job_titles)
print(len(job_titles))
'''

job_lists = driver.find_element_by_class_name('jobs-search__results-list')
jobs = job_lists.find_elements_by_tag_name('li')

#print(len(jobs))

#the data from job description ("jd") is so far the only reliable outcome.
job_title = []
company_name = []
location = []
date = []
job_link = []

jd = []
seniority = []
emp_type = []
job_func = []
industries = []

for job in jobs:
    jd0 = []
    job_func0=[]
    industries0=[]
 
    job_title0 = job.find_element_by_css_selector('h3').get_attribute('innerText')
    job_title.append(job_title0)
 
    company_name0 = job.find_element_by_css_selector('h4').get_attribute('innerText')
    company_name.append(company_name0)
 
    location0 = job.find_element_by_css_selector('[class="job-search-card__location"]').get_attribute('innerText')
    location.append(location0)
 
    date0 = job.find_element_by_css_selector('div>div>time').get_attribute('datetime')
    date.append(date0)
 
    job_link0 = job.find_element_by_css_selector('a').get_attribute('href')
    print(job_link0)
    job_link.append(job_link0)
    job.find_element_by_css_selector('a').click()
    time.sleep(3)
    #/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div/text()[1]

    jd_path = '/html/body/div[3]/div/section/div[2]/div/section[1]/div/div/section/div'
    #jd_elements = job.find_element(By.CSS_SELECTOR, 'div.show-more-less-html__markup')
    if job.find_elements_by_xpath(jd_path):
        jd_elements = job.find_elements_by_xpath(jd_path)
        for element in jd_elements:
            jd0.append(element.get_attribute('innerText'))
            jd_final = ', '.join(jd0)
            jd.append(jd_final)
    else:
        jd.append('NULL')
    #TODO: doesnt work all the time so find another path
    seniority_path = '/html/body/div[3]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'

    if job.find_element_by_xpath(seniority_path):
        seniority0 = job.find_element_by_xpath(seniority_path).get_attribute('innerText')
        seniority.append(seniority0)
    else:
        seniority.append('NULL')

    #TODO: not a good solution for the two emp_type, find a better way to locate the html element
    emp_type_path = '/html/body/div[3]/div/section/div[2]/div/section[1]/div/ul/li[2]/span'
    emp_type_path0 = '/html/body/div[3]/div/section/div[2]/div/section/div/ul/li/span'

    try:
        if job.find_element_by_xpath(emp_type_path):
            emp_type0 = job.find_element_by_xpath(emp_type_path).get_attribute('innerText')
            emp_type.append(emp_type0)
        else:
            emp_type.append('NULL')
    except:
        if job.find_element_by_xpath(emp_type_path0):
            emp_type0 = job.find_element_by_xpath(emp_type_path0).get_attribute('innerText')
            emp_type.append(emp_type0)
        else:
            emp_type.append('NULL')

    
    #TODO: doesnt work all the time, find another path
    job_func_path = '/html/body/div[3]/div/section/div[2]/div/section[1]/div/ul/li[3]/span'

    if job.find_elements_by_xpath(job_func_path):
        job_func_elements = job.find_elements_by_xpath(job_func_path)
        for element in job_func_elements:
            job_func0.append(element.get_attribute('innerText'))
            job_func_final = ', '.join(job_func0)
            job_func.append(job_func_final)
    else:
        job_func.append('NULL')

    #TODO: doesnt work all the time, find another path
    industries_path = '/html/body/div[3]/div/section/div[2]/div/section[1]/div/ul/li[4]/span'

    if job.find_elements_by_xpath(industries_path):
        industries_elements = job.find_elements_by_xpath(industries_path)
        for element in industries_elements:
            industries0.append(element.get_attribute('innerText'))
            industries_final = ', '.join(industries0)
            industries.append(industries_final)
    else:
        industries.append('NULL')


#headings for the csv file:
headings = ["URL", "Title", "Company", "Location", "Date", "Description", "Seniority", "Employment Type", "Function", "Industries" ]
#open csv file

save_cvs_row = [job_link, job_title, company_name, location, date, jd, seniority, emp_type, job_func, industries]


with open('C:/Users/Admin/source/repos/webcrawler3/' + company_name_csv + '.csv', 'w', encoding='utf-8') as fi:
    #create csv writer
    writer = csv.writer(fi)
    writer.writerow(headings)
    for a, b, c, d, e, f, g, h, i, j in zip(job_link, job_title, company_name, location, date, jd, seniority, emp_type, job_func, industries):
        row = [a, b, c, d, e, f, g, h, i, j]
        writer.writerow(row)
    fi.close()

print(job_title)
print(location)
print(date)

print(len(job_title))
print(len(company_name))
print(len(location))
print(len(date))
print(len(job_link))

print(jd)
print(seniority)
print(emp_type)
print(job_func)
print(industries)

print(len(jd))
print(len(seniority))
print(len(emp_type))
print(len(job_func))
print(len(industries))



#some other ideas below but it has problems
'''
jd = []
seniority = []
emp_type = []
job_func = []
industries = []

#job_click_path = f'/html/body/div[3]/div/main/section[2]/ul/li[166]/div/a'
#job_click = wd.find_element_by_xpath(job_click_path).click()
#wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='view all']"))).click()

for item in range(len(jobs)):
    jd0 = []
    job_func0=[]
    industries0=[]
    # clicking job to view job details
    job_click_path = f'//html/body/div[1]/div/main/section[2]/ul/li[{item+1}]/div/a'
    job_click_path0 = f'/html/body/div[1]/div/main/section[2]/ul/li[{item+1}]/a'
    print(f'{item+1}')
    try:
        job_click = job.find_element_by_xpath(job_click_path0).click()
    except:
        job_click = job.find_element_by_xpath(job_click_path0).click()
    time.sleep(3)

    jd_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/div/section/div'
    jd_elements = job.find_element_by_xpath(jd_path)
    for element in jd_elements:
        jd0.append(element.get_attribute('innerText'))
        jd_final = ', '.join(jd0)
        jd.append(jd_final)

    seniority_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[1]/span'
    try:
        seniority0 = job.find_element_by_xpath(seniority_path).get_attribute('innerText')
        seniority.append(seniority0)
    except:
        seniority.append(' ')
    
 
    emp_type_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[2]/span'
    try:
        emp_type0 = job.find_element_by_xpath(emp_type_path).get_attribute('innerText')
        emp_type.append(emp_type0)
    except:
        emp_type.append(' ')
        pass
    
 
    job_func_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[3]/span'
    try:
        job_func_elements = job.find_elements_by_xpath(job_func_path)
        for element in job_func_elements:
            job_func0.append(element.get_attribute('innerText'))
            job_func_final = ', '.join(job_func0)
            job_func.append(job_func_final)
    except:
        job_func.append(' ')
        pass

    industries_path = '/html/body/div[1]/div/section/div[2]/div/section[1]/div/ul/li[4]/span'
    try:
        industries_elements = job.find_elements_by_xpath(industries_path)
        for element in industries_elements:
            industries0.append(element.get_attribute('innerText'))
            industries_final = ', '.join(industries0)
            industries.append(industries_final)
    except:
        industries.append(' ')
        pass


print(jd)
print(seniority)
print(emp_type)
print(job_func)
print(industries)

print(len(jd))
print(len(seniority))
print(len(emp_type))
print(len(job_func))
print(len(industries))

'''