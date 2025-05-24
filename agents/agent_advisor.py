import sqlite3
import sys
import os
from collections import Counter

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DB_PATH = "shadowfox.db"

def get_targets():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    targets = c.fetchall()
    conn.close()
    return targets

def analyze_results(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT payload_type, reflected, status_code, response_size
        FROM scan_results WHERE target_id = ?
    """, (target_id,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print("[!] Nema rezultata za ovu metu.")
        return

    type_counter = Counter([row[0] for row in rows])
    reflected_hits = [row for row in rows if row[1] == 1]
    large_responses = [row for row in rows if row[3] and row[3] > 10000]

    print("\n[AI ADVISOR] Analiza rezultata:")
    print("-" * 40)
    print(f"[+] Broj payloada po tipu: {dict(type_counter)}")
    print(f"[+] Reflektovanih pogodaka: {len(reflected_hits)}")
    print(f"[+] Veliki response size (>10KB): {len(large_responses)}")
    print()

    if not reflected_hits:
        print("[!] Nema refleksija — moguće WAF ili filtering. Probaj mutacije ili header injection.")
    if len(large_responses) > 0:
        print("[!] Detektovan output leakage — pogledaj raw odgovore (Replay modul).")
    if "SSRF" in type_counter and type_counter["SSRF"] > 0:
        print("[*] Ako SSRF nije uspešan, probaj lokalne IP-e sa bypass payloadima.")
    if "SQLi" in type_counter and len(reflected_hits) == 0:
        print("[*] SQLi payloadi nisu reflektovani — probaj time-based (SLEEP, BENCHMARK).")

def run():
    targets = get_targets()
    print("\n[+] Dostupne mete:")
    for tid, turl in targets:
        print(f"[{tid}] {turl}")

    izbor = int(input("\n[?] Izaberi ID mete: "))
    analyze_results(izbor)

if __name__ == "__main__":
    run()
