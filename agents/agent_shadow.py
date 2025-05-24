import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import requests
import sqlite3
from urllib.parse import quote
from core import db_insert

DB_PATH = "shadowfox.db"

def uzmi_mete():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    mete = c.fetchall()
    conn.close()
    return mete

def uzmi_payloade(tip):
    with open("payloads/payload_zahoor_db.json", "r") as f:
        import json
        data = json.load(f)
    return data.get(tip, [])

def napadni(target_id, url, payload_type, payload_list):
    print(f"\n[*] Napadam metu: {url} | Tip: {payload_type}")
    for payload in payload_list:
        try:
            test_url = f"{url}?test={quote(payload)}"
            r = requests.get(test_url, timeout=5)
            reflected = 1 if payload in r.text else 0
            print(f"[DEBUG] Insertujem za {target_id} | {payload}")
            db_insert.insert_scan_result(
                target_id, payload_type, payload,
                reflected, str(r.status_code), len(r.text)
            )
            if reflected:
                print(f"[+] Reflektovan payload: {payload}")
        except Exception as e:
            print(f"[-] Greška: {e}")

def start_manual():
    mete = uzmi_mete()
    if not mete:
        print("[!] Nema meta.")
        return

    print("\n[+] Dostupne mete:\n")
    for mid, murl in mete:
        print(f"[{mid}] {murl}")

    izbor = int(input("\n[?] Izaberi ID mete: "))
    tip = input("[?] Tip payloada (XSS, SQLi, LFI...): ").strip()

    payloadi = uzmi_payloade(tip)
    if not payloadi:
        print("[!] Nema payloada tog tipa.")
        return

    url = [u for (i, u) in mete if i == izbor][0]
    napadni(izbor, url, tip, payloadi)

if __name__ == "__main__":
    start_manual()
