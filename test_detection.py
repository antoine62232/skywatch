from detection import detecter_urgence, detecter_descente_rapide

def avion_test(squawk=None, taux_vertical=None):
    """Fabrique un faux avion minimal avec le squawk voulu.
    On remplit jusqu'à l'index 14 car c'est là qu'est le squawk."""
    avion = [None] * 15
    avion[0] = "abc123" # icao24
    avion[1] = "TEST01" # Indicatif
    avion[11] = taux_vertical # taux vertical
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


def test_code_7000_pas_une_urgence():
    avion = avion_test("7000")
    alerte = detecter_urgence(avion)
    assert alerte is None


def test_descente_rapide_detectee():
    avion = avion_test(taux_vertical=-20.0)
    alerte = detecter_descente_rapide(avion)
    assert alerte is not None


def test_montee_pas_d_alerte():
    avion = avion_test(taux_vertical=12.0)
    alerte = detecter_descente_rapide(avion)
    assert alerte is None


def test_descente_lente_pas_d_alerte():
    avion = avion_test(taux_vertical=-5.0)
    alerte = detecter_descente_rapide(avion)
    assert alerte is None