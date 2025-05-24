import sqlite3
import os

DB_PATH = "shadowfox.db"

def init_db():
    if os.path.exists(DB_PATH):
        print("[=] Baza već postoji.")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''
        CREATE TABLE targets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            ip TEXT,
            status TEXT,
            title TEXT,
            recon_time TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE recon_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,
            tool TEXT,
            data TEXT,
            timestamp TEXT,
            FOREIGN KEY(target_id) REFERENCES targets(id)
        )
    ''')

    c.execute('''
        CREATE TABLE scan_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,
            payload_type TEXT,
            payload TEXT,
            reflected INTEGER,
            status_code TEXT,
            response_size INTEGER,
            timestamp TEXT,
            FOREIGN KEY(target_id) REFERENCES targets(id)
        )
    ''')

    c.execute('''
        CREATE TABLE mutations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_payload TEXT,
            mutated_payload TEXT,
            technique TEXT,
            effectiveness TEXT,
            timestamp TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target_id INTEGER,
            summary TEXT,
            file_path TEXT,
            format TEXT,
            created_at TEXT,
            FOREIGN KEY(target_id) REFERENCES targets(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("[+] Baza shadowfox.db kreirana.")

if __name__ == "__main__":
    init_db()
