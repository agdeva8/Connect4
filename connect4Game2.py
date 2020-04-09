import pygame
import sys
import numpy as np
# from pygame.locals import *
import pygame.locals
from itertools import product

# we will be using d insted of self


class Game:
    def __init__(d, numRows=6, numCols=7):
        d.numRows = numRows
        d.numCols = numCols

        d.WHITE = (255, 255, 255)
        d.BLACK = (0, 0, 0)
        d.RED = (255, 0, 0)
        d.GREEN = (0, 255, 0)
        d.BLUE = (0, 0, 255)
        d.YELLOW = (255,  255,  0)
        d.LGREY = (140, 140, 140)
        d.LLGREY = (153, 153, 153)

        d.bgColor = d.LLGREY
        d.displayWidth = 500
        d.displayHeight = 700
        d.startX = 50
        d.startY = 50
        d.lineWidth = 2
        d.lineColor = d.BLUE
        d.cellWidth = 50
        d.cellHeight = 50
        # d.diskColor = [d.YELLOW,  d.RED]
        d.diskColor = {
            +1: d.YELLOW,
            -1: d.RED,
        }

        d.canUndo = True
        d.d_isCheckMate = False
        d.lastmove = [-1, -1]
        d.playerID = 1

        pygame.init()
        d.display = pygame.display.set_mode((
            d.displayWidth, d.displayHeight))

        d.font = pygame.font.Font('fonts/FreeSansBold.ttf', 32)

        d.endX = d.startX + d.numCols * d.cellWidth
        d.endY = d.startY + d.numRows * d.cellHeight

        d.xvals = np.arange(d.startX, d.endX + d.cellWidth,  d.cellWidth)
        d.yvals = np.arange(d.startY, d.endY + d.cellHeight,  d.cellHeight)

        d.boardConfig = np.zeros((d.numRows, d.numCols))
        d.diskRadius = int(d.cellWidth / 2) - 5

    def grid(d):
        # drawing vertical d.lines
        for xVal in d.xvals:
            pygame.draw.line(d.display, d.lineColor, (xVal,  d.startY), (xVal,  d.endY),  d.lineWidth)

            for yVal in d.yvals:
                # drawing horizontal d.lines
                pygame.draw.line(d.display, d.lineColor,
                                 (d.startX,  yVal),
                                 (d.endX,  yVal),  d.lineWidth)

                pygame.display.flip()

    def fillgrid(d):
        pygame.draw.rect(d.display, d.BLUE,
                (d.startX,  d.startY,
                    d.cellWidth * d.numCols,
                    d.cellHeight * d.numRows),  0)

    def rowColFromXY(d, pos):
        x, y = pos
        col = (x - d.startX) / d.cellWidth
        row = (y - d.startY) / d.cellHeight
        return (row, col)

    def creatediskXY(d, x, y, radius, color):
        pygame.draw.circle(d.display, color,  (x,  y),  radius,  0)

    def centerFromRC(d, row, col):
        x = int((d.xvals[col] + d.xvals[col + 1]) / 2) + 1
        y = int((d.yvals[row] + d.yvals[row + 1]) / 2) + 1
        return (x, y)

    def createdisk(d, row,  col,  color):
        x, y = d.centerFromRC(row, col)
        d.creatediskXY(x, y, d.diskRadius, color)

    def changeTurn(d):
        d.playerID = d.playerID * -1

    def performAction(d, state, action):
        player, boardConfig = state
        lastMove = (-1, -1)

        if d.isValidAction(state, action) is False:
            return (d.lastMove, False)

        for row in reversed(range(d.numRows)):
            if boardConfig[row][action] == 0:
                lastMove = (row, action)
                break

        d.createdisk(lastMove[0], lastMove[1], d.diskColor[d.playerID])
        d.boardConfig[lastMove[0], lastMove[1]] = player

        return lastMove, True

    def updateConfig(d, currConfig,  row,  col):
        lastMove = (-1, -1)

        if d.checkValidity(row,  col) is False:
            return (lastMove, False)

        if currConfig[col] == -1:
            return (lastMove, False)

        lastMove = (currConfig[col], col)

        d.createdisk(lastMove[0], lastMove[1], d.diskColor[d.playerID])

        d.boardConfig[currConfig[col]][col] = d.playerID
        currConfig[col] = currConfig[col] - 1

        return (lastMove, True)

    def displayStatus(d, text):
        x = 260
        y = d.endY + 30
        width = 200
        height = 50

        statusFont = pygame.font.Font('fonts/FreeSansBold.ttf', 24)
        text = statusFont.render(text, True, d.BLACK, d.GREEN)

        textRect = text.get_rect()
        textRect.x = x + 10
        textRect.y = y + 10

        # pygame.draw.rect(d.display, d.BLACK, (x, y, width, height), 2)
        pygame.draw.rect(d.display, d.bgColor, (x, y, width, height), 0)
        pygame.display.update()
        d.display.blit(text, textRect)

        d.diskX = x + width - 30 - d.diskRadius
        d.diskY = textRect.centery
        d.creatediskXY(d.diskX, d.diskY, d.diskRadius, d.diskColor[d.playerID])

    def undoButtonPos(d):
        x = 110
        y = d.endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def dispUndoButton(d):
        undoImg2 = pygame.image.load('icons/undo_48x48.jpg')
        x, y, width, height = d.undoButtonPos()
        d.display.blit(undoImg2, (x, y))
        # pygame.draw..rect(d.display, d.BLACK, (x, y, width, height), 2)

    def restrictUndoImg(d):
        pygame.draw.rect(d.display, d.RED, d.undoButtonPos(), 2)
        # d.dispUndoButton()

    def admitUndoImg(d):
        pygame.draw.rect(d.display, d.bgColor, d.undoButtonPos(), 2)
        # d.dispUndoButton()

    def isUndoPressed(d, pos):
        undoRec = pygame.Rect(d.undoButtonPos())
        if undoRec.collidepoint(pos):
            return True

    def takeUndoAction(d, s):
        player, boardConfig = s
        # print("Take Undo: Last move is {} , {}".format(lastMove[0], lastMove[1]))

        if d.canUndo is False:
            return

        row, col = d.lastMove
        if d.checkValidity(row,  col, d.state()) is False:
            return (d.lastMove, False)

        d.canUndo = False
        d.restrictUndoImg()

        # print("creating empty disk")
        d.createdisk(row, col, d.bgColor)

        d.boardConfig[row][col] = 0

        d.changeTurn()
        d.displayStatus("PLAYER")

    def resetButtonPos(d):
        x = 50
        y = d.endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def dispResetButton(d):
        resetImg = pygame.image.load('icons/reset_48x48.jpg')
        x, y, width, height = d.resetButtonPos()
        d.display.blit(resetImg, (x, y))
        # pygame.draw..rect(d.display, d.BLACK, (x, y, width, height), 2)

    def isResetPressed(d, pos):
        resetRec = pygame.Rect(d.resetButtonPos())
        if resetRec.collidepoint(pos):
            return True

    def showColSelected(d, row, col):
        x = 30
        y = d.startY - 40
        width = d.endX - d.startX + 40
        height = 30
        pygame.draw.rect(d.display, d.bgColor, (x, y, width, height), 0)

        if d.checkValidity(row, col, d.state()) is False:
            return

        cx, cy = d.centerFromRC(row, col)
        pygame.draw.polygon(d.display, d.diskColor[d.playerID], ((cx - 10, y + 10), (cx + 10, y + 10), (cx, y + 25)))

    def winnerCelebration(d):
        image = pygame.image.load('icons/winner_400x300.jpg')

        x = 25
        y = d.endY + 80
        d.display.blit(image, (x, y))
        # pygame.draw.rect(d.display, d.BLACK, (x, y, width, height), 2)

    def resetGrid(d):
        # print("reseting Grid")
        d.playerID = 1

        d.display.fill(d.bgColor)

        # building d.grid
        d.grid()
        d.fillgrid()

        # # print("# printing status")
        d.displayStatus("PLAYER")
        d.dispUndoButton()
        d.dispResetButton()

        d.d_isCheckMate = False
        d.lastMove = [-1, -1]
        # empty coins
        for row in range(0,  d.numRows):
            for col in range(0,  d.numCols):
                d.createdisk(row,  col, d.bgColor)

        # clear board and curr config
        for i in range(d.numCols):
            for j in range(d.numRows):
                d.boardConfig[j][i] = 0
        pygame.display.flip()

    def mapToIndex(d, i):
        if i == -1:
            return 1
        return 0

    def gameLoop(d, playerPolicies):
        # mapping from -1, 1 to 1, 0 for indexing:
        policy = playerPolicies[d.mapToIndex(d.playerID)]

        d.resetGrid()
        # main loop to capture events

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # print("mouse button pressed")
                        if (d.isResetPressed(event.pos)):
                            d.resetGrid()
                            continue

            # # print("checking for checkmate")
            if d.d_isCheckMate:
                continue
            # print("Player id {} , value is {}".format(d.playerID, d.mapToIndex(d.playerID)))
            # print("Policy is {}".format(policy))
            action = policy.getAction(d.state())
            # # print("action is {}".format(action))
            d.lastMove, success = d.performAction(d.state(), action)
            if success:
                d.changeTurn()
                policy = playerPolicies[d.mapToIndex(d.playerID)]
                d.displayStatus("PLAYER")
                d.canUndo = True
                d.admitUndoImg()

                if d.isEnd(d.state()):
                    d.d_isCheckMate = True
                    d.changeTurn()
                    if (d.isCheckMate(d.state())):
                        d.displayStatus("WINNER")
                        d.winnerCelebration()
                    else:
                        d.displayStatus("DRAW")

            pygame.display.update()

