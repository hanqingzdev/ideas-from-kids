from dice import Dice
from player import Player
from board import GameBoard, Square
from items import SquareContent
from game import Game
import factory

def printUsage():
    print("""
        q | quit: quite the game
        r | report: print out current game report
        h | help: print this help message
    """)

def safeStringInt(s):
    try:
        return int(s)
    except ValueError:
        return 0

def main():
    N_Player, N_Square = 5, 200

    print("====== Game set up...")

    d = Dice()
    print('...Test rolling a dice: {}'.format(d.Roll()))

    players = factory.GeneratePlayers(N_Player)
    for p in players:
        print('...' + p.StatusReport())

    b = GameBoard(factory.GenerateSquares(N_Square))
    print('...The game board: ' + str(b))

    g = Game(b, players, d)
    print("...Game roaster: " + str(g.roaster))
    print("====== Game set up complete!")

    print("====== The game STARTS!!!")
    
    while True:
        print()
        command = str(input(">>> Command or ENTER for next player: ")).lower()

        if command == '':
            print("====== Move on:")
            g.Next()
        elif safeStringInt(command) > 0:
            rounds = safeStringInt(command)
            print("====== Move on for {} rounds:".format(rounds))
            for i in range(rounds):
                if not g.winner:
                    print("------ round {}".format(i))
                    g.Next()
        elif command == 'quit' or command == 'q':
            break
        elif command == 'report' or command == 'r':
            print("====== Current game report:")
            g.Print()
        elif command == 'help' or command == 'h':
            print("====== Usage:")
            printUsage()



if __name__ == "__main__":
    main()
