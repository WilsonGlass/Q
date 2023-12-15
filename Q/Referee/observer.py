from Q.Common.game_state import GameState
from Q.Referee.observer_gui import ObserverGui
from typing import List
from os import path, listdir, remove
from git import Repo

from Q.Common.render import Render


class Observer:
    """
    Observer component with which dev ops can watch and inspect a game from a referee’s perspective.
    In a typical game, the observer will be updated with a game state once per turn. To view the game states
    added to the observer, run the make_gui() method.
    """
    def __init__(self, game_states: List[GameState] = []):
        self.game_states: List[GameState] = game_states
        self.game_ended = False

        for game_state in game_states:
            self.save_png(game_state)

    def receive_a_state(self, game_state: GameState):
        """
        Consumes a state
        Informs the observer of a change in state before a turn is completed and at the very end of the game.
        """
        if not self.game_ended:
            self.game_states.append(game_state)
            self.save_png(game_state)

    def save_png(self, game_state: GameState):
        """
        Saves a given map to the tmp folder as a png
        """
        repo_path = Repo(search_parent_directories=True).working_tree_dir
        directory_path = path.join(repo_path, "Q", "Referee", "Tmp")
        self.wipe_tmp(directory_path)
        files = listdir(directory_path)
        list_of_files = list(map((lambda filename: int(filename[0])), files))

        new_png_index = f"{str(max(list_of_files) + 1)}.png" if len(list_of_files) else "0.png"
        Render(game_state.map.tiles).get_im().save(path.join(directory_path, new_png_index))

    def wipe_tmp(self, directory_path: str):
        """
        Wipes the tmp folder where game state pngs live
        """
        for filename in listdir(directory_path):
            file_path = path.join(directory_path, filename)
            if path.isfile(file_path):
                remove(file_path)

    def game_over(self):
        """
        Called when the referee shuts down since the observer is only wired into the referee on demand.
        """
        self.game_ended = True
        self.make_gui()

    def make_gui(self):
        """
        Creates the GUI to view the referee's game states.
        """
        gui = ObserverGui(self.game_states)
        gui.mainloop()
