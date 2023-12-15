from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from Q import Util
from Q.Common.Board.pos import Pos
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook
from Q.Player.Strategy.strategy import Strategy
from Q.Common.public_player_data import PublicPlayerData
from Q.Common.Turn.turn import Turn
from Q.Common.Turn.turn_outcome import TurnOutcome


class PlayerStrategy(Strategy, ABC):
    """
    Represents a strategy that a well behaving player would employ
    """
    def get_turn(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        """
        Gets the turn object depending on the current public player data
        """
        if Rulebook.get_legal_hand(pub_data.current_map, hand, []):
            return Turn(TurnOutcome.PLACED, self.get_tile_placements(pub_data, hand, {}))
        if pub_data.num_ref_tiles < len(hand):
            return Turn(TurnOutcome.PASSED, {})
        return Turn(TurnOutcome.REPLACED, {})

    @abstractmethod
    def get_tile_placements(self, pub_data: PublicPlayerData, hand: List[Tile], placed_so_far: Dict[Pos, Tile] = {}) -> Dict[Pos, Tile]:
        """
        Return a dictionary of positions and tiles to place
        """
        tile = self.choose_tile(pub_data.current_map, hand)
        if tile:
            position_to_place_tile = self.choose_position(pub_data.current_map, tile)
            if position_to_place_tile in Rulebook.get_legal_positions(pub_data.current_map, tile, list(placed_so_far.keys())):
                pub_data.current_map.add_tile_to_board(tile, position_to_place_tile)
                placed_so_far.update({position_to_place_tile: tile})
                hand.remove(tile)
                return self.get_tile_placements(pub_data, hand, placed_so_far)
        return placed_so_far

    @abstractmethod
    def choose_position(self, given_map: Map, tile: Tile) -> Pos:
        """
        Get the position that a tile should be placed at
        """
        possible_positions = Rulebook.get_all_positions(given_map, tile)
        return self.get_smallest_placement(list(possible_positions))

    @abstractmethod
    def choose_tile(self, given_map: Map, hand: List[Tile]) -> Optional[Tile]:
        """
        Get the tile that should be placed
        """
        filtered_hand = Rulebook.get_legal_hand(given_map, hand, [])
        smallest_tile = None
        if filtered_hand:
            smallest_shape_rank = min([tile.shape.value for tile in filtered_hand])
            tiles_with_smallest_shape_rank = [tile for tile in filtered_hand if tile.shape.value == smallest_shape_rank]

            smallest_color_rank = min([tile.color.value for tile in tiles_with_smallest_shape_rank])
            # If we have multiple of the same smallest tile, we just return the first one.
            smallest_tile = [tile for tile in tiles_with_smallest_shape_rank if tile.color.value == smallest_color_rank][0]
        return smallest_tile

    def get_smallest_placement(self, possible_positions: List[Pos]) -> Pos:
        """
        Chooses smallest placement by row-column order
        """
        smallest_row = min([position.y for position in possible_positions])
        positions_with_smallest_row = [position for position in possible_positions if position.y == smallest_row]

        return min(positions_with_smallest_row, key=lambda position: position.x)
    