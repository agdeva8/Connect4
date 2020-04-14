import numpy as np
import random
import sys


class RandomPolicy:
    def __init__(d, game):
        d.game = game

    def getAction(d, state):
        actionList = d.game.actions(state)
        action = random.choice(actionList)
        return action


class MiniMaxRaw:
    def __init__(d, game):
        d.game = game

    def recursion(d, state, depth):
        if d.game.isEnd(state):
            utility = d.game.utility(state) - (-state["player"]) * depth
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

        if state["player"] == 1:
            ans = max(candidates)
        elif state["player"] == -1:
            ans = min(candidates)

        # if depth == 0:
        #     print("player is {} , utility, action {}".format(player, ans))
        return ans

    def getAction(d, state):
        # print("Player is {}".format(player))
        # succP, succB = d.game.succ(s, d.game.actions(s)[0])
        # print("succ player is {}".format(succP))

        sys.stderr.write("AI Processing")
        utility, action = d.recursion(state, 0)
        sys.stderr.write("returning action {}".format(str(action)))
        # print("utility is {}, action is {}".format(utility, action))
        return action

# not a practical solution for big boards with nConnectivity = 4 or higher


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

        if d.findFilledDisks(board) < 5:
            return d.randomPolicy.getAction(state)
        return d.minMaxPolicy.getAction(state)
