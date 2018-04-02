#https://www.nseindia.com/content/indices/ind_nifty500list.csv
import logging
from kiteconnect import KiteConnect
from kiteconnect import WebSocket
import csv
import requests
import sqlite3

url = 'https://www.nseindia.com/content/indices/ind_nifty500list.csv'
r = requests.get(url)
text = r.iter_lines()
reader = csv.reader(text, delimiter=',')
firstline = True
nifty500=[]
for lines in reader:
    if firstline:    #skip first line
        firstline = False
        continue
    nifty500.append(lines[2])
    print lines[2]

kite = KiteConnect(api_key="yw8yelu5bpfel8ib")
kite.set_access_token("s4on3tuaxkiquqxws5duxx0n3xgszdmi")

instruments= kite.instruments("NSE")
nifty500dict={}
for symbol in nifty500:
    for k in instruments:
        if k["tradingsymbol"]== symbol:
            nifty500dict[k["exchange_token"]] = k["tradingsymbol"]

print nifty500dict
print (len(nifty500dict))


conn = sqlite3.connect(r"instruments.db")

c = conn.cursor()

for k in nifty500dict.keys():

    # Insert a row of data
    qry = "INSERT INTO instruments VALUES ({},'{}')".format(k,nifty500dict[k])
    print qry
    c.execute(qry)

    # Save (commit) the changes

conn.commit()
conn.close()