import json
from collections import Counter, defaultdict

LOG_FILE = "logs/agent_log.jsonl"

def load_logs():
    logs = []
    try:
        with open(LOG_FILE, "r") as f:
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except json.JSONDecodeError:
                    continue
    except FileNotFoundError:
        print("[!] Log fajl ne postoji.")
    return logs

def show_summary(logs):
    print("\n=== Statistika po agentima ===")
    agents = Counter(log["module"] for log in logs)
    for agent, count in agents.items():
        print(f"{agent}: {count} zapisa")

def show_status_codes(logs):
    print("\n=== Status kodovi ===")
    codes = Counter(log.get("status", "N/A") for log in logs if "status" in log)
    for code, count in codes.items():
        print(f"{code}: {count} puta")

def show_urls(logs):
    print("\n=== Skenirani URL-ovi ===")
    urls = defaultdict(list)
    for log in logs:
        if "url" in log:
            urls[log["module"]].append(log["url"])
    for mod, url_list in urls.items():
        print(f"\n[{mod}]")
        for url in sorted(set(url_list)):
            print(f" - {url}")

def main():
    logs = load_logs()
    if not logs:
        return

    show_summary(logs)
    show_status_codes(logs)
    show_urls(logs)

if __name__ == "__main__":
    main()
