import pygame
import random
import math

screen_width = 640
screen_height = 480

class SudokuMatrix(object):
    def __init__(self, size, missingNum):
        self.size = size
        self.missingNum = missingNum
        #square root to used for diagonal sub-matrixes
        self.sqrt = math.sqrt(size)
        self.matrix = [[0 for x in range(size)] for x in range(size)]

    # main function for building matrix
    def generateMatrix():
        fillDiagonalSubMatrixes()
        fillMissingSubMatrixes()
        addMissingSquares()
        print(self.matrix)
    
    #1. fill diagonal submatrixes
    def fillDiagonalSubmatrixes():
        for a in range(0, N, self.sqrt):
            fillSubmatrix(a,a)

    #2. fill rest of submatrixes
    def fillMissingSubmatrixes():
        for a in range(0, N, self.sqrt):
            fillSubmatrix(a,a)

    #3. remove missing squares
    def addMissingSquares():
        left = self.missingNum
        while (left > 0):
            rangeMax = self.size*self.size
            cellIndex = random.randrange(0..rangeMax)
            subMatrixIndex = cellIndex / 9
            subMatrixMod = math.mod(cellIndex , 9)
            remove = random.randrange(0, 5)
            if ((remove == 0) and (self.matrix[subMatrixIndex][subMatrixMod] != 0)):
                self.matrix[subMatrixIndex][subMatrixMod] = 0
                left = left - 1

    def fillSubMatrix(row, col):
        a = [[0 for x in range(3)] for x in range(3)]
        used = []
        for n in range(3):
            for m in range(3):
                randNum = random.randrange(1,9)
                while(randNum in used):
                    randNum = random.randrange(1,9)
                self.matrix[row + n][col + m] = randNum
                used.append(randNum)

def main():
    pygame.init()
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Sudoku!")

    screen = pygame.display.set_mode((screen_width,screen_height))
    
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__=="__main__":
    main()