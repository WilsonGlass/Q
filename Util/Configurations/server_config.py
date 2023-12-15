from dataclasses import dataclass, field

from Q.Common.game_state import GameState
from Q.Util.Configurations.referee_config import RefereeConfig
from Q.Util.Configurations.score_config import ScoreConfig


@dataclass
class ServerConfig:
    """
    Represents the configuration to be passed into the server. These will be loaded and changed within server.py
    """
    ref_spec: RefereeConfig = field(default_factory=RefereeConfig)
    server_tries: int = 1
    server_wait: int = 20
    wait_for_signup: int = 6
    quiet: bool = True
    port: int = 12345
