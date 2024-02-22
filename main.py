import pygame
import math
import asyncio
from random import choice

pygame.init()
score = 0
boardType = "SmallHexagonal"
gameType = "power2"
lose = False

title = "Hexagonal-2048"
font = pygame.font.SysFont(None, 60, False)
font2 = pygame.font.SysFont(None, 80, False)
font3 = pygame.font.SysFont(None, 50, False)
bgColor = "grey20"
uiTextColor = "lightgreen"

def smallHexBoard():
    global boardType
    # emptyBoard = [[-1,0,1],  # test board
    #               [7,8,9,2],
    #               [6,10,3],
    #               [5,4]]
    emptyBoard = [[-1,-1,-1], # empty board
                  [-1,-1,-1,-1],
                  [-1,-1,-1],
                  [-1,-1]]
    boardType = "SmallHexagonal"
    return [l.copy() for l in emptyBoard]

def largeHexBoard():
    global boardType
    # emptyBoard = [[35,-1,1],  # test board
    #               [19,21,23,3],
    #               [17,31,33,25,5],
    #               [15,29,27,7],
    #               [13,11,9]]
    emptyBoard = [[-1,-1,-1], # empty board
                  [-1,-1,-1,-1],
                  [-1,-1,-1,-1,-1],
                  [-1,-1,-1,-1],
                  [-1,-1,-1]]
    boardType = "LargeHexagonal"
    return [l.copy() for l in emptyBoard]

def triangleBoard():
    global boardType
    # emptyBoard = [[-1,0,1,2,3], # test board
    #                [10,11,12,4],
    #                [9,13,5],
    #                [8,6],
    #                [7]]
    emptyBoard = [[-1,-1,-1,-1,-1], # empty board
                  [-1,-1,-1,-1],
                  [-1,-1,-1],
                  [-1,-1],
                  [-1]]
    boardType = "Triangular"
    return [l.copy() for l in emptyBoard]

def drawHexagon(screen, size, pos, color, thickness, content):
    position = [(pos[0] + size * math.sin(2 * math.pi * i / 6), 
                 pos[1] + size * math.cos(2 * math.pi * i / 6)) for i in range(6)]
    pygame.draw.polygon(screen, color, position)
    pygame.draw.polygon(screen, bgColor, position, math.ceil(thickness))
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
    board = rotateBoard(board, (6 - direction) % 6)
    return board, change

def collapseRow(row:list[int]):
    global gameType
    if gameType == "power2":
        return collapseRowPowerTwo(row)
    elif gameType == "power3":
        return collapseRowPowerThree(row)
    elif gameType == "fibonacci":
        return collapseRowFibonacci(row)
    else:
        raise NotImplementedError(f"{gameType} not implemented")

def collapseRowFibonacci(row:list[int]):
    change = False
    emptyIndex = 0
    lastNumber = None
    lastNumberIndex = None
    for i in range(len(row)):
        if row[i] == 0 and lastNumber == 0:
            row[lastNumberIndex] = 1
            row[i] = -1
            emptyIndex = lastNumberIndex + 1
            lastNumber = None
            lastNumberIndex = None
            change = True
        elif row[i] >= 0 and lastNumber!=None and abs(row[i] - lastNumber) == 1:
            row[lastNumberIndex] = max(row[i], lastNumber) + 1
            row[i] = -1
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

def collapseRowPowerThree(row:list[int]):
    change = False
    emptyIndex = 0
    lastNumber = None
    lastNumberIndex = None
    for i in range(len(row)):
        if (lastNumberIndex and lastNumberIndex > 0 and row[i] >= 0 and 
                row[i] == lastNumber and row[lastNumberIndex-1] == lastNumber):
            row[lastNumberIndex-1] += 1
            row[i] = -1
            row[lastNumberIndex] = -1
            emptyIndex = lastNumberIndex
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

def collapseRowPowerTwo(row:list[int]):
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
    global boardType
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

