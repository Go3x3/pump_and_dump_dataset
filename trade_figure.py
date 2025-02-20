import os
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import tqdm


out = 'figure/'
if not os.path.exists(out):
    os.mkdir(out)

root_dir = 'data1'
files = os.listdir(root_dir)
for file in tqdm(files):
    print(file)
    fp = os.path.join(root_dir, file)
    df = pd.read_csv(fp)
    df['datetime'] = pd.to_datetime(df['datetime'])
    # df['time'] = df['datetime'].apply(lambda x: x.strftime('%d-%H'))
    df['side_marker'] = df['side'].apply(lambda x: 1 if x == 'buy' else -1)
    df['btc_volume'] = df['btc_volume'] * df['side_marker']

    # 分买卖聚合到秒级
    df['time'] = df['datetime'].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
    agg = df.groupby(by=['time', 'side'], as_index=False)['btc_volume'].sum()
    agg['time'] = pd.to_datetime(agg['time'])
    agg['time'] = agg['time'].apply(lambda x: x.strftime('%d-%H'))

    # print(agg.head())
    print(agg.shape)
    # agg.to_csv(file, index=False)

    mean = agg['btc_volume'].mean()
    std = agg['btc_volume'].std()
    threshold = mean + 3 * std

    x = []
    times = []
    x_normal = []
    normal = []
    x_abnormal = []
    abnormal = []
    for i in range(agg.shape[0]):
        t = agg.iloc[i]['time']
        volume = agg.iloc[i]['btc_volume']
        if t not in times:
            x.append(i)
            times.append(t)
        if volume > threshold or volume < -threshold:
            x_abnormal.append(i)
            abnormal.append(volume)
        else:
            x_normal.append(i)
            normal.append(volume)

    # print(x)
    # print(times)
    # trade_volume = df.groupby(by='time', as_index=False)['btc_volume'].sum()
    plt.figure(figsize=(10, 6))
    plt.stem(x_normal, normal, linefmt='g-', markerfmt='o')
    plt.stem(x_abnormal, abnormal, linefmt='r-', markerfmt='o')
    plt.hlines(y=[-threshold, threshold], xmin=0, xmax=agg.shape[0], linestyles='dashed', colors='orange', label='anomalous volumes')
    plt.xticks(ticks=x, labels=times, rotation=90)
    plt.xlabel('datetime')
    plt.ylabel('btc_volume')
    plt.legend()
    # plt.show()
    plt.savefig(out + file.replace('.csv', '.png'), dpi=100)
    plt.close()
