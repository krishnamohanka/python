import logging
import requests
from kiteconnect import KiteConnect
from kiteconnect import WebSocket

r_proxy = {'http': r'EU\NG6EADA:Password123%25@fr0-proxylan-vip.eu.airbus.corp:3128',
           'https': r'EU\NG6EADA:Password123%25@fr0-proxylan-vip.eu.airbus.corp:3128' }


proxy = {
					'host': 'fr0-proxylan-vip.eu.airbus.corpfr0-proxylan-vip.eu.airbus.corp',
					'port': 3000,
					'auth': ('username', 'password')
				}

kite_api_key = "yw8yelu5bpfel8ib"
kite_api_secret = "vaddqe1qb3lzorst3uolc1ptdo0l2cku"

logging.basicConfig(level=logging.DEBUG)

kite = KiteConnect(api_key="yw8yelu5bpfel8ib",proxies=r_proxy)

rq = kite.request_access_token("sulTUnrQxqYumZGVmOgXzWcCTxAaRbnc","vaddqe1qb3lzorst3uolc1ptdo0l2cku")

kite.set_access_token(rq['access_token'])

kite.ohlc("NSE:INFY")

#kite.set_access_token('xjsfx1mymtr3j340g2u4hhy1sshrtl6d')
kws = WebSocket(kite_api_key,'Kf879HRiMNS0DbOREhO1KyDqRl3J2bWu',"YK8879")


def on_ticks(tick,ws):
    # Callback to receive ticks.
    #logging.debug("Ticks: {}".format(ticks))
    print(tick)

def on_connect(ws):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([738561, 5633])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [738561])



# Assign the callbacks.
kws.on_tick = on_ticks
kws.on_connect = on_connect


# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect(disable_ssl_verification=True,proxy=proxy)
