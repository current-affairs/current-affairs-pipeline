from enum import Enum

class FeedStatus(Enum):
    Pending = 0
    Ignore = 1
    ReadyToTake = 2
    Picked = 3