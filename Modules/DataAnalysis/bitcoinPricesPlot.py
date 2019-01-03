import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv('../BitcoinPriceCrawler/data/BitcoinPrice_from_2013-06-18_to_2019-01-02.csv', parse_dates=['date'])
df.plot(x='date', y='price', kind='line', grid=True)
plt.title('Bitcoin price')
plt.show()