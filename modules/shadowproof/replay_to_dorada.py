import json
import os

INPUT_LOG = "signature_log.json"
OUTPUT_FILE = "todo_targets.json"

def extract_failed_targets():
    if not os.path.exists(INPUT_LOG):
        print("[!] Nema log fajla.")
        return []

    with open(INPUT_LOG, "r") as f:
        logs = json.load(f)

    targets = []
    for entry in logs:
        if not entry.get("reflected") and not entry.get("potential_exploit", False):
            base_url = entry["url"].split("?")[0]
            targets.append({
                "url": base_url,
                "reason": "No reflection or exploit detected",
                "payload": entry["payload"]
            })

    return targets

def save_dorada(targets):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(targets, f, indent=2)
    print(f"[✓] Prebačeno {len(targets)} meta za doradu → {OUTPUT_FILE}")

if __name__ == "__main__":
    t = extract_failed_targets()
    save_dorada(t)
