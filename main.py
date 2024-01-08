import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys

from utils import get_urls, get_jobs

# instantier le dataframe des entreprises
# company_list_df = pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/liste_initiale.csv', sep=';')

# url_df=get_urls(company_list_df[:5]) # récupérer les urls web et linkedin des entreprises

# url_df.to_csv('data/test_links/csv')

keyword='data' # instancier le mot clé à chercher dans les offres

url_list=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', sep=',')

get_jobs(url_list[119:131], keyword) # récupérer les offres sur linkedin dans new_job_offers.csv
