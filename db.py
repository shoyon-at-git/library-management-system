from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import mysql.connector
from mysql.connector import MySQLConnection

from utils.security import hash_password


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_ENV_FILE = BASE_DIR / ".env"


def _load_env_file() -> None:
    """Load a local .env file without requiring python-dotenv."""
    env_path = Path(os.getenv("LMS_ENV_FILE", DEFAULT_ENV_FILE))
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


_load_env_file()

DB_HOST = os.getenv("LMS_DB_HOST", "localhost")
DB_PORT = int(os.getenv("LMS_DB_PORT", "3306"))
DB_USER = os.getenv("LMS_DB_USER", "root")
DB_PASSWORD = os.getenv("LMS_DB_PASSWORD", "")
DB_NAME = os.getenv("LMS_DB_NAME", "hstulibrary")
DEFAULT_ADMIN_USERNAME = os.getenv("LMS_DEFAULT_ADMIN_USERNAME", "admin")
DEFAULT_ADMIN_PASSWORD = os.getenv("LMS_DEFAULT_ADMIN_PASSWORD", "admin123")


class DatabaseConfigurationError(RuntimeError):
    """Raised when the database is not configured or reachable."""



def _connection_kwargs(database: Optional[str] = None) -> dict:
    kwargs = {
        "host": DB_HOST,
        "port": DB_PORT,
        "user": DB_USER,
        "password": DB_PASSWORD,
    }
    if database:
        kwargs["database"] = database
    return kwargs



def _get_server_connection() -> MySQLConnection:
    try:
        return mysql.connector.connect(**_connection_kwargs())
    except mysql.connector.Error as exc:
        raise DatabaseConfigurationError(
            "Unable to connect to MySQL. Check your .env settings and confirm MySQL is running."
        ) from exc



def get_connection() -> MySQLConnection:
    try:
        return mysql.connector.connect(**_connection_kwargs(DB_NAME))
    except mysql.connector.Error as exc:
        raise DatabaseConfigurationError(
            f"Unable to connect to database '{DB_NAME}'. Run the app once to initialize the schema, "
            "or verify your .env credentials."
        ) from exc



def table_exists(table_name: str) -> bool:
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute("SHOW TABLES LIKE %s", (table_name,))
        return cur.fetchone() is not None
    finally:
        cur.close()
        con.close()



def column_exists(table_name: str, column_name: str) -> bool:
    con = get_connection()
    cur = con.cursor()
    try:
        cur.execute(f"SHOW COLUMNS FROM {table_name} LIKE %s", (column_name,))
        return cur.fetchone() is not None
    finally:
        cur.close()
        con.close()



def _column_exists_with_cursor(cur, table_name: str, column_name: str) -> bool:
    cur.execute(f"SHOW COLUMNS FROM {table_name} LIKE %s", (column_name,))
    return cur.fetchone() is not None



def _ensure_column(cur, table_name: str, column_name: str, definition: str) -> None:
    cur.execute(f"SHOW COLUMNS FROM {table_name} LIKE %s", (column_name,))
    if not cur.fetchone():
        cur.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}")



def _index_exists(cur, table_name: str, index_name: str) -> bool:
    cur.execute(f"SHOW INDEX FROM {table_name} WHERE Key_name = %s", (index_name,))
    return cur.fetchone() is not None



def _ensure_index(cur, table_name: str, index_name: str, ddl: str) -> None:
    if not _index_exists(cur, table_name, index_name):
        cur.execute(ddl)



def _foreign_key_exists(cur, table_name: str, constraint_name: str) -> bool:
    cur.execute(
        "SELECT CONSTRAINT_NAME FROM information_schema.TABLE_CONSTRAINTS "
        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND CONSTRAINT_TYPE='FOREIGN KEY' AND CONSTRAINT_NAME=%s",
        (DB_NAME, table_name, constraint_name),
    )
    return cur.fetchone() is not None



def _drop_fk_if_exists(cur, table_name: str, constraint_name: str) -> None:
    if _foreign_key_exists(cur, table_name, constraint_name):
        cur.execute(f"ALTER TABLE {table_name} DROP FOREIGN KEY {constraint_name}")



