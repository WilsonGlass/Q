from Q.Common.game_state import GameState
from typing import List
from PIL import Image, ImageTk
from tkinter import filedialog, Frame, Button, Label, StringVar, LEFT, BOTH, TOP, Text, END, WORD, Scrollbar, Canvas
from Q.Util.util import Util
from json import dump

from Q.Common.render import Render

class ObserverGui(Frame):
    """
    Represents the GUI for the observer. Can seek through the game states provided.
    """
    def __init__(self, game_states: list[GameState], master=None):
        self.game_states = game_states
        self.curr_turn = 0

        Frame.__init__(self, master)
        self.master.title('Image Viewer')
        self.num_page_tv = StringVar()

        fram = Frame(self)
        Button(fram, text="Save", command=self.save).pack(side='left')
        Button(fram, text="Prev", command=self.seek_prev).pack(side='left')
        Button(fram, text="Next", command=self.seek_next).pack(side='left')
        Label(fram, textvariable=self.num_page_tv).pack(side='left')
        fram.pack(side='top', fill='both')

        max_canvas_height = 400
        max_canvas_width = 600
        self.canvas = Canvas(self, height=max_canvas_height, width=max_canvas_width)
        self.v_scrollbar = Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.h_scrollbar = Scrollbar(self, orient='horizontal', command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set, xscrollcommand=self.h_scrollbar.set)

        self.v_scrollbar.pack(side='right', fill='y')
        self.h_scrollbar.pack(side='bottom', fill='x')
        self.canvas.pack(side='top', fill='both', expand=True)

        self.canvas_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.canvas_frame, anchor='nw')

        if self.game_states:
            self.img = ImageTk.PhotoImage((Render(self.game_states[self.curr_turn].map.tiles).get_im()))
            self.la = Label(self.canvas_frame, image=self.img)
            self.la.pack()

        self.player_game_state_text = Text(self.canvas_frame, height=5, width=50, wrap='word', state='normal')
        self.player_game_state_text.pack()
        self.display_player_game_state()
        self.player_game_state_text.config(state='disabled')

        self.canvas_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.pack(fill='both', expand=True)

    def add_game_state(self, game_state: GameState):
        self.game_states.append(game_state)

    def save(self):
        """
        Saves to file directory
        """
        util = Util()
        filename_with_path = filedialog.asksaveasfilename() if len(self.game_states) else None
        if filename_with_path:
            filename_with_path = f"{filename_with_path}.json"
            jstate = util.convert_gamestate_to_jstate(self.game_states[self.curr_turn])
            with open(filename_with_path, "w") as fp:
                dump(jstate, fp)

    def get_curr_game_state(self):
        return self.game_states[self.curr_turn]

    def seek_prev(self):
        """
        Changes the current turn to the previous turn
        """
        if self.curr_turn != 0:
            self.curr_turn -= 1
            self.update_image()

    def seek_next(self):
        """
        Changes the current turn to the next turn
        """
        if self.curr_turn < len(self.game_states) - 1:
            self.curr_turn += 1
            self.update_image()

    def update_image(self):
        try:
            self.img = ImageTk.PhotoImage((Render(self.game_states[self.curr_turn].map.tiles).get_im()))
            self.la.configure(image=self.img)
            self.la.pack()
            self.display_player_game_state()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        except Exception as e:
            print(e)

    def display_player_game_state(self):
        """
        Displays all the current game state's information in plain text at the bottom of the window
        """
        if self.curr_turn < len(self.game_states):
            game_state = self.game_states[self.curr_turn]
            text_content = f"Number of referee tiles: {len(game_state.referee_deck)}\n\n"
            for pgs in game_state.players:
                text_content += (
                    f"Player Name: {pgs.name}\n"
                    f"Hand: {pgs.hand}\n"
                    f"{pgs.name}'s Points: {pgs.points}\n\n"
                )
            self.player_game_state_text.config(state="normal")
            self.player_game_state_text.delete(1.0, END)
            self.player_game_state_text.insert(END, text_content)
            self.player_game_state_text.config(state="disabled")
