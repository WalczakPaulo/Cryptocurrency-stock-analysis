import requests
from bs4 import BeautifulSoup
from constants import COIN_TELEGRAPH_URL, LATEST_NEWS_FILENAME, TO_BE_PROCESSED_NEWS
from email.utils import parsedate_tz
import csv
import pandas as pd
import re

url = COIN_TELEGRAPH_URL
resp = requests.get(url)
soup = BeautifulSoup(resp.content, features='xml')
items = soup.findAll('item')
news_items = []
cleanr = re.compile('<.*?>')

for item in items:
    news_item = {}
    news_item['title'] = item.title.text
    description = item.description.text
    cleantext = re.sub(cleanr, '', description).replace('"', '')
    news_item['description'] = cleantext
    news_item['link'] = item.link.text
    news_item['image'] = item.content['url']
    date = parsedate_tz(item.pubDate.text)
    news_item['pubDate'] = str(date[0]) + '-' + str(date[1]) + '-' + str(date[2])
    news_items.append(news_item)

titles = []
try:
    latestNewsCsv = pd.read_csv(LATEST_NEWS_FILENAME,  error_bad_lines=False)
    titles = latestNewsCsv['title'].tolist()
except:
    pass
print(len(titles))
to_be_processed_news = []
with open(LATEST_NEWS_FILENAME, 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if len(titles) == 0:
        filewriter.writerow(['date', 'title', 'description'])
    for item in news_items:
        if len(titles) == 0 or item['title'] not in titles:
            filewriter.writerow([item['pubDate'], item['title'], item['description']])
            to_be_processed_news.append(item)

with open(TO_BE_PROCESSED_NEWS, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['date', 'title', 'description'])
    for item in to_be_processed_news:
        filewriter.writerow([item['pubDate'], item['title'], item['description']])







