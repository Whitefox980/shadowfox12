import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time, json

# Ispravno:

from tools.zip_utils import create_zip
from core.shadow_mutator import mutate_payload
from agent_shadow import test_reflection
from agents.agent_replay import generate_replay
from agents.agent_report import create_pdf_report
from tools.shadowfox_config import get_path
from agents.agent_replay import export
generate_replay = export()

PAYLOADS = json.load(open("payloads/top_payloads.json"))

import sqlite3

def load_targets():
    conn = sqlite3.connect("shadowfox.db")
    c = conn.cursor()
    c.execute("SELECT url FROM targets")
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

TARGETS = load_targets()
LOG_FILE = get_path("logs") + "/shadowfuzz_ai.jsonl"

def log_entry(data):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def run_cron():
    for payload_type, payload_list in PAYLOADS.items():
        for payload in payload_list:
            for target in TARGETS:
                url = f"{target}?q={payload}"
                try:
                    result = test_reflection(url, payload)

                    log = {
                        "url": url,
                        "payload_type": payload_type,
                        "payload": payload,
                        "status": result.get("status") if isinstance(result, dict) else "N/A",
                        "length": result.get("length") if isinstance(result, dict) else 0,
                        "reflected": result.get("reflected", False) if isinstance(result, dict) else False
                    }
                    log_entry(log)

                    if result.get("reflected"):
                        generate_replay(url, payload)
                        create_pdf_report(target)
                        create_zip(target)

                    time.sleep(2)
                except Exception as e:
                    log_entry({"url": url, "payload": payload, "error": str(e)})
    time.sleep(5)

if __name__ == "__main__":
    while True:
        run_cron()
