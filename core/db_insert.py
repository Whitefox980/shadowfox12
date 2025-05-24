import sqlite3
from datetime import datetime

DB_PATH = "shadowfox.db"

def insert_target(url, ip, status, title):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT INTO targets (url, ip, status, title, recon_time)
        VALUES (?, ?, ?, ?, ?)
    ''', (url, ip, status, title, now))
    conn.commit()
    conn.close()

def insert_recon_result(target_id, tool, data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT INTO recon_results (target_id, tool, data, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (target_id, tool, data, now))
    conn.commit()
    conn.close()

def insert_scan_result(target_id, payload_type, payload, reflected, status_code, response_size):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT INTO scan_results (target_id, payload_type, payload, reflected, status_code, response_size, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (target_id, payload_type, payload, reflected, status_code, response_size, now))
    conn.commit()
    conn.close()

def insert_mutation(base_payload, mutated_payload, technique, effectiveness):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT INTO mutations (base_payload, mutated_payload, technique, effectiveness, timestamp)
        VALUES (?, ?, ?, ?, ?)
    ''', (base_payload, mutated_payload, technique, effectiveness, now))
    conn.commit()
    conn.close()

def insert_report(target_id, summary, file_path, format_):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().isoformat()
    c.execute('''
        INSERT INTO reports (target_id, summary, file_path, format, created_at)
        VALUES (?, ?, ?, ?, ?)
    ''', (target_id, summary, file_path, format_, now))
    conn.commit()
    conn.close()
