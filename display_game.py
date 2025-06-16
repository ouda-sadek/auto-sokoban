import pygame
from models.map import SokobanMap
from models.game_state import GameState
from config.display_config import (
    TILE_SIZE, FPS,
    COLOR_BG, COLOR_WALL, COLOR_FLOOR,
    COLOR_TARGET, COLOR_BOX, COLOR_BOX_OK, COLOR_PLAYER
)



def draw_grid(screen, game):
    for y, row in enumerate(game.map.grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

            # Wallpaper
            pygame.draw.rect(screen, COLOR_FLOOR, rect)

            # Wall
            if cell == -1:
                pygame.draw.rect(screen, COLOR_WALL, rect)
            # Target
            elif (x, y) in game.map.targets:
                pygame.draw.circle(screen, COLOR_TARGET, rect.center, TILE_SIZE // 4)

    # Boxes
    for box in game.boxes:
        bx, by = box.position()
        rect = pygame.Rect(bx * TILE_SIZE, by * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        color = COLOR_BOX_OK if (bx, by) in game.map.targets else COLOR_BOX
        pygame.draw.rect(screen, color, rect.inflate(-10, -10))

    # Player
    px, py = game.player.position()
    player_rect = pygame.Rect(px * TILE_SIZE, py * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.circle(screen, COLOR_PLAYER, player_rect.center, TILE_SIZE // 3)

def main():
    pygame.init()
    clock = pygame.time.Clock()

    # Load level and status
    sokomap = SokobanMap()
    sokomap.load_from_file("levels/level1.txt")
    game = GameState(sokomap)

    # Determine the window size
    width = len(game.map.grid[0]) * TILE_SIZE
    height = len(game.map.grid) * TILE_SIZE
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Auto Sokoban")

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                dx, dy = 0, 0
                if event.key == pygame.K_z:
                    dy = -1
                elif event.key == pygame.K_s:
                    dy = 1
                elif event.key == pygame.K_q:
                    dx = -1
                elif event.key == pygame.K_d:
                    dx = 1

                if dx or dy:
                    game.move_player(dx, dy)

        screen.fill(COLOR_BG)
        draw_grid(screen, game)
        pygame.display.flip()

        if game.is_win():
            print("🎉 Victory !")
            pygame.time.wait(1500)
            running = False

    pygame.quit()

if __name__ == "__main__":
    main()
