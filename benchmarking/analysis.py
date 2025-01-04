import pandas as pd
from multiprocessing import Pool

def analysis(input_data):
    data = input_data.copy()
    data['timestamp'] = pd.to_datetime(data['timestamp'])

    data = data.sort_values(['city', 'timestamp'])
    data['rolling_avg_30'] = data.groupby('city')['temperature'].transform(lambda x: x.rolling(window=30, min_periods=1).mean())

    seasonal_stats = data.groupby(['city', 'season'])['temperature'].agg(['mean', 'std']).reset_index()
    seasonal_stats.rename(columns={'mean': 'mean_temp', 'std': 'std_temp'}, inplace=True)

    data = data.merge(seasonal_stats, on=['city', 'season'], how='left')

    data['is_anomaly'] = (data['temperature'] < (data['mean_temp'] - 2 * data['std_temp'])) | \
                        (data['temperature'] > (data['mean_temp'] + 2 * data['std_temp']))

    return data

def parallel_analysis(input_data):
    data = input_data.copy()
    data_split = [group for _, group in data.groupby('city')]
    with Pool() as pool:
        result = pool.map(analysis, data_split)
    return pd.concat(result)