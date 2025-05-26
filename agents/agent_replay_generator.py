import json, os
from tools.shadowfox_config import get_path

LOGFILE = get_path("logs") + "/shadowfuzz_ai.jsonl"
OUTDIR = get_path("reports") + "/replay_ai"

def generate_replay():
    if not os.path.exists(LOGFILE):
        print("[!] Nema shadowfuzz_ai loga.")
        return

    os.makedirs(OUTDIR, exist_ok=True)
    count = 0

    with open(LOGFILE, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get("reflected"):
                    count += 1
                    fname = f"proof_ai_{count}.html"
                    path = os.path.join(OUTDIR, fname)
                    with open(path, "w") as out:
                        out.write(f"""
<!DOCTYPE html>
<html>
<head><title>ShadowFox AI Proof #{count}</title></head>
<body>
<h2>URL:</h2>
<p>{data['url']}</p>
<h3>Original Payload:</h3>
<pre>{data['original']}</pre>
<h3>Mutated Payload:</h3>
<pre>{data['mutated']}</pre>
<h3>Status:</h3>
<p>{data['status']}</p>
</body>
</html>
""")
            except:
                continue

    print(f"[✓] Replay generacija gotova. Sačuvano {count} fajlova u: {OUTDIR}")
