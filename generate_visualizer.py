from pathlib import Path
from datetime import datetime

replay_dir = Path("replay")
proof_dir = Path("visual_proofs")
visualizer_path = Path("proof_pack/visualizer.html")

proof_dir.mkdir(parents=True, exist_ok=True)
visualizer_path.parent.mkdir(parents=True, exist_ok=True)

signature = "<h1>Chupko was here.. H1:Whitefox980</h1>"

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>ShadowFox Replay Visualizer</title>
  <style>
    body {{ background:#111; color:#0f0; font-family:monospace; padding:20px; }}
    h1 {{ text-align:center; }}
    iframe {{ width:100%; height:600px; margin-bottom:40px; border:2px solid #0f0; background:#fff; }}
    h2 {{ border-bottom:1px solid #0f0; margin-top:40px; }}
  </style>
</head>
<body>
<h1>Replay Visualizer with Signature Highlights</h1>
<p>Generated: {datetime.now().isoformat()}</p>
<hr>
"""

for replay_file in sorted(replay_dir.glob("replay_*.html")):
    content = replay_file.read_text(errors="ignore")

    # Ako ima signature, pravi proof sa boldiranim markerom
    if signature in content:
        highlighted = content.replace(
            signature,
            f'<span style="color:lime;font-weight:bold;">{signature}</span>'
        )
        proof_file = proof_dir / f"proof_{replay_file.name}"
        proof_file.write_text(highlighted)
        html += f"<h2>{proof_file.name}</h2><iframe src='../visual_proofs/{proof_file.name}'></iframe>\n"
    else:
        html += f"<h2>{replay_file.name}</h2><iframe src='../replay/{replay_file.name}'></iframe>\n"

html += "</body></html>"
visualizer_path.write_text(html)
print(f"[✓] Visualizer updated: {visualizer_path}")
