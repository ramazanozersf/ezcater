import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

page=1
linkler=[]
isimler=[]
minprice=[]
while page<=16:

    url="https://www.ezcater.com/store/caterer_search/105089251?page%5Bnumber%5D=" + str(page)
    r = requests.get(url)
    html_icerigi = r.content
    soup = BeautifulSoup(html_icerigi,"html.parser")
    

    """-------------------------------------------------------------------------"""
    a=soup.find_all("a",{"class":"caterer-show-link"})
    for b in a:
        linkler.append(b.get("href"))
    """-------------------------------------------------------------------------"""
    #TITLE
    linc=soup.find_all(class_="search-result-title")
    for i in linc:
        isimler.append(i.text)
    """-------------------------------------------------------------------------"""
    #MINIMUM-$
    linc2=soup.find_all(class_="delivery-detail")
    for i in linc2:
        minprice.append(i.text)
    
    page+=1
    """-------------------------------------------------------------------------"""

minorder=[]
for i in minprice:
    if i.endswith("mum"):
        minorder.append(i)
minprice=[]
for i in minorder:
    i=i.strip("Minimum")
    i=i.strip("$")
    minprice.append(i)
"""-------------------------------------------------------------------------"""
v=str(linkler)
with open("linkler.txt", "w") as folder:
    for i in v:
        folder.write(i)
"""-------------------------------------------------------------------------"""        
df=pd.DataFrame({
    "NAME":isimler,
    "MINIMUM-$":minprice
})


df.to_excel("atlanta.xlsx", index=False)


"""-------------------------------------------------------------------------"""







