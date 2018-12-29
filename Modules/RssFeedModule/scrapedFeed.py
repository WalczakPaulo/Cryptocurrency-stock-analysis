import requests
from bs4 import BeautifulSoup
from constants import COIN_TELEGRAPH_URL, LATEST_NEWS_FILENAME
from email.utils import parsedate_tz
import csv
import pandas as pd
url = COIN_TELEGRAPH_URL
resp = requests.get(url)
soup = BeautifulSoup(resp.content, features='xml')
items = soup.findAll('item')
news_items = []

for item in items:
    news_item = {}
    news_item['title'] = item.title.text
    news_item['description'] = item.description.text
    news_item['link'] = item.link.text
    news_item['image'] = item.content['url']
    date = parsedate_tz(item.pubDate.text)
    news_item['pubDate'] = str(date[0]) + '-' + str(date[1]) + '-' + str(date[2])
    news_items.append(news_item)

latestNewsCsv = pd.read_csv(LATEST_NEWS_FILENAME,  error_bad_lines=False)
titles = latestNewsCsv['title'].tolist()

with open(LATEST_NEWS_FILENAME, 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    if 'title' not in titles:
        filewriter.writerow(['date', 'title', 'description'])
    for item in news_items:
        if(item['title'] not in titles):
            filewriter.writerow([item['pubDate'], item['title'], item['description']])





