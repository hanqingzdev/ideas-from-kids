import random

class Dice(object):
    def __init__(self):
        self.min = 1
        self.max = 6

    def Roll(self):
        return random.randint(self.min, self.max)
