# SkyWatch — Console de supervision du trafic aérien

Petite console qui suit le trafic aérien en temps réel et repère automatiquement les situations anormales. Données 100% publiques, aucune donnée sensible.

## L'idée de départ

En lisant une annonce sur l'exploration et le prototypage, je me suis posé une question : est-ce que je suis capable de prendre un flux de données brutes qui ne veut rien dire tout seul, et d'en tirer un outil qu'un humain peut lire d'un coup d'œil pour décider ? Donnée brute, algorithme, interface. Je me suis donné le défi de le construire.

## Ce que ça fait

L'application interroge l'API publique OpenSky, récupère tous les avions au-dessus de la France, les affiche sur une carte, et lève trois types d'alertes :

- Code transpondeur d'urgence (7500 détournement, 7600 panne radio, 7700 urgence).
- Descente anormalement rapide, au-delà d'un seuil réglable.
- Perte de signal, un avion présent au relevé précédent et absent au suivant.

Les avions sont colorés sur la carte selon leur état, et les alertes sont listées par niveau de gravité. Le tout se rafraîchit tout seul.

## Comment le lancer

```
pip install -r requirements.txt
streamlit run app.py
```

Fonctionne en accès anonyme. Pour un rafraîchissement plus fréquent, on peut s'authentifier avec un client API OpenSky.

Les tests de la logique de détection tournent sans réseau :

```
pytest
```

## Les choix techniques

- La logique de détection est isolée dans `detection.py`, en fonctions pures, séparée de l'affichage dans `app.py`. Ça la rend lisible et testable.
- Chaque détecteur est couvert par des tests, y compris des cas qui ne doivent PAS déclencher d'alerte, pour vérifier qu'il ne se trompe pas.
- La détection de perte de signal compare deux relevés successifs, ce qui oblige à garder en mémoire le tour précédent via le session_state de Streamlit.

## Ce qui marche, et ce qui ne marche pas

Les trois détecteurs fonctionnent. Le squawk et la descente se lisent sur un seul relevé, la perte de signal sur deux relevés consécutifs.

Mais la détection de perte de signal génère énormément de faux positifs, et c'est sa vraie limite. Un avion qui sort simplement de la zone France par un bord est compté comme perdu, alors qu'il vole parfaitement, il est juste passé ailleurs. Mon détecteur confond deux choses différentes : un avion qui disparaît vraiment des radars, et un avion qui quitte ma fenêtre d'observation. La limite n'est pas dans les données, elle est dans le découpage que j'ai choisi.

J'ai aussi remarqué qu'une alerte de perte s'affichait sans indicatif, simplement parce que le callsign était absent dans les données.

## Ce que je testerais ensuite

- Ne déclarer perdu qu'un avion qui disparaît loin des bords, en plein centre de la zone, là où une disparition est réellement suspecte.
- Ou regarder sa dernière trajectoire pour voir s'il se dirigeait vers une frontière.
- Lisser le taux vertical sur plusieurs relevés, car une valeur instantanée sous le seuil peut être un simple soubresaut et générer une fausse alerte.

## Verdict

À poursuivre. L'approche donnée brute vers décision fonctionne, l'outil attrape de vraies descentes et de vraies urgences quand il y en a. La perte de signal, elle, demande à être affinée avant d'être fiable. J'ai appris à parler à une API réelle, à détecter des anomalies et à tester ma propre logique.

## Structure du projet

```
app.py               interface Streamlit, carte et affichage des alertes
detection.py         logique de détection, fonctions pures
test_detection.py    tests des détecteurs, sans réseau
requirements.txt     dépendances
```