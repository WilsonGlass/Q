import json
import sys
from jsonstream import loads
from Q.Referee.observer import Observer

from Q.Referee.referee import Referee
from Q.Referee.referee_data import RefereeData
from Q.Util.util import Util


def main(show=False):
    """
    Test harness to run a game with an observer.
    """
    stream = loads(sys.stdin.read())
    util = Util()
    observer = Observer()

    jstate = next(stream)
    jactors = next(stream)

    game_state = util.convert_jstate_to_gamestate(jstate)
    players = list(map(lambda jactorspeca: util.jactor_spec_a_to_player(jactorspeca), jactors))
    referee = Referee()
    ref_data = RefereeData(players, game_state, [])
    pair_results = referee.start_from_state(ref_data, observer=observer)
    print(json.dumps(util.pair_results_to_jresults(pair_results)))
    if show:
        Observer().make_gui()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        show = sys.argv[1] == "-show"
        main(show)
    else:
        main(True)
