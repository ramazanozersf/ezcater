# From Web Site Scraping to Business Intelligence

Help the business make better decisions through scraped data from website

**General structure of the project is analysis and interpretation of complex digital data to extract or discover knowledge and assist decision-making. So I scraped datas from a website that I think it will be important for companies which is related food industry in the US and then transform it for business analytics.**


Firstly I must determine that this process is an academic study and there is no any commercial purpose.

With that project we could observe the frequency of order of caterers in the city and at the same time we could see how these caterers are distributed in the city.


#### That is which information we need.

#Import library
from IPython.display import Image

# Load image from local storage
Image(filename = "/Users/ramazanozer/Desktop/1_YKIWG5Py8pytuYXdjq0RGA.png")

**Here is ; Name of caterers, Minimum price of one order, last order, address of caterers and which day are they have open for deliveries.**

**Firstly we will scrape name, minimum price and link of caterers .**

import requests

from bs4 import BeautifulSoup

import pandas as pd

import numpy as np

page=1

links=[]

name=[]

minprice=[]

while page<=16:

url="https://www.ezcater.com/store/caterer_search/105089251?page%5Bnumber%5D=" + str(page)
    r = requests.get(url)
    html_icerigi = r.content
    soup = BeautifulSoup(html_icerigi,"html.parser")
    """--------------------------------------------------------"""
    #LINKS    
    a=soup.find_all("a",{"class":"caterer-show-link"})
    for b in a:
        linkler.append(b.get("href"))
    """--------------------------------------------------------"""
    #NAMES
    linc=soup.find_all(class_="search-result-title")
    for i in linc:
        name.append(i.text)
    """--------------------------------------------------------"""
    #MINIMUM-$
    linc2=soup.find_all(class_="delivery-detail")
    for i in linc2:
        minprice.append(i.text)
    
    page+=1

**For now we get names, prices and also links of caterers with codes.**

**Now we have an irregular data that is minimum price. When we scraped data is like that ‘ $ 50 Minimum ’, ‘ $ 200 Minimum ’. That is a categorical variable we must return that to numerical variable.**


#these codes is continuous of upper codes.

minorder=[]

for i in minprice:

    if i.endswith("mum"):
    
        minorder.append(i)
        
minprice=[]

for i in minorder:

    i=i.strip("Minimum")
    
    i=i.strip("$")
    
    minprice.append(i)
    
"""--------------------------------------------------------"""

v=str(linkler)

with open("linkler.txt", "w") as folder:

    for i in v:
    
        folder.write(i)
        
"""--------------------------------------------------------"""  

df=pd.DataFrame({

    "NAME":isimler,
    
    "MINIMUM-$":minprice
    
})

df.to_excel("atlanta.xlsx", index=False)

**We got links with that scraping. Keep it for now for another scraping. We have the caterers names and minimum prices in the excel file.**

**Now we will go in each of the links we have taken and then we will take the address and which hours and days it is open. At the same time, we will take the coordinates of the addresses by geocoding to show the addresses on the map.**


import requests

from bs4 import BeautifulSoup

import urllib

import geopy

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="cityandregionalplanning")

import pandas as pd

import numpy as np

links=['/catering/baja-fresh-mexican-grill-atlanta', 
'/catering/vegan-vibez-riverdale?page%5Bnumber%5D=6',..... ]

address=[]

delivery=[]

kordinatlar=[]

for i in links:

    url = "https://www.ezcater.com"+ str(i)
    
    request = urllib.request.Request(url)
    
    request.add_header('User-Agent',"Aslan")
    
    data = urllib.request.urlopen(request).read()
    
    soup = BeautifulSoup(data,"html.parser")
    
    al=soup.find("div",{"class":"caterer-header__location inline-    dropdown-container"})
    
    c=al.find("span").string
    
    address.append(c)
    
    try:
    
        a=geolocator.geocode(c)
        
        if a == None:
        
            kordinatlar.append(None)
            
        else:
        
            kordinatlar.append((a.latitude, a.longitude))
            
    except:
    
        kordinatlar.append("fail, do it again")
        
    al2=soup.find_all("div",{"class":"caterer-about-section"})[1]
    
    for c in al2:
    
        delivery.append((c.text))

