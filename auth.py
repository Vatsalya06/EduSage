import sqlite3
import bcrypt

DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT UNIQUE,
        password_hash BLOB
    )
    """)
    conn.commit()
    conn.close()

# -------------------- REGISTER --------------------
def register_user(email, password, username):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    # Hash password as bytes
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        # Insert username, email, password_hash
        c.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, hashed)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Email already exists
        return False
    except Exception as e:
        print("Registration error:", e)
        return False
    finally:
        conn.close()

# -------------------- LOGIN --------------------
def validate_user(email, password):
    """
    Returns username if valid login, else False
    """
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT username, password_hash FROM users WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()

    if not row:
        return False

    username, stored_hash = row

    # Ensure stored_hash is bytes
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode()

    # Check password
    if bcrypt.checkpw(password.encode(), stored_hash):
        return username  # Return username on successful login
    else:
        return False
