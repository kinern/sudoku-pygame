import pygame
from pygame.locals import *
import os
from pathlib import Path
import shelve
from enum import Enum

from alertBox import AlertBox
from button import Button
from sudokuMatrix import SudokuMatrix

screen_width = 640
screen_height = 480

class GameState(Enum):
    PREVSTATE = -2
    QUIT = -1
    TITLE = 0
    NEWGAME = 1
    LOAD = 2

class GameData:
    def __init__(self, gameMatrix, solutionMatrix, inputValues):
        self.gameMatrix = gameMatrix
        self.solutionMatrix = solutionMatrix
        self.inputValues = inputValues
    
gameState = GameState.TITLE

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

    titleImage = pygame.image.load("assets/sudoku-title.png").convert_alpha()

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
                screen.blit(m.surface, (m.x, m.y))
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

    def alertIsActive():
        active = False
        for n in alertBoxCollection:
            if (n.active):
                active = True
        return active

    while True:
        if localGameState != GameState.NEWGAME:
            return {'state':localGameState, 'data':currentGameData} #Change this
        #Handle Title Screen Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {'state': GameState.QUIT, 'data': None }
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if (alertIsActive()):
                        for alert in alertBoxCollection:
                            alert.click(event)
                    else:
                        for button in buttons:
                            button.click(event)
                    renderScreen()

            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
                for n in inputBoxCollection:
                    n.handleEvent(event)


def loadScreen(screen, currentGameData = None):

    localGameState = GameState.LOAD
    
    class saveFileBox:
        def __init__(self, num, hasSave = True, bgColor=(255,255,255) ):
            self.x = 40
            self.y = 120*num+40
            self.size = (560, 100)
            self.hasSave = hasSave
            self.selected = False
            self.num = num
            self.font = pygame.font.SysFont("Verdana", 20)
            self.uiText = "Game File "+str(num+1) if hasSave else "Empty"
            self.text = self.font.render(self.uiText, 1, (80,80,80))
            self.surface = pygame.Surface(self.size)
            self.surface.fill(bgColor)
            self.surface.blit(self.text, (int(self.size[0]/2)-int(self.text.get_rect().width/2), int(self.size[1]/2)-int(self.text.get_rect().height/2)))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        
        def render(self):
            bgColor = (255,255,255) if (self.hasSave) else (200,200,200)
            bgColor = (245, 250, 150) if (self.selected) else bgColor
            self.surface.fill(bgColor)
            self.text = self.font.render(self.uiText, 1, (80,80,80))
            self.surface.blit(self.text, (int(self.size[0]/2)-int(self.text.get_rect().width/2), int(self.size[1]/2)-int(self.text.get_rect().height/2)))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
            screen.blit(self.surface, (self.x, self.y))

        def click(self, event):
            #if (not self.hasSave): 
            #    return False
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                clearSaveSelection()
                self.selected = True
                renderSaveFiles()



    #Display files with buttons
    saveFileBoxes = []
    for n in range(3):
        fileName = "save-"+str(n+1)+".bin.dat"
        saveFile = Path(fileName)
        if (not saveFile.is_file()):
            bgColor = (200,200,200)
            hasSave = False
            newBox = saveFileBox(n,hasSave=hasSave,bgColor=bgColor)
            saveFileBoxes.append(newBox)
        else:
            newBox = saveFileBox(n)
            saveFileBoxes.append(newBox)
    
    def clearSaveSelection():
        for n in saveFileBoxes:
            n.selected = False
    
    def renderSaveFiles():
        for n in saveFileBoxes:
            n.render()
        pygame.display.flip()
    
    def saveGame():
        if (currentGameData == None):
            print("No game data to save")
            return False
        selected = False
        selectedIndex = 0
        for n in saveFileBoxes:
            if (n.selected == True):
                selected = n
                selectedIndex = n.num
        if (selected == False):
            print("No save file selected")
            return False
        gameData = shelve.open("save-"+str(selected.num+1)+".bin") 
        gameData['matrix'] = currentGameData.gameMatrix
        gameData['solutionMatrix'] = currentGameData.solutionMatrix
        gameData['inputValues'] = currentGameData.inputValues
        gameData.close()
        saveFileBoxes[selectedIndex].hasSave = True
        saveFileBoxes[selectedIndex].uiText = "Game File "+str(selected.num+1)
        print("saved data")
        renderSaveFiles()

    def deleteSave():
        selected = False
        selectedIndex = 0
        for n in saveFileBoxes:
            if ((n.selected == True) and (n.hasSave == True)):
                selected = n
                selectedIndex = n.num
        if (selected == False):
            print("No save file to delete")
            return False
        os.remove("save-"+str(selected.num+1)+".bin.bak")
        os.remove("save-"+str(selected.num+1)+".bin.dat")
        os.remove("save-"+str(selected.num+1)+".bin.dir")
        saveFileBoxes[selectedIndex].hasSave = False
        saveFileBoxes[selectedIndex].uiText = "Empty"
        print("deleted save file")
        renderSaveFiles()

    
    loadedGameData = None

    def load():
        nonlocal localGameState
        nonlocal loadedGameData

        selected = False
        selectedIndex = 0
        for n in saveFileBoxes:
            if ((n.selected == True) and (n.hasSave == True)):
                selected = n
                selectedIndex = n.num
        if (selected == False):
            print("Loadable file not selected")
            return False
        try:
            gameData = shelve.open("save-"+str(selected.num+1)+".bin") 
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


    saveBtnColor = (255,255,255) if (currentGameData != None) else (200,200,200)
    saveBtn = Button(
    "Save",
    pos=(60, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=saveBtnColor,
    onClick=saveGame)

    #Check if no loads available
    loadBtn = Button(
    "Load",
    pos=(160, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=load)

    returnBtn = Button(
    "Return",
    pos=(270, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=goBack)

    deleteBtn = Button(
    "Delete",
    pos=(380, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=deleteSave)

    quitBtn = Button(
    "Quit",
    pos=(490, 420),
    size=(80, 30),
    font=14,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=quitGame)

    buttons = [saveBtn, loadBtn, returnBtn, quitBtn, deleteBtn]

    modalBox = AlertBox(
    pos=(int(screen_width/2)-int(300/2),int(screen_height/2)-int(120/2)), 
    text="Message", 
    size=(300,120), 
    fontSize=40,
    bgColor=(255,255,255), 
    fontColor=(80,80,80)
    )

    alertBoxCollection = []

    #Render Load Screen
    screen.fill((150,200,180))
    for button in buttons:
        screen.blit(button.surface, (button.x, button.y))
    for saveFile in saveFileBoxes:
        saveFile.render()
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
                return {'state':GameState.QUIT, 'data':None}
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    if (modalBox.active):
                        modalBox.click(event)
                    else: 
                        for button in buttons:
                            button.click(event)
                        for saveFile in saveFileBoxes:
                            saveFile.click(event)
        
        
def main(gameState):
    pygame.init()
    logo = pygame.image.load("assets/logo.png")
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