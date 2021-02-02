import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime
from pymongo import MongoClient 

url1 = 'https://timesofindia.indiatimes.com/news'
url2 = 'https://www.thehindu.com/news/'
url3 = 'https://www.thehindu.com/'
url4 = 'https://www.bbc.com'

page1 = requests.get(url1)
page2 = requests.get(url2)
page3 = requests.get(url3)
page4 = requests.get(url4)

news = []

soup1 = BeautifulSoup(page1.content, 'lxml')
soup2 = BeautifulSoup(page2.content, 'lxml')
soup3 = BeautifulSoup(page3.content, 'lxml')
soup4 = BeautifulSoup(page4.content, 'lxml')

headlines = soup1.find_all("span", class_="w_tle")
imgs = soup1.find_all("a", class_="w_img")
descriptions = soup1.find_all("span", class_="w_desc")
more = soup2.find_all("div", class_="story4-sub-cont")
thehindu_news = soup3.find_all("div", class_="story-card")
bbc_news = soup4.find_all("ul", class_="media-list--fixed-height")
        
id = 1

# fetch from Times of India
for line in headlines:
    link = ""
    for anchor in line:
        if anchor.get('href')[0:5] == "https":
            link = "{0}".format( anchor.get('href'))  
        else:
            link = "https://timesofindia.indiatimes.com{0}".format( anchor.get('href'))

    news_format = {
        # "Id" : str(id),
        "Img_src" : "https://static.toiimg.com/photo/34824568.cms",
        "Headline" : line.text,
        "Article_link" : link,
        "Category" : "",
        "Content" : "",
        "Source" : "Times Of India",
        "DateTime" : (datetime.now()).strftime("%H:%M")
    }
    id+=1
    news.append(news_format)


i=0
for img in imgs:
    for tag in img:
        if tag.get('data-src') is not None:
            news[i]['Img_src'] = tag.get('data-src')
            i+=1


i=len(headlines) - len(descriptions)
for desc in descriptions:
    news[i]['Content'] = desc.text
    i+=1

# fetch from The Hindu
for i in more:
    tmp1 = i.find_all("img")
    tmp2 = i.find_all("a") 

    for j in range(len(tmp1)):
        content = tmp1[j].get('alt')
        if (content=="Representational image"):
            content = ""
        if (content=="For representational purpose only."):
            content = ""
            
        news_format = {
            # "Id" : str(id),
            "Img_src" : tmp1[j].get('data-proxy-image'),
            "Headline" : tmp2[j].text.strip(),
            "Article_link" : tmp2[j].get('href'),
            "Category" : "",
            "Content" :  content,
            "Source" : "The Hindu",
            "DateTime" : (datetime.now()).strftime("%H:%M")
        }
        id+=1
        news.append(news_format)

for i in thehindu_news:
    tmp1 = i.find_all("img")
    tmp2 = i.find_all("h2")

    for j in range(len(tmp2)):
        content = tmp1[j].get('alt')
        if (content=="Representational image"):
            content = ""
        if (content=="For representational purpose only."):
            content = ""

        news_format = {
            # "Id" : str(id),
            "Img_src" : tmp1[j].get('data-src-template'),
            "Headline" : tmp2[j].text.strip(),
            "Article_link" : tmp2[j].find("a").get('href'),
            "Category" : "",
            "Content" :  content,
            "Source" : "The Hindu",
            "DateTime" : (datetime.now()).strftime("%H:%M")
        }
        id+=1
        news.append(news_format)

# fetch from bbc news
for i in range(4):
    w = bbc_news[i].find_all("p", class_="media__summary")
    x = bbc_news[i].find_all("h3", class_="media__title")
    y = bbc_news[i].find_all("div", class_="delayed-image-load")
    z = bbc_news[i].find_all("a", class_="media__link")

    for j in range(len(x)):

        news_format = {
            # "Id" : str(id),
            "Img_src" : str(y[j].get('data-src')).replace("{width}","300"),
            "Headline" : x[j].text.strip(),
            "Article_link" : url4 + z[j].get('href'),
            "Category" : "",
            "Content" :  w[j].text.strip(),
            "Source" : "BBC News",
            "DateTime" : (datetime.now()).strftime("%H:%M")
        }
        id+=1
        news.append(news_format)

# create json file of the news
news_file = open('latest_news/news.json','w+')
print(json.dumps(news, indent=4), file=news_file)
news_file.close()

# insert data in database
try: 
	conn = MongoClient() 
	print("Connected successfully!!!") 
except: 
	print("Could not connect to MongoDB") 

client = MongoClient("mongodb://localhost:27017/") 

web_scraper = client['web_scraper']

db = conn.web_scraper

collection = db.news_table 

for i in news:
    x = collection.find_one({'Headline' : i['Headline']})
    if x is None:
        collection.insert_one( i )