import os
from datetime import datetime

LOG_FILE = "logs/bounce_log.txt"

def prikazi_logove():
    if not os.path.exists(LOG_FILE):
        print("[!] Nema bounce logova još.")
        return

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    print("\n[+] Prikaz svih detektovanih bounce callbackova:\n")

    for line in lines:
        print(line.strip())

    print(f"\n[✓] Ukupno: {len(lines)} zahteva.\n")

def filtriraj_po_ip(ip):
    with open(LOG_FILE, "r") as f:
        matches = [l for l in f if ip in l]

    print(f"\n[+] Filter za IP: {ip}")
    for line in matches:
        print(line.strip())

def run():
    prikazi_logove()
    q = input("\n[?] Želiš da filtriraš po IP? (da/ne): ").strip().lower()
    if q == "da":
        ip = input("[?] Unesi IP: ")
        filtriraj_po_ip(ip)

if __name__ == "__main__":
    run()
