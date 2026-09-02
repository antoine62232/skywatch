import streamlit as st
import requests

st.set_page_config(page_title="Supervision trafic aérien", layout="wide")

st.title("Console de supervision du trafic aérien en temps réel")

# Zone surveillée : la France, en coordonnées (min/max latitude et longitude)
ZONE_FRANCE = {"lamin": 41.0, "lomin": -5.5, "lamax": 51.5, "lomax": 9.6}

# URL de l'API OpenSky pour renvoie tous les avions d'une zone géographique
URL = "https://opensky-network.org/api/states/all"

reponse = requests.get(URL, params=ZONE_FRANCE, timeout=15)
donnees = reponse.json()

avions = donnees["states"]
st.write("Nombre d'avions détectés : ", len(avions))