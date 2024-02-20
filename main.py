import pygame
import math
from random import choice
from os import chdir
import sys

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    chdir(sys._MEIPASS)

pygame.init() #Initaization and clock and game loop condition
info = pygame.display.Info()
clock = pygame.time.Clock()
run = True

#Screen
title = "Hexagonal-2048"
screenSize = (800, 800)
screen = pygame.display.set_mode(screenSize)
pygame.display.set_caption(title)
h = screen.get_height()
w = screen.get_width()

font = pygame.font.SysFont('couriernew', 45, False)
font2 = pygame.font.SysFont('couriernew', 60, False)
font3 = pygame.font.SysFont('couriernew', 37, False)
score = 0
start = True
game = False
lose = False
mouseDownLocation = None
bgColor = "grey20"
uiTextColor = "lightgreen"
menuBtn = pygame.Rect(w/2-65, h-75, 65*2, 50)
smallHexBtn = pygame.Rect(w/6-110, 6/7*h-50, 110*2, 100)
triangleBtn = pygame.Rect(w*1/2-120, 6/7*h-50, 120*2, 100)
largeHexBtn = pygame.Rect(w*5/6-110, 6/7*h-50, 110*2, 100)
boardType = None

def smallHexBoard():
    global boardType
    emptyBoard = [[-1,0,1],  # test board
                   [7,8,9,2],
                   [6,10,3],
                   [5,4]]
    emptyBoard = [[8,-1,1],  # test board
                   [7,9,10,2],
                   [6,11,3],
                   [5,4]]
    emptyBoard = [[-1,-1,-1], # regular board
                   [-1,-1,-1,-1],
                   [-1,-1,-1],
                   [-1,-1]]
    boardType = "SmallHexagonal"
    return [l.copy() for l in emptyBoard]

def largeHexBoard():
    global boardType
    # emptyBoard = [[-1,-1,-1], # test board
    #                [-1,-1,-1,-1],
    #                [-1,-1,-1,-1,-1],
    #                [-1,-1,-1,-1],
    #                [-1,-1,-1]]
    emptyBoard = [[-1,-1,-1], # regular board
                   [-1,-1,-1,-1],
                   [-1,-1,-1,-1,-1],
                   [-1,-1,-1,-1],
                   [-1,-1,-1]]
    boardType = "LargeHexagonal"
    return [l.copy() for l in emptyBoard]

def triangleBoard():
    global boardType
    emptyBoard = [[11,-1,1,2,3],
                   [10,12,13,4],
                   [9,14,5],
                   [8,6],
                   [7]] # testboard
    emptyBoard = [[-1,-1,-1,-1,-1],
                  [-1,-1,-1,-1],
                  [-1,-1,-1],
                  [-1,-1],
                  [-1]]
    boardType = "Triangular"
    return [l.copy() for l in emptyBoard]

def drawHexagon(size, pos, color, thickness, content):
    position = [(pos[0] + size * math.sin(2 * math.pi * i / 6), 
                 pos[1] + size * math.cos(2 * math.pi * i / 6)) for i in range(6)]
    pygame.draw.polygon(screen, color, position)
    pygame.draw.polygon(screen, bgColor, position, thickness)
    contrastColor = "white" if pygame.Color(color).grayscale().g < 127 else "black"
    if len(content) < 3:
        x,y = font2.size(content)
        screen.blit(font2.render(content, True, contrastColor), [pos[0]-x/2, pos[1]-y/2])
    elif len(content) < 5:
        x,y = font.size(content)
        screen.blit(font.render(content, True, contrastColor), [pos[0]-x/2, pos[1]-y/2])
    else:
        x,y = font3.size(content)
        screen.blit(font3.render(content, True, contrastColor), [pos[0]-x/2, pos[1]-y/2])

def collapseBoardAndSpawnNewNumber(board:list[list[int]], direction:int):
    board, change = collapseBoard(board, direction)
    if change: board = spawnNewNumber(board)
    return board

