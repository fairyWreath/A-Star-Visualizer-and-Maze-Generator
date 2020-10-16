import math
import pygame
import sys
sys.setrecursionlimit(10**6)

WIDTH = 600
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption(" A Star Maze Visualizer")

LIME = (0, 255, 0)
FUCHSIA = (255, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0 , 0, 255)            
PINK = (255, 153, 255)
PURPLE = (153, 0, 255)
GRAY = (128, 128, 128)
AQUA = (0, 255, 255)            
TURQUOISE = (64,224,208)

BASE = PINK
CLOSED = WHITE
OPEN = LIME
OBSTACLE = FUCHSIA
START = TURQUOISE
END = RED
LINE = GRAY
BACKTRACK = TURQUOISE
PATH = TURQUOISE

class Spot:
    def __init__(self, row, col, width, total, emptyStart):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        if emptyStart is False:
            self.color = OBSTACLE
        else:
            self.color = BASE
        self.width = width
        self.prev = None
        self.f = None

    def getPos(self):
        return self.x, self.y

    def getCoord(self):
        return self.row, self.col    

    def isClosed(self):
        return self.color == CLOSED
    
    def isOpen(self):
        return self.color == OPEN

    def isObs(self):
        return self.color == OBSTACLE

    def isStart(self):
        return self.color == START
    
    def isEnd(self):
        return self.color == END
    
    def reset(self):
        self.color = BASE

    def setOpen(self):
        self.color = OPEN

    def setClosed(self):
        self.color = CLOSED
    
    def setObs(self):
        self.color = OBSTACLE
       
    def setStart(self):
        self.color = START

    def setEnd(self):
        self.color = END
    
    def setBacktrack(self):
        self.color = BACKTRACK
    
    def setPath(self):
        self.color = PATH
    
    def resetBetween(self, compare, grid):      # for maze generation
        self.reset()
        compare.reset()
        x1, y1 = self.getCoord()
        x2, y2 = compare.getCoord()
        x, y = 0, 0

        if x1 - x2 == 0:
            x = x1
        elif (x1 - x2) < 0:
            x = x2 - 1
        else:
            x = x1 - 1
        if y1 - y2 == 0:
            y = y1
        elif (y1 - y2) < 0:
            y = y2 - 1
        else:
            y = y1 - 1
        
        grid[x][y].reset()

    def draw(self, win):    
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    def __str__(self):
        return "x: %d y: %d" % (self.row, self.col)

    # for maze generation
    def getFurtherNeighbors(self, grid, rows):     
        neighbors = set()
        if self.row > 1:
            neighbors.add(grid[self.row-2][self.col])
        if self.row < rows - 2:
            neighbors.add(grid[self.row+2][self.col])
        if self.col > 1:
            neighbors.add(grid[self.row][self.col-2])
        if self.col < rows - 2:
            neighbors.add(grid[self.row][self.col+2])
        return neighbors

    # for a star
    def getNeighbors(self, grid, rows):
        neighbors = set()
        if self.row > 0:
            neighbors.add(grid[self.row-1][self.col])
        if self.row < rows - 1:
            neighbors.add(grid[self.row+1][self.col])
        if self.col > 0:
            neighbors.add(grid[self.row][self.col-1])
        if self.col < rows - 1:
            neighbors.add(grid[self.row][self.col+1])
        if self.row > 0 and self.col > 0:
            neighbors.add(grid[self.row-1][self.col-1])
        if self.row > 0 and self.col  < rows - 1:
            neighbors.add(grid[self.row-1][self.col+1])
        if self.row < rows - 1 and self.col > 0:
            neighbors.add(grid[self.row+1][self.col-1])
        if self.row < rows - 1 and self.col < rows - 1:
            neighbors.add(grid[self.row+1][self.col+1])   
        return neighbors
    
    def getFourNeighbors(self, grid, rows):
        neighbors = set()
        if self.row > 0:
            neighbors.add(grid[self.row-1][self.col])
        if self.row < rows - 1:
            neighbors.add(grid[self.row+1][self.col])
        if self.col > 0:
            neighbors.add(grid[self.row][self.col-1])
        if self.col < rows - 1:
            neighbors.add(grid[self.row][self.col+1]) 
        return neighbors

    def setPrev(self, spot):
        self.prev = spot
    
    def getPrev(self):
        return self.prev

    def setF(self, val):
        self.f = val    

    def getF(self):
       return self.f

    def getDistanceBetween(self, spot):
        x1, y1 = self.getCoord()
        x2, y2 = spot.getCoord()

        if abs(x1 - x2) > 0 and abs(y1 - y2) > 0:
            return 14
        else:
            return 10    

