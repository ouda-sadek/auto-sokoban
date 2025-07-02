import sqlite3
import os

DB_PATH = os.path.join("data", "scores.db")
print("Utilisation de la base :", DB_PATH)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level_name TEXT NOT NULL,
            player_name TEXT DEFAULT 'Anonymous',
            moves INTEGER NOT NULL,
            time REAL NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_score(level_name, moves, duration, player_name="Anonymous"):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO scores (level_name, player_name, moves, time)
        VALUES (?, ?, ?, ?)
    """, (level_name, player_name, moves, duration))
    conn.commit()
    conn.close()

def get_leaderboard(level_name=None, limit=5):
    conn = sqlite3.connect(DB_PATH)
    #conn = sqlite3.connect("data/scores.db")
    cursor = conn.cursor()
    if level_name:
        cursor.execute("""
            SELECT player_name, level_name, moves, time, date
            FROM scores
            WHERE level_name = ?
            ORDER BY moves ASC, time ASC
            LIMIT ?
        """, (level_name, limit))
        scores = cursor.fetchall()
        conn.close()
        return scores
    
    else:
        cursor.execute("""
            SELECT player_name, level_name, moves, time, date
            ORDER BY moves, time
            LIMIT ?
        """, (limit,))
        results = cursor.fetchall()
        conn.close()
        return results