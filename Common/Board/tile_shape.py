from enum import Enum


class TileShape(Enum):
    """
    # Enumeration of tile shapes
    # These values are ranked from smallest to biggest
    """
    STAR = 1
    EIGHTSTAR = 2
    SQUARE = 3
    CIRCLE = 4
    CLOVER = 5
    DIAMOND = 6

    def get_name(self):
        return "8star" if self == TileShape.EIGHTSTAR else self.name.lower()

    @staticmethod
    def get_shape_by_name(name: str) -> "TileShape":
        for shape in TileShape:
            if shape.get_name() == name:
                return shape
        raise ValueError(f"No TileShape found with the name: {name}")

