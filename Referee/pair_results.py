from typing import Set, List
from dataclasses import dataclass


@dataclass
class PairResults:
    """
    Represents a pair of names of the winning player(s) and the names those players that misbehaved - from specs webpage
    """
    winners: Set[str]
    misbehaved: List[str]
