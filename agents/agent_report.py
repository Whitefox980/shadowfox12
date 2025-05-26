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
from fpdf import FPDF
from datetime import datetime

def create_pdf_report(target_id):
    scanovi = izlistaj_scanove(target_id)
    if not scanovi:
        print("[!] Nema skenova za zadati ID.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_text_color(0, 255, 0)
    pdf.cell(200, 10, txt="ShadowFox AI - Vulnerability Report", ln=True, align="C")
    pdf.set_text_color(255, 255, 255)

    for s in scanovi:
        tip, payload, ref, code, size, t = s
        oznaka = "[HIT]" if ref else "[INFO]"
        line = f"{oznaka} [{tip}] {payload} | Code: {code} | Size: {size}B | Time: {t}"
        pdf.cell(200, 10, txt=line, ln=True)

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = f"reports/report_target_{target_id}_{now}.pdf"
    pdf.output(path)

    print(f"[+] PDF sačuvan: {path}")
if __name__ == "__main__":
    run()
