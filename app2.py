from coinbase.rest import RESTClient
from json import dumps
from coinbase.websocket import WSUserClient
from cbTraderTest import coinbase
from detectEvents import eventFinder
from userInputs import dialog
from threading import *
import time
import json
import random


def main():
    file = open("transactionId.txt","r")
    latestTransaction=file.read()
    file.close()

    with open('configs.json', 'r') as file:
        configs = json.load(file)

    file.close()

    with open('coinWhiteListCB.json', 'r') as file:
        whiteList = json.load(file)
    tradingList=[]
    for i in whiteList:
        if whiteList[i]!=[]:
            tradingList.append(i)
    file.close() 

    max_trade=configs["coinbase"]["max"]
    min_trade=configs["coinbase"]["min"]
    range_trade=float(max_trade)-float(min_trade)

    startup=dialog()
    events=eventFinder()
    cb=coinbase(latestTransaction)
    messageThread=Thread(target=startup.startCB)
    messageThread.setDaemon(True)
    messageThread.start()
    starting=True
    points=0
    timeStamp1 = time.time()
    booting=True
    print("starting valorant cv")
    while True:
        if booting==False:
            time.sleep(30)
        else:
            booting=False
        kills=events.detect_kills()
        print("kills detected")

        if kills>=5:
            points=1000
        print("starting round start detection")
        roundFound=events.detect_round_start()

        #this is to calc the time from the last timestap
        timeStamp2 = time.time()
        diff=timeStamp2-timeStamp1
        diff=round(diff)
        timeStamp1=timeStamp2
        timeStamp2 = time.time()
        rounded=round(diff)

        if diff>200:
            continue


        #get if the final second was odd or even
        modRes=rounded%2

        #convert points into usable num for amt to sell or buy
        points=kills*20+diff
        tradeNum=(points%100)

        #randomize how a coin and it's variant gets chosen
        startRand=random.choice(tradingList)
        ind=tradingList.index(startRand)
        choiceInd=(tradeNum+ind)% len(tradingList)
        trade_coin=tradingList[choiceInd]

        coinPair=""

        variants=whiteList[trade_coin]
        if len(variants)==1:
            variant_coin=variants[0]
            buying=trade_coin
            desiredCoinVar=variant_coin
            coinPair=desiredCoinVar

        else:
            variant_coin=random.choice(variants)
            ind=variants.index(variant_coin)
            coinInd=(kills+ind)% len(tradingList)
            variant_coin=variants[coinInd]
            buying=trade_coin
            desiredCoinVar=variant_coin
            coinPair=desiredCoinVar




        if tradeNum==0:
            trade_amt=max_trade
        else:

            trade_amt=range_trade*(tradeNum/100)
            trade_amt=round(trade_amt,3)
        modRes=1
        if modRes==1:#trades will be from 0(min trade) to 100 (max trade)
            cb.makeSell(coinPair,trade_amt)
        else:
            cb.makeBuy(coinPair,trade_amt)





if __name__ == "__main__":
    main()