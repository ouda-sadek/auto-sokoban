import pygame
from models.map import SokobanMap
from models.game_state import GameState
from config.display_config import *
from level_manager import LevelManager
from sprite_loader import SpriteLoader
from database import save_score
import time
from database import get_leaderboard





class SokobanGameApp:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont(None, FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.level_manager = LevelManager()
        self.load_level()
        self.sprite_loader = SpriteLoader("assets/images", TILE_SIZE)
        self.player_direction = "down"
        self.player_frame = 0
        self.player_frame_timer = 0
        self.move_count = 0
        self.start_time = time.time()



    def load_level(self):
        level_path = self.level_manager.get_current_level_path()
        self.sokomap = SokobanMap()
        self.sokomap.load_from_file(level_path)
        self.game = GameState(self.sokomap)
        self.setup_display()

    def setup_display(self):
        self.grid_width = max(len(row) for row in self.game.map.grid) * TILE_SIZE
        self.grid_height = len(self.game.map.grid) * TILE_SIZE
        self.screen_width = WINDOW_WIDTH
        self.screen_height = WINDOW_HEIGHT
        self.grid_offset_x = (self.screen_width - self.grid_width) // 2
        self.grid_offset_y = BUTTON_HEIGHT + 2 * BUTTON_MARGIN + GRID_MARGIN

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Auto Sokoban")

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            self.screen.fill(COLOR_BG)
            buttons = self.draw_buttons()
            self.draw_grid()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos, buttons)

            if self.game.is_win():
                pygame.time.wait(1000)

                duration = round(time.time() - self.start_time, 2)
                level_name = self.level_manager.get_current_level_path()
                save_score(level_name, self.move_count, duration)

                # Affichage du leaderboard (top 5)
                print("\n Niveau terminé ! Voici le classement :")
                print(f" Niveau : {level_name}")
                scores = get_leaderboard(level_name)
                for i, (name, moves, t, date) in enumerate(scores, 1):
                    print(f"{i}. {name} - {moves} coups - {t}s - {date}")

                if self.level_manager.next_level():
                    self.load_level()
                    self.move_count = 0
                    self.start_time = time.time()

                else:
                    print("Tous les niveaux terminés.")
                    running = False

        pygame.quit()

    def draw_buttons(self):
        buttons = {}
        labels = ["Undo", "Reset", "Quit"]
        for i, label in enumerate(labels):
            x = BUTTON_MARGIN + i * (BUTTON_WIDTH + BUTTON_MARGIN)
            y = BUTTON_MARGIN
            rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
            buttons[label.lower()] = rect
            pygame.draw.rect(self.screen, (180, 180, 180), rect)
            text = self.font.render(label, True, (0, 0, 0))
            self.screen.blit(text, text.get_rect(center=rect.center))
        return buttons

    def draw_grid(self):
        for y, row in enumerate(self.game.map.grid):
            for x, cell in enumerate(row):
                pos = (
                    x * TILE_SIZE + self.grid_offset_x,
                    y * TILE_SIZE + self.grid_offset_y
                )

                # 1. Floor display (always)
                self.screen.blit(self.sprite_loader.get("floor"), pos)

                # 2. Wall
                if cell == -1:
                    self.screen.blit(self.sprite_loader.get("wall"), pos)

                # 3. Target
                elif (x, y) in self.game.map.targets:
                    self.screen.blit(self.sprite_loader.get("target"), pos)

        # Boxes display
        for box in self.game.boxes:
            bx, by = box.position()
            pos = (
                bx * TILE_SIZE + self.grid_offset_x,
                by * TILE_SIZE + self.grid_offset_y
            )
            sprite = self.sprite_loader.get("box_ok") if (bx, by) in self.game.map.targets else self.sprite_loader.get("box")
            self.screen.blit(sprite, pos)

        # Player display
        px, py = self.game.player.position()
        pos = (
            px * TILE_SIZE + self.grid_offset_x,
            py * TILE_SIZE + self.grid_offset_y
        )
        sprite = self.sprite_loader.get("player")[self.player_direction][self.player_frame]
        self.screen.blit(sprite, pos)



    def handle_key(self, key):
        dx, dy = 0, 0
        if key == pygame.K_z:
            dy = -1
            self.player_direction = "up"
        elif key == pygame.K_s:
            dy = 1
            self.player_direction = "down"
        elif key == pygame.K_q:
            dx = -1
            self.player_direction = "left"
        elif key == pygame.K_d:
            dx = 1
            self.player_direction = "right"

        if dx or dy:
            moved = self.game.move_player(dx, dy)
            if moved:
                self.move_count += 1
                # if effective movement, move to the next frame
                frames_list = self.sprite_loader.get("player")[self.player_direction]
                nb_frames = len(frames_list)
                self.player_frame = (self.player_frame + 1) % nb_frames  




    def handle_click(self, pos, buttons):
        mx, my = pos
        if buttons["undo"].collidepoint(mx, my):
            self.game.undo()
        elif buttons["reset"].collidepoint(mx, my):
            self.game.reset()
        elif buttons["quit"].collidepoint(mx, my):
            pygame.quit()
            exit()
