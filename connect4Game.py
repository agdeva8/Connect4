import pygame, sys
import numpy as np
from pygame.locals import *

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

displayWidth = 500;     displayHeight = 700;
startX = 50; startY = 50;
lineWidth = 2;
numLines = 7;
lineColor = BLUE; 

cellWidth = 50; 
cellHeight = 50;

endX = startX + numLines * cellWidth;
endY = startY + numLines * cellHeight;

xvals = np.arange(startX, endX + cellWidth, cellWidth)
yvals = np.arange(startY, endY + cellHeight, cellHeight)

def grid(DISPLAY):
    # drawing vertical lines
    for xVal in xvals:
        pygame.draw.line(DISPLAY, lineColor, (xVal, startY), (xVal, endY), lineWidth);
    
    for yVal in yvals:
    # drawing horizontal lines
        pygame.draw.line(DISPLAY, lineColor, (startX, yVal), (endX, yVal), lineWidth);

    pygame.display.flip()
    
def fillGrid(DISPLAY):
    pygame.draw.rect(DISPLAY, BLUE, (startX, startY, cellWidth * numLines, cellHeight * numLines), 0)
    pygame.display.update()

def createDisk(DISPLAY, row, col, color):
    x = int((xvals[row] + xvals[row + 1]) / 2) + 1;
    y = int((yvals[col] + yvals[col + 1]) / 2) + 1;
    pygame.draw.circle(DISPLAY, color, (x, y), int(cellWidth / 2) - 2, 0); 

def main():
    pygame.init()

    DISPLAY=pygame.display.set_mode((displayWidth,displayHeight))
    DISPLAY.fill(WHITE)
    
    # building grid
    grid(DISPLAY)
    fillGrid(DISPLAY)

    for row in range(0, numLines):
        for col in range(0, numLines):
            createDisk(DISPLAY, row, col, WHITE)

    # main loop to capture events
    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    x = event.pos[0];                       y = event.pos[1]
                    rowNum = (x - startX) / cellWidth;      colNum = (y - startY) / cellHeight 
                    if (rowNum < numLines and colNum < numLines): 
                        print("Col Num is {} and row Num is {}".format(colNum, rowNum))
                        createDisk(DISPLAY, rowNum, colNum, GREEN)

        pygame.display.update()

main()
