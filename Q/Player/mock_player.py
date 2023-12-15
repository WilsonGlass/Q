from copy import deepcopy
from typing import List

from Q.Common.Board.tile import Tile
from Q.Player.Strategy.dag import Dag
from Q.Player.exn import Exn
from Q.Common.Turn.turn import Turn

from Q.Player.Strategy.strategy import Strategy
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.base import Player


class MockPlayer(Player):
    """
    Represents a player that is mocked to have some certain kind of errors
    """
    def __init__(self, name, strategy: Strategy = Dag(), hand: List[Tile] = [], exn: Exn = Exn.SETUP):
        """
        # initializes a player with a given name, strategy and hand for the Q Game
        """
        self._name = name
        self.strategy = strategy
        self.hand = hand
        self.exn = exn

    def attempt_exception(self, exn):
        if self.exn == exn.value:
            raise Exception(f"{exn} method in player errored out")

    def name(self) -> str:
        return self._name

    def win(self, w: bool):
        """
        Raises an exception if called for. Otherwise runs the desired parents win method.
        """
        self.attempt_exception(Exn.WIN)
        if w:
            print("You won!")
        else:
            print("You lost!")

    def setup(self, pub_data: PublicPlayerData, tiles: List[Tile]):
        """
        Raises an exception if called for. Otherwise runs the desired parents setup method.
        """
        self.attempt_exception(Exn.SETUP)
        self.hand = pub_data.current_player_data.hand

    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        Raises an exception if called for. Otherwise runs the desired parents take turn method.
        """
        self.attempt_exception(Exn.TAKE_TURN)
        return self.strategy.get_turn(s, deepcopy(self.hand))

    def new_tiles(self, st: List[Tile]):
        """
        Raises an exception if called for. Otherwise runs the desired parents newTiles method.
        """
        self.attempt_exception(Exn.NEW_TILES)
        self.hand = st