import os, json, shutil, hashlib, zipfile
from tools.shadowfox_config import get_path

DOMAIN = "target"  # možeš menjati
BASE_DIR = f"proof_pack_{DOMAIN}"
PDF = get_path("reports") + "/ShadowFox_Report.pdf"
HTML_DIR = get_path("reports") + "/replay_ai"
IMG_DIR = get_path("reports") + "/replay_ai_screens"
LOGFILE = get_path("logs") + "/shadowfuzz_ai.jsonl"
ZIP_NAME = f"{BASE_DIR}.zip"

def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        h.update(f.read())
    return h.hexdigest()

def build_proof_pack():
    print(f"[*] Pripremam proof paket: {BASE_DIR}/")
    os.makedirs(BASE_DIR, exist_ok=True)

    files = []

    # Kopiraj PDF
    if os.path.exists(PDF):
        shutil.copy(PDF, BASE_DIR)
        files.append(os.path.join(BASE_DIR, os.path.basename(PDF)))

    # Kopiraj HTML replay
    if os.path.exists(HTML_DIR):
        for f in os.listdir(HTML_DIR):
            if f.endswith(".html"):
                shutil.copy(os.path.join(HTML_DIR, f), BASE_DIR)
                files.append(os.path.join(BASE_DIR, f))

    # Kopiraj slike
    if os.path.exists(IMG_DIR):
        for f in os.listdir(IMG_DIR):
            if f.endswith(".png"):
                shutil.copy(os.path.join(IMG_DIR, f), BASE_DIR)
                files.append(os.path.join(BASE_DIR, f))

    # Upis hash-eva
    with open(os.path.join(BASE_DIR, "hashes.txt"), "w") as out:
        for f in files:
            out.write(f"{os.path.basename(f)}: {sha256sum(f)}\n")

    # Summary JSON
    if os.path.exists(LOGFILE):
        with open(LOGFILE, "r") as f:
            entries = [json.loads(line) for line in f if '"reflected": true' in line]
        with open(os.path.join(BASE_DIR, "proof_summary.json"), "w") as out:
            json.dump(entries, out, indent=2)

    # ZIP-uj sve
    with zipfile.ZipFile(ZIP_NAME, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in os.listdir(BASE_DIR):
            zipf.write(os.path.join(BASE_DIR, f), arcname=f)

    print(f"[✓] Paket spakovan: {ZIP_NAME}")
