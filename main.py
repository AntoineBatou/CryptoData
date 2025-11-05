import sqlite3
import data_load
import api_extract
import datetime
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

CRYPTO_DICO = {1: "bitcoin",
               2: "ethereum",
               3: "solana"}

CRYPTO_CHOICE = [1, 2, 3]
crypto_basket = []

connex = sqlite3.connect("crypto.db")


def format_timedelta(td):
    """Formate un timedelta de manière lisible"""
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if days > 0:
        parts.append(f"{days}j")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}min")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)

def create_base():
    if not DIR/"crypto.db":
        with connex:
            connex.execute(data_load.CREATE_TABLE)
    else:
        return True

def get_and_save_data(currency="usd", *ids_args):
    liste = api_extract.get_infos(currency, *ids_args)
    for i, j in enumerate(liste, start=1):
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
            if int(new_crypto) not in crypto_basket:
                crypto_basket.append(int(new_crypto))
                print("\n")
                print(f"{CRYPTO_DICO.get(int(new_crypto)).title()} ajouté !")
                print("------")
            else:
                print("Déjà dans le panier !")
        else:
            print("Mauvais choix !")
    print("\n")
    print("------")
    print("Votre choix :")
    for i in crypto_basket:
        print(f"- {CRYPTO_DICO.get(i).title()}")
    print("------")
    liste = [CRYPTO_DICO[i] for i in crypto_basket]
    return liste


def get_prec(name):
    with connex:
        cursor = connex.cursor()
        cursor.execute(data_load.SELECT_PREC_PRICE, (name,))
        final = cursor.fetchall()
        prix1, prix2 = final
        final_tup = (prix1[0], prix2[0])
        return final_tup

def get_cap_t0(name):
    with connex:
        cursor = connex.cursor()
        cursor.execute(data_load.SELECT_CAP_T0, (name,))
        return cursor.fetchall()[1][0]

def get_time_diff(name):
    with connex:
        cursor = connex.cursor()
        cursor.execute(data_load.SELECT_2LAST_TIME, (name,))
        times = cursor.fetchall()
        time_final = datetime.datetime.fromisoformat(times[0][0])
        time_start = datetime.datetime.fromisoformat(times[1][0])
        time_diff = time_final - time_start
        format = format_timedelta(time_diff)
        print(f"⏱️ Intervalle de calcul : {format}")
        return format


def analyze_prec(tup):
    #Compare uniquement le dernier prix avec l'avant dernier, pas de comparaison du panier
        prix1, prix2 = tup
        diff = ((prix2 - prix1) / prix1) * 100
        print(f"Différence de {diff:.2f} %")
        return diff

def analyse_basket(sum_cap, data_price_capi):
    #Réalise comparaison de l'évolution du panier au global en pondérant par la market cap
    variations = []
    capitalisations = []
    for i in data_price_capi:
        variations.append(((i['price_ev'][1] - i['price_ev'][0]) / i['price_ev'][0]) * 100)
        capitalisations.append(i['capitalisation'])
    total = (sum(v * c for v, c in zip(variations,capitalisations)) / sum_cap)
    return(f"Le panier a évolué de {total:.2f} % en moyenne !")


def basket_var():
    liste = [CRYPTO_DICO[i] for i in crypto_basket]
    ### Je vais créer un dictionnaire qui contiendra chacune des cryptos du panier (nom), la capitalisation (t0). Pour faire une évolution globale de l'indice par capitalsiation
    data_price_capi = []
    sum_cap = 0
    for i in liste:
        price_tup = get_prec(i.title())
        cap_t0 = get_cap_t0(i.title())
        sum_cap += cap_t0
        dico = {"name": i.title(),
                "price_ev": price_tup,
                "capitalisation": cap_t0}
        data_price_capi.append(dico)
    return sum_cap, data_price_capi

while (user_choice := int(input(MENU))) != 6:
    create_base()
    if user_choice == 1:
        print("\n")
        print("------")
        basket_choice()
    elif user_choice == 2:
        # Am&liorer cette répétition
        liste = [CRYPTO_DICO[i] for i in crypto_basket]
        if len(liste) == 0:
            print("Vous n'avez pas défini de panier, donc on récupère les 100 premières !")
        get_and_save_data('usd', *liste)
    elif user_choice == 3:
        # Améliorer cette répétition
        liste = [CRYPTO_DICO[i] for i in crypto_basket]
        for i in liste:
            print("\n")
            print(i.title())
            valeurs = get_prec(i.title())
            analyze_prec(valeurs)
            get_time_diff(i.title())
            print("---")
        print_basket_var = input('Souhaitez-vous obtenir la variation du panier ? (y/n)')
        if print_basket_var == "y":
            sum_cap, data_price_capi = basket_var()
            print(analyse_basket(sum_cap, data_price_capi))


    elif user_choice == 4:
        pass

    elif user_choice == 5:
        print(show_data())
    else:
        print("Mauvais choix !")
