import pygame
from display_game import SokobanGameApp
from level_manager import LevelManager
from solver import SokobanSolver
from models.map import SokobanMap
from models.game_state import GameState


if __name__ == "__main__":
    app = SokobanGameApp()
    
    # Charger la map actuelle (niveau courant)
    level_path = app.level_manager.get_current_level_path()
    sokomap = SokobanMap()
    sokomap.load_from_file(level_path)
    
    # Lancer le solveur
    game_state = GameState(sokomap)
    solver = SokobanSolver(game_state)
    solution = solver.solve_bfs()  # ou solve_dfs()

    if solution:
        print("Solution trouvée :", solution)
        app.play_solution(solution)
    else:
        print("Aucune solution trouvée.")
