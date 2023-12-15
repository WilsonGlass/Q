import sys
from jsonstream import loads, dumps

from Q.Util.util import Util

from Q.Player.turn_outcome import TurnOutcome


def main():
    """
    the main method for reading in jpub and it's strategy and outputting the jaction
    """
    stream = loads(sys.stdin.read())
    util = Util()
    jpub = next(stream)
    strat_string = next(stream)

    strategy = util.convert_jstrategy_to_strategy(strat_string)
    game_state = util.convert_jpub_json_to_game_state(jpub)
    jplayer = jpub["players"][0]
    player = util.convert_jplayer_to_player(jplayer, strategy=strategy, name="dilan")

    player_public_data = game_state.extract_public_player_data()
    move = player.choose_move_type(player_public_data)
    placement = player.get_placement(player_public_data, strategy, player.hand, tiles_placed=[])\
        if move == TurnOutcome.PLACED else []

    j_action = util.convert_single_turn_to_j_action(move, placement)

    print(dumps(j_action))


if __name__ == "__main__":
    main()
