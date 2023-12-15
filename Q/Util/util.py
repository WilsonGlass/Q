import json
from collections import defaultdict
from typing import Set, Dict, List, Union

from Q.Common.Turn.turn import Turn
from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Common.game_state import GameState
from Q.Common.Board.pos import Pos
from Q.Common.map import Map
from Q.Common.Board.tile import Tile
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Player.Strategy.Cheat.bad_ask_for_tiles import BadAskForTiles
from Q.Player.Strategy.Cheat.no_fit import NoFit
from Q.Player.Strategy.Cheat.non_adjacent_coordinate import NonAdjacentCoordinate
from Q.Player.Strategy.Cheat.not_a_line import NotALine
from Q.Player.Strategy.Cheat.tile_not_owned import TileNotOwned
from Q.Player.cheater import Cheater
from Q.Player.Strategy.Cheat.cheat import Cheat
from Q.Player.Strategy.cheater_strategy import CheaterStrategy
from Q.Player.Strategy.dag import Dag
from Q.Player.Strategy.ldasg import LDasg
from Q.Player.Strategy.player_strategy import PlayerStrategy
from Q.Player.count_player import CountPlayer
from Q.Player.behaved_player import Player
from Q.Common.public_player_data import PublicPlayerData
from Q.Common.Turn.turn_outcome import TurnOutcome
from Q.Player.mock_player import MockPlayer
from Q.Referee.pair_results import PairResults
from Q.Util.Configurations.client_config import ClientConfig
from Q.Util.Configurations.referee_config import RefereeConfig
from Q.Util.Configurations.score_config import ScoreConfig
from Q.Util.Configurations.server_config import ServerConfig


