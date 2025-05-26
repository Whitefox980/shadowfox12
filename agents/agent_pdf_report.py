from fpdf import FPDF
import sqlite3
from datetime import datetime

def generate_pdf(payload_type='SSRF', output_path=None):
    conn = sqlite3.connect("shadowfox.db")
    c = conn.cursor()
    c.execute("""
        SELECT payload, reflected, status_code, response_size, timestamp
        FROM scan_results
        WHERE payload_type=? AND reflected=1
        ORDER BY id DESC
    """, (payload_type,))
    results = c.fetchall()
    conn.close()

    if not results:
        print(f"[ok] Nema reflektovanih pogodaka za tip: {payload_type}")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 255, 0)
    pdf.cell(200, 10, txt=f"ShadowFox Report - {payload_type} Hits", ln=True, align="C")
    pdf.set_text_color(255, 255, 255)

    for payload, reflected, status, size, timestamp in results:
        line = f"[ok] {payload} | Status: {status} | Size: {size} | Time: {timestamp}"
        pdf.cell(200, 10, txt=line, ln=True)

    if not output_path:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"reports/report_{payload_type}_{timestamp}.pdf"

    pdf.output(output_path)
    print(f"[ok] PDF sačuvan: {output_path}")
if __name__ == "__main__":
    generate_pdf()
