import json
from collections import Counter, defaultdict

def review_results(logfile="fuzz_results.jsonl"):
    hits = []
    status_counter = Counter()
    reflection_hits = []

    try:
        with open(logfile, "r") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    status_counter[data["status"]] += 1
                    if data.get("reflected"):
                        reflection_hits.append(data)
                        hits.append({
                            "url": data["url"],
                            "status": data["status"],
                            "reflected": True,
                            "length": data["length"]
                        })
                except:
                    continue
    except FileNotFoundError:
        print("[!] Log fajl nije pronađen.")
        return

    print("\n=== AI REVIEW SUMMARY ===")
    print(f"[+] Ukupno testiranih URL-ova: {sum(status_counter.values())}")
    for status, count in status_counter.items():
        print(f" - Status {status}: {count} puta")

    print(f"[+] Reflektovani payload-i: {len(reflection_hits)}")

    # Snimi reflektovane kao JSON
    with open("ai_hits_summary.json", "w") as out:
        json.dump(hits, out, indent=2)

    # Prikaži top 10 po dužini odgovora
    print("\n=== TOP 10 reflektovanih odgovora po veličini ===")
    top = sorted(hits, key=lambda x: x["length"], reverse=True)[:10]
    for i, entry in enumerate(top, 1):
        print(f"{i}. {entry['url']} → Status: {entry['status']}, Len: {entry['length']}")

    print("\n[✓] Pregled završen. Sačuvan fajl: ai_hits_summary.json")
