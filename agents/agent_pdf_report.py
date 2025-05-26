import os, json
from fpdf import FPDF
from tools.shadowfox_config import get_path

REPLAY_JSON = get_path("logs") + "/shadowfuzz_ai.jsonl"
SCREENSHOT_DIR = get_path("reports") + "/replay_ai_screens"
OUTPUT_PDF = get_path("reports") + "/ShadowFox_Report.pdf"

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "ShadowFox AI Report", 0, 1, "C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_pdf_report():
    if not os.path.exists(REPLAY_JSON):
        print("[!] Nema AI fuzz loga.")
        return

    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    with open(REPLAY_JSON, "r") as f:
        for i, line in enumerate(f):
            try:
                data = json.loads(line)
                if data.get("reflected"):
                    pdf.set_font("Arial", "B", 11)
                    pdf.multi_cell(0, 10, f"[{i+1}] {data['url']}", 0)

                    pdf.set_font("Arial", "", 10)
                    pdf.multi_cell(0, 8, f"Status: {data['status']}")
                    pdf.multi_cell(0, 8, f"Original: {data['original']}")
                    pdf.multi_cell(0, 8, f"Mutated: {data['mutated']}")

                    img_path = os.path.join(SCREENSHOT_DIR, f"proof_ai_{i+1}.png")
                    if os.path.exists(img_path):
                        try:
                            pdf.image(img_path, w=100)
                        except:
                            pdf.cell(0, 8, "[!] Screenshot nije mogao da se ubaci.", ln=1)

                    pdf.ln(10)
            except:
                continue

    pdf.output(OUTPUT_PDF)
    print(f"[✓] PDF izveštaj sačuvan: {OUTPUT_PDF}")
