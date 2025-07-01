class Box:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return self.x, self.y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def copy(self):
        return Box(self.x, self.y)