def _get_primary_key_columns(cur, table_name: str) -> list[str]:
    cur.execute(
        "SELECT COLUMN_NAME FROM information_schema.KEY_COLUMN_USAGE "
        "WHERE TABLE_SCHEMA=%s AND TABLE_NAME=%s AND CONSTRAINT_NAME='PRIMARY' "
        "ORDER BY ORDINAL_POSITION",
        (DB_NAME, table_name),
    )
    return [row[0] for row in cur.fetchall()]



def _has_unique_index_on_column(cur, table_name: str, column_name: str) -> bool:
    cur.execute(f"SHOW INDEX FROM {table_name} WHERE Column_name = %s", (column_name,))
    for row in cur.fetchall():
        # SHOW INDEX columns: Key_name, Column_name, Non_unique, ...
        non_unique = row[1] if len(row) > 1 else None
        key_name = row[2] if len(row) > 2 else None
        if key_name == "PRIMARY" or non_unique == 0:
            return True
    return False



def _get_column_type(cur, table_name: str, column_name: str) -> str | None:
    cur.execute(f"SHOW COLUMNS FROM {table_name} LIKE %s", (column_name,))
    row = cur.fetchone()
    return str(row[1]).lower() if row else None



def _ensure_student_id_columns_are_text(cur) -> None:
    """Normalize student_id columns to VARCHAR so alphanumeric IDs like STU100A work."""
    if table_exists("student_users"):
        _drop_fk_if_exists(cur, "student_users", "fk_student_users_student")
    if table_exists("issued"):
        _drop_fk_if_exists(cur, "issued", "fk_issued_student")

    # Parent table first.
    if table_exists("students"):
        col_type = _get_column_type(cur, "students", "student_id")
        if col_type and "varchar" not in col_type:
            cur.execute("ALTER TABLE students MODIFY COLUMN student_id VARCHAR(20) NOT NULL")

    # Child tables next so FK recreation sees matching types.
    if table_exists("student_users"):
        col_type = _get_column_type(cur, "student_users", "student_id")
        if col_type and "varchar" not in col_type:
            cur.execute("ALTER TABLE student_users MODIFY COLUMN student_id VARCHAR(20) NOT NULL")

    if table_exists("issued"):
        col_type = _get_column_type(cur, "issued", "student_id")
        if col_type and "varchar" not in col_type:
            cur.execute("ALTER TABLE issued MODIFY COLUMN student_id VARCHAR(20) NOT NULL")


def _ensure_students_keys(cur) -> None:
    """Make students.id the primary key and students.student_id uniquely indexed."""
    if not table_exists("students"):
        return

    # Child FKs must be out of the way before we reshape indexes on students.
    _drop_fk_if_exists(cur, "student_users", "fk_student_users_student")
    _drop_fk_if_exists(cur, "issued", "fk_issued_student")

    if not _column_exists_with_cursor(cur, "students", "id"):
        cur.execute("ALTER TABLE students ADD COLUMN id INT NOT NULL AUTO_INCREMENT UNIQUE FIRST")

    id_col = None
    cur.execute("SHOW COLUMNS FROM students LIKE 'id'")
    id_col = cur.fetchone()
    if id_col:
        col_type = str(id_col[1]).lower()
        nullable = str(id_col[2]).upper()
        extra = str(id_col[5]).lower() if len(id_col) > 5 else ""

        # Make sure id behaves like the durable internal identifier.
        if nullable != "NO" or "int" not in col_type:
            cur.execute("ALTER TABLE students MODIFY COLUMN id INT NOT NULL")
        if not _has_unique_index_on_column(cur, "students", "id"):
            cur.execute("ALTER TABLE students ADD UNIQUE INDEX uq_students_id (id)")
        if "auto_increment" not in extra:
            cur.execute("ALTER TABLE students MODIFY COLUMN id INT NOT NULL AUTO_INCREMENT")

    primary_key_columns = _get_primary_key_columns(cur, "students")
    if primary_key_columns != ["id"]:
        if primary_key_columns:
            cur.execute("ALTER TABLE students DROP PRIMARY KEY")
        cur.execute("ALTER TABLE students ADD PRIMARY KEY (id)")

    if not _has_unique_index_on_column(cur, "students", "student_id"):
        cur.execute("ALTER TABLE students ADD UNIQUE INDEX uq_students_student_id (student_id)")



