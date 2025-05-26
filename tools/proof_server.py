import http.server, socketserver

PORT = 9000
DIR = "proof_pack_target"

def run():
    print(f"[+] ShadowFox Proof Server pokrenut na http://localhost:{PORT}/")
    print(f"[i] Serving: {DIR}/")
    handler = http.server.SimpleHTTPRequestHandler
    os.chdir(DIR)
    socketserver.TCPServer(("", PORT), handler).serve_forever()

if __name__ == "__main__":
    run()
