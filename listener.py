from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from datetime import datetime
import os

PORT = 8888
LOG_FILE = "logs/bounce_log.txt"

class BounceHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        ip = self.client_address[0]
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] IP: {ip} | PATH: {parsed.path} | DATA: {query}\n"

        print(log_entry.strip())

        if not os.path.exists("logs"):
            os.makedirs("logs")

        with open(LOG_FILE, "a") as f:
            f.write(log_entry)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"[ShadowFox] Bounce received.")

def run():
    server = HTTPServer(('', PORT), BounceHandler)
    print(f"[+] Listener aktivan na portu {PORT}...")
    print("[*] Čeka dolazne zahteve...\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[!] Zatvaram listener.")
        server.server_close()

if __name__ == "__main__":
    run()
