import os
import time
import psycopg2
from flask import Flask

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        dbname=os.environ.get("DB_NAME", "tododb"),
        user=os.environ.get("DB_USER", "user"),
        password=os.environ.get("DB_PASSWORD", "password")
    )

def init_db():
    for attempt in range(10):
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT,
                    done BOOLEAN DEFAULT FALSE
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("Database initialized successfully.")
            return
        except psycopg2.OperationalError as e:
            print(f"Attempt {attempt + 1}/10 — DB not ready: {e}")
            time.sleep(2)
    raise Exception("Could not connect to the database after 10 attempts.")

@app.route("/create/<title>")
def create_task(title):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (title) VALUES (%s)", (title,))
    conn.commit()
    cur.close()
    conn.close()
    return "created"

@app.route("/done/<int:task_id>")
def done_task(task_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE tasks SET done = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    cur.close()
    conn.close()
    return "updated"

@app.route("/pending")
def pending_tasks():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, title FROM tasks WHERE done = FALSE ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    result = "\n".join(f"{row[0]} {row[1]}" for row in rows)
    return result

@app.route("/stats")
def stats():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM tasks")
    total = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM tasks WHERE done = TRUE")
    done = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM tasks WHERE done = FALSE")
    pending = cur.fetchone()[0]
    cur.close()
    conn.close()
    return f"total: {total}\ndone: {done}\npending: {pending}"

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
