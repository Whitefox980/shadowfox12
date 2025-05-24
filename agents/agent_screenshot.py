import sqlite3
import sys
import os
from datetime import datetime
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

DB_PATH = "shadowfox.db"
OUTPUT_DIR = "screenshots"

def get_targets():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    targets = c.fetchall()
    conn.close()
    return targets

def get_hits(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT payload_type, payload FROM scan_results
        WHERE target_id = ? AND reflected = 1
    """, (target_id,))
    hits = c.fetchall()
    conn.close()
    return hits

def capture(url, filename):
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    options = Options()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')

    driver = webdriver.Chrome(options=options)
    driver.get(url)
    driver.save_screenshot(filename)
    driver.quit()

def run():
    targets = get_targets()
    print("\n[+] Dostupne mete:")
    for tid, url in targets:
        print(f"[{tid}] {url}")

    izbor = int(input("\n[?] Izaberi ID mete za screenshot HIT payload-a: "))
    base_url = [url for tid, url in targets if tid == izbor][0]
    hits = get_hits(izbor)

    if not hits:
        print("[!] Nema reflektovanih HIT-ova za ovu metu.")
        return

    for tip, payload in hits:
        full_url = f"{base_url}?test={quote(payload)}"
        fname = f"{OUTPUT_DIR}/target{izbor}_{tip}_{datetime.now().strftime('%H%M%S')}.png"
        print(f"[+] Slikam: {full_url}")
        capture(full_url, fname)
        print(f"[✓] Screenshot sačuvan: {fname}")

if __name__ == "__main__":
    run()
