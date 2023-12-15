from jsonstream import dumps
from Q.Client.RefereeMethods.referee_method import RefereeMethod


class Win(RefereeMethod):
    """
    Represents the method to tell a player they won remotely.
    """
    def name(self):
        return "win"
    
    def go(self, args):
        """
        Inform a player that if they've won or lost
        :param args: A list containing a JPub to send to player
        """
        win = args[0]
        self.player.win(win)
        self.socket.sendall(dumps("void").encode("utf-8"))
