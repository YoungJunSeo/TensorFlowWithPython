import sys
from xcoin_api_client import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import time
import pandas as pd
import datetime
import numpy as np
import csv
import datetime

api_key = ""
api_secret = ""

Coins = ["XRP"]
#Coins = ["BTC", "ETH", "DASH", "LTC", "ETC", "XRP", "BCH", "XMR", "ZEC", "QTUM", "BTG", "EOS"]

call_count = 10


class Worker(QThread):
    finished = pyqtSignal(str, str)

    def run(self):
        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')

        self.file = open('Coin_rawdata_%s.csv' % nowDate, 'w', encoding='utf-8', newline='')
        self.write = csv.writer(self.file)

        self.price_quantity_dqn_data = []

        # Using HDFStore
        #store = pd.HDFStore('coins_raw_datas.h5')


        #store.close()
        count = 0
        print("save_coin_rawdata")

        while True:
            try:
                self.api = XCoinAPI(api_key, api_secret)
                rgParams = {
                    "count": call_count
                };

                for currency in Coins:

                    # URL 생성
                    result = self.api.xcoinApiCall("/public/ticker/" + currency, rgParams)
                    if result == None:
                        continue

                    self.msleep(100)

                    self.average_price = float(result['data']['average_price'])

                    # URL 생성
                    result = self.api.xcoinApiCall("/public/orderbook/" + currency, rgParams)
                    if result == None:
                        continue

                    self.msleep(900)


                    self.price_quantity_dqn_data.clear()

                    self.price_quantity_dqn_data.append(currency)
                    self.timestamp = result['data']['timestamp']
                    self.price_quantity_dqn_data.append(self.timestamp)
                    self.price_quantity_dqn_data.append(self.average_price)
                    self.price_quantity_dqn_data.append(float(result['data']['bids'][0]['price']))
                    self.price_quantity_dqn_data.append(float(result['data']['asks'][0]['price']))

                    self.sum_volume = 0

                    for i in range(0, call_count):
                        self.sum_volume = self.sum_volume + float(result['data']['bids'][call_count - 1 - i]['quantity'])
                        self.sum_volume = self.sum_volume + float(result['data']['asks'][i]['quantity'])

                    self.sum_volume = self.sum_volume * 0.5

                    for i in range(0, call_count):
                        self.price_quantity_dqn_data.append(round(float(result['data']['bids'][call_count - 1 - i]['quantity'])/self.sum_volume ,8))

                    self.price_quantity_dqn_data.append(round(float(result['data']['bids'][0]['price'])/self.average_price ,8))
                    self.price_quantity_dqn_data.append(round(float(result['data']['asks'][0]['price'])/self.average_price ,8) )

                    for i in range(0,call_count):
                        self.price_quantity_dqn_data.append(
                            round(float(result['data']['asks'][i]['quantity']) / self.sum_volume, 8))

                    self.write.writerow(self.price_quantity_dqn_data)

                    store = pd.HDFStore('coins_raw_datas.h5')
                    pd.set_option('io.hdf.default_format', 'table')

                    raw_data = np.array([[float(self.timestamp), float(self.average_price)]])
                    #print(ddd)
                    raw_data_list = ['time','av_price']
                    #print(ccc)
                    df = pd.DataFrame(raw_data , columns=raw_data_list)
                    #store['coin'] = df
                    print(count)
                    if count == 0:
                        store.put('coin', df)
                    else:
                        store.append('coin', df)

                    count = count + 1
                    store.close()

                    df_read = pd.read_hdf('coins_raw_datas.h5', 'coin')

                    print(df_read)


                    print(currency + " "+ self.timestamp )
                    #print(str(self.price_quantity_dqn_data))

            except Exception as e:
                print(type(e))


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.worker = Worker()
        self.worker.start()


app = QApplication(sys.argv)
window = MyWindow()
app.exec_()

