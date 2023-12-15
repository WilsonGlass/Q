import unittest

from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.rulebook import Rulebook


class TestRulebook(unittest.TestCase):
    def setUp(self) -> None:
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

        self.dict = {
            Pos(0, 0): self.tile1,
            Pos(0, 1): self.tile2,
            Pos(0, 2): self.tile3,
            Pos(1, 1): self.tile2
        }

        self.m1 = Map(config=self.dict)

    def test_get_neighbors(self):
        neigh = {
            Pos(0, -1): None,
            Pos(0, 1): self.tile2,
            Pos(1, 0): None,
            Pos(-1, 0): None
        }

        self.assertEqual(self.m1.get_neighbors(Pos(0, 0)), neigh)

    def test_get_neighbors2(self):
        neigh = {
            Pos(0, 2): self.tile3,
            Pos(0, 0): self.tile1,
            Pos(1, 1): self.tile2,
            Pos(-1, 1): None
        }

        self.assertEqual(self.m1.get_neighbors(Pos(0, 1)), neigh)

    def test_rulebook(self):
        # no valid positions
        no_positions = set()
        self.assertEqual(Rulebook.get_legal_positions(self.m1, self.tile6, []), no_positions)

    def test_rulebook2(self):
        # all valid positions
        positions = set()
        positions.add(Pos(1, 2))
        positions.add(Pos(2, 1))
        positions.add(Pos(-1, 1))
        positions.add(Pos(0, 3))
        positions.add(Pos(-1, 0))
        positions.add(Pos(1, 0))
        positions.add(Pos(-1, 2))
        positions.add(Pos(0, -1))
        self.assertEqual(Rulebook.get_legal_positions(self.m1, self.tile2, []), positions)

    def test_rulebook3(self):
        # some valid 
        positions = set()
        positions.add(Pos(-1, 0))
        positions.add(Pos(0, -1))
        self.assertEqual(Rulebook.get_legal_positions(self.m1, self.tile10), positions)


if __name__ == '__main__':
    unittest.main()
