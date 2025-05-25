import sqlite3
from rich import print
from rich.table import Table

DB = "shadowfox.db"

def prikazi_payloade(target_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT payload_type, payload, reflected, status_code, response_size
        FROM scan_results
        WHERE target_id = ?
        ORDER BY payload_type, reflected DESC
    """, (target_id,))
    rows = c.fetchall()
    conn.close()

    tabela = Table(title=f"Payload analiza za metu ID {target_id}")
    tabela.add_column("Tip", style="bold cyan")
    tabela.add_column("Payload", style="white", overflow="fold")
    tabela.add_column("Status", justify="center")
    tabela.add_column("HIT", justify="center")
    tabela.add_column("Size", justify="center")

    for tip, payload, reflected, status, size in rows:
        boja = "green" if reflected else "red"
        tabela.add_row(tip, payload[:60] + ("..." if len(payload) > 60 else ""), str(status), f"[{boja}]{'YES' if reflected else 'NO'}[/{boja}]", str(size))

    print(tabela)

if __name__ == "__main__":
    print("\n[+] Dostupne mete:")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    for tid, url in c.fetchall():
        print(f"[{tid}] {url}")
    conn.close()

    izbor = input("\n[?] Unesi ID mete za prikaz: ").strip()
    prikazi_payloade(int(izbor))
