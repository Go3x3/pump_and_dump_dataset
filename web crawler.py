import datetime
import pandas as pd
import requests

headers = {
    'cookie': '_gid=GA1.2.1468696955.1676523668; uid=c030e1b4-6fd8-43ea-9045-912c3aab8246; utoken=lHH0vUTZqH/Vh4QiooXHT8AES6dhmY+yu/B8jbjsCdY=; _ga=GA1.1.1971064938.1676523668; _ga_95K58XEK0N=GS1.1.1676523667.1.1.1676523959.0.0.0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
}
res = requests.get('https://pumpolymp.com/api/allPumps', headers=headers).json()

result_list = []
for row in res:
    result = {}
    result['Channel'] = str(row['channelTitle'])
    result['currency'] = str(row['currency'])
    result['exchange'] = str(row['exchange'])
    result['duration'] = str(row['duration'])
    result['volume'] = str(row['volume'])
    result['priceBeforePump'] = str(row['priceBeforePump'])
    result['max'] = str(row['max'])
    result['ourBuyPrice'] = str(row['ourBuyPrice'])
    result['ourProfit'] = str(row['ourProfit'])
    result['theoreticalBuyPrice'] = str(row['theoreticalBuyPrice'])
    result['theoreticalProfit'] = str(row['theoreticalProfit'])
    result['date'] = str(datetime.datetime.strftime(datetime.datetime.strptime(row['signalTime'].replace('T', ' ')[:19], '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=-8), '%Y-%m-%d %H:%M:%S'))
    time=str(datetime.datetime.strftime(datetime.datetime.strptime(row['signalTime'].replace('T', ' ')[:19], '%Y-%m-%d %H:%M:%S') - datetime.timedelta(hours=0), '%Y-%m-%d %H:%M:%S'))
    if 20210601<=int(time.split(' ')[0].replace('-',''))<=20220920:
        print(result)
        result_list.append(result)

df = pd.DataFrame(result_list)
df.to_csv('result1.csv', encoding='utf8', index=False)
