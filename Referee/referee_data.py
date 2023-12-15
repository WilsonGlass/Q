from dataclasses import dataclass, field
from typing import List
from Q.Common.game_state import GameState
from Q.Player.base import Player
from Q.Util.Configurations.referee_config import RefereeConfig


@dataclass
class RefereeData:
    """
    Information pertaining to the referee
    """
    player_queue: List[Player]
    game_state: GameState
    misbehaved: List[Player]
    config: RefereeConfig = field(default_factory=RefereeConfig)
