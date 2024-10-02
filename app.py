from coinbase import jwt_generator
import pip._vendor.requests
import json
import os
api_key       = os.getenv('KEY_NAME')
api_secret     = os.getenv('PRIVATE_KEY')


request_method = "GET"
request_path = "/api/v3/brokerage/accounts"

jwt_uri = jwt_generator.format_jwt_uri(request_method, request_path)
jwt_token = jwt_generator.build_rest_jwt(jwt_uri, api_key, api_secret)


url= 'https://api.coinbase.com/api/v3/brokerage/accounts'        #gets the cards requested
headers = {
    "Authorization":f'Bearer {jwt_token}',
    "Content-Type": "application/json" ,
}
r = pip._vendor.requests.get(url, headers=headers)
print(r)
res=r.json()
print(res.keys())