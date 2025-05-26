import os
from datetime import datetime

def save_proof(url, payload, response, exploit=False):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"proofs/proof_{timestamp}.html"

    banner_color = "#00ff00" if exploit else "#0066ff"  # Zeleno za exploit, plavo za refleksiju

    html = f"""
<html><body style='background:#000;color:{banner_color};font-family:monospace;padding:20px;'>
<h1>Čupko was here.</h1>
<h2>H1: Whitefox980 Team</h2>
<hr>
<b>Target:</b> {url}<br>
<b>Payload:</b> {payload}<br>
<b>Tip:</b> {"[!] POTENCIJALNI EXPLOIT" if exploit else "Reflected Only"}<br>
<hr>
<pre>{response}</pre>
</body></html>
"""

    with open(filename, "w") as f:
        f.write(html)
    return filename
