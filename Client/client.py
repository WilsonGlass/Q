import asyncio
import secrets
import string
import traceback
import socket

from Q.Client.referee import ProxyReferee
from Q.Player.behaved_player import Player
from Q.Util.Configurations.client_config import ClientConfig


def main(client_config: ClientConfig = ClientConfig(), given_name: str = None, port: int = 12345):
    """
    Where the client connects to the server, provides a name, and sends back information parsed in the proxy referee.
    Configurable client information is set in the client config. This must be parsed before being passed in.
    """
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((client_config.host, port))

        characters = string.ascii_letters + string.digits
        for given_player in client_config.players:
            if given_player.name() == given_name:
                player = given_player
                break
        else:
            generated_name = given_name if given_name else ''.join(secrets.choice(characters) for _ in range(5))
            player = Player(name=generated_name)
        proxy_ref = ProxyReferee(player, client_socket)
        client_socket.sendall(player.name().encode("utf-8"))
        proxy_ref.stream()
        client_socket.close()
    except Exception as e:
        traceback.print_exc()
        print(e)


if __name__ == "__main__":
    main()
