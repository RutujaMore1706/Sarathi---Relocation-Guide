import duckdb
import pandas as pd
from datetime import datetime

def init_duckdb_connection():
    return duckdb.connect('saarthi_conversation.db')

def create_table(conn):
    conn.execute("""
         CREATE TABLE IF NOT EXISTS saarthi_talks (
             conversation_id TEXT,
             name TEXT,
             rating INT,
             summary TEXT,
             feedback TEXT,
             message_count INT,
             summary_timestamp TIMESTAMP
         );
     """)

def get_all_records(conn):
    return conn.execute("SELECT * FROM saarthi_talks").fetchdf()

def get_filtered_records(conn, rating, date):
    query = """
    SELECT * FROM saarthi_talks
    WHERE rating = ?
    AND CAST(summary_timestamp as DATE) = ?
    """
    return conn.execute(query, [rating, date]).fetchdf()

def insert_text(conn, conversation_id, extracted_preference, msg):
    summary_timestamp = datetime.now()
    conn.execute(
        "INSERT INTO saarthi_talks (conversation_id, summary, message_count, summary_timestamp) VALUES (?, ?, ?, ?)",
        (conversation_id, extracted_preference, msg, summary_timestamp)
    )
    conn.commit()

def update_text(conn, conversation_id, feedback, rating, name):
    conn.execute("""
        UPDATE saarthi_talks
        SET feedback = ?,
            rating = ?,
            name = ?
        WHERE conversation_id = ?
    """, (feedback, rating, name, conversation_id))
    conn.commit()


def get_total_users(conn):
    result = conn.execute("SELECT COUNT(DISTINCT name) AS total_users FROM saarthi_talks").fetchone()
    return result[0]

def get_daily_active_users(conn, date):
    query = """
        SELECT COUNT(DISTINCT name) AS daily_active_users
        FROM saarthi_talks
        WHERE CAST(summary_timestamp as DATE) = ?;
    """
    result = conn.execute(query, [date]).fetchone()
    return result[0]