import os
import json
import sqlite3
import uuid
from datetime import datetime
from src.utils import get_project_root

DB_PATH = os.path.join(get_project_root(), "data", "scamshield.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            scan_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            scanner_type TEXT NOT NULL,
            risk_score INTEGER NOT NULL,
            risk_level TEXT NOT NULL,
            category TEXT NOT NULL,
            short_summary TEXT,
            full_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def save_scan(scanner_type, result_dict, raw_input="", privacy_mode=False):
    init_db()
    scan_id = str(uuid.uuid4())[:8]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    score = result_dict.get("risk_score", 0)
    level = result_dict.get("risk_level", "SAFE")
    category = result_dict.get("category", "General")

    if privacy_mode:
        summary = f"Privacy Mode Active: {scanner_type.title()} scan evaluated as {level} risk ({score}/100)."
        clean_result = result_dict.copy()
        if "raw_input" in clean_result:
            clean_result["raw_input"] = "[REDACTED - PRIVACY MODE]"
        if "text" in clean_result:
            clean_result["text"] = "[REDACTED - PRIVACY MODE]"
        full_json = json.dumps(clean_result)
    else:
        summary_text = raw_input if raw_input else result_dict.get("explanation", "")
        summary = (summary_text[:120] + "...") if len(summary_text) > 120 else summary_text
        full_json = json.dumps(result_dict)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scans (scan_id, timestamp, scanner_type, risk_score, risk_level, category, short_summary, full_json)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (scan_id, timestamp, scanner_type, score, level, category, summary, full_json))
    conn.commit()
    conn.close()

    return scan_id


def get_scans(limit=100, scanner_type=None, risk_level=None, search_query=None):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM scans WHERE 1=1"
    params = []

    if scanner_type and scanner_type != "All":
        query += " AND scanner_type = ?"
        params.append(scanner_type.lower())

    if risk_level and risk_level != "All":
        query += " AND risk_level = ?"
        params.append(risk_level.upper())

    if search_query and search_query.strip():
        query += " AND (short_summary LIKE ? OR category LIKE ?)"
        term = f"%{search_query.strip()}%"
        params.extend([term, term])

    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    scans = []
    for r in rows:
        scan_dict = dict(r)
        try:
            scan_dict["full_json"] = json.loads(scan_dict["full_json"])
        except Exception:
            pass
        scans.append(scan_dict)

    return scans


def delete_scan(scan_id):
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE scan_id = ?", (scan_id,))
    conn.commit()
    conn.close()


def clear_all_scans():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans")
    conn.commit()
    conn.close()


def get_analytics_summary():
    init_db()
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM scans")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT risk_level, COUNT(*) as count FROM scans GROUP BY risk_level")
    risk_counts = {row["risk_level"]: row["count"] for row in cursor.fetchall()}

    cursor.execute("SELECT category, COUNT(*) as count FROM scans GROUP BY category")
    category_counts = {row["category"]: row["count"] for row in cursor.fetchall()}

    cursor.execute("SELECT scanner_type, COUNT(*) as count FROM scans GROUP BY scanner_type")
    scanner_counts = {row["scanner_type"]: row["count"] for row in cursor.fetchall()}

    conn.close()

    return {
        "total": total,
        "risk_counts": risk_counts,
        "category_counts": category_counts,
        "scanner_counts": scanner_counts
    }
