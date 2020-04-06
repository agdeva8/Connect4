import pygame
import sys
import numpy as np
from pygame.locals import *
from itertools import product 

pygame.init()

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
font = pygame.font.Font('freesansbold.ttf', 32)

canUndo = True
playerID = 0

endX = startX + numCols * cellWidth
endY = startY + numRows * cellHeight

xvals = np.arange(startX,  endX + cellWidth,  cellWidth)
yvals = np.arange(startY,  endY + cellHeight,  cellHeight)

boardConfig = [ [-1]*numCols for _ in range(numRows)]

diskRadius = int(cellWidth / 2) - 5
def grid(DISPLAY):
    # drawing vertical lines
    for xVal in xvals:
        pygame.draw.line(DISPLAY,  lineColor,  (xVal,  startY),  (xVal,  endY),  lineWidth)
    
    for yVal in yvals:
    # drawing horizontal lines
        pygame.draw.line(DISPLAY,  lineColor,  (startX,  yVal),  (endX,  yVal),  lineWidth)

    pygame.display.flip()
    
def fillGrid(DISPLAY):
    pygame.draw.rect(DISPLAY,  BLUE,  (startX,  startY,  cellWidth * numCols,  cellHeight * numRows),  0)

def createDiskXY(DISPLAY, x, y, radius, color):
    pygame.draw.circle(DISPLAY,  color,  (x,  y),  radius,  0) 

def createDisk(DISPLAY,  row,  col,  color):
    x = int((xvals[col] + xvals[col + 1]) / 2) + 1
    y = int((yvals[row] + yvals[row + 1]) / 2) + 1
    createDiskXY(DISPLAY, x, y, diskRadius, color)

def changeTurn():
    global playerID
    if playerID == 0:
        playerID = 1
    else:
        playerID = 0

def checkValidity(row,  col):
    # print( str(row) + " " + str(numRows) + " " + str(col) + " " + str(numCols) + " ") 
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


def updateConfig(DISPLAY,  currConfig,  row,  col,   diskColor):
    lastMove = (-1, -1)

    if checkValidity(row,  col) is False: 
        return (lastMove, False)

    if currConfig[col] == -1:
        return (lastMove, False)

    lastMove = (currConfig[col], col)

    createDisk(DISPLAY,  lastMove[0], lastMove[1],  diskColor[playerID])

    boardConfig[currConfig[col]][col] = playerID
    currConfig[col] = currConfig[col] - 1
    
    return (lastMove, True)


def displayStatus(DISPLAY, text, diskColor):
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
    createDiskXY(DISPLAY, diskX, diskY, diskRadius, diskColor[playerID]) 


def undoButtonPos():
    x = 50
    y = endY + 30
    width = 48
    height = 48
    return (x, y, width, height)


def dispUndoButton(DISPLAY):
    undoImg2 = pygame.image.load('icons/undo_48x48.jpg')
    x, y, width, height = undoButtonPos()
    DISPLAY.blit(undoImg2, (x, y))
    # pygame.draw.rect(DISPLAY, BLACK, (x, y, width, height), 2)

def restrictUndoImg(DISPLAY):
    pygame.draw.rect(DISPLAY, RED, undoButtonPos(), 2)
    # dispUndoButton(DISPLAY)

def admitUndoImg(DISPLAY):
    pygame.draw.rect(DISPLAY, WHITE, undoButtonPos(), 2)
    # dispUndoButton(DISPLAY)

def isUndoPressed(pos):
    undoRec = pygame.Rect(undoButtonPos())
    if undoRec.collidepoint(pos):
        return True


def takeUndoAction(DISPLAY, currConfig, lastMove, diskColor):
    global canUndo
    if canUndo is False:
        return 

    row, col = lastMove
    if checkValidity(row,  col) is False: 
        return (lastMove, False)

    canUndo = False
    restrictUndoImg(DISPLAY)

    createDisk(DISPLAY, row, col, WHITE)

    boardConfig[row][col] = -1
    currConfig[col] = currConfig[col] + 1

    changeTurn()
    displayStatus(DISPLAY, "PLAYER", diskColor)


def main():
    global canUndo

    DISPLAY = pygame.display.set_mode((displayWidth, displayHeight))
    DISPLAY.fill(WHITE)

    # building grid
    grid(DISPLAY)
    fillGrid(DISPLAY)

    for row in range(0,  numRows):
        for col in range(0,  numCols):
            createDisk(DISPLAY,  row,  col,  WHITE)

    currConfig = [numRows - 1]*numCols
    diskColor = [YELLOW,  RED]

    # main loop to capture events
    d_isCheckMate = False

    displayStatus(DISPLAY, "PLAYER", diskColor)
    dispUndoButton(DISPLAY)

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
                        takeUndoAction(DISPLAY, currConfig, lastMove, diskColor)
                        continue

                    x = event.pos[0];                       y = event.pos[1]
                    colNum = (x - startX) / cellWidth;      rowNum = (y - startY) / cellHeight 

                    lastMove, success = updateConfig(DISPLAY,  currConfig,  rowNum,  colNum,   diskColor)
                    if success:
                        changeTurn()
                        displayStatus(DISPLAY, "PLAYER", diskColor)
                        canUndo = True
                        admitUndoImg(DISPLAY)

                        if isCheckMate():
                            d_isCheckMate = True
                            changeTurn()
                            displayStatus(DISPLAY, "WINNER", diskColor)

        pygame.display.update()


main()
