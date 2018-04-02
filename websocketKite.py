from kiteconnect import WebSocket
import logging
import pickle
logging.basicConfig(level=logging.DEBUG)

kite_api_key = "yw8yelu5bpfel8ib"
kite_api_secret = "vaddqe1qb3lzorst3uolc1ptdo0l2cku"

kws = WebSocket(kite_api_key,'Kf879HRiMNS0DbOREhO1KyDqRl3J2bWu',"YK8879")



def on_ticks(tick,ws):
    # Callback to receive ticks.
    #logging.debug("Ticks: {}".format(ticks))
    with open("2_4_2018_1", "a+") as f:
        f.write(str(tick))
    print(tick)

def on_connect(ws):
    # Callback on successful connect.
    # Subscribe to a list of instrument_tokens (RELIANCE and ACC here).
    ws.subscribe([738561, 5633])

    # Set RELIANCE to tick in `full` mode.
    ws.set_mode(ws.MODE_FULL, [738561,5633])



# Assign the callbacks.
kws.on_tick = on_ticks
kws.on_connect = on_connect


# Infinite loop on the main thread. Nothing after this will run.
# You have to use the pre-defined callbacks to manage subscriptions.
kws.connect()