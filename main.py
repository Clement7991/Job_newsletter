import pandas as pd

from utils import get_urls
from utils_copy import get_jobs

# instantier le dataframe des entreprises
# company_list_df = pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/liste_initiale.csv', sep=';')

# url_df=get_urls(company_list_df[:5]) # récupérer les urls web et linkedin des entreprises

# url_df.to_csv('data/test_links/csv')

keyword='data' # instancier le mot clé à chercher dans les offres

url_list=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', sep=',')

get_jobs(url_list[30:], keyword) # récupérer les offres sur linkedin dans new_job_offers.csv


# Repackager le code pour qu'à chaque entreprise, un dataframe soit créé puis ajouté
# à un dataframe global. Permettra de ne pas perdre les données si le code plante

# Trier les offres par date de publication contenant hour/day (exclure week et month?)"
