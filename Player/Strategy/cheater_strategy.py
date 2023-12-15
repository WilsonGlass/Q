from Q.Player.Strategy.Cheat.cheat import Cheat
from typing import List
from Q.Common.Board.tile import Tile
from Q.Player.Strategy.strategy import Strategy
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.Strategy.player_strategy import PlayerStrategy
from Q.Common.Turn.turn import Turn


class CheaterStrategy(Strategy):
    """
    Represents a cheater's strategy. By default, the cheater strategy references its base strategy.
    E.g. dag, ldasg. Though, when a cheat is requested, get_turn in Cheater() will return a turn with
    said requested cheat.
    """
    def __init__(self, cheat: Cheat, strategy: PlayerStrategy):
        self.cheat = cheat
        self.strategy = strategy

    def get_turn(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        cheat_turn = self.cheat.get_turn(pub_data, hand)
        return cheat_turn if cheat_turn else self.strategy.get_turn(pub_data, hand)
