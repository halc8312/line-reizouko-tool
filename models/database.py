import os
import psycopg2
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def init_db():
    try:
        result = urlparse(os.getenv("DATABASE_URL"))
        connection = psycopg2.connect(
            dbname=result.path[1:],
            user=result.username,
            password=result.password,
            host=result.hostname,
            port=result.port
        )
        cursor = connection.cursor()
        # Example queries to create tables if they don't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                expiration_date DATE NOT NULL,
                quantity INTEGER NOT NULL,
                user_id VARCHAR(100) NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id VARCHAR(100) PRIMARY KEY,
                username VARCHAR(100) NOT NULL
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

def get_db_connection():
    result = urlparse(os.getenv("DATABASE_URL"))
    return psycopg2.connect(
        dbname=result.path[1:],
        user=result.username,
        password=result.password,
        host=result.hostname,
        port=result.port
    )

def add_item(user_id, name, expiration_date, quantity):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO items (name, expiration_date, quantity, user_id)
                    VALUES (%s, %s, %s, %s)
                ''', (name, expiration_date, quantity, user_id))
                connection.commit()
        return True
    except Exception as e:
        print(f"Error adding item: {e}")
        return False

def get_items(user_id):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    SELECT name, expiration_date, quantity FROM items WHERE user_id = %s
                ''', (user_id,))
                items = cursor.fetchall()
        return items
    except Exception as e:
        print(f"Error fetching items: {e}")
        return []

def delete_item(user_id, name):
    try:
        with get_db_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute('''
                    DELETE FROM items WHERE user_id = %s AND name = %s
                ''', (user_id, name))
                connection.commit()
        return True
    except Exception as e:
        print(f"Error deleting item: {e}")
        return False
