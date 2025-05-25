import os

def banner():
    print("""
  ███████╗██╗  ██╗ █████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗
  ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██║ ██╔╝
  ███████╗███████║███████║██████╔╝██████╔╝██║   ██║█████╔╝ 
  ╚════██║██╔══██║██╔══██║██╔═══╝ ██╔═══╝ ██║   ██║██╔═██╗ 
  ███████║██║  ██║██║  ██║██║     ██║     ╚██████╔╝██║  ██╗
  ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚═════╝ ╚═╝  ╚═╝

        [ SHADOWFOX 12 - OPERATOR TERMINAL ]
    """)

def menu():
    print("""
[1] Pokreni AutoMod (agent_shadowx)
[2] Pokreni Replay sistem
[3] Prikaži Signature dokaze
[4] Vizuelni pregled (generate_visualizer)
[5] Pokreni Recon agenta
[6] Pokreni Mutator agenta
[7] Pokreni Report agenta
[8] Pokreni Advisor agenta
[9] Pokreni Signature Tracker
[10] Pokreni Listener Log
[11] Otvori serve_local.py
[0] Izlaz
""")

def run(choice):
    commands = {
        "1": "python3 agents/agent_shadowx.py",
        "2": "python3 agents/agent_replay.py",
        "3": "python3 agents/agent_signature_tracker.py",
        "4": "python3 generate_visualizer.py",
        "5": "python3 agents/agent_recon.py",
        "6": "python3 agents/agent_mutant.py",
        "7": "python3 agents/agent_report.py",
        "8": "python3 agents/agent_advisor.py",
        "9": "python3 agents/agent_signature_tracker.py",
        "10": "python3 agents/agent_listener_log.py",
        "11": "python3 serve_local.py"
    }
    os.system(commands.get(choice, "echo Nepoznata opcija."))

if __name__ == "__main__":
    while True:
        os.system("clear")
        banner()
        menu()
        choice = input("[?] Izbor: ")
        if choice == "0":
            print("Zatvaram ShadowFox Terminal...")
            break
        run(choice)
        input("\n[ENTER za povratak u meni]")
