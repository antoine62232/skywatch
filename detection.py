# Les trois codes transpondeur universels qui signalent une urgence
CODES_URGENCE = {
    "7500": "Détournement",
    "7600": "Panne radio",
    "7700": "Urgence générale",
}


def detecter_urgence(avion):
    """Renvoie une alerte si l'avion affiche un code de détresse, sinon None"""
    squawk = avion[14]
    if squawk in CODES_URGENCE:
        return {
            "icao24": avion[0],
            "indicatif": avion[1],
            "motif": CODES_URGENCE[squawk],
            "squawk": squawk,
        }
    return None


# Seuil de descente rapide, en mètres par seconde (négatif = l'avion descend)
SEUIL_DESCENTE = -15.0


def detecter_descente_rapide(avion):
    """Renvoie une alerte si l'avion descend plus vite que le seuil, sinon None."""
    taux_vertical = avion[11]
    if taux_vertical is not None and taux_vertical <= SEUIL_DESCENTE:
        return {
            "icao24": avion[0],
            "indicatif": avion[1],
            "motif": "Descente rapide",
            "taux_vertical": taux_vertical,
        }
    return None