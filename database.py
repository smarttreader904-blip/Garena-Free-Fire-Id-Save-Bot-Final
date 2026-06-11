# ==========================================
# database.py
# FF ID Management Bot Database
# Final Part 1
# ==========================================

import sqlite3
from datetime import datetime
import config

DB_NAME = config.DATABASE_NAME


# ==========================================
# DATABASE CONNECT
# ==========================================

def connect():
    return sqlite3.connect(DB_NAME)


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():
    conn = connect()
    cur = conn.cursor()

    # Users
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        name TEXT
    )
    """)

    # FF IDs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ff_ids (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        uid TEXT UNIQUE,
        nickname TEXT,
        category TEXT,
        status TEXT,
        views INTEGER DEFAULT 0,
        favorite INTEGER DEFAULT 0,
        created_at TEXT
    )
    """)

    # Pending
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pending (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        uid TEXT UNIQUE,
        nickname TEXT,
        category TEXT,
        created_at TEXT
    )
    """)

    # Logs
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT,
        admin_id INTEGER,
        uid TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


# ==========================================
# USER SYSTEM
# ==========================================

def add_user(user_id, name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT OR IGNORE INTO users(user_id, name) VALUES (?, ?)",
        (user_id, name)
    )

    conn.commit()
    conn.close()


def get_all_users():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users")
    data = cur.fetchall()

    conn.close()
    return data


def total_users():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")

    count = cur.fetchone()[0]

    conn.close()
    return count


# ==========================================
# FF ID SYSTEM
# ==========================================

def add_ff_id(user_id, uid, nickname, category):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO ff_ids
    (user_id, uid, nickname, category, status, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        uid,
        nickname,
        category,
        "approved",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_all_ff_ids():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM ff_ids")

    data = cur.fetchall()

    conn.close()
    return data


def total_ff_ids():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM ff_ids")

    count = cur.fetchone()[0]

    conn.close()
    return count


def get_ff_by_uid(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM ff_ids WHERE uid=?",
        (uid,)
    )

    data = cur.fetchone()

    conn.close()
    return data
    # ==========================================
# SEARCH / CATEGORY / RECENT
# Final Part 2
# ==========================================

def search_nickname(name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM ff_ids WHERE nickname LIKE ?",
        (f"%{name}%",)
    )

    data = cur.fetchall()

    conn.close()
    return data


def get_by_category(category):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM ff_ids WHERE category=?",
        (category,)
    )

    data = cur.fetchall()

    conn.close()
    return data


def recent_ids(limit=10):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM ff_ids ORDER BY id DESC LIMIT ?",
        (limit,)
    )

    data = cur.fetchall()

    conn.close()
    return data


def delete_ff_id(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM ff_ids WHERE uid=?",
        (uid,)
    )

    conn.commit()
    conn.close()


def edit_ff_id(uid, new_name):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE ff_ids SET nickname=? WHERE uid=?",
        (new_name, uid)
    )

    conn.commit()
    conn.close()


# ==========================================
# DUPLICATE CHECK
# ==========================================

def uid_exists(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT uid FROM ff_ids WHERE uid=?",
        (uid,)
    )

    if cur.fetchone():
        conn.close()
        return True

    cur.execute(
        "SELECT uid FROM pending WHERE uid=?",
        (uid,)
    )

    data = cur.fetchone()

    conn.close()
    return data is not None


# ==========================================
# PENDING SYSTEM
# ==========================================

def add_pending(user_id, uid, nickname, category):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO pending
    (user_id, uid, nickname, category, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        uid,
        nickname,
        category,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_pending_requests():
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM pending")

    data = cur.fetchall()

    conn.close()

    requests = []

    for row in data:
        requests.append({
            "id": row[0],
            "user_id": row[1],
            "uid": row[2],
            "nickname": row[3],
            "category": row[4]
        })

    return requests


def clear_pending():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM pending"
    )

    conn.commit()
    conn.close()


def approve_request(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM pending WHERE uid=?",
        (uid,)
    )

    data = cur.fetchone()

    if data:

        cur.execute("""
        INSERT INTO ff_ids
        (user_id, uid, nickname, category, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            data[1],
            data[2],
            data[3],
            data[4],
            "approved",
            datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        ))

        cur.execute(
            "DELETE FROM pending WHERE uid=?",
            (uid,)
        )

    conn.commit()
    conn.close()

    return data


def reject_request(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM pending WHERE uid=?",
        (uid,)
    )

    conn.commit()
    conn.close()
    # ==========================================
# VIEW COUNTER
# Final Part 3
# ==========================================

def increase_view(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE ff_ids SET views = views + 1 WHERE uid=?",
        (uid,)
    )

    conn.commit()
    conn.close()


def most_viewed():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT uid, views
    FROM ff_ids
    ORDER BY views DESC
    LIMIT 1
    """)

    data = cur.fetchone()

    conn.close()
    return data


def top_10_viewed():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT uid, nickname, views
    FROM ff_ids
    ORDER BY views DESC
    LIMIT 10
    """)

    data = cur.fetchall()

    conn.close()
    return data


# ==========================================
# FAVORITES
# ==========================================

def add_favorite(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE ff_ids SET favorite=1 WHERE uid=?",
        (uid,)
    )

    conn.commit()
    conn.close()


def remove_favorite(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "UPDATE ff_ids SET favorite=0 WHERE uid=?",
        (uid,)
    )

    conn.commit()
    conn.close()


def get_favorites():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM ff_ids WHERE favorite=1"
    )

    data = cur.fetchall()

    conn.close()
    return data


# ==========================================
# LOG SYSTEM
# ==========================================

def add_log(action, admin_id, uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO logs
    (action, admin_id, uid, date)
    VALUES (?, ?, ?, ?)
    """, (
        action,
        admin_id,
        uid,
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_logs():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM logs ORDER BY id DESC"
    )

    data = cur.fetchall()

    conn.close()
    return data


def get_logs_by_uid(uid):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM logs WHERE uid=? ORDER BY id DESC",
        (uid,)
    )

    data = cur.fetchall()

    conn.close()
    return data


def total_logs():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "SELECT COUNT(*) FROM logs"
    )

    count = cur.fetchone()[0]

    conn.close()
    return count


def clear_logs():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM logs"
    )

    conn.commit()
    conn.close()


# ==========================================
# AUTO CREATE DATABASE
# ==========================================

create_tables()
