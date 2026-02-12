import mysql.connector
from mysql.connector import pooling
from backend.config import DB_CONFIG
from contextlib import contextmanager

print("✓ MySQL Connection Pool created successfully")

connection_pool = pooling.MySQLConnectionPool(
    pool_name="ecommerce_pool",
    pool_size=5,
    pool_reset_session=True,
    **DB_CONFIG
)

@contextmanager
def mysql_connection():
    conn = connection_pool.get_connection()
    try:
        yield conn
    finally:
        conn.close()


# Create connection pool
try:
    connection_pool = pooling.MySQLConnectionPool(
        pool_name="shophub_pool",
        pool_size=5,
        **DB_CONFIG
    )
    print("✓ MySQL Connection Pool created successfully")
except mysql.connector.Error as err:
    print(f"✗ Error creating connection pool: {err}")
    connection_pool = None

@contextmanager
def get_db_cursor(dictionary=True):
    """
    Context manager for database operations
    Usage:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    connection = None
    cursor = None
    
    try:
        connection = connection_pool.get_connection()
        cursor = connection.cursor(dictionary=dictionary)
        yield cursor
        connection.commit()
    except Exception as e:
        if connection:
            connection.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_connection():
    """Get a database connection from the pool"""
    return connection_pool.get_connection()