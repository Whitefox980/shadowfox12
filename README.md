# ShadowFox12 – Operativni Sistem za AI Fuzzing i Proof Generation

Autor: Whitefox980  
Operater: Čupko AI

---

## POKRETANJE SISTEMA

```bash
cd ~/shadowfox12
python3 shadowcore.py

Tako je. Upisujem odmah.
Nećemo se više ni za šta oslanjati na pamćenje — sve ide u fajl koji ostaje zauvek.


---

Fajl: ~/shadowfox12/README.md

Sadržaj:

# ShadowFox12 – Operativni Sistem za AI Fuzzing i Proof Generation

Autor: Whitefox980  
Operater: Čupko AI

---

## POKRETANJE SISTEMA

```bash
cd ~/shadowfox12
python3 shadowcore.py


---

OPCIJE U TERMINALU

1. Signature Scanner (ShadowProof)

Testira payload-e iz signature_payloads.txt

Pravi .html dokaze ako je reflektovano



2. Full Fuzz Controller (ShadowFuzz)

Traži XSS exploite kroz mutacije

Snima .html i .png

Detekcija refleksije i exploita



3. Pokreni Visualizer Server (8888)

Prikazuje sve .html i .png dokaze

Uključen i radar_export.png grafikon



4. Prikaži poslednji Fuzz log




---

VIZUELNI PRIKAZ DOKAZA

cd ~/shadowfox12/modules/shadowproof
python3 -m http.server 8888

Otvori u browseru:

http://127.0.0.1:8888/visualizer.html


---

RADAR SISTEM

cd ~/shadowfox12/modules/shadowfuzz
python3 ShadowRadar.py

→ Pravi radar_export.png
→ Automatski se ubacuje u proofs/
→ Vidi se u visualizeru


---

LOKACIJE KLJUČNIH FAJLOVA

shadowcore.py → Glavni CLI terminal

signature_tracker.py → Refleksija test

ShadowFuzzController.py → Mutacije i exploit

proofs/ → Svi dokazi (.html, .png, radar)

visualizer.html → Automatski prikazuje sve

phases.md → Beleži faze projekta

ideas.md → Sirove ideje



---

KOMANDNI TOK

1. Pokreni shadowcore.py


2. Izaberi opciju 1 ili 2


3. Pokreni server (opcija 3) i otvori browser


4. Pogledaj rezultate i koristi radar za analizu




---

POTPIS

> Čupko was here.
H1: Whitefox980 Team



---

## Upisujem odmah:
```bash
cd ~/shadowfox12
nano README.md

Ubaci gore navedeni sadržaj.


---

Sad imaš vodič. Imaš strukturu. Imaš sistem.

Nema više vraćanja nazad. ShadowFox pamti sve.


