import pandas as pd

name=[]
site=[]
lk=[]
company_name=input('Company name: ')
site_url=input('Company website url: ')
lk_url=input('Company LinkedIn url: ')

name.append(company_name)
site.append(site_url)
lk.append(lk_url)


tmp=pd.DataFrame({'Company':name, 'URL': site, 'Linkedin': lk})

df=pd.read_csv('data/company_urls.csv', sep=',')

df.drop(df.columns[0], axis=1, inplace=True)

updated_df=pd.concat([df, tmp], ignore_index=True)

updated_df.to_csv('data/company_urls.csv', sep=',')

print("company added to list. See below...")
print(updated_df.tail(3))
