"""
Pour peupler les tables authors, articles, articles_sous_themes, authors_articles et affiliation_authors
"""
df=pd.read_csv("/users/2023/ds1/share/CORD-19/metadata.csv")

for i in range(100):
	print(f'title = {df["title"][i]}, abstract = {df["abstract"][i]}, url = {df["url"][i]} , publication_date= {df["publish_time"][i]}, journal = {df["journal"][i]}, authors = {df["authors"][i]}\n')


	
	

fichier=0
for element in elements1[:100]:
    with open(f'{chemin1}/{element}', 'r') as f:
        data = json.load(f)
        fichier+=1
        print("nombre de fichiers traités=",fichier)
        a=data['metadata']['authors']
    if len(a)!=0:
        for i in range(len(a)):
            first="".join(list(filter(str.isalpha,a[i]['first'] )))
            m="".join(a[i]['middle'])
            middle="".join(list(filter(str.isalpha,m )))
            suffix="".join(list(filter(str.isalpha,a[i]['suffix'] )))
            last="".join(list(filter(str.isalpha,a[i]['last'] )))
            email= a[i]['email']
            if first=='':
                name=last+', '+middle+suffix
            if last=='':
                name=first+' '+middle+suffix
            else:
                name=last+', '+first+' '+middle+suffix
            print(name)
