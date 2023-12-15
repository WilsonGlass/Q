class RefereeMethod:
    """
    Interface for referee methods
    """
    def __init__(self, player, socket):
        self.player = player
        self.socket = socket
    
    def name(self) -> str:
        """
        Return the name of a method
        """
        raise NotImplementedError

    def go(self, args):
        """
        Implement referee method behavior
        :param args: List containg method arguments
        """
        raise NotImplementedError
