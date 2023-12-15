import traceback
from json import loads
from socket import socket
from Q.Client.RefereeMethods.referee_factory import RefereeMethodFactory

from Q.Player.behaved_player import Player
from Q.Util.util import Util


class ProxyReferee:
    """
    Represents the proxy that methods go through before being sent to a player.
    This is meant to parse function calls on the client side.
    """
    def __init__(self, player: Player, client_socket: socket):
        self.player = player
        self.client_socket = client_socket
        self.util = Util()

    def stream(self):
        """
        Runs a continuous stream and dispatching it until the game ends or an exception occurs.
        """
        buffer_size = 9999999
        while True:
            try:
                dispatch_bytes = self.client_socket.recv(buffer_size)
                if dispatch_bytes:
                    dispatch_decoded = dispatch_bytes.decode("utf-8")
                    loaded = loads(dispatch_decoded)
                    self.dispatch_command(loaded)
                    if loaded[0] == "win":
                        break
            except Exception as e:
                print(e)
                break

    def dispatch_command(self, stream):
        """
        Dispatches mname functions. Parses each function call and calls them accordingly.
        """
        try:
            mname = stream[0]
            args = stream[1]
            referee_method = RefereeMethodFactory.generate(mname, self.player, self.client_socket)
            referee_method.go(args)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
