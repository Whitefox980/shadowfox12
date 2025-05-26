import json
import os

CONFIG_FILE = "shadowfox.config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError("Config nije pronađen. Pokreni setup.")
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def get_path(key):
    cfg = load_config()
    return cfg["paths"].get(key, "")

def get_logfile():
    cfg = load_config()
    return cfg.get("default_logfile", "logs/fuzz_results.jsonl")
