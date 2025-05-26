import os
from html2image import Html2Image
from tools.shadowfox_config import get_path

INPUT_DIR = get_path("reports") + "/replay_ai"
OUTPUT_DIR = get_path("reports") + "/replay_ai_screens"

def generate_screenshots():
    if not os.path.exists(INPUT_DIR):
        print("[!] Replay AI folder ne postoji.")
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    hti = Html2Image(output_path=OUTPUT_DIR)

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".html")]
    total = len(files)
    print(f"[*] Generišem screenshot-ove za {total} replay fajlova...")

    for i, file in enumerate(files, 1):
        full_path = os.path.join(INPUT_DIR, file)
        try:
            hti.screenshot(html_file=full_path, save_as=file.replace(".html", ".png"))
            print(f"[{i}/{total}] ✓ Screenshot → {file.replace('.html', '.png')}")
        except Exception as e:
            print(f"[{i}/{total}] [!] Greška: {e}")

    print(f"[✓] Screenshot generacija završena → {OUTPUT_DIR}")
