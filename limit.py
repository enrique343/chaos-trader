from coinbase.rest import RESTClient
from coinbase.websocket import WSClient
import json
import math
import os

api_key       = os.getenv('KEY_NAME')
api_secret     = os.getenv('PRIVATE_KEY')

limit_order_id = ""
order_filled = False


def on_message(msg):
    global order_filled
    global limit_order_id
    message_data = json.loads(msg)
    if 'channel' in message_data and message_data['channel'] == 'user':
        orders = message_data['events'][0]['orders']
        for order in orders:
            order_id = order['order_id']
            if order_id == limit_order_id and order['status'] == 'FILLED':
                order_filled = True

with open('coinIds.json', 'r') as file:
    coins = json.load(file)
done=False
while not done:
    currInput=input("Please type in the currency you would like to buy. e.g Bitcoin,Dogecoin,Solana: \n")
    if currInput not in coins.keys():
        print("Please check coinIds for the currency name (Bitcoin, Solana, etc). If you don't have that file please run the coinList function in app.py \n")
    else:
        done=True
print()
done=False
while not done:
    coinInput=input("Please type in the coin you would like to buy. e.g BTC-USD, BTC-USDC, BTC-USDT, BTC-EUR, BTC-GBP: \n")
    if coinInput not in coins[currInput]:
        print("Please check coinIds for the coin name (BTC-USD, BTC-USDC, etc). If you don't have that file please run the coinList function in app.py \n")
    else:
        done=True


print()

done=False
while not done:
    amtInput=input("Please type in the amount you wish to purchase: \n")
    try:
        amtFloat=float(amtInput)
        done=True
    except ValueError:
        print("Please input a valid number \n")


amtFloat="5"
coinInput="DOGE-USD"

file = open("transactionId.txt","r")
latest=file.read()
file.close()

update=str(int(latest)+1)
file = open("transactionId.txt","w")

file.write(update)
file.close()


# initialize REST and WebSocket clients
rest_client = RESTClient(api_key=api_key, api_secret=api_secret, verbose=True)
ws_client = WSClient(api_key=api_key, api_secret=api_secret, on_message=on_message, verbose=True)
# rest_client.cancel_orders(order_ids=["16"])
# open WebSocket connection and subscribe to channels
ws_client.open()
ws_client.subscribe([coinInput], ["heartbeats", "user"])

# get current price of BTC-USD and place limit-buy order 5% below
product = rest_client.get_product(coinInput)
coin_usd_price = float(product["price"])
calculated_coin_usd_price = coin_usd_price -(coin_usd_price * 0.05)
adjusted_coin_usd_price = str(math.floor(calculated_coin_usd_price))

if float(adjusted_coin_usd_price)>=1:
    limit_order = rest_client.limit_order_gtc_buy(
        client_order_id=latest,
        product_id=coinInput,
        base_size=amtFloat,# how much of the coin you want to buy
        limit_price=adjusted_coin_usd_price # uses the adjusted price if equal to or greater than 1. This is meant for stable coins.
    )
else:
    limit_order = rest_client.limit_order_gtc_buy(
        client_order_id=latest,
        product_id=coinInput,
        base_size=amtFloat,# how much of the coin you want to buy in the second asset in the asset pair
        limit_price=str(calculated_coin_usd_price) # uses the calculated price. This is meant for meme coins or coins under a dollar.
    )



limit_order_id = latest

# wait for order to fill
while not order_filled:
    ws_client.sleep_with_exception_check(1)




print(f"order {limit_order_id} filled!")
ws_client.close()