class Util:
    """
    # Represents a utility class used mainly for json parsing
    """
    def jactor_spec_a_to_player(self, jactor):
        """
        A JActorSpecA is one of:
        - a JSON array of two elements: [JName, JStrategy]
        - a JSON array of three elements: [JName, JStrategy, JExn]
        - a JSON array of four elements: [JName, JStrategy, "a cheat", JCheat]
        """
        jname = jactor[0]
        jstrategy = jactor[1]
        strategy = self.convert_jstrategy_to_strategy(jstrategy)
        if len(jactor) == 2:
            return Player(jname, strategy)
        if len(jactor) == 3:
            jexn = jactor[2]
            return MockPlayer(jname, strategy, [], jexn)
        elif len(jactor) == 4:
            jcheat = jactor[3]
            cheater_strategy = CheaterStrategy(self.convert_jcheat_to_cheat(jcheat), self.convert_jstrategy_to_strategy(jstrategy))
            return Cheater(jname, cheater_strategy)

    def jactor_spec_b_to_player(self, jactor):
        """
        A JActorSpecB is one of:
        - a JSON array of two elements: [JName, JStrategy]
        - a JSON array of three elements: [JName, JStrategy, JExn]
        - a JSON array of three four elements: [JName, JStrategy, "a cheat", JCheat]
        - a JSON array of four elements: [JName, JStrategy, JExn, Count]
        """
        jname = jactor[0]
        jstrategy = jactor[1]
        strategy = self.convert_jstrategy_to_strategy(jstrategy)
        if len(jactor) == 2:
            return Player(jname, strategy)
        if len(jactor) == 3:
            jexn = jactor[2]
            return MockPlayer(jname, strategy, [], jexn)
        if len(jactor) == 4 and jactor[2] == "a cheat":
            jcheat = jactor[3]
            cheater_strategy = CheaterStrategy(self.convert_jcheat_to_cheat(jcheat), self.convert_jstrategy_to_strategy(jstrategy))
            return Cheater(jname, cheater_strategy)
        else:
            jexn = jactor[2]
            count = jactor[3]
            return CountPlayer(jname, strategy, [], jexn, count)

    def pair_results_to_jresults(self, pair_results: PairResults):
        jwinners = sorted(list(pair_results.winners))
        jmisbehaved = list(pair_results.misbehaved)
        jresults = [jwinners, jmisbehaved]
        return jresults

    def jactors_to_players(self, jactors) -> List[Player]:
        players = []
        for jactorspec in jactors:
            jname = jactorspec[0]
            strategy = self.convert_jstrategy_to_strategy(jactorspec[1])
            if len(jactorspec) == 3:
                jexn = jactorspec[2]
                players.append(MockPlayer(name=jname, strategy=strategy, exn=jexn))
            else:
                players.append(Player(jname, strategy))
        return players

    def convert_jstate_to_gamestate(self, jstate):
        """
         { "map"      : JMap,

        "tile*"    : [JTile, ..., JTile],

        "players"  : [JPlayer, ..., JPlayer] }

        :param jstate:
        :return:
        """
        map = self.convert_json_to_map(jstate["map"])
        tiles = [self.json_to_tile(t) for t in jstate["tile*"]]
        players = self.convert_jplayers_to_playergamestates(jstate["players"])
        game_state = GameState(given_map=map, tiles=tiles, player_game_states=players)
        return game_state

    def convert_gamestate_to_jstate(self, game_state: GameState):
        jstate = {
            "map": self.convert_map_to_jmap(game_state.map),
            "tile*": [self.convert_tile_to_json(tile) for tile in game_state.referee_deck],
            "players": [self.convert_player_game_state_to_jplayer(name, player) for name, player in game_state.players.items()]
        }
        return jstate

    def convert_gamestate_to_jpub(self, game_state: GameState, player: Player):
        pub_data = game_state.extract_public_player_data(player.name())
        jplayer_data = self.convert_player_game_state_to_jplayer(pub_data.current_player_data)
        players = [jplayer_data]
        for points in pub_data.other_points:
            players.append(points)
        jpub = {
            "map": self.convert_map_to_jmap(game_state.map),
            "tile*": len([self.convert_tile_to_json(tile) for tile in game_state.referee_deck]),
            "players": players
        }
        return jpub

    def convert_public_player_data_to_jpub(self, pub_data: PublicPlayerData):
        """
        Converts public player data into a jpub.
        """
        jplayer_data = self.convert_player_game_state_to_jplayer(pub_data.current_player_data)
        players = [jplayer_data]
        for other_player_point in pub_data.other_points:
            players.append(other_player_point)
        jpub = {
            "map": self.convert_map_to_jmap(pub_data.current_map),
            "tile*": [self.convert_tile_to_json(tile) for tile in pub_data.current_player_data.hand],
            "players": players
        }
        return jpub

    def convert_player_to_public_player_knowledge(self, pub_data: PublicPlayerData):
        map = self.convert_map_to_jmap(pub_data.current_map)
        num_ref_tiles = pub_data.num_ref_tiles
        players = [self.convert_player_game_state_to_jplayer(pub_data.current_player_data)]
        for score in pub_data.other_points:
            players.append(score)
        jpub = {
            "map": map,
            "tile*": num_ref_tiles,
            "players": players
        }
        return jpub

    def convert_jpub_to_pub_data(self, jpub):
        current_player_data = self.convert_jplayer_to_playergamestate(jpub["players"][0])
        other_points = jpub["players"][1:]
        current_map = self.convert_json_to_map(jpub["map"])
        return PublicPlayerData(num_ref_tiles=jpub["tile*"], current_map=current_map, current_player_data=current_player_data, other_points=other_points)

    def convert_player_game_state_to_jplayer(self, player: PlayerGameState):
        jplayer = {
            "score": player.points,
            "name": player.name,
            "tile*": [self.convert_tile_to_json(tile) for tile in player.hand]
        }
        return jplayer

    def convert_jplayers_to_playergamestates(self, jplayers) -> List[PlayerGameState]:
        players = []
        for jplayer in jplayers:
            name = jplayer["name"]
            score = jplayer["score"]
            tiles = [self.json_to_tile(t) for t in jplayer["tile*"]]
            players.append(PlayerGameState(name=name, hand=tiles, points=score))
        return players

    def convert_jplayer_to_playergamestate(self, jplayer) -> PlayerGameState:
        name = jplayer["name"]
        score = jplayer["score"]
        tiles = [self.json_to_tile(t) for t in jplayer["tile*"]]
        return PlayerGameState(name=name, hand=tiles, points=score)

    def convert_single_turn_to_j_action(self, outcome: TurnOutcome, placement: Dict[Pos, Tile]):
        """
        converts a single turn to a jaction with the given outcome and given placement
        :param outcome the outcome of the turn
        :param placement: the placement
        :return: A j_action which is either pass, replace, or a 1Placement
        """
        if outcome == TurnOutcome.PASSED:
            return "pass"
        if outcome == TurnOutcome.REPLACED:
            return "replace"
        if outcome == TurnOutcome.PLACED:
            return self.convert_placement_to_jplacement(placement)

    def convert_turn_to_j_choice(self, turn: Turn):
        if turn.turn_outcome == TurnOutcome.PASSED:
            return "pass"
        elif turn.turn_outcome == TurnOutcome.REPLACED:
            return "replace"
        elif turn.turn_outcome == TurnOutcome.PLACED:
            return [self.convert_placement_to_jplacement({pos: tile}) for pos, tile in turn.placements.items()]

    def convert_jchoice_to_turn(self, jchoice):
        if jchoice == "pass":
            return Turn(turn_outcome=TurnOutcome.PASSED)
        elif jchoice == "replace":
            return Turn(turn_outcome=TurnOutcome.REPLACED)
        else:
            placements = self.convert_jplacements_to_tiles(jchoice)
            return Turn(turn_outcome=TurnOutcome.PLACED, placements=placements)

    def convert_placement_to_jplacement(self, placement: Dict[Pos, Tile]) -> dict:
        """
        convert placement to a jplacement of the given placement
        :param placement: the given placements to be converted to a jplacement
        :return the j_placement
        """
        if len(placement) != 1:
            raise Exception("Placements must be of length 1")
        pos = list(placement.keys())[0]
        tile = list(placement.values())[0]
        jpos = self.__create_json_pos(pos)
        jtile = self.convert_tile_to_json(tile)
        return {"coordinate": jpos, "1tile": jtile}

    def convert_jplacements_to_tiles(self, python_json) -> Dict[Pos, Tile]:
        """
        Converts jplacements to dict from pos to tile
        JPlacements is an array of the following shape:
        [{"coordinate": JCoordinate, "1tile": JTile}, ...]
        """
        pos_to_tile = {}
        for placement in python_json:
            pos = self.convert_coorindate_to_pos(placement["coordinate"])
            tile = self.json_to_tile(placement["1tile"])
            pos_to_tile[pos] = tile
        return pos_to_tile

    def convert_coorindate_to_pos(self, python_json) -> Pos:
        return Pos(python_json["column"], python_json["row"])

    def convert_jstrategy_to_strategy(self, strat_string: str) -> PlayerStrategy:
        """
        converts a string representation of a strategy to a player strategy
        :param strat_string the given strategy to be converted to a playerstrategy
        """
        if strat_string == "dag":
            return Dag()
        if strat_string == "ldasg":
            return LDasg()


    def convert_json_to_map(self, python_json: List[Union[int, List[Union[int, Dict[str, str]]]]]) -> Map:

        """
        Converts python_json from a list of json
        :param python_json: json that will be parsed into
        :return: a default dict from positions to their corresponding tiles
        """
        map_rep = defaultdict()
        for row in python_json:
            for i in range(1, len(row)):
                ci, tile = row[i]
                map_tile = Util.json_to_tile(tile)
                pos = Pos(x=ci, y=row[0])
                map_rep[pos] = map_tile
        return Map(config=map_rep)

    def convert_game_state_to_false_or_j_map(self, game_state: GameState, tiles: [Pos, Tile]) -> str:
        """
        Returns expected output:
        The expected output is either false or the newly constructed JMap if the placement is legal.
        """
        try:
            game_state.place_tiles(tiles)
        except:
            return json.dumps(False)
        j_map = self.convert_map_to_jmap(game_state.map)
        return json.dumps(j_map)

    def convert_map_to_jmap(self, given_map: Map):
        """
        Converts map object into json readable JMap such as:
        [[row, [col, {"color":  color, "shape":  shape}], [col, {...}], ...], [row, [col, {...}, ...]]]
        """
        j_map_dict: [int, List[Dict[str, str]]] = defaultdict(list)
        for pos, tile in sorted(given_map.tiles.items(), key=lambda item: item[0].x):
            json_tile = self.convert_tile_to_json(tile)
            if pos.y not in j_map_dict:
                j_map_dict[pos.y] = []
            j_cells = j_map_dict.get(pos.y)
            j_cells.append([pos.x, json_tile])

        j_map = []
        for y, jcell in sorted(j_map_dict.items()):
            jcell.insert(0, y)
            j_map.append(jcell)

        return j_map

    def create_names(self, num_of_players: int):
        """
        Automatically creates player names
        :param num_of_players: Number of players to create names for
        """
        return [i for i in range(num_of_players)]

    @staticmethod
    def convert_jplayer_to_player(python_json, strategy: PlayerStrategy, name: str) -> Player:
        """
        Converts JSON representation of a player into an actual Q player
        :param python_json: JSON representation of a player
        :param strategy: Strategy to create player with
        :param name: Name of player to be created
        """
        player_tiles = [Util.json_to_tile(tile) for tile in python_json["tile*"]]
        return Player(name=name, strategy=strategy, hand=player_tiles)

    @staticmethod
    def write_legal_json_coordinates(given_map: Map, tile: Tile) -> str:
        """
        Determines legal moves for a tile and outputs the data as json formatted JCoordinates
        :param given_map: the map for where valid positions are to be searched
        :param tile: the tile which will be placed on the map
        :return: json of the valid JCoordinates
        """
        positions = Rulebook.get_legal_positions(given_map, tile, [])
        dict_positions = Util.__convert_positions_to_sorted_dicts(positions)
        return json.dumps(dict_positions)

    @staticmethod
    def json_to_tile(python_json_tile: Dict[str, str]) -> Tile:
        """
        Converts a json tile to an internal representation of a tile
        :param python_json_tile: the tile to be converted
        :return: Tile conversion result
        """
        color = TileColor.get_color_by_name(python_json_tile["color"])
        shape = TileShape.get_shape_by_name(python_json_tile["shape"])
        return Tile(shape, color)

    def convert_tile_to_json(self, tile: Tile) -> Dict[str, str]:
        """
        Converts internal representation of a tile to JSON representation
        """
        return {"color": tile.color.get_name(), "shape": tile.shape.get_name()}

    @staticmethod
    def __convert_positions_to_sorted_dicts(positions: Set[Pos]) -> List[Dict[str, int]]:
        """
        Converts given positions into row-column json coordinates
        :param positions: positions to be converted
        :return: the converted positions in json coordinate form
        """
        row_col_positions = sorted(positions, key=lambda pos: (pos.y, pos.x))
        positions = [Util.__create_json_pos(pos) for pos in row_col_positions]
        return positions

    @staticmethod
    def __create_json_pos(pos: Pos) -> Dict[str, int]:
        """
        Converts a pos into a dictionary pos
        :param pos: the pos that will be converted
        :return: the converted pos
        """
        return {"row": pos.y, "column": pos.x}

    def convert_jcheat_to_cheat(self, jcheat: str) -> Cheat:
        if jcheat == "non-adjacent-coordinate":
            return NonAdjacentCoordinate()
        elif jcheat == "tile-not-owned":
            return TileNotOwned()
        elif jcheat == "not-a-line":
            return NotALine()
        elif jcheat == "bad-ask-for-tiles":
            return BadAskForTiles()
        elif jcheat == "no-fit":
            return NoFit()

    @staticmethod
    def get_server_config(config: dict) -> ServerConfig:
        return ServerConfig(
            port=config["port"],
            server_tries=config["server-tries"],
            server_wait=config["server-wait"],
            wait_for_signup=config["wait-for-signup"],
            quiet=config["quiet"],
            ref_spec=RefereeConfig(
                state0=Util().convert_jstate_to_gamestate(config["ref-spec"]["state0"]),
                config_s=ScoreConfig(
                    q_bonus=config["ref-spec"]["config-s"]["qbo"],
                    final_bonus=config["ref-spec"]["config-s"]["fbo"]
                ),
                per_turn=config["ref-spec"]["per-turn"],
                observe=config["ref-spec"]["observe"],
                quiet=config["ref-spec"]["quiet"]
            )
        )

    @staticmethod
    def get_client_config(config: dict) -> ClientConfig:
        return ClientConfig(
            players=list(map(Util().jactor_spec_b_to_player, config["players"])),
            port=config["port"],
            host=config["host"],
            wait=config["wait"],
            quiet=config["quiet"]
        )
