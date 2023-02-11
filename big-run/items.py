from enum import Enum
import random

class SquareContent(str, Enum):
    NOTHING = 'Nothing'
    X = 'X'
    WATER = 'Water'
    FOOD = 'Food'

    def __str__(self):
        return self.value


def RandomItem(item_type):
    return random.choice(list(item_type))
