import sqlite3
from rich.table import Table
from rich.console import Console

DB_PATH = "shadowfox.db"
SIGNATURE = "Chupko was here"

console = Console()

def prikazi_signature_hitove():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT target_id, payload, reflected, status_code, response_size, timestamp
        FROM scan_results
        WHERE payload LIKE ? AND payload_type = 'SIGNATURE' 
        ORDER BY timestamp DESC
    """, (f"%{SIGNATURE}%",))
    rows = c.fetchall()
    conn.close()

    if not rows:
        console.print("[bold red]Nema zabeleženih signature payload pogodaka.[/bold red]")
        return

    table = Table(title="Signature Payload Reflections")
    table.add_column("Target ID", style="cyan", justify="center")
    table.add_column("Payload", style="magenta")
    table.add_column("Reflected", style="green", justify="center")
    table.add_column("Status", justify="center")
    table.add_column("Size", justify="center")
    table.add_column("Timestamp", style="white")

    for tid, payload, reflected, status, size, timestamp in rows:
        hit = "[green]YES[/green]" if reflected else "[red]NO[/red]"
        table.add_row(str(tid), payload[:50], hit, str(status), str(size), timestamp)

    console.print(table)

if __name__ == "__main__":
    prikazi_signature_hitove()
