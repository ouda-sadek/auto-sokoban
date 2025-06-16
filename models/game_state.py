from models.player import Player
from copy import deepcopy

class GameState:
    def __init__(self, sokomap):
        self.map = sokomap
        px, py = sokomap.player_pos
        self.player = Player(px, py)
        self.history = []

    def is_target(self, x, y):
        return (x, y) in self.map.targets

    def move_player(self, dx, dy):
        nx, ny = self.player.x + dx, self.player.y + dy

        if not self.map.in_bounds(nx, ny) or self.map.is_wall(nx, ny):
            return False


        elif not self.map.is_wall(nx, ny):
            self.history.append(self.snapshot())

        self.player.move(dx, dy)
        return True

    def snapshot(self):
        return {
            "player": (self.player.x, self.player.y),
           
        }

    def undo(self):
        if self.history:
            state = self.history.pop()
            self.player.x, self.player.y = state["player"]
