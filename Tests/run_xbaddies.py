import asyncio
import json
import sys
from jsonstream import loads
from Q.Referee.observer import Observer

from Q.Referee.referee import Referee
from Q.Referee.referee_data import RefereeData
from Q.Util.util import Util


def main():
    """
    Runs game to completion with xbaddies requirements.txt
    """
    stream = loads(sys.stdin.read())
    util = Util()

    jstate = next(stream)
    jactorsb = next(stream)

    game_state = util.convert_jstate_to_gamestate(jstate)
    players = list(map(lambda jactorspecb: util.jactor_spec_b_to_player(jactorspecb), jactorsb))
    ref_data = RefereeData(players, game_state, [])
    referee = Referee()
    pair_results = referee.start_from_state(ref_data)
    print(json.dumps(util.pair_results_to_jresults(pair_results)))


if __name__ == "__main__":
    main()
