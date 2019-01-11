import argparse
import pandas as pd
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument(
      '--path_to_prices',
      help='Local path to Bitcoin\'s price history',
      default='../BitcoinPriceCrawler/data/BitcoinPrice_from_2013-06-18_to_2019-01-02.csv',
)
parser.add_argument(
      '--path_to_messages',
      help='Local path to messages',
      default='../RssFeedModule/data/historicNews.csv',
)
parser.add_argument(
    '--save_to',
    help='Path to folder where we want to save file with its name',
    default='./data/ProcessedData.csv'
)
parser.add_argument(
    '--threshold',
    help='The absolute value of the percentage change for which we assume that it is significant',
    default=0
)
args = parser.parse_args()
arguments = args.__dict__
path_to_prices = arguments['path_to_prices']
save_to = arguments['save_to']
threshold = arguments['threshold']
path_to_messages = arguments['path_to_messages']

prices = pd.read_csv(path_to_prices)
price_diffs = 100*(prices['price'].diff()[1:].reset_index(drop=True) / prices['price'][:-1].reset_index(drop=True))
categories = price_diffs.map(lambda diff: 0 if (diff <= -threshold) else (1 if (diff >= threshold) else 2))
prices.drop(['price'], axis=1, inplace=True)
prices = prices[:-1]
prices['class'] = categories
prices['messages'] = np.nan

messages = pd.read_csv(path_to_messages, parse_dates=['date'])
messages['title_and_description'] = messages[['title', 'description']].apply(lambda x: ' '.join(x), axis=1)
grouped_messages = messages.groupby([pd.to_datetime(messages['date'])])['title_and_description'].apply(lambda x: ' '.join(x))
indexes = grouped_messages.index.values

pd.options.mode.chained_assignment = None
for i in range(len(prices)):
    date = np.datetime64(prices['date'][i])
    if date in indexes:
        prices['messages'][i] = grouped_messages[date]

prices.dropna(inplace=True)
prices.to_csv(save_to, sep=',', encoding='utf-8', index=False)