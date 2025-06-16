from models.player import Player
from models.box import Box
from copy import deepcopy

class GameState:
    def __init__(self, sokomap):
        self.map = sokomap
        px, py = sokomap.player_pos
        self.player = Player(px, py)
        self.boxes = [Box(x, y) for (x, y) in sokomap.boxes]
        self.history = []

    def get_box_at(self, x, y):
        for box in self.boxes:
            if box.position() == (x, y):
                return box
        return None

    def is_box(self, x, y):
        return self.get_box_at(x, y) is not None

    def is_target(self, x, y):
        return (x, y) in self.map.targets

    """ def move_player(self, dx, dy):
        
        nx, ny = self.player.x + dx, self.player.y + dy

        if not self.map.in_bounds(nx, ny) or self.map.is_wall(nx, ny):
            return False

        if self.is_box(nx, ny):
            bx, by = nx + dx, ny + dy
            if not self.map.in_bounds(bx, by) or self.map.is_wall(bx, by) or self.is_box(bx, by):
                return False
            # Move box
            box = self.get_box_at(nx, ny)
            self.history.append(self.snapshot())
            box.move(dx, dy)

        elif not self.map.is_wall(nx, ny):
            self.history.append(self.snapshot())

        self.player.move(dx, dy)
        return True"""
    

    def move_player(self, dx, dy):
        if not self.is_valid_move(dx, dy):
            return False

        nx, ny = self.player.x + dx, self.player.y + dy

        # S'il y a une caisse, on la pousse
        if self.is_box(nx, ny):
            box = self.get_box_at(nx, ny)
            self.history.append(self.snapshot())
            box.move(dx, dy)
        else:
            self.history.append(self.snapshot())

        self.player.move(dx, dy)
        return True


    def snapshot(self):
        return {
            "player": (self.player.x, self.player.y),
            "boxes": [(box.x, box.y) for box in self.boxes]
        }

    def undo(self):
        if self.history:
            state = self.history.pop()
            self.player.x, self.player.y = state["player"]
            for box, (x, y) in zip(self.boxes, state["boxes"]):
                box.x, box.y = x, y

    def is_win(self):
        return all((box.x, box.y) in self.map.targets for box in self.boxes)
    
    def is_valid_move(self, dx, dy):
        nx, ny = self.player.x + dx, self.player.y + dy

        # 1. Outside the limits
        if not self.map.in_bounds(nx, ny):
            return False

        # 2. Wall in front
        if self.map.is_wall(nx, ny):
            return False

        # 3. Cash register in front
        if self.is_box(nx, ny):
            bx, by = nx + dx, ny + dy
            # Cannot push out of bounds or against a wall or another crate
            if (not self.map.in_bounds(bx, by) or
                self.map.is_wall(bx, by) or
                self.is_box(bx, by)):
                return False

        return True

