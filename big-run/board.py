from player import Player
from items import SquareContent

class Square(object):
    content: SquareContent

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return str(self.content)

class GameBoard(object):
    def __init__(self, square_seq):
        self.world = square_seq
        self.size = len(square_seq)

    def __str__(self):
        world_str = [str(s) for s in self.world]
        return '[' + '->'.join(world_str) + ']'

    def StepForwardTo(self, start, step):
        # return the end position based on the start position and steps.
        # the second return value indicate if it looped from the start.
        far = start + step
        laps, position  = divmod(far, self.size)
        return (self.size - 1, True) if laps > 0 else (position, False)

    def ContentAt(self, position):
        return self.world[position].content
