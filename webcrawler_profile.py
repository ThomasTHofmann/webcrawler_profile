from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import csv

from bs4 import BeautifulSoup

driver = webdriver.Chrome(executable_path='C:/Users/Admin/Downloads/chromedriver_win32/chromedriver.exe')
driver.maximize_window()
# some example names from their company:
# seven senders: "Johannes Plehn", "Thomas Hagemann", "Thorben Seiler", "Clemens Kress", "Martijn Kleij", "Steffen Heilmann"
# airttable: "Howie Liu", "Andrew Ofstad", "Emmett Nicholas", "Archana Agrawal", "Peter Deng", "Raymond Endres", "Johanna Jackman,", "Seth Shaw", "Ambereen Toubassy"
names = ["Blair LaCorte", "Luis Dussan", "Bob Brown", "Rick Tewell", "T.R. Ramachandran", "Stephen Lambright", "Andrew Hughes", "Brent Blanchard", "Jordan Greene"]
company = "Aeye"

#headings for the csv file:
headings = ["Profile URL", "Name", "Title", "About", "Experience", "Education", "Skills"]
#open csv file: this just writes the headings. New rows get edited further down
with open('C:/Users/Admin/source/repos/webcrawler-profile/' + company + '.csv', 'w') as f:
    #create csv writer
    writer = csv.writer(f)
    writer.writerow(headings)
    f.close()

profile_links = []

# this searches bing with the name and company and returns the most relevant link.
# TODO: The most relevant link however is not always correct as they might not have a linked in profile, something else will be taken instead. But it doesnt happen often. Most have linkedin profiles.
for name in names:
    query = "site:linkedin.com/in/ " + "AND " + name + " " + "AND " + company
    print(query)
    url = f"https://bing.com/search?q={query}"
    driver.get(url)
    time.sleep(2)
    
    #use this for all links on the bing page: "//a[@href]"

    #path for links on bing search page
    url_path = '//h2/a[@href]'
    links = driver.find_elements_by_xpath(url_path)

    #get first result from the bing search page
    link0 = links[0].get_attribute("href")
    profile_links.append(link0)
    #Code below is to get all the links on the bing search page.
    #for link in links:
        #link0 = link.get_attribute("href")
        #profile_links.append(link0)

print(profile_links)


#linkedin profile scrapper part:
#Some Test profiles:
#https://www.linkedin.com/in/thhagemann
#https://de.linkedin.com/in/johannes-plehn-phd-11588919
#https://de.linkedin.com/in/thorsten-seiler-18169a166
#profile = 'https://www.linkedin.com/in/thhagemann'

#fill in own linkedin account username and password
linkedin_username = "username"
linkedin_password = "password"

#open linkedin login page
driver.get('https://www.linkedin.com/login')

#Enter login info:
username = driver.find_element_by_id('username')
username.send_keys(linkedin_username)

password = driver.find_element_by_id('password')
password.send_keys(linkedin_password)

