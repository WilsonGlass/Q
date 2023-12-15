import threading
import traceback
from time import time
from socketserver import BaseRequestHandler, TCPServer, ThreadingMixIn
from socket import socket
from typing import List

import select

from Q.Referee.referee import Referee
from Q.Server.player import ProxyPlayer
from Q.Util.Configurations.server_config import ServerConfig
from Q.Util.util import Util


# This is shared information between threads as the server handles clients concurrently
global_timer = None
conns: List[ProxyPlayer] = []
game_lock = threading.Lock()
time_lock = threading.Lock()
server_should_stop = threading.Event()
game_ran = False
server_config = ServerConfig()


def main(config: ServerConfig = None, port=None):
    try:
        if config:
            global server_config
            server_config = config

        server = ThreadedTCPServer(("localhost", port), ThreadedTCPRequestHandler)
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.start()

        while not server_should_stop.is_set():
            pass

        server.shutdown()
        server.server_close()
    except Exception as e:
        print(e)


class ThreadedTCPRequestHandler(BaseRequestHandler):
    def handle(self):
        """
        Handles clients on an individual basis. Socketserver runs this method on a clients connection to the server.
        """
        global game_lock
        global conns
        global server_should_stop
        global game_ran
        global server_config

        if self._gather_players(self.request, server_config):
            self._launch_game(conns, server_config)
        self.request.close()
        server_should_stop.set()

    def _launch_game(self, conns: List[ProxyPlayer], server_config: ServerConfig):
        """
        Launches the game once and locks the other threads until the game has been complete.
        """
        global game_ran
        global game_lock

        with game_lock:
            if not game_ran:
                pair_results = Referee().main(conns, server_config.ref_spec)
                print(Util().pair_results_to_jresults(pair_results))
                game_ran = True

    def _gather_players(self, server_socket: socket, server_config: ServerConfig) -> bool:
        """
        Tries to gather players in a certain amount of tries. Returns whether it was successful or not.
        """
        tries = 0
        gathered = False

        try:
            while not gathered:
                gathered = self._attempt_gather(server_socket, server_config)
                tries += 1
                if tries > server_config.server_tries:
                    return False
            return True
        except Exception as e:
            if not server_config.quiet:
                print(f"gather_players exception: {e}")
                print(traceback.print_exc())

    def _attempt_gather(self, server_socket: socket, server_config: ServerConfig, players_allotted: int = 4) -> bool:
        """
        Listens for player name. Once players_allotted join by providing their name or time_to_gather has been
        surpassed  (if the players joined is >= 2), this method will return whether there is a sufficient amount of
        players connected. We reset the global timer in case another call to attempt_gather is made.
        """
        global global_timer
        global conns

        initial_time = self._get_initial_time()
        while time() < initial_time + server_config.server_wait and len(conns) <= players_allotted:
            if select.select([server_socket], [], [], server_config.wait_for_signup)[0]:
                name = server_socket.recv(9999)
                if name:
                    conns.append(ProxyPlayer(name=name.decode("utf-8"), server_socket=server_socket))
        global_timer = None
        return True if len(conns) >= 2 else False

    def _get_initial_time(self):
        """
        Gets current time and sets global timer if it has not already been set. This is so every thread can share a
        timer.
        """
        global global_timer
        global time_lock

        with time_lock:
            if not global_timer:
                global_timer = time()
        return global_timer


class ThreadedTCPServer(ThreadingMixIn, TCPServer):
    """
    This class extends the functionality of the TCPServer by enabling threading support,
    allowing multiple clients to be handled concurrently.
    """
    daemon_threads = True


if __name__ == "__main__":
    main()
