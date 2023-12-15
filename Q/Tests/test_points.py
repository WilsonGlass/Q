import unittest

from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Common.game_state import GameState
from Q.Common.rulebook import Rulebook
from Q.Player.behaved_player import Player
from Q.Player.public_player_data import PublicPlayerData


class TestPoints(unittest.TestCase):

    def setUp(self) -> None:
        self.tile1 = Tile(TileShape.CIRCLE, TileColor.BLUE)
        self.tile2 = Tile(TileShape.STAR, TileColor.BLUE)
        self.tile3 = Tile(TileShape.CLOVER, TileColor.BLUE)
        self.tile4 = Tile(TileShape.SQUARE, TileColor.BLUE)
        self.tile5 = Tile(TileShape.EIGHTSTAR, TileColor.BLUE)
        self.tile6 = Tile(TileShape.DIAMOND, TileColor.BLUE)
        self.tile7 = Tile(TileShape.STAR, TileColor.GREEN)
        self.tiles = [self.tile2, self.tile3, self.tile4, self.tile5, self.tile6]
        self.positions = [Pos(0, 1), Pos(0, 2), Pos(0, 3), Pos(0, 4), Pos(0, 5)]
        self.config1 = {Pos(0, 1): self.tile2,
                        Pos(0, 2): self.tile3,
                        Pos(0, 3): self.tile4,
                        Pos(0, 4): self.tile5,
                        Pos(0, 5): self.tile6}

        self.pgs = Player(name="bob", hand=self.tiles)
        self.ref_tile = {Pos(0, 0): self.tile1}
        self.m1 = Map(config=self.ref_tile)
        self.ppd1 = PublicPlayerData(num_ref_tiles=1080, current_map=self.m1, scores={})
        self.gs = GameState(self.ppd1)
        self.gs.signup_player(self.pgs)
        self.gs.place_tiles(tiles=self.config1)

        self.config2 = {Pos(0, 1): self.tile5, Pos(1, 0): self.tile4, Pos(1, 1): self.tile3}
        self.m2 = Map(config=self.config2)
        self.ppd2 = PublicPlayerData(num_ref_tiles=1080,current_map=self.m2, scores={})
        self.gs2 = GameState(self.ppd2)
        self.p2 = Player(name="bob", hand=[self.tile3, self.tile7])
        self.gs2.signup_player(self.p2)

    def test_points1(self):
        # completing a Q (+6), placing five tiles (+5), creating a 6 length col (+6)
        self.assertEqual(17, self.gs.score_turn(self.config1))

    def test_points2(self):
        # completing a Q (+6), placing one tile (+1) existing contiguous col (+6)
        self.assertEqual(13, self.gs.score_turn({Pos(0, 5): self.tile6}))

    def test_points3(self):
        # contiguous in row (+1), contiguous in col (+1) placing one tile (+1)
        self.assertEqual(5, self.gs2.score_turn({Pos(1, 1): self.tile3}))


if __name__ == '__main__':
    unittest.main()
