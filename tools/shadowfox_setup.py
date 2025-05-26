import json
import os

DEFAULT_CONFIG = {
    "paths": {
        "logs": "logs",
        "intel": "intel",
        "recon_data": "recon_data",
        "reports": "reports",
        "replay": "reports/replay",
        "db": "intel/intel.db",
        "payloads": "payloads/top_payloads.json"
    },
    "project": "ShadowFox12",
    "version": "1.0",
    "default_logfile": "logs/fuzz_results.jsonl"
}

def setup():
    for path in DEFAULT_CONFIG["paths"].values():
        dir_path = path if not path.endswith(".db") and not path.endswith(".json") else os.path.dirname(path)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
    with open("shadowfox.config.json", "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)

    print("[✓] ShadowFox config postavljen.")
    print("[+] Folderi kreirani:")
    for k, v in DEFAULT_CONFIG["paths"].items():
        print(f" - {k}: {v}")

if __name__ == "__main__":
    setup()
