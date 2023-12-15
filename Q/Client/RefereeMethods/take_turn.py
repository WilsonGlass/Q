from json import dumps
from Q.Client.RefereeMethods.referee_method import RefereeMethod
from Q.Util.util import Util

class TakeTurn(RefereeMethod):
    """
    Represents the method of a referee querying a player for their turn
    """
    def name(self):
        return "take-turn"
    
    def go(self, args):
        """
        Query a player's turn and send result to socket
        :param args: A list containing a JPub to send to player
        """
        jpub = args[0]
        pub_data = Util().convert_jpub_to_pub_data(jpub)
        turn = self.player.take_turn(pub_data)
        jchoice = Util().convert_turn_to_j_choice(turn)
        self.socket.sendall(dumps(jchoice).encode("utf-8"))
