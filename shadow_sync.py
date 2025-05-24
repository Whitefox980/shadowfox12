import os
import subprocess
from datetime import datetime

def sync_to_github():
    print("[*] ShadowSync: proveravam promene...")
    os.chdir("/root/shadowfox12")  # prilagodi ako ti je negde drugde

    subprocess.run(["git", "add", "."], check=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_msg = f"Sync sa tableta u {timestamp}"
    subprocess.run(["git", "commit", "-m", commit_msg])

    print("[*] Pokušavam push na GitHub...")
    subprocess.run(["git", "push", "origin", "main"])
    print("[✓] ShadowSync: završen push.")

if __name__ == "__main__":
    sync_to_github()
