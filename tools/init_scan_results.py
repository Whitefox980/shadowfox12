import sqlite3

db_path = "shadowfox.db"

create_table_sql = """
CREATE TABLE IF NOT EXISTS scan_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_id INTEGER,
    tip TEXT,
    payload TEXT,
    reflected INTEGER,
    status_code TEXT,
    response_size INTEGER,
    timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute(create_table_sql)
conn.commit()
conn.close()

print("✅ Tabela 'scan_results' kreirana ili već postoji.")
