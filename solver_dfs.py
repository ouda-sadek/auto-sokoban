# solver_dfs.py

from models.map import SokobanMap
from models.game_state import GameState


MOVES = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}


def dfs_solver(sokomap, depth_limit=1000):
    initial_state = GameState(sokomap)
    visited = set()
    stack = [(initial_state, [])]

    while stack:
        state, path = stack.pop()
        if len(path) > depth_limit:
            continue

        key = state.get_hash()
        if key in visited:
            continue
        visited.add(key)

        if state.is_win():
            return path

        for direction, (dx, dy) in MOVES.items():
            new_state = state.clone()
            if new_state.move_player(dx, dy):
                stack.append((new_state, path + [direction]))

    return None

if __name__ == "__main__":
    from models.map import SokobanMap

    map_path = "levels/level1.txt"
    sokomap = SokobanMap()
    sokomap.load_from_file(map_path)

    solution = dfs_solver(sokomap, depth_limit=100)

    if solution:
        print("🧠 DFS Solution trouvée :", solution)
        print("✅ Nombre de coups :", len(solution))
    else:
        print("❌ Aucune solution trouvée.")

