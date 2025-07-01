# test_all_levels.py

import os
import time
import csv
from models.map import SokobanMap
from models.game_state import GameState
from solver import SokobanSolver

LEVEL_DIR = "levels/"
RESULTS_CSV = "results/results_solver.csv"
ALGORITHMS = [("BFS", "solve_bfs"), ("DFS", "solve_dfs")]

def test_all_levels():
    print(f"📂 Test de tous les niveaux dans le dossier '{LEVEL_DIR}'\n")

    with open(RESULTS_CSV, mode="w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Level", "Algorithm", "Moves", "Time (s)", "Solution"])

        for filename in sorted(os.listdir(LEVEL_DIR)):
            if not filename.endswith(".txt"):
                continue

            level_path = os.path.join(LEVEL_DIR, filename)
            print(f"🧩 Niveau : {filename}")

            sokomap = SokobanMap()
            sokomap.load_from_file(level_path)

            for name, method in ALGORITHMS:
                solver = SokobanSolver(GameState(sokomap))
                start = time.time()
                solution = getattr(solver, method)()
                end = time.time()

                if solution:
                    moves = len(solution)
                    duration = round(end - start, 4)
                    print(f"   ✅ {name} → {moves} coups en {duration}s")
                    writer.writerow([filename, name, moves, duration, solution])
                else:
                    print(f"   ❌ {name} → Aucune solution trouvée")
                    writer.writerow([filename, name, "N/A", 0.0, "[]"])

            print("-" * 40)

    print(f"\n📝 Résultats enregistrés dans : {RESULTS_CSV}")

if __name__ == "__main__":
    test_all_levels()
