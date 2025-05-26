import os
from PIL import Image, ImageDraw, ImageFont
from tools.shadowfox_config import get_path

IMG_DIR = get_path("reports") + "/replay_ai_screens"
MARK = "Chupko was here.. H1:Whitefox980"
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # menjaš ako koristiš nešto drugo

def add_watermark():
    if not os.path.exists(IMG_DIR):
        print("[!] Folder sa screenshot-ima ne postoji.")
        return

    files = [f for f in os.listdir(IMG_DIR) if f.endswith(".png")]
    if not files:
        print("[!] Nema screenshotova za watermark.")
        return

    for i, file in enumerate(files, 1):
        path = os.path.join(IMG_DIR, file)
        try:
            img = Image.open(path).convert("RGBA")
            txt_layer = Image.new("RGBA", img.size, (255,255,255,0))
            draw = ImageDraw.Draw(txt_layer)
            font = ImageFont.truetype(FONT_PATH, 20)

            # Bottom left ugao
            draw.text((10, img.size[1] - 30), MARK, font=font, fill=(255, 0, 0, 180))

            out = Image.alpha_composite(img, txt_layer)
            out.convert("RGB").save(path)
            print(f"[✓] Watermark dodat → {file}")
        except Exception as e:
            print(f"[!] Greška za {file}: {e}")

    print("[✓] Svi screenshotovi su potpisani.")
