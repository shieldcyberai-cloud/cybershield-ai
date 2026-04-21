import sqlite3

DB_NAME = 'message_assistant_db.sqlite'

def create_connection():
    """Establishes a connection to the SQLite database."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row 
        return conn
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None

def init_db():
    """Initializes the database schema if it does not already exist."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS chats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    role TEXT,
                    message TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            """)
            conn.commit()
        except Exception as e:
            print(f"Database Initialization Error: {e}")
        finally:
            conn.close()

def register_user(username, email, password):
    """Registers a new operator node in the database with validation."""
    if not username.isalpha(): 
        return False, "Username must contain only alphabetic characters."
    if not email.endswith("@gmail.com"): 
        return False, "Only @gmail.com domains are permitted for registration."
    if len(password) < 6: 
        return False, "Access key must be at least 6 characters in length."

    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
            conn.commit()
            return True, "Account successfully provisioned. You may now authenticate."
        except sqlite3.IntegrityError: 
            return False, "This Operator ID is already registered in the system."
        finally: 
            conn.close()
    return False, "Internal database error occurred."

def login_user(username, password):
    """Authenticates a user against the database records."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    return None

def save_chat(user_id, role, message):
    """Persists chat telemetry to the database."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO chats (user_id, role, message) VALUES (?, ?, ?)", (user_id, role, message))
        conn.commit()
        conn.close()

def get_user_chats(user_id):
    """Retrieves conversation history for a specific user."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role, message FROM chats WHERE user_id = ? ORDER BY id ASC", (user_id,))
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
    return []

def clear_user_chats(user_id):
    """Purges all chat history associated with a specific user."""
    conn = create_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM chats WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

# ==================================================
# PASSWORD RECOVERY PROTOCOL
# ==================================================
def update_user_password(email, new_password):
    """Updates the user's access key after successful OTP verification."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
            conn.commit()
            success = cursor.rowcount > 0 
            return success
        except Exception as e:
            print(f"Password Update Error: {e}")
            return False
        finally:
            conn.close()
    return False

def get_username_by_email(email):
    """Fetches the username associated with the provided email for personalized recovery."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT username FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()
            if user:
                return user['username']
        except Exception as e:
            print(f"Error fetching username: {e}")
        finally:
            conn.close()
    return None