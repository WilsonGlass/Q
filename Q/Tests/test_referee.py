import unittest

from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Common.game_state import GameState
from Q.Common.player_game_state import PlayerGameState
from Q.Player.behaved_player import Player
from Q.Player.Strategy.dag import Dag
from Q.Player.Strategy.ldasg import LDasg
from Q.Referee.pair_results import PairResults
from Q.Referee.referee import Referee
from Q.Referee.referee_data import RefereeData


class TestReferee(unittest.TestCase):
    def setUp(self):
        self.tile1 = Tile(TileShape.CIRCLE, TileColor.BLUE)
        self.tile2 = Tile(TileShape.STAR, TileColor.BLUE)
        self.tile3 = Tile(TileShape.CLOVER, TileColor.BLUE)
        self.tile4 = Tile(TileShape.SQUARE, TileColor.BLUE)
        self.tile5 = Tile(TileShape.EIGHTSTAR, TileColor.BLUE)
        self.tile6 = Tile(TileShape.DIAMOND, TileColor.BLUE)
        self.tile7 = Tile(TileShape.STAR, TileColor.GREEN)
        self.tile8 = Tile(TileShape.SQUARE, TileColor.PURPLE)
        self.tiles = [self.tile2, self.tile3, self.tile4, self.tile5, self.tile6]
        self.positions = [Pos(0, 1), Pos(0, 2), Pos(0, 3), Pos(0, 4), Pos(0, 5)]
        self.config1 = {Pos(0, 1): self.tile2,
                        Pos(0, 2): self.tile3,
                        Pos(0, 3): self.tile4,
                        Pos(0, 4): self.tile5,
                        Pos(0, 5): self.tile6}

        self.player1 = Player(strategy=Dag(), name="bob", hand=self.tiles)
        self.player2 = Player(strategy=LDasg(), name="bob2", hand=[self.tile3, self.tile7])
        self.ref_tile = {Pos(0, 0): self.tile1}
        self.m1 = Map(config=self.ref_tile)
        self.gs = GameState()
        self.gs.place_tiles(tiles=self.config1)

        self.config2 = {Pos(0, 1): self.tile5, Pos(1, 0): self.tile4, Pos(1, 1): self.tile3}
        self.m2 = Map(config=self.config2)

        self.config3 = {Pos(0, 0): self.tile5,
                        Pos(0, 1): self.tile6,
                        Pos(1, 1): self.tile6,
                        Pos(2, 1): self.tile6}
        self.m3 = Map(config=self.config3)
        self.player3 = Player(strategy=LDasg(), name="bob3", hand=[self.tile2, self.tile3])

        self.config4 = {
            Pos(0, 0): self.tile1,
            Pos(0, 1): self.tile1,
            Pos(0, 2): self.tile1,
            Pos(1, 2): self.tile1,
            Pos(2, 2): self.tile1,
            Pos(2, 1): self.tile1,
            Pos(2, 0): self.tile1,
            Pos(1, 0): self.tile1,
        }
        self.m4 = Map(config=self.config4)
        self.player4 = Player(strategy=LDasg(), name="bob4", hand=[self.tile8])
        self.player5 = Player(strategy=LDasg(), name="bob5", hand=[self.tile8, self.tile1])
        self.player6 = Player(strategy=LDasg(), name="bob6", hand=[self.tile1, self.tile2])
        self.player7 = Player(strategy=LDasg(), name="bob7", hand=[self.tile1, self.tile2])

    def test_run(self):
        """
        Runs the game with two dags
        """
        referee = Referee()
        player1 = Player(strategy=Dag(), name="bob", hand=self.tiles)
        player2 = Player(strategy=Dag(), name="dan", hand=self.tiles)

        pgs = [
            PlayerGameState("bob", self.player1.hand, 0),
            PlayerGameState("dan", self.tiles, 0)
        ]
        gs = GameState(given_map=self.m1, tiles=self.tiles, random_seed=1234, player_game_states=pgs)
        players = [player1, player2]
        ref_data = RefereeData(game_state=gs, misbehaved=[], player_queue=players)
        pair_results = referee.start_from_state(ref_data)
        self.assertEqual(pair_results, PairResults(winners={'bob'}, misbehaved=[]))

    def test_signup(self):
        """
        Tests to see if you can sign up 2 players
        """
        referee = Referee()
        player_list = [Player(strategy=Dag(), name="dag"), Player(strategy=LDasg(), name="ldasg")]
        ref_data = RefereeData(game_state=self.gs, misbehaved=[], player_queue=player_list)
        referee.signup_players(ref_data)
        self.assertEqual(len(self.gs.players), 2)

    def test_signup2(self):
        """
        Tests to see if you cant signup more than 4 players
        """
        referee = Referee()
        player_list = [
            Player(strategy=Dag(), name="dag1"),
            Player(strategy=LDasg(), name="ldasg1"),
            Player(strategy=Dag(), name="dag2"),
            Player(strategy=LDasg(), name="ldasg2"),
            Player(strategy=LDasg(), name="extra_player"),
        ]
        ref_data = RefereeData(player_queue=player_list, game_state=self.gs, misbehaved=[])
        referee.signup_players(ref_data)
        self.assertEqual(len(self.gs.players), 4)

    def test_game_with_one_player(self):
        """
        Tests the game with one player added
        """
        referee = Referee()
        player1 = Player(strategy=Dag(), name="bob", hand=self.tiles)

        pgs = [
            Player(strategy=Dag(), name="bob", hand=self.tiles)
        ]
        gs = GameState(given_map=self.m1, tiles=self.tiles, random_seed=1234, player_game_states=pgs)
        ref_data = RefereeData(player_queue=[player1], game_state=gs, misbehaved=[])
        pair_results = referee.start_from_state(ref_data)
        self.assertEqual(pair_results, PairResults(winners={'bob'}, misbehaved=[]))


if __name__ == '__main__':
    unittest.main()
