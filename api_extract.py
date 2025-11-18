import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import yfinance as yf
import pandas as pd
import pytz

## Cryptos infos

load_dotenv()
api_key_cg = os.getenv("API_KEY_CG")

url = "https://api.coingecko.com/api/v3/coins/markets"


# Replace 'YOUR_API_KEY' with your actual API key
headers = {"x-cg-demo-api-key": api_key_cg}

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

## SP500 infos

TICKER = "^GSPC"
INTERVAL = "1m"

TIMEZONE = "America/New_York"

TICKER = "^GSPC"
INTERVAL = "1m"
TIMEZONE = "America/New_York"


def get_price_simple(dt_input: datetime) -> float | None:
    """
    Récupère le prix de clôture du S&P 500 (dernière valeur disponible).

    Args:
        dt_input: L'horodatage cible (doit être un objet datetime.datetime).

    Returns:
        float: Le prix de clôture trouvé, ou None si aucune donnée n'est disponible.
    """

    # 1. Préparation de l'heure cible (arrondi à la minute)
    dt_cible_naive = dt_input.replace(second=0, microsecond=0)

    # 2. Localisation et plage de recherche
    tz = pytz.timezone(TIMEZONE)
    # On localise l'heure cible dans le fuseau horaire du marché (NY)
    dt_cible_tz = tz.localize(dt_cible_naive)

    # Début : 7 jours avant (plage de sécurité pour garantir la donnée)
    start_time = dt_cible_tz - pd.Timedelta(days=7)

    # 3. Récupération des données
    data = yf.download(
        tickers=TICKER,
        start=start_time,
        end=dt_cible_tz,
        interval=INTERVAL,
        progress=False
    )

    if data.empty:
        return None

    # 4. Conversion de l'index au fuseau horaire du marché
    data.index = data.index.tz_convert(TIMEZONE)

    # 5. Extraction du prix le plus proche (Trouve la dernière valeur avant ou à l'heure cible)
    dernier_prix = data.asof(dt_cible_tz)

    # 6. Vérification et Extraction du prix (Résout l'erreur de ValueError et retourne un float)

    # Si la Series est complètement nulle (marché fermé ou donnée manquante):
    if dernier_prix.isnull().all():
        # On prend la toute dernière valeur disponible dans le DataFrame (le prix de clôture précédent).
        if not data.empty:
            return data.iloc[-1]['Close'].item()  # <-- Utilisation de .item()
        else:
            return None
    else:
        # Sinon, on retourne la valeur de 'Close' trouvée par asof.
        return dernier_prix['Close'].item()  # <-- Utilisation de .item()
# moment_a = "2025-11-13 22:33:27.888082"
# moment_b = "2025-11-05 19:39:35.511611"
#
# prix1, date1_clean =
# prix2, date2_clean = get_price_simple(moment_b)
#
# print("-" * 50)
# if prix1 and prix2:
#     # Déterminer la chronologie pour le calcul
#     if date1_clean < date2_clean:
#         prix_depart = prix1
#         prix_arrivee = prix2
#         date_depart = date1_clean
#         date_arrivee = date2_clean
#     else:
#         prix_depart = prix2
#         prix_arrivee = prix1
#         date_depart = date2_clean
#         date_arrivee = date1_clean
#
#     evolution = ((prix_arrivee - prix_depart) / prix_depart) * 100
#
#     print(f"📈 Prix de départ ({date_depart}) : {prix_depart:.2f}")
#     print(f"🏁 Prix d'arrivée ({date_arrivee}) : {prix_arrivee:.2f}")
#     print(f"**Taux d'évolution : {evolution:.2f}%**")
# else:
#     print("Impossible de calculer l'évolution : au moins un prix n'a pas été trouvé.")
