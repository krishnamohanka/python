import datetime
import talib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print(
    datetime.datetime.fromtimestamp(
        int("1284101485")
    ).strftime('%Y-%m-%d %H:%M:%S')
)


df1= pd.read_csv("C:\Users\krsna\PycharmProjects\Flaskweb\BhartiAirtel_16-03_2018")
df1.columns=['LTP','TIME']
df1['ctime']  = pd.to_datetime(df1['TIME'], unit='s')
df1 = df1.set_index('ctime')
df1=df1.LTP.resample('5Min').ohlc()
df1['EMA7'] = talib.EMA(df1.close,timeperiod=7)
df1['EMA14'] = talib.EMA(df1.close,timeperiod=14)

df1['K'], df1['D'] = talib.STOCHRSI(df1.close, timeperiod=14, fastk_period=5, fastd_period=3, fastd_matype=0)

plt.plot(df1['EMA7'])
plt.plot(df1['EMA14'])
plt.show()

plt.plot(df1['K'])
plt.plot(df1['D'])
plt.show()

pass
