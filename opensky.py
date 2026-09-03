import time
import requests

# Adresses officielles d'OpenSky
TOKEN_URL = "https://auth.opensky-network.org/auth/realms/opensky-network/protocol/openid-connect/token"
STATES_URL = "https://opensky-network.org/api/states/all"

# Mémoire du token entre deux appels
_token = None
_token_expire = 0


def _obtenir_token(client_id, client_secret):
    """Demande un token à OpenSky, ou réutilise le précédent s'il est encore valide."""
    global _token, _token_expire

    # Si on a déjà un token encore valide, on le réutilise
    if _token is not None and time.time() < _token_expire - 30:
        return _token

    reponse = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=15,
    )
    reponse.raise_for_status()
    donnees = reponse.json()

    _token = donnees["access_token"]
    _token_expire = time.time() + donnees["expires_in"]
    return _token


def recuperer_avions(zone, client_id=None, client_secret=None):
    """Récupère les avions d'une zone. S'authentifie si des identifiants sont fournis."""
    entetes = {}
    if client_id and client_secret:
        token = _obtenir_token(client_id, client_secret)
        entetes["Authorization"] = f"Bearer {token}"

    reponse = requests.get(STATES_URL, params=zone, headers=entetes, timeout=15)
    reponse.raise_for_status()
    return reponse.json()