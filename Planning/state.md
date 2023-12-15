Gamestate needs to hold the logic under the referee. The key components of the game are held in the game state.
Some of these items can include:
    1) A queue of PlayerStates (designed below)
        PlayerState contains:
            1) Player object (to be designed)
            2) Score (int)
            3) The player's hand (listof Tile)
    2) The map (Map class we defined) the players are playing on
    3) The deck (queue) of shuffled tiles (Tile class we defined) the referee can draw from and add to
    4) A counter (int) to keep track of the contiguous number of exchages or passes.

Gamestate Wishlist:
    # returns the new current player
    # effect: player moves to end of queue
    def cycle_queue() -> PlayerState:
        pass

    # effect: pops the player at the front of the queue out
    def kick_current_player() -> None:
        pass

    #effect: adds the given player to the front of the queue
    def signup_player(player: Player) -> None:
        pass
 
    #has the game ended?
    def is_game_over() -> bool:
        pass

    # effect: instantiates the game map with a given referee tile and orders the players in descending order of age
    def setup_game(tile: Tile):
        pass
