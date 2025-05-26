import json
import os
from collections import defaultdict
from tools.shadowfox_config import get_path

LOGS_PATH = get_path("logs")
OUTPUT = get_path("intel") + "/ai_hits_summary.json"

def evaluate_fuzz_logs():
    print("[*] Pokrećem AI evaluaciju fuzz logova...")

    summary = defaultdict(list)

    for file in os.listdir(LOGS_PATH):
        if file.endswith(".jsonl"):
            full_path = os.path.join(LOGS_PATH, file)
            with open(full_path, "r") as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        if data.get("reflected") or data.get("status") == 200 and data.get("length", 0) > 1000:
                            category = data.get("category", "unknown")
                            summary[category].append(data)
                    except:
                        continue

    # Analiza
    result = {k: len(v) for k, v in summary.items()}
    print("[AI] Detekcija po tipu:")
    for k, v in result.items():
        print(f" → {k}: {v} uspešnih")

    # Upis
    with open(OUTPUT, "w") as out:
        json.dump(summary, out, indent=2)

    print(f"[✓] AI summary sačuvan u: {OUTPUT}")
