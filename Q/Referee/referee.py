import traceback
from copy import deepcopy
from threading import Thread, Lock
from typing import List, Set, Optional, Callable, Dict
from Q.Common.Board.tile import Tile
from Q.Common.map import Map
from Q.Common.player_game_state import PlayerGameState
from Q.Common.rulebook import Rulebook
from Q.Common.Turn.turn import Turn
from Q.Common.Turn.turn_outcome import TurnOutcome
from Q.Referee.pair_results import PairResults
from Q.Player.behaved_player import Player
from Q.Referee.observer import Observer
from Q.Referee.referee_data import RefereeData

from Q.Util.Configurations.referee_config import RefereeConfig


class Referee:
    """
    Represents the static methods that supervise an individual game. May this be through setting up the game,
    interacting with players, eliminating cheaters, or running games to completion.
    """
    @staticmethod
    def main(player_list: List[Player], ref_config: RefereeConfig = RefereeConfig) -> PairResults:
        """
        executes the Q game for a given list of players
        :param player_list: list of players that will play the game
        :param ref_config: configuration to be passed into the referee
        :return winners and kicked players
        """
        game_state = ref_config.state0
        game_state.setup_state()
        ref_data = RefereeData(player_list, game_state, misbehaved=[], config=ref_config)
        Referee.signup_players(ref_data)
        return Referee.run_game(ref_data)

    @staticmethod
    def run_game(ref_data: RefereeData) -> PairResults:
        """
        Runs the given game state to completion and notifies a given observer of each state of the game.
        :param ref_data: Information the referee must keep track of between separate functions
        :return: winners and kicked players
        """
        if ref_data.config.observe:
            observer = Observer()
            observer.receive_a_state(deepcopy(ref_data.game_state))
        else:
            observer = None

        while not Referee.is_game_over(ref_data):
            try:
                current_player = ref_data.player_queue.pop(0)
                player_name = current_player.name()
                pub_data = ref_data.game_state.extract_public_player_data(player_name)
                try:
                    turn = Referee.run_method_with_time_limit(ref_data, current_player.take_turn, args=[pub_data])
                except Exception as e:
                    if not ref_data.config.quiet:
                        print(e)
                    Referee.remove_current_player(ref_data, current_player)
                    continue

                if Referee.is_valid_move(turn, deepcopy(ref_data.game_state.map), ref_data.game_state.get_active_player(current_player.name()), pub_data.num_ref_tiles):
                    Referee.handle_turn(turn, current_player, ref_data)
                    new_tiles = ref_data.game_state.draw_tiles_for_player(player_name)
                    Referee.send_player_tiles(new_tiles, current_player, ref_data)
                    if ref_data.config.observe:
                        observer.receive_a_state(deepcopy(ref_data.game_state))
                else:
                    Referee.remove_current_player(ref_data, current_player)
                    continue

                ref_data.player_queue.append(current_player)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
        Referee.end_game(ref_data, observer=observer)
        return Referee.get_pair_of_results(ref_data)

    @staticmethod
    def run_method_with_time_limit(ref_data: RefereeData, method: Callable, args=[]) -> any:
        """
        Waits for a given amount of seconds for a method to complete. If the thread is still alive after 6 seconds
        a TimeoutError is thrown.
        :param method: method to be called
        :param ref_data: dataclass with configurable information
        :param args: args to be passed into the method
        :return: whatever the method returns
        """
        result_container = []
        lock = Lock()

        def set_container():
            try:
                res = method(*args)
                with lock:
                    result_container.append(res)
            except Exception as e:
                print(e)
                print(traceback.format_exc())
                with lock:
                    pass

        t = Thread(target=set_container)
        t.daemon = True
        t.start()
        t.join(ref_data.config.per_turn)
        if t.is_alive():
            raise TimeoutError

        with lock:
            if result_container:
                return result_container[0]

    @staticmethod
    def is_game_over(ref_data: RefereeData):
        """
        is the game over according to the referee
        :param ref_data: data the referee needs to know
        :return: true if the game is over
        """
        return not ref_data.player_queue or ref_data.game_state.played_all_tiles() \
            or ref_data.game_state.has_all_passed_or_exchanged_for_a_round()

    @staticmethod
    def send_results(winner_names: Set[str], ref_data: RefereeData):
        """
        sends the results of the game to the respective player who are winners and losers
        :param winner_names: the names of the winners of the game
        :param ref_data: datat the referee needs to know
        """
        for player in ref_data.player_queue:
            try:
                if player.name() in winner_names:
                    Referee.run_method_with_time_limit(ref_data, player.win, args=[True])
                else:
                    Referee.run_method_with_time_limit(ref_data, player.win, args=[False])
            except Exception as e:
                if not ref_data.config.quiet:
                    print(e)
                Referee.remove_current_player(ref_data, player)

    @staticmethod
    def send_player_tiles(new_tiles: List[Tile], player: Player, ref_data: RefereeData):
        """
        sends a player new tiles by calling the player new-tiles API function
        :param new_tiles: the new tiles the player will receive
        :param player: the player who you are sending the update to
        :param ref_data: Current state of the referee
        """
        if not new_tiles:
            return
        Referee.try_player_method(ref_data, player, player.new_tiles, args=[new_tiles])

    @staticmethod
    def is_valid_move(turn: Turn, given_map: Map, current_player: PlayerGameState, num_of_ref_tiles: int):
        """
        is this a valid move according to the rulebook?
        :param turn: the turn the player wants to perform
        :param given_map: the map tiles are placed on
        :param current_player: the player that is currently trying to place tiles
        :param num_of_ref_tiles: the num of ref tiles in the game
        :return: true if the turn is valid according to the rulebook else false
        """
        copy_hand = current_player.hand.copy()
        for tile in turn.placements.values():
            if tile not in copy_hand:
                return False
            copy_hand.remove(tile)

        if turn.turn_outcome == TurnOutcome.PLACED:
            return Rulebook.valid_placements(given_map, turn.placements)
        if turn.turn_outcome == TurnOutcome.REPLACED:
            return Rulebook.valid_replacement(num_of_ref_tiles, current_player.hand)
        return True


    @staticmethod
    def start_from_state(ref_data: RefereeData) -> PairResults:
        """
        Initializes players in at a particular given state
        :param ref_data: referee data with configuration
        :return: winners and kicked players
        """
        Referee.setup_players(ref_data)
        return Referee.run_game(ref_data)

    @staticmethod
    def signup_players(ref_data: RefereeData):
        """
        Starts the game with the given players and some given game
        :param ref_data: Data pertaining to the referee
        """
        for player in ref_data.player_queue:
            hand = ref_data.game_state.draw_tiles(6)
            player_game_state = PlayerGameState(name=player.name(), hand=hand, points=0)
            ref_data.game_state.signup_player(player_game_state)
            Referee.try_player_method(ref_data, player, player.setup,
              [ref_data.game_state.extract_public_player_data(player.name()), ref_data.game_state.referee_deck])

    @staticmethod
    def setup_players(ref_data: RefereeData):
        """
        setups the player by calling the setup API for each player
        :param ref_data: Data pertaining to the referee
        """
        players_to_remove = []
        for player in ref_data.player_queue:
            try:
                pub_data = ref_data.game_state.extract_public_player_data(player.name())
                hand = pub_data.current_player_data.hand
                Referee.run_method_with_time_limit(ref_data, player.setup, args=[pub_data, hand])
            except Exception as e:
                if not ref_data.config.quiet:
                    print(f"Exception occurred in setup_players: {e}")
                players_to_remove.append(player)

        for player in players_to_remove:
            Referee.remove_current_player(ref_data, player)
            ref_data.player_queue.remove(player)

    @staticmethod
    def try_player_method(ref_data: RefereeData, player: Player, method: Callable, args: List = []):
        """
        Tries a player method with time limit and kicks them if an exception is raised. Likely
        a timeout.
        """
        try:
            Referee.run_method_with_time_limit(ref_data, method, args=args)
        except Exception as e:
            if not ref_data.config.quiet:
                print(f"Exception occurred in setup_players: {e}")
            Referee.remove_current_player(ref_data, player)

    @staticmethod
    def remove_current_player(ref_data: RefereeData, misbehaved_player: Player):
        """
        NOTE: may need to call continue ofter this function to not add the player back to the queue
        """
        ref_data.misbehaved.append(misbehaved_player)
        ref_data.player_queue.remove(misbehaved_player)
        misbehaved_hand = misbehaved_player.hand
        misbehaved_player.hand = []
        ref_data.game_state.referee_deck.extend(misbehaved_hand)

    @staticmethod
    def remove_placements_from_hand(turn: Turn, hand: List[Tile]):
        """
        Removes tiles placed from hand after turn
        """
        for tile in turn.placements.values():
            hand.remove(tile)

    @staticmethod
    def handle_turn(turn: Turn, current_player: Player, ref_data: RefereeData):
        """
        Tells the game state to process a turn and removes tiles from hand if placed.
        """
        if turn.turn_outcome == TurnOutcome.PLACED:
            ref_data.game_state.process_turn(turn, current_player.name())
            Referee.remove_placements_from_hand(turn, current_player.hand)
        elif turn.turn_outcome == TurnOutcome.REPLACED or turn.turn_outcome == TurnOutcome.PASSED:
            ref_data.game_state.process_turn(turn, current_player.name())

    @staticmethod
    def end_game(ref_data: RefereeData, observer: Optional[Observer] = None):
        """
        Sends results and notifies the observer that the game has ended.
        """
        game_results = Referee.get_pair_of_results(ref_data)
        Referee.send_results(game_results.winners, ref_data)
        if observer:
            observer.game_over()
        return Referee.get_pair_of_results(ref_data)

    @staticmethod
    def get_max_points(ref_data: RefereeData, scores: Dict[str, int]):
        """
        Gets max points for all behaving players
        """
        misbehaved_names = list(map(Player.name, ref_data.misbehaved))
        valid_scores = []
        for name, score in scores.items():
            if name not in misbehaved_names:
                valid_scores.append(score)
        return max(valid_scores) if len(valid_scores) else -1

    @staticmethod
    def get_winners(ref_data: RefereeData) -> Set[str]:
        """
        Gets the winner's names by highest score
        :param ref_data: Data pertaining to the referee
        """
        scores = ref_data.game_state.get_scores()
        max_points = Referee.get_max_points(ref_data, scores)
        winners = set()
        for player in ref_data.player_queue:
            pgs = ref_data.game_state.get_player_by_name(player.name())
            if pgs.points == max_points and player not in ref_data.misbehaved:
                winners.add(player.name())
        return winners

    @staticmethod
    def get_pair_of_results(ref_data: RefereeData):
        """
        Returns the results of the game: winners and misbehaved.
        """
        winners = Referee.get_winners(ref_data)
        return PairResults(winners, [player.name() for player in ref_data.misbehaved])
