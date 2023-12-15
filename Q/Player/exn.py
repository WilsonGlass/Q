from enum import Enum


class Exn(Enum):
    SETUP = "setup"
    TAKE_TURN = "take-turn"
    NEW_TILES = "new-tiles"
    WIN = "win"
