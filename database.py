import psycopg2
import os
from dotenv import load_dotenv

load_dotenv() 

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")  # Added this line to load DB_PASS

def get_db_connection():
    try:
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        return connection
    except Exception as error:
        print(f"Error while connecting to database: {error}")
        return None

def store_chat_history(user_query, model_response):
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            insert_query = """
            INSERT INTO chat_history (user_query, model_response) VALUES (%s, %s);
            """
            cursor.execute(insert_query, (user_query, model_response))
            connection.commit()
        except Exception as e:
            print(f"Error storing chat history: {e}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to the database for storing chat history.")
