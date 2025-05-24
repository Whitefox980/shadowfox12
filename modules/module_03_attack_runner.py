import requests
import json
import os
from urllib.parse import urljoin

PAYLOAD_DB = "payloads/payload_zahoor_db.json"
TARGETS_FILE = "data/targets.txt"

def ucitaj_payloade():
    if not os.path.exists(PAYLOAD_DB):
        print("[!] Nema payload baze.")
        return {}
    with open(PAYLOAD_DB, "r") as f:
        return json.load(f)

def ucitaj_mete():
    if not os.path.exists(TARGETS_FILE):
        print("[!] Nema fajla targets.txt")
        return []
    with open(TARGETS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def prikazi_tipove(payloads):
    print("\n[+] Dostupni tipovi:")
    for idx, tip in enumerate(payloads):
        print(f"  [{idx+1}] {tip}")
    return list(payloads.keys())

def pokreni_napad(mete, payloadi, tip):
    print(f"\n[*] Pokrećem testove za: {tip}\n")
    for url in mete:
        for payload in payloadi:
            try:
                test_url = f"{url}?test={requests.utils.quote(payload)}"
                r = requests.get(test_url, timeout=5)

                if payload in r.text:
                    print(f"[+] HIT! {url} reflektuje payload: {payload}")
            except Exception as e:
                print(f"[-] Greška za {url}: {e}")

if __name__ == "__main__":
    baza = ucitaj_payloade()
    if not baza:
        exit()

    tipovi = prikazi_tipove(baza)

    try:
        izbor = int(input("[?] Izaberi broj payload tipa: "))
        izabrani_tip = tipovi[izbor - 1]
    except:
        print("[!] Neispravan izbor.")
        exit()

    mete = ucitaj_mete()
    if not mete:
        print("[!] Nema meta.")
        exit()

    pokreni_napad(mete, baza[izabrani_tip], izabrani_tip)