**I added urlllib library along with the Beautifulsoup and request libraries. I was unable to access the page by request, so that I accessed it with the urllib library. I made geocoding with the geopy library to convert address to coordinate. ( not: geopy library works with the openstreetmap api and it does not convert more than 100 addresses to coordinate per day .).**


**When I scraped the data of which day caterers open, we see a text like this; ‘Delivery Hours’, ‘Mon-Fri: 6am-7pm’. In order to fix this, we run the code below and get the time that we need;**

deliveries=[]

for i in delivery:

    if (i=='Delivery Hours'):
    
        pass
        
    else:
    
        deliveries.append(i[:7])

**After dealing with these, let’s export all of our edited data.**

df=pd.DataFrame({
    
    "DEliveries":deliveries,
    
    "Coordinates":kordinatlar,
    
    "Address":"address"
    
})

df.to_excel("atlanta1.xlsx", index=False)

**When I took the data, I bought it separately because the caterers name, minimum price and address information are fixed but last order information is changing continuously.**

**Let’s run the following code to get the last order information.**

import requests

from bs4 import BeautifulSoup  

"""-------------------------------------------------------------"""

page=1

lastorderss=[]

name=[]

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
    
        name.append(i.text)
    
    page+=1

**With these codes, the data I have is something like this. : “Last order: about 3 hours ago”, “Last order: 22 minutes ago”, “Last order: 2 days ago”, “Last order: January 27”, “Last order: January 5”. This variables is useless so we must return that to numerical variable.**

**At first we will get rid of “last order:”**


p=[]

for i in lastorderss:

    i=str(i)
    
    if i.startswith("Last order:"):
    
        i=i.strip("Last order:")
        
        p.append(i)
        
    else:
    
        p.append('\xa0')

**And then we will return these dates to day. For that I prepare this algorithm.**

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

**And here are we have just numerical variables as day.**

**We have finished scraping website and also regulation of data. The next is visualization of these data to make some analytics.**

-----------------------

**Now, by doing some analytical studies with these data, we will see with which features the caterers are distributed in the city.**

**The flow of the study proceeded with an organization as follows.**

# Load image from local storage
Image(filename = "/Users/ramazanozer/Desktop/1_Uvt7ReowoNqux_f7-Y50MQ.png")

**We will make a general comparison of the cities. Cities with more caterers usually expect to be higher in this market. In the barchart and list there is a direct proportion between the number of caterers and the number of active kitchens. But there may be a few exceptions. Let’s look at Austin, for example. Here, the number of active kitchens is quite high when we compared to the number of kitchens. If I were an investor, instead of Philadelphia, Houston, Brooklyn I would make invest to Austin, because there are more active kitchens in Austin. In this way, we can notice that such situations are observed in some other cities.**

# Load image from local storage
Image(filename = "/Users/ramazanozer/Desktop/1_WNaMMN-2eeRc6FW5J_pXNg.png")

**We can see in which states and cities this market has developed. California and New York markets has more developed.**

# Load image from local storage
Image(filename = "/Users/ramazanozer/Desktop/1_njsytcgmutWtT9CD256V7Q.png")

Here we take the example of the Boston city. Analytics contain;

Distribution of caterers in the city.

Frequency of orders, that is in how many day the caterers take one order. By determining a certain grid area, and then I determined the colors of the square by consider the average and the standard deviation of orders.

Traffic Situation of the city, this traffic flow is showed most heavy traffic hours(9am-13am). 

According to that we can determine that which caterers located on heavy traffic lines.

Status of caterers (well, good, medium,bad, inactive)

Scale of minmum price of order.

Between which days are caterers open.

# Load image from local storage
Image(filename = "/Users/ramazanozer/Desktop/1_SyDFTTrgLE9iNCe_J0lXgA.png")

Companies interested in food marketing can develop many strategies and improve their business based on this analytical study.

If we make some inferences based on these analytics;

In which city you could invest in marketing of catering?

If there will be an investmen, in which part of the city should be invested?

Real estate valuation can realised easily according to the distribution of dense of caterers or activity of the caterers.

Food service companies can optimize their route according to these maps. And also it can revise the organization plan to be close to the most active caterers area.

According to these analytics, companies that are concerned with food can make the best decision in choosing a place in the city.

Any company that wants to serve food online can make a good start based on these analytics.
