import os

class LevelManager:
    def __init__(self, levels_folder="levels"):
        self.levels_folder = levels_folder
        self.level_files = sorted(
            [f for f in os.listdir(levels_folder) if f.endswith(".txt")]
        )
        self.current_index = 0

    def get_current_level_path(self):
        if self.current_index < len(self.level_files):
            return os.path.join(self.levels_folder, self.level_files[self.current_index])
        return None

    def next_level(self):
        self.current_index += 1
        if self.current_index < len(self.level_files):
            return self.get_current_level_path()
        # End of levels
        return None  

    def reset(self):
        self.current_index = 0
