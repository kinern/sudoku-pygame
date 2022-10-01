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
        self.sqrt = int(math.sqrt(size))
        self.matrix = [[0 for x in range(size)] for x in range(size)]

    def generateMatrix(self):
        self.fillDiagonalSubmatrixes()
        self.fillMissingSubMatrixes(0, self.sqrt)
        #self.addMissingSquares()
        print(self.matrix)
    
    def fillDiagonalSubmatrixes(self):
        for a in range(0, self.size, self.sqrt):
            self.fillSubMatrix(a,a)

    def addMissingSquares(self):
        left = self.missingNum
        while (left > 0):
            rangeMax = int(self.size*self.size)
            cellIndex = random.randrange(0,rangeMax)
            subMatrixIndex = int(cellIndex / 9)
            subMatrixMod = int(cellIndex % 9)
            remove = random.randrange(0, 5)
            if ((remove == 0) and (self.matrix[subMatrixIndex][subMatrixMod] != 0)):
                self.matrix[subMatrixIndex][subMatrixMod] = 0
                left = left - 1

    def fillSubMatrix(self, row, col):
        for i in range(0, self.sqrt):
            for j in range(0, self.sqrt):
                num = random.randrange(1,self.size)
                while (self.unusedInBox(row, col, num) == False): 
                    num = random.randrange(1,self.size+1)
                self.matrix[row + i][col + j] = num


    def checkIfPlaceable(self, row, col, num):
        return (self.unusedInRow(row, num) and
                self.unusedInCol(col, num) and
                self.unusedInBox(row-int(row % self.sqrt), col-int(col % self.sqrt), num))
    
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


    def fillMissingSubMatrixes(self, row, col):
        print("row, col",str(row)+","+str(col))
        #Exit out of recursion if row is larger than matrix size
        if (row == self.size):
            return True
        else:
            #If at the end of the column and not the last row, recursively call next row
            if (row < self.size and col == self.size):
                self.fillMissingSubMatrixes(row+1, 0)
            else:
                #Check if cell is not filled yet
                if (self.matrix[row][col] == 0):
                    for num in range(1,10):
                        print("check:,"+str(row)+str(col)+str(num))
                        if (self.checkIfPlaceable(row, col, num)):
                            print("found")
                            #Check and add number
                            self.matrix[row][col] = num
                            self.fillMissingSubMatrixes(row, col+1)
                            return True
                    if (self.matrix[row][col] == 0):
                        self.matrix[row][col] = "ERR"
                
                #matrix cell is now (or already) filled, increment column
                self.fillMissingSubMatrixes(row, col+1)


def main():
    pygame.init()
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Sudoku!")

    screen = pygame.display.set_mode((screen_width,screen_height))
    
    running = True

    matrix = SudokuMatrix(9, 0)
    matrix.generateMatrix()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

if __name__=="__main__":
    main()