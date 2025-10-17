import sqlite3
import data_load
import api_extract
from pathlib import Path

DIR = Path.cwd()

MENU = '''1. Ajouter ou retirer des cryptos au panier
2. Obtenir et sauvegarder les données actuelles du panier
3. Calculer l'évolution du panier par rapport à la précédente sauvegarde (Moyenne des cryptos du panier).
4. Comparer l'évolution du panier avec celle du Nasdaq100.
5. Afficher les données sauvegardées
6. Quitter'''

MENU_BASKET = '''Entrer le numéro puis faites entrée pour chacune des cryptos que vous voulez ajouter.
Faites simplement entré quand vous avez fait votre choix : 

1. Bitcoin
2. Ethereum
3. Solana '''

CRYPTO_DICO = {"1": "bitcoin",
               "2": "ethereum",
               "3": "solana"}

CRYPTO_CHOICE = [1, 2, 3]
crypto_basket = []

connex = sqlite3.connect("crypto.db")

def create_base():
    if not DIR/"crypto.db":
        with connex:
            connex.execute(data_load.CREATE_TABLE)
    else:
        return True

def get_and_save_data(currency="usd", *ids_args):
    liste = api_extract.get_infos(currency, *ids_args)
    for i, j in enumerate(liste):
        nom = j['nom']
        price = j['price']
        market_cap = j['market_cap']
        volume = j['volume']
        time = j['time']
        print(f"{i} Nom : {nom} \n"
              f"Prix actuel : {price} \n"
              f"Capitalisation : {market_cap} \n"
              f"Volume : {volume}. \n")
        with connex:
            connex.execute(data_load.ADD_DATA, (nom, price, market_cap, volume, time))
    return True

def show_data():
    with connex:
        cursor = connex.cursor()
        cursor.execute(data_load.SHOW_DATA)
        return cursor.fetchall()

def basket_choice():
    print(MENU_BASKET)
    while new_crypto := (input(MENU_BASKET)):
        if int(new_crypto) in CRYPTO_CHOICE:
            crypto_basket.append(int(new_crypto))
        else:
            print("Mauvais choix !")
    print(f"Votre choix : {crypto_basket}")
    return crypto_basket

while (user_choice := int(input(MENU))) != 6:
    create_base()
    if user_choice == 1:
        basket_choice()
    elif user_choice == 2:
        ### A remplacer par un try except pour savoir si crypto basket existe
        ### Simplifier la procédure ici pour basket_choice retourne directement la liste avec les str
        liste = [CRYPTO_DICO[str(i)] for i in crypto_basket]
        get_and_save_data('usd', *liste)
    elif user_choice == 3:
        pass
    elif user_choice == 4:
        pass
    elif user_choice == 5:
        print(show_data())
    else:
        print("Mauvais choix !")


