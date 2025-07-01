# solver_bfs.py

from collections import deque
from models.map import SokobanMap
from models.game_state import GameState



MOVES = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}


def bfs_solver(sokomap):
    initial_state = GameState(sokomap)
    visited = set()
    queue = deque()
    queue.append((initial_state, []))

    while queue:
        state, path = queue.popleft()
        key = state.get_hash()
        if key in visited:
            continue
        visited.add(key)

        if state.is_win():
            return path

        for direction, (dx, dy) in MOVES.items():
            new_state = state.clone()
            if new_state.move_player(dx, dy):
                queue.append((new_state, path + [direction]))

    return None

if __name__ == "__main__":
    from models.map import SokobanMap

    map_path = "levels/level1.txt"  # ou level2.txt etc.
    sokomap = SokobanMap()
    sokomap.load_from_file(map_path)

    solution = bfs_solver(sokomap)

    if solution:
        print("🧠 BFS Solution trouvée :", solution)
        print("✅ Nombre de coups :", len(solution))
    else:
        print("❌ Aucune solution trouvée.")

