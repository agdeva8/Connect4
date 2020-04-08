import pygame
import sys
import numpy as np
# from pygame.locals import *
import pygame.locals
from itertools import product

# we will be using d insted of d


class Game:
    def __init__(d, numRows=6, numCols=7):
        d.__numRows = numRows
        d.__numCols = numCols

        d.__WHITE = (255, 255, 255)
        d.__BLACK = (0, 0, 0)
        d.__RED = (255, 0, 0)
        d.__GREEN = (0, 255, 0)
        d.__BLUE = (0, 0, 255)
        d.__YELLOW = (255,  255,  0)
        d.__LGREY = (140, 140, 140)
        d.__LLGREY = (153, 153, 153)

        d.__bgColor = d.__LLGREY
        d.__displayWidth = 500
        d.__displayHeight = 700
        d.__startX = 50
        d.__startY = 50
        d.__lineWidth = 2
        d.__numRows = 6
        d.__numCols = 7
        d.__lineColor = d.__BLUE
        d.__cellWidth = 50
        d.__cellHeight = 50
        d.__diskColor = [d.__YELLOW,  d.__RED]

        d.__canUndo = True
        d.__playerID = 0

        pygame.init()
        d.__display = pygame.display.set_mode((
            d.__displayWidth, d.__displayHeight))

        d.__font = pygame.font.Font('fonts/FreeSansBold.ttf', 32)

        d.__endX = d.__startX + d.__numCols * d.__cellWidth
        d.__endY = d.__startY + d.__numRows * d.__cellHeight

        d.__xvals = np.arange(d.__startX,
                               d.__endX + d.__cellWidth,  d.__cellWidth)
        d.__yvals = np.arange(d.__startY,
                               d.__endY + d.__cellHeight,  d.__cellHeight)

        d.__boardConfig = [[-1]*d.__numCols for _ in range(d.__numRows)]

        d.__diskRadius = int(d.__cellWidth / 2) - 5

    def __grid(d):
        # drawing vertical d.__lines
        for xVal in d.__xvals:
            pygame.draw.line(d.__display, d.__lineColor,
                             (xVal,  d.__startY),
                             (xVal,  d.__endY),  d.__lineWidth)

            for yVal in d.__yvals:
                # drawing horizontal d.__lines
                pygame.draw.line(d.__display, d.__lineColor,
                                 (d.__startX,  yVal),
                                 (d.__endX,  yVal),  d.__lineWidth)

            pygame.display.flip()

    def __fillgrid(d):
        pygame.draw.rect(d.__display, d.__BLUE,
                         (d.__startX,  d.__startY,
                          d.__cellWidth * d.__numCols,
                          d.__cellHeight * d.__numRows),  0)

    def __rowColFromXY(d, pos):
        x, y = pos
        col = (x - d.__startX) / d.__cellWidth
        row = (y - d.__startY) / d.__cellHeight
        return (row, col)

    def __creatediskXY(d, x, y, radius, color):
        pygame.draw.circle(d.__display, color,  (x,  y),  radius,  0)

    def __centerFromRC(d, row, col):
        x = int((d.__xvals[col] + d.__xvals[col + 1]) / 2) + 1
        y = int((d.__yvals[row] + d.__yvals[row + 1]) / 2) + 1
        return (x, y)

    def __createdisk(d, row,  col,  color):
        x, y = d.__centerFromRC(row, col)
        d.__creatediskXY(x, y, d.__diskRadius, color)

    def __changeTurn(d):
        if d.__playerID == 0:
            d.__playerID = 1
        else:
            d.__playerID = 0

    def __checkValidity(d, row,  col):
        # print(str(row) + " " + str(d.__numRows) + " " +
        # str(col) + " " + str(d.__numCols) + " ")
        if (row >= 0 and row < d.__numRows) \
                and (col >= 0 and col < d.__numCols):
            return True
        return False

    def __isCheckMate(d):
        def markDots(row, col, ri, ci):
            for i in range(4):
                x, y = d.__centerFromRC(row + i*ri, col + i*ci)
                d.__creatediskXY(x, y, 5, d.__BLACK)

        def markline(row, col, ri, ci):
            x, y = d.__centerFromRC(row, col)
            x2, y2 = d.__centerFromRC(row + 3*ri, col + 3*ci)
            pygame.draw.line(d.__display, d.__BLACK,
                             (x, y), (x2, y2), 2)

        for row, col in product(range(d.__numRows), range(d.__numCols)):
            if d.__boardConfig[row][col] == -1:
                continue

            # for horizontal
            count = 0
            for i in range(4):
                if d.__checkValidity(row + i, col):
                    if d.__boardConfig[row][col] == \
                            d.__boardConfig[row + i][col]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, 0)
                markline(row, col, 1, 0)
                return True

            # for vertical
            count = 0
            for i in range(4):
                if d.__checkValidity(row, col + i):
                    if d.__boardConfig[row][col] == \
                            d.__boardConfig[row][col + i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 0, 1)
                markline(row, col, 0, 1)
                return True

            # for reverse diagonal
            count = 0
            for i in range(4):
                if d.__checkValidity(row + i, col + i):
                    if d.__boardConfig[row][col] == \
                            d.__boardConfig[row + i][col + i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, 1)
                markline(row, col, 1, 1)
                return True

            # for diagonal
            count = 0
            for i in range(4):
                if d.__checkValidity(row + i, col - i):
                    if d.__boardConfig[row][col] == \
                            d.__boardConfig[row + i][col - i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, -1)
                markline(row, col, 1, -1)
                return True
        return False

    def __updateConfig(d, currConfig,  row,  col):
        lastMove = (-1, -1)

        if d.__checkValidity(row,  col) is False:
            return (lastMove, False)

        if currConfig[col] == -1:
            return (lastMove, False)

        lastMove = (currConfig[col], col)

        d.__createdisk(lastMove[0], lastMove[1],
                        d.__diskColor[d.__playerID])

        d.__boardConfig[currConfig[col]][col] = d.__playerID
        currConfig[col] = currConfig[col] - 1

        return (lastMove, True)

    def __displayStatus(d, text):
        x = 260
        y = d.__endY + 30
        width = 200
        height = 40

        statusFont = pygame.font.Font('fonts/FreeSansBold.ttf', 24)
        text = statusFont.render(text, True, d.__BLACK, d.__GREEN)

        textRect = text.get_rect()
        textRect.x = x + 10
        textRect.y = y + 10

        # pygame.draw.rect(d.__display, d.__BLACK, (x, y, width, height), 2)
        pygame.draw.rect(d.__display, d.__bgColor, (x, y, width, height), 0)
        pygame.display.update()
        d.__display.blit(text, textRect)

        d.__diskX = x + width - 30 - d.__diskRadius
        d.__diskY = textRect.centery
        d.__creatediskXY(d.__diskX, d.__diskY,
                          d.__diskRadius, d.__diskColor[d.__playerID])

    def __undoButtonPos(d):
        x = 110
        y = d.__endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def __dispUndoButton(d):
        undoImg2 = pygame.image.load('icons/undo_48x48.jpg')
        x, y, width, height = d.__undoButtonPos()
        d.__display.blit(undoImg2, (x, y))
        # pygame.draw..rect(d.__display, d.__BLACK, (x, y, width, height), 2)

    def __restrictUndoImg(d):
        pygame.draw.rect(d.__display, d.__RED, d.__undoButtonPos(), 2)
        # d.__dispUndoButton()

    def __admitUndoImg(d):
        pygame.draw.rect(d.__display, d.__bgColor, d.__undoButtonPos(), 2)
        # d.__dispUndoButton()

    def __isUndoPressed(d, pos):
        undoRec = pygame.Rect(d.__undoButtonPos())
        if undoRec.collidepoint(pos):
            return True

    def __takeUndoAction(d, currConfig, lastMove):
        if d.__canUndo is False:
            return

        row, col = lastMove
        if d.__checkValidity(row,  col) is False:
            return (lastMove, False)

        d.__canUndo = False
        d.__restrictUndoImg()

        d.__createdisk(row, col, d.__bgColor)

        d.__boardConfig[row][col] = -1
        currConfig[col] = currConfig[col] + 1

        d.__changeTurn()
        d.__displayStatus("PLAYER")

    def __resetButtonPos(d):
        x = 50
        y = d.__endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def __dispResetButton(d):
        resetImg = pygame.image.load('icons/reset_48x48.jpg')
        x, y, width, height = d.__resetButtonPos()
        d.__display.blit(resetImg, (x, y))
        # pygame.draw..rect(d.__display, d.__BLACK, (x, y, width, height), 2)

    def __isResetPressed(d, pos):
        resetRec = pygame.Rect(d.__resetButtonPos())
        if resetRec.collidepoint(pos):
            return True

    def __resetgrid(d, currConfig):
        d.__playerID = 0

        d.__display.fill(d.__bgColor)

        # building d.__grid
        d.__grid()
        d.__fillgrid()

        d.__displayStatus("PLAYER")
        d.__dispUndoButton()
        d.__dispResetButton()

        # empty coins
        for row in range(0,  d.__numRows):
            for col in range(0,  d.__numCols):
                d.__createdisk(row,  col, d.__bgColor)

        # clear board and curr config
        for i in range(d.__numCols):
            for j in range(d.__numRows):
                currConfig[i] = d.__numRows - 1
                d.__boardConfig[j][i] = -1

    def __showColSelected(d, row, col):
        x = 30
        y = d.__startY - 40
        width = d.__endX - d.__startX + 40
        height = 30
        pygame.draw.rect(d.__display, d.__bgColor, (x, y, width, height), 0)

        if d.__checkValidity(row, col) is False:
            return

        cx, cy = d.__centerFromRC(row, col)
        pygame.draw.polygon(d.__display, d.__diskColor[d.__playerID],
                            ((cx - 10, y + 10),
                            (cx + 10, y + 10), (cx, y + 25)))

    def __winnerCelebration(d):
        image = pygame.image.load('icons/winner_400x300.jpg')

        x = 25
        y = d.__endY + 80
        d.__display.blit(image, (x, y))
        # pygame.draw.rect(d.__display, d.__BLACK, (x, y, width, height), 2)

    def main(d):
        currConfig = [d.__numRows - 1]*d.__numCols

        d.__resetgrid(currConfig)
        # main loop to capture events
        d_isCheckMate = False

        lastMove = (-1, -1)
        while True:
            row, col = d.__rowColFromXY(pygame.mouse.get_pos())
            if (d.__checkValidity(row, col)):
                # print("hovered: row {}, col{}".format(row, col))
                d.__showColSelected(row, col)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if (d.__isResetPressed(event.pos)):
                            d.__resetgrid(currConfig)
                            d_isCheckMate = False
                            lastMove = (-1, -1)
                            continue

                        if d_isCheckMate:
                            continue

                        if (d.__isUndoPressed(event.pos)):
                            d.__takeUndoAction(currConfig, lastMove)
                            continue

                        rownum, colnum = d.__rowColFromXY(event.pos)

                        lastMove, success = d.__updateConfig(currConfig,
                                                              rownum,  colnum)
                        if success:
                            d.__changeTurn()
                            d.__displayStatus("PLAYER")
                            d.__canUndo = True
                            d.__admitUndoImg()

                            if d.__isCheckMate():
                                d_isCheckMate = True
                                d.__changeTurn()
                                d.__displayStatus("WINNER")
                                d.__winnerCelebration()

            pygame.display.update()


myGame = Game()
myGame.main()
