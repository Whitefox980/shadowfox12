import subprocess, os, re, requests, sqlite3, json
from urllib.parse import urlparse

def init_db():
    conn = sqlite3.connect("intel.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS js_files (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT, url TEXT, filename TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS endpoints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT, file TEXT, endpoint TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS secrets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        domain TEXT, file TEXT, keyword TEXT
    )""")
    conn.commit()
    return conn

def extract_endpoints(js_text):
    pattern = re.compile(r'(?<=[\'"`])\/[a-zA-Z0-9_\-\/\.]*?(?=[\'"`])')
    return sorted(set(pattern.findall(js_text)))

def extract_keywords(js_text):
    keywords = ["accesskey", "admin", "api_key", "apikey", "password", "secret", "token"]
    found = []
    for key in keywords:
        if key in js_text:
            found.append(key)
    return found

def recon_meta(domain):
    parsed = urlparse(domain).netloc
    print(f"\n[*] Pokrećem RECON za: {parsed}")
    conn = init_db()
    c = conn.cursor()

    # Step 1: gau .js files
    cmd = f"gau {parsed} | grep '\\.js'"
    print("[*] Pronalazim JS fajlove...")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    js_links = sorted(set(result.stdout.strip().split("\n")))

    summary = {
        "domain": parsed,
        "js_files": [],
        "endpoints": [],
        "secrets": []
    }

    for link in js_links:
        if not link.startswith("http"):
            continue
        print(f"[JS] {link}")
        try:
            r = requests.get(link, timeout=7)
            fname = parsed + "_" + os.path.basename(link).split("?")[0]
            with open(fname, "w") as f:
                f.write(r.text)
            c.execute("INSERT INTO js_files (domain, url, filename) VALUES (?, ?, ?)", (parsed, link, fname))
            summary["js_files"].append(link)

            eps = extract_endpoints(r.text)
            for ep in eps:
                c.execute("INSERT INTO endpoints (domain, file, endpoint) VALUES (?, ?, ?)", (parsed, fname, ep))
                summary["endpoints"].append(ep)

            kws = extract_keywords(r.text)
            for kw in kws:
                c.execute("INSERT INTO secrets (domain, file, keyword) VALUES (?, ?, ?)", (parsed, fname, kw))
                summary["secrets"].append(kw)

        except Exception as e:
            print(f"[!] Greška za {link}: {e}")

    conn.commit()
    conn.close()

    with open(f"intel_summary_{parsed}.json", "w") as out:
        json.dump(summary, out, indent=2)
    print(f"\n[✓] Završeno. Sačuvan summary: intel_summary_{parsed}.json")
