import requests
import socket
import time
from bs4 import BeautifulSoup
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core import db_insert

TARGETS_FILE = "data/targets.txt"

import subprocess

def find_js_files(domain):
    cmd = f"gau {domain} | grep '\\.js'"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.strip().split("\n")
        for line in lines:
            if line:
                print(f"[JS] {line}")
    except Exception as e:
        print(f"[ERROR] {e}")
def ucitaj_mete():
    if not os.path.exists(TARGETS_FILE):
        print(f"[!] Fajl ne postoji: {TARGETS_FILE}")
        return []
    with open(TARGETS_FILE, "r") as f:
        return [line.strip() for line in f if line.strip()]

def analiziraj(url):
    try:
        start = time.time()
        head = requests.head(url, timeout=5, allow_redirects=True)
        html = requests.get(url, timeout=5).text
        title = BeautifulSoup(html, "html.parser").title
        naslov = title.text.strip() if title else "N/A"
        ip = socket.gethostbyname(url.replace("https://", "").replace("http://", "").split("/")[0])
        trajanje = round(time.time() - start, 2)

        db_insert.insert_target(url, ip, str(head.status_code), naslov)
        print(f"[+] {url} | {ip} | {head.status_code} | {naslov} | {trajanje}s")
    except Exception as e:
        print(f"[-] {url} | GREŠKA: {e}")

def run():
    mete = ucitaj_mete()
    for m in mete:
        analiziraj(m)

if __name__ == "__main__":
    run()
