import sqlite3
import os
from time import sleep
from datetime import datetime

DB_PATH = "shadowfox.db"
BOUNCE_LOG = "logs/bounce_log.txt"

def prikazi_mete():
    print("\n[+] Liste meta:")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    for tid, url in c.fetchall():
        print(f"[{tid}] {url}")
    conn.close()

def poslednji_rezultati():
    print("\n[+] Poslednjih 5 pogodaka:")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT target_id, payload_type, payload, reflected, status_code, timestamp
        FROM scan_results ORDER BY timestamp DESC LIMIT 5
    """)
    rows = c.fetchall()
    for row in rows:
        print(f"MetaID:{row[0]} | {row[1]} | Status:{row[4]} | HIT:{'YES' if row[3] else 'NO'} | {row[2][:40]}...")
    conn.close()

def bounce_log_pregled():
    if not os.path.exists(BOUNCE_LOG):
        print("[!] Nema bounce logova.")
        return
    print("\n[+] Poslednji bounce logovi:")
    with open(BOUNCE_LOG, "r") as f:
        lines = f.readlines()[-5:]
        for l in lines:
            print(l.strip())

def pokreni_agenta():
    print("\n[+] Pokreni agenta:")
    print("[1] agent_shadowx (AutoMod)")
    print("[2] agent_recon")
    print("[3] agent_mutant")
    print("[4] agent_report")
    print("[5] agent_listener")
    print("[6] agent_advisor")
    print("[7] agent_replay")
    izbor = input("\n[?] Unesi broj agenta: ").strip()

    agent_map = {
        "1": "agent_shadowx.py",
        "2": "agent_recon.py",
        "3": "agent_mutant.py",
        "4": "agent_report.py",
        "5": "listener.py",
        "6": "agent_advisor.py",
        "7": "agent_replay.py"
    }

    agent = agent_map.get(izbor)
    if agent:
        os.system(f"python3 agents/{agent}" if agent != "listener.py" else f"python3 {agent}")
    else:
        print("[!] Nepoznat izbor.")

def operator_meni():
    while True:
        print("\n==== ShadowFox Operator Terminal ====")
        print("[1] Prikaži mete")
        print("[2] Poslednjih 5 rezultata")
        print("[3] Pregled bounce loga")
        print("[4] Pokreni agenta")
        print("[5] Izlaz")

        cmd = input("\n[?] Izbor: ").strip()

        if cmd == "1":
            prikazi_mete()
        elif cmd == "2":
            poslednji_rezultati()
        elif cmd == "3":
            bounce_log_pregled()
        elif cmd == "4":
            pokreni_agenta()
        elif cmd == "5":
            print("[✓] Izlaz iz Operatora.")
            break
        else:
            print("[!] Nepoznata komanda.")

if __name__ == "__main__":
    operator_meni()
