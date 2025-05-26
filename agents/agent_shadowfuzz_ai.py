import sqlite3, json, requests, time
from urllib.parse import urlencode, urljoin
from tools.shadowfox_config import get_path
from core.shadow_logger import log_result

DB_PATH = get_path("db")
PAYLOADS_PATH = get_path("payloads").replace("top_", "mutated_")
LOGFILE = get_path("logs") + "/shadowfuzz_ai.jsonl"

def load_endpoints(domain):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT endpoint FROM endpoints WHERE domain=?", (domain,))
    endpoints = [row[0] for row in c.fetchall()]
    conn.close()
    return list(set(endpoints))

def load_payloads():
    with open(PAYLOADS_PATH, "r") as f:
        return json.load(f)

def run_shadowfuzz(domain, base_url):
    print(f"[*] ShadowFuzz AI aktiviran za: {domain}")
    endpoints = load_endpoints(domain)
    payloads = load_payloads()

    if not endpoints or not payloads:
        print("[!] Nema endpointa ili payload-a.")
        return

    total = len(endpoints) * len(payloads)
    count = 0

    for ep in endpoints:
        full_ep = urljoin(base_url, ep)
        for item in payloads:
            count += 1
            mutated = item["mutated"]
            full_url = f"{full_ep}?q={mutated}"
            try:
                r = requests.get(full_url, timeout=10)
                result = {
                    "url": full_url,
                    "status": r.status_code,
                    "length": len(r.text),
                    "reflected": mutated in r.text,
                    "original": item["original"],
                    "mutated": mutated
                }
                log_result(LOGFILE, result)
                if result["reflected"]:
                    print(f"[{count}/{total}] [✓] REFLECTED → {full_url}")
                elif r.status_code in [403, 500]:
                    print(f"[{count}/{total}] [!] STATUS {r.status_code} → {full_url}")
            except Exception as e:
                continue
            time.sleep(0.2)

    print(f"[✓] ShadowFuzz AI napad završen. Rezultati: {LOGFILE}")
