from models.map import SokobanMap
from models.game_state import GameState

def render_console(game):
    grid = [[' ' for _ in range(len(game.map.grid[0]))] for _ in range(len(game.map.grid))]

    # Walls and targets
    for y, row in enumerate(game.map.grid):
        for x, cell in enumerate(row):
            if cell == -1:
                grid[y][x] = '#'
            elif (x, y) in game.map.targets:
                grid[y][x] = '.'

    # Boxes
    for box in game.boxes:
        x, y = box.position()
        grid[y][x] = '*' if (x, y) in game.map.targets else '$'

    # Player
    px, py = game.player.position()
    if grid[py][px] == '.':
        grid[py][px] = '+'
    else:
        grid[py][px] = '@'

    # Display
    for row in grid:
        print(''.join(row))
    print()

def main():
    sokomap = SokobanMap()
    sokomap.load_from_file('levels/level1.txt')
    game = GameState(sokomap)

    print("Controls: z=up, s=down, q=left, d=right, u=undo, x=quit\n")

    while True:
        render_console(game)
        if game.is_win():
            print("Victory !")
            break
        # Afficher les mouvements possibles
        dirs = {'z': (0, -1), 's': (0, 1), 'q': (-1, 0), 'd': (1, 0)}
        valid = [k for k, (dx, dy) in dirs.items() if game.is_valid_move(dx, dy)]
        print("Possible moves:", ' '.join(valid))

        cmd = input("Command : ")
        if cmd == 'z':
            game.move_player(0, -1)
        elif cmd == 's':
            game.move_player(0, 1)
        elif cmd == 'q':
            game.move_player(-1, 0)
        elif cmd == 'd':
            game.move_player(1, 0)
        elif cmd == 'u':
            game.undo()
        elif cmd == 'x':
            break
        else:
            print("Unknown command")

       


if __name__ == "__main__":
    main()
