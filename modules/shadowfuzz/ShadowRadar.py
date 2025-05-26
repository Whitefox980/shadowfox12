import json
import os
import matplotlib.pyplot as plt

def load_latest_log():
    logs = sorted([f for f in os.listdir() if f.startswith("controller_log_") and f.endswith(".json")], reverse=True)
    if not logs:
        print("[!] Nema logova.")
        return []
    with open(logs[0], "r") as f:
        return json.load(f)

def analyze(data):
    total = len(data)
    reflected = sum(1 for x in data if x.get("reflected"))
    exploit = sum(1 for x in data if x.get("potential_exploit"))
    failed = total - reflected - exploit
    return reflected, exploit, failed

def draw_pie(reflected, exploit, failed):
    labels = ["Reflected", "Exploit Possible", "No Effect"]
    sizes = [reflected, exploit, failed]
    colors = ["#0066ff", "#00ff00", "#555555"]

    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
    plt.title("ShadowRadar – Detection Breakdown")

    output_file = "../shadowproof/proofs/radar_export.png"
    plt.savefig(output_file)
    print(f"[✓] Radar snimljen i prebačen u: {output_file}")
    print("[✓] Snimljen radar kao: radar_export.png")
if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    data = load_latest_log()
    if data:
        r, e, f = analyze(data)
        draw_pie(r, e, f)