def collapseBoard(board:list[list[int]], direction:int):
    board = rotateBoard(board, direction)
    change = False
    for row in board:
        row, c = collapseRow(row)
        if c: change = True
    board = rotateBoard(board, (6-direction)%6)
    return board, change

def collapseRow(row:list[int]):
    change = False
    emptyIndex = 0
    lastNumber = None
    lastNumberIndex = None
    for i in range(len(row)):
        if row[i] >= 0 and row[i] == lastNumber:
            row[i] = -1
            row[lastNumberIndex] += 1
            emptyIndex = lastNumberIndex + 1
            lastNumber = None
            lastNumberIndex = None
            change = True
        elif row[i] != -1 and i != emptyIndex:
            row[emptyIndex] = row[i]
            lastNumber = row[emptyIndex]
            lastNumberIndex = emptyIndex
            row[i] = -1
            emptyIndex += 1
            change = True
        elif row[i] != -1 and i == emptyIndex:
            emptyIndex += 1
            lastNumberIndex = i
            lastNumber = row[i]
    return row, change

def rotateBoard(board:list[list[int]], amount:int):
    for _ in range(amount):
        board = rotateBoardOneClockwise(board)
    return board

def rotateBoardOneClockwise(board:list[list[int]]):
    if boardType == "Triangular":
        return rotateTriangleBoard(board)
    elif boardType == "SmallHexagonal":
        return rotateSmallHexagonalBoard(board)
    elif boardType == "LargeHexagonal":
        return rotateLargeHexagonalBoard(board)
    else:
        raise ValueError(f"The board type '{boardType}' was not expected")

def rotateTriangleBoard(board:list[list[int]]):
    if len(board[0]) == 1:
        board = [[board[4][0],board[3][0],board[2][0],board[1][0],board[0][0]],
                 [board[4][1],board[3][1],board[2][1],board[1][1]],
                 [board[4][2],board[3][2],board[2][2]],
                 [board[4][3],board[3][3]],
                 [board[4][4]]]
    else:
        board = [[board[0][0]],
                 [board[1][0],board[0][1]],
                 [board[2][0],board[1][1],board[0][2]],
                 [board[3][0],board[2][1],board[1][2],board[0][3]],
                 [board[4][0],board[3][1],board[2][2],board[1][3],board[0][4]]]
    return board

def rotateSmallHexagonalBoard(board:list[list[int]]):
    if len(board[0]) == 3:
        board = [[board[1][0],board[0][0]],
                 [board[2][0],board[1][1],board[0][1]],
                 [board[3][0],board[2][1],board[1][2],board[0][2]],
                 [board[3][1],board[2][2],board[1][3]]]
    else:
        board = [[board[2][0],board[1][0],board[0][0]],
                 [board[3][0],board[2][1],board[1][1],board[0][1]],
                 [board[3][1],board[2][2],board[1][2]],
                 [board[3][2],board[2][3]]]
    return board

def rotateLargeHexagonalBoard(board:list[list[int]]):
    board = [[board[2][0],board[1][0],board[0][0]],
             [board[3][0],board[2][1],board[1][1],board[0][1]],
             [board[4][0],board[3][1],board[2][2],board[1][2],board[0][2]],
             [board[4][1],board[3][2],board[2][3],board[1][3]],
             [board[4][2],board[3][3],board[2][4]]]
    return board

def spawnNewNumber(board:list[list[int]]):
    global lose, score
    options = []
    for y in range(len(board)):
        for x in range(len(board[y])):
            if board[y][x] == -1:
                options.append((x,y))
    if options:
        x,y = choice(options)
        board[y][x] = 0
        score += 1
        if boardIsFull(board) and not legalMoves(board):
            lose = True
    else:
        lose = True
    return board

def boardIsFull(board):
    for row in board:
        for cell in row:
            if cell == -1:
                return False
    return True

