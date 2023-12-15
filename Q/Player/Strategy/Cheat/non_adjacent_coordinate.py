from typing import List, Optional
from Q.Common.Board.tile import Tile
from Q.Player.Strategy.Cheat.cheat import Cheat
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.Strategy.dag import Dag
from Q.Common.Turn.turn import Turn
from Q.Common.Turn.turn_outcome import TurnOutcome
from Q.Util.pos_funcs import PosFuncs


class NonAdjacentCoordinate(Cheat):
    """
    Represents a cheater's interface for requesting a placement that is non-adjacent.
    """
    def cheat(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        player_strat = Dag()
        some_tile = player_strat.choose_tile(pub_data.current_map, hand)
        placement = player_strat.choose_position(pub_data.current_map, some_tile)
        while any(pub_data.current_map.get_neighbors(placement).values()):
            placement = PosFuncs.right(placement)
        return Turn(TurnOutcome.PLACED, placements={placement: some_tile})
