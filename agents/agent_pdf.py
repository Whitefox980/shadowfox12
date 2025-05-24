import sqlite3
from fpdf import FPDF
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
DB_PATH = "shadowfox.db"
OUTPUT_DIR = "reports"

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "ShadowFox Report", border=False, ln=1, align="C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def prikazi_mete():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    mete = c.fetchall()
    conn.close()
    print("\n[+] Dostupne mete:")
    for tid, url in mete:
        print(f"[{tid}] {url}")
    return [tid for tid, _ in mete]

def get_target_info(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT url, ip, status, title FROM targets WHERE id = ?", (target_id,))
    result = c.fetchone()
    conn.close()
    return result

def get_results(target_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT payload_type, payload, reflected, status_code, response_size, timestamp
        FROM scan_results WHERE target_id = ?
    """, (target_id,))
    results = c.fetchall()
    conn.close()
    return results

def generate_pdf(target_id):
    info = get_target_info(target_id)
    results = get_results(target_id)

    if not info or not results:
        print("[!] Nema podataka za izveštaj.")
        return

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    url, ip, status, title = info

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(0, 10, f"Target: {url}", ln=1)
    pdf.cell(0, 10, f"IP: {ip} | Status: {status}", ln=1)
    pdf.cell(0, 10, f"Title: {title}", ln=1)
    pdf.ln(5)

    for r in results:
        tip, payload, refl, code, size, t = r
        oznaka = "[HIT]" if refl else "     "
        pdf.multi_cell(0, 8, f"{oznaka} {t} | {tip} | {payload} | {code} | {size}B", border=0)
        pdf.ln(1)

    filename = f"{OUTPUT_DIR}/report_target_{target_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    print(f"[+] PDF izveštaj sačuvan: {filename}")

if __name__ == "__main__":
    dostupni = prikazi_mete()
    izbor = input("\n[?] Izaberi ID mete za PDF: ")
    if int(izbor) in dostupni:
        generate_pdf(int(izbor))
    else:
        print("[!] Neispravan ID.")
