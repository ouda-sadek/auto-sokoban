import sqlite3

# Chemin vers ta base de données
DB_PATH = "data/scores.db"

# Connexion et interrogation du schéma
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(scores)")
print("Schéma de la table 'scores' :\n")
for row in cursor.fetchall():
    print(row)

conn.close()
