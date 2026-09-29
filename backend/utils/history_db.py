"""
SQLite database and dynamic statistics tracker for TrustGuard AI.
Stores content authenticity scan history and computes live trust metrics.
"""
import sqlite3
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent.parent / "trustguard.db"


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initializes the SQLite schema if it doesn't already exist and migrates columns."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER DEFAULT 1,
                timestamp REAL NOT NULL,
                scan_type TEXT NOT NULL,
                content_label TEXT NOT NULL,
                classification TEXT NOT NULL,
                confidence REAL NOT NULL,
                risk_score REAL NOT NULL,
                risk_level TEXT NOT NULL,
                trust_score REAL DEFAULT 50.0,
                trust_category TEXT DEFAULT 'UNCERTAIN',
                is_threat INTEGER NOT NULL DEFAULT 0,
                is_deepfake INTEGER NOT NULL DEFAULT 0,
                is_scam INTEGER NOT NULL DEFAULT 0,
                explanation TEXT,
                indicators_json TEXT,
                frame_results_json TEXT DEFAULT '[]',
                segment_results_json TEXT DEFAULT '[]'
            )
        """)
        
        # Check and migrate columns if missing from legacy tables
        cols = [r["name"] for r in conn.execute("PRAGMA table_info(scan_history)").fetchall()]
        if "user_id" not in cols:
            conn.execute("ALTER TABLE scan_history ADD COLUMN user_id INTEGER DEFAULT 1")
        if "trust_score" not in cols:
            conn.execute("ALTER TABLE scan_history ADD COLUMN trust_score REAL DEFAULT 50.0")
        if "trust_category" not in cols:
            conn.execute("ALTER TABLE scan_history ADD COLUMN trust_category TEXT DEFAULT 'UNCERTAIN'")
        if "frame_results_json" not in cols:
            conn.execute("ALTER TABLE scan_history ADD COLUMN frame_results_json TEXT DEFAULT '[]'")
        if "segment_results_json" not in cols:
            conn.execute("ALTER TABLE scan_history ADD COLUMN segment_results_json TEXT DEFAULT '[]'")
            
        conn.commit()


def record_scan(
    scan_type: str,
    content_label: str,
    classification: str,
    confidence: float,
    risk_score: float,
    risk_level: str,
    trust_score: Optional[float] = None,
    trust_category: Optional[str] = None,
    user_id: Optional[int] = 1,
    explanation: str = "",
    indicators_json: str = "[]",
    frame_results_json: str = "[]",
    segment_results_json: str = "[]"
) -> int:
    """Inserts a completed scan record into the database."""
    init_db()
    
    if trust_score is None:
        trust_score = round(max(0.0, min(100.0, 100.0 - risk_score)), 1)
    if trust_category is None:
        if trust_score >= 90.0:
            trust_category = "HIGH TRUST"
        elif trust_score >= 70.0:
            trust_category = "LIKELY TRUSTWORTHY"
        elif trust_score >= 40.0:
            trust_category = "UNCERTAIN / REVIEW"
        else:
            trust_category = "LOW TRUST"

    is_threat = 1 if risk_score > 40.0 or "FAKE" in classification.upper() or "SCAM" in classification.upper() else 0
    is_deepfake = 1 if scan_type in ["image", "video", "audio"] and (risk_score > 40.0 or "AI" in classification.upper()) else 0
    is_scam = 1 if scan_type in ["text", "job", "internship", "url", "ocr", "social"] and (risk_score > 40.0 or "SCAM" in classification.upper()) else 0
    u_id = user_id if user_id is not None else 1

    with get_db() as conn:
        cursor = conn.execute("""
            INSERT INTO scan_history (
                user_id, timestamp, scan_type, content_label, classification,
                confidence, risk_score, risk_level, trust_score, trust_category,
                is_threat, is_deepfake, is_scam, explanation, indicators_json,
                frame_results_json, segment_results_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            u_id, time.time(), scan_type, content_label, classification,
            confidence, risk_score, risk_level, trust_score, trust_category,
            is_threat, is_deepfake, is_scam, explanation, indicators_json,
            frame_results_json, segment_results_json
        ))
        conn.commit()
        return cursor.lastrowid