def _rebuild_student_foreign_keys(cur) -> None:
    # At this point students.student_id must already be indexed uniquely.
    _drop_fk_if_exists(cur, "student_users", "fk_student_users_student")
    cur.execute(
        "ALTER TABLE student_users ADD CONSTRAINT fk_student_users_student "
        "FOREIGN KEY (student_id) REFERENCES students(student_id) "
        "ON DELETE CASCADE ON UPDATE CASCADE"
    )

    _drop_fk_if_exists(cur, "issued", "fk_issued_student")
    cur.execute(
        "ALTER TABLE issued ADD CONSTRAINT fk_issued_student "
        "FOREIGN KEY (student_id) REFERENCES students(student_id) "
        "ON DELETE CASCADE ON UPDATE CASCADE"
    )



def _cleanup_orphan_student_refs(cur) -> None:
    """Remove broken child rows that reference non-existent students before re-adding FKs."""
    if table_exists("student_users"):
        cur.execute(
            """
            DELETE su FROM student_users su
            LEFT JOIN students s ON s.student_id = su.student_id
            WHERE s.student_id IS NULL
            """
        )

    if table_exists("issued"):
        cur.execute(
            """
            DELETE i FROM issued i
            LEFT JOIN students s ON s.student_id = i.student_id
            WHERE s.student_id IS NULL
            """
        )


def _seed_default_admin(cur) -> None:
    cur.execute("SELECT username FROM admin WHERE username=%s", (DEFAULT_ADMIN_USERNAME,))
    if cur.fetchone():
        return

    password_hash, salt = hash_password(DEFAULT_ADMIN_PASSWORD)
    if _column_exists_with_cursor(cur, "admin", "password"):
        cur.execute(
            "INSERT INTO admin(username, password, password_hash, password_salt) VALUES(%s,%s,%s,%s)",
            (DEFAULT_ADMIN_USERNAME, None, password_hash, salt),
        )
    else:
        cur.execute(
            "INSERT INTO admin(username, password_hash, password_salt) VALUES(%s,%s,%s)",
            (DEFAULT_ADMIN_USERNAME, password_hash, salt),
        )



def _migrate_legacy_passwords(cur) -> None:
    if _column_exists_with_cursor(cur, "admin", "password"):
        cur.execute(
            "SELECT username, password FROM admin WHERE (password_hash IS NULL OR password_hash='') "
            "AND password IS NOT NULL AND password <> ''"
        )
        for username, plain_password in cur.fetchall():
            password_hash, salt = hash_password(plain_password)
            cur.execute(
                "UPDATE admin SET password_hash=%s, password_salt=%s WHERE username=%s",
                (password_hash, salt, username),
            )

    if _column_exists_with_cursor(cur, "student_users", "password"):
        cur.execute(
            "SELECT id, password FROM student_users WHERE (password_hash IS NULL OR password_hash='') "
            "AND password IS NOT NULL AND password <> ''"
        )
        for row_id, plain_password in cur.fetchall():
            password_hash, salt = hash_password(plain_password)
            cur.execute(
                "UPDATE student_users SET password_hash=%s, password_salt=%s WHERE id=%s",
                (password_hash, salt, row_id),
            )



