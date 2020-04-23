from itertools import product
import numpy as np
import sys


class GameEnv:
    def __init__(d):
        d.nConnect = 4
        pass

    def isBoardFull(d, state):
        nRows, nCols = np.shape(state["board"])

        for row in range(state["nRows"]):
            for col in range(state["nCols"]):
                if state["board"][row][col] == 0:
                    return False
        return True

    def isCheckMate(d, state):

        ijPattern = [
            [1, 0],
            [0, 1],
            [1, 1],
            [1, -1]
        ]
        for i in range(4):
            for row, col in product(range(state["nRows"]), range(state["nCols"])):
                if state["board"][row][col] == 0:
                    continue
                count = 0

                for j in range(d.nConnect):
                    cRow = row + ijPattern[i][0] * j
                    cCol = col + ijPattern[i][1] * j
                    if d.checkValidity(cRow, cCol, state) is False:
                        continue

                    if state["board"][row][col] == state["board"][cRow][cCol]:
                        count = count + 1

                    if count == d.nConnect:
                        return True

        return False

    def checkValidity(d, row,  col, state):
        if (row >= 0 and row < state["nRows"]) and (col >= 0 and col < state["nCols"]):
            return True
        return False

    # def startState(d):
    #     return np.zeros((d.numRows, d.numCols))

    # def state(d):
    #     return [d.playerID, d.board]

    def isValidAction(d, state, action):
        if d.checkValidity(0, action, state) and state["board"][0][action] == 0:
            return True
        return False

    def actions(d, state):
        actionList = []
        for col in range(state["nCols"]):
            if d.isValidAction(state, col):
                actionList.append(col)
        return actionList

    def succ(d, state, action):
        # Assuming a is valid action
        for row in reversed(range(state["nRows"])):
            if state["board"][row][action] == 0:
                state["board"][row][action] = state["player"]
                break

        state["player"] = -state["player"]
    # print("before state[0] {}".format(state[0]))
    # state[0] = -state[0]
    # print("after state[0] {}".format(state[0]))

    def prec(d, state, action):
        # Assuming a is valid action
        for row in range(state["nRows"]):
            if state["board"][row][action] != 0:
                state["board"][row][action] = 0
                break

        state["player"] = -state["player"]

    def isEnd(d, state):
        if d.isCheckMate(state) or d.isBoardFull(state):
            return True
        return False

    def isDraw(d, state):
        if d.isCheckMate(state):
            return False
        return d.isBoardFull(state)

    def utility(d, state):
        # print("Player is {}".format(player))
        if d.isCheckMate(state):
            return -state["player"] * 1000
        return 0

    def state2List(d, state):
        # stateList = [state["player"]]
        # stateList.extend(d.board2List(state["board"]))
        # stateList = d.board2List(state["board"])
        # return np.array(stateList)
        return np.array(state["board"])

    def board2List(d, board):
        board = np.array(board)
        # sys.stderr.write('\n')
        # sys.stderr.write(str(board))
        # sys.stderr.write('\n')
        boardList = board.flatten()
        boardList2 = list(boardList == 0)*1
        boardList2.extend(list(boardList == 1)*1)
        boardList2.extend(list(boardList == -1)*1)
        return boardList2
