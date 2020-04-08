import pygame
import sys
import numpy as np
# from pygame.locals import *
import pygame.locals
from itertools import product


class Game:
    def __init__(self, numRows=6, numCols=7):
        self.numRows = numRows
        self.numCols = numCols

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.YELLOW = (255,  255,  0)
        self.LGREY = (140, 140, 140)
        self.LLGREY = (153, 153, 153)

        self.bgColor = self.LLGREY
        self.displayWidth = 500
        self.displayHeight = 700
        self.startX = 50
        self.startY = 50
        self.lineWidth = 2
        self.numRows = 6
        self.numCols = 7
        self.lineColor = self.BLUE
        self.cellWidth = 50
        self.cellHeight = 50
        self.diskColor = [self.YELLOW,  self.RED]

        self.canUndo = True
        self.playerID = 0

        pygame.init()
        self.display = pygame.display.set_mode((
            self.displayWidth, self.displayHeight))

        self.font = pygame.font.Font('fonts/FreeSansBold.ttf', 32)

        self.endX = self.startX + self.numCols * self.cellWidth
        self.endY = self.startY + self.numRows * self.cellHeight

        self.xvals = np.arange(self.startX,
                               self.endX + self.cellWidth,  self.cellWidth)
        self.yvals = np.arange(self.startY,
                               self.endY + self.cellHeight,  self.cellHeight)

        self.boardConfig = [[-1]*self.numCols for _ in range(self.numRows)]

        self.diskRadius = int(self.cellWidth / 2) - 5

    def grid(self):
        # drawing vertical self.lines
        for xVal in self.xvals:
            pygame.draw.line(self.display, self.lineColor,
                             (xVal,  self.startY),
                             (xVal,  self.endY),  self.lineWidth)

            for yVal in self.yvals:
                # drawing horizontal self.lines
                pygame.draw.line(self.display, self.lineColor,
                                 (self.startX,  yVal),
                                 (self.endX,  yVal),  self.lineWidth)

            pygame.display.flip()

    def fillgrid(self):
        pygame.draw.rect(self.display, self.BLUE,
                         (self.startX,  self.startY,
                          self.cellWidth * self.numCols,
                          self.cellHeight * self.numRows),  0)

    def rowColFromXY(self, pos):
        x, y = pos
        col = (x - self.startX) / self.cellWidth
        row = (y - self.startY) / self.cellHeight
        return (row, col)

    def creatediskXY(self, x, y, radius, color):
        pygame.draw.circle(self.display, color,  (x,  y),  radius,  0)

    def centerFromRC(self, row, col):
        x = int((self.xvals[col] + self.xvals[col + 1]) / 2) + 1
        y = int((self.yvals[row] + self.yvals[row + 1]) / 2) + 1
        return (x, y)

    def createdisk(self, row,  col,  color):
        x, y = self.centerFromRC(row, col)
        self.creatediskXY(x, y, self.diskRadius, color)

    def changeTurn(self):
        if self.playerID == 0:
            self.playerID = 1
        else:
            self.playerID = 0

    def checkValidity(self, row,  col):
        # print(str(row) + " " + str(self.numRows) + " " +
        # str(col) + " " + str(self.numCols) + " ")
        if (row >= 0 and row < self.numRows) \
                and (col >= 0 and col < self.numCols):
            return True
        return False

    def isCheckMate(self):
        def markDots(row, col, ri, ci):
            for i in range(4):
                x, y = self.centerFromRC(row + i*ri, col + i*ci)
                self.creatediskXY(x, y, 5, self.BLACK)

        def markline(row, col, ri, ci):
            x, y = self.centerFromRC(row, col)
            x2, y2 = self.centerFromRC(row + 3*ri, col + 3*ci)
            pygame.draw.line(self.display, self.BLACK,
                             (x, y), (x2, y2), 2)

        for row, col in product(range(self.numRows), range(self.numCols)):
            if self.boardConfig[row][col] == -1:
                continue

            # for horizontal
            count = 0
            for i in range(4):
                if self.checkValidity(row + i, col):
                    if self.boardConfig[row][col] == \
                            self.boardConfig[row + i][col]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, 0)
                markline(row, col, 1, 0)
                return True

            # for vertical
            count = 0
            for i in range(4):
                if self.checkValidity(row, col + i):
                    if self.boardConfig[row][col] == \
                            self.boardConfig[row][col + i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 0, 1)
                markline(row, col, 0, 1)
                return True

            # for reverse diagonal
            count = 0
            for i in range(4):
                if self.checkValidity(row + i, col + i):
                    if self.boardConfig[row][col] == \
                            self.boardConfig[row + i][col + i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, 1)
                markline(row, col, 1, 1)
                return True

            # for diagonal
            count = 0
            for i in range(4):
                if self.checkValidity(row + i, col - i):
                    if self.boardConfig[row][col] == \
                            self.boardConfig[row + i][col - i]:
                        count = count + 1
            if count == 4:
                markDots(row, col, 1, -1)
                markline(row, col, 1, -1)
                return True
        return False

    def updateConfig(self, currConfig,  row,  col):
        lastMove = (-1, -1)

        if self.checkValidity(row,  col) is False:
            return (lastMove, False)

        if currConfig[col] == -1:
            return (lastMove, False)

        lastMove = (currConfig[col], col)

        self.createdisk(lastMove[0], lastMove[1],
                        self.diskColor[self.playerID])

        self.boardConfig[currConfig[col]][col] = self.playerID
        currConfig[col] = currConfig[col] - 1

        return (lastMove, True)

    def displayStatus(self, text):
        x = 260
        y = self.endY + 30
        width = 200
        height = 40

        statusFont = pygame.font.Font('fonts/FreeSansBold.ttf', 24)
        text = statusFont.render(text, True, self.BLACK, self.GREEN)

        textRect = text.get_rect()
        textRect.x = x + 10
        textRect.y = y + 10

        # pygame.draw.rect(self.display, self.BLACK, (x, y, width, height), 2)
        pygame.draw.rect(self.display, self.bgColor, (x, y, width, height), 0)
        pygame.display.update()
        self.display.blit(text, textRect)

        self.diskX = x + width - 30 - self.diskRadius
        self.diskY = textRect.centery
        self.creatediskXY(self.diskX, self.diskY,
                          self.diskRadius, self.diskColor[self.playerID])

    def undoButtonPos(self):
        x = 110
        y = self.endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def dispUndoButton(self):
        undoImg2 = pygame.image.load('icons/undo_48x48.jpg')
        x, y, width, height = self.undoButtonPos()
        self.display.blit(undoImg2, (x, y))
        # pygame.draw..rect(self.display, self.BLACK, (x, y, width, height), 2)

    def restrictUndoImg(self):
        pygame.draw.rect(self.display, self.RED, self.undoButtonPos(), 2)
        # self.dispUndoButton()

    def admitUndoImg(self):
        pygame.draw.rect(self.display, self.bgColor, self.undoButtonPos(), 2)
        # self.dispUndoButton()

    def isUndoPressed(self, pos):
        undoRec = pygame.Rect(self.undoButtonPos())
        if undoRec.collidepoint(pos):
            return True

    def takeUndoAction(self, currConfig, lastMove):
        if self.canUndo is False:
            return

        row, col = lastMove
        if self.checkValidity(row,  col) is False:
            return (lastMove, False)

        self.canUndo = False
        self.restrictUndoImg()

        self.createdisk(row, col, self.bgColor)

        self.boardConfig[row][col] = -1
        currConfig[col] = currConfig[col] + 1

        self.self.changeTurn()
        self.displayStatus("self.player")

    def resetButtonPos(self):
        x = 50
        y = self.endY + 30
        width = 48
        height = 48
        return (x, y, width, height)

    def dispResetButton(self):
        resetImg = pygame.image.load('icons/reset_48x48.jpg')
        x, y, width, height = self.resetButtonPos()
        self.display.blit(resetImg, (x, y))
        # pygame.draw..rect(self.display, self.BLACK, (x, y, width, height), 2)

    def isResetPressed(self, pos):
        resetRec = pygame.Rect(self.resetButtonPos())
        if resetRec.collidepoint(pos):
            return True

    def resetgrid(self, currConfig):
        self.playerID = 0

        self.display.fill(self.bgColor)

        # building self.grid
        self.grid()
        self.fillgrid()

        self.displayStatus("self.player")
        self.dispUndoButton()
        self.dispResetButton()

        # empty coins
        for row in range(0,  self.numRows):
            for col in range(0,  self.numCols):
                self.createdisk(row,  col, self.bgColor)

        # clear board and curr config
        for i in range(self.numCols):
            for j in range(self.numRows):
                currConfig[i] = self.numRows - 1
                self.boardConfig[j][i] = -1

    def showColSelected(self, row, col):
        x = 30
        y = self.startY - 40
        width = self.endX - self.startX + 40
        height = 30
        pygame.draw.rect(self.display, self.bgColor, (x, y, width, height), 0)

        if self.checkValidity(row, col) is False:
            return

        cx, cy = self.centerFromRC(row, col)
        pygame.draw.polygon(self.display, self.diskColor[self.playerID],
                            ((cx - 10, y + 10),
                            (cx + 10, y + 10), (cx, y + 25)))

    def winnerCelebration(self):
        image = pygame.image.load('icons/winner_400x300.jpg')

        x = 25
        y = self.endY + 80
        self.display.blit(image, (x, y))
        # pygame.draw.rect(self.display, self.BLACK, (x, y, width, height), 2)

    def main(self):
        currConfig = [self.numRows - 1]*self.numCols

        self.resetgrid(currConfig)
        # main loop to capture events
        d_isCheckMate = False

        lastMove = (-1, -1)
        while True:
            row, col = self.rowColFromXY(pygame.mouse.get_pos())
            if (self.checkValidity(row, col)):
                # print("hovered: row {}, col{}".format(row, col))
                self.showColSelected(row, col)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        if (self.isResetPressed(event.pos)):
                            self.resetgrid(currConfig)
                            d_isCheckMate = False
                            lastMove = (-1, -1)
                            continue

                        if d_isCheckMate:
                            continue

                        if (self.isUndoPressed(event.pos)):
                            self.takeUndoAction(currConfig, lastMove)
                            continue

                        rownum, colnum = self.rowColFromXY(event.pos)

                        lastMove, success = self.updateConfig(currConfig,
                                                              rownum,  colnum)
                        if success:
                            self.changeTurn()
                            self.displayStatus("self.player")
                            self.canUndo = True
                            self.admitUndoImg()

                            if self.isCheckMate():
                                d_isCheckMate = True
                                self.changeTurn()
                                self.displayStatus("WINNER")
                                self.winnerCelebration()

            pygame.display.update()


myGame = Game()
myGame.main()
