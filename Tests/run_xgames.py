import json
import sys
from jsonstream import loads

from Q.Referee.referee import Referee
from Q.Util.util import Util


# main method for reading json from the standard in and outputting to standard out
def main():
    stream = loads(sys.stdin.read())
    util = Util()

    jstate = next(stream)
    jactors = next(stream)

    game_state = util.convert_jstate_to_gamestate(jstate)
    players = util.jactors_to_players(jactors)
    player_game_states = util.convert_jplayers_to_playergamestates(jstate["players"])
    name_to_player_game = {player.name(): pgs for player, pgs in zip(players, player_game_states)}
    game_state.players = name_to_player_game
    referee = Referee()
    pair_results = referee.start_from_state(players, game_state)
    print(json.dumps(util.pair_results_to_jresults(pair_results)))


if __name__ == "__main__":
    main()
