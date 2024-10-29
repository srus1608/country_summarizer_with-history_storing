from database import get_db_connection
from datetime import datetime

def create_chat_history_table():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS chat_history (
            id SERIAL PRIMARY KEY,
            query TEXT NOT NULL,
            summary TEXT NOT NULL,
            country_name TEXT NOT NULL,  -- Added country_name field
            timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        connection.close()

def store_chat_history(query, summary, name):
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        insert_query = """
        INSERT INTO chat_history (query, summary, name, timestamp)
        VALUES (%s, %s, %s, %s);
        """
        cursor.execute(insert_query, (query, summary, name, datetime.now()))
        connection.commit()
        cursor.close()
        connection.close()


def fetch_chat_history():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        select_query = """
        SELECT query, summary, timestamp FROM chat_history ORDER BY timestamp DESC;
        """
        cursor.execute(select_query)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()

        # Adjust the history list to exclude 'country_name' if it doesn't exist
        history = [{'query': row[0], 'summary': row[1], 'timestamp': row[2].strftime('%Y-%m-%d %H:%M:%S')} for row in rows]
        return history
    return []

