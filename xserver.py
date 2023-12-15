#!/usr/bin/env python

import sys
from jsonstream import loads
from Q.Util.util import Util
from Q.Server import server


def main():
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        print("no port given")
        exit(1)

    stream = loads(sys.stdin.read())
    config = Util.get_server_config(next(stream))
    server.main(config=config, port=port)


if __name__ == "__main__":
    main()