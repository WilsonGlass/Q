from dataclasses import dataclass, field

from Q.Util.Configurations.score_config import ScoreConfig
from Q.Common.game_state import GameState


@dataclass
class RefereeConfig:
    """
    Represents the referee configuration. Alters all of these configurable variables per request.
    """
    state0: GameState = field(default_factory=GameState)
    quiet: bool = True
    per_turn: int = 6
    observe: bool = False
    config_s: ScoreConfig = field(default_factory=ScoreConfig)
