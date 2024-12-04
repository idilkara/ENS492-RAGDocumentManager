HISTORY_SIZE = 2  # Keep only the last 2 queries and responses
GLOBAL_SESSION_ID = "global_session"  # Single global session ID
import sqlite3

def init_history_db():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            session_id TEXT,
            query TEXT,
            response TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_to_history(query, response):
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()

    # Remove the oldest entry if the history size exceeds the limit
    cursor.execute('SELECT COUNT(*) FROM history WHERE session_id = ?', (GLOBAL_SESSION_ID,))
    count = cursor.fetchone()[0]
    if count >= HISTORY_SIZE:
        print("HISTORY COUNT: ", count)
        cursor.execute('DELETE FROM history WHERE rowid IN (SELECT rowid FROM history WHERE session_id = ? ORDER BY rowid ASC LIMIT 1)', (GLOBAL_SESSION_ID,))

    # Add the new query and response to the history
    cursor.execute('INSERT INTO history (session_id, query, response) VALUES (?, ?, ?)',
                   (GLOBAL_SESSION_ID, query, response))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT query, response FROM history WHERE session_id = ? ORDER BY rowid ASC', (GLOBAL_SESSION_ID,))
    history = cursor.fetchall()
    conn.close()
    return history

# Initialize the history database
init_history_db()