password.send_keys(Keys.RETURN)
time.sleep(6)
for profile in profile_links:

    driver.get(profile)
    time.sleep(7)

    #to move forward and backward use driver.forward() driver.back()

    #experience, education, skills
    experience_title = []
    #experience_company = []
    education_school = []
    #education_subject = []
    skills = []

    section_lists = driver.find_elements_by_css_selector('.artdeco-card.ember-view.relative.break-words.pb3.mt2 ')
    #EXPERIENCE
    for section in section_lists:
        #if this section contains the id 'experience' continue
        if section.find_elements_by_id('experience'):
            #if a show more button exists continue and click on the link, then scrape the new page that opened and then go back to the previous page.
            if section.find_elements_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid'):
                section.find_element_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid').click()
                time.sleep(6)
                #Scroll all the way down
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    #Scroll to bottom
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # Wait to load page
                    time.sleep(2)
                    # Calculate new scroll height and compare with last scroll height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                #get new driver page for the new page that opened after the click
                lists = driver.find_element_by_css_selector('.pvs-list ')
                parts = lists.find_elements_by_tag_name('li')
                for part in parts:
                    #first part is the experience title
                    if part.find_elements_by_css_selector('.visually-hidden'):
                        p = part.find_elements_by_css_selector('.visually-hidden')
                        for part0 in p:
                            experience_title.append(part0.get_attribute('innerText'))
                    else:
                        experience_title.append('NULL')
                    # The comment below was another idea but doesnt work reliably
                    #TODO: If the experience has multiple sub elements it will return NULL so fix it.
                    #second part is the company where they worked at
                    '''
                    if part.find_elements_by_css_selector('.visually-hidden')[1]:
                        part1 = part.find_elements_by_css_selector('.visually-hidden')[1]
                        experience_company.append(part1.get_attribute('innerText'))
                    else:
                        experience_company.append('NULL')
                    '''

                print("scrape experiences from site")
                driver.execute_script("window.history.go(-1)")
                time.sleep(7)
                #leave the loop early since the data is already scraped
                break
            else:
                #no show more button so just scrape what is already there
                print("scrape experiences from profile")
                #check if there is a list is empty in this section
                if section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap'):
                    section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap')
                    items = section.find_elements_by_tag_name('li')
                    for item in items:
                        if item.find_elements_by_css_selector('.visually-hidden'):
                            i = item.find_elements_by_css_selector('.visually-hidden')
                            for item0 in i:
                                experience_title.append(item0.get_attribute('innerText'))
                        else:
                            experience_title.append('NULL')
                        '''
                        #code below is a way to try to divide the experience section into sub sections like the experience title and experience company name instead of 
                        #check if the item exists
                        if item.find_elements_by_css_selector('.visually-hidden')[0]:
                            #title of the experience
                            item0 = item.find_elements_by_css_selector('.visually-hidden')[0]
                            experience_title.append(item0.get_attribute('innerText'))
                            print(item0)
                        else:
                            experience_title.append('NULL')
                            
                        #TODO: if there are multiple sub experiences, it will return NULL, fix it
                        if item.find_elements_by_css_selector('.visually-hidden')[1]:
                            #company of the experience
                            item1 = item.find_elements_by_css_selector('.visually-hidden')[1]
                            experience_company.append(item1.get_attribute('innerText'))
                            print(item1)
                        else:
                            experience_company.append('NULL')
                            '''
                    break

    #create a new section_lists since there is a possibility that the page was reloaded from the previous code
    section_lists = driver.find_elements_by_css_selector('.artdeco-card.ember-view.relative.break-words.pb3.mt2 ')
    #EDUCATION
    for section in section_lists:
        if section.find_elements_by_id('education'):
            if section.find_elements_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid'):
                section.find_element_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid').click()
                time.sleep(6)
                #Scroll all the way down
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    #Scroll to bottom
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # Wait to load page
                    time.sleep(2)
                    # Calculate new scroll height and compare with last scroll height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                lists = driver.find_element_by_css_selector('.pvs-list ')
                parts = lists.find_elements_by_tag_name('li')
                for part in parts:
                    if part.find_elements_by_css_selector('.visually-hidden'):
                        p = part.find_elements_by_css_selector('.visually-hidden')
                        for part0 in p:
                            education_school.append(part0.get_attribute('innerText'))
                    else:
                        education_school.append('NULL')
                    '''
                    if part.find_elements_by_css_selector('.visually-hidden')[0]:
                        part0 = part.find_elements_by_css_selector('.visually-hidden')[0]
                        education_school.append(part0.get_attribute('innerText'))
                    else:
                        education_school.append('NULL')

                    if part.find_elements_by_css_selector('.visually-hidden')[1]:
                        part1 = part.find_elements_by_css_selector('.visually-hidden')[1]
                        education_subject.append(part1.get_attribute('innerText'))
                    else:
                        education_subject.append('NULL')
                        '''
                print("scrape educations from site")
                driver.execute_script("window.history.go(-1)")
                time.sleep(7)
                break
            else:
                #no show more button so just scrape what is already there
                print("scrape educations from profile")
                #check if there is a list is empty in this section
                if section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap'):
                    section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap')
                    items = section.find_elements_by_tag_name('li')
                    for item in items:
                        if item.find_elements_by_css_selector('.visually-hidden'):
                            i = item.find_elements_by_css_selector('.visually-hidden')
                            for item0 in i:
                                education_school.append(item0.get_attribute('innerText'))
                        else:
                            education_school.append('NULL')
                        '''
                        #check if the item exists
                        if item.find_elements_by_css_selector('.visually-hidden')[0]:
                            #title of the experience
                            item0 = item.find_elements_by_css_selector('.visually-hidden')[0]
                            education_school.append(item0.get_attribute('innerText'))
                        else:
                            education_school.append('NULL')

                        if item.find_elements_by_css_selector('.visually-hidden')[1]:
                            #company of the experience
                            item1 = item.find_elements_by_css_selector('.visually-hidden')[1]
                            education_subject.append(item1.get_attribute('innerText'))                       
                        else:
                            education_subject.append('NULL')
                            '''
                break

    section_lists = driver.find_elements_by_css_selector('.artdeco-card.ember-view.relative.break-words.pb3.mt2 ')
    #SKILLS
    for section in section_lists:
        if section.find_elements_by_id('skills'):
            if section.find_elements_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid'):
                section.find_element_by_css_selector('.optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--3.artdeco-button--muted.inline-flex.justify-center.full-width.align-items-center.artdeco-button--fluid').click()
                time.sleep(5)
                #Scroll all the way down
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    #Scroll to bottom
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    # Wait to load page
                    time.sleep(2)
                    # Calculate new scroll height and compare with last scroll height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                lists = driver.find_element_by_css_selector('.pvs-list ')
                #this part is different than the previous code because the tag name 'li' is not only used for the name of the skill but also the endorsement. So used locate by css_selector instead.
                parts = lists.find_elements_by_css_selector('.mr1.t-bold')
                for part in parts:
                    if part.find_element_by_css_selector('.visually-hidden'):
                        part0 = part.find_element_by_css_selector('.visually-hidden')
                        skills.append(part0.get_attribute('innerText'))
                    else:
                        skills.append('NULL')

                print("scrape skills from site")
                driver.execute_script("window.history.go(-1)")
                time.sleep(6)
                break
            else:
                #no show more button so just scrape what is already there
                print("scrape skills from profile")
                #check if the list is empty in this section
                if section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap'):
                    section.find_elements_by_css_selector('.pvs-list.ph5.display-flex.flex-row.flex-wrap')
                    items = section.find_elements_by_css_selector('.mr1.t-bold')
                    for item in items:
                        #check if the item exists
                        if item.find_element_by_css_selector('.visually-hidden'):
                            #title of the experience
                            item0 = item.find_element_by_css_selector('.visually-hidden')
                            skills.append(item0.get_attribute('innerText'))
                            print(item0)
                        else:
                            skills.append('NULL')
                break
    '''
    print(experience_title)
    print(experience_company)
    print(education_school)
    print(education_subject)
    print(skills)
    '''
    #BeautifulSoup part:
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    #first profile part (the box with the name,title, location and number of connections)
    name_path = soup.find('div', {'class': 'mt2 relative'})

    #name
    try:
        name = name_path.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
    except:
        name = 'NULL'

    #title
    try:
        title = name_path.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
    except:
        title = 'NULL'

    #about
    about_path = soup.find('div', {'class': 'display-flex ph5 pv3'})
    try:
        about = about_path.find('span', {'class': "visually-hidden"}).get_text().strip()
    except:
        about = 'NULL'

    '''
    print(name)
    print(title)
    print(about)
    '''
    #join experience_title array into a single string
    a = ' + '.join(str(x) for x in experience_title)
    #join education_school array into a single string
    b = ' + '.join(str(x) for x in education_school)
    #join skills array into a single string
    c = ' + '.join(str(x) for x in skills)

    save_csv_row = [profile, name, title, about, a, b, c]


    with open('C:/Users/Admin/source/repos/webcrawler-profile/' + company + '.csv', 'a', encoding='utf-8') as f:
        #create csv writer
        writer = csv.writer(f)
        writer.writerow(save_csv_row)
        f.close()