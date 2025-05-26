import os
import subprocess

def shadowproof():
    os.chdir("modules/shadowproof")
    os.system("python3 signature_tracker.py")
    os.chdir("../../")

def shadowfuzz():
    os.chdir("modules/shadowfuzz")
    os.system("python3 ShadowFuzzController.py")
    os.chdir("../../")

def start_server():
    try:
        os.chdir("modules/shadowproof")
        print("\n[+] Pokrećem lokalni server na portu 8888...")
        print("[✓] Otvori u browseru: http://127.0.0.1:8888/visualizer.html\n")
        subprocess.run(["python3", "-m", "http.server", "8888"])
    except Exception as e:
        print("[!] Greška:", e)
    finally:
        os.chdir("../../")

def view_last_log():
    os.chdir("modules/shadowfuzz")
    logs = sorted([f for f in os.listdir() if f.startswith("controller_log_")], reverse=True)
    if logs:
        print(f"\n[+] Poslednji log: {logs[0]}\n")
        os.system(f"cat {logs[0]}")
    else:
        print("[!] Nema logova.")
    os.chdir("../../")

while True:
    print("\n=== ShadowFox Main Terminal ===")
    print("1. Signature Scanner (ShadowProof)")
    print("2. Full Fuzzing Controller")
    print("3. Pokreni Visualizer server (8888)")
    print("4. Prikaži poslednji Fuzz log")
    print("5. Izlaz")
    izbor = input("Izaberi opciju: ").strip()

    if izbor == "1":
        shadowproof()
    elif izbor == "2":
        shadowfuzz()
    elif izbor == "3":
        start_server()
    elif izbor == "4":
        view_last_log()
    elif izbor == "5":
        print("Zatvaram ShadowFox. Čupko is out.")
        break
    else:
        print("Nepoznata opcija.")
