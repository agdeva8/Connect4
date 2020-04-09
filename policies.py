# from connect4Game import Game
from connect4Game2 import Game
import random
import copy
import numpy as np


class RandomPolicy:
    def init(d, game):
        d.game = game

    def getAction(d, s):
        # print("in policy get action of Ai")
        while True:
            actionList = d.game.actions(d.game.state())
            action = random.choice(actionList)
            return action


class MiniMaxRaw:
    def __init__(d, game):
        d.game = game

    def recursion(d, state, depth):
        player, board = state
        if d.game.isEnd(state):
            print("utility is {}".format(d.game.utility(state) - player*depth))
            return (d.game.utility(state) - player*depth, None)

        actionList = d.game.actions(state)
        # print("Player is {}".format(player))
        # print(actionList)

        candidates = []
        for action in actionList:
            # print(action)
            succState = d.game.succ(state, action)
            candidates.append((d.recursion(succState, depth + 1)[0], action))
            d.game.prec(state, action)

        if player == 1:
            return max(candidates)
        elif player == -1:
            return min(candidates)

    def getAction(d, state):
        player, board = state

        # print("Player is {}".format(player))
        # succP, succB = d.game.succ(s, d.game.actions(s)[0])
        # print("succ player is {}".format(succP))

        utility, action = d.recursion(state, 0)
        print("utility is {}, action is {}".format(utility, action))
        return action


def main():
    game = Game(3, 4)
    # AIPolicy = RandomPolicy(game)
    minMaxPolicy = MiniMaxRaw(game)
    # game.gameLoop((game, minMaxPolicy))
    game.gameLoop((minMaxPolicy, game))
    # game.gameLoop((game, AIPolicy))
    # game.gameLoop((AIPolicy, game))
    # game.gameLoop((AIPolicy, AIPolicy))


main()
