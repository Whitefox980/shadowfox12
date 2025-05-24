import requests
import socket
import time
from bs4 import BeautifulSoup
import os

TARGETS_FILE = "data/targets.txt"

def ucitaj_mete():
    if not os.path.exists(TARGETS_FILE):
        print(f"[!] Fajl ne postoji: {TARGETS_FILE}")
        return []
    with open(TARGETS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def proveri_metu(url):
    try:
        start = time.time()
        r = requests.head(url, timeout=5, allow_redirects=True)
        trajanje = round(time.time() - start, 2)

        html = requests.get(url, timeout=5).text
        title = BeautifulSoup(html, "html.parser").title
        naslov = title.text.strip() if title else "N/A"

        ip = socket.gethostbyname(url.replace("http://", "").replace("https://", "").split("/")[0])
        return {
            "url": url,
            "status": r.status_code,
            "ip": ip,
            "title": naslov,
            "response_time": trajanje
        }
    except Exception as e:
        return {
            "url": url,
            "status": "ERR",
            "ip": "N/A",
            "title": "N/A",
            "response_time": "Timeout"
        }

def prikazi_izvestaj(lista):
    print("\n[+] Izveštaj o metama:\n")
    for meta in lista:
        print(f"- {meta['url']}  [{meta['status']}]")
        print(f"    IP: {meta['ip']} | TITLE: {meta['title']} | {meta['response_time']}s")
        print()

if __name__ == "__main__":
    mete = ucitaj_mete()
    if not mete:
        print("[!] Nema meta.")
        exit()

    rezultati = []
    for url in mete:
        print(f"[~] Proveravam: {url}")
        rezultati.append(proveri_metu(url))

    prikazi_izvestaj(rezultati)
