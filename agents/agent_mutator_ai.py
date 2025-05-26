import json
import os
import random
import urllib.parse
from tools.shadowfox_config import get_path

INPUT = get_path("intel") + "/ai_hits_summary.json"
OUTPUT = get_path("payloads").replace("top_", "mutated_")

def mutate(payload):
    variants = []

    # URL encode
    variants.append(urllib.parse.quote(payload))

    # HTML encoded
    variants.append(payload.replace("<", "&lt;").replace(">", "&gt;"))

    # Obfuscated
    variants.append(payload.replace("script", "scr<script>ipt"))

    # Unicode obfuscation
    variants.append(payload.replace("a", "\\u0061"))

    # Inline comment bypass
    variants.append(payload.replace("alert", "al<!--comment-->ert"))

    return list(set(variants))

def generate_mutated_payloads():
    print("[*] Mutiram payload-e iz AI evaluacije...")

    if not os.path.exists(INPUT):
        print("[!] Nema AI evaluacije.")
        return

    with open(INPUT, "r") as f:
        data = json.load(f)

    all_payloads = set()
    for category in data:
        for item in data[category]:
            payload = item.get("payload") or item["url"].split("q=")[-1]
            all_payloads.add(payload)

    mutated = []
    for p in all_payloads:
        m = mutate(p)
        for var in m:
            mutated.append({"original": p, "mutated": var})

    with open(OUTPUT, "w") as out:
        json.dump(mutated, out, indent=2)

    print(f"[✓] Mutacija završena. Sačuvano: {len(mutated)} → {OUTPUT}")
