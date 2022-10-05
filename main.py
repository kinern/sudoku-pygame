import pygame
from pygame.locals import *
import random
import math
import copy
from enum import Enum
import shelve


screen_width = 640
screen_height = 480

class SudokuMatrix(object):
    def __init__(self, size, missingNum):
        self.size = size
        self.missingNum = missingNum
        #square root to used for diagonal sub-matrixes
        self.sqrt = int(math.sqrt(size))
        self.matrix = [[0 for x in range(size)] for x in range(size)]
        self.solutionMatrix = [[0 for x in range(size)] for x in range(size)]

    def generateMatrix(self):
        self.matrix = [[0 for x in range(self.size)] for x in range(self.size)]
        self.fillDiagonalSubmatrixes()
        self.fillMissingSubMatrixes()
        self.solutionMatrix = copy.deepcopy(self.matrix)
        self.addMissingSquares()
        #print(self.matrix)
    
    def fillDiagonalSubmatrixes(self):
        for a in range(0, self.size, self.sqrt):
            self.fillSubMatrix(a,a)

    def addMissingSquares(self):
        left = self.missingNum
        while (left > 0):
            rangeMax = int(self.size*self.size)
            cellIndex = random.randrange(0,rangeMax)
            subMatrixIndex = int(cellIndex / self.size)
            subMatrixMod = int(cellIndex % self.size)
            if ((self.matrix[subMatrixIndex][subMatrixMod] != "")):
                self.matrix[subMatrixIndex][subMatrixMod] = ""
                left = left - 1

    def fillSubMatrix(self, row, col):
        for i in range(0, self.sqrt):
            for j in range(0, self.sqrt):
                num = random.randrange(1,self.size)
                while (self.unusedInBox(row, col, num) == False): 
                    num = random.randrange(1,self.size+1)
                self.matrix[row + i][col + j] = num


    def checkIfPlaceable(self, row, col, num):
        check = (self.unusedInRow(row, num) and
                self.unusedInCol(col, num) and
                self.unusedInBox(row-int(row % self.sqrt), col-int(col % self.sqrt), num))
        return check
    
    def unusedInRow(self, row, num):
        for j in range(0, self.size):
           if (self.matrix[row][j] == num):
                return False
        return True
    
    def unusedInCol(self, col, num):
        for i in range(0, self.size):
           if (self.matrix[i][col] == num):
                return False
        return True

    def unusedInBox(self, row, col, num):
        for i in range(0, self.sqrt):
            for j in range(0, self.sqrt):
                if (self.matrix[row+i][col+j] == num):
                    return False
        return True

    def hasEmptySquare(self, l):
        for row in range(self.size):
            for col in range(self.size):
                if(self.matrix[row][col] == 0):
                    l[0]= row
                    l[1]= col
                    return True
        return False


    def fillMissingSubMatrixes(self):
        l = [0, 0]
        if(self.hasEmptySquare(l) == False):
            return True
        else:
            row = l[0]
            col = l[1]
            for num in range(1, self.size+1):
                if(self.checkIfPlaceable(row, col, num)):
                    self.matrix[row][col]= num
                    if(self.fillMissingSubMatrixes()):
                        return True
                    self.matrix[row][col] = 0      
            return False

class GameState(Enum):
    PREVSTATE = -2
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    LOAD = 2
    

gameState = GameState.TITLE

class Button():
        def __init__(self, text,  pos, size, font, onClick, fontColor="White", bg="black"):
            self.x, self.y = pos
            self.font = pygame.font.SysFont("Verdana", font)
            self.onClick = onClick
            self.text = self.font.render(text, 1, pygame.Color(fontColor))
            self.size = size
            self.surface = pygame.Surface(self.size)
            self.surface.fill(bg)
            self.surface.blit(self.text, (int(self.size[0]/2)-int(self.text.get_rect().width/2), int(self.size[1]/2)-int(self.text.get_rect().height/2)))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    
        #def show(self):
        #    screen.blit(self.surface, (self.x, self.y))
    
        def click(self, event):
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.onClick()