def drawStartMenu(screen:pygame.Surface, mousePosition, boardButtons, gameTypeButtons, startButton):
    global font, font2, font3, title, uiTextColor, gameType
    h = screen.get_height()
    w = screen.get_width()
    x,y = font2.size(title)
    screen.blit(font2.render(title, True, uiTextColor), [w/2 - x/2, 100 - y/2])
    text = "Drag with mouse or finger,"
    x,y = font3.size(text)
    screen.blit(font3.render(text, True, uiTextColor), [w/2 - x/2, 200 - y/2])
    size = 70
    text = "or use the"
    x,y = font3.size(text)
    screen.blit(font3.render(text, True, uiTextColor), [w/2 - x/2, 240 - y/2])
    size = 70
    letters = ["D","X","Z","A","W","E"]
    for i in range(6):
        x,y = font.size(letters[i])
        screen.blit(font.render(letters[i], True, uiTextColor), 
                    [w/2 - x/2 + size * math.cos(2 * math.pi * i / 6), 
                     350 - y/2 + size * math.sin(2 * math.pi * i / 6)])
    text = "keys to move the hexagons."
    x,y = font3.size(text)
    screen.blit(font3.render(text,True, uiTextColor), [w/2 - x/2, 460 - y/2])
    
    gtDoubleBtn, gtFiboBtn, gtTripleBtn = gameTypeButtons
    buttonColor = 'yellow' if gameType == "power2" else uiTextColor
    drawButton(screen, "Double", gtDoubleBtn, buttonColor)
    buttonColor = 'yellow' if gameType == "fibonacci" else uiTextColor
    drawButton(screen, "Fibonacci", gtFiboBtn, buttonColor)
    buttonColor = 'yellow' if gameType == "power3" else uiTextColor
    drawButton(screen, "Triple", gtTripleBtn, buttonColor)
    [pygame.draw.rect(screen, "black", r, 4) for r in gameTypeButtons]

    smallHexBtn, triangleBtn, largeHexBtn = boardButtons
    buttonColor = 'yellow' if boardType == "SmallHexagonal" else uiTextColor
    drawButton(screen, "Small Hexagon", smallHexBtn, buttonColor, True)
    buttonColor = 'yellow' if boardType == "Triangular" else uiTextColor
    drawButton(screen, "Triangle", triangleBtn, buttonColor)
    buttonColor = 'yellow' if boardType == "LargeHexagonal" else uiTextColor
    drawButton(screen, "Large Hexagon", largeHexBtn, buttonColor, True)
    [pygame.draw.rect(screen, "black", r, 4) for r in boardButtons]

    mp = mousePosition
    buttonColor = 'yellow' if startButton.collidepoint(mp[0],mp[1]) else uiTextColor
    drawButton(screen, "Start", startButton, buttonColor)

def drawButton(surface:pygame.Surface, text:str, rect:pygame.Rect, color, twoLine=False):
    pygame.draw.rect(surface, color, rect)
    if not twoLine:
        x,y = font.size(text)
        surface.blit(font.render(text, True, bgColor), [rect.centerx-x/2, rect.centery-y/2])
        return
    texts = text.split()
    x,y = font.size(texts[0])
    surface.blit(font.render(texts[0], True, bgColor), [rect.centerx-x/2, rect.centery-20-y/2])
    x,y = font.size(texts[1])
    surface.blit(font.render(texts[1], True, bgColor), [rect.centerx-x/2, rect.centery+20-y/2])

def drawUIText(screen:pygame.Surface):
    global score
    w = screen.get_width()
    x,_ = font.size(f'Score: {score}')
    screen.blit(font.render(f'Score: {score}', True, uiTextColor), [w-x-20,20])

