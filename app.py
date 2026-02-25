from fastapi import FastAPI, HTTPException
import sqlite3
import random
import time
from pathlib import Path

app = FastAPI(title="New Relic APM Demo with DB")

DB_PATH = Path("demo.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.on_event("startup")
def startup():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.get("/")
def root():
    delay = random.uniform(0.1, 1.5)
    time.sleep(delay)

    if random.random() < 0.2:
        raise HTTPException(status_code=500, detail="Simulated application error")

    return {
        "message": "FastAPI + SQLite + New Relic",
        "latency_seconds": round(delay, 2)
    }

@app.get("/users")
def get_users():
    # Simulate slow database query
    if random.random() < 0.3:
        time.sleep(1.2)

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        conn.close()

        return {"users": [dict(row) for row in rows]}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database query failed")

@app.post("/users")
def create_user():
    # Simulate occasional DB write failure
    if random.random() < 0.15:
        raise HTTPException(status_code=500, detail="Simulated DB insert failure")

    name = f"user_{random.randint(1, 1000)}"
    email = f"{name}@example.com"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )
    conn.commit()
    conn.close()

    return {"status": "created", "name": name}

@app.get("/health")
def health():
    if random.random() < 0.1:
        raise HTTPException(status_code=503, detail="Service unhealthy")
    return {"status": "ok"}