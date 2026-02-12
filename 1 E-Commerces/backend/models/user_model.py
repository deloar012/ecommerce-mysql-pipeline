from backend.models.db import mysql_connection


def check_email_exists(email):
    with mysql_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )
        return cursor.fetchone() is not None


def create_user(full_name, email, mobile, password_hash):
    with mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (full_name, email, mobile, password_hash)
            VALUES (%s, %s, %s, %s)
            """,
            (full_name, email, mobile, password_hash)
        )
        conn.commit()
        return cursor.lastrowid


def get_user_by_email(email):
    with mysql_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT id AS user_id, full_name, email, mobile, password_hash
            FROM users WHERE email = %s
            """,
            (email,)
        )
        return cursor.fetchone()


def update_user_password(email, new_password_hash):
    with mysql_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE users SET password_hash = %s
            WHERE email = %s
            """,
            (new_password_hash, email)
        )
        conn.commit()
        return cursor.rowcount > 0
