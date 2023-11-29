# With Enum
from enum import Enum

class RoomStatus(Enum):
    CHECKED_IN = 'checked_in'
    CHECKED_OUT = 'checked_out'
    CLEANED = 'cleaned'