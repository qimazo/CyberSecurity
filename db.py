
from datetime import datetime
import sqlite3

DB_FILE = "phishing.db"


def get_summary():
    """Get small report numbers from the database."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM results")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(confidence) FROM results")
    average_confidence = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results WHERE prediction = 'phishing'")
    phishing_count = cursor.fetchone()[0]

    connection.close()

    if average_confidence is None:
        average_confidence = 0

    legit_count = total - phishing_count

    return {
        "total": total,
        "phishing_count": phishing_count,
        "legit_count": legit_count,
        "avg_confidence": average_confidence,
    }


def get_history(limit=20):
    """Get the last saved results. Newest results come first."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    sql = """
        SELECT id, prediction, confidence, email_text, date_checked
        FROM results
        ORDER BY id DESC
        LIMIT ?
    """

    cursor.execute(sql, (limit,))
    results = cursor.fetchall()

    connection.close()
    return results


def save_result(email_text, prediction, confidence, links_found, warning_signs):
    """Save one email check result in the database."""
    checked_time = datetime.now().strftime("%Y-%m-%d %H:%M")

    if warning_signs is None:
        warning_text = ""
    else:
        warning_text = ", ".join(warning_signs)

    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    sql = """
        INSERT INTO results
        (email_text, prediction, confidence, links_found, warning_signs, date_checked)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    values = (
        email_text,
        prediction,
        confidence,
        links_found,
        warning_text,
        checked_time,
    )

    cursor.execute(sql, values)
    connection.commit()
    connection.close()


def create_table():
    """Make the results table if it does not already exist."""
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    sql = """
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email_text TEXT,
            prediction TEXT,
            confidence REAL,
            links_found INTEGER,
            warning_signs TEXT,
            date_checked TEXT
        )
    """

    cursor.execute(sql)
    connection.commit()
    connection.close()
