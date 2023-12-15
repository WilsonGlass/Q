import random
from copy import deepcopy
from typing import List, Dict, Set, Union

from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.Board.pos import Pos
from Q.Common.render import Render
from Q.Common.Turn.turn import Turn
from Q.Common.Turn.turn_outcome import TurnOutcome
from Q.Common.Board.tile_color import TileColor
from Q.Common.Board.tile_shape import TileShape
from Q.Common.public_player_data import PublicPlayerData
from Q.Referee.pair_results import PairResults

NUM_OF_Q_TILES = 1080
MAX_NUM_OF_PLAYERS = 4
NUM_OF_EACH_KIND = 30
MAX_NUM_OF_TILES_IN_PLAYER_HAND = 6


class GameState:
    """
    Represents the state of the game available to the referee
    """

    def __init__(self, config: PublicPlayerData = None, tiles: List[Tile] = [],
                 player_game_states: List[PlayerGameState] = [], given_map: Map = Map(), random_seed=None):
        """
        :param config: the player public data - used for testing
        :param tiles: the tiles in which the ref hold
        :param player_game_states: the states of all players
        :param given_map: the map at which you place tiles on
        :param random_seed: the seed of the referee deck
        :param rulebook: the rules of the game
        """
        self.players: List[PlayerGameState] = player_game_states
        self.consecutive_exc_or_rep = 0

        if config:
            self.referee_deck = self.create_randomize_deck(config.num_ref_tiles, random_seed)
            self.map = config.current_map
        else:
            self.map = given_map
            if tiles:
                self.referee_deck = tiles
            else:
                self.referee_deck = self.create_randomize_deck(NUM_OF_Q_TILES, random_seed)

    def place_ref_tile(self):
        """
        Takes first tile off the top of the ref deck and places at 0,0
        """
        ref_tile = {Pos(0, 0): self.draw_tiles(1)[0]}
        self.map = Map(config=ref_tile)

    def create_randomize_deck(self, num_of_ref_tiles=NUM_OF_Q_TILES, seed=None) -> List[Tile]:
        """
        Initializes Q's set of num_of_ref_tiles, 6 different colors, 6 different shapes, 30 of each kind randomized.
        """
        if seed:
            random.seed(seed)

        deck = []
        for color in TileColor:
            for shape in TileShape:
                for _ in range(NUM_OF_EACH_KIND):
                    deck.append(Tile(shape, color))

        random.shuffle(deck)
        return deck[:num_of_ref_tiles]

    def setup_state(self):
        """
        sets up the state of the game
        """
        if self.referee_deck is None:
            self.referee_deck = self.create_randomize_deck(1080)

        if not len(self.map.tiles):
            self.map = Map()
            self.place_ref_tile()

    def signup_player(self, player: PlayerGameState):
        """
        effect: adds the given Player to the front of the queue
        effect: adds an entry to the scores for the given player
        param: player: the given player to be added to the game
        """
        if len(self.players) < MAX_NUM_OF_PLAYERS:
            self.players.append(player)

    def played_all_tiles(self) -> bool:
        """
        Has any Player played all of their tiles?
        The referee will not replenish the tiles if this is the case
        :return: True if the player has played all of their tiles else return false
        """
        return any(not len(player_game_state.hand) for player_game_state in self.players)

    def get_player_by_name(self, name):
        for player in self.players:
            if player.name == name:
                return player

    def has_all_passed_or_exchanged_for_a_round(self):
        """
        Has every place passed or replaced for an entire round
        :returns true if all players have passed or replaced else false
        """
        return self.consecutive_exc_or_rep == len(self.players)

    def extract_public_player_data(self, active_name: str) -> PublicPlayerData:
        """
        Extracts a copy of the data to be sent to a Player when it is its turn
        :return the player public data of the game state
        """
        num_ref_tiles = len(self.referee_deck)
        current_map = deepcopy(self.map)
        player = self.get_active_player(active_name)
        other_points = self.get_other_points(active_name)
        return PublicPlayerData(num_ref_tiles=num_ref_tiles, current_map=current_map, current_player_data=player, other_points=other_points)

    def get_other_points(self, active_name: str) -> List[Union[PlayerGameState, int]]:
        """
        Gets public information that a player can know about the player queue. (their points)
        """
        public_player_queue = []
        for player in self.players:
            if active_name != player.name:
                public_player_queue.append(player.points)
        return public_player_queue

    def get_active_player(self, active_name: str) -> PlayerGameState:
        """
        Gets the active player's PlayerGameState
        """
        for player in self.players:
            if active_name == player.name:
                return player

    def get_scores(self) -> Dict[str, int]:
        """
        gets the scores of the players
        :return: the name to number of points a player has
        """
        scores = {}
        for player in self.players:
            scores[player.name] = player.points
        return scores

    def process_turn(self, turn: Turn, name: str):
        """
        Processes a turn which a Player submits
        :param turn: turn to be processed
        :param name: the name of the player that performed the turn
        """
        outcome = turn.turn_outcome
        if outcome is TurnOutcome.PASSED:
            pass
        if outcome is TurnOutcome.REPLACED:
            self.turn_replace(name)
        if outcome is TurnOutcome.PLACED:
            self.turn_placed(turn.placements, name)

        is_game_over = len(self.get_player_by_name(name).hand) == 0
        additional_points = Rulebook.score_turn(turn.placements, self.map, self.get_player_by_name(name).hand,
                                                     end_game=is_game_over)
        self.get_player_by_name(name).points += additional_points
        self.update_consecutive_exc_or_rep(outcome)

    def turn_placed(self, placements: Dict[Pos, Tile], name: str):
        """
        Places the given tiles on the map and gives the player their new hand
        :param name: the name of which player is placing
        :param placements: Placements to be put on the map
        """
        self.place_tiles(placements)

        placed_tiles = list(placements.values())
        self.get_player_by_name(name).hand = list(filter(lambda a: a not in placed_tiles, self.get_player_by_name(name).hand))

    def draw_tiles_for_player(self, name: str) -> List[Tile]:
        """
        draws the max number of tiles possible for a player
        :param name: the name of the player
        :return: the tiles of the player
        """
        num_of_new_tiles = MAX_NUM_OF_TILES_IN_PLAYER_HAND - len(self.get_player_by_name(name).hand)
        new_tiles = self.draw_tiles(num_of_new_tiles)
        self.get_player_by_name(name).hand.extend(new_tiles)
        return self.get_player_by_name(name).hand

    def turn_replace(self, name: str):
        """
        :param name: the players name
        Replaces tiles from hand with top of ref deck
        """
        player_hand = self.get_player_by_name(name).hand
        self.get_player_by_name(name).hand = []
        self.add_tiles_to_referee_deck(player_hand)

    def place_tiles(self, tiles: Dict[Pos, Tile]):
        """
        We assume that a placement is already valid
        attempts to place all the given tiles and corresponding positions on the map
        :param tiles: a dictionary of keyed positions to their corresponding tiles
        """
        for pos, tile in tiles.items():
            self.map.add_tile_to_board(tile, pos)

    def update_consecutive_exc_or_rep(self, outcome: TurnOutcome):
        """
        updates the consecutive exchanged or replaced for determining
        :param outcome: outcome of the most recent turn
        """
        if outcome == TurnOutcome.PLACED:
            self.consecutive_exc_or_rep = 0
        else:
            self.consecutive_exc_or_rep += 1

    def add_tiles_to_referee_deck(self, tiles: List[Tile]):
        """
        adds the given tiles to the bag
        :param tiles:  the tile to be added to the referee deck
        """
        self.referee_deck.extend(tiles)

    def draw_tiles(self, n: int) -> List[Tile]:
        """
        draws tiles from the referee deck. If the referee has less than n tiles return the rest of the referee deck
        :param n: the number of tiles to be drawn
        :return: the drawn tiles
        """
        if n > len(self.referee_deck):
            return []
        else:
            tiles = deepcopy(self.referee_deck[:n])
            del self.referee_deck[:n]

        return tiles

    def render(self):
        """
        renders the map board
        a pop-up will appear of the rendered board
        """
        Render(self.map.tiles).show()
