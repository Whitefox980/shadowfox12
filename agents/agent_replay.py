import requests
import sqlite3
import sys
import os
from urllib.parse import quote
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DB_PATH = "shadowfox.db"
OUTPUT_DIR = "replay"

def get_targets():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    rows = c.fetchall()
    conn.close()
    return rows

def get_payloads(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT id, payload_type, payload FROM scan_results
        WHERE target_id = ?
    """, (target_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def replay(target_id, base_url, payload):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    full_url = f"{base_url}?test={quote(payload)}"
    try:
        r = requests.get(full_url, timeout=6)
        html_file = f"{OUTPUT_DIR}/replay_{target_id}_{datetime.now().strftime('%H%M%S')}.html"
        with open(html_file, "w", encoding="utf-8") as f:
            f.write(r.text)
        print(f"[+] Snimljen HTML odgovor: {html_file}")
        print(f"[i] Status: {r.status_code} | Length: {len(r.text)}\n")
    except Exception as e:
        print(f"[!] Greška prilikom replay-a: {e}")

def run():
    targets = get_targets()
    print("\n[+] Dostupne mete:")
    for tid, url in targets:
        print(f"[{tid}] {url}")

    izbor = int(input("\n[?] Izaberi ID mete: "))
    payloads = get_payloads(izbor)
    if not payloads:
        print("[!] Nema payload-a za ovu metu.")
        return

    print("\n[+] Payload-i za replay:")
    for idx, (pid, ptype, pval) in enumerate(payloads):
        print(f"[{idx+1}] {ptype}: {pval}")

    pidx = int(input("\n[?] Izaberi payload za replay: ")) - 1
    payload = payloads[pidx][2]
    base_url = [url for tid, url in targets if tid == izbor][0]
    replay(izbor, base_url, payload)

if __name__ == "__main__":
    run()
