from dice import Dice
from player import Player
from board import GameBoard, Square
from game import Game

import items
import random
import dataset

def GeneratePlayers(n, init_lives = 5):
    players = []
    randomNames = random.sample(dataset.NAME_DATASET, n)

    for i in range(n):
        players.append(Player(
            id = i + 1,
            name = randomNames.pop(),
            lives = init_lives))

    return players

def GenerateSquares(n):
    squares = []
    for i in range(n):
        content = items.RandomItem(items.SquareContent)
        squares.append(Square(content))

    return squares
