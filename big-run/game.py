from enum import Enum
from typing import Dict, List, Optional, Sequence, Set, Text, Union

from items import SquareContent
import dice
import player
import board

class PlayerChain(object):
    def __init__(self, this_player):
        self.this_player = this_player
        self.previous_player = None
        self.next_player = None

    def __str__(self):
        return str(self.this_player)

class Roaster(object):
    def __init__(self, players):
        startDumpPlayer = self._constractPlayerChains(players)

        self.next_player = startDumpPlayer.next_player
        self.dead_players = []

    def __str__(self):
        start = self.next_player
        current = start

        player_str_list = [str(start) + '*']
        while current.next_player != start:
            current = current.next_player
            player_str_list.append(str(current))

        return ' -> '.join(player_str_list)

    def _constractPlayerChains(self, players):
        startDumpPlayer = PlayerChain(None)
        currentPlayer = startDumpPlayer

        for p in players:
            new_player = PlayerChain(p)
            new_player.previous_player = currentPlayer
            currentPlayer.next_player = new_player

            currentPlayer = currentPlayer.next_player

        # close the loop
        currentPlayer.next_player = startDumpPlayer.next_player
        startDumpPlayer.next_player.previous_player = currentPlayer

        return startDumpPlayer

    def ActivePlayerDumps(self):
        start = self.next_player
        current = start

        player_dumps = [start.this_player.Dump()]
        while current.next_player != start:
            current = current.next_player
            player_dumps.append(current.this_player.Dump())

        return player_dumps

    def DeadPlayerDumps(self):
        player_dumps = []

        for p in self.dead_players:
            player_dumps.append(p.Dump())

        return player_dumps

    def RemovePlayer(self, player):
        self.dead_players.append(player)

        second_next_player_in_roaster = self.next_player.next_player

        current = self.next_player
        previous_player = current.previous_player
        next_player = current.next_player

        while current.this_player != player:
            current = current.next_player
            previous_player = current
            next_player = current.next_player

        current.previous_player.next_player = current.next_player
        current.next_player.previous_player = current.previous_player

        if current == self.next_player:
            self.next_player = second_next_player_in_roaster


    def PlayerNumber(self):
        start = self.next_player
        current = start
        count = 1

        while current.next_player != start:
            count += 1
            current = current.next_player

        return count


    def _pickNextPlayer(self):
        next_player = self.next_player
        self.next_player = next_player.next_player

        return next_player

class PlayerEvaluation(str, Enum):
    NORMAL = 'Normal'
    WIN = 'Win'
    DIED = 'Died'
    RESET = 'Reset'

    def __str__(self):
        return self.value

class Game(object):
    def __init__(self, board, players, dice):
        self.board = board
        self.players = players
        self.dice = dice

        self.roaster = Roaster(players)
        self.winner = None

    def Next(self):
        if self.winner: 
            print('!!! The game has ended. The winner is {} !!!'.format(self.winner))
            return

        player_chained = self.roaster._pickNextPlayer()
        player = player_chained.this_player
        print('...The next player is {}'.format(player))

        step = self.dice.Roll()
        print('...Rolling the dice: {}'.format(step))

        end_position, complete_loop = self.board.StepForwardTo(player.position, step)
        player.position = end_position
        content_stand_on = self.board.ContentAt(player.position)

        self._takeEffect(player, content_stand_on)
        player.TakeEffect(content_stand_on)

        evaluation = self._evaluatePlayer(player, content_stand_on, complete_loop)

        print('...{} moved to position {}. It is a {}'.format(
            player.name, player.position, content_stand_on))

        if evaluation == PlayerEvaluation.RESET:
            print('...{} RESET to position {}'.format(player.name, player.position))
        elif evaluation == PlayerEvaluation.DIED:
            print('...{} DIED'.format(player.name))
        elif evaluation == PlayerEvaluation.WIN:
            self.winner = player
            print('...{} WON'.format(player.name))
            return

        if self.roaster.PlayerNumber() == 1:
            self.winner = self.roaster.next_player
            print('...{} WON! He/she is the only one standing!'.format(self.winner))

    def _takeEffect(self, player, content_stand_on):
        if content_stand_on == SquareContent.X:
            player.position = 0

    def _evaluatePlayer(self, player, stand_on, complete_loop):
        if complete_loop and player.lives > 0:
            return PlayerEvaluation.WIN
        elif player.lives <= 0:
            self.roaster.RemovePlayer(player)
            return PlayerEvaluation.DIED

        return PlayerEvaluation.NORMAL
        
    def Print(self):
        print('...The game board: ' + str(self.board))
        print("...Game roaster: " + str(self.roaster))

        print("...Alive player status: ")
        for line in self.roaster.ActivePlayerDumps():
            print('......' + line)

        print("...Dead player status: ")
        for line in self.roaster.DeadPlayerDumps():
            print('......' + line)
