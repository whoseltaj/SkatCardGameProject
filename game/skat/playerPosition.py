from enum import Enum


class PlayerPosition(Enum):
    FOREHAND = 1
    MIDDLEHAND = 2
    REARHAND = 3

    @property
    def next_player(self):
        if self == PlayerPosition.FOREHAND:
            return PlayerPosition.MIDDLEHAND
        elif self == PlayerPosition.MIDDLEHAND:
            return PlayerPosition.REARHAND
        else:
            return PlayerPosition.FOREHAND
