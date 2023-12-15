import unittest
from copy import deepcopy

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
from Q.Referee.observer import Observer
from Q.Referee.pair_results import PairResults
from Q.Referee.referee import Referee
from Q.Referee.referee_data import RefereeData
from Q.Util.Configurations.referee_config import RefereeConfig


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

    def test_gui(self):
        """
        Runs the game with two dags
        """
        pgs = [
            PlayerGameState("bob", self.player1.hand, 0),
            PlayerGameState("dan", self.tiles, 0)
        ]
        gs = GameState(given_map=self.m1, tiles=self.tiles, random_seed=1234, player_game_states=pgs)
        gs2 = GameState(given_map=self.m2, tiles=[self.tile3, self.tile7], random_seed=1234, player_game_states=pgs)
        gs3 = GameState(given_map=self.m3, tiles=[self.tile5, self.tile6, self.tile6, self.tile6], random_seed=1234, player_game_states=pgs)
        observer = Observer(game_states=[gs, gs2, gs3])
        observer.make_gui()

    def test_add_state(self):
        """
        adds a state to the observer
        """
        pgs = [
            PlayerGameState("bob", self.player1.hand, 200),
            PlayerGameState("dan", self.player1.hand, 100)
        ]
        gs = GameState(given_map=self.m1, tiles=self.tiles, random_seed=1234, player_game_states=pgs)
        gs2 = GameState(given_map=self.m2, tiles=[self.tile3, self.tile7], random_seed=1234, player_game_states=pgs)
        gs3 = GameState(given_map=self.m3, tiles=[self.tile5, self.tile6, self.tile6, self.tile6], random_seed=1234,
                        player_game_states=pgs)
        observer = Observer(game_states=[gs, gs2])
        observer_before_adding = deepcopy(observer)
        observer.receive_a_state(gs3)
        self.assertTrue(len(observer.game_states) > len(observer_before_adding.game_states))

    def test_observer_with_run(self):
        """
        Runs the game to completion and presents the observer
        """
        referee = Referee()
        player1 = Player(strategy=Dag(), name="bob", hand=self.tiles)
        player2 = Player(strategy=Dag(), name="dan", hand=self.tiles)

        pgs = [
            PlayerGameState("bob", self.player1.hand, 200),
            PlayerGameState("dan", self.player1.hand, 100)
        ]
        gs = GameState(given_map=self.m1, tiles=self.tiles, random_seed=1234, player_game_states=pgs)
        players = [player1, player2]
        ref_data = RefereeData(game_state=gs, player_queue=players, misbehaved=[], config=RefereeConfig(observe=True))
        pair_results = referee.start_from_state(ref_data)
        self.assertEqual(pair_results, PairResults(winners={'bob'}, misbehaved=[]))


if __name__ == '__main__':
    unittest.main()
