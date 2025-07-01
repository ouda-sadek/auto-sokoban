from display_game import SokobanGameApp
from database import init_db
init_db()

if __name__ == "__main__":
    app = SokobanGameApp()
    app.run()
