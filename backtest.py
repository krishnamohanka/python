import datetime
import talib
import pandas as pd
import numpy as np
from collections import namedtuple
from autostk import ZerodhaSelenium
import matplotlib.pyplot as plt
#df1 = pd.DataFrame([[1,2],[3,4]],columns=['LTP','Time'])


class Simbha:
    def __init__(self, filename):
        self.filename = filename
        self.buynow, self.sellnow, self.shortsellnow, self.shortbuynow = False, True, False, True
        self.buynowindex, self.sellnowindex, self.shortsellnowindex, self.shortbuynowindex = 0, 0, None, None
        self.previousindex, self.lastindex = 0, 0
        self.stratliveTrade(self.filename)

    def round_nearest(self, x, a):
        return round(x / a) * a

    def ohlc(self, df):
        #df = pd.read_csv(filename)
        # df = pd.read_csv('intraday_1min_MSFT.csv')
        # df = df.iloc[::-1]
        #df.columns = ['price', 'time']
        df['timepass'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('timepass', inplace=True)
        dataOhlc = df['price'].resample('5Min').ohlc()
        # return df
        return dataOhlc

    def createOhlcFile(self, filename,timeframe):
        df = pd.read_csv(filename)
        # df = pd.read_csv('intraday_1min_MSFT.csv')
        # df = df.iloc[::-1]
        df.columns = ['price', 'time']
        df['timepass'] = pd.to_datetime(df['time'], unit='s')
        df.set_index('timepass', inplace=True)
        dataOhlc = df['price'].resample(str(timeframe)+'Min').ohlc()
        dataOhlc.to_csv(filename + "ohlc")
        # return df
        return dataOhlc

    def HA(self, df):
        df['HA_Close'] = (df['open'] + df['high'] + df['low']+df['close'])/4
        hkOpen, hkclose = [], []
        nt = namedtuple('nt', ['open', 'close'])
        previous_row = nt(df.ix[0, 'open'], df.ix[0, 'close'])
        i = 0
        for row in df.itertuples():
            ha_open = (previous_row.open + previous_row.close) / 2
            hkOpen.append(previous_row[0])
            hkclose.append(previous_row[1])
            df.ix[i, 'HA_Open'] = ha_open
            previous_row = nt(ha_open, row.close)
            i += 1

        df['HA_High'] = df[['HA_Open', 'HA_Close', 'high']].max(axis=1)
        df['HA_Low'] = df[['HA_Open', 'HA_Close', 'low']].min(axis=1)
        df['HA_OldOPEN'] = pd.Series(np.array(hkOpen), index=df.index)
        df['HA_OldCLOSE'] = pd.Series(np.array(hkclose), index=df.index)
        return df

    def EMA(self, df):
        df['EMA7'] = talib.EMA(df.close.values, timeperiod=5)
        df['EMA14'] = talib.EMA(df.close.values, timeperiod=10)
        return df

    def trades(self, df):
        bullishCandle = (df['HA_Close'] > df['HA_Open']) & (df['HA_Low'] == df['HA_Open'])
        bearishCandle = (df['HA_Close'] < df['HA_Open']) & (df['HA_High'] == df['HA_Open'])
        numCandle = bullishCandle.values
        numbearishCandle = bearishCandle.values
        buyIndex = []
        sellIndex = []
        self.buynowindex, self.sellnowindex = 0, 0
        for val in range(0, len(numCandle) - 1):
            # buy
            if val == 0:
                buyIndex.append(False)
            if numCandle[val] and numCandle[val+1]:
                if buyIndex[val] != True:
                    buyIndex.append(True)
                    if (not self.buynow) and self.sellnow:
                        self.buynow = True
                        self.sellnow = False
                        self.buynowindex = val + 1
                        print('buy price ', df['open'][self.buynowindex], 'buy index ', self.buynowindex)
                else:
                    buyIndex.append(False)
            else:
                buyIndex.append(False)
            # sell
            if val == 0:
                sellIndex.append(False)
            if numbearishCandle[val] and numbearishCandle[val + 1]:
                if sellIndex[val] != True:
                    sellIndex.append(True)
                    if (not self.sellnow) and self.buynow and (self.buynowindex > self.sellnowindex):
                        self.buynow = False
                        self.sellnow = True
                        self.sellnowindex = val + 1
                        print('sell price ', df['close'][self.sellnowindex], 'sell index ', self.sellnowindex)
                else:
                    sellIndex.append(False)
            else:
                sellIndex.append(False)

        if buyIndex == []:
            buyIndex=[False]
        df["Buy"] = buyIndex
        previous_7 = df['EMA7'].shift(1)
        previous_14 = df['EMA14'].shift(1)
        df['Sell'] = ((df['EMA7'] <= df['EMA14']) & (previous_7 >= previous_14))

        if sellIndex == []:
            sellIndex = [False]

        df["ShortSell"] = sellIndex

        previous_7 = df['EMA7'].shift(1)
        previous_14 = df['EMA14'].shift(1)
        df['ShortBuy'] = ((df['EMA14'] <= df['EMA7']) & (previous_14 >= previous_7))
        self.lastindex = df['close'].count()
        for onerow in df[self.previousindex:self.lastindex].iterrows():
            stockdata = onerow[1]
            shortbuy = stockdata['ShortBuy']
            shortsell = stockdata['ShortSell']
            if shortsell and (not shortbuy):
                if (not self.shortsellnow) and self.shortbuynow:
                    self.shortbuynow = False
                    self.shortsellnow = True
                    self.shortsellnowindex = onerow[0] + 1
                    print('short sell price ', df['open'][onerow[0]], 'ShortSell index ', self.shortsellnowindex - 1)
            if shortbuy and (not shortsell):
                if (not self.shortbuynow) and self.shortsellnow:
                    self.shortbuynow = True
                    self.shortsellnow = False
                    self.shortbuynowindex = onerow[0] + 1
                    print ('short Buy', df['close'][onerow[0]], 'ShortBuy Index ', self.shortbuynowindex - 1)

    def startTrade(self, df):
        hadf = self.HA(df)
        emadf = self.EMA(hadf)
        self.trades(emadf)

    def stratliveTrade(self, filename):
        self.createOhlcFile(filename, 10)
        df1 = pd.DataFrame()
        with open(filename +"ohlc", "r+") as f:
            for index, lines in enumerate(f.readlines()[1:]):
                if 'close' in df1:
                    self.previousindex = df1['close'].count()
                else:
                    self.previousindex = 0
                openi = float(lines.split(',')[1])
                high = float(lines.split(',')[2])
                low = float(lines.split(',')[3])
                close = float(lines.split(',')[4].replace('\n', ''))
                data = pd.Series([openi, high, low, close], index=['open', 'high', 'low', 'close'])
                df1 = df1.append(data, ignore_index=True)
                self.lastindex = df1['close'].count()
                if index == 29:
                    pass
                self.startTrade(df1)
                # print (index)
            print('working')


if __name__ == '__main__':
    filename = "C:\Users\NG6E4BC\workspace\pythonTradingAlgo\src\BrtiArtl_19_03_2018.csv"
    driver = "C:\Users\NG6E4BC\Documents\DoNotDelete\chromedriver_win32\chromedriver.exe"
    Simbha(filename)
