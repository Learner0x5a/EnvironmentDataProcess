import pandas as pd
import numpy as np
import os 
from time import time


csv_file = './HuiTian/汇天历史数据_1至4月.csv'
print('Reading csv file...')
df = pd.read_csv(csv_file,encoding='gbk')
print('Reading done.')
# print(df)
# print(df['label'].values.min(), df['label'].values.max())
# print(df[df['label']==6789]['x'].values[0])
# filename = df[df['label']==6789]['x'].values[0]
# df[df['label']==6789].to_csv('res-huitian/' + filename + '.csv')
count = 0 
print(df['label'].values.min(), df['label'].values.max())
start = time()
for i in range(df['label'].values.min(), df['label'].values.max()):
    # print(df[df['label']==6789])
    index = df['label']==i
    subdf = df[index]
    count += 1

    
    # if count % 1e4 == 0:
        # print('Processing...', count)
    if not subdf.empty:
        # print('empty sub dataframe, label: ',i)
    # else:    
        filename = subdf['x'].values[0]
        # print('Writing sub dataframe ',filename)
        subdf.to_csv('res-huitian/' + filename + '.csv')
    if count % 10 == 0:
        end = time()
        print(count, 'Processing time: ', end - start)
