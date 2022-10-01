import pygame
from pygame.locals import *
import random
import math
import copy

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


def main():
    pygame.init()
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Sudoku!")
    pygame.font.init() 
    my_font = pygame.font.SysFont('Verdana', 30)
    screen = pygame.display.set_mode((screen_width,screen_height))
    running = True
    bgColor = (180, 150, 220)

    matrix = SudokuMatrix(9, 54)

    #All input boxes
    inputBoxCollection = []
    
    #All message boxes (win, lose, no hints available)
    alertBoxCollection = []

    class InputBox():
        def __init__(self, pos, font, matrixIndex, bgColor=(255,255,255), fontColor=(0,0,0)):
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
                        if ((len(self.value) < 1) and str(event.unicode).isnumeric() and str(event.unicode) != "0" ):
                            self.value += event.unicode
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
            self.surface.blit(self.text, (10, 0))
            self.rect = pygame.Rect(self.x, self.y, self.size[0]+5, self.size[1]+5)

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
                        pos=(row*50+100, col*50+10),
                        font=30,
                        matrixIndex=[row,col],
                    )
                    newInputBox.show()
                    inputBoxCollection.append(newInputBox)
                else:
                    matrixNum = my_font.render(str(matrix.matrix[row][col]), True, (255,255,255))
                    screen.blit(matrixNum, (row*50+110,col*50+10))
    
    #Existing matrix
    def renderMatrix():
        for row in range(9):
            for col in range(9):
                if (str(matrix.matrix[row][col]) != ""):
                    matrixNum = my_font.render(str(matrix.matrix[row][col]), True, (255,255,255))
                    screen.blit(matrixNum, (row*50+110,col*50+10))
        for m in inputBoxCollection:
            m.show()

    class Button():
        def __init__(self, text,  pos, font, onClick, fontColor="White", bg="black"):
            self.x, self.y = pos
            self.font = pygame.font.SysFont("Verdana", font)
            self.onClick = onClick
            self.text = self.font.render(text, 1, pygame.Color(fontColor))
            self.size = self.text.get_size()
            self.surface = pygame.Surface(self.size)
            self.surface.fill(bg)
            self.surface.blit(self.text, (0, 0))
            self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    
        def show(self):
            screen.blit(self.surface, (self.x, self.y))
    
        def click(self, event):
            x, y = pygame.mouse.get_pos()
            if self.rect.collidepoint(x, y):
                self.onClick()

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
        pos=(170,150), 
        text="Incorrect!", 
        size=(300,120), 
        fontSize=40,
        bgColor=(255,255,255), 
        fontColor=(80,80,80)
    )

    winAlert = AlertBox(
        pos=(170,150), 
        text="You Win!", 
        size=(300,120), 
        fontSize=40, 
        bgColor=(255,255,255), 
        fontColor=(80,80,80)
    )
    alertBoxCollection.append(loseAlert)
    alertBoxCollection.append(winAlert)

    def hideAlerts():
        for n in alertBoxCollection:
            n.hide()
    
    def newGame():
        inputBoxCollection.clear()
        screen.fill(bgColor)
        matrix.generateMatrix()
        renderNewMatrix()
        newGameButton.show()
        checkButton.show()
        pygame.display.flip()

    #Render everything to screen
    def renderScreen():
        screen.fill(bgColor)
        renderMatrix()
        newGameButton.show()
        checkButton.show()
        for m in alertBoxCollection:
            if m.active:
                m.show()
        pygame.display.flip()
    
    newGameButton = Button(
    "New Game",
    (10, 10),
    font=15,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=newGame)

    checkButton = Button(
    "Check",
    (10, 50),
    font=15,
    fontColor=(80,80,80),
    bg=(255,255,255),
    onClick=checkAnswers)

    #Initial Render
    newGame()

    clock = pygame.time.Clock()

    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            #Click Only Events
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    for m in alertBoxCollection:
                        m.click(event)
                    newGameButton.click(event)
                    checkButton.click(event)
                    renderScreen()
            
            #Click And Text Entry Events
            if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN):
                for n in inputBoxCollection:
                    n.handleEvent(event)

if __name__=="__main__":
    main()