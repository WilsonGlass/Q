import unittest

from collections import defaultdict
from Q.Common.player_game_state import PlayerGameState
from Q.Player.behaved_player import Player

from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Common.game_state import GameState
from Q.Common.map import Map
from Q.Common.public_player_data import PublicPlayerData
from Q.Common.render import Render
from Q.Common.rulebook import Rulebook
from Q.Util.Configurations.score_config import ScoreConfig


class TestConfig(unittest.TestCase):
    def setUp(self):
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
        
        self.ref_tile = {Pos(0, 0): self.tile1}
        self.m1 = Map(config=self.ref_tile)
        self.pgs = PlayerGameState("bob", self.tiles, 0)
        self.ppd1 = PublicPlayerData(num_ref_tiles=1080, current_map=self.m1, current_player_data=self.pgs, other_points=[])
        self.gs = GameState(self.ppd1)
        self.gs.signup_player(self.pgs)
        self.gs.place_tiles(tiles=self.config1)
        self.p2 = PlayerGameState("mary",[self.tile3, self.tile7], 0)
        self.config2 = {Pos(0, 1): self.tile5, Pos(1, 0): self.tile4, Pos(1, 1): self.tile3}
        self.m2 = Map(config=self.config2)
        self.ppd2 = PublicPlayerData(num_ref_tiles=1080,current_map=self.m2, current_player_data=self.p2, other_points=[])
        self.gs2 = GameState(self.ppd2)
        self.gs2.signup_player(self.p2)
        self.score_config_1 = ScoreConfig(final_bonus=5, q_bonus=5)
        self.score_config_2 = ScoreConfig(final_bonus=5, q_bonus=10)
        self.score_config_3 = ScoreConfig(final_bonus=10, q_bonus=5)
    def test_q_bonus(self):
        # completing a Q (+5), placing five tiles (+5), creating a 6 length col (+6)
        score_1 = Rulebook.score_turn(tiles=self.config1, 
                                                 curr_map=self.m1, 
                                                 player_hand=self.pgs.hand, 
                                                 end_game=False, 
                                                 score_config=self.score_config_1)
        # completing a Q (+10), placing five tiles (+5), creating a 6 length col (+6)
        score_2 = Rulebook.score_turn(tiles=self.config1, 
                                                 curr_map=self.m1, 
                                                 player_hand=self.pgs.hand, 
                                                 end_game=False, 
                                                 score_config=self.score_config_2)
        self.assertNotEqual(score_1, score_2)

    def test_f_bonus(self):
        # completing a Q (+5), placing five tiles (+5), creating a 6 length col (+6)
        score_1 = Rulebook.score_turn(tiles=self.config1, 
                                                 curr_map=self.m1, 
                                                 player_hand=self.pgs.hand, 
                                                 end_game=False, 
                                                 score_config=self.score_config_1)
        # completing a Q (+10), placing five tiles (+5), creating a 6 length col (+6)
        score_3 = Rulebook.score_turn(tiles=self.config1, 
                                                 curr_map=self.m1, 
                                                 player_hand=[], 
                                                 end_game=True, 
                                                 score_config=self.score_config_3)
        self.assertNotEqual(score_1, score_3)

if __name__ == "__main__":
    unittest.main()