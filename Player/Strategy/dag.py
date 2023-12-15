from typing import Dict, List
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.Board.tile import Tile

from Q.Player.Strategy.player_strategy import PlayerStrategy
from Q.Common.Turn.turn import Turn
from Q.Common.public_player_data import PublicPlayerData


class Dag(PlayerStrategy):
    """
    Represents the dag (dumb and greedy) player strategy.
    From assignment specs: Chooses the player's smallest tile that can extend the current map.
    If there is more than one place, it breaks the tie using the row-column order for the coordinates.
    """

    def get_turn(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        """
        Gets the turn object depending on the current public player data
        """
        return super().get_turn(pub_data, hand)

    def get_tile_placements(self, pub_data: PublicPlayerData, hand: List[Tile], placed_so_far: Dict[Pos, Tile] = {}) -> Dict[Pos, Tile]:
        """
        Return a dictionary of positions and tiles to place
        """
        return super().get_tile_placements(pub_data, hand, placed_so_far)

    def choose_position(self, given_map: Map, tile: Tile) -> Pos:
        """
        Get the position that a tile should be placed at
        """
        return super().choose_position(given_map, tile)

    def choose_tile(self, given_map: Map, filtered_hand: List[Tile]) -> Tile:
        """
        Get the tile that should be placed
        """
        return super().choose_tile(given_map, filtered_hand)

