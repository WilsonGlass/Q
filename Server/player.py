from json import loads
from typing import List
from socket import socket

from Q.Common.Board.tile import Tile
from Q.Common.Turn.turn import Turn
from Q.Common.public_player_data import PublicPlayerData
from Q.Player.behaved_player import Player
from Q.Util.util import Util
from jsonstream import dumps


class ProxyPlayer(Player):
    """
    Represents a remote proxy player for the referee to interact with. Communicates with the client by providing
    the necessary information for a real player.
    """
    def __init__(self, name: str, server_socket: socket):
        self.server_socket = server_socket
        self.util = Util()
        self._name = name
        self.hand = []

    def name(self) -> str:
        return self._name

    def setup(self, state: PublicPlayerData, tiles: List[Tile]):
        """
        Sends a jpub and jtiles to the proxy referee. This is then converted to PublicPlayerData and updates the
        players initial hand.
        [ "setup", [JPub, JTile*] ]
        """
        try:
            self.hand = tiles
            jpub = self.util.convert_public_player_data_to_jpub(state)
            jtiles = [self.util.convert_tile_to_json(tile) for tile in tiles]
            self.server_socket.sendall(dumps(["setup", [jpub, jtiles]]).encode("utf-8"))
            void_bytes = self.server_socket.recv(9999)
        except Exception as e:
            print(e)

    def take_turn(self, s: PublicPlayerData) -> Turn:
        """
        Sends a jpub to the player, so they can make an informed decision for making a turn. We await their
        response and return it
        [ "take-turn", [JPub] ]
        """
        jpub = self.util.convert_player_to_public_player_knowledge(s)
        self.server_socket.sendall(dumps(["take-turn", [jpub]]).encode("utf-8"))
        jchoice_bytes = self.server_socket.recv(99999)
        jchoice = loads(jchoice_bytes.decode("utf-8"))
        turn = self.util.convert_jchoice_to_turn(jchoice)
        return turn

    def new_tiles(self, st: List[Tile]):
        """
        [ "new-tiles", [JTile, ..., JTile] ]
        """
        self.hand = st
        jtiles = [self.util.convert_tile_to_json(tile) for tile in st]
        self.server_socket.sendall(dumps(["new-tiles", [jtiles]]).encode("utf-8"))
        void_bytes = self.server_socket.recv(9999)

    def win(self, w: bool):
        """
        Informs an individual client whether they won or not.
        [ "win", [bool] ]
        """
        if w:
            self.server_socket.sendall(dumps(["win", [True]]).encode("utf-8"))
        else:
            self.server_socket.sendall(dumps(["win", [False]]).encode("utf-8"))
        void_bytes = self.server_socket.recv(9999)

