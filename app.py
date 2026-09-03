import streamlit as st
import requests
import pydeck as pdk
from detection import detecter_urgence, detecter_descente_rapide, detecter_pertes_signal, CODES_URGENCE
from streamlit_autorefresh import st_autorefresh
from opensky import recuperer_avions

st.set_page_config(page_title="Supervision trafic aérien", layout="wide")
# Rafraîchissement automatique toutes les 30 secondes
st_autorefresh(interval=30000, key="refresh")

st.title("Console de supervision du trafic aérien en temps réel")

# Zone surveillée : la France, en coordonnées (min/max latitude et longitude)
ZONE_FRANCE = {"lamin": 41.0, "lomin": -5.5, "lamax": 51.5, "lomax": 9.6}

# Identifiants OpenSky pour l'authentification
client_id = st.secrets.get("OPENSKY_CLIENT_ID")
client_secret = st.secrets.get("OPENSKY_CLIENT_SECRET")

donnees = recuperer_avions(ZONE_FRANCE, client_id, client_secret)
avions = donnees["states"]

# Construction d'une liste propre : une entrée par avion, avec sa position
# Couleurs RVB selon l'état de l'avion
COULEUR_NORMAL = [40, 180, 99] # vert
COULEUR_DESCENTE = [230, 150, 30] # orange
COULEUR_URGENCE = [220, 40, 40] # rouge

points = []
for avion in avions:
    longitude = avion[5]
    latitude = avion[6]
    if latitude is None or longitude is None:
        continue  # pas de position, on passe au suivant

    # Par défaut l'avion est normal, donc vert
    couleur = COULEUR_NORMAL
    if detecter_descente_rapide(avion) is not None:
        couleur = COULEUR_DESCENTE
    if detecter_urgence(avion) is not None:
        couleur = COULEUR_URGENCE

    points.append({
        "lat": latitude,
        "lon": longitude,
        "couleur": couleur,
    })

st.write("Nombre d'avions positionnés dans la zone : ", len(points))

# On passe chaque avion au détecteur d'urgence
alertes = []
for avion in avions:
    alerte_urgence = detecter_urgence(avion)
    if alerte_urgence is not None:
        alertes.append(alerte_urgence)

    alerte_descente = detecter_descente_rapide(avion)
    if alerte_descente is not None:
        alertes.append(alerte_descente)

# On compare le relevé actuel à celui du tour précédent, gardé en mémoire
avions_avant = st.session_state.get("avions_precedents", [])
pertes = detecter_pertes_signal(avions_avant, avions)
for perte in pertes:
    alertes.append(perte)

# On mémorise le relevé actuel pour le prochain rafraîchissement
st.session_state["avions_precedents"] = avions

st.subheader("Alertes en cours")

if len(alertes) == 0:
    st.success("Aucune anomalie détectée pour le moment.")
else:
    st.write(f"{len(alertes)} alerte(s) en cours")
    for alerte in alertes:
        motif = alerte["motif"]
        indicatif = alerte["indicatif"]
        if motif in CODES_URGENCE.values():
            st.error(f"🔴 {indicatif} — {motif}")
        elif motif == "Descente rapide":
            st.warning(f"🟠 {indicatif} — {motif}")
        else:
            st.info(f"🟣 {indicatif} — {motif}")

# Carte centrée sur la France
vue = pdk.ViewState(latitude=46.6, longitude=2.5, zoom=4.5)

# Une couche de points, colorés selon l'état de chaque avion
couche = pdk.Layer(
    "ScatterplotLayer",
    data=points,
    get_position=["lon", "lat"],
    get_fill_color="couleur",
    get_radius=10000,
)

st.pydeck_chart(pdk.Deck(layers=[couche], initial_view_state=vue))