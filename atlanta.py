import requests
from bs4 import BeautifulSoup   
"""-------------------------------------------------------------"""
page=1
lastorderss=[]
titles=[]
while page<=16:

    newurl="https://www.ezcater.com/store/caterer_search/105089251?page%5Bnumber%5D=" + str(page)

    r = requests.get(newurl)
    html_icerigi = r.content
    soup = BeautifulSoup(html_icerigi, "html.parser")
    lastorders=soup.find_all(class_="search-result-message")

    for i in lastorders:
        lastorderss.append(i.text)
        
    title=soup.find_all(class_="search-result-title")
    for i in title:
        titles.append(i.text)
    
    page+=1

p=[]
for i in lastorderss:
    i=str(i)
    if i.startswith("Last order:"):
        i=i.strip("Last order:")
        p.append(i)
    else:
        p.append('\xa0')
        
"""-------------------------------------------------------------"""
#names
v=str(titles)
with open("name9.txt", "w") as folder:
    for i in v:
        folder.write(i)

"""-------------------------------------------------------------"""

#last-orders
x=[]
a=7
for i in p:
    if i.find("minu")!=-1 :
        i="1"
        x.append(int(i))
        
    elif len(i)==14:
        i=i[5]
        x.append(int(i))
    elif len(i)==15:
        i=i[5]
        x.append(int(i))
    elif len(i)==16:
        i=i[5] + i[6]
        x.append(int(i))
        
    elif len(i)==9 and not i.startswith("August"):
        i=i[0] + i[1]
        x.append(int(int(i)*24))
    elif len(i)==8 and not i.startswith("August"):
        i=i[0]
        x.append(int(int(i)*24))
        
    elif i.startswith("September"):
        
        if len(i)==11:
            f=abs(int(i[10])- a)*24
            x.append(int(f))
        else:
            f=abs(int(i[10]+i[11])- a)*24
            x.append(int(f))
            
    elif i.startswith("August"):
        if len(i)==8:
            f=abs((31 - int(i[7]))+ a)*24
            x.append(int(f))
        else:
            f=abs((31- int(i[7]+i[8]))+ a)*24
            x.append(int(f))
    elif (i=="nan"):
        i=i.replace('nan', '\xa0')
        x.append(i)
    else:
        x.append(i)
y=[]
for i in x:
    if i=="\xa0":
        y.append(i)
    elif i<24:
        y.append(1)
    else:
        y.append(int(i/24))
        
v=str(y)
with open("lasorders9.txt", "w") as folder:
    for i in v:
        folder.write(i)
