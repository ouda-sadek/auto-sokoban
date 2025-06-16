class SokobanMap:
    def __init__(self, grid=None):
        self.grid = grid or []
        self.player_pos = None
        self.boxes = []
        self.targets = []

    def load_from_file(self, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()

        self.grid = []
        self.boxes = []
        self.targets = []

        for y, line in enumerate(lines):
            row = []
            for x, char in enumerate(line.strip()):
                if char == '#':
                    # Mur
                    row.append(-1)  
                elif char == '.':
                    # Cible
                    row.append(1)   
                    self.targets.append((x, y))
                elif char == '$':
                    # Caisse
                    row.append(2)   
                    self.boxes.append((x, y))
                elif char == '@':
                    # Joueur
                    row.append(0)   
                    self.player_pos = (x, y)
                elif char == '*':
                    row.append(2)
                    self.boxes.append((x, y))
                    self.targets.append((x, y))
                elif char == '+':
                    row.append(0)
                    self.player_pos = (x, y)
                    self.targets.append((x, y))
                else:
                    row.append(0)
            self.grid.append(row)

    def is_wall(self, x, y):
        return self.grid[y][x] == -1

    def in_bounds(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0])
