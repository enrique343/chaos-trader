import requests
import json
import base64
import hmac
import hashlib
import time
import os
url = "https://api.gemini.sandbox.com/v1/mytrades"
gemini_api_key = "3JYTWud4F11ugGQCngHnjb6vo7ED"
gemini_api_secret = "account-wnDUlwqWZa2cuAE75efB".encode()

payload_nonce = time.time()

payload =  {"request": "/v1/mytrades", "nonce": payload_nonce}
encoded_payload = json.dumps(payload).encode()
b64 = base64.b64encode(encoded_payload)
signature = hmac.new(gemini_api_secret, b64, hashlib.sha384).hexdigest()

request_headers = {
    'Content-Type': "text/plain",
    'Content-Length': "0",
    'X-GEMINI-APIKEY': gemini_api_key,
    'X-GEMINI-PAYLOAD': b64,
    'X-GEMINI-SIGNATURE': signature,
    'Cache-Control': "no-cache"
    }

response = requests.post(url, headers=request_headers)

my_trades = response.json()
print(my_trades)