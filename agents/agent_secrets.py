import requests

def extract_secrets(js_url, log_func):
    keywords = ["accesskey", "admin", "api_key", "apikey", "password", "secret", "token"]
    try:
        r = requests.get(js_url, timeout=5)
        for key in keywords:
            if key in r.text:
                print(f"[!] Possible secret '{key}' found in: {js_url}")
                log_func("agent_secrets", {"url": js_url, "keyword": key})
    except Exception as e:
        print(f"[-] Error fetching {js_url}: {e}")
        log_func("agent_secrets", {"url": js_url, "error": str(e)})
