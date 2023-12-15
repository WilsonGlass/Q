import unittest

from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Board.pos import Pos
from Q.Common.game_state import GameState
from Q.Common.rulebook import Rulebook
from Q.Player.behaved_player import Player
from Q.Player.dag import Dag
from Q.Player.ldasg import LDasg
from Q.Player.behaved_player import PublicPlayerData
from Q.Player.turn import Turn
from Q.Player.turn_outcome import TurnOutcome


class TestPlayer(unittest.TestCase):
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

        self.player = Player(strategy=Dag(), name="bob", hand=self.tiles)
        self.player2 = Player(strategy=LDasg(), name="bob2", hand=[self.tile3, self.tile7])
        self.ref_tile = {Pos(0, 0): self.tile1}
        self.m1 = Map(config=self.ref_tile)
        self.ppd = PublicPlayerData(1080, self.m1, {})
        self.gs = GameState(self.ppd)
        self.gs.signup_player(self.player)
        self.gs.place_tiles(tiles=self.config1)

        self.config2 = {Pos(0, 1): self.tile5, Pos(1, 0): self.tile4, Pos(1, 1): self.tile3}
        self.m2 = Map(config=self.config2)

        self.config3 = {Pos(0, 0): self.tile5,
                        Pos(0, 1): self.tile6,
                        Pos(1, 1): self.tile6,
                        Pos(2, 1): self.tile6}
        self.m3 = Map(config=self.config3)
        self.ppd3 = PublicPlayerData(1080, self.m3, {})
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
        self.ppd4 = PublicPlayerData(1080, self.m4, {})
        self.player4 = Player(strategy=LDasg(), name="bob4", hand=[self.tile8])
        self.player5 = Player(strategy=LDasg(), name="bob5", hand=[self.tile8, self.tile1])
        self.player6 = Player(strategy=LDasg(), name="bob6", hand=[self.tile1, self.tile2])
        self.player7 = Player(strategy=LDasg(), name="bob7", hand=[self.tile1, self.tile2])

    def test_dag(self):
        # testing basic dag
        this_turn = self.player.take_turn(self.ppd)
        expected_turn = Turn(turn_outcome=TurnOutcome.PLACED, placements={
            Pos(0, -1): Tile(TileShape.STAR, TileColor.BLUE),
            Pos(0, -2): Tile(TileShape.EIGHTSTAR, TileColor.BLUE),
            Pos(0, -3): Tile(TileShape.SQUARE, TileColor.BLUE),
            Pos(0, -4): Tile(TileShape.CLOVER, TileColor.BLUE),
            Pos(0, -5): Tile(TileShape.DIAMOND, TileColor.BLUE)
        })

        self.assertEqual(expected_turn, this_turn)

    def test_dag2(self):
        # testing dag vs lsdag setup
        this_turn = self.player7.take_turn(self.ppd4)
        expected_turn = Turn(turn_outcome=TurnOutcome.PLACED, placements={
            Pos(0, -2): Tile(TileShape.CIRCLE, TileColor.BLUE),
            Pos(0, -1): Tile(TileShape.STAR, TileColor.BLUE)
        })
        self.assertEqual(expected_turn, this_turn)

    def test_ldasg1(self):
        # testing basic ldasg
        this_turn = self.player2.take_turn(self.ppd)
        expected_turn = Turn(turn_outcome=TurnOutcome.PLACED, placements={
            Pos(-1, 1): Tile(TileShape.STAR, TileColor.GREEN),
            Pos(0, -1): Tile(TileShape.CLOVER, TileColor.BLUE)
        })

        self.assertEqual(expected_turn, this_turn)

    def test_ldasg2(self):
        # testing when their are varying num of neighbors
        this_turn = self.player3.take_turn(self.ppd3)
        expected_turn = Turn(turn_outcome=TurnOutcome.PLACED,
                             placements={Pos(0,-1): Tile(TileShape.CIRCLE, TileColor.BLUE),
                             Pos(1,1): Tile(TileShape.STAR, TileColor.BLUE)})
        self.assertEqual(expected_turn, this_turn)

    def test_ldasg3(self):
        # testing when you can't place any tiles in your hand
        this_turn = self.player4.take_turn(self.ppd4)
        expected_turn = Turn(turn_outcome=TurnOutcome.REPLACED,
                             placements={})
        self.assertEqual(this_turn, expected_turn)

    def test_ldasg4(self):
        # testing with max neighbor of 4 where you can place one and another tile you can't place in hand
        this_turn = self.player5.take_turn(self.ppd4)
        expected_turn = Turn(turn_outcome=TurnOutcome.PLACED,
                             placements={
                                 Pos(1, 1): Tile(TileShape.CIRCLE, TileColor.BLUE)
                             })
        self.assertEqual(this_turn, expected_turn)

    def test_ldasg5(self):
        # testing multiple good tiles that can be placed, picked based on rank for the 'best' position
        this_turn = self.player6.take_turn(self.ppd4)
        expected_turn = Turn(turn_outcome=TurnOutcome.PLACED,
                             placements={Pos(1, 1): Tile(TileShape.STAR, TileColor.BLUE),
                                         Pos(0, -1): Tile(TileShape.CIRCLE, TileColor.BLUE)})
        self.assertEqual(this_turn, expected_turn)


if __name__ == '__main__':
    unittest.main()
