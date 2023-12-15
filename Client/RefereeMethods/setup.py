from jsonstream import dumps
from Q.Client.RefereeMethods.referee_method import RefereeMethod
from Q.Util.util import Util


class Setup(RefereeMethod):
    """
    Represents the method of a referee initially setting up a player
    """
    def name(self):
        return "setup"
    
    def go(self, args):
        """
        Set up a player with a public game state and initial bag of tiles
        :param args: A list containing a JPub, and a JTiles
        """
        jpub, jtiles = args
        self.player.setup(Util().convert_jpub_to_pub_data(jpub), [Util().json_to_tile(tile) for tile in jtiles])
        self.socket.sendall(dumps("void").encode("utf-8"))
