import pygame
from pygame.locals import *
import random
import math

screen_width = 640
screen_height = 480

class SudokuMatrix(object):
    def __init__(self, size, missingNum):
        self.size = size
        self.missingNum = missingNum
        #square root to used for diagonal sub-matrixes
        self.sqrt = int(math.sqrt(size))
        self.matrix = [[0 for x in range(size)] for x in range(size)]

    def generateMatrix(self):
        self.fillDiagonalSubmatrixes()
        self.fillMissingSubMatrixes()
        self.addMissingSquares()
        print(self.matrix)
    
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

    screen = pygame.display.set_mode((screen_width,screen_height))
    
    running = True

    bgColor = (180, 150, 220)
    screen.fill(bgColor)


    matrix = SudokuMatrix(9, 54)
    matrix.generateMatrix()

    pygame.font.init() 
    my_font = pygame.font.SysFont('Verdana', 30)
    for row in range(9):
        for col in range(9):
            if (str(matrix.matrix[row][col]) == ""):
                inputRect = Rect(row*50+100, col*50+10, 40, 40)
                pygame.draw.rect(screen, (255,255,255), inputRect)
            else:
                matrixNum = my_font.render(str(matrix.matrix[row][col]), True, (255,255,255))
                screen.blit(matrixNum, (row*50+110,col*50+10))
    pygame.display.flip()


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__=="__main__":
    main()