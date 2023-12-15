from collections import defaultdict

from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Common.render import Render


class TestRender:
    def __init__(self):
        self.one_tile = defaultdict()

        self.tile1 = Tile(TileShape.CIRCLE, TileColor.BLUE)
        self.tile2 = Tile(TileShape.CLOVER, TileColor.BLUE)
        self.tile3 = Tile(TileShape.CLOVER, TileColor.GREEN)
        self.tile4 = Tile(TileShape.DIAMOND, TileColor.YELLOW)
        self.tile5 = Tile(TileShape.EIGHTSTAR, TileColor.YELLOW)
        self.tile6 = Tile(TileShape.STAR, TileColor.PURPLE)
        self.tile7 = Tile(TileShape.CLOVER, TileColor.BLUE)
        self.tile8 = Tile(TileShape.CIRCLE, TileColor.RED)
        self.tile9 = Tile(TileShape.CIRCLE, TileColor.BLUE)
        self.tile10 = Tile(TileShape.CIRCLE, TileColor.RED)
        self.tile11 = Tile(TileShape.SQUARE, TileColor.RED)

        self.config = {
            Pos(0, 0): self.tile1,
            Pos(0, 1): self.tile2,
            Pos(0, 2): self.tile3,
            Pos(1, 1): self.tile2
        }

    def main(self):
        self.render_board()

    def render_board(self):
        self.one_tile[Pos(1, 1)] = self.tile1
        self.one_tile[Pos(1, 2)] = self.tile2
        self.one_tile[Pos(2, 1)] = self.tile3
        Render(self.one_tile).show()


if __name__ == "__main__":
    t = TestRender()
    t.main()
