import pip._vendor.requests
import json
import os
import http.client
from coinbase.rest import RESTClient
from json import dumps
from coinbase.websocket import WSUserClient
import time

class coinbase:
    def __init__(self):
        self.api_key =  os.getenv('KEY_NAME')
        self.api_secret = os.getenv('PRIVATE_KEY')
        self.client = RESTClient(api_key=self.api_key, api_secret= self.api_secret)
        with open('configs.json', 'r') as file:
            self.configs = json.load(file)

        file.close() 

    def coinList(self):
        with open("coinIdsCB.json", "w") as file:
            file.truncate()
        file.close()
        coinDict={}
        products = self.client.get_products()
        coins=products["products"]
        cnt=0
        for i in coins:
            if i["base_name"] not in coinDict.keys():
                coinDict[i["base_name"]]=[i["product_id"]]
            else:
                base=coinDict[i["base_name"]]
                base.append(i["product_id"])
                coinDict[i["base_name"]]=base

            cnt+=1


        with open('coinIdsCB.json', 'w') as f:
            f.write(json.dumps(coinDict))
        print("finished populating coinIdsCB.json")

    def makeBuy(self,coinId,amount):#base and coin args refer to coinIdsCB.json
        '''Purchases coins'''
        if amount<=0:
            return

        file = open("transactionId.txt","r")
        latest=file.read()
        file.close()


        order = self.client.market_order_buy(client_order_id="clientOrderId"+str(latest), product_id=str(coinId), quote_size=str(amount)) #amtount is the amt you want to buy in the second asset in the id pair. if BTC-USDC you'll make the purchase using USDC
        latest=str(int(latest)+1)
        file = open("transactionId.txt","w")

        file.write(latest)
        print(order)

    def makeSell(self,coinId,amount):#base and coin args refer to coinIdsCB.json
        '''Sells coins'''
        if amount<=0:
            return

        file = open("transactionId.txt","r")
        latest=file.read()
        file.close()


        order = self.client.market_order_sell(client_order_id="clientOrderId"+str(latest), product_id=str(coinId), base_size=str(amount)) #amt is the amt of coins you want to sell
        latest=str(int(latest)+1)
        file = open("transactionId.txt","w")
        

        file.write(latest)
        print(order)

    def checkWallet(self):
        '''checks what coins are available in the wallet currently'''
        products = self.client.get_accounts()
        available={}
        for i in products["accounts"]:
            if float(i["available_balance"]["value"])>0 and i["currency"] not in available.keys():
                available[i["currency"]]=[i["available_balance"]["value"]]


        with open("heldCoins.json", "w") as file:
            file.truncate()
        file.close()

        with open('heldCoins.json', 'w') as file:
            file.write(json.dumps(available))
        file.close()
    def message(self):
        while True:
            print("Running program on coinbase platform")
            time.sleep(600)

    def validateWhiteList(self):
        with open('coinWhiteListCB.json', 'r') as file:
            whiteList = json.load(file)
        file.close()
        present={}
        for i in whiteList.keys():
            if whiteList[i]!=[]:
                present[i]=whiteList[i]
        with open('coinIdsCB.json', 'r') as file:
            coinIds = json.load(file)
        file.close()
        invalidTemp=[]
        invaild=[]
        for i in present:
            for coin in present[i]:
                if coin not in coinIds[i]:
                    invalidTemp.append(coin)
            if invalidTemp!=[]:
                invaild.append(invalidTemp)
                invalidTemp=[]
        if invaild!=[]:
            print("Please remove invalid tokens below: ")
            print(invaild)

            tempConfig=self.configs
            tempConfig["coinbase"]["valid"]="False"
            self.configs=tempConfig
            with open('configs.json', 'w') as file:
                file.write(json.dumps(tempConfig))
            file.close()            
        



def main():
    #coinList()  #makes a json file that has a list of each base and coin that trades under that name
    #makeBuy("DOGE-USDC",5)
    #makeSell("DOGE-USDC",4)
    runner=coinbase()
    runner.checkWallet()
    print("done")
    #checkWallet()
if __name__ == "__main__":
    main()