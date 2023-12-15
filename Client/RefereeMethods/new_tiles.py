from jsonstream import dumps
from Q.Util.util import Util
from Q.Client.RefereeMethods.referee_method import RefereeMethod


class NewTiles(RefereeMethod):
    """
    Represents the method of a referee giving a player new tiles
    """
    def name(self):
        return "new-tiles"
    
    def go(self, args):
        """
        Send a list of tiles to the player
        :param args: A list contining a JTiles
        """
        jtiles = args[0]
        self.player.new_tiles([Util().json_to_tile(tile) for tile in jtiles])
        self.socket.sendall(dumps("void").encode("utf-8"))
