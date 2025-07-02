import sqlite3
import os

DB_PATH = os.path.join("data", "scores.db")

def reset_scores_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Supprimer l’ancienne table si elle existe
    cursor.execute("DROP TABLE IF EXISTS scores")

    # Recréer la table avec la bonne structure
    cursor.execute("""
        CREATE TABLE scores (
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
    print(" Table 'scores' supprimée et recréée avec succès.")

if __name__ == "__main__":
    reset_scores_table()
