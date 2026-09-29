"""
Authentication and User Profile Database Manager for TrustGuard AI.
Handles user registration, password hashing (PBKDF2-HMAC-SHA256), session tokens, and profile preferences.
"""
import os
import time
import hashlib
import secrets
import sqlite3
from pathlib import Path
from typing import Optional, Dict, Any

DB_PATH = Path(__file__).resolve().parent.parent / "trustguard.db"
SESSION_DURATION_SEC = 30 * 24 * 3600  # 30 days session validity


def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_auth_db():
    """Initializes user and session tables if they don't exist and seeds default admin account."""
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                display_name TEXT NOT NULL,
                organization TEXT DEFAULT '',
                preferred_language TEXT DEFAULT 'en',
                theme TEXT DEFAULT 'dark',
                notifications_enabled INTEGER DEFAULT 1,
                created_at REAL NOT NULL,
                last_login REAL NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                created_at REAL NOT NULL,
                expires_at REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

        # Seed default admin user if not exists
        admin_row = conn.execute("SELECT id FROM users WHERE email = 'admin@trustguard.ai'").fetchone()
        if not admin_row:
            salt_hex = os.urandom(16).hex()
            pwd_hash = hash_password("password123", salt_hex)
            now = time.time()
            conn.execute("""
                INSERT INTO users (
                    email, password_hash, salt, display_name,
                    organization, preferred_language, theme,
                    notifications_enabled, created_at, last_login
                ) VALUES (?, ?, ?, ?, ?, 'en', 'dark', 1, ?, ?)
            """, ("admin@trustguard.ai", pwd_hash, salt_hex, "Lead SOC Analyst", "TrustGuard Cyber Defense", now, now))
            conn.commit()


def hash_password(password: str, salt_hex: str) -> str:
    """Computes PBKDF2-HMAC-SHA256 password hash."""
    salt_bytes = bytes.fromhex(salt_hex)
    pwd_bytes = password.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', pwd_bytes, salt_bytes, 100000)
    return key.hex()


def sanitize_user(row: sqlite3.Row) -> Dict[str, Any]:
    """Returns safe user dictionary without exposing password hash or salt."""
    return {
        "id": row["id"],
        "email": row["email"],
        "display_name": row["display_name"],
        "organization": row["organization"] or "",
        "preferred_language": row["preferred_language"] or "en",
        "theme": row["theme"] or "dark",
        "notifications_enabled": bool(row["notifications_enabled"]),
        "created_at": row["created_at"],
        "last_login": row["last_login"]
    }


