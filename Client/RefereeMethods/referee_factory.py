from Q.Client.RefereeMethods.new_tiles import NewTiles
from Q.Client.RefereeMethods.referee_method import RefereeMethod
from Q.Client.RefereeMethods.setup import Setup
from Q.Client.RefereeMethods.take_turn import TakeTurn
from Q.Client.RefereeMethods.win import Win

from Q.Player.base import Player
import socket


class RefereeMethodFactory:
    """
    Factory to return proxy referee methods.
    """
    @staticmethod
    def generate(mname: str, player: Player, client_socket: socket) -> RefereeMethod:
        if mname == "take-turn":
            return TakeTurn(player, client_socket)
        elif mname == "setup":
            return Setup(player, client_socket)
        elif mname == "new-tiles":
            return NewTiles(player, client_socket)
        elif mname == "win":
            return Win(player, client_socket)
        else:
            raise Exception(f"{mname} is an invalid mname.")
