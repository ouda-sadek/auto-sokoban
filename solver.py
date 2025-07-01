# solver.py

from collections import deque
from copy import deepcopy

MOVES = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0)
}

class SokobanSolver:
    def __init__(self, game_state):
        self.initial_state = deepcopy(game_state)
        self.map = self.initial_state.map

    def solve_bfs(self):
        return self._bfs()

    def solve_dfs(self):
        return self._dfs()

    def _bfs(self):
        visited = set()
        queue = deque()
        queue.append((self.initial_state.clone(), []))

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

    def _dfs(self, depth_limit=1000):
        visited = set()
        stack = [(self.initial_state.clone(), [])]

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
