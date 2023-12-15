from Q.Common.Board.pos import Pos


class PosFuncs:
    """
    Functions that perform operations on the given pos and return another pos
    """
    @staticmethod
    def above(pos: Pos) -> Pos:
        return Pos(pos.x, pos.y + 1)

    @staticmethod
    def below(pos: Pos) -> Pos:
        return Pos(pos.x, pos.y - 1)

    @staticmethod
    def left(pos: Pos) -> Pos:
        return Pos(pos.x - 1, pos.y)

    @staticmethod
    def right(pos: Pos) -> Pos:
        return Pos(pos.x + 1, pos.y)
