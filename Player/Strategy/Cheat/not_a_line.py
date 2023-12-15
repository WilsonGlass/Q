from typing import List

from Q.Common.Board.tile import Tile
from Q.Player.Strategy.Cheat.cheat import Cheat
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.Strategy.player_strategy import PlayerStrategy
from Q.Common.Turn.turn import Turn
from Q.Common.Turn.turn_outcome import TurnOutcome
from Q.Util.pos_funcs import PosFuncs


class NotALine(Cheat):
    """
    Represents a cheater's interface for requesting a placement that is non-contiguous
    """
    def cheat(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        player_strat = PlayerStrategy()
        copy_hand = hand.copy()
        tiles_to_play = []
        for _ in range(3):
            tile = player_strat.choose_tile(pub_data.current_map, copy_hand)
            tiles_to_play.append(tile)
            copy_hand.remove(tile)

        placement1 = player_strat.choose_position(pub_data.current_map, tiles_to_play[0])
        placement2 = PosFuncs.right(placement1)
        placement3 = PosFuncs.above(placement2)

        turn = {
            placement1: tiles_to_play[0],
            placement2: tiles_to_play[1],
            placement3: tiles_to_play[2]
        }
        return Turn(TurnOutcome.PLACED, turn)
