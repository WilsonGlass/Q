from typing import Dict, Set, Callable, List

from Q.Util.Configurations.score_config import ScoreConfig
from Q.Util.pos_funcs import PosFuncs
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.Board.pos import Pos

END_BONUS = 4
Q_BONUS = 8


class Rulebook:
    """
    Represents the game rules which the referee and players may consult
    Source of truth of all dynamically changeable items of the game
    """

    @staticmethod
    def get_legal_positions(given_map: Map, given_tile: Tile, placed_positions: List[Pos]) -> Set[Pos]:
        """
        Computes all of the legal positions to place the given tile onto the given map
        :param placed_positions: the positions that have already been placed
        :param given_map: the map searched for valid positions
        :param given_tile: the tile that is placed
        :return: a set of valid positions
        """
        valid_positions: Set[Pos] = set()
        for p, tile in given_map.tiles.items():
            if tile.shape != given_tile.shape and tile.color != given_tile.color:
                continue
            neighbors: Dict[Pos, Tile] = given_map.get_neighbors(p)
            valid_neighbor_positions = Rulebook.filter_adjacent_positions(neighbors, given_tile, given_map)
            for neighbor in valid_neighbor_positions:
                potential_positions = placed_positions.copy()
                potential_positions.append(neighbor)
                if Rulebook.all_same_row_or_col(potential_positions):
                    valid_positions.add(neighbor)

        return valid_positions

    @staticmethod
    def get_all_positions(given_map: Map, given_tile: Tile) -> Set[Pos]:
        """
        Finds valid positions without checking for same row/col in turn
        """
        valid_positions: Set[Pos] = set()
        for p, tile in given_map.tiles.items():
            if tile.shape != given_tile.shape and tile.color != given_tile.color:
                continue
            neighbors: Dict[Pos, Tile] = given_map.get_neighbors(p)
            valid_neighbor_positions = Rulebook.filter_adjacent_positions(neighbors, given_tile, given_map)
            for neighbor in valid_neighbor_positions:
                valid_positions.add(neighbor)

        return valid_positions

    @staticmethod
    def get_legal_hand(given_map: Map, hand: List[Tile], already_placed: List[Pos]) -> List[Tile]:
        """
        Gets the legal hand based on the rulebook
        """
        return list(filter(lambda tile: len(Rulebook.get_legal_positions(given_map, tile, already_placed)) != 0, hand))

    @staticmethod
    def filter_adjacent_positions(neighbors: Dict[Pos, Tile], given_tile: Tile, map: Map) -> Set[Pos]:
        """
        Filters out the neighbors of a specific tile which the given tile can be placed
        :param neighbors: potential tile placements
        :param given_tile: the tile being placed
        :param map: the map at which we inspect for valid placements
        :return: the set of valid positions
        """
        valid_positions = set()
        for pos, tile in neighbors.items():
            if tile:
                continue
            is_valid: bool = Rulebook.is_valid_space(map, pos, given_tile)
            if is_valid:
                valid_positions.add(pos)

        return valid_positions

    @staticmethod
    def is_valid_space(given_map: Map, pos: Pos, given_tile: Tile) -> bool:
        """
        Is this given tile allowed to be placed at the given position on the given map according to the rulebook?
        :param given_map: the map at which we insect for a valid placement
        :param pos: the position of the potentially valid space
        :param given_tile: the tile we are trying to place
        :return: true if the tile can be placed
        """
        nbrs: Dict[Pos, Tile] = given_map.get_neighbors(pos)

        def compare_features(call1: Callable[[Pos], Pos], call2: Callable[[Pos], Pos], p: Pos,
                             comparator: Callable[[Tile, Tile], bool]) -> bool:
            if p is None:
                return False
            return comparator(given_tile, nbrs[call1(p)]) and comparator(given_tile, nbrs[call2(p)])

        shapes_same_vert = compare_features(PosFuncs.above, PosFuncs.below, pos, Rulebook.compatible_shapes)
        shapes_same_hor = compare_features(PosFuncs.left, PosFuncs.right, pos, Rulebook.compatible_shapes)
        colors_same_vert = compare_features(PosFuncs.above, PosFuncs.below, pos, Rulebook.compatible_colors)
        colors_same_hor = compare_features(PosFuncs.left, PosFuncs.right, pos, Rulebook.compatible_colors)

        return (shapes_same_vert or colors_same_vert) and (shapes_same_hor or colors_same_hor)

    @staticmethod
    def valid_replacement(num_of_ref_tiles: int, player_hand: List[Tile]) -> bool:
        """
        is this a valid replacement move
        :param num_of_ref_tiles: the number of ref tiles
        :param player_hand: the players current hand
        :return: true if a replacement is possible
        """
        return len(player_hand) <= num_of_ref_tiles

    @staticmethod
    def valid_placements(given_map: Map, tiles_placed: Dict[Pos, Tile]) -> bool:
        """
        if the given tiles can be placed according to the rules of the Q game
        :param given_map: the given map we are placing tiles at
        :param tiles_placed: the tiles attempting to be placed
        returns true if the tiles can be placed
        """
        for pos, tile in tiles_placed.items():
            if pos not in Rulebook.get_legal_positions(given_map, tile, list(tiles_placed.keys())):
                return False
            given_map.add_tile_to_board(tile, pos)
        return True

    @staticmethod
    def compatible_shapes( tile1: Tile, tile2: Tile):
        return tile1 is None or tile2 is None or tile1.compatible_shape(tile2)

    @staticmethod
    def compatible_colors(tile1: Tile, tile2: Tile):
        return tile1 is None or tile2 is None or tile1.compatible_color(tile2)

    # SCORING
    @staticmethod
    def score_turn(tiles: Dict[Pos, Tile], curr_map: Map, player_hand: List[Tile], end_game=False, score_config: ScoreConfig = ScoreConfig()) -> int:
        """
        Calculates the points scored on a given turn
        Note: Everything has already been placed before scoring. So it's fine if the player hand is empty.
        :param tiles: the tiles placed which is a mapping from position to tile
        :param end_game: is the game over which add the end bonus points
        :param player_hand: Player's current hand
        :param curr_map: Current map to score turn
        :return: the points scored on a turn
        """
        points_in_turn = 0
        points_in_turn += Rulebook.score_place_tiles(tiles)
        positions = [pos for pos in tiles.keys()]
        points_in_turn += Rulebook.get_contiguous_sequence_points(curr_map, positions)
        points_in_turn += Rulebook.get_completing_q_points(curr_map, positions, score_config)
        if end_game:
            points_in_turn += Rulebook.score_end_bonus_points(player_hand, score_config)
        return points_in_turn

    @staticmethod
    def score_place_tiles(tiles: Dict[Pos, Tile]) -> int:
        """
        calculates the score for placing tiles
        :param tiles: the tiles that are placed to be scored
        :return the points valued to be scored
        """
        return len(tiles)

    @staticmethod
    def score_end_bonus_points(player_hand: List[Tile], score_config: ScoreConfig) -> int:
        """
        calculates the score for the end bonus points if the player places all their tiles
        :param player_hand: the tiles that are placed on the board to be scored
        :param score_config: configured point values
        :return the points to be scored
        """
        if not len(player_hand):
            return score_config.final_bonus
        else:
            return 0

    @staticmethod
    def get_contiguous_sequence_points(curr_map: Map, positions: List[Pos]) -> int:
        """
        From instructions: A Player receives one point per tile in a contiguous sequence of tiles (in a row or column)
        that contains at least one of its newly placed tiles.
        :param positions: List of positions played in a given turn
        :return: number of points to be added for this rule
        """
        row_items = curr_map.get_seen_contiguous_items(curr_map.get_contiguous_row, positions)
        col_items = curr_map.get_seen_contiguous_items(curr_map.get_contiguous_col, positions)
        return len(row_items) + len(col_items)

    @staticmethod
    def __get_seen_components_points(curr_map: Map, contiguous_positions: Set[Pos], score_config: ScoreConfig) -> int:
        """
        Gets points for seen components for a list of positions contiguous rows/cols
        :param contiguous_positions: list of contiguous positions
        :return: points to be added
        """
        points = 0
        seen_component_shape = set()
        seen_component_color = set()
        for position in contiguous_positions:
            seen_component_shape.add(curr_map.tiles.get(position).shape)
            seen_component_color.add(curr_map.tiles.get(position).color)
            if (len(seen_component_shape) == 6 and len(seen_component_color) == 1) or \
                    (len(seen_component_color) == 6 and len(seen_component_shape) == 1):
                points += score_config.q_bonus
        return points

    @staticmethod
    def get_completing_q_points(curr_map: Map, positions: List[Pos], score_config: ScoreConfig) -> int:
        """
        :param curr_map: Map to check for new q's on
        :param positions: determines the points for completing some number of q's
        :return: the points for completing q's
        """
        seen_contiguous = set()
        points = 0

        for position in positions:
            contiguous_row = curr_map.get_contiguous_row(position)
            contiguous_col = curr_map.get_contiguous_col(position)
            if contiguous_row not in seen_contiguous:
                points += Rulebook.__get_seen_components_points(curr_map, contiguous_row, score_config)
                seen_contiguous.add(frozenset(contiguous_row))

            if contiguous_col not in seen_contiguous:
                points += Rulebook.__get_seen_components_points(curr_map, contiguous_col, score_config)
                seen_contiguous.add(frozenset(contiguous_col))
        return points

    @staticmethod
    def all_same_row_or_col(tiles: List[Pos]) -> bool:
        """
        are all the tiles in the same row xor the same col?
        param: tiles: a list of pos which are checked if they are same row or col
        return: true if tiles are same row or col, else false
        """
        return len(set(pos.x for pos in tiles)) == 1 or \
               len(set(pos.y for pos in tiles)) == 1
