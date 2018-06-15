import pandas as pd
import requests
import io
import time
import datetime
import logging
from simbaSimple.kiteUtility import KiteUtility
from simbaSimple.algoUtility import AlgoUtile
from datetime import date
import talib


def startTrade(ku, it_df):
    print("started simba successfully!")
    first=True
    while (1):
        d = {}
        for instrument in list(it_df["instrument_token"]):
            if(instrument == 2714625):
                ohlc_df = None
                ohlc_df = ku.getHistoricalData(instrument)
                time.sleep(1)
                symbol = ku.getSymbolFromInstrument(instrument)
                d[symbol] = AlgoUtile.EMA(ohlc_df)
                break

        for k in d.keys():
            HA = d[k]
            if (HA["EMABuy"].tail(1).values[0] == True):
                print(k)
                time.sleep(1)
                instrument = ku.getInstrumentFromSymabol(k)
                buyprice, buyqty,sellprice,selqty = ku.get_price(instrument)
                time.sleep(1)

                ku.placeOrderBuy(k, buyprice, 10)
                if (not first):
                    time.sleep(1)
                    ku.placeOrderBuy(k, buyprice + .10, 10)

                if first:
                    first = False

                print("Buy_" + k + str(buyprice))

            if (HA["EMASell"].tail(1).values[0] == True):

                time.sleep(1)
                instrument = ku.getInstrumentFromSymabol(k)
                sellprice,selqty = ku.get_price(instrument)
                time.sleep(1)

                ku.placeOrderSell(k, sellprice, 10)
                if (not first):
                    time.sleep(1)
                    ku.placeOrderSell(k, sellprice - .10, 10)

                if first:
                    first = False
                print("Sell_" + k + str(sellprice))
            pass

        print("waiting")
        time.sleep(300)

        dt = datetime.datetime.now()
        if (dt.hour == 15 and dt.minute >= 30):
            break

print("waiting to start ")
while (1):
    dt = datetime.datetime.now()
    if (dt.hour == 9 and dt.minute == 45 and dt.second == 3):
        break

print("started")
token = ''
with open("token.txt", "r")as f:
    token = f.read()
print(token)
ku = KiteUtility(token)
# ku.getNwriteNifty50InstrumentToken()
it_df = ku.getInstrumentTokenDF()
startTrade(ku, it_df)

pass