def legalMoves(board:list[list[int]]):
    result = []
    for direction in range(6):
        testBoard = [row.copy() for row in board]
        _, change = collapseBoard(testBoard, direction)
        if change: result.append(direction)
    return result

def drawStartMenu(mousePosition):
    x,y = font2.size(title)
    screen.blit(font2.render(title, True, uiTextColor), [w/2-x/2, h/4-y/2])
    text = "Drag the mouse or use the"
    x,y = font3.size(text)
    screen.blit(font3.render(text, True, uiTextColor), [w/2-x/2, 3*h/7-y/2])
    size = 70
    letters = ["D","X","Z","A","W","E"]
    for i in range(6):
        x,y = font.size(letters[i])
        screen.blit(font.render(letters[i], True, uiTextColor), 
                    [w/2 - x/2 + size * math.cos(2 * math.pi * i / 6), 
                     4*h/7 - y/2 + size * math.sin(2 * math.pi * i / 6)])
    text = "keys to move the hexagons."
    x,y = font3.size(text)
    screen.blit(font3.render(text,True, uiTextColor), [w/2-x/2, 5*h/7-y/2])
    
    mp = mousePosition

    buttonColor = 'yellow' if smallHexBtn.collidepoint(mp[0],mp[1]) else uiTextColor
    pygame.draw.rect(screen, buttonColor, smallHexBtn)
    x,y = font.size("Small")
    screen.blit(font.render("Small", True, bgColor), [smallHexBtn.centerx-x/2,smallHexBtn.centery-y])
    x,y = font.size("Hexagon")
    screen.blit(font.render("Hexagon", True, bgColor), [smallHexBtn.centerx-x/2,smallHexBtn.centery])

    buttonColor = 'yellow' if triangleBtn.collidepoint(mp[0],mp[1]) else uiTextColor
    pygame.draw.rect(screen, buttonColor, triangleBtn)
    x,y = font.size("Triangle")
    screen.blit(font.render("Triangle", True, bgColor), [triangleBtn.centerx-x/2,triangleBtn.centery-y/2])
    
    buttonColor = 'yellow' if largeHexBtn.collidepoint(mp[0],mp[1]) else uiTextColor
    pygame.draw.rect(screen, buttonColor, largeHexBtn)
    x,y = font.size("Large")
    screen.blit(font.render("Large", True, bgColor), [largeHexBtn.centerx-x/2,largeHexBtn.centery-y])
    x,y = font.size("Hexagon")
    screen.blit(font.render("Hexagon", True, bgColor), [largeHexBtn.centerx-x/2,largeHexBtn.centery])

def drawUIText():
    x,_ = font.size(f'Score: {score}')
    screen.blit(font.render(f'Score: {score}', True, uiTextColor), [w-x-20,20])

def getValueString(number:int):
    match number:
        case -1: return ""
        case n: return str(2**n)

# thanks to https://sashamaps.net/docs/resources/20-colors/
def getColor(number:int):
    colors = [
    '#a9a9a9', # grey
    '#800000', # maroon
    '#f58231', # orange
    '#ffe119', # yellow
    '#3cb44b', # green
    '#808000', # olive
    '#42d4f4', # cyan
    '#911eb4', # purple
    '#000075', # navy
    '#f032e6', # magenta
    '#000000', # black
    '#ffffff', # white
    '#bfef45', # lime
    '#fabed4', # pink
    '#e6194B', # red
    '#9A6324', # brown
    '#4363d8', # blue
    '#ffd8b1', # apricot
    '#aaffc3', # mint
    '#469990', # teal
    '#dcbeff', # lavender
    '#fffac8', # beige
    ]
    return colors[number+1]

def drawCurrentBoard(position, size:int):
    global board
    boardSize = len(board)
    px, py = position
    m = size // (10*boardSize)
    px += (10*m) // 2
    py += (9*m) // 2
    for y in range(boardSize):
        for x in range(len(board[y])):
            padding = boardSize - len(board[y])
            i:int = board[y][x]
            drawHexagon(6*m, [padding*5*m+(x*10*m)+px, (y*9*m)+py], getColor(i), m, getValueString(i))

