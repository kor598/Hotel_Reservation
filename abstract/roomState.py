# state.py
from abc import ABC, abstractmethod

class RoomState(ABC):
    @abstractmethod
    def handle(self, room):
        pass

class CheckedOutState(RoomState):
    def handle(self, room):
        # Implement the behavior for the Checked Out state
        room.clean_status = 'checked_out'

class BeingCleanedState(RoomState):
    def handle(self, room):
        # Implement the behavior for the Being Cleaned state
        room.clean_status = 'being_cleaned'

class ReadyForCheckinState(RoomState):
    def handle(self, room):
        # Implement the behavior for the Ready for Check-in state
        room.clean_status = 'ready_for_checkin'

class CheckedinState(RoomState):
    def handle(self, room):
        # Implement the behavior for the Ready for Check-in state
        room.clean_status = 'ready_for_checkin'