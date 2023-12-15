from .tile_color import TileColor
from .tile_shape import TileShape


class Tile:
    """
    # Represents a tile on the board of the Q Game
    """
    def __init__(self, shape: TileShape, color: TileColor):
        self.shape = shape
        self.color = color
    
    def compatible_shape(self, other: "Tile") -> bool:
        """
        is the other tile of matching shape with this tile?
        :param other: the tile you are matching shape against
        :return: if the tile is matching shape.
        """
        return self.shape is other.shape
    
    def compatible_color(self, other: "Tile") -> bool:
        """
        is the other tile of matching color with this tile?
        :param other: the tile you are matching color against
        :return: if the tile is matching color.
        """
        return self.color is other.color
    
    def __repr__(self) -> str:
        return f"Tile({self.shape}, {self.color})"
    
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__)\
          and self.shape is other.shape\
          and self.color is other.color
