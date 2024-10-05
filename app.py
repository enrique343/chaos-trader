import pip._vendor.requests
import json
import os
import http.client
from coinbase.rest import RESTClient
from json import dumps
from coinbase.websocket import WSUserClient
from cbTrader import coinbase

from threading import *





def main():
    with open('configs.json', 'r') as file:
        configs = json.load(file)

    file.close() 

    done=False
    while not done:
        userInput=input("Please type a command below: \n")
        if userInput=="help":
           #commands=["startCB \t\t\t Run program on Coinbase\n","startGEM \t\t\t Run program on Gemini\n","startBIN \t\t\t Run program on Binance\n","quit \t\t\t Shut down the program"]
            print("startCB \t\t\tRun program on Coinbase\nstartGEM \t\t\tRun program on Gemini\nstartBIN \t\t\tRun program on Binance\nquit \t\t\tShut down the program")
        elif userInput=="startCB":
            #some stuff to implement the connection to coinbase
            print("coinbase")
            running=True
            cb=coinbase()
            if configs["coinbase"]["new"]=="True":
                makeIds=Thread(target=cb.coinList)
                makeIds.start()
                print("Please insert 10 valid coin pairs into the coinWhiteList.json file. Example of coin pair: BTC-USDC")
                print("Shutting down..")
                exit()

            validateThread=Thread(target=cb.validateWhiteList)
            # validateThread.setDaemon(True)
            validateThread.start()
            if configs["coinbase"]["valid"]=="False":
                print("Please fix your coinWhiteListCB.json file to have valid coin pairs such as: BTC-USDC")
                print("Shutting down..")
                exit()

            messageThread=Thread(target=cb.message)
            messageThread.setDaemon(True)
            messageThread.start()
            while running:
                
                coinBInput=input("Please input any commands or the program will run normally: \n")
                if coinBInput=="list":
                    with open('coinIdsCB.json', 'r') as file:
                        data = json.load(file)
                    print(data.keys())
                    file.close()
                elif coinBInput=="wallet":
                    with open('heldCoins.json', 'r') as file:
                        data = json.load(file)
                    print(data.keys())
                    file.close()
                elif coinBInput=="whitelist":
                    with open('coinWhiteListCB.json', 'r') as file:
                        data = json.load(file)
                    whiteListed=[]
                    for i in data.keys():
                        if data[i]!=[]:
                            whiteListed.append(data[i])

                    file.close()    
                    print(whiteListed)
                elif coinBInput=="quit":
                    exit()

            print("done")
        elif userInput=="startGEM":
            #some stuff to implement the connection to Gemini
            print("Gemini")
        elif userInput=="startBIN":
            #some stuff to implement the connection to Binance
            print("Binance")
        elif userInput=="quit":
            print("Shutting down..")

            exit()
        else:
            print("please enter a valid command. If you  need to see all the commands please type help into the terminal\n")

if __name__ == "__main__":
    main()