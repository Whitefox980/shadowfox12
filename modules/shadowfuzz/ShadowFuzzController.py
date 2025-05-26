from mutator_engine import mutate_payload
from signature_tracker_lib import test_reflection
from proof_writer import save_proof
import json
import os
from datetime import datetime
from screenshot_maker import screenshot_proof

TARGET = input("Meta (npr. https://site.com/search?q=): ").strip()
BASE_PAYLOAD = input("Osnovni payload (npr. <script>alert(1)</script>): ").strip()

os.makedirs("proofs", exist_ok=True)

mutated_payloads = mutate_payload(BASE_PAYLOAD)
log_data = []

print(f"\n[+] Generisanih mutacija: {len(mutated_payloads)}\n")

for payload in mutated_payloads:
    full_url = TARGET + payload
    print(f"[>] Testiram: {full_url}")
    result = test_reflection(full_url, payload)

    if result["reflected"] or result["potential_exploit"]:
        proof_path = save_proof(result["url"], result["payload"], result["response"], result.get("potential_exploit", False))
        print(f"[✓] POTENCIJALNI HIT! → Snimljen dokaz: {proof_path}")
        result["proof"] = proof_path

        png_path = proof_path.replace(".html", ".png")
        print(f"[+] Snimam screenshot → {png_path}")
        screenshot_proof(proof_path, png_path)
    else:
        print("[-] Nema refleksije ni exploita.")

    log_data.append(result)

# Logovanje
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = f"controller_log_{timestamp}.json"
with open(log_file, "w") as f:
    json.dump(log_data, f, indent=2)

print(f"\n[✓] Sken završio. Log: {log_file}")
