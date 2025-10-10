import requests
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.coingecko.com/api/v3/simple/price"
params = {
         "ids": "bitcoin",
         "vs_currencies": "USD"
}
# Replace 'YOUR_API_KEY' with your actual API key
headers = {"x-cg-demo-api-key": api_key}

response = requests.get(url, params = params)

btc_price = response.json()
print(btc_price["bitcoin"]["usd"])
