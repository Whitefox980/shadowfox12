import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core import db_insert

import time
from datetime import datetime
import sqlite3
from urllib.parse import quote
import requests
from core import db_insert

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DB_PATH = "shadowfox.db"
PAYLOADS = "payloads/payload_zahoor_db.json"

def get_target(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url FROM targets WHERE id = ?", (target_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def get_payloads():
    import json
    with open(PAYLOADS, "r") as f:
        return json.load(f)

def run_payloads(target_id, base_url, tip, payload_list):
    print(f"\n[*] Pokrećem {tip} payload-e na: {base_url}")
    hits = 0
    for payload in payload_list:
        try:
            test_url = f"{base_url}?test={quote(payload)}"
            r = requests.get(test_url, timeout=5)
            reflected = 1 if payload in r.text else 0
            db_insert.insert_scan_result(target_id, tip, payload, reflected, str(r.status_code), len(r.text))
            if reflected:
                print(f"[HIT] {payload}")
                hits += 1
        except Exception as e:
            print(f"[!] Greška: {e}")
    return hits

def get_mutations(tip):
    technique_map = {
        "XSS": "basic-mix",
        "SSRF": "ssrf-bypass",
        "SQLi": "sql-obf",
        "LFI": "lfi-basic"
    }

    technique = technique_map.get(tip.upper())
    if not technique:
        return []

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT mutated_payload FROM mutations WHERE technique = ?', (technique,))
    rows = c.fetchall()
    conn.close()
    return [row[0] for row in rows]
def advisor(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT reflected, response_size FROM scan_results WHERE target_id = ?", (target_id,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("[AI] Nema rezultata za analizu.")
        return

    reflections = sum(1 for r in rows if r[0] == 1)
    large_resp = sum(1 for r in rows if r[1] and r[1] > 10000)

    if reflections == 0:
        print("[AI] Nema refleksije. Pokušaj mutaciju ili header injection.")
    if large_resp > 0:
        print("[AI] Veliki response detektovan. Pogledaj Replay.")
    if reflections > 0:
        print("[AI] Refleksija potvrđena. Aktiviraj Screenshot ili Listener ako payload sadrži JS.")

def generate_report(target_id):
    from agents.agent_pdf import generate_pdf
    generate_pdf(target_id)

def run_auto(target_id):
    base_url = get_target(target_id)
    # Signature Payload Injection
    signature_payload = "<h1>Chupko was here - ShadowFox AI</h1>"
    test_url = f"{base_url}?test={quote(signature_payload)}"
    try:
        r = requests.get(test_url, timeout=5)
        reflected = 1 if signature_payload in r.text else 0
        db_insert.insert_scan_result(target_id, "SIGNATURE", signature_payload, reflected, str(r.status_code), len(r.text))
        if reflected:
            print(f"[SIGNATURE-HIT] {signature_payload}")
    except Exception as e:
        print(f"[!] Greška sa signature payloadom: {e}")

    if not base_url:
        print("[!] Meta nije pronađena.")
        return

    payloads = get_payloads()
    total_hits = 0

    for tip, plist in payloads.items():
        hits = run_payloads(target_id, base_url, tip, plist)
        total_hits += hits

        if hits == 0:
            print(f"[!] Nema pogodaka za {tip}... pokušavam mutacije")
            mutations = get_mutations(tip)
            if mutations:
                mhits = run_payloads(target_id, base_url, tip, mutations)
                total_hits += mhits

    advisor(target_id)
    print("[*] Generišem izveštaj...")
    generate_report(target_id)

if __name__ == "__main__":
    print("\n[+] Dostupne mete:")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    targets = c.fetchall()
    conn.close()
    for tid, url in targets:
        print(f"[{tid}] {url}")

    izbor = int(input("\n[?] Izaberi ID mete za AutoMod sekvencu: "))
    run_auto(izbor)
