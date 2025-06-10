from enum import Enum, auto

class SortType(Enum):
    LowestValue = auto()
    HighestValue = auto()
    NameAsc = auto()
    NameDesc = auto()
    NameLength = auto()