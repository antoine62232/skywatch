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