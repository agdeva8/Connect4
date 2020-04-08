import pygame
import sys
import numpy as np
# from pygame.locals import *
import pygame.locals
from itertools import product


class Game:
    def __init__(self, numRows=6, numCols=7):
        self.____numRows = numRows
        self.__numCols = numCols

        self.__WHITE = (255, 255, 255)
        self.__BLACK = (0, 0, 0)
        self.__RED = (255, 0, 0)
        self.__GREEN = (0, 255, 0)
        self.__BLUE = (0, 0, 255)
        self.__YELLOW = (255,  255,  0)
        self.__LGREY = (140, 140, 140)
        self.__LLGREY = (153, 153, 153)

        self.__bgColor = self.__LLGREY
        self.__displayWidth = 500
        self.__displayHeight = 700
        self.__startX = 50
        self.__startY = 50
        self.__lineWidth = 2
        self.__numRows = 6
        self.__numCols = 7
        self.__lineColor = self.__BLUE
        self.__cellWidth = 50
        self.__cellHeight = 50
        self.__diskColor = [self.__YELLOW,  self.__RED]

        self.__canUndo = True
        self.__playerID = 0

        pygame.init()
        self.__display = pygame.display.set_mode((
            self.__displayWidth, self.__displayHeight))

        self.__font = pygame.font.Font('fonts/FreeSansBold.ttf', 32)

        self.__endX = self.__startX + self.__numCols * self.__cellWidth
        self.__endY = self.__startY + self.__numRows * self.__cellHeight

        self.__xvals = np.arange(self.__startX,
                               self.__endX + self.__cellWidth,  self.__cellWidth)
        self.__yvals = np.arange(self.__startY,
                               self.__endY + self.__cellHeight,  self.__cellHeight)

        self.__boardConfig = [[-1]*self.__numCols for _ in range(self.__numRows)]

        self.__diskRadius = int(self.__cellWidth / 2) - 5

    def __grid(self):
        # drawing vertical self.__lines
        for xVal in self.__xvals:
            pygame.draw.line(self.__display, self.__lineColor,
                             (xVal,  self.__startY),
                             (xVal,  self.__endY),  self.__lineWidth)

            for yVal in self.__yvals:
                # drawing horizontal self.__lines
                pygame.draw.line(self.__display, self.__lineColor,
                                 (self.__startX,  yVal),
                                 (self.__endX,  yVal),  self.__lineWidth)

            pygame.display.flip()

    def __fillgrid(self):
        pygame.draw.rect(self.__display, self.__BLUE,
                         (self.__startX,  self.__startY,
                          self.__cellWidth * self.__numCols,
                          self.__cellHeight * self.__numRows),  0)

    def __rowColFromXY(self, pos):
        x, y = pos
        col = (x - self.__startX) / self.__cellWidth
        row = (y - self.__startY) / self.__cellHeight
        return (row, col)

    def __creatediskXY(self, x, y, radius, color):
        pygame.draw.circle(self.__display, color,  (x,  y),  radius,  0)

    def __centerFromRC(self, row, col):
        x = int((self.__xvals[col] + self.__xvals[col + 1]) / 2) + 1
        y = int((self.__yvals[row] + self.__yvals[row + 1]) / 2) + 1
        return (x, y)

    def __createdisk(self, row,  col,  color):
        x, y = self.__centerFromRC(row, col)
        self.__creatediskXY(x, y, self.__diskRadius, color)

    def __changeTurn(self):
        if self.__playerID == 0:
            self.__playerID = 1
        else:
            self.__playerID = 0

    def __checkValidity(self, row,  col):
        # print(str(row) + " " + str(self.__numRows) + " " +
        # str(col) + " " + str(self.__numCols) + " ")
        if (row >= 0 and row < self.__numRows) \
                and (col >= 0 and col < self.__numCols):
            return True
        return False

    def __isCheckMate(self):
        def markDots(row, col, ri, ci):
            for i in range(4):
                x, y = self.__centerFromRC(row + i*ri, col + i*ci)
                self.__creatediskXY(x, y, 5, self.__BLACK)

        def markline(row, col, ri, ci):
            x, y = self.__centerFromRC(row, col)
            x2, y2 = self.__centerFromRC(row + 3*ri, col + 3*ci)
            pygame.draw.line(self.__display, self.__BLACK,
                             (x, y), (x2, y2), 2)

        for row, col in product(range(self.__numRows), range(self.__numCols)):
            if self.__boardConfig[row][col] == -1:
                continue

            # for horizontal
            count = 0
            for i in range(4):
                if self.__checkValidity(row + i, col):
                    if self.__boardConfig[row][col] == \
                            self.__boardConfig[row + i][col]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, 0)
                markline(row, col, 1, 0)
                return True

            # for vertical
            count = 0
            for i in range(4):
                if self.__checkValidity(row, col + i):
                    if self.__boardConfig[row][col] == \
                            self.__boardConfig[row][col + i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 0, 1)
                markline(row, col, 0, 1)
                return True

            # for reverse diagonal
            count = 0
            for i in range(4):
                if self.__checkValidity(row + i, col + i):
                    if self.__boardConfig[row][col] == \
                            self.__boardConfig[row + i][col + i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, 1)
                markline(row, col, 1, 1)
                return True

            # for diagonal
            count = 0
            for i in range(4):
                if self.__checkValidity(row + i, col - i):
                    if self.__boardConfig[row][col] == \
                            self.__boardConfig[row + i][col - i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, -1)
                markline(row, col, 1, -1)
                return True
        return False

    def __updateConfig(self, currConfig,  row,  col):
        lastMove = (-1, -1)

        if self.__checkValidity(row,  col) is False:
            return (lastMove, False)

        if currConfig[col] == -1:
            return (lastMove, False)

        lastMove = (currConfig[col], col)

        self.__createdisk(lastMove[0], lastMove[1],
                        self.__diskColor[self.__playerID])

        self.__boardConfig[currConfig[col]][col] = self.__playerID
        currConfig[col] = currConfig[col] - 1

        return (lastMove, True)

    def __displayStatus(self, text):
        x = 260
        y = self.__endY + 30
        width = 200
        height = 40

        statusFont = pygame.font.Font('fonts/FreeSansBold.ttf', 24)
        text = statusFont.render(text, True, self.__BLACK, self.__GREEN)

        textRect = text.get_rect()
        textRect.x = x + 10
        textRect.y = y + 10

        # pygame.draw.rect(self.__display, self.__BLACK, (x, y, width, height), 2)
        pygame.draw.rect(self.__display, self.__bgColor, (x, y, width, height), 0)
        pygame.display.update()
        self.__display.blit(text, textRect)

        self.__diskX = x + width - 30 - self.__diskRadius
        self.__diskY = textRect.centery
        self.__creatediskXY(self.__diskX, self.__diskY,
                          self.__diskRadius, self.__diskColor[self.__playerID])

    def __undoButtonPos(self):
        x = 110
        y = self.__endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def __dispUndoButton(self):
        undoImg2 = pygame.image.load('icons/undo_48x48.jpg')
        x, y, width, height = self.__undoButtonPos()
        self.__display.blit(undoImg2, (x, y))
        # pygame.draw..rect(self.__display, self.__BLACK, (x, y, width, height), 2)

    def __restrictUndoImg(self):
        pygame.draw.rect(self.__display, self.__RED, self.__undoButtonPos(), 2)
        # self.__dispUndoButton()

    def __admitUndoImg(self):
        pygame.draw.rect(self.__display, self.__bgColor, self.__undoButtonPos(), 2)
        # self.__dispUndoButton()

    def __isUndoPressed(self, pos):
        undoRec = pygame.Rect(self.__undoButtonPos())
        if undoRec.collidepoint(pos):
            return True

    def __takeUndoAction(self, currConfig, lastMove):
        if self.__canUndo is False:
            return

        row, col = lastMove
        if self.__checkValidity(row,  col) is False:
            return (lastMove, False)

        self.__canUndo = False
        self.__restrictUndoImg()

        self.__createdisk(row, col, self.__bgColor)

        self.__boardConfig[row][col] = -1
        currConfig[col] = currConfig[col] + 1

        self.__self.__changeTurn()
        self.__displayStatus("self.__player")

    def __resetButtonPos(self):
        x = 50
        y = self.__endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def __dispResetButton(self):
        resetImg = pygame.image.load('icons/reset_48x48.jpg')
        x, y, width, height = self.__resetButtonPos()
        self.__display.blit(resetImg, (x, y))
        # pygame.draw..rect(self.__display, self.__BLACK, (x, y, width, height), 2)

    def __isResetPressed(self, pos):
        resetRec = pygame.Rect(self.__resetButtonPos())
        if resetRec.collidepoint(pos):
            return True

    def __resetgrid(self, currConfig):
        self.__playerID = 0

        self.__display.fill(self.__bgColor)

        # building self.__grid
        self.__grid()
        self.__fillgrid()

        self.__displayStatus("self.__player")
        self.__dispUndoButton()
        self.__dispResetButton()

        # empty coins
        for row in range(0,  self.__numRows):
            for col in range(0,  self.__numCols):
                self.__createdisk(row,  col, self.__bgColor)

        # clear board and curr config
        for i in range(self.__numCols):
            for j in range(self.__numRows):
                currConfig[i] = self.__numRows - 1
                self.__boardConfig[j][i] = -1

    def __showColSelected(self, row, col):
        x = 30
        y = self.__startY - 40
        width = self.__endX - self.__startX + 40
        height = 30
        pygame.draw.rect(self.__display, self.__bgColor, (x, y, width, height), 0)

        if self.__checkValidity(row, col) is False:
            return

        cx, cy = self.__centerFromRC(row, col)
        pygame.draw.polygon(self.__display, self.__diskColor[self.__playerID],
                            ((cx - 10, y + 10),
                            (cx + 10, y + 10), (cx, y + 25)))

    def __winnerCelebration(self):
        image = pygame.image.load('icons/winner_400x300.jpg')

        x = 25
        y = self.__endY + 80
        self.__display.blit(image, (x, y))
        # pygame.draw.rect(self.__display, self.__BLACK, (x, y, width, height), 2)

    def main(self):
        currConfig = [self.__numRows - 1]*self.__numCols

        self.__resetgrid(currConfig)
        # main loop to capture events
        d_isCheckMate = False

        lastMove = (-1, -1)
        while True:
            row, col = self.__rowColFromXY(pygame.mouse.get_pos())
            if (self.__checkValidity(row, col)):
                # print("hovered: row {}, col{}".format(row, col))
                self.__showColSelected(row, col)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if (self.__isResetPressed(event.pos)):
                            self.__resetgrid(currConfig)
                            d_isCheckMate = False
                            lastMove = (-1, -1)
                            continue

                        if d_isCheckMate:
                            continue

                        if (self.__isUndoPressed(event.pos)):
                            self.__takeUndoAction(currConfig, lastMove)
                            continue

                        rownum, colnum = self.__rowColFromXY(event.pos)

                        lastMove, success = self.__updateConfig(currConfig,
                                                              rownum,  colnum)
                        if success:
                            self.__changeTurn()
                            self.__displayStatus("self.__player")
                            self.__canUndo = True
                            self.__admitUndoImg()

                            if self.__isCheckMate():
                                d_isCheckMate = True
                                self.__changeTurn()
                                self.__displayStatus("WINNER")
                                self.__winnerCelebration()

            pygame.display.update()


myGame = Game()
myGame.main()
