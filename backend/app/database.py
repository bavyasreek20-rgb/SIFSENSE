import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = os.getenv("SIFSENSE_DB_PATH", str(Path(__file__).resolve().parent.parent / "sifsense.db"))


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                report_text TEXT NOT NULL,
                site TEXT NOT NULL,
                activity TEXT NOT NULL,
                report_type TEXT NOT NULL,
                classification TEXT NOT NULL,
                severity_score INTEGER NOT NULL,
                evidence_json TEXT NOT NULL,
                life_saving_rules_json TEXT NOT NULL,
                recommendation TEXT NOT NULL,
                disclaimer TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_report(payload: Dict[str, Any]) -> int:
    import json
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO reports (
                report_text, site, activity, report_type, classification,
                severity_score, evidence_json, life_saving_rules_json,
                recommendation, disclaimer
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            payload["report_text"], payload["site"], payload["activity"],
            payload["report_type"], payload["classification"], payload["severity_score"],
            json.dumps(payload["evidence"]), json.dumps(payload["life_saving_rules"]),
            payload["recommendation"], payload["disclaimer"]
        ))
        conn.commit()
        return int(cursor.lastrowid)


def row_to_dict(row):
    import json
    item = dict(row)
    item["evidence"] = json.loads(item.pop("evidence_json"))
    item["life_saving_rules"] = json.loads(item.pop("life_saving_rules_json"))
    return item


def list_reports(limit: int = 100) -> List[Dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM reports ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [row_to_dict(row) for row in rows]


def get_report(report_id: int) -> Optional[Dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM reports WHERE id = ?", (report_id,)).fetchone()
    return row_to_dict(row) if row else None


def get_summary() -> Dict[str, Any]:
    with get_connection() as conn:
        row = conn.execute("""
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN classification = 'SIF-Potential' THEN 1 ELSE 0 END) AS sif,
                   SUM(CASE WHEN classification = 'Non-SIF-Potential' THEN 1 ELSE 0 END) AS non_sif,
                   AVG(severity_score) AS avg_score
            FROM reports
        """).fetchone()
    return {
        "total_reports": row["total"] or 0,
        "sif_potential": row["sif"] or 0,
        "non_sif_potential": row["non_sif"] or 0,
        "average_severity_score": round(row["avg_score"] or 0, 2),
    }
