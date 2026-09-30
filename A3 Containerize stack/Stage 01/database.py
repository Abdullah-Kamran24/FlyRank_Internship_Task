import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

db = psycopg.connect(DATABASE_URL)

cmnd = db.cursor()

cmnd.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title TEXT,
        done BOOLEAN
    )
""")

cmnd.execute("SELECT COUNT(*) FROM tasks")

count = cmnd.fetchone()[0]

if count == 0:
    cmnd.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s)",
        ("LEARN POSTGRESQL", False)
    )

    cmnd.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s)",
        ("BUILD FAST API", False)
    )

    cmnd.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s)",
        ("FINISH ASSIGNMENT", True)
    )

db.commit()