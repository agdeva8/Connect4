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
diskColor = [YELLOW,  RED]

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


def rowColFromXY(pos):
    x, y = pos
    col = (x - startX) / cellWidth
    row = (y - startY) / cellHeight 
    return (row, col)

def createDiskXY(x, y, radius, color):
    pygame.draw.circle(DISPLAY, color,  (x,  y),  radius,  0) 


def centerFromRC(row, col):
    x = int((xvals[col] + xvals[col + 1]) / 2) + 1
    y = int((yvals[row] + yvals[row + 1]) / 2) + 1
    return (x, y)

def createDisk(row,  col,  color):
    x, y = centerFromRC(row, col)
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
    def markDots(row, col, ri, ci):
        for i in range(4):
            x, y = centerFromRC(row + i*ri, col + i*ci)        
            createDiskXY(x, y, 5, BLACK)


    def markLine(row, col, ri, ci):
        x, y = centerFromRC(row, col)        
        x2, y2 = centerFromRC(row + 3*ri, col + 3*ci)        
        pygame.draw.line(DISPLAY, BLACK, (x, y), (x2, y2), 2) 

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
            markDots(row, col, 1, 0)
            markLine(row, col, 1, 0)
            return True

        # for vertical
        count = 0
        for i in range(4):
            if checkValidity(row, col + i):
                if boardConfig[row][col] == boardConfig[row][col + i]:
                    count = count + 1
        if count == 4:
            markDots(row, col, 0, 1)
            markLine(row, col, 0, 1)
            return True

        # for reverse diagonal
        count = 0
        for i in range(4):
            if checkValidity(row + i, col + i):
                if boardConfig[row][col] == boardConfig[row + i][col + i]:
                    count = count + 1
        if count == 4:
            markDots(row, col, 1, 1)
            markLine(row, col, 1, 1)
            return True

        # for diagonal
        count = 0
        for i in range(4):
            if checkValidity(row + i, col - i):
                if boardConfig[row][col] == boardConfig[row + i][col - i]:
                    count = count + 1
        if count == 4:
            markDots(row, col, 1, -1)
            markLine(row, col, 1, -1)
            return True
    return False


def updateConfig(currConfig,  row,  col):
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


def displayStatus(text):
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
    x = 110
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


def takeUndoAction(currConfig, lastMove):
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
    displayStatus("PLAYER")


def resetButtonPos():
    x = 50
    y = endY + 30
    width = 48
    height = 48
    return (x, y, width, height)


def dispResetButton():
    resetImg = pygame.image.load('icons/reset_48x48.jpg')
    x, y, width, height = resetButtonPos()
    DISPLAY.blit(resetImg, (x, y))
    # pygame.draw.rect(DISPLAY, BLACK, (x, y, width, height), 2)


def isResetPressed(pos):
    resetRec = pygame.Rect(resetButtonPos())
    if resetRec.collidepoint(pos):
        return True

def resetGrid(currConfig):
    global boardConfig
    global playerID

    playerID = 0

    DISPLAY.fill(WHITE)

    # building grid
    grid()
    fillGrid()

    displayStatus("PLAYER")
    dispUndoButton()
    dispResetButton()

    # empty coins
    for row in range(0,  numRows):
        for col in range(0,  numCols):
            createDisk(row,  col,  WHITE)

    # clear board and curr config
    for i in range(numCols):
        for j in range(numRows):
            currConfig[i] = numRows - 1
            boardConfig[j][i] = -1


def showColSelected(row, col):
    x = 30
    y = startY - 40
    width = endX - startX + 40
    height = 30
    pygame.draw.rect(DISPLAY, WHITE, (x, y, width, height), 0)
    
    if checkValidity(row, col) is False:
        return
    
    cx, cy = centerFromRC(row, col) 
    pygame.draw.polygon(DISPLAY, diskColor[playerID], ((cx - 10, y + 10), (cx + 10, y + 10), (cx, y + 25)))

def winnerCelebration():
    image = pygame.image.load('icons/winner_400x300.jpg')

    x = 25
    y = endY + 80
    DISPLAY.blit(image, (x, y))
    # pygame.draw.rect(DISPLAY, BLACK, (x, y, width, height), 2)


def main():
    global canUndo
    
    currConfig = [numRows - 1]*numCols

    resetGrid(currConfig)
    # main loop to capture events
    d_isCheckMate = False

    lastMove = (-1, -1)
    while True:
        row, col = rowColFromXY(pygame.mouse.get_pos())
        if (checkValidity(row, col)):
            # print("hovered: row {}, col{}".format(row, col))
            showColSelected(row, col)
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if (isResetPressed(event.pos)):
                        resetGrid(currConfig)
                        d_isCheckMate = False
                        lastMove = (-1, -1)
                        continue

                    if d_isCheckMate:
                        continue

                    if (isUndoPressed(event.pos)):
                        takeUndoAction(currConfig, lastMove)
                        continue

                    rowNum, colNum = rowColFromXY(event.pos)

                    lastMove, success = updateConfig(currConfig,  rowNum,  colNum)
                    if success:
                        changeTurn()
                        displayStatus("PLAYER")
                        canUndo = True
                        admitUndoImg()

                        if isCheckMate():
                            d_isCheckMate = True
                            changeTurn()
                            displayStatus("WINNER")
                            winnerCelebration()

        pygame.display.update()


main()
