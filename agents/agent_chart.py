import sqlite3
from collections import Counter
from rich import print
from rich.console import Console
from rich.table import Table
from rich.progress import BarColumn, Progress

DB = "shadowfox.db"
console = Console()

def load_stats(target_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT payload_type, reflected, status_code
        FROM scan_results
        WHERE target_id = ?
    """, (target_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def display_charts(data):
    by_type = Counter([r[0] for r in data])
    by_reflect = Counter(['YES' if r[1] == 1 else 'NO' for r in data])
    by_status = Counter([r[2] for r in data])

    table1 = Table(title="Broj payload-a po tipu")
    table1.add_column("Tip", style="cyan", no_wrap=True)
    table1.add_column("Ukupno", style="bold")

    for k, v in by_type.items():
        table1.add_row(k, str(v))

    table2 = Table(title="Reflektovani pogodci")
    table2.add_column("Reflected", style="green" )
    table2.add_column("Ukupno", style="bold")

    for k, v in by_reflect.items():
        table2.add_row(k, str(v))

    table3 = Table(title="HTTP status kodovi")
    table3.add_column("Status", style="magenta")
    table3.add_column("Ukupno", style="bold")

    for k, v in by_status.items():
        table3.add_row(str(k), str(v))

    console.print(table1)
    console.print(table2)
    console.print(table3)

if __name__ == "__main__":
    print("\n[+] Dostupne mete:")
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT id, url FROM targets")
    for tid, url in c.fetchall():
        print(f"[{tid}] {url}")
    conn.close()

    izbor = input("\n[?] Unesi ID mete za analizu: ").strip()
    rows = load_stats(int(izbor))
    display_charts(rows)
