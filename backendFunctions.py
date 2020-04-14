import numpy as np

class GameEnv:
    def __init__(d):
        pass

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
        for row in range(d.numRows):
            if state["board"][row][action] != 0:
                state["board"][row][action] = 0
                break
        state["player"] = -state["player"]

    def isEnd(d, state):
        if d.isCheckMate(state, False) or d.isBoardFull(state):
            return True
        return False

    def isDraw(d, state):
        if d.isCheckMate(state, False):
            return False
        return d.isBoardFull(state)

    def utility(d, state):
        # print("Player is {}".format(player))

        if d.isCheckMate(state, False):
            return -state["player"] * 1000
        return 0
