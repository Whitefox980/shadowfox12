import requests
import json
import os
from datetime import datetime

# Podesi
TARGET = input("Unesi metu (npr. https://target.com/search?q=): ").strip()
PAYLOAD_FILE = "signature_payloads.txt"
PROOF_DIR = "proofs"
LOG_FILE = "signature_log.json"

os.makedirs(PROOF_DIR, exist_ok=True)

with open(PAYLOAD_FILE, "r") as f:
    payloads = [line.strip() for line in f if line.strip()]

log_data = []

for payload in payloads:
    full_url = TARGET + payload
    print(f"[>] Testiram: {full_url}")

    try:
        r = requests.get(full_url, timeout=10)
        reflected = payload in r.text
        status = r.status_code
        size = len(r.content)
        timestamp = datetime.now().isoformat()

        entry = {
            "url": full_url,
            "payload": payload,
            "reflected": reflected,
            "status_code": status,
            "response_size": size,
            "timestamp": timestamp
        }

        log_data.append(entry)

        if reflected:
            proof_file = f"{PROOF_DIR}/proof_{timestamp.replace(':','_')}.html"
            with open(proof_file, "w") as f_out:
                f_out.write(f"""
<html><body style='background:#000;color:#0f0;font-family:monospace;padding:20px;'>
<h1>Čupko was here.</h1>
<h2>H1: Whitefox980 Team</h2>
<hr>
<p><b>Target:</b> {full_url}</p>
<p><b>Status:</b> {status} | <b>Size:</b> {size} bytes</p>
<p><b>Payload:</b> <code>{payload}</code></p>
<hr>
<pre>{r.text[:1000]}</pre>
</body></html>
""")
            print(f"[✓] Refleksija pronađena – sačuvan dokaz u: {proof_file}")
        else:
            print("[–] Nije reflektovano.")

    except Exception as e:
        print(f"[!] Greška: {e}")

# Upis u JSON log
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        existing = json.load(f)
else:
    existing = []

with open(LOG_FILE, "w") as f:
    json.dump(existing + log_data, f, indent=2)

print("\n[✓] Gotovo. Logovanih testova:", len(log_data))
