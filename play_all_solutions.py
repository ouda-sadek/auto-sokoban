import csv
import time
import pygame
from display_game import SokobanGameApp
from level_manager import LevelManager

CSV_PATH = "results/results_solver.csv"

"""def read_solutions_from_csv(csv_path):
    solutions = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            path = "levels/" + row["Level"]
            algo = row["algorithm"]
            solution = row["solution"].strip("[]").replace("'", "").split(", ")
            if solution != ['']:
                solutions.append((path, algo, solution))
    return solutions"""

def read_solutions_from_csv(csv_path):
    solutions = []
    with open(csv_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            path = "levels/" + row["Level"]
            algo = row["Algorithm"]
            solution_str = row["Solution"]
            if solution_str.strip("[]").strip():
                moves = solution_str.strip("[]").replace("'", "").split(", ")
                solutions.append((path, algo, moves))
    return solutions



def main():
    pygame.init()
    solutions = read_solutions_from_csv(CSV_PATH)
    
    for level_path, algo, moves in solutions:
        print(f"\n🧩 Niveau : {level_path} | Algo : {algo}")
        app = SokobanGameApp(level_path_override=level_path)
        app.display_message(f"{algo} - {level_path}", pause=1.5)
        app.play_solution(moves, delay=0.2)
        time.sleep(1)  # Pause entre les niveaux

    print("\n🎉 Toutes les solutions ont été jouées.")
    pygame.quit()

if __name__ == "__main__":
    main()
