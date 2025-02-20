import ccxt
from ccxt.base.errors import RequestTimeout
import pandas as pd
from datetime import datetime
from datetime import timedelta
import time

binance = ccxt.binance({'proxies': {'http': '127.0.0.1:33210', 'https': '127.0.0.1:33210' }})


def to_timestamp(dt):
    return binance.parse8601(dt.isoformat())


def download(symbol, start, end):
    
    records = []
    since = start
    ten_minutes = 60000 * 10

    print('Downloading {} from {} to {}'.format(symbol, binance.iso8601(start), binance.iso8601(end)))

    while since < end:

        try:
            orders = binance.fetch_trades(symbol + '/BTC', since)
        except RequestTimeout:
            time.sleep(5)
            orders = binance.fetch_trades(symbol + '/BTC', since)

        if len(orders) > 0:

            latest_ts = orders[-1]['timestamp']
            if since != latest_ts:
                since = latest_ts
            else:
                since += ten_minutes

            for l in orders:
                records.append({
                    'symbol': l['symbol'],
                    'timestamp': l['timestamp'],
                    'datetime': l['datetime'],
                    'side': l['side'],
                    'price': l['price'],
                    'amount': l['amount'],
                    'btc_volume': float(l['price']) * float(l['amount']),
                })
        else:
            since += ten_minutes

    return pd.DataFrame.from_records(records)


def download_binance(days_before=1, days_after=1):
   
    df = pd.read_csv('result2.csv')
    binance_only = df[df['exchange'] == 'binance']

    for i, pump in binance_only.iterrows():
        symbol = pump['symbol']
        date = pump['date'] + ' ' + pump['hour']
        pump_time = datetime.strptime(date, "%Y-%m-%d %H:%M")
        before = to_timestamp(pump_time - timedelta(days=days_before))
        after = to_timestamp(pump_time + timedelta(days=days_after))
        
        import os
        
        if os.path.exists('data1/{}_{}'.format(symbol, str(date).replace(':', '.') + '.csv')):
            print(symbol)
            continue
        
        df = download(symbol, before, after)
        df.to_csv('data1/{}_{}'.format(symbol, str(date).replace(':', '.') + '.csv'), index=False)

if __name__ == '__main__':
    download_binance(days_before=1, days_after=0)
