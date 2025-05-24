import json
import os

DB_PATH = "payloads/payload_zahoor_db.json"

def ucitaj_bazu():
    if not os.path.exists(DB_PATH):
        print(f"[!] Nema baze na putanji: {DB_PATH}")
        return {}

    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception as e:
            print(f"[!] Greška pri učitavanju JSON baze: {e}")
            return {}

def prikazi_tipove(baza):
    print("\n[+] Dostupne kategorije payloada:\n")
    for idx, tip in enumerate(baza.keys()):
        print(f"  [{idx+1}] {tip}")
    print()

def prikazi_payloade(baza, izbor):
    kljuc = list(baza.keys())[izbor - 1]
    print(f"\n[>] Payloadi za: {kljuc}\n")
    for i, payload in enumerate(baza[kljuc]):
        if isinstance(payload, dict):
            print(f"{i+1}. {payload.get('payload')}  # {payload.get('notes', '')}")
        else:
            print(f"{i+1}. {payload}")
    print()

if __name__ == "__main__":
    baza = ucitaj_bazu()
    if not baza:
        exit()

    prikazi_tipove(baza)

    try:
        izbor = int(input("[?] Izaberi broj kategorije: "))
        prikazi_payloade(baza, izbor)
    except Exception as e:
        print(f"[!] Neispravan unos: {e}")
