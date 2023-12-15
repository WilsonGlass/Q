from dataclasses import dataclass


@dataclass
class ScoreConfig:
    """
    Represents the score configuration. If the scores are desired to be changed then they will be loaded and altered.
    """
    final_bonus: int = 5
    q_bonus: int = 5
