import datetime
import talib
import pandas as pd
import numpy as np
from collections import namedtuple
import matplotlib.pyplot as plt
#df1 = pd.DataFrame([[1,2],[3,4]],columns=['LTP','Time'])




def round_nearest(x, a):
    return round(x / a) * a

def ohlc(df):
    #df = pd.read_csv(filename)
    # df = pd.read_csv('intraday_1min_MSFT.csv')
    # df = df.iloc[::-1]
    #df.columns = ['price', 'time']
    df['timepass'] = pd.to_datetime(df['time'], unit='s')
    df.set_index('timepass', inplace=True)
    dataOhlc = df['price'].resample('10Min').ohlc()
    # return df
    return dataOhlc


def HA(df):
    df['HA_Close'] = (df['open'] + df['high'] + df['low']+df['close'])/4
    hkOpen, hkclose = [], []
    nt = namedtuple('nt', ['open','close'])
    previous_row = nt(df.ix[0, 'open'], df.ix[0, 'close'])
    i = 0
    for row in df.itertuples():
        ha_open = (previous_row.open + previous_row.close) / 2
        hkOpen.append(previous_row[0])
        hkclose.append(previous_row[1])
        df.ix[i,'HA_Open'] = ha_open
        previous_row = nt(ha_open, row.close)
        i += 1

    df['HA_High'] = df[['HA_Open', 'HA_Close', 'high']].max(axis=1)
    df['HA_Low'] = df[['HA_Open', 'HA_Close', 'low']].min(axis=1)
    df['HA_OldOPEN'] = pd.Series(np.array(hkOpen), index=df.index)
    df['HA_OldCLOSE'] = pd.Series(np.array(hkclose), index=df.index)
    return df

def EMA(df):
        df['EMA7'] = talib.EMA(df.close, timeperiod=5)
        df['EMA14'] = talib.EMA(df.close, timeperiod=10)

        return df

def trades(df):

    bullishCandle = (df['HA_Close'] > df['HA_Open']) & (df['HA_Low'] == df['HA_Open'])
    numCandle = bullishCandle.values
    buyIndex = []
    for val in range(0, len(numCandle) - 1):
        if val == 0:
            buyIndex.append(False)

        if numCandle[val] and numCandle[val+1]:
            if buyIndex[val] != True:
                buyIndex.append(True)

            else:
                buyIndex.append(False)
        else:
            buyIndex.append(False)

    if buyIndex==[]:
        buyIndex=['False']
    df["Buy"] = buyIndex
    previous_7 = df['EMA7'].shift(1)
    previous_14 = df['EMA14'].shift(1)
    df['Sell'] = ((df['EMA7'] <= df['EMA14']) & (previous_7 >= previous_14))

    pass
    ###  Shorting ##############################################################################################
    bearishCandle = (df['HA_Close'] < df['HA_Open']) & (df['HA_High'] == df['HA_Open'])
    numCandle = bearishCandle.values
    sellIndex = []
    for val in range(0, len(numCandle) - 1):
        if val == 0:
            sellIndex.append(False)

        if numCandle[val] and numCandle[val + 1]:
            if sellIndex[val] != True:
                sellIndex.append(True)
            else:
                sellIndex.append(False)
        else:
            sellIndex.append(False)

    if sellIndex == []:
        sellIndex = ['False']

    df["ShortSell"] = sellIndex

    previous_7 = df['EMA7'].shift(1)
    previous_14 = df['EMA14'].shift(1)
    df['ShortBuy'] = ((df['EMA14'] <= df['EMA7']) & (previous_14 >= previous_7))

    try:
        if(len(df.loc[df['ShortSell'] == True]['open'])>0):
            print ('ShortSell')
            print (df.loc[df['ShortSell'] == True]['open'][0])
        if (len(df.loc[df['ShortBuy'] == True]['open'])>0):
            print ('ShortBuy')
            print (df.loc[df['ShortBuy'] == True]['open'][0])
        if (len(df.loc[df['Buy'] == True]['open'])>0):
            print ('Buy')
            print (df.loc[df['Buy'] == True]['open'][0])
        if (len(df.loc[df['Sell'] == True]['open'])>0):
            print ('Sell')
            print (df.loc[df['Sell'] == True]['open'][0])
    except Exception as e:
        print(e.message)
        pass

def startTrade(df):
    dfohlc = ohlc(df)
    hadf = HA(dfohlc)
    emadf = EMA(hadf)
    trades(emadf)

with open ("C:\Users\krsna\PycharmProjects\Flaskweb\BhartiAirtel_16-03_2018","r")  as f:
    df1 = pd.DataFrame()
    for lines in f.readlines():
        ltp = float(lines.split(',')[0])
        time = float(lines.split(',')[1].replace('\n',''))
        data = pd.Series([ltp,time],index=['price','time'])
        df1 = df1.append(data,ignore_index=True)
        startTrade(df1)
        pass
