import pandas as pd
from utils import get_urls, get_jobs


## CREER LE DATAFRAME DES ENTREPRISES
# company_list_df = pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/liste_initiale.csv', sep=';')
# url_df=get_urls(company_list_df[:5]) # récupérer les urls web et linkedin des entreprises
# url_df.to_csv('data/test_links/csv')

# RECUPERER LES OFFRES D'EMPLOI
keyword='data' # instancier le mot clé à chercher dans les offres

url_list=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', sep=',')

get_jobs(url_list.iloc[:1], keyword) # récupérer les offres sur linkedin dans new_job_offers.csv