def titleScreen(screen):

    localGameState = GameState.TITLE

    def changeToNewGame():
        nonlocal localGameState
        localGameState = GameState.NEWGAME

    def changeToLoadScreen():
        nonlocal localGameState
        localGameState = GameState.LOAD

    def quitGame():
        nonlocal localGameState
        localGameState = GameState.QUIT

    startBtn = Button(
        "Start",
        pos=(int(640/2)-40, 250),
        size=(80, 30),
        font=14,
        fontColor=(80,80,80),
        bg=(255,255,255),
        onClick=changeToNewGame)

    loadBtn = Button(
        "Load",
        pos=(int(640/2)-40, 290),
        size=(80,30),
        font=14,
        fontColor=(80,80,80),
        bg=(255,255,255),
        onClick=changeToLoadScreen)

    quitBtn = Button(
        "Quit",
        pos=(int(640/2)-40, 330),
        size=(80, 30),
        font=14,
        fontColor=(80,80,80),
        bg=(255,255,255),
        onClick=quitGame)

    buttons = [startBtn, loadBtn, quitBtn]

    titleImage = pygame.image.load("sudoku-title.png").convert_alpha()

    footerFont = pygame.font.SysFont("Verdana", 14)
    footerText = footerFont.render("Created by Natalie (kinern @ github)", 1, pygame.Color(80,80,80))

    #Render Title Screen
    screen.fill((230,150,150))
    screen.blit(titleImage, pygame.rect.Rect(int(640/2)-int(305/2),60, 305, 102))
    screen.blit(footerText, (int(640/2)-140, 440))
    for button in buttons:
        screen.blit(button.surface, (button.x, button.y))
    pygame.display.flip()

    while True:
        if (localGameState != GameState.TITLE):
            return localGameState

        #Handle Title Screen Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for button in buttons:
                        button.click(event)


#Game data class for returning from load menu
class GameData:
    def __init__(self, gameMatrix, solutionMatrix, inputValues):
        self.gameMatrix = gameMatrix
        self.solutionMatrix = solutionMatrix
        self.inputValues = inputValues

