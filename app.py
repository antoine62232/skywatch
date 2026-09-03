import streamlit as st
import requests
from detection import detecter_urgence, detecter_descente_rapide

st.set_page_config(page_title="Supervision trafic aérien", layout="wide")

st.title("Console de supervision du trafic aérien en temps réel")

# Zone surveillée : la France, en coordonnées (min/max latitude et longitude)
ZONE_FRANCE = {"lamin": 41.0, "lomin": -5.5, "lamax": 51.5, "lomax": 9.6}

# URL de l'API OpenSky qui renvoie tous les avions d'une zone géographique
URL = "https://opensky-network.org/api/states/all"

reponse = requests.get(URL, params=ZONE_FRANCE, timeout=15)
donnees = reponse.json()

avions = donnees["states"]

# Construction d'une liste propre : une entrée par avion, avec sa position
positions = []
for avion in avions:
    longitude = avion[5]
    latitude = avion[6]
    # Certains avions n'envoient pas leur position, on les ignore
    if latitude is not None and longitude is not None:
        positions.append({"lat": latitude, "lon": longitude})

st.write("Nombre d'avions positionnés dans la zone : ", len(positions))

# On passe chaque avion au détecteur d'urgence
alertes = []
for avion in avions:
    alerte_urgence = detecter_urgence(avion)
    if alerte_urgence is not None:
        alertes.append(alerte_urgence)

    alerte_descente = detecter_descente_rapide(avion)
    if alerte_descente is not None:
        alertes.append(alerte_descente)

st.subheader("Alertes en cours")
if len(alertes) == 0:
    st.success("Aucune urgence détectée")
else:
    for alerte in alertes:
        st.error(f"{alerte['indicatif']} — {alerte['motif']}")
# st.map attend un tableau de points avec des colonnes "lat" et "lon"
st.map(positions)