def getValueString(number:int):
    global gameType
    if gameType == "power2":
        a = 2 
    elif gameType == "power3":
        a = 3
    elif gameType == "fibonacci":
        return ["","1","2","3","5","8","13","21","34","55","89","144","233","377","610",
                "987","1597","2584","4181","6765","10946","17711","28657","46368","75025",
                "121393","196418","317811","514229","832040","1.3 M","2.2 M","3.5 M",
                "5.7 M","9.2 M","14 M","24 M","WOW!"][number + 1]
    else:
        raise NotImplementedError()
    match number:
        case -1: return ""
        case n: return str(a**n)

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
    '#000075', # navy
    '#911eb4', # purple
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
    n = (number + 1) % len(colors)
    return colors[n]

def drawCurrentBoard(screen, board:list[list[int]], position, boardWidth:int):
    boardSize = len(board)
    rt = math.sqrt(3)
    px, py = position
    size = boardWidth / (boardSize * rt)
    px += size * rt / 2
    py += size * 3/2
    for y in range(boardSize):
        for x in range(len(board[y])):
            padding = (boardSize - len(board[y])) * size * rt / 2
            i:int = board[y][x]
            place = [padding + (x * size * rt) + px, (y * size * 3/2) + py]
            drawHexagon(screen, size, place, getColor(i), size/6, getValueString(i))

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

async def main():
    global font, font2, font3, lose, score, gameType
    clock = pygame.time.Clock()
    #Screen
    screenSize = (800, 900)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption(title)
    h = screen.get_height()
    w = screen.get_width()

    game = False
    mouseDownLocation = None
    gtDoubleBtn = pygame.Rect(w/2-356, h-375, 120*2, 100)
    gtFiboBtn = pygame.Rect(w/2-120, h-375, 120*2, 100)
    gtTripleBtn = pygame.Rect(w/2+116, h-375, 120*2, 100)
    gameTypeButtons = [gtDoubleBtn, gtFiboBtn, gtTripleBtn]
    smallHexBtn = pygame.Rect(w/2-356, h-250, 120*2, 100)
    triangleBtn = pygame.Rect(w/2-120, h-250, 120*2, 100)
    largeHexBtn = pygame.Rect(w/2+116, h-250, 120*2, 100)
    boardButtons = [smallHexBtn, triangleBtn, largeHexBtn]
    startBtn = pygame.Rect(w/2-120, h-125, 120*2, 100)
    menuBtn = pygame.Rect(w/2-80, h-110, 80*2, 75)
    run = True
    start = True
    randomGame = False
    boringGame = False
    board = smallHexBoard()
    while run: #Game loop
        await asyncio.sleep(0)
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
                    board = [[-1 for _ in row] for row in board]
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
                if gtDoubleBtn.collidepoint(mos[0], mos[1]):
                    gameType = "power2"
                elif gtFiboBtn.collidepoint(mos[0], mos[1]):
                    gameType = "fibonacci"
                elif gtTripleBtn.collidepoint(mos[0], mos[1]):
                    gameType = "power3"
                if triangleBtn.collidepoint(mos[0], mos[1]):
                    board = triangleBoard()
                elif smallHexBtn.collidepoint(mos[0], mos[1]):
                    board = smallHexBoard()
                elif largeHexBtn.collidepoint(mos[0], mos[1]):
                    board = largeHexBoard()
                elif startBtn.collidepoint(mos[0], mos[1]):
                    start = False
                    game = True
                    board = spawnNewNumber(board)
        if randomGame and not lose: board = collapseBoardAndSpawnNewNumber(board, choice(legalMoves(board)))
        elif boringGame and not lose: board = collapseBoardAndSpawnNewNumber(board, legalMoves(board)[0])
        screen.fill(bgColor)
        if start: # Start menu
            drawStartMenu(screen, mos, boardButtons, gameTypeButtons, startBtn)
        elif game: # Game board
            drawUIText(screen)
            drawCurrentBoard(screen, board, [50, 50], 700)
        if lose: # Draw back to menu button
            buttonColor = 'yellow' if menuBtn.collidepoint(mos[0],mos[1]) else uiTextColor
            drawButton(screen, "Menu", menuBtn, buttonColor)
        pygame.display.flip() # Update screen
        clock.tick(60)

asyncio.run(main())