def gameScreen(screen, currentGameData = None):

    localGameState = GameState.NEWGAME

    def changeToTitle():
        nonlocal localGameState
        localGameState = GameState.TITLE
    
    def quitGame():
        nonlocal localGameState
        localGameState = GameState.QUIT
    
    def loadGameScreen():
        nonlocal localGameState
        nonlocal currentGameData
        inputValues = getInputValues()
        currentGameData = GameData(matrix.matrix, matrix.solutionMatrix, inputValues)
        localGameState = GameState.LOAD

    def getInputValues():
        inputValues = [] 
        for n in inputBoxCollection:
            inputValues.append({"matrixIndex": n.matrixIndex, "value": n.value})
        return inputValues

    screenBgColor = (180, 150, 220)
    matrixFont = pygame.font.SysFont('Verdana', 30)
    matrix = SudokuMatrix(9, 54)

    inputBoxCollection = []
    alertBoxCollection = []

    class InputBox():
        def __init__(self, pos, font, matrixIndex, bgColor=(255,255,255), fontColor=(80,80,80)):
            self.x, self.y = pos
            self.value = ""
            self.selected = False
            self.font = pygame.font.SysFont("Verdana", font)
            self.fontColor = fontColor
            self.bgColor = bgColor
            self.inactiveBgColor = bgColor
            self.selectedBgColor = (bgColor[0]-50, bgColor[1]-50, bgColor[2]-50)
            self.wrongColor = (255, 100, 100)
            self.text = self.font.render(self.value, 1, pygame.Color(self.fontColor))
            self.size = (40, 40)
            self.surface = pygame.Surface(self.size)
            self.surface.fill(self.bgColor)
            self.surface.blit(self.text, (10, 0))
            self.rect = pygame.Rect(self.x, self.y, self.size[0]+10, self.size[1]+10)
            self.matrixIndex = matrixIndex
        
        def show(self):
            screen.blit(self.surface, (self.x, self.y))
        
        def update(self):
            self.text = self.font.render(self.value, 1, pygame.Color(self.fontColor))
            self.surface.fill(self.bgColor)
            self.surface.blit(self.text, (10, 0))
            self.rect = pygame.Rect(self.x, self.y, self.size[0]+10, self.size[1]+10)
            screen.blit(self.surface, (self.x, self.y))
            pygame.display.flip()
    
        def handleEvent(self, event):
            x, y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if self.rect.collidepoint(x, y):
                        self.selected = True
                        if (self.bgColor == self.inactiveBgColor or self.bgColor == self.wrongColor):
                            self.bgColor = self.selectedBgColor
                            self.update()
                    else:
                        self.selected = False
                        if (self.bgColor == self.selectedBgColor):
                            self.bgColor = self.inactiveBgColor
                            self.update()

            if (self.selected):
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.value = self.value[:-1]
                    else:
                        if (str(event.unicode).isnumeric() and str(event.unicode) != "0" ):
                            self.value = event.unicode
                    self.update()
        
        def highlightRed(self):
            self.bgColor = self.wrongColor
            self.update()
    

    #Win / Lose Messages
    class AlertBox():
        def __init__(self, pos, text, size, fontSize, bgColor=(255,255,255), fontColor=(80,80,80)):
            self.x, self.y = pos
            self.active = False
            self.bgColor = bgColor
            self.fontColor = fontColor
            self.font = pygame.font.SysFont("Verdana", fontSize)
            self.text = self.font.render(text, 1, pygame.Color(self.fontColor))
            self.size = size
            self.surface = pygame.Surface(self.size)
            self.surface.fill(self.bgColor)
            self.surface.blit(self.text, (int(self.size[0]/2)-int(self.text.get_rect().width/2), int(self.size[1]/2)-int(self.text.get_rect().height/2)))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

        def show(self):
            self.active = True
            screen.blit(self.surface, (self.x, self.y))
        
        def hide(self):
            self.active = False

        def click(self, event):
            x, y = pygame.mouse.get_pos()
            if (not self.rect.collidepoint(x, y)):
                self.hide()


    #New Matrix 
    def renderNewMatrix():
        for row in range(9):
            for col in range(9):
                if (str(matrix.matrix[row][col]) == ""):
                    #inputRect = Rect(row*50+100, col*50+10, 40, 40)
                    #pygame.draw.rect(screen, (255,255,255), inputRect)
                    newInputBox = InputBox(
                        pos=(row*50+100, col*50+20),
                        font=30,
                        matrixIndex=[row,col],
                    )
                    newInputBox.show()
                    inputBoxCollection.append(newInputBox)
                else:
                    matrixNum = matrixFont.render(str(matrix.matrix[row][col]), True, (255,255,255))
                    screen.blit(matrixNum, (row*50+110,col*50+20))
    
    #Existing matrix
    def renderMatrix():
        for row in range(9):
            for col in range(9):
                if (str(matrix.matrix[row][col]) != ""):
                    matrixNum = matrixFont.render(str(matrix.matrix[row][col]), True, (255,255,255))
                    screen.blit(matrixNum, (row*50+110,col*50+20))
        for m in inputBoxCollection:
            m.show()


    def checkAnswers():
        wrong = False
        for n in inputBoxCollection:
            matrixIndex = n.matrixIndex
            if (str(n.value) != str(matrix.solutionMatrix[matrixIndex[0]][matrixIndex[1]])):
                n.highlightRed()
                wrong = True
        if (wrong):
            hideAlerts()
            loseAlert.show()
        else:
            hideAlerts()
            winAlert.show()
        renderScreen()
    

    loseAlert = AlertBox(
        pos=(int(screen_width/2)-int(300/2),int(screen_height/2)-int(120/2)), 
        text="Incorrect!", 
        size=(300,120), 
        fontSize=40,
        bgColor=(255,255,255), 
        fontColor=(80,80,80)
    )

    winAlert = AlertBox(
        pos=(int(screen_width/2)-int(300/2),int(screen_height/2)-int(120/2)), 
        text="You Win!", 
        size=(300,120), 
        fontSize=40, 
        bgColor=(255,255,255), 
        fontColor=(80,80,80)
    )

    noHintsAlert = AlertBox(
        pos=(int(screen_width/2)-int(300/2),int(screen_height/2)-int(120/2)), 
        text="No Hints Left", 
        size=(300,120), 
        fontSize=40, 
        bgColor=(255,255,255), 
        fontColor=(80,80,80)
    )

    alertBoxCollection.append(loseAlert)
    alertBoxCollection.append(winAlert)
    alertBoxCollection.append(noHintsAlert)

    def hideAlerts():
        for n in alertBoxCollection:
            n.hide()
    
    def newGame():
        inputBoxCollection.clear()
        screen.fill(screenBgColor)
        matrix.generateMatrix()
        renderNewMatrix()
        for button in buttons:
            screen.blit(button.surface, (button.x, button.y))
        pygame.display.flip()

    #Render everything to screen
    def renderScreen():
        screen.fill(screenBgColor)
        renderMatrix()
        for button in buttons:
            screen.blit(button.surface, (button.x, button.y))
        for m in alertBoxCollection:
            if m.active:
                m.show()
        pygame.display.flip()
    
    def getHint():
        i = 0
        found = False
        while (i < len(inputBoxCollection)):
            curInput = inputBoxCollection[i]
            solutionValue = str(matrix.solutionMatrix[curInput.matrixIndex[0]][curInput.matrixIndex[1]])
            if (str(curInput.value) != solutionValue):
                found = True
                inputBoxCollection[i].value = solutionValue
                clearBgColors()
                inputBoxCollection[i].bgColor = inputBoxCollection[i].selectedBgColor
                inputBoxCollection[i].update()
                i = len(inputBoxCollection)
            i = i + 1 
        if (not found):
            hideAlerts()
            noHintsAlert.show()
        renderScreen()

    def clearBgColors():
        for n in inputBoxCollection:
            n.bgColor = n.inactiveBgColor
            n.update()


    def loadGame():
        savedMatrix, solutionMatrix, inputValues = load()
        gameData = GameData(savedMatrix, solutionMatrix, inputValues)
        renderGameData(gameData)

    def load():
        try:
            gameData = shelve.open("save.bin") 
            return gameData['matrix'], gameData['solutionMatrix'], gameData['inputValues']
        except KeyError:
            return None
        finally:
            gameData.close()
        
    
    newGameButton = Button(
    "New Game",
    pos=(10, 10),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=newGame)

    checkButton = Button(
    "Check",
    pos=(10, 50),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=checkAnswers)

    hintButton = Button(
    "Hint",
    pos=(10, 90),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=getHint)

    titleButton = Button(
    "Title",
    pos=(10, 130),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=changeToTitle)

    quitButton = Button(
    "Quit",
    pos=(10, 170),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=quitGame)

    loadScreenButton = Button(
    "Save",
    pos=(10, 210),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=loadGameScreen)

    buttons = [newGameButton, checkButton, hintButton, titleButton, quitButton, loadScreenButton]

    def renderGameData(gameData):
        inputBoxCollection.clear()
        screen.fill(screenBgColor)
        matrix.matrix = gameData.gameMatrix
        matrix.solutionMatrix = gameData.solutionMatrix
        renderNewMatrix()
        for n in inputBoxCollection:
            inputVal =  [m for m in gameData.inputValues if m["matrixIndex"] == n.matrixIndex]
            inputVal = inputVal[0]
            n.value = inputVal["value"]
            n.update()
        renderScreen()
        for button in buttons:
            screen.blit(button.surface, (button.x, button.y))
        pygame.display.flip()

    #Initial Render
    if (currentGameData != None):
        renderGameData(currentGameData)
    else:
        newGame()

    while True:
        if localGameState != GameState.NEWGAME:
            return {'state':localGameState, 'data':currentGameData} #Change this
        #Handle Title Screen Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for alert in alertBoxCollection:
                        alert.click(event)
                    for button in buttons:
                        button.click(event)
                    renderScreen()

            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
                for n in inputBoxCollection:
                    n.handleEvent(event)

