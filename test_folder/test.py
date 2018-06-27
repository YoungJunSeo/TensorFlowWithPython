import sys
import numpy as np
import tables as tb
import time
import pandas as pd
import csv

name = []
time = []
average_price = []
bids_price = []
asks_price = []

bids_call_1 = []
bids_call_2 = []
bids_call_3 = []
bids_call_4 = []
bids_call_5 = []
bids_call_6 = []
bids_call_7 = []
bids_call_8 = []
bids_call_9 = []
bids_call_10 = []
bids_price_average = []
buyed_price = []
asks_price_average = []
asks_call_1 = []
asks_call_2 = []
asks_call_3 = []
asks_call_4 = []
asks_call_5 = []
asks_call_6 = []
asks_call_7 = []
asks_call_8 = []
asks_call_9 = []
asks_call_10 = []




with open('miner-test.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in spamreader:
        name.append(row[0])
        time.append(row[1])
        average_price.append(float(row[2]))
        bids_price.append(float(row[3]))
        asks_price.append(float(row[4]))
        bids_call_10.append(float(row[5]))
        bids_call_9.append(float(row[6]))
        bids_call_8.append(float(row[7]))
        bids_call_7.append(float(row[8]))
        bids_call_6.append(float(row[9]))
        bids_call_5.append(float(row[10]))
        bids_call_4.append(float(row[11]))
        bids_call_3.append(float(row[12]))
        bids_call_2.append(float(row[13]))
        bids_call_1.append(float(row[14]))
        bids_price_average.append(float(row[15]))
        asks_price_average.append(float(row[16]))
        asks_call_1.append(float(row[17]))
        asks_call_2.append(float(row[18]))
        asks_call_3.append(float(row[19]))
        asks_call_4.append(float(row[20]))
        asks_call_5.append(float(row[21]))
        asks_call_6.append(float(row[22]))
        asks_call_7.append(float(row[23]))
        asks_call_8.append(float(row[24]))
        asks_call_9.append(float(row[25]))
        asks_call_10.append(float(row[26]))


list_data = ['average_price','bids_price','asks_price','bids_call_10','bids_call_9','bids_call_8','bids_call_7',
             'bids_call_6','bids_call_5','bids_call_4','bids_call_3','bids_call_2','bids_call_1','bids_price_average',
             'asks_price_average','asks_call_1','asks_call_2','asks_call_3','asks_call_4','asks_call_5','asks_call_6',
             'asks_call_7','asks_call_8','asks_call_9','asks_call_10']
list_data1 = list('ABC')

raw_data1 = np.stack([average_price, bids_price, asks_price, bids_call_10, bids_call_9, bids_call_8, bids_call_7,
                      bids_call_6, bids_call_5, bids_call_4, bids_call_3, bids_call_2, bids_call_1,bids_price_average,
                      asks_price_average, asks_call_1, asks_call_2, asks_call_3, asks_call_4, asks_call_5, asks_call_6,
                      asks_call_7, asks_call_8, asks_call_9, asks_call_10], axis=1)


df = pd.DataFrame(raw_data1, columns=list_data)

store = pd.HDFStore('store.h5')
store['data'] = df # save it

store.close()


