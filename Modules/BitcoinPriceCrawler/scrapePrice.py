import requests
import sys
import json
import datetime
import csv
from constMessages \
    import WELCOME_INFO, BASE_URL, DATE_PERIOD_BASE_URL, INCORRECT_NUMBER_OF_ARGS, ERROR_API, SUCCESSFUL_API

def argsSize():
    return len(sys.argv)

print(WELCOME_INFO)

url = ''
if argsSize() == 1:
    url = BASE_URL
elif argsSize() == 3:
    url = DATE_PERIOD_BASE_URL + sys.argv[1] + '&end=' + sys.argv[2]
else:
    print(INCORRECT_NUMBER_OF_ARGS)

response = requests.get(url)
if response.status_code != 200:
    print(ERROR_API)
else:
    print(SUCCESSFUL_API)
    filename = ''
    if argsSize() == 1:
        filename = './data/BitcoinPrice' + datetime.datetime.now().strftime('%m-%d-%Y') + '.csv'
    else:
        filename = './data/BitcoinPrice_from_' + sys.argv[1] + '_to_' + sys.argv[2] + '.csv'
    myJson = json.loads(response.text)
    with open(filename, 'w') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['date', 'price'])
        if argsSize() == 1:
            filewriter.writerow([myJson['time']['updatedISO'][0:10], myJson['bpi']['USD']['rate_float']])
        elif argsSize() == 3:
            priceList = myJson['bpi']
            for item in sorted(priceList.items()):
                filewriter.writerow([item[0], item[1]])
        print('Data saved to: ' + filename)