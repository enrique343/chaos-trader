from coinbase import jwt_generator
import pip._vendor.requests
import json
import os
import http.client
from coinbase.rest import RESTClient
from json import dumps
api_key       = os.getenv('KEY_NAME')
api_secret     = os.getenv('PRIVATE_KEY')


client = RESTClient(api_key=api_key, api_secret=api_secret)





def coinList():
    with open("coinIds.json", "w") as file:
        file.truncate()
    file.close()
    coinDict={}
    products = client.get_products()
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

    print(cnt)

    with open('coinIds.json', 'w') as f:
        f.write(json.dumps(coinDict))
def main():
    coinList()  #makes a json file that has a list of each base and coin that trades under that name
    

if __name__ == "__main__":
    main()