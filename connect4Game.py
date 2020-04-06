import pygame
import sys
import numpy as np
from pygame.locals import *
from itertools import product 

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,  255,  0)

displayWidth = 500;     displayHeight = 700
startX = 50; startY = 50
lineWidth = 2
numRows = 6
numCols = 7
lineColor = BLUE
cellWidth = 50
cellHeight = 50

canUndo = True
playerID = 0

pygame.init()
DISPLAY = pygame.display.set_mode((displayWidth, displayHeight))

font = pygame.font.Font('freesansbold.ttf', 32)

endX = startX + numCols * cellWidth
endY = startY + numRows * cellHeight

xvals = np.arange(startX,  endX + cellWidth,  cellWidth)
yvals = np.arange(startY,  endY + cellHeight,  cellHeight)

boardConfig = [ [-1]*numCols for _ in range(numRows)]

diskRadius = int(cellWidth / 2) - 5
def grid():
    # drawing vertical lines
    for xVal in xvals:
        pygame.draw.line(DISPLAY, lineColor,  (xVal,  startY),  (xVal,  endY),  lineWidth)
    
    for yVal in yvals:
    # drawing horizontal lines
        pygame.draw.line(DISPLAY, lineColor,  (startX,  yVal),  (endX,  yVal),  lineWidth)

    pygame.display.flip()
    
def fillGrid():
    pygame.draw.rect(DISPLAY, BLUE,  (startX,  startY,  cellWidth * numCols,  cellHeight * numRows),  0)

def createDiskXY(x, y, radius, color):
    pygame.draw.circle(DISPLAY, color,  (x,  y),  radius,  0) 

def createDisk(row,  col,  color):
    x = int((xvals[col] + xvals[col + 1]) / 2) + 1
    y = int((yvals[row] + yvals[row + 1]) / 2) + 1
    createDiskXY(x, y, diskRadius, color)

def changeTurn():
    global playerID
    if playerID == 0:
        playerID = 1
    else:
        playerID = 0

def checkValidity(row,  col):
    # print(str(row) + " " + str(numRows) + " " + str(col) + " " + str(numCols) + " ") 
    if (row >= 0 and row < numRows) and (col >= 0 and col < numCols): 
        return True
    return False

def isCheckMate():
    for row, col in product(range(numRows), range(numCols)):
        if boardConfig[row][col] == -1:
            continue

        # for horizontal
        count = 0
        for i in range(4):
            if checkValidity(row + i, col):
                if boardConfig[row][col] == boardConfig[row + i][col]:
                    count = count + 1
        if count == 4:
            return True

        # for vertical
        count = 0
        for i in range(4):
            if checkValidity(row, col + i):
                if boardConfig[row][col] == boardConfig[row][col + i]:
                    count = count + 1
        if count == 4:
            return True

        # for reverse diagonal
        count = 0
        for i in range(4):
            if checkValidity(row + i, col + i):
                if boardConfig[row][col] == boardConfig[row + i][col + i]:
                    count = count + 1
        if count == 4:
            return True

        # for diagonal
        count = 0
        for i in range(4):
            if checkValidity(row + i, col - i):
                if boardConfig[row][col] == boardConfig[row + i][col - i]:
                    count = count + 1
        if count == 4:
            return True
    return False


def updateConfig(currConfig,  row,  col,   diskColor):
    lastMove = (-1, -1)

    if checkValidity(row,  col) is False: 
        return (lastMove, False)

    if currConfig[col] == -1:
        return (lastMove, False)

    lastMove = (currConfig[col], col)

    createDisk(lastMove[0], lastMove[1],  diskColor[playerID])

    boardConfig[currConfig[col]][col] = playerID
    currConfig[col] = currConfig[col] - 1
    
    return (lastMove, True)


def displayStatus(text, diskColor):
    x = 260
    y = endY + 30
    width = 200
    height = 40

    statusFont = pygame.font.Font('freesansbold.ttf', 24)
    text = statusFont.render(text, True, BLACK, GREEN) 

    textRect = text.get_rect()  
    textRect.x = x + 10
    textRect.y = y + 10
   
    # pygame.draw.rect(DISPLAY, BLACK, (x, y, width, height), 2)
    pygame.draw.rect(DISPLAY, WHITE, (x, y, width, height), 0)
    pygame.display.update()
    DISPLAY.blit(text, textRect) 
    
    diskX = x + width - 30 - diskRadius
    diskY = textRect.centery
    createDiskXY(diskX, diskY, diskRadius, diskColor[playerID]) 


def undoButtonPos():
    x = 50
    y = endY + 30
    width = 48
    height = 48
    return (x, y, width, height)


def dispUndoButton():
    undoImg2 = pygame.image.load('icons/undo_48x48.jpg')
    x, y, width, height = undoButtonPos()
    DISPLAY.blit(undoImg2, (x, y))
    # pygame.draw.rect(DISPLAY, BLACK, (x, y, width, height), 2)

def restrictUndoImg():
    pygame.draw.rect(DISPLAY, RED, undoButtonPos(), 2)
    # dispUndoButton()

def admitUndoImg():
    pygame.draw.rect(DISPLAY, WHITE, undoButtonPos(), 2)
    # dispUndoButton()

def isUndoPressed(pos):
    undoRec = pygame.Rect(undoButtonPos())
    if undoRec.collidepoint(pos):
        return True


def takeUndoAction(currConfig, lastMove, diskColor):
    global canUndo
    if canUndo is False:
        return 

    row, col = lastMove
    if checkValidity(row,  col) is False: 
        return (lastMove, False)

    canUndo = False
    restrictUndoImg()

    createDisk(row, col, WHITE)

    boardConfig[row][col] = -1
    currConfig[col] = currConfig[col] + 1

    changeTurn()
    displayStatus("PLAYER", diskColor)


def main():
    global canUndo

    DISPLAY.fill(WHITE)

    # building grid
    grid()
    fillGrid()

    for row in range(0,  numRows):
        for col in range(0,  numCols):
            createDisk(row,  col,  WHITE)

    currConfig = [numRows - 1]*numCols
    diskColor = [YELLOW,  RED]

    # main loop to capture events
    d_isCheckMate = False

    displayStatus("PLAYER", diskColor)
    dispUndoButton()

    lastMove = (-1, -1)
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            if d_isCheckMate:
                continue

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if (isUndoPressed(event.pos)):
                        takeUndoAction(currConfig, lastMove, diskColor)
                        continue

                    x = event.pos[0];                       y = event.pos[1]
                    colNum = (x - startX) / cellWidth;      rowNum = (y - startY) / cellHeight 

                    lastMove, success = updateConfig(currConfig,  rowNum,  colNum,   diskColor)
                    if success:
                        changeTurn()
                        displayStatus("PLAYER", diskColor)
                        canUndo = True
                        admitUndoImg()

                        if isCheckMate():
                            d_isCheckMate = True
                            changeTurn()
                            displayStatus("WINNER", diskColor)

        pygame.display.update()


main()
