import os
import pandas as pd
from datetime import datetime, timedelta
from tqdm import tqdm


data_file = 'features_60S_1.csv'
df = pd.read_csv(data_file)

root_dir = 'data1'
files = os.listdir(root_dir)
for file in tqdm(files):
    print(file)
    file_path = os.path.join(root_dir, file)
    symbol, dt = file.replace('.csv', '').split('_')

    # flag 1
    # dt = datetime.strptime(dt, '%Y-%m-%d %H.%M').strftime('%Y-%m-%d %H:%M:%S')
    # print(symbol, dt)
    # df.loc[(df['symbol'] == symbol) & (df['date'] == dt), 'gt'] = 1

    # flag 2
    tmp_df = pd.read_csv(file_path)
    tmp_df['datetime'] = pd.to_datetime(tmp_df['datetime'])

    # Aggregate buying and selling to the minute level
    tmp_df['time'] = tmp_df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M:00'))
    agg = tmp_df.groupby(by=['time'], as_index=False)['btc_volume'].sum()

    mean = agg['btc_volume'].mean()
    std = agg['btc_volume'].std()
    threshold = mean + 3 * std

    # Filter out the time corresponding to abnormal trading volume of 'agg', then filter out the data in 'features' that match the symbol and abnormal trading time, and label it as 1
    df.loc[(df['symbol'] == symbol) & (df['date'].isin(agg.loc[agg['btc_volume'] > threshold]['time'])), 'gt'] = 1

    df.to_csv('features_60S_mark2.csv', index=False)
