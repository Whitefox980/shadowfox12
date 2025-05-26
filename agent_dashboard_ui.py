from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
import json
import os
from tools.shadowfox_config import get_path
from datetime import datetime

app = FastAPI()
templates = Environment(loader=FileSystemLoader("templates"))

app.mount("/static", StaticFiles(directory="static"), name="static")

LOG_PATH = get_path("logs") + "/shadowfuzz_ai.jsonl"
PDF_PATH = get_path("reports") + "/ShadowFox_Report.pdf"
ZIP_PATH = "proof_pack_target.zip"

def load_logs():
    entries = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            for line in list(f)[-10:]:
                try:
                    data = json.loads(line.strip())
                    data["time"] = datetime.now().strftime("%H:%M:%S")
                    entries.append(data)
                except:
                    continue
    return list(reversed(entries))

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    logs = load_logs()
    return templates.get_template("dashboard.html").render(
        request=request,
        logs=logs,
        pdf_exists=os.path.exists(PDF_PATH),
        zip_exists=os.path.exists(ZIP_PATH),
        agent_status={
            "Recon": "✅",
            "Fuzz": "✅" if logs else "❌",
            "Replay": "✅" if any(l.get("reflected") for l in logs) else "❌",
            "Screenshot": "✅" if os.path.exists(get_path("reports") + "/replay_ai_screens") else "❌",
            "PDF": "✅" if os.path.exists(PDF_PATH) else "❌",
            "Zip": "✅" if os.path.exists(ZIP_PATH) else "❌",
            "Email": "❌"
        }
    )