def getDirectionFromMouse(down, up):
    dx, dy = down
    ux, uy = up
    x = dx - ux
    y = dy - uy
    dist = math.sqrt(x**2+y**2)
    theta = math.pi + math.atan2(y,x)
    if dist < 25:
        return -1
    for angle in range(7):
        if abs(math.pi*angle/3-theta) < math.pi/8:
            return [3,2,1,0,5,4,3][angle]
    return -1

randomGame = False
boringGame = False

while run: #Game loop
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    mos = pygame.mouse.get_pos()
    for event in pygame.event.get(): # Event loop
        if event.type == pygame.QUIT:
            run = False
        elif not lose and not start and event.type == pygame.KEYDOWN: # key controls
            if event.key == pygame.K_a:
                board = collapseBoardAndSpawnNewNumber(board, 0)
            elif event.key == pygame.K_z:
                board = collapseBoardAndSpawnNewNumber(board, 1)
            elif event.key == pygame.K_x:
                board = collapseBoardAndSpawnNewNumber(board, 2)
            elif event.key == pygame.K_d:
                board = collapseBoardAndSpawnNewNumber(board, 3)
            elif event.key == pygame.K_e:
                board = collapseBoardAndSpawnNewNumber(board, 4)
            elif event.key == pygame.K_w:
                board = collapseBoardAndSpawnNewNumber(board, 5)
            elif event.key == pygame.K_r:
                board = rotateBoardOneClockwise(board)
            elif event.key == pygame.K_PAGEDOWN:
                move = choice(legalMoves(board))
                board = collapseBoardAndSpawnNewNumber(board, move)
            elif event.key == pygame.K_END:
                randomGame = True
            elif event.key == pygame.K_HOME:
                boringGame = True
        elif lose and event.type == pygame.MOUSEBUTTONDOWN: # Menu button
            if menuBtn.collidepoint(mos[0], mos[1]):
                randomGame = False
                boringGame = False
                start = True
                lose = False
                game = False
                score = 0
        elif game and not lose and event.type == pygame.MOUSEBUTTONDOWN: # mouse controls
            mouseDownLocation = mos
        elif mouseDownLocation and event.type == pygame.MOUSEBUTTONUP: # mouse controls
            direction = getDirectionFromMouse(mouseDownLocation, mos)
            if direction != -1:
                board = collapseBoardAndSpawnNewNumber(board, direction)
            mouseDownLocation = None
        elif start and (event.type==pygame.MOUSEBUTTONDOWN): # Title screen
            if triangleBtn.collidepoint(mos[0], mos[1]):
                board = triangleBoard()
            elif smallHexBtn.collidepoint(mos[0], mos[1]):
                board = smallHexBoard()
            elif largeHexBtn.collidepoint(mos[0], mos[1]):
                board = largeHexBoard()
            else:
                continue
            start = False
            game = True
            board = spawnNewNumber(board)
    if randomGame and not lose: board = collapseBoardAndSpawnNewNumber(board, choice(legalMoves(board)))
    if boringGame and not lose: board = collapseBoardAndSpawnNewNumber(board, legalMoves(board)[0])
    screen.fill(bgColor)
    if start: # Start menu
        drawStartMenu(mos)
    elif game: # Game board
        drawUIText()
        drawCurrentBoard([50, 100], 700)
    if lose: # Draw back to menu button
        buttonColor = 'yellow' if menuBtn.collidepoint(mos[0],mos[1]) else uiTextColor
        pygame.draw.rect(screen, buttonColor, menuBtn)
        x,y = font.size("Menu")
        screen.blit(font.render('Menu', True, bgColor), [menuBtn.centerx-x/2, menuBtn.centery-y/2])
    pygame.display.flip() # Update screen
    clock.tick(60)
pygame.quit()
