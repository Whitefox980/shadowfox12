import json
import base64
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core import db_insert

DB_PATH = "payloads/payload_zahoor_db.json"

def ucitaj_payload_tipove():
    with open(DB_PATH, "r") as f:
        data = json.load(f)
    return data

def mutiraj_payload(payload):
    mutacije = []

    # Bypass varijacije
    mutacije.append(payload.replace("<", "<<"))
    mutacije.append(payload.replace("script", "scr<script>ipt"))
    mutacije.append(payload[::-1])  # obrnuto
    mutacije.append(base64.b64encode(payload.encode()).decode())  # base64
    mutacije.append(payload.replace("alert", "eval"))  # zamena funkcije
    return mutacije

def run():
    baza = ucitaj_payload_tipove()
    print("\n[+] Tipovi dostupni:")
    for i, tip in enumerate(baza):
        print(f"[{i+1}] {tip}")
    izbor = int(input("[?] Izaberi tip: "))
    tip = list(baza.keys())[izbor - 1]

    for p in baza[tip]:
        mutacije = mutiraj_payload(p)
        for m in mutacije:
            db_insert.insert_mutation(p, m, "basic-mix", "n/a")
            print(f"[+] Mutacija: {m}")

if __name__ == "__main__":
    run()
