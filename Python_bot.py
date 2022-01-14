import time
from binance.client import Client
from binance.enums import *
import pandas as pd
import numpy as np
import talib as ta
import matplotlib.pyplot as plt
from datetime import datetime

trdPair1="ETH"
trdPair2="USDT"
winRate=1.017

symbol = trdPair1 + trdPair2
interval = '5m'
limit = 500
start="2021-12-19 06:00:00"


sellQtyEth=0.1
buyQtyEth=0.1

gainUsdt=0.0;
takeUsdt=0.0;


#lastrade = trdPair1

api_key=""
secret_key=""

client=Client(api_key=api_key, api_secret=secret_key)


price=client.get_ticker(symbol=symbol)

lasPrice = client.get_ticker(symbol=symbol)

while True:
        Sonuclar = open("sonuclar.txt", "a")
        CuzdanTxt = open("Cuzdan.txt", "r")
        Cuzdan=CuzdanTxt.readlines()

        totalEth=float(Cuzdan[0][9:-1])
        totalUsdt=float(Cuzdan[1][10:])
        CuzdanTxt.close()

        totalEthMoney= totalEth* float(price['askPrice'])
        # Initial value
        
        klines = client.get_klines(symbol=symbol, interval='5m', limit='500')
        now = datetime.now()
        coitime = now.strftime("%H:%M:%S")
        
        
        #klines2 = client.get_historical_klines(tradePair, Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")
        close = [float(entry[4]) for entry in klines]

        close_array = np.asarray(close)
        close_finished = close_array[:-1]
        macd, macdsignal, macdhist = ta.MACD(close_finished, fastperiod=12, slowperiod=26, signalperiod=9)
        rsi = ta.RSI (close_finished, 14)

        price = client.get_ticker(symbol=symbol)

        macdArray = []
        macdSignalArray = []
        macdDiffArray = []

        for i in macd:
        #if not np.isnan(i):
                macdArray.append(i)
 
        for i in macdsignal:
        #if not np.isnan(i):
                macdSignalArray.append(i)
        for i in range(len(macdArray)):
        #if not np.isnan(i):
                macdDiffArray.append(macdArray[i] - macdSignalArray[i])

        i=len(macdArray)-1
        macdSatinAl=False
        rsiSatinAl=False

        macdSat=False
        rsiSat=False

        ########Sat 
        if (macdArray[i] > 0 and macdSignalArray[i] > 0 and macdDiffArray[i-1] > 0 and macdDiffArray[i] < 0):
                macdSat=True

        if (rsi[i-1] > 69 and rsi[i] > 58):
                rsiSat=True
        ########Al
        if  macdArray[i] < 0 and macdSignalArray[i] < 0 and macdDiffArray[i-1]< 0 and macdDiffArray[i]>0:
                macdSatinAl=True

        if(rsi[i-1] < 33 and rsi[i-1]< rsi[i] <=33):
                rsiSatinAl=True
        

        coiprice = format(float(price['askPrice']), '.2f')
        coiprice=float(coiprice)

        if  rsiSat==True and macdSat==True:
                gainUsdt= sellQtyEth * coiprice
                totalUsdt = totalUsdt + gainUsdt

                totalEth = totalEth - sellQtyEth
                totalEthMoney = totalEth * coiprice
                

                stat = 'Time: ' + str(coitime) + ' sell' + str(symbol) + ' gain: ' + str(gainUsdt) + ' TotalUsdt: ' + str(totalUsdt) + ' Total Eth Qty : ' + str(totalEth) + ' TotalEthMoney : ' + str(totalEthMoney)
                
                CuzdanTxt = open("Cuzdan.txt", "w")
                CuzdanTxt.write("totalEth=" + str(totalEth) + '\n' + "totalUsdt=" + str(totalUsdt))
                CuzdanTxt.close()

                Bakiye = open("Bakiye.txt", "a")
                Bakiye.write(stat + ' Coin Price: ' + str(coiprice)  + '\n')
                Bakiye.close()

        elif rsiSatinAl==True and macdSatinAl==True:
                takeUsdt = buyQtyEth * coiprice

                totalUsdt = totalUsdt - takeUsdt

                totalEth=totalEth + buyQtyEth
                totalEthMoney = totalEth * coiprice

                stat ='Time: ' + str(coitime) + ' buy' + str(symbol) + ' takeUsdt: ' + str(takeUsdt) + ' TotalUsdt: ' + str(totalUsdt) + ' Total Eth Qty : ' + str(totalEth) + ' TotalEthMoney : ' + str(totalEthMoney)
                
                CuzdanTxt = open("Cuzdan.txt", "w")
                CuzdanTxt.write("totalEth=" + str(totalEth) + '\n' + "totalUsdt=" + str(totalUsdt))
                CuzdanTxt.close()
                
                Bakiye = open("Bakiye.txt", "a")
                Bakiye.write(stat + '\n')
                Bakiye.close()
                
        else:
                stat = 'hold: ' + trdPair1 

        Sonuclar.write(coitime + ' ' + ' Previous Rsi: ' + str(rsi[i-1]) + ' Current Rsi: ' + str(rsi[i]) +
        ' Previous MacdDiff: ' + str(macdDiffArray[i-1]) + ' Current macdDiff: ' + str(macdDiffArray[i]) + ' '
        + price['askPrice'] + '  ' + stat +'\n' +'\n')

        Sonuclar.close()
        time.sleep(120)