"""
Reports management and persistent storage for TrustGuard AI.
Stores generated compliance, forensic audit, and threat incident reports in SQLite.
"""
import sqlite3
import time
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent.parent / "trustguard.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_reports_db():
    """Initializes the reports table if it doesn't exist."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                timestamp REAL NOT NULL,
                report_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                report_type TEXT NOT NULL,
                scan_id INTEGER,
                summary TEXT,
                metrics_json TEXT,
                findings_json TEXT,
                status TEXT DEFAULT 'FINAL',
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def create_report(
    title: str,
    report_type: str = "forensic_audit",
    user_id: int = 1,
    scan_id: Optional[int] = None,
    summary: str = "",
    metrics: Optional[Dict[str, Any]] = None,
    findings: Optional[List[Dict[str, Any]]] = None,
    status: str = "FINAL"
) -> Dict[str, Any]:
    """Creates and persists a new security/forensic report."""
    init_reports_db()
    ts = time.time()
    rep_id = f"REP-{int(ts)}-{int(ts * 1000) % 1000:03d}"
    created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(ts))

    m_json = json.dumps(metrics or {})
    f_json = json.dumps(findings or [])

    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO reports (
                user_id, timestamp, report_id, title, report_type,
                scan_id, summary, metrics_json, findings_json, status, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id, ts, rep_id, title, report_type,
            scan_id, summary, m_json, f_json, status, created_at
        ))
        conn.commit()
        db_id = cursor.lastrowid

    return {
        "id": db_id,
        "report_id": rep_id,
        "title": title,
        "report_type": report_type,
        "scan_id": scan_id,
        "summary": summary,
        "metrics": metrics or {},
        "findings": findings or [],
        "status": status,
        "created_at": created_at,
        "timestamp": ts
    }

def get_reports(user_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Fetches security reports ordered by creation date."""
    init_reports_db()
    with get_db() as conn:
        if user_id is not None:
            rows = conn.execute("""
                SELECT id, user_id, timestamp, report_id, title, report_type,
                       scan_id, summary, metrics_json, findings_json, status, created_at
                FROM reports
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT id, user_id, timestamp, report_id, title, report_type,
                       scan_id, summary, metrics_json, findings_json, status, created_at
                FROM reports
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()

        out = []
        for r in rows:
            d = dict(r)
            try:
                d["metrics"] = json.loads(d.get("metrics_json") or "{}")
            except Exception:
                d["metrics"] = {}
            try:
                d["findings"] = json.loads(d.get("findings_json") or "[]")
            except Exception:
                d["findings"] = []
            out.append(d)
        return out

def get_report_by_id(report_id_or_db_id) -> Optional[Dict[str, Any]]:
    """Fetches a specific report by database ID or alphanumeric report_id."""
    init_reports_db()
    with get_db() as conn:
        if str(report_id_or_db_id).isdigit():
            row = conn.execute("SELECT * FROM reports WHERE id = ?", (int(report_id_or_db_id),)).fetchone()
        else:
            row = conn.execute("SELECT * FROM reports WHERE report_id = ?", (str(report_id_or_db_id),)).fetchone()

        if not row:
            return None
        d = dict(row)
        try:
            d["metrics"] = json.loads(d.get("metrics_json") or "{}")
        except Exception:
            d["metrics"] = {}
        try:
            d["findings"] = json.loads(d.get("findings_json") or "[]")
        except Exception:
            d["findings"] = []
        return d

# Initialize on import
init_reports_db()
