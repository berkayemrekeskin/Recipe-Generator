import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

def create_connection():
    """Creates a connection to the MySQL database."""
    try:
        load_dotenv()

        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password="Berkay2003",
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            print("Successfully connected to the database")
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None