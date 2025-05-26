from html2image import Html2Image
import os

def screenshot_proof(html_file, output_file):
    try:
        hti = Html2Image(output_path=os.path.dirname(output_file))
        full_path = os.path.abspath(html_file)
        filename = os.path.basename(output_file)
        hti.screenshot(html_file=full_path, save_as=filename, size=(1280, 800))
        print(f"[✓] Screenshot snimljen u: {output_file}")
    except Exception as e:
        print(f"[!] Greška pri snimanju slike: {e}")