def initializeGrid(rows, width, emptyStart):
    grid = []               # 2d list for grid
    gap = width // rows     # integer division, width of each spot
    for x in range(rows):
        grid.append([])
        for y in range(rows):
            spot = Spot(x, y, gap, rows, emptyStart)
            grid[x].append(spot)
    return grid

def drawBorders(win, rows, width):
    gap = width // rows
    for x in range(rows):
        pygame.draw.line(win, LINE, (0, x * gap),(width, x* gap))
        for y in range(rows):
            pygame.draw.line(win, LINE,  (y * gap, 0),(y* gap, width))


def drawGrid(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)
    drawBorders(win, rows, width)
    pygame.display.update()

def getClickedPos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    ROWS = 30

    emptyStart = False
    grid = initializeGrid(ROWS, width, emptyStart)
        
    start = None
    end = None
    
    if emptyStart is True:
        generateMaze = False
    else:
        generateMaze = True

    run = True
    while run:
        drawGrid(win, grid, ROWS, width)

        if generateMaze is True:
            draw_dfs_maze(lambda: drawGrid(win, grid, ROWS, width), grid, ROWS, 1, 1)
            generateMaze = False

        for event in pygame.event.get():
            if event.type  == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:   
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                spot = grid[row][col]

                if not start:          
                    if spot.isObs() == False:
                        start = spot
                        start.setStart()
                        
                elif not end:          
                    if spot.isObs() == False:
                        end = spot
                        end.setEnd()

                elif start != None and end != None:
                    if spot != start and spot != end:
                        spot.setObs()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    pathlist = draw_astar(lambda: drawGrid(win, grid, ROWS, width), grid, ROWS, start, start, end)
                    for path in pathlist:
                        path.setPath()


                if event.key == pygame.K_r:
                    grid = initializeGrid(ROWS, width, emptyStart)
                    start = None
                    end = None
                    generateMaze = True

    pygame.quit


import random
def draw_dfs_maze(draw, grid, rows, startx, starty, stack=None, visited=None, backtrack=False):
    if stack is None:
        stack = []
        visited = set()
    
    currspot = grid[startx][starty]

    if backtrack is False:
        stack.append(currspot)
        visited.add(currspot)

    neighbors = currspot.getFurtherNeighbors(grid, rows) - visited

    if len(neighbors) !=  0:
        sample = random.sample(neighbors,1)[0]
        sample.resetBetween(currspot, grid)
        draw()

        x, y = sample.getCoord()
        draw_dfs_maze(draw, grid, rows, x, y, stack, visited)    

    if len(neighbors) == 0 and len(stack) != 0:
        backspot = stack.pop()
        backspot.setBacktrack()
        x, y = backspot.getCoord()
        draw() 

        backspot.reset()
        draw_dfs_maze(draw, grid, rows, x, y, stack, visited, True) 
    
   
def heuristic(point1, point2):
    x1, y1 = point1.getCoord()
    x2, y2 = point2.getCoord()
    length = abs(x1 - x2)
    width = abs(y1 - y2)
    return (math.sqrt(pow(length,2) + pow(width,2)) * 10)


def calculateG(start, spot, value=0):
    if  start.getCoord() == spot.getCoord():
        return value

    value += spot.getDistanceBetween(spot.getPrev())
    return calculateG(start, spot.getPrev(), value)


def draw_astar(draw, grid, rows, mstart, start, end, closedlist=None,  pathlist=None, backtrack=False):
    if closedlist is None:
        closedlist = []
        pathlist = []
        start.setF(0)

    if  start.getCoord() == end.getCoord():
        pathlist.append(end)
        return pathlist

    if backtrack is False:
        closedlist.append(start)
        pathlist.append(start)
    
    neighbors = start.getFourNeighbors(grid, rows) - set(closedlist)
    leastf = 9999
    fspot = None
   
    for neighbor in neighbors:
        neighbor.setPrev(start)
        if neighbor.isObs():
            continue
        neighbor.setClosed()
        draw()
        g = calculateG(mstart, neighbor)
        h = heuristic(neighbor, end)
        neighbor.setF(g+h)
        if neighbor.getF() < leastf:
            leastf = neighbor.getF()
            fspot = neighbor
            neighbor.setOpen()
            draw()

    if backtrack is True and fspot:
        pathlist.append(start)

    if fspot is None:
        currspot = pathlist.pop()
        currspot.reset()
        draw()
        return draw_astar(draw, grid, rows, mstart, currspot, end, closedlist, pathlist, True)

    return draw_astar(draw, grid, rows, mstart, fspot, end, closedlist, pathlist)

main(WINDOW, WIDTH)

