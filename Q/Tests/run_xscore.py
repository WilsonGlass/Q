import sys
from jsonstream import loads, dumps

from Q.Common.rulebook import Rulebook
from Q.Util.util import Util
from Q.Common.game_state import GameState
from Q.Player.public_player_data import PublicPlayerData


# main method for reading json from the standard in and outputting to standard out
def main():
    stream = loads(sys.stdin.read())
    util = Util()
    given_map = util.convert_json_to_map(next(stream))
    tiles = util.convert_jplacements_to_tiles(next(stream))
    score = Rulebook.score_turn(tiles, given_map, [], False)
    print(dumps(score))


if __name__ == "__main__":
    main()
