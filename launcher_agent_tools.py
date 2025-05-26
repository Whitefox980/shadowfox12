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
        print("10. Očisti sistem (Deep Cleaner)")
        print("11. Izvuci uspešne payload-e (Top Payload Extractor)")
        print("12. Param Spammer (RCE / LFI / SSRF / XSS parametri)")
        print("13. SSRF Bypasser modul")
        print("14. Evaluacija uspešnih fuzz logova (AI analiza)")
        print("15. Mutacija uspešnih payload-a (AI Mutator)")
        print("16. ShadowFuzz AI: Mutacija + Endpoint napad")
        print("17. Generiši AI Replay dokaze (.html)")
        print("18. Generiši screenshot-ove replay dokaza (.png)")
        print("19. Generiši PDF izveštaj svih uspešnih pogodaka")
        print("20. Kreiraj finalni proof paket + ZIP")
        print("21. Dodaj watermark na sve AI screenshot-ove")

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

        elif choice == "10":
            from tools import shadowfox_deepclean
            shadowfox_deepclean.deep_clean()
        elif choice == "11":
            from agents import top_payload_extractor
            top_payload_extractor.extract_top_payloads()
        elif choice == "12":
            from agents import agent_param_spammer
            dom = input("Unesi domen iz baze (npr. www.target.com): ").strip()
            base = input("Unesi bazni URL (npr. https://target.com): ").strip()
            agent_param_spammer.spam_parameters(dom, base)
        elif choice == "13":
            from agents import agent_ssrf_bypasser
            dom = input("Unesi domen iz baze (npr. www.target.com): ").strip()
            base = input("Unesi bazni URL (npr. https://target.com): ").strip()
            agent_ssrf_bypasser.bypass_ssrf(dom, base)
        elif choice == "14":
            from agents import agent_fuzz_evaluator
            agent_fuzz_evaluator.evaluate_fuzz_logs()
        elif choice == "15":
            from agents import agent_mutator_ai
            agent_mutator_ai.generate_mutated_payloads()
        elif choice == "16":
            from agents import agent_shadowfuzz_ai
            dom = input("Unesi domen iz baze (npr. www.target.com): ").strip()
            base = input("Unesi bazni URL (https://target.com): ").strip()
            agent_shadowfuzz_ai.run_shadowfuzz(dom, base)
        elif choice == "17":
            from agents import agent_replay_generator
            agent_replay_generator.generate_replay()
        elif choice == "18":
            from agents import agent_replay_screenshot
            agent_replay_screenshot.generate_screenshots()
        elif choice == "19":
            from agents import agent_pdf_report
            agent_pdf_report.generate_pdf_report()
        elif choice == "20":
            from agents import agent_proof_packager
            agent_proof_packager.build_proof_pack()
        elif choice == "21":
            from agents import agent_watermark_screens
            agent_watermark_screens.add_watermark()

        elif choice == "0":
            print("Izlaz...")
            sys.exit()

        else:
            print("Nepoznata opcija.")

if __name__ == "__main__":
    menu()
