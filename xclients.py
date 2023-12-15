#!/usr/bin/env python

import sys
import threading
from functools import partial

from jsonstream import loads
from Q.Util.util import Util
from Q.Client import client


def main():
    """
    A thread gets created for each jactorb passed in. They act as their own connection.
    """
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        print("no port given")
        exit(1)

    stream = loads(sys.stdin.read())
    client_config = Util.get_client_config(next(stream))
    threads = []
    for player in client_config.players:
        partial_main = partial(client.main, client_config, player.name(), port=port)
        thread = threading.Thread(target=partial_main)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()