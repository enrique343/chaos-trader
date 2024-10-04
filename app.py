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
            messageThread=Thread(target=cb.message)
            messageThread.setDaemon(True)
            messageThread.start()

            while running:
                coinBInput=input("Please input any commands or the program will run normally: \n")

                if coinBInput=="quit":
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