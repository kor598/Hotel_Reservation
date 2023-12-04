# With Enum
from enum import Enum
#room states
class RoomStatus(Enum):
    CHECKED_IN = 'CHECKED_IN'
    CHECKED_OUT = 'CHECKED_OUT'
    CLEANED = 'CLEANED'