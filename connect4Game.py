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

def changeTurn(playerID):
    if playerID == 0:
        return 1
    return 0

def checkValidity(row,  col):
    print( str(row) + " " + str(numRows) + " " + str(col) + " " + str(numCols) + " ") 
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


def updateConfig(DISPLAY,  currConfig,  row,  col,  playerID,  diskColor):
    if checkValidity(row,  col) is False: 
        return False

    if currConfig[col] == -1:
        return False

    createDisk(DISPLAY,  currConfig[col],  col,  diskColor[playerID])
    boardConfig[currConfig[col]][col] = playerID
    currConfig[col] = currConfig[col] - 1
    return True


def displayStatus(DISPLAY, text, playerID, diskColor):
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
    pygame.draw.rect(DISPLAY, WHITE, (x, y, 200, 50), 0)
    pygame.display.update()
    DISPLAY.blit(text, textRect) 
    
    diskX = x + width - 30 - diskRadius
    diskY = textRect.centery
    createDiskXY(DISPLAY, diskX, diskY, diskRadius, diskColor[playerID]) 


def dispUndoButton(DISPLAY):
    undoImg2 = pygame.image.load('icons/undo_48x48.jpg')

    DISPLAY.blit(undoImg2, (50, endY + 30))


def main():
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
    playerID = 0
    displayStatus(DISPLAY, "PLAYER", playerID, diskColor)
    dispUndoButton(DISPLAY)
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if d_isCheckMate:
                continue
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    x = event.pos[0];                       y = event.pos[1]
                    colNum = (x - startX) / cellWidth;      rowNum = (y - startY) / cellHeight 
                    # if (rowNum < numRows and colNum < numCols): 
                    print("Col Num is {} and row Num is {}".format(rowNum,  colNum))
                    # createDisk(DISPLAY,  rowNum,  colNum,  diskColor[playerID])
                    if updateConfig(DISPLAY,  currConfig,  rowNum,  colNum,  playerID,  diskColor):
                        playerID = changeTurn(playerID)
                        displayStatus(DISPLAY, "PLAYER", playerID, diskColor)
                        if isCheckMate():
                            d_isCheckMate = True
                            playerID = changeTurn(playerID)
                            displayStatus(DISPLAY, "WINNER", playerID, diskColor)
        pygame.display.update()


main()