def init_db() -> None:
    server_con = _get_server_connection()
    server_cur = server_con.cursor()
    try:
        server_cur.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        server_cur.execute(f"USE `{DB_NAME}`")

        server_cur.execute(
            """
            CREATE TABLE IF NOT EXISTS books(
                id INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(100) NOT NULL,
                author VARCHAR(100) NOT NULL,
                quantity INT NOT NULL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        server_cur.execute(
            """
            CREATE TABLE IF NOT EXISTS students(
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20) NOT NULL UNIQUE,
                name VARCHAR(100) NOT NULL,
                dept VARCHAR(50) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                session VARCHAR(30),
                birth_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        server_cur.execute(
            """
            CREATE TABLE IF NOT EXISTS student_users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id VARCHAR(20) NOT NULL,
                username VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(255),
                password_hash VARCHAR(128),
                password_salt VARCHAR(64),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_student_users_student
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
            """
        )

        server_cur.execute(
            """
            CREATE TABLE IF NOT EXISTS issued(
                id INT AUTO_INCREMENT PRIMARY KEY,
                book_id INT NOT NULL,
                student_id VARCHAR(20) NOT NULL,
                issue_date DATE NOT NULL,
                due_date DATE NOT NULL,
                return_date DATE NULL,
                fine_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
                fine_paid TINYINT(1) NOT NULL DEFAULT 0,
                fine_paid_at DATETIME NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_issued_book
                    FOREIGN KEY (book_id) REFERENCES books(id)
                    ON DELETE RESTRICT,
                CONSTRAINT fk_issued_student
                    FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE
                    ON UPDATE CASCADE
            )
            """
        )

        server_cur.execute(
            """
            CREATE TABLE IF NOT EXISTS admin(
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(255),
                password_hash VARCHAR(128),
                password_salt VARCHAR(64),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Backfill missing columns for already-existing databases.
        _ensure_column(server_cur, "books", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(server_cur, "students", "email", "VARCHAR(150) NULL")
        _ensure_column(server_cur, "students", "session", "VARCHAR(30) NULL")
        _ensure_column(server_cur, "students", "birth_date", "DATE NULL")
        _ensure_column(server_cur, "students", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(server_cur, "student_users", "password", "VARCHAR(255) NULL")
        _ensure_column(server_cur, "student_users", "password_hash", "VARCHAR(128) NULL")
        _ensure_column(server_cur, "student_users", "password_salt", "VARCHAR(64) NULL")
        _ensure_column(server_cur, "student_users", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(server_cur, "issued", "due_date", "DATE NULL")
        _ensure_column(server_cur, "issued", "fine_amount", "DECIMAL(10, 2) NOT NULL DEFAULT 0")
        _ensure_column(server_cur, "issued", "fine_paid", "TINYINT(1) NOT NULL DEFAULT 0")
        _ensure_column(server_cur, "issued", "fine_paid_at", "DATETIME NULL")
        _ensure_column(server_cur, "issued", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        _ensure_column(server_cur, "admin", "password", "VARCHAR(255) NULL")
        _ensure_column(server_cur, "admin", "password_hash", "VARCHAR(128) NULL")
        _ensure_column(server_cur, "admin", "password_salt", "VARCHAR(64) NULL")
        _ensure_column(server_cur, "admin", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

        _ensure_student_id_columns_are_text(server_cur)
        _ensure_students_keys(server_cur)

        _ensure_index(server_cur, "issued", "idx_issued_student_id", "CREATE INDEX idx_issued_student_id ON issued(student_id)")
        _ensure_index(server_cur, "issued", "idx_issued_book_id", "CREATE INDEX idx_issued_book_id ON issued(book_id)")
        _ensure_index(server_cur, "issued", "idx_issued_return_date", "CREATE INDEX idx_issued_return_date ON issued(return_date)")

        _cleanup_orphan_student_refs(server_cur)
        _rebuild_student_foreign_keys(server_cur)
        _migrate_legacy_passwords(server_cur)
        _seed_default_admin(server_cur)

        # Best-effort backfill of missing student emails for old rows.
        server_cur.execute("SELECT student_id, name, email FROM students")
        for student_id, name, email in server_cur.fetchall():
            if not email:
                clean_name = "".join(ch for ch in name if ch.isalnum()).lower() or "student"
                generated_email = f"{clean_name}{student_id}@hstu.ac.bd"
                server_cur.execute(
                    "UPDATE students SET email=%s WHERE student_id=%s",
                    (generated_email, student_id),
                )

        server_con.commit()
    finally:
        server_cur.close()
        server_con.close()
