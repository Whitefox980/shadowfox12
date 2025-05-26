import os
import sys
import datetime
import json
import requests
from agents import agent_bypass, agent_secrets, agent_js_scraper, agent_recon, agent_payload_mutator

LOG_FILE = "logs/agent_log.jsonl"

def log_result(module, data):
    data["module"] = module
    data["timestamp"] = datetime.datetime.now().isoformat()
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def download_js_file(js_url):
    try:
        r = requests.get(js_url, timeout=5)
        domain = js_url.split("//")[-1].split("/")[0]
        filename = js_url.split("/")[-1].split("?")[0] or "script.js"
        filename = f"{domain}_{filename}"
        with open(filename, "w") as f:
            f.write(r.text)
        print(f"[✓] JS fajl sačuvan kao: {filename}")
    except Exception as e:
        print(f"[!] Greška pri preuzimanju: {e}")
def menu():
    while True:
        print("\n=== ShadowFox Agent Tools ===")
        print("1. Test 403 Bypass")
        print("2. Extract Secrets from JS URL")
        print("3. Extract Endpoints from JS File")
        print("4. Find JS Files on Domain")
        print("5. Show Upload Payloads")
        print("6. Download JS file")
        print("7. Auto Recon META")
        print("8. Fuzz endpoints from DB")
        print("9. AI Review fuzz rezultata")
        print("0. Exit")

        choice = input("Izaberi opciju: ").strip()

        if choice == "1":
            url = input("Unesi URL (npr. https://site.com): ").strip()
            agent_bypass.test_403_bypass(url, log_result)

        elif choice == "2":
            js_url = input("Unesi JS URL: ").strip()
            agent_secrets.extract_secrets(js_url, log_result)

        elif choice == "3":
            file_path = input("Putanja do .js fajla: ").strip()
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    js_code = f.read()
                    endpoints = agent_js_scraper.extract_endpoints(js_code)
                    for ep in endpoints:
                        print(f"[+] Endpoint: {ep}")
            else:
                print("Fajl ne postoji.")

        elif choice == "4":
            domain = input("Unesi domen (npr. site.com): ").strip()
            agent_recon.find_js_files(domain)

        elif choice == "5":
            agent_payload_mutator.file_upload_payloads()

        elif choice == "6":
            js_url = input("Unesi JS URL za preuzimanje: ").strip()
            download_js_file(js_url)

        elif choice == "7":
            meta = input("Unesi početni URL (https://...): ").strip()
            from agents import agent_recon_auto
            agent_recon_auto.recon_meta(meta)
        elif choice == "8":
            domain = input("Unesi domen iz baze (npr. www.checkfelix.com): ").strip()
            base_url = input("Unesi bazni URL (https://www.checkfelix.com): ").strip()
            from agents import agent_endpoint_fuzzer
            agent_endpoint_fuzzer.run_fuzzer(domain, base_url)
        elif choice == "9":
            from agents import agent_ai_reviewer
            agent_ai_reviewer.review_results()
        elif choice == "0":
            print("Izlaz...")
            sys.exit()

        else:
            print("Nepoznata opcija.")

if __name__ == "__main__":
    menu()
