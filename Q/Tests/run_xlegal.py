import sys
from json import dumps

from jsonstream import loads

from Q.Util.util import Util


# main method for reading json from the standard in and outputting to standard out
def main():
    stream = loads(sys.stdin.read())
    util = Util()
    game_state = util.convert_jpub_json_to_game_state(next(stream))
    tiles = util.convert_jplacements_to_tiles(next(stream))
    json_coords = util.convert_game_state_to_false_or_j_map(game_state, tiles=tiles)
    print(dumps(json_coords))


if __name__ == "__main__":
    main()
