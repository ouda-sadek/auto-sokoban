from models.player import Player
from models.box import Box
from models.map import SokobanMap
from copy import deepcopy

class GameState:
    def __init__(self, sokomap: SokobanMap):
        self.initial_map = sokomap
        self.map = deepcopy(sokomap)
        self.player = Player(*self.map.player_pos)
        self.boxes = [Box(x, y) for (x, y) in self.map.boxes]
        self.history = []

    def snapshot(self):
        return {
            'player': (self.player.x, self.player.y),
            'boxes': [(box.x, box.y) for box in self.boxes]
        }

    def restore_snapshot(self, snapshot):
        self.player.x, self.player.y = snapshot['player']
        for box, (x, y) in zip(self.boxes, snapshot['boxes']):
            box.x, box.y = x, y

    def move_player(self, dx, dy):
        if not self.is_valid_move(dx, dy):
            return False

        nx, ny = self.player.x + dx, self.player.y + dy

        self.history.append(self.snapshot())

        # Push a box
        if self.is_box(nx, ny):
            box = self.get_box_at(nx, ny)
            box.move(dx, dy)

        self.player.move(dx, dy)
        return True

    def undo(self):
        if self.history:
            snapshot = self.history.pop()
            self.restore_snapshot(snapshot)

    def reset(self):
        # Reloads the initial map
        self.__init__(deepcopy(self.initial_map))  

    def is_box(self, x, y):
        return any(box.position() == (x, y) for box in self.boxes)

    def get_box_at(self, x, y):
        for box in self.boxes:
            if box.position() == (x, y):
                return box
        return None

    def is_valid_move(self, dx, dy):
        nx, ny = self.player.x + dx, self.player.y + dy
        if not self.map.in_bounds(nx, ny) or self.map.is_wall(nx, ny):
            return False

        if self.is_box(nx, ny):
            bx, by = nx + dx, ny + dy
            if not self.map.in_bounds(bx, by) or self.map.is_wall(bx, by) or self.is_box(bx, by):
                return False

        return True

    def is_win(self):
        return all((box.x, box.y) in self.map.targets for box in self.boxes)
