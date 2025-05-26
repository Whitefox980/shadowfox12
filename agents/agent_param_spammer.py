import requests
import json
import random
from urllib.parse import urlencode
from tools.shadowfox_config import get_path
from core.shadow_logger import log_result

# Parametri po tipu
PARAMS = {
    "XSS": ["q", "search", "input", "s", "term", "query"],
    "LFI": ["file", "page", "path", "doc", "template", "inc"],
    "SSRF": ["url", "next", "dest", "target", "domain", "feed"],
    "RCE": ["cmd", "exec", "run", "query", "load", "function"]
}

# Fajl payload-a
TOP_PAYLOADS_PATH = get_path("payloads")
OUTPUT_LOG = get_path("logs") + "/param_spammer_results.jsonl"

def spam_parameters(domain, base_url):
    print(f"[*] Pokrećem ParamSpammer na metu: {domain}")
    
    try:
        with open(TOP_PAYLOADS_PATH, "r") as f:
            payloads = json.load(f)
    except:
        print("[!] Nema payload-a za napad.")
        return

    for category, param_names in PARAMS.items():
        print(f"[+] Napad kategorije: {category}")
        for param in param_names:
            for entry in payloads:
                payload = entry["payload"]
                full_url = f"{base_url}?{param}={payload}"
                try:
                    r = requests.get(full_url, timeout=10)
                    result = {
                        "url": full_url,
                        "status": r.status_code,
                        "length": len(r.text),
                        "category": category,
                        "param": param,
                        "payload": payload,
                        "reflected": payload in r.text
                    }
                    log_result(OUTPUT_LOG, result)
                    if result["reflected"]:
                        print(f"[✓] HIT ({category}) → {full_url}")
                except:
                    continue

    print(f"[✓] Završeno. Log: {OUTPUT_LOG}")
