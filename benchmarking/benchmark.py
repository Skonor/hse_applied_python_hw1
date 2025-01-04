from analysis import parallel_analysis, analysis
import pandas as pd
import time

if __name__ == '__main__':

    data = pd.read_csv('temperature_data.csv')

    start = time.time()
    result = analysis(data)
    end = time.time()
    print(f'Serial Execution Time: {end - start}')

    start = time.time()
    result = parallel_analysis(data)
    end = time.time()
    print(f'Parallel Execution Time: {end - start}')