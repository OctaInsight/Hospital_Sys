"""
Lightweight SQLite data layer for the prototype.
One database file (hospital.db) is shared by every module, mirroring the
"one app, one system, one database" design discussed in the proposal.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "hospital.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create tables if they don't exist and seed demo data on first run."""
    conn = get_conn()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name_en TEXT NOT NULL,
            name_ar TEXT NOT NULL,
            role TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mrn TEXT UNIQUE NOT NULL,
            name_en TEXT NOT NULL,
            name_ar TEXT NOT NULL,
            phone TEXT
        );

        CREATE TABLE IF NOT EXISTS queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            department TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'waiting',
            created_at TEXT NOT NULL,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );

        CREATE TABLE IF NOT EXISTS medication_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            medicine TEXT NOT NULL,
            dosage TEXT,
            instructions TEXT,
            ordered_by TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            updated_at TEXT,
            FOREIGN KEY (patient_id) REFERENCES patients(id)
        );

        CREATE TABLE IF NOT EXISTS complaints (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'open',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caller_name TEXT NOT NULL,
            phone TEXT,
            purpose TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )
    conn.commit()

    # Seed demo users (only if table is empty)
    if cur.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0:
        demo_users = [
            ("admin", "admin123", "Administrator", "مدير النظام", "admin"),
            ("doctor", "doctor123", "Dr. Sarah Ahmed", "د. سارة أحمد", "doctor"),
            ("pharmacist", "pharm123", "Mona Youssef", "منى يوسف", "pharmacist"),
            ("reception", "recep123", "Ali Mostafa", "علي مصطفى", "reception"),
            ("callcenter", "call123", "Heba Nabil", "هبة نبيل", "call_center"),
            ("pr", "pr123", "Karim Adel", "كريم عادل", "pr"),
        ]
        cur.executemany(
            "INSERT INTO users (username, password, name_en, name_ar, role) VALUES (?, ?, ?, ?, ?)",
            demo_users,
        )

    # Seed demo patients
    if cur.execute("SELECT COUNT(*) FROM patients").fetchone()[0] == 0:
        demo_patients = [
            ("MRN-1001", "Mohamed Ibrahim", "محمد إبراهيم", "01000000001"),
            ("MRN-1002", "Fatma El Sayed", "فاطمة السيد", "01000000002"),
            ("MRN-1003", "Youssef Khaled", "يوسف خالد", "01000000003"),
            ("MRN-1004", "Nour Hassan", "نور حسن", "01000000004"),
        ]
        cur.executemany(
            "INSERT INTO patients (mrn, name_en, name_ar, phone) VALUES (?, ?, ?, ?)",
            demo_patients,
        )

    conn.commit()
    conn.close()


def now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


# ---------- Users ----------
def authenticate(username: str, password: str):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM users WHERE username = ? AND password = ?", (username, password)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


# ---------- Patients ----------
def list_patients():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM patients ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------- Queue ----------
def add_to_queue(patient_id: int, department: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO queue (patient_id, department, status, created_at) VALUES (?, ?, 'waiting', ?)",
        (patient_id, department, now()),
    )
    conn.commit()
    conn.close()


def list_queue(department: str | None = None):
    conn = get_conn()
    query = """
        SELECT q.id, q.department, q.status, q.created_at,
               p.name_en, p.name_ar, p.mrn
        FROM queue q JOIN patients p ON p.id = q.patient_id
    """
    params = ()
    if department:
        query += " WHERE q.department = ?"
        params = (department,)
    query += " ORDER BY q.id"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_queue_status(queue_id: int, status: str):
    conn = get_conn()
    conn.execute("UPDATE queue SET status = ? WHERE id = ?", (status, queue_id))
    conn.commit()
    conn.close()


# ---------- Medication orders ----------
def create_medication_order(patient_id: int, medicine: str, dosage: str, instructions: str, ordered_by: str):
    conn = get_conn()
    conn.execute(
        """INSERT INTO medication_orders
           (patient_id, medicine, dosage, instructions, ordered_by, status, created_at)
           VALUES (?, ?, ?, ?, ?, 'pending', ?)""",
        (patient_id, medicine, dosage, instructions, ordered_by, now()),
    )
    conn.commit()
    conn.close()


def list_medication_orders(status: str | None = None, ordered_by: str | None = None):
    conn = get_conn()
    query = """
        SELECT m.*, p.name_en, p.name_ar, p.mrn
        FROM medication_orders m JOIN patients p ON p.id = m.patient_id
    """
    conditions, params = [], []
    if status:
        conditions.append("m.status = ?")
        params.append(status)
    if ordered_by:
        conditions.append("m.ordered_by = ?")
        params.append(ordered_by)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY m.id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_medication_status(order_id: int, status: str):
    conn = get_conn()
    conn.execute(
        "UPDATE medication_orders SET status = ?, updated_at = ? WHERE id = ?",
        (status, now(), order_id),
    )
    conn.commit()
    conn.close()


# ---------- Complaints ----------
def create_complaint(description: str, patient_id: int | None = None):
    conn = get_conn()
    conn.execute(
        "INSERT INTO complaints (patient_id, description, status, created_at) VALUES (?, ?, 'open', ?)",
        (patient_id, description, now()),
    )
    conn.commit()
    conn.close()


def list_complaints(status: str | None = None):
    conn = get_conn()
    query = "SELECT * FROM complaints"
    params = ()
    if status:
        query += " WHERE status = ?"
        params = (status,)
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def update_complaint_status(complaint_id: int, status: str):
    conn = get_conn()
    conn.execute("UPDATE complaints SET status = ? WHERE id = ?", (status, complaint_id))
    conn.commit()
    conn.close()


# ---------- Calls ----------
def log_call(caller_name: str, phone: str, purpose: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO calls (caller_name, phone, purpose, created_at) VALUES (?, ?, ?, ?)",
        (caller_name, phone, purpose, now()),
    )
    conn.commit()
    conn.close()


def list_calls():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM calls ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]
