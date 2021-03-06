# from connect4Game import Game
from connect4Game2 import Game
import numpy as np
import random


class RandomPolicy:
    def __init__(d, game):
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
            utility = d.game.utility(state) - (-player[0]) * depth
            # if depth == 0 or depth == 1 or depth == 2:
                # print("End, depth {}, utility is {}".format(depth, utility))

            return (utility, None)

        actionList = d.game.actions(state)
        # print("Player is {}".format(player))
        # print(actionList)

        candidates = []
        for action in actionList:
            # print(action)

            # state now becomes Successor state
            d.game.succ(state, action)
            candidate = (d.recursion(state, depth + 1)[0], action)
            candidates.append(candidate)

            # getting back the original state
            d.game.prec(state, action)
            # if depth == 0 or depth == 1:
                # print("player {}, depth {}, utility is {}".
                      # format(player, depth, candidate))

        if player[0] == 1:
            ans = max(candidates)
        elif player[0] == -1:
            ans = min(candidates)

        # if depth == 0:
        #     print("player is {} , utility, action {}".format(player, ans))

        return ans

    def getAction(d, state):
        player, board = state

        # print("Player is {}".format(player))
        # succP, succB = d.game.succ(s, d.game.actions(s)[0])
        # print("succ player is {}".format(succP))

        utility, action = d.recursion(state, 0)
        # print("utility is {}, action is {}".format(utility, action))
        return action


class MiniMaxRandom:
    def __init__(d, game):
        d.game = game
        d.randomPolicy = RandomPolicy(game) 
        d.minMaxPolicy = MiniMaxRaw(game)

    def findFilledDisks(d, board):
        nRows, nCols = np.shape(board)
        count = 0
        for row in range(nRows):
            for col in range(nCols):
                if board[row][col] != 0:
                    count = count + 1
        return count

    def getAction(d, state):
        player, board = state

        if d.findFilledDisks(board) < 3:
            return d.randomPolicy.getAction(state)
        return d.minMaxPolicy.getAction(state)


def main():
    game = Game(4, 4)
    # AIPolicy = RandomPolicy(game)
    # minMaxPolicy = MiniMaxRaw(game)
    minMaxRandomPolicy = MiniMaxRandom(game)

    game.gameLoop((game, minMaxRandomPolicy))
    # game.gameLoop((game, minMaxPolicy))
    # game.gameLoop((minMaxPolicy, minMaxPolicy))
    # game.gameLoop((minMaxPolicy, game))
    # game.gameLoop((game, game))
    # game.gameLoop((game, AIPolicy))
    # game.gameLoop((AIPolicy, game))
    # game.gameLoop((AIPolicy, AIPolicy))


main()
