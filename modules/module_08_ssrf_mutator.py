import json
from datetime import datetime

def load_bypass_payloads():
    with open("modules/ssrf_bypass_list.json") as f:
        return json.load(f)

def generate_mutations():
    payloads = load_bypass_payloads()
    with open("mutations/ssrf_mutations.txt", "w") as f:
        for p in payloads:
            f.write(p + "\n")
    print(f"[+] {len(payloads)} SSRF bypass payloada upisano u mutations/ssrf_mutations.txt")

if __name__ == "__main__":
    generate_mutations()
