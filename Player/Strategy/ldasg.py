from Q.Common.rulebook import Rulebook
from Q.Common import public_player_data
from Q.Player.Strategy.player_strategy import PlayerStrategy
from typing import Dict, List
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Turn.turn import Turn
from Q.Common.public_player_data import PublicPlayerData


class LDasg(PlayerStrategy):
    """
    Represents the LDASG (less dumb and still greedy) player strategy.
    From assignment specs: Chooses the player's smallest tile that can extend the current map.
    If there is more than one place, it picks the one that has the most existing neighbors, that is, the most
    constrained one.
    """

    def get_turn(self, pub_data: PublicPlayerData, hand: List[Tile]) -> Turn:
        """
        Gets the turn object depending on the current public player data
        """
        return super().get_turn(pub_data, hand)

    def get_tile_placements(self, pub_data: PublicPlayerData, hand: List[Tile], placed_so_far: Dict[Pos, Tile] = {}) -> Dict[Pos, Tile]:
        return super().get_tile_placements(pub_data, hand, placed_so_far)

    def choose_position(self, given_map: Map, tile: Tile) -> Pos:
        """
        Chooses placement firstly by picking a position that has the most neighbors
        Tie breaks with the smallest placement (row-col order)
        """
        max_neighbors = 0
        possible_positions = Rulebook.get_all_positions(given_map, tile)
        positions_with_most_neighbors = []
        for position in possible_positions:
            neighbors = given_map.get_number_of_tile_neighbors(position)
            if neighbors > max_neighbors:
                max_neighbors = neighbors
                positions_with_most_neighbors = [position]
            elif neighbors == max_neighbors:
                positions_with_most_neighbors.append(position)

        return self.get_smallest_placement(positions_with_most_neighbors)

    def choose_tile(self, given_map: Map, filtered_hand: List[Tile]) -> Tile:
        return super().choose_tile(given_map, filtered_hand)
