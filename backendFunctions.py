import numpy as np


class GameEnv: 
    def __init__(d):
        d.numRows = 6
        d.numCols = 7

        d.d_isCheckMate = False
        d.playerID = [1]
        d.board = np.zeros((d.numRows, d.numCols))

    def checkValidity(d, row,  col, state):
        player, board = state
        nRows, nCols = np.shape(board)
        if (row >= 0 and row < nRows) and (col >= 0 and col < nCols):
            return True
        return False

    def startState(d):
        return np.zeros((d.numRows, d.numCols))

    def state(d):
        return [d.playerID, d.board]

    def isValidAction(d, state, action):
        player, boardConfig = state
        if d.checkValidity(0, action, state) and boardConfig[0][action] == 0:
            return True
        return False

    def actions(d, state):
        player, board = state
        actionList = []
        nRows, nCols = np.shape(board)
        for col in range(nCols):
            if d.isValidAction(state, col):
                actionList.append(col)
        return actionList

    def succ(d, state, a):
        player, boardConfig = state

        # Assuming a is valid action
        for row in reversed(range(d.numRows)):
            if boardConfig[row][a] == 0:
                boardConfig[row][a] = player[0]
                break
        player[0] = -player[0]
        # print("before state[0] {}".format(state[0]))
        # state[0] = -state[0]
        # print("after state[0] {}".format(state[0]))

    def prec(d, state, action):
        player, board = state

        # Assuming a is valid action
        for row in range(d.numRows):
            if board[row][action] != 0:
                board[row][action] = 0
                break
        player[0] = -player[0]


    def isEnd(d, state):
        if d.isCheckMate(state, False) or d.isBoardFull(state):
            return True
        return False


    def isDraw(d, state):
        if d.isCheckMate(state, False):
            return False
        return d.isBoardFull(state)


    def utility(d, state):
        player, board = state
        # print("Player is {}".format(player))

        if d.isCheckMate(state, False):
            return -player[0] * 1000
        return 0
