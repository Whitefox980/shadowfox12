import json
import os
from urllib.parse import unquote, urlparse, parse_qs
from collections import Counter
from tools.shadowfox_config import get_logfile, get_path

def extract_top_payloads():
    logfile = get_logfile()
    payloads_out = get_path("payloads")
    counter = Counter()

    if not os.path.exists(logfile):
        print(f"[!] Log fajl nije pronađen: {logfile}")
        return

    with open(logfile, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get("status") == 200 and data.get("reflected"):
                    parsed_url = urlparse(data["url"])
                    q = parse_qs(parsed_url.query).get("q")
                    if q:
                        payload = unquote(q[0])
                        counter[payload] += 1
            except:
                continue

    top_payloads = [{"payload": k, "reflected_count": v} for k, v in counter.items()]
    os.makedirs(os.path.dirname(payloads_out), exist_ok=True)
    with open(payloads_out, "w") as out:
        json.dump(top_payloads, out, indent=2)

    print(f"[✓] Sačuvano {len(top_payloads)} top payload-a u: {payloads_out}")
