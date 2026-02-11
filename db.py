
import mysql.connector

DB_NAME = "hstulibrary"

def init_db():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sadidalislam#1"
    )
    cur = con.cursor()

    cur.execute("CREATE DATABASE IF NOT EXISTS " + DB_NAME)
    cur.execute("USE " + DB_NAME)

    cur.execute("""CREATE TABLE IF NOT EXISTS books(
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(100),
        author VARCHAR(100),
        quantity INT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS students(
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        dept VARCHAR(50)
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS student_users(
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id INT,
        username VARCHAR(50) UNIQUE,
        password VARCHAR(100),
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS issued(
        id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT,
        student_id INT,
        issue_date DATE,
        return_date DATE
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS admin(
        username VARCHAR(50) PRIMARY KEY,
        password VARCHAR(50)
    )""")

    cur.execute("SELECT * FROM admin WHERE username='admin'")
    if not cur.fetchone():
        cur.execute("INSERT INTO admin VALUES('admin','admin123')")

    con.commit()
    con.close()

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sadidalislam#1",
        database=DB_NAME
    )
