import csv
import pandas as pd
import numpy as np
import datetime


def data_extend(input_file_name, output_file_name):
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    pd.set_option('display.width', 5000)

    df = pd.read_csv(input_file_name, header=None)
    col_names = ['time', 'stock_id', 'exchange_id', 'price']
    df.columns = col_names

    df['time'] = pd.to_datetime(df['time'])

    grouped = df.groupby('stock_id')

    for name, group in grouped:
        print(name)

        group = group.drop_duplicates(subset=['time'], keep='first', inplace=False)
        group.index = group['time']

        group['time_diff'] = group['time'].shift(-1) - group['time']
        group['price_diff'] = group['price'].shift(-1) - group['price']
        group['is_buy'] = group.price_diff.apply(lambda x: 1 if x > 0 else 0)

        group['time_30s'] = group['time'] + datetime.timedelta(seconds=30)
        group['time_nearest_30'] = np.nan
        group['price_30s'] = 0
        group['reward_30s'] = 0

        group['time_1min'] = group['time'] + datetime.timedelta(seconds=60)
        group['time_nearest_1min'] = np.nan
        group['price_1min'] = 0
        group['reward_1min'] = 0

        group['time_3min'] = group['time'] + datetime.timedelta(seconds=180)
        group['time_nearest_3min'] = np.nan
        group['price_3min'] = 0
        group['reward_3min'] = 0

        group['time_5min'] = group['time'] + datetime.timedelta(seconds=300)
        group['time_nearest_5min'] = np.nan
        group['price_5min'] = 0
        group['reward_5min'] = 0

        df_is_buy_rows = group[group['is_buy'] == 1]

        for index, row in df_is_buy_rows.iterrows():

            i = group.index.get_loc(row['time_30s'], method='nearest')
            group.loc[index, 'time_nearest_30'] = group.loc[group.index[i], 'time']
            group.loc[index, 'price_30s'] = group.loc[group.index[i], 'price']
            group.loc[index, 'reward_30s'] = (group.loc[index, 'price_30s'] - group.loc[index, 'price']) * 100

            i = group.index.get_loc(row['time_1min'], method='nearest')
            group.loc[index, 'time_nearest_1min'] = group.loc[group.index[i], 'time']
            group.loc[index, 'price_1min'] = group.loc[group.index[i], 'price']
            group.loc[index, 'reward_1min'] = (group.loc[index, 'price_1min'] - group.loc[index, 'price']) * 100

            i = group.index.get_loc(row['time_3min'], method='nearest')
            group.loc[index, 'time_nearest_3min'] = group.loc[group.index[i], 'time']
            group.loc[index, 'price_3min'] = group.loc[group.index[i], 'price']
            group.loc[index, 'reward_3min'] = (group.loc[index, 'price_3min'] - group.loc[index, 'price']) * 100

            i = group.index.get_loc(row['time_5min'], method='nearest')
            group.loc[index, 'time_nearest_5min'] = group.loc[group.index[i], 'time']
            group.loc[index, 'price_5min'] = group.loc[group.index[i], 'price']
            group.loc[index, 'reward_5min'] = (group.loc[index, 'price_5min'] - group.loc[index, 'price']) * 100


        # print(group)
        group[['time', 'stock_id', 'exchange_id', 'price', 'is_buy', 'reward_30s', 'reward_1min', 'reward_3min', 'reward_5min']].to_csv(output_file_name, mode='a', header=True, index=None, float_format='%.3f', date_format='%H:%M:%S.%f')


if __name__ == '__main__':
    data_extend('stock_price.csv', '../stock_scv_parser/stock_price_extended.csv')