def get_stats(user_id: Optional[int] = None) -> Dict[str, Any]:
    """Calculates live authenticity statistics from stored history."""
    init_db()
    with get_db() as conn:
        base_query = "FROM scan_history"
        params = ()
        if user_id is not None:
            base_query += " WHERE user_id = ?"
            params = (user_id,)

        total = conn.execute(f"SELECT COUNT(*) {base_query}", params).fetchone()[0]
        
        # Breakdown by authenticity categories
        authentic_query = f"SELECT COUNT(*) {base_query} {'AND' if user_id is not None else 'WHERE'} (trust_score >= 70.0 OR classification LIKE '%REAL%' OR classification LIKE '%GENUINE%')"
        ai_generated_query = f"SELECT COUNT(*) {base_query} {'AND' if user_id is not None else 'WHERE'} (trust_score < 40.0 OR classification LIKE '%AI%' OR classification LIKE '%FAKE%' OR is_deepfake = 1)"
        suspicious_query = f"SELECT COUNT(*) {base_query} {'AND' if user_id is not None else 'WHERE'} (classification LIKE '%SUSPICIOUS%' OR (trust_score >= 40.0 AND trust_score < 55.0))"
        uncertain_query = f"SELECT COUNT(*) {base_query} {'AND' if user_id is not None else 'WHERE'} (classification LIKE '%UNCERTAIN%' OR (trust_score >= 50.0 AND trust_score < 70.0))"

        authentic = conn.execute(authentic_query, params).fetchone()[0]
        ai_generated = conn.execute(ai_generated_query, params).fetchone()[0]
        suspicious = conn.execute(suspicious_query, params).fetchone()[0]
        uncertain = conn.execute(uncertain_query, params).fetchone()[0]

        threats = conn.execute(f"SELECT COUNT(*) {base_query} {'AND' if user_id is not None else 'WHERE'} is_threat = 1", params).fetchone()[0]
        deepfakes = conn.execute(f"SELECT COUNT(*) {base_query} {'AND' if user_id is not None else 'WHERE'} is_deepfake = 1", params).fetchone()[0]
        scams = conn.execute(f"SELECT COUNT(*) {base_query} {'AND' if user_id is not None else 'WHERE'} is_scam = 1", params).fetchone()[0]

        avg_row = conn.execute(f"SELECT AVG(trust_score) {base_query} {'AND' if user_id is not None else 'WHERE'} trust_score IS NOT NULL", params).fetchone()
        avg_trust = round(avg_row[0], 1) if avg_row and avg_row[0] is not None else 85.0

        return {
            "total_scans": total,
            "scans": total,
            "authentic": authentic,
            "ai_generated": ai_generated,
            "suspicious": suspicious,
            "uncertain": uncertain,
            "threats": threats,
            "deepfakes": deepfakes,
            "scams": scams,
            "average_trust_score": avg_trust
        }


def get_history(user_id: Optional[int] = None, limit: int = 50) -> List[Dict[str, Any]]:
    """Fetches recent scan history with trust scores and classifications."""
    init_db()
    with get_db() as conn:
        if user_id is not None:
            rows = conn.execute("""
                SELECT id, user_id, timestamp, scan_type, content_label, classification,
                       confidence, risk_score, risk_level, trust_score, trust_category, explanation,
                       frame_results_json, segment_results_json
                FROM scan_history
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit)).fetchall()
        else:
            rows = conn.execute("""
                SELECT id, user_id, timestamp, scan_type, content_label, classification,
                       confidence, risk_score, risk_level, trust_score, trust_category, explanation,
                       frame_results_json, segment_results_json
                FROM scan_history
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,)).fetchall()

        out = []
        for r in rows:
            d = dict(r)
            # Guarantee trust_score exists
            if d.get("trust_score") is None:
                d["trust_score"] = round(max(0.0, min(100.0, 100.0 - (d.get("risk_score") or 0.0))), 1)
            if not d.get("trust_category"):
                ts = d["trust_score"]
                d["trust_category"] = "HIGH TRUST" if ts >= 90 else "LIKELY TRUSTWORTHY" if ts >= 70 else "UNCERTAIN / REVIEW" if ts >= 40 else "LOW TRUST"
            out.append(d)
        return out


def clear_history(user_id: Optional[int] = None):
    """Clears scan history."""
    init_db()
    with get_db() as conn:
        if user_id is not None:
            conn.execute("DELETE FROM scan_history WHERE user_id = ?", (user_id,))
        else:
            conn.execute("DELETE FROM scan_history")
        conn.commit()


def get_scan_by_id(scan_id: int) -> Optional[Dict[str, Any]]:
    """Fetches a specific scan record by ID."""
    init_db()
    with get_db() as conn:
        row = conn.execute("""
            SELECT id, user_id, timestamp, scan_type, content_label, classification,
                   confidence, risk_score, risk_level, trust_score, trust_category, explanation,
                   indicators_json, frame_results_json, segment_results_json
            FROM scan_history
            WHERE id = ?
        """, (scan_id,)).fetchone()
        if not row:
            return None
        d = dict(row)
        if d.get("trust_score") is None:
            d["trust_score"] = round(max(0.0, min(100.0, 100.0 - (d.get("risk_score") or 0.0))), 1)
        if not d.get("trust_category"):
            ts = d["trust_score"]
            d["trust_category"] = "HIGH TRUST" if ts >= 90 else "LIKELY TRUSTWORTHY" if ts >= 70 else "UNCERTAIN / REVIEW" if ts >= 40 else "LOW TRUST"
        return d


# Initialize on import
init_db()
