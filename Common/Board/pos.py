class Pos:
    """
    # represents a position in R2
    # -y is up, +y is down
    # +x is right, -x is left
    """
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return isinstance(other, self.__class__)\
          and self.x == other.x\
          and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"Pos({self.x},{self.y})"
