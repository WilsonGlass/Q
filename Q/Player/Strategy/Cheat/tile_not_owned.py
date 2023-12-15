from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook
from Q.Player.Strategy.Cheat.cheat import Cheat
from typing import List

from Q.Common.public_player_data import PublicPlayerData
from Q.Player.Strategy.dag import Dag
from Q.Player.Strategy.player_strategy import PlayerStrategy
from Q.Common.Turn.turn import Turn
from Q.Common.Turn.turn_outcome import TurnOutcome


class TileNotOwned(Cheat):
    """
    Represents a cheater's interface for requesting a placement for a tile it does not own.
    """
    def cheat(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        player_strat = Dag()
        possible_tiles = [Tile(shape, color) for color in TileColor for shape in TileShape]
        for tile in possible_tiles:
            if tile not in hand and Rulebook.get_legal_positions(pub_data.current_map, tile, []):
                return Turn(TurnOutcome.PLACED, {player_strat.choose_position(pub_data.current_map, tile): tile})
