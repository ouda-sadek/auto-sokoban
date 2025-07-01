import pygame
import os

class SpriteLoader:
    def __init__(self, image_dir, tile_size):
        self.tile_size = tile_size
        self.image_dir = image_dir
        self.sprites = {}
        self.load_all()

    def load(self, name, filename):
        path = os.path.join(self.image_dir, filename)
        image = pygame.image.load(path).convert_alpha()
        image = pygame.transform.scale(image, (self.tile_size, self.tile_size))
        self.sprites[name] = image

    def load_all(self):
        # Sol généré en gris clair
        floor = pygame.Surface((self.tile_size, self.tile_size))
        floor.fill((200, 200, 200))  # gris clair
        self.sprites["floor"] = floor

        # Images chargées depuis les fichiers
        self.load("wall", "wall.png")
        self.load("box", "box.png")
        self.load("box_ok", "valid_box.png")
        self.load("target", "target.png")
        #self.load("player", "player_sprites.png")  # ou découpe plus tard si besoin
        self.load_player_sheet("player", "player_sprites.png")

    def load_player_sheet(self, name, filename):
        path = os.path.join(self.image_dir, filename)
        sheet = pygame.image.load(path).convert_alpha()

        directions = ["down", "left", "right", "up"]
        frames = {}

        for row, direction in enumerate(directions):
            frames[direction] = []
            for col in range(3):
                frame = sheet.subsurface(pygame.Rect(col * 32, row * 32, 32, 32))
                frame = pygame.transform.scale(frame, (self.tile_size, self.tile_size))
                frames[direction].append(frame)

        self.sprites[name] = frames



    def get(self, name):
        return self.sprites.get(name)
