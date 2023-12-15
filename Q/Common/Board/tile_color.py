from enum import Enum


class TileColor(Enum):
    """
    # Enumeration of different tile colors
    # These values are ranked from smallest to biggest
    """
    RED = 1
    GREEN = 2
    BLUE = 3
    YELLOW = 4
    ORANGE = 5
    PURPLE = 6

    def get_name(self):
        return self.name.lower()

    @staticmethod
    def get_color_by_name(name: str) -> "TileColor":
        for color in TileColor:
            if color.get_name() == name:
                return color
        raise ValueError(f"No TileColor found with the name: {name}")

