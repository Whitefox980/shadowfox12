import os
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 8888

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_my_headers()
        super().end_headers()

    def send_my_headers(self):
        self.send_header("Cache-Control", "no-store")

if __name__ == "__main__":
    print(f"[+] Pokrećem lokalni server na http://localhost:{PORT}")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    httpd = HTTPServer(("", PORT), CustomHandler)
    print("[✓] ShadowFox lokalni web server aktivan.")
    httpd.serve_forever()
