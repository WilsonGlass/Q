from typing import List
from Q.Player.behaved_player import Player
from dataclasses import dataclass, field


@dataclass
class ClientConfig:
    """
    Represents the configuration for the client to connect to the server with.
    """
    players: List[Player] = field(default_factory=list)
    port: int = 12345
    host: str = "localhost"
    wait: int = 3
    quiet: int = True
