from typing import Dict, List, Callable, Set
from collections import defaultdict


from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Util.pos_funcs import PosFuncs


class Map:
    """
    Represents a grid layout for a possibly very large board game
    """

    def __init__(self, ref_tile: Tile = None, config: Dict[Pos, Tile] = None):
        """
        # Constructs a game board
        :param ref_tile: the tile a ref may place at the start at (0,0). Default value is None
        :param config: a dictionary of given tiles to start the game from a specific state
        """
        if config:
            self.tiles = config
        else:
            self.tiles = defaultdict()
        if ref_tile:
            self.tiles[Pos(0, 0)] = ref_tile

    def add_tiles_to_board_dict(self, placement: Dict[Pos, Tile]):
        """
        Converts placements in Dict[Pos, Tile] form to iterators. With those iterators we can add them all placements
        to the board individually.
        :param placement: Placements to be added to the map
        """
        pos = next(iter(placement.keys()))
        tile = next(iter(placement.values()))
        self.add_tile_to_board(tile, pos)

    def add_tile_to_board(self, tile: Tile, pos: Pos):
        """
        Adds a given tile to the board at a given position. Assumes placement is valid.
        :param tile: The tile to be added to the board
        :param pos: the position of the tile
        """
        self.tiles[pos] = tile

    def get_number_of_tile_neighbors(self, pos: Pos):
        neighbors = self.get_neighbors(pos)
        len_of_neighbors = 0
        for neighbor in neighbors:
            if self.tiles.get(neighbor) is not None:
                len_of_neighbors += 1
        return len_of_neighbors

    def get_neighbors(self, pos: Pos) -> Dict[Pos, Tile]:
        """
        gets the immediate neighbors of a given position (up, down, left, right)
        :param pos: the position of on the map of whose neighbors you get from.
        :return: a dictionary of positions to tiles
        """
        return {
            PosFuncs.above(pos): self.tiles.get(PosFuncs.above(pos)),
            PosFuncs.below(pos): self.tiles.get(PosFuncs.below(pos)),
            PosFuncs.left(pos): self.tiles.get(PosFuncs.left(pos)),
            PosFuncs.right(pos): self.tiles.get(PosFuncs.right(pos))
        }

    def get_contiguous(self, direction: Callable[[Pos], Pos], pos: Pos) -> List[Pos]:
        """
        Gets all positions in contiguous direction
        Note: Not including the initial position.
        :param pos: position of the starting pos
        :param direction: a function that returns a new pos in some direction
        :return: List of positions in contiguous row
        """
        current_pos = direction(pos)
        positions = []
        while self.tiles.get(current_pos) is not None:
            positions.append(current_pos)
            current_pos = direction(current_pos)

        return positions

    def get_contiguous_row(self, pos: Pos) -> Set[Pos]:
        """
        Gets the contiguous row for the given position
        :param pos: Position to find contiguous row for
        :return: List of positions in contiguous row
        """
        positions = set()
        positions.update(self.get_contiguous(PosFuncs.left, pos))
        positions.add(pos)
        positions.update(self.get_contiguous(PosFuncs.right, pos))
        return positions

    def get_contiguous_col(self, pos: Pos) -> Set[Pos]:
        """
        Gets the contiguous col for the given position
        :param pos: Position to find contiguous col for
        :return: List of positions in contiguous col
        """
        positions = set()
        positions.update(self.get_contiguous(PosFuncs.above, pos))
        positions.add(pos)
        positions.update(self.get_contiguous(PosFuncs.below, pos))
        return positions


    def get_seen_contiguous_items(self, get_contiguous_axis: Callable[[Pos], Set[Pos]], positions: List[Pos]) -> Set[Pos]:
        """
        gets the seen contiguous items in a given direction for given positions
        :param get_contiguous_axis: the function which gets items in a particular row or col
        :param positions: the given positions at which you want to get rows or col
        """
        seen_items = set()
        for position in positions:
            contiguous_sequence = get_contiguous_axis(position)
            if len(contiguous_sequence) > 1:
                seen_items.update(contiguous_sequence)
        return seen_items



    



