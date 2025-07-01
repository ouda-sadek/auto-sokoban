import pygame
from models.map import SokobanMap
from models.game_state import GameState
from config.display_config import *
from level_manager import LevelManager



def draw_buttons(screen, font, width):
    buttons = {}
    labels = ["Undo", "Reset", "Quit"]
    for i, label in enumerate(labels):
        x = BUTTON_MARGIN + i * (BUTTON_WIDTH + BUTTON_MARGIN)
        y = BUTTON_MARGIN
        rect = pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT)
        buttons[label.lower()] = rect
        pygame.draw.rect(screen, (180, 180, 180), rect)
        text = font.render(label, True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=rect.center))
    return buttons

def draw_grid(screen, game, offset_x, offset_y):
    for y, row in enumerate(game.map.grid):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * TILE_SIZE + offset_x, y * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)

            pygame.draw.rect(screen, COLOR_FLOOR, rect)
            if cell == -1:
                pygame.draw.rect(screen, COLOR_WALL, rect)
            elif (x, y) in game.map.targets:
                pygame.draw.circle(screen, COLOR_TARGET, rect.center, TILE_SIZE // 4)

    for box in game.boxes:
        bx, by = box.position()
        rect = pygame.Rect(bx * TILE_SIZE, by * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)
        color = COLOR_BOX_OK if (bx, by) in game.map.targets else COLOR_BOX
        pygame.draw.rect(screen, color, rect.inflate(-10, -10))

    px, py = game.player.position()
    player_rect = pygame.Rect(px * TILE_SIZE, py * TILE_SIZE + offset_y, TILE_SIZE, TILE_SIZE)
    pygame.draw.circle(screen, COLOR_PLAYER, player_rect.center, TILE_SIZE // 3)

def main():
    pygame.init()
    font = pygame.font.SysFont(None, FONT_SIZE)
    clock = pygame.time.Clock()

    level_manager = LevelManager()
    level_path = level_manager.get_current_level_path()
    sokomap = SokobanMap()
    sokomap.load_from_file(level_path)
    game = GameState(sokomap)


    
    """grid_width = max(len(row) for row in game.map.grid) * TILE_SIZE
    #grid_width = len(game.map.grid[0]) * TILE_SIZE
    grid_height = len(game.map.grid) * TILE_SIZE
    screen_width = grid_width + 2 * GRID_MARGIN
    screen_height = grid_height + BUTTON_HEIGHT + 3 * BUTTON_MARGIN + 2 * GRID_MARGIN
    grid_offset_x = GRID_MARGIN
    grid_offset_y = BUTTON_HEIGHT + 2 * BUTTON_MARGIN + GRID_MARGIN
    """
    """grid_width = max(len(row) for row in game.map.grid) * TILE_SIZE
        grid_height = len(game.map.grid) * TILE_SIZE

        # Dimensions de la fenêtre plus larges pour permettre le centrage
        screen_width = grid_width + 2 * GRID_MARGIN
        screen_height = grid_height + BUTTON_HEIGHT + 3 * BUTTON_MARGIN + 2 * GRID_MARGIN

        # Crée la fenêtre avec ces dimensions
        screen = pygame.display.set_mode((screen_width, screen_height))

        # 🔥 Calcul du centrage dynamique
        grid_offset_x = (screen_width - grid_width) // 2

        space_below_buttons = screen_height - (BUTTON_HEIGHT + 2 * BUTTON_MARGIN)
        grid_offset_y = BUTTON_HEIGHT + 2 * BUTTON_MARGIN + (space_below_buttons - grid_height) // 2


        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Auto Sokoban")
    """

    grid_width = max(len(row) for row in game.map.grid) * TILE_SIZE
    grid_height = len(game.map.grid) * TILE_SIZE

    # Largeur minimum de la fenêtre pour avoir une vraie marge
    screen_width = max(grid_width + 2 * GRID_MARGIN, 800)
    screen_height = grid_height + BUTTON_HEIGHT + 3 * BUTTON_MARGIN + 2 * GRID_MARGIN

    grid_offset_x = (screen_width - grid_width) // 2
    grid_offset_y = BUTTON_HEIGHT + 2 * BUTTON_MARGIN + GRID_MARGIN

    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(COLOR_BG)

        # Draw the buttons
        buttons = draw_buttons(screen, font, grid_width)

        # Draw the grid
        #draw_grid(screen, game, BUTTON_HEIGHT + 2 * BUTTON_MARGIN)
        draw_grid(screen, game, grid_offset_x, grid_offset_y)

        pygame.display.flip()

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

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if buttons["undo"].collidepoint(mx, my):
                    game.undo()
                elif buttons["reset"].collidepoint(mx, my):
                    game.reset()
                elif buttons["quit"].collidepoint(mx, my):
                    running = False

        if game.is_win():
            print("Victory !")
            pygame.time.wait(1000)

            next_path = level_manager.next_level()
            if next_path:
                sokomap = SokobanMap()
                sokomap.load_from_file(next_path)
                game = GameState(sokomap)

            else:
                print("🏁 Tous les niveaux terminés.")
                pygame.time.wait(1000)
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