def loadScreen(screen, currentGameData = None):

    localGameState = GameState.LOAD
    
    class saveFileBox:
        def __init__(self, num):
            self.num = num

        def render(self, num):
            boxRect = Rect(40, 80*self.num+10, 240, 80)
            pygame.draw.rect(screen, (255,255,255), boxRect)
    
    #Display files with buttons
    saveFileBoxes = []
    for n in range(3):
        newBox = saveFileBox(n)
        saveFileBoxes.append(newBox)
    
    def saveGame():
        if (currentGameData == None):
            print("No game data to save")
            return False
        gameData = shelve.open("save.bin") 
        gameData['matrix'] = currentGameData.gameMatrix
        gameData['solutionMatrix'] = currentGameData.solutionMatrix
        gameData['inputValues'] = currentGameData.inputValues
        gameData.close()
        print("saved data")

    loadedGameData = None

    def load():
        nonlocal localGameState
        nonlocal loadedGameData
        try:
            gameData = shelve.open("save.bin") 
            loadedGameData =  GameData(gameData['matrix'], gameData['solutionMatrix'], gameData['inputValues'])
            localGameState = GameState.NEWGAME
        except KeyError:
            return None
        finally:
            gameData.close()

    def goBack():
        nonlocal localGameState
        localGameState = GameState.PREVSTATE

    def quitGame():
        nonlocal localGameState
        localGameState = GameState.QUIT

    #Get history from main loop to determine if this is disabled
    saveBtn = Button(
    "Save",
    pos=(100, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=saveGame)

    #Check if no loads available
    loadBtn = Button(
    "Load",
    pos=(220, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=load)

    returnBtn = Button(
    "Return",
    pos=(340, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=goBack)

    quitBtn = Button(
    "Quit",
    pos=(460, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=quitGame)

    buttons = [saveBtn, loadBtn, returnBtn, quitBtn]

    #Render Load Screen
    screen.fill((150,200,180))
    for button in buttons:
        screen.blit(button.surface, (button.x, button.y))
    pygame.display.flip()

    running = True
    while running:
        if localGameState != GameState.LOAD:
            if (loadedGameData != None):
                return {'state': localGameState, 'data': loadedGameData}
            else: 
                return {'state': localGameState, 'data': currentGameData}
        #Handle Load Screen Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GameState.QUIT
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for button in buttons:
                        button.click(event)
        
        

        


def main(gameState):
    pygame.init()
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Sudoku!")

    clock = pygame.time.Clock()

    screen = pygame.display.set_mode((screen_width,screen_height))
    screenBgColor = (180, 150, 220)
    screen.fill((255,255,255))

    screenHistory = []
    gameData = None

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameState = GameState.QUIT
        
        #Back Button For Load Screen
        if gameState == GameState.PREVSTATE:
            if (len(screenHistory) < 1):
                print("Error - empty screen history")
                gameState = GameState.TITLE
            elif (len(screenHistory) < 2):
                print("Error - less than 2 screens in history")
                gameState = screenHistory.pop()
            else: 
                screenHistory.pop()
                gameState = screenHistory.pop()
        
        #Regular Screens
        if gameState == GameState.TITLE:
            screenHistory.append(GameState.TITLE)
            gameData = None
            gameState = titleScreen(screen)
        if gameState == GameState.NEWGAME:
            screenHistory.append(GameState.NEWGAME)
            gameObj = gameScreen(screen, gameData)
            gameData = gameObj['data']
            gameState = gameObj['state']
        if gameState == GameState.LOAD:
            screenHistory.append(GameState.LOAD)
            gameObj = loadScreen(screen, gameData)
            gameData = gameObj['data']
            gameState = gameObj['state']
        #Quit
        if gameState == GameState.QUIT:
            pygame.quit()
            return
        
        #Maintain small screen history list
        if (len(screenHistory) > 2):
            screenHistory = screenHistory[-2:]


if __name__=="__main__":
    main(gameState)