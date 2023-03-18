"""
Pour peupler les tables authors, articles, articles_sous_themes, authors_articles et affiliation_authors
"""
df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")

for i in range(100):
	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} , publication_date= {df["publish_time"][i]}, journal = {df["journal"][i]}, authors = {df["authors"][i]}\n')
