import pandas as pd
import numpy as np
import os 



def get_data(csv_file,arg_date):
    df = pd.read_csv(csv_file)
    # print(df.values.shape)

    filter_data = {}
    count = 0
    for row in df.values:
        date = row[0].split()[0]
        # if date == '2017/8/15' or date == '2018/1/22':
        if date == arg_date:
            time = row[0].split()[-1]
            hour = int(time.split(':')[0])
            minute = int(time.split(':')[1]) + hour*60
            dist = minute % 60
            if dist < 5:
                try:
                    if dist < filter_data[date+':'+str(hour)][0]:
                        filter_data[date+':'+str(hour)] = [dist,count]
                        #print(date,time,dist,hour,count)
                    else:
                        pass
                except:
                    filter_data[date+':'+str(hour)] = [dist,count]
                    #print(date,time,dist,hour,count)
            if dist > 55:
                dist = 60 - dist
                try:
                    if dist < filter_data[date+':'+str(hour+1)][0]:
                        filter_data[date+':'+str(hour+1)] = [dist,count]
                        #print(date,time,dist,hour+1,count)
                    else:
                        pass
                except:
                    filter_data[date+':'+str(hour+1)] = [dist,count]
                    #print(date,time,dist,hour+1,count)
            count += 1
            # print(count)

    idx = []
    for key in filter_data:
        # print(key,filter_data[key])
        idx.append(filter_data[key][-1])

    # print(df.values[idx], df.values[idx].shape)
    if filter_data:
        return df.values[idx].T
    else:
        return False

DATE = '2017/8/15'
DATA = {}
FILES = [['File\\Time']]
for root,parent,files in os.walk('Saidi'):
    for _file in files:
        print('Processing file ',_file)
        data_T = get_data(os.path.join(root,_file),DATE)

        if type(data_T) == type(False):
            continue
        FILES.append([_file])

        # df_new = pd.DataFrame(get_data(os.path.join(root,_file)))
        # df_new.to_csv('res/' + _file.split('.')[0] + '.csv')
        '''
        Row 
        0 Time
        1 Temp
        2 Humidity
        3 PM25
        4 CO2
        5 Light 
        '''
        DATA['Time'] = np.array([data_T[0]])
        idx = 1 # Start from metric Temp
        for metric in ['Temp','Humidity','PM25','CO2','Light']:
            try:
                DATA[metric].append(data_T[idx])
            except:
                DATA[metric] = [data_T[idx]]
            idx += 1
        
FILES = np.array(FILES)
for metric in ['Temp','Humidity','PM25','CO2','Light']:
    DATA[metric] = np.array(DATA[metric])
    print(metric, DATA[metric].shape)
    # print(DATA[metric])
    res = np.vstack((DATA['Time'],DATA[metric]))
    print(res.shape)
    res = np.hstack((FILES,res))
    print(res.shape)

    df_new = pd.DataFrame(res)
    df_new.to_csv('res-Saidi/' + DATE.replace('/','_') + '_' + metric + '.csv')


'''
以CO2为例
每一行是每个测量点在不同时间点的指标值；
保留时间点信息为每一列的0元素
'''