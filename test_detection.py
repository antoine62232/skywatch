from detection import detecter_urgence

def avion_test(squawk):
    """Fabrique un faux avion minimal avec le squawk voulu.
    On remplit jusqu'à l'index 14 car c'est là qu'est le squawk."""
    avion = [None] * 15
    avion[0] = "abc123" # icao24
    avion[1] = "TEST01" # Indicatif
    avion[14] = squawk # le code que l'on veut tester
    return avion


def test_detecte_urgence_generale():
    avion = avion_test("7700")
    alerte = detecter_urgence(avion)
    assert alerte is not None
    assert alerte["motif"] == "Urgence générale"


def test_detecte_detournement():
    avion = avion_test("7500")
    alerte = detecter_urgence(avion)
    assert alerte is not None


def test_avion_normal_pas_d_alerte():
    avion = avion_test("1000")
    alerte = detecter_urgence(avion)
    assert alerte is None