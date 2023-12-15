from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook
from Q.Player.Strategy.Cheat.cheat import Cheat
from typing import List, Optional

from Q.Common.public_player_data import PublicPlayerData
from Q.Player.Strategy.player_strategy import PlayerStrategy
from Q.Common.Turn.turn import Turn
from Q.Common.Turn.turn_outcome import TurnOutcome


class NoFit(Cheat):
    """
    Represents a cheater's interface for requesting a placement that does not match an adjacent color/shape
    """
    def cheat(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Optional[Turn]:
        player_strat = PlayerStrategy()
        tile = player_strat.choose_tile(pub_data.current_map, hand)
        placement = player_strat.choose_position(pub_data.current_map, tile)
        neighbors = pub_data.current_map.get_neighbors(placement)
        possible_tiles = [Tile(shape, color) for color in TileColor for shape in TileShape]
        possible_tiles.remove(Tile(tile.shape, tile.color))
        tile_to_place = possible_tiles[0]
        for neighbor in neighbors:
            if neighbor not in pub_data.current_map.tiles.keys():
                return Turn(TurnOutcome.PLACED, {placement: tile_to_place})
