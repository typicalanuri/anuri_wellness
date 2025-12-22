import sqlite3

def get_db_connection():
    """Create a database connection to the SQLite database."""
    conn = sqlite3.connect('wellness_email.db')
    return conn

def get_email_history():
    """Fetch email history from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM email_history")
    emails = cursor.fetchall()
    conn.close()
    return emails

def save_email(email_data):
    """Save an email to the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO email_history (sender, recipient, subject, content) VALUES (?, ?, ?, ?)",
        (email_data['sender'], email_data['recipient'], email_data['subject'], email_data['content'])
    )
    conn.commit()
    conn.close()

def create_email_history_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE 
                   ''')