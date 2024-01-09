### IMPORTS LIBRAIRES ###

import pandas as pd

# Scraping
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from datetime import timedelta, date

# Récupérer les url web des sites des entreprises
def get_urls(df):
    ''' Prends un dataframe comprenant la liste d'entreprises en entrée et retourne
    un dataframe avec les url web et linkedin des entreprises '''

    # instantier le driver
    options = Options()
    options.add_experimental_option("detach", True)
    driver=webdriver.Chrome(options=options)
    driver.get('https://www.google.com/')

    # Passer la demande de cookies
    try:
        cookie_popup = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'S3BnEe')))

        # Assuming there is an "Refuse" button in the cookie consent pop-up
        refuse_button = cookie_popup.find_element(By.XPATH, '//*[@id="W0wltc"]/div')
        refuse_button.click()

    except Exception as e:
        print(f"Cookie consent popup not found or encountered an error: {str(e)}")

    # Récupérer les url web des entreprises
    url_list=[]
    for company in df['Company']:
        search_box = driver.find_element("name", "q")
        search_box.clear()
        search_box.send_keys(company)
        search_box.send_keys(Keys.RETURN)
        wait = WebDriverWait(driver, 30)
        wait.until(ec.visibility_of_element_located((By.XPATH, "//*[@id='result-stats']")))
        soup = BeautifulSoup(driver.page_source, 'html.parser', multi_valued_attributes=None)

        url=soup.find('a', jsname='UWckNb', href=True).get('href')
        url_list.append(url)

    # récupérer les liens linkedin des entreprises
    linkedin=[]
    for url in url_list:
        driver.get(url)
        driver.implicitly_wait(3)
        soup = BeautifulSoup(driver.page_source, 'html.parser', multi_valued_attributes=None)
        desired_link = soup.find(href=lambda href: 'linkedin.com/company/' in str(href))
        if desired_link != None:
            linkedin.append(desired_link.get('href'))
        else :
            linkedin.append('No linkedin found')

    # Rassembler les url web et linkedin dans un dataframe
    results=pd.DataFrame({'Company': df['Company'], 'URL': url_list, 'Linkedin': linkedin})

    results.to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', index=False)

    driver.close()
    return results