# creating ENVIRONMENT for AI Agent (or u can say :-)
# defining all public definitions for AI Agent
# these can act as wrapper definitions to provide proper environment

    # this is for human policy
    def getAction(d, state):
        board, player = state
        # print("Getting Action from getAction")
        # Giving special powers of QUIT, Undo and Reset to Human Player
        while True:
            row, col = d.rowColFromXY(pygame.mouse.get_pos())
            if (d.checkValidity(row, col, d.state())):
                # # print("hovered: row {}, col{}".format(row, col))
                d.showColSelected(row, col)

            for event in pygame.event.get():
                # d.resetandquitroutine()
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # print("mouse button pressed")
                        if (d.isResetPressed(event.pos)):
                            d.resetGrid()
                            return -1

                        if d.d_isCheckMate:
                            return -1

                        if (d.isUndoPressed(event.pos)):
                            # print("Undo pressed")
                            d.takeUndoAction(d.state())
                            return -1

                        if d.isValidAction(d.state(), col):
                            return col

    def checkValidity(d, row,  col, state):
        player, board = state
        nRows, nCols = np.shape(board)
        if (row >= 0 and row < nRows) and (col >= 0 and col < nCols):
            return True
        return False

    def isBoardFull(d, state):
        player, board = state
        nRows, nCols = np.shape(board)

        for row in range(nRows):
            for col in range(nCols):
                if board[row][col] == 0:
                    return False
        return True

    def isCheckMate(d, state, d_markDots=False):
        def markDots(row, col, ri, ci):
            if d_markDots is False:
                return
            for i in range(3):
                x, y = d.centerFromRC(row + i*ri, col + i*ci)
                d.creatediskXY(x, y, 5, d.BLACK)

        def markline(row, col, ri, ci):
            if d_markDots is False:
                return
            x, y = d.centerFromRC(row, col)
            x2, y2 = d.centerFromRC(row + 2*ri, col + 2*ci)
            pygame.draw.line(d.display, d.BLACK, (x, y), (x2, y2), 2)

        player, board = state
        nRows, nCols = np.shape(board)

        for row, col in product(range(nRows), range(nCols)):
            if board[row][col] == 0:
                continue

            # for horizontal
            count = 0
            for i in range(3):
                if d.checkValidity(row + i, col, state):
                    # # print("valid for {} and {}".format(row + i, col))
                    if board[row][col] == board[row + i][col]:
                        count = count + 1

            if count == 3:
                markDots(row, col, 1, 0)
                markline(row, col, 1, 0)
                return True

            # for vertical
            count = 0
            for i in range(3):
                if d.checkValidity(row, col + i, state):
                    if board[row][col] == board[row][col + i]:
                        count = count + 1
            if count == 3:
                markDots(row, col, 0, 1)
                markline(row, col, 0, 1)
                return True

            # for reverse diagonal
            count = 0
            for i in range(3):
                if d.checkValidity(row + i, col + i, state):
                    if board[row][col] == board[row + i][col + i]:
                        count = count + 1
            if count == 3:
                markDots(row, col, 1, 1)
                markline(row, col, 1, 1)
                return True

            # for diagonal
            count = 0
            for i in range(3):
                if d.checkValidity(row + i, col - i, state):
                    if board[row][col] == board[row + i][col - i]:
                        count = count + 1
            if count == 3:
                markDots(row, col, 1, -1)
                markline(row, col, 1, -1)
                return True
        return False

    def startState(d):
        return np.zeros((d.numRows, d.numCols))

    def state(d):
        return (d.playerID, d.boardConfig)

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
                boardConfig[row][a] = player
                break
        return -player, boardConfig

    def prec(d, state, action):
        player, board = state

        # Assuming a is valid action
        for row in range(d.numRows):
            if board[row][action] != 0:
                board[row][action] = 0
                break
        return -player, board
    
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
            return -player * 100
        return 0
