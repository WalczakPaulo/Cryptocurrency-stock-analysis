import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.insert(0, '../RssFeedModule')
from constants import HISTORIC_FEED_FILENAME

print(HISTORIC_FEED_FILENAME)
df = pd.read_csv('../RssFeedModule/' + HISTORIC_FEED_FILENAME,  error_bad_lines=False, parse_dates=['date'])
dates = df['date']
dates.groupby([df['date'].dt.year, df['date'].dt.month]).count().plot(kind="bar")
plt.title('Dates distribution')
plt.show()