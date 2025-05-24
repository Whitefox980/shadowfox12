import sqlite3
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DB_PATH = "shadowfox.db"

def prikazi_mete():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    rezultati = c.fetchall()
    conn.close()
    return rezultati

def izlistaj_scanove(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT payload_type, payload, reflected, status_code, response_size, timestamp
        FROM scan_results WHERE target_id = ?
    """, (target_id,))
    rezultati = c.fetchall()
    conn.close()
    return rezultati

def run():
    mete = prikazi_mete()
    print("\n[+] Dostupne mete:")
    for id_, url in mete:
        print(f"[{id_}] {url}")

    izbor = int(input("\n[?] Izaberi ID mete: "))
    skenovi = izlistaj_scanove(izbor)

    print(f"\n[+] Rezultati za metu {izbor}:\n")
    for s in skenovi:
        tip, payload, ref, code, size, t = s
        oznaka = "[HIT]" if ref else "     "
        print(f"{oznaka} [{tip}] {payload} | {code} | {size}B | {t}")

if __name__ == "__main__":
    run()