def register_user(
    email: str,
    password: str,
    display_name: str,
    organization: str = ""
) -> Dict[str, Any]:
    """Registers a new user account."""
    init_auth_db()
    email_clean = email.strip().lower()
    if not email_clean or "@" not in email_clean:
        raise ValueError("Please provide a valid email address.")
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters long.")

    salt_hex = os.urandom(16).hex()
    pwd_hash = hash_password(password, salt_hex)
    now = time.time()
    disp_name = display_name.strip() or email_clean.split("@")[0].title()

    with get_db() as conn:
        try:
            cursor = conn.execute("""
                INSERT INTO users (
                    email, password_hash, salt, display_name,
                    organization, preferred_language, theme,
                    notifications_enabled, created_at, last_login
                ) VALUES (?, ?, ?, ?, ?, 'en', 'dark', 1, ?, ?)
            """, (email_clean, pwd_hash, salt_hex, disp_name, organization, now, now))
            user_id = cursor.lastrowid

            token = secrets.token_hex(24)
            expires = now + SESSION_DURATION_SEC
            conn.execute("""
                INSERT INTO sessions (token, user_id, created_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (token, user_id, now, expires))
            conn.commit()

            user_row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
            return {
                "success": True,
                "token": token,
                "user": sanitize_user(user_row)
            }
        except sqlite3.IntegrityError:
            raise ValueError("An account with this email address already exists.")


def login_user(email: str, password: str) -> Dict[str, Any]:
    """Authenticates a user and creates a new session token."""
    init_auth_db()
    email_clean = email.strip().lower()

    with get_db() as conn:
        user_row = conn.execute("SELECT * FROM users WHERE email = ?", (email_clean,)).fetchone()
        if not user_row:
            raise ValueError("Invalid email or password.")

        expected_hash = hash_password(password, user_row["salt"])
        if not secrets.compare_digest(expected_hash, user_row["password_hash"]):
            raise ValueError("Invalid email or password.")

        now = time.time()
        conn.execute("UPDATE users SET last_login = ? WHERE id = ?", (now, user_row["id"]))

        token = secrets.token_hex(24)
        expires = now + SESSION_DURATION_SEC
        conn.execute("""
            INSERT INTO sessions (token, user_id, created_at, expires_at)
            VALUES (?, ?, ?, ?)
        """, (token, user_row["id"], now, expires))
        conn.commit()

        # Fetch updated user
        updated_row = conn.execute("SELECT * FROM users WHERE id = ?", (user_row["id"],)).fetchone()
        return {
            "success": True,
            "token": token,
            "user": sanitize_user(updated_row)
        }


def logout_user(token: str) -> bool:
    """Invalidates a session token."""
    init_auth_db()
    if not token:
        return True
    with get_db() as conn:
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
    return True


def get_user_by_token(token: str) -> Optional[Dict[str, Any]]:
    """Retrieves authenticated user given a session token."""
    init_auth_db()
    if not token:
        return None

    now = time.time()
    with get_db() as conn:
        sess = conn.execute("""
            SELECT user_id, expires_at FROM sessions WHERE token = ?
        """, (token,)).fetchone()

        if not sess:
            return None

        if sess["expires_at"] < now:
            conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
            conn.commit()
            return None

        user_row = conn.execute("SELECT * FROM users WHERE id = ?", (sess["user_id"],)).fetchone()
        if not user_row:
            return None

        return sanitize_user(user_row)


def update_user_profile(
    user_id: int,
    display_name: Optional[str] = None,
    organization: Optional[str] = None,
    preferred_language: Optional[str] = None,
    theme: Optional[str] = None,
    notifications_enabled: Optional[bool] = None
) -> Dict[str, Any]:
    """Updates user profile and preferences."""
    init_auth_db()
    with get_db() as conn:
        user_row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        if not user_row:
            raise ValueError("User not found.")

        new_name = display_name.strip() if display_name is not None and display_name.strip() else user_row["display_name"]
        new_org = organization.strip() if organization is not None else user_row["organization"]
        new_lang = preferred_language if preferred_language is not None else user_row["preferred_language"]
        new_theme = theme if theme is not None else user_row["theme"]
        new_notif = 1 if (notifications_enabled if notifications_enabled is not None else bool(user_row["notifications_enabled"])) else 0

        conn.execute("""
            UPDATE users
            SET display_name = ?, organization = ?, preferred_language = ?, theme = ?, notifications_enabled = ?
            WHERE id = ?
        """, (new_name, new_org, new_lang, new_theme, new_notif, user_id))
        conn.commit()

        updated = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return sanitize_user(updated)


def seed_default_user_if_needed():
    """Ensures at least one default demonstrator user exists."""
    init_auth_db()
    with get_db() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            salt_hex = os.urandom(16).hex()
            pwd_hash = hash_password("trustguard2026", salt_hex)
            now = time.time()
            conn.execute("""
                INSERT INTO users (
                    email, password_hash, salt, display_name,
                    organization, preferred_language, theme,
                    notifications_enabled, created_at, last_login
                ) VALUES ('reshma@trustguard.ai', ?, ?, 'Reshma A.', 'TrustGuard AI Cyber Labs', 'en', 'dark', 1, ?, ?)
            """, (pwd_hash, salt_hex, now, now))
            conn.commit()


# Initialize on import
init_auth_db()
seed_default_user_if_needed()
