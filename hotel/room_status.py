# With Enum
from enum import Enum

class RoomStatus(Enum):
    CHECKED_IN = 'CHECKED_IN'
    CHECKED_OUT = 'CHECKED_OUT'
    CLEANED = 'CLEANED'