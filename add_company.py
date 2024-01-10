from annotated_types import LowerCase
import pandas as pd
from utils import add_company, get_jobs

add_company()

answer = input('Do you wish to launch a new search? (y/n) :')

if answer.lower() == 'y' or answer.lower() == 'yes':
    keyword = 'data'
    df=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', sep=';')
    get_jobs(df, keyword)

else:
    answer2=input('Do you wish to launch a search just for this company ? (y/n) :')
    if answer2.lower() == 'y' or answer2.lower() == 'yes':
        keyword = 'data'
        df=pd.read_csv('/home/clem7991/code/Clement7991/local_job_newsletter/data/company_urls.csv', sep=';')
        get_jobs(df.iloc[-1:], keyword)

    else :
        print('The company has been added to the list.')
