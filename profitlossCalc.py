def calculatePnL(bp,sp,qty):
    brokerage_buy = 20 if (bp * qty * 0.0001)>20 else round(float(bp * qty * 0.0001),2)
    brokerage_sell =20 if ((sp * qty * 0.0001)>20) else round(float(sp * qty * 0.0001),2)
    brokerage = float(brokerage_buy + brokerage_sell)

    turnover = round(float((bp+sp)*qty),2)

    stt_total = round(float((sp * qty) * 0.00025))

    total_trans_charge = round(float(0.0000325*float(turnover)),2)

    stax = round(float(0.18 * float(brokerage + total_trans_charge)),2)

    sebi_charges = round(float(float(turnover)*0.0000015),2)

    total_tax = round(float(brokerage + stt_total + total_trans_charge + stax + sebi_charges),2)

    breakeven = round(float(total_tax / qty),2)

    net_profit = round(float(((sp - bp) * qty) - total_tax),2)

    print net_profit

    return net_profit

def getMargin(symbol):


calculatePnL(2000,1999,1000)



#margin calculator api
#https://api.kite.trade/margins/equity
