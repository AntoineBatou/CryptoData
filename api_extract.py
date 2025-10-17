import requests
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()
api_key = os.getenv("API_KEY")

url = "https://api.coingecko.com/api/v3/coins/markets"


# Replace 'YOUR_API_KEY' with your actual API key
headers = {"x-cg-demo-api-key": api_key}

def get_infos(currency, *ids_args):
    ids = ",".join(ids_args)
    token = {"ids": ids,
             "vs_currency": currency}
    response = requests.get(url, params= token, headers= headers)

    if response.status_code != 200:
        print('Erreur avec la demande !')
        return False


    liste_resultat = []
    for i in response.json():
        curr_dir = {
        "nom": i["name"],
        "price": i["current_price"],
        "market_cap": i["market_cap"],
        "volume": i["total_volume"],
        "time": datetime.now().isoformat()
        }

        liste_resultat.append(curr_dir)

    if len([*ids_args]) != len(liste_resultat):
        print("!! TOUS LES IDS N'ONT PAS ETE PRIS EN COMPTE !!")
    return liste_resultat
