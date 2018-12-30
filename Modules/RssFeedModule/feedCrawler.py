import requests
import sys
from bs4 import BeautifulSoup
from constants import \
    ERROR, COIN_TELEGRAPH_URL, LATEST_NEWS_FILENAME, TO_BE_PROCESSED_NEWS, WELCOME_INFO, \
    HISTORIC_FEED_URL, INCORRECT_ARGUMENT, HISTORIC_FEED_FILENAME, WELCOME_INFO_HISTORIC
from email.utils import parsedate_tz
import csv
import pandas as pd
import re

if len(sys.argv) != 2:
    print(ERROR)
    exit()

crawlerType = sys.argv[1]
url = ''
filename = ''
newNewsFilename = ''
if crawlerType == 'historic':
    url = HISTORIC_FEED_URL
    filename = HISTORIC_FEED_FILENAME
    print(WELCOME_INFO_HISTORIC)
elif crawlerType == 'current':
    url = COIN_TELEGRAPH_URL
    filename = LATEST_NEWS_FILENAME
    newNewsFilename = TO_BE_PROCESSED_NEWS
    print(WELCOME_INFO)
else:
    print(INCORRECT_ARGUMENT)
    exit()

resp = requests.get(url)
soup = BeautifulSoup(resp.content, features='xml')
items = soup.findAll('item')
news_items = []
cleanr = re.compile('<.*?>')

for item in items:
    news_item = {}
    news_item['title'] = '\"' + item.title.text + '\"'
    description = item.description.text.replace('\'', '')
    cleantext = re.sub(cleanr, '', description).replace('"', '').replace('\n', ' ')
    news_item['description'] = '\"' + cleantext + '\"'
    date = parsedate_tz(item.pubDate.text)
    month = ''
    day = ''
    if date[1] < 10:
        month = '0' + str(date[1])
    else:
        month = str(date[1])
    if date[2] < 10:
        day = '0' + str(date[2])
    else:
        day = str(date[2])
    news_item['pubDate'] = str(date[0]) + '-' + month + '-' + day
    news_items.append(news_item)

titles = []
try:
    dataFilename = ''
    if(crawlerType == 'current'):
        dataFilename = LATEST_NEWS_FILENAME
    else:
        dataFilename = HISTORIC_FEED_FILENAME
    csvfile = pd.read_csv(dataFilename,  error_bad_lines=False)
    titles = csvfile['title'].tolist()
except:
    pass

to_be_processed_news = []
with open(filename, 'a') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    if len(titles) == 0:
        filewriter.writerow(['date', 'title', 'description'])
    for item in news_items:
        if len(titles) == 0 or item['title'] not in titles:
            filewriter.writerow([item['pubDate'], item['title'], item['description']])
            to_be_processed_news.append(item)

if crawlerType == 'historic':
    exit()

with open(newNewsFilename, 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',')
    filewriter.writerow(['date', 'title', 'description'])
    for item in to_be_processed_news:
        filewriter.writerow([item['pubDate'], item['title'], item['description']])







