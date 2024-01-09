import pandas as pd

new_df=pd.read_csv('data/new_company_urls.csv')
new_df.rename(columns={'linkedin':'Linkedin'}, inplace=True)
old_df=pd.read_csv('data/company_urls.csv')
old_df.drop(columns=['Unnamed: 0'], inplace=True)

df=pd.concat([old_df, new_df], ignore_index=True)
df.drop_duplicates(subset=['URL'], inplace=True)
df.to_csv('data/company_urls_vf.csv')
