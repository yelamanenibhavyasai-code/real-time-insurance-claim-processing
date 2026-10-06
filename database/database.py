import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).resolve().parent / "claims.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with get_connection() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS claims (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_id TEXT UNIQUE NOT NULL,
                policy_id TEXT NOT NULL,
                customer_id TEXT NOT NULL,
                claim_amount REAL NOT NULL,
                risk_score INTEGER NOT NULL,
                risk_level TEXT NOT NULL,
                status TEXT NOT NULL,
                processed_timestamp TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS fraud_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                claim_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                risk_score INTEGER NOT NULL,
                created_timestamp TEXT NOT NULL
            )
        ''')
        conn.commit()

def insert_claim(claim: dict):
    initialize_database()
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO claims
            (claim_id, policy_id, customer_id, claim_amount, risk_score,
             risk_level, status, processed_timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(claim_id) DO UPDATE SET
                risk_score=excluded.risk_score,
                risk_level=excluded.risk_level,
                status=excluded.status,
                processed_timestamp=excluded.processed_timestamp
        ''', (
            claim["claim_id"], claim["policy_id"], claim["customer_id"],
            claim["claim_amount"], claim["risk_score"], claim["risk_level"],
            claim["status"], claim["processed_timestamp"]
        ))
        conn.commit()

def insert_fraud_alert(claim_id: str, reason: str, risk_score: int, timestamp: str):
    initialize_database()
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO fraud_alerts
            (claim_id, reason, risk_score, created_timestamp)
            VALUES (?, ?, ?, ?)
        ''', (claim_id, reason, risk_score, timestamp))
        conn.commit()

def get_claim(claim_id: str) -> Optional[dict]:
    initialize_database()
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM claims WHERE claim_id = ?", (claim_id,)
        ).fetchone()
        return dict(row) if row else None

def get_all_claims() -> list[dict]:
    initialize_database()
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM claims ORDER BY id").fetchall()
        return [dict(row) for row in rows]