def get_jobs(linkedin_list, keywords : str = 'Data'):
    ''' Prend une liste de liens linkedin et des mots clefs en entrée et met à jour le fichier csv
    contenant les offres d'emploi postées aujourd'hui tout en sauvegardant les anciennes offres dans un
    nouveau fichier csv
    '''
    # Ajouter la requête jobs
    linkedin_series=linkedin_list['Linkedin']
    linkedin_list= linkedin_series.apply(lambda x: str(x)+'jobs/' if str(x).endswith('/') else str(x)+'/jobs/')

    # Sauvegarder les anciennes offres d'emploi
    old_df=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/new_job_offers.csv')
    yesterday = date.today() - timedelta(days=1)
    old_df['Date'] = yesterday

    old_job_offers=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/old_job_offers.csv')

    history_of_offers = pd.concat([old_df, old_job_offers], ignore_index=True)
    history_of_offers.drop_duplicates(inplace=True)
    history_of_offers.to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/history_job_offers.csv', index=False)

    # Vider le fichier new_job_offers.csv
    old_df.drop(old_df.index, inplace=True)
    old_df.to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/new_job_offers.csv', index=False)

    # Chercher les nouvelles offres d'emploi
    options = Options()
    driver=webdriver.Chrome(options=options)
    driver.get('https://www.google.com/')

    # passer la demande de cookies
    try:
        cookie_popup = WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.ID, 'S3BnEe'))
        )

        # Assuming there is an "Refuse" button in the cookie consent pop-up
        refuse_button = cookie_popup.find_element(By.XPATH, '//*[@id="W0wltc"]/div')
        refuse_button.click()

    except Exception as e:
        print(f"Cookie consent popup not found or encountered an error: {str(e)}")

    # s'authentifier sur linkedin
    driver.get('https://www.linkedin.com/')
    #Locating the email field on the Linkedin login page
    username = driver.find_element(By.XPATH, '//*[@id="session_key"]')
    #Entering in an email address
    username.send_keys('clement7991@hotmail.fr')
    #Locating the password field on the Linkedin login page
    password = driver.find_element(By.XPATH,'//*[@id="session_password"]')
    #Entering in a password
    pass_df=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/pass.csv', sep=';')
    password.send_keys(pass_df['pass'][0])
    #Locating the Login button on the Linkedin login page
    log_in_button= driver.find_element(By.XPATH,'//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')
    #Clicking on the Login button
    log_in_button.click()
    #Applying a delay for the web page to load
    driver.implicitly_wait(5)

    job_company=[]
    job_title=[]
    job_date=[]
    job_url=[]
    faulty_links=[]
    no_jobs=[]
    scraping_error=[]
    scraping_flaw=[]

    # se rendre sur chaque page linkedin et récupérer les offres d'emploi
    for url in linkedin_list:
        try :
            driver.get(url)
            driver.implicitly_wait(5)
        except :
            faulty_links.append(url)
            continue

        # no jobs posted
        if "There are no jobs right now." in driver.page_source:
            no_jobs.append(url)
            continue
        else :
            try :
                job_box = driver.find_element("css selector", "input.org-jobs-job-search-form-module__typeahead-input")
            except :
                faulty_links.append(url)
                continue

            job_box.send_keys(keywords)
            search_button=driver.find_element(By.XPATH, '//a[text()="Search"]')
            search_button.click()
            driver.switch_to.window(driver.window_handles[1])

            while True:
                old_height = driver.execute_script("return document.body.scrollHeight")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                driver.implicitly_wait(2)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == old_height:
                    break

            if "No matching jobs found." in driver.page_source:
                no_jobs.append(url)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                continue

            else :

                job_company=[]
                job_title=[]
                job_date=[]
                job_url=[]

                #close chat window to avoid date/time errors
                chat_window = driver.find_element(By.XPATH, '//*[@id="msg-overlay"]/div[1]/header/div[2]/button')
                try :
                    if driver.find_element(By.XPATH, '//*[@id="msg-overlay-list-bubble-search__search-typeahead-input"]') != None:
                        chat_window.click()
                        driver.implicitly_wait(2)
                except :
                    scraping_error.append(url)
                    scraping_flaw.append('Unable to locate element')
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                job_results=WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[1]/header/div[1]/small/div/span')))
                results=job_results.find_element(By.XPATH, '//*[@id="main"]/div/div[1]/header/div[1]/small/div/span')
                job_number=int(results.text.split(' ')[0])

                soup=BeautifulSoup(driver.page_source, 'html.parser', multi_valued_attributes=None)

                title_url=soup.find_all(class_='disabled ember-view job-card-container__link job-card-list__title')
                for jobs in list(title_url)[:job_number+1]:
                    # print(jobs.text.strip())
                    job_title.append(jobs.text.strip())
                    # print(jobs.get('href').strip())
                    job_url.append("https://www.linkedin.com/"+jobs.get('href').strip())

                companies=soup.find_all(class_='job-card-container__primary-description ')
                for company in list(companies)[:job_number+1]:
                    # print(company.string.strip())
                    job_company.append(company.string.strip())

                # Make sure it doesn't go to Recommendations
                dates=soup.find_all('time')
                for d in list(dates)[:job_number+1]:
                    # print(d.text.strip())
                    job_date.append(d.text.strip())

                try :
                    company_result_df=pd.DataFrame({'Company': job_company, 'Job_title': job_title, 'Date_published': job_date, 'Job_url': job_url})
                except ValueError :
                    scraping_error.append(url)
                    scraping_flaw.append('arrays of unequal length')
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                today_result_df=company_result_df[(company_result_df['Date_published'] == '1 day ago') | (company_result_df['Date_published'].str.contains('hour'))]

                jobs_df=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/new_job_offers.csv')

                new_jobs_df=pd.concat([jobs_df, today_result_df], ignore_index=True)

                new_jobs_df.to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/new_job_offers.csv', index=False)

                driver.close()
                driver.switch_to.window(driver.window_handles[0])

    pd.DataFrame({'Companies with no jobs': no_jobs}).to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/no_jobs_list.csv', index=False)

    pd.DataFrame({'Faulty links': faulty_links}).to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/faulty_links_list.csv', index=False)

    pd.DataFrame({'URLs': scraping_error, 'Error' : scraping_flaw}).to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/scraping_errors.csv', index=False)

    driver.close()

    print("*************************************")
    print("Done!")
    print(f"Number of jobs posted today = {len(pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/new_job_offers.csv'))}")
    print("*************************************")

def add_company():
    name=[]
    site=[]
    lk=[]

    company_name=input('Company name: ')
    name.append(company_name)

    site_url=input('Company website url: ')
    site.append(site_url)

    lk_url=input('Company LinkedIn url: ')
    lk.append(lk_url)


    tmp=pd.DataFrame({'Company':name, 'URL': site, 'Linkedin': lk})

    df=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', sep=',')

    df.drop(df.columns[0], axis=1, inplace=True)

    updated_df=pd.concat([df, tmp], ignore_index=True)

    updated_df.to_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', sep